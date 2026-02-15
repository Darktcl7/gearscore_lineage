import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from items.models import Character

# Get users
admin = User.objects.get(username='admin')
player1 = User.objects.get(username='player1')

# Assign SonOfZeus (ID 7) to admin
try:
    char7 = Character.objects.get(pk=7)
    char7.owner = admin
    char7.save()
    print(f"Assigned character '{char7.name}' (ID 7) to admin")
except Character.DoesNotExist:
    print("Character ID 7 not found")

# Assign all characters without owner to admin
chars_updated = Character.objects.filter(owner__isnull=True).update(owner=admin)
print(f"Assigned {chars_updated} orphan characters to admin")

# List all characters with owners
print("\nAll characters:")
for c in Character.objects.all():
    owner_name = c.owner.username if c.owner else "None"
    print(f"  - {c.name} (ID {c.pk}): owner={owner_name}")
