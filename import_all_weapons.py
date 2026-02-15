"""
Import ALL weapon data from alto files/weapon folders into:
1. Item model (for weapon database)
2. Copy images to media/items/weapons/<type>/
3. Generate WEAPON_CHOICES for CharacterAttributes model
"""
import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import Item
from django.conf import settings

# Mapping: folder name -> (class_name, weapon_type_key)
FOLDER_TO_CLASS = {
    'bow': ('Bow Skill', 'bow'),
    'cane': ('Staff Skill', 'cane'),
    'chainsword': ('Chainsword Skill', 'chainsword'),
    'crossbow': ('Crossbow Skill', 'crossbow'),
    'dagger': ('Dagger Skill', 'dagger'),
    'double axe': ('Dual Axe Skill', 'double_axe'),
    'greatsword': ('Greatsword Skill', 'greatsword'),
    'magic cannon': ('Magic Cannon Skill', 'magic_cannon'),
    'one handed sword': ('One-Handed Sword Skill', 'one_handed_sword'),
    'orb': ('Orb Skill', 'orb'),
    'rapier': ('Rapier Skill', 'rapier'),
    'soul breaker': ('Soul Breaker Skill', 'soul_breaker'),
    'two sword style': ('Dual-Wield Skills', 'two_sword_style'),
    'window': ('Spear Skill', 'spear'),
}

SOURCE_BASE = r"D:\Django Project\Alto Project\alto files\weapon"

# First, delete all existing WEAPON items
deleted_count = Item.objects.filter(item_type='WEAPON').delete()[0]
print(f"Deleted {deleted_count} old weapon items.")

total = 0
all_choices = {}  # weapon_type -> list of (value, label)

for folder_name, (class_name, weapon_type_key) in FOLDER_TO_CLASS.items():
    folder_path = os.path.join(SOURCE_BASE, folder_name)
    if not os.path.isdir(folder_path):
        print(f"WARNING: Folder not found: {folder_path}")
        continue
    
    # Create media target directory
    media_dir = os.path.join(settings.MEDIA_ROOT, 'items', 'weapons', weapon_type_key)
    os.makedirs(media_dir, exist_ok=True)
    
    choices_for_type = []
    
    for filename in sorted(os.listdir(folder_path)):
        if not filename.lower().endswith('.png'):
            continue
        
        item_name = os.path.splitext(filename)[0]
        
        # Copy image to media
        src = os.path.join(folder_path, filename)
        dst = os.path.join(media_dir, filename)
        shutil.copy2(src, dst)
        
        # Relative path for DB
        relative_path = f"items/weapons/{weapon_type_key}/{filename}"
        
        # Create Item in database
        Item.objects.create(
            name=item_name,
            item_type='WEAPON',
            slot=weapon_type_key,
            icon_file=relative_path,
            grade='',
        )
        
        # Build choice value: "weapon_type|weapon_name"
        choice_value = f"{weapon_type_key}|{item_name}"
        choices_for_type.append((choice_value, item_name))
        
        total += 1
    
    all_choices[weapon_type_key] = choices_for_type
    print(f"{class_name} ({folder_name}): {len(choices_for_type)} weapons imported")

print(f"\nTotal weapons imported: {total}")

# Generate Python code for WEAPON_CHOICES
print("\n\n=== GENERATED WEAPON_CHOICES ===")
print("WEAPON_CHOICES = [")
print("    ('', 'No weapon selected'),")
for weapon_type, choices in sorted(all_choices.items()):
    for value, label in choices:
        print(f"    ('{value}', '{label}'),")
print("]")

# Generate CLASS_TO_WEAPONS mapping
print("\n\n=== GENERATED CLASS_TO_WEAPONS MAPPING ===")
print("CLASS_TO_WEAPON_TYPE = {")
for folder_name, (class_name, weapon_type_key) in sorted(FOLDER_TO_CLASS.items(), key=lambda x: x[1][0]):
    print(f"    '{class_name}': '{weapon_type_key}',")
print("}")
