import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import Character

def check_char_equipment(pk):
    print(f"\n--- Checking Equipment Character ID {pk} ---")
    try:
        char = Character.objects.get(pk=pk)
        print(f"Main Weapon: {char.main_weapon}")  
        # If any foreign key is problematic, accessing it might trigger error or return None
        print(f"Helmet: {char.helmet}")
        print(f"Armor: {char.armor}")
        print(f"Gloves: {char.gloves}")
        print(f"Boots: {char.boots}")
        
    except Character.DoesNotExist:
        print("Character NOT FOUND.")
    except Exception as e:
        print(f"ERROR accessing equipment: {e}")

check_char_equipment(8)
