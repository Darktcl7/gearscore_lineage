import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from items.models import Character

# Get admin user
admin = User.objects.get(username='admin')
player1 = User.objects.get(username='player1')

# Assign all existing characters without owner to admin
chars_updated = Character.objects.filter(owner__isnull=True).update(owner=admin)
print(f"Assigned {chars_updated} characters to admin")

# Assign character ID 7 to player1 for testing
try:
    char7 = Character.objects.get(pk=7)
    char7.owner = player1
    char7.save()
    print(f"Assigned character '{char7.name}' (ID 7) to player1")
except Character.DoesNotExist:
    print("Character ID 7 not found")
