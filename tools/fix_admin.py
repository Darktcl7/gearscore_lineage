import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Check admin user
try:
    admin = User.objects.get(username='admin')
    print(f"Admin found: is_staff={admin.is_staff}, is_superuser={admin.is_superuser}")
    
    # Fix admin to have superuser rights
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print("Admin updated: is_staff=True, is_superuser=True")
except User.DoesNotExist:
    # Create new admin
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created new admin superuser")

# List all users
print("\nAll users:")
for u in User.objects.all():
    print(f"  - {u.username}: is_staff={u.is_staff}, is_superuser={u.is_superuser}")
