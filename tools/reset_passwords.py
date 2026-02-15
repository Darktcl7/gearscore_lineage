import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Reset admin password
try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print("Admin password reset to: admin123")
except User.DoesNotExist:
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created admin with password: admin123")

# Reset player1 password  
try:
    player1 = User.objects.get(username='player1')
    player1.set_password('player123')
    player1.save()
    print("Player1 password reset to: player123")
except User.DoesNotExist:
    player1 = User.objects.create_user('player1', 'player1@example.com', 'player123')
    print("Created player1 with password: player123")

print("\n=== CREDENTIALS ===")
print("Admin: admin / admin123")
print("Player1: player1 / player123")
