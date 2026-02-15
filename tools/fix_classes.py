import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import Character

print("Checking Character Classes...")
chars = Character.objects.all()
for c in chars:
    print(f"Name: {c.name}, Level: {c.level}, Class: '{c.character_class}'")
    if not c.character_class:
        print(f"  -> FIXING empty class for {c.name} to 'Spear'")
        c.character_class = 'Spear'
        c.save()

print("Done.")
