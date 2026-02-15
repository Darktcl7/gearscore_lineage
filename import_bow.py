import os
import shutil
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import Item
from django.conf import settings

# Source folder
SOURCE_DIR = r"D:\Django Project\Alto Project\alto files\lineage2\bow_files"

# Target Media folder
# Pastikan folder media/items/bow ada
MEDIA_ITEMS_DIR = os.path.join(settings.MEDIA_ROOT, 'items', 'bow')
os.makedirs(MEDIA_ITEMS_DIR, exist_ok=True)

print(f"Scanning {SOURCE_DIR}...")

count = 0
for filename in os.listdir(SOURCE_DIR):
    # Filter hanya file PNG dan abaikan file sistem/sampah
    if filename.lower().endswith('.png') and 'l2m-game-grade' not in filename:
        item_name = os.path.splitext(filename)[0]
        
        # Abaikan jika masih nama file lama (Icon_WP...) - Jaga-jaga
        if filename.startswith('Icon_WP'):
            print(f"Skipping old filename: {filename}")
            continue

        # Copy file ke media folder
        src_path = os.path.join(SOURCE_DIR, filename)
        dst_path = os.path.join(MEDIA_ITEMS_DIR, filename)
        shutil.copy2(src_path, dst_path)
        
        # Path relatif untuk disimpan di database
        relative_path = f"items/bow/{filename}"
        
        # Create Item
        # Cek apakah item sudah ada untuk menghindari duplikat (walau tadi sudah dihapus)
        item, created = Item.objects.get_or_create(
            name=item_name,
            defaults={
                'item_type': 'WEAPON',
                'slot': 'BOW',
                'icon_file': relative_path,
                'grade': 'Unknown',
                'attack_power': 0,
                'defense_power': 0
            }
        )
        
        if created:
            print(f"Imported: {item_name}")
            count += 1
        else:
            # Update icon path jika item sudah ada
            item.icon_file = relative_path
            item.slot = 'BOW'
            item.item_type = 'WEAPON'
            item.save()
            print(f"Updated: {item_name}")
            count += 1

print(f"Total Processed: {count}")
