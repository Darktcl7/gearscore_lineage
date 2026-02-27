import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

from items.models import Item

# Show all items by type with their icons to find duplicates
target_types = ['Helmet', 'Armor', 'Gloves', 'Boots', 'Cloak', 'Sigil', 'Pants', 'Torso', 'T-Shirt']

for t in target_types:
    items = Item.objects.filter(item_type=t).order_by('id')
    print(f"\n=== {t} ({items.count()}) ===")
    for i in items:
        old = "OLD" if not i.icon_file.startswith("choices/") else "NEW"
        print(f"  [{i.id}] {i.name} | {old} | {i.icon_file}")
