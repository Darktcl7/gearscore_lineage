import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from items.models import Character

def check_char(pk):
    print(f"\n--- Checking Character ID {pk} ---")
    try:
        char = Character.objects.get(pk=pk)
        print(f"Name: {char.name}")
        print(f"Owner: {char.owner} (ID: {char.owner.id if char.owner else 'None'})")
        print(f"Level: {char.level}")
        print(f"Class: '{char.character_class}'")
        print(f"Clan: '{char.clan}'")
        
        # Check if class is valid
        from items.models import CLASS_CHOICES, CLAN_CHOICES
        valid_classes = [c[0] for c in CLASS_CHOICES]
        if char.character_class not in valid_classes:
            print(f"WARNING: Class '{char.character_class}' is NOT in CLASS_CHOICES!")
            print(f"Valid choices: {valid_classes}")

        valid_clans = [c[0] for c in CLAN_CHOICES]
        # Clan can be blank if field allows it, but let's see.
        if char.clan and char.clan not in valid_clans:
             print(f"WARNING: Clan '{char.clan}' is NOT in CLAN_CHOICES!")

    except Character.DoesNotExist:
        print("Character NOT FOUND.")

check_char(7)
check_char(8)
