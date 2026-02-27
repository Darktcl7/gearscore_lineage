import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

from items.models import Item

# Check current PvP equipment types
for item_type in ['Helmet', 'Armor', 'Gloves', 'Boots']:
    items = Item.objects.filter(item_type=item_type)
    print(f"\n=== {item_type} ({items.count()}) ===")
    for item in items:
        print(f"  [{item.id}] {item.name} | icon: {item.icon_file}")

# Check what other item_types exist
print("\n=== All item_types ===")
types = Item.objects.values_list('item_type', flat=True).distinct()
for t in types:
    count = Item.objects.filter(item_type=t).count()
    print(f"  {t}: {count}")
