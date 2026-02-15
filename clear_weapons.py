import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import Item

# Hapus semua item dengan tipe Weapon
weapon_count = Item.objects.filter(category='WEAPON').count()
Item.objects.filter(category='WEAPON').delete()

print(f"Deleted {weapon_count} weapons.")
