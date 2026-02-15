# D:\Django Project\Alto Project\myproject\urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.http import HttpResponseForbidden

# Custom logout view that accepts GET
def logout_view(request):
    logout(request)
    return redirect('login')

# Custom Authentication Form: show "pending approval" for inactive users
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class CustomAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "Your account is pending approval from an admin. Please wait.",
                code='inactive',
            )

# Custom login view
class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthForm

    def get_success_url(self):
        return '/portal/profiles/'


# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        errors = []
        
        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username is already taken.')
        
        if not password1:
            errors.append('Password is required.')
        elif len(password1) < 4:
            errors.append('Password must be at least 4 characters.')
        elif password1 != password2:
            errors.append('Passwords do not match.')
        
        if errors:
            return render(request, 'registration/register.html', {
                'errors': errors,
                'form_data': {'username': username},
            })
        
        # Create user with is_active=False (needs admin approval)
        user = User.objects.create_user(username=username, password=password1)
        user.is_active = False
        user.save()
        
        return render(request, 'registration/register.html', {'success': True})
    
    return render(request, 'registration/register.html')


# Admin: Approve user
@login_required(login_url='/login/')
def approve_user(request, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Admin only.")
    target = get_object_or_404(User, pk=user_id)
    target.is_active = True
    target.save()
    return redirect('character-management')


# Admin: Reject (delete) user
@login_required(login_url='/login/')
def reject_user(request, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Admin only.")
    target = get_object_or_404(User, pk=user_id)
    if not target.is_staff:  # Safety: never delete admin/staff
        target.delete()
    return redirect('character-management')


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    
    # Admin user approval
    path('portal/manage/approve-user/<int:user_id>/', approve_user, name='approve-user'),
    path('portal/manage/reject-user/<int:user_id>/', reject_user, name='reject-user'),
    
    # Redirect the root URL '/' to the new portal
    path('', RedirectView.as_view(url='/portal/profiles/', permanent=False), name='index'),
    
    # NEW: DKP System (standalone) -> /dkp/
    path('dkp/', include('dkp.urls')),

    # NEW: Main Game Portal (Renamed from items) -> /portal/
    path('portal/', include('items.urls')),
]

# Serve static files during development
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
    # This helper function specifically serves static files in debug mode
    urlpatterns += staticfiles_urlpatterns()
    
    # Also add manual serving just in case
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
