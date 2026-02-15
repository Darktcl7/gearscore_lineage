import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin superuser if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created admin superuser: admin / admin123")
else:
    print("Admin user already exists")

# Create regular user if not exists
if not User.objects.filter(username='player1').exists():
    User.objects.create_user('player1', 'player1@example.com', 'player123')
    print("Created regular user: player1 / player123")
else:
    print("Player1 user already exists")
