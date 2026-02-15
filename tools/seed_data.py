import os
import django
import random

# --- Setup Django Environment ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import (
    Item, Character, BonusStats, SubclassStats, LegendaryClass, 
    CharacterAttributes, LegendaryAgathion, InheritorBook
)

# --- Data Definitions ---
LEGENDARY_CLASSES_DATA = [
    {"name": "Demon Slayer", "icon_file": "Zariche.png"},
    {"name": "Scryde", "icon_file": "Icon_Classcard_Scryde.png"},
    {"name": "Lionel Hunter", "icon_file": "Icon_Classcard_LionelHunter.png"},
    {"name": "Aria", "icon_file": "Icon_Classcard_Aria.png"},
    {"name": "Veora", "icon_file": "Icon_Classcard_Veora.png"},
    {"name": "Solina", "icon_file": "Icon_Classcard_Solina.png"},
    {"name": "Regina", "icon_file": "Icon_Classcard_Regina.png"},
    {"name": "Daphne", "icon_file": "Icon_Classcard_Daphne.png"},
    {"name": "No legendary class", "icon_file": "вопрос_PiWb3ob.png"}, # Placeholder icon
]

LEGENDARY_AGATHIONS_DATA = [
    {"name": "No legendary agathions", "icon_file": "вопрос_PiWb3ob.png"}, # Placeholder icon
    {"name": "Zarich", "icon_file": "Icon_Agathion_Zariche.png"},
    {"name": "Orfen", "icon_file": "Icon_Agathion_Orfen.png"},
    {"name": "Baium", "icon_file": "Icon_Agathion_Baium.png"},
    {"name": "Anakim", "icon_file": "Icon_Agathion_Anakim.png"},
    {"name": "Lilith", "icon_file": "Icon_Agathion_Lilith.png"},
    {"name": "Timiniel", "icon_file": "Icon_Agathion_Timiniel.png"},
]
INHERITOR_BOOKS_DATA = [
    "Increase Strength", "Increase Dexterity", "Increase Intelligence", # ... (omitted for brevity)
]

def parse_slot_from_name(filename):
    name = filename.lower()
    if 'helmet' in name: return 'Helmet'
    if 'glove' in name: return 'Gloves'
    if 'boot' in name: return 'Boots'
    if 'torso' in name or 'pants' in name: return 'Armor'
    if 'weapon' in name or 'spear' in name: return 'Weapon'
    if 'necklace' in name or 'ring' in name or 'earring' in name: return 'Accessory'
    return 'Misc'

def parse_grade_from_name(filename):
    parts = filename.split('_')
    for part in parts:
        if part.startswith('G') and len(part) == 2 and part[1].isdigit():
            return part
    return 'Common'

def run_seed():
    print("--- Starting database seeding process ---")

    # --- 1. Clear Existing Data ---
    print("Deleting all old data...")
    Character.objects.all().delete()
    Item.objects.all().delete()
    LegendaryClass.objects.all().delete()
    LegendaryAgathion.objects.all().delete()
    InheritorBook.objects.all().delete()
    print("Old data cleared.")

    # --- 2. Create Static Data ---
    print("\n--- Creating static choice data ---")
    created_legendary_classes = [LegendaryClass.objects.create(**data) for data in LEGENDARY_CLASSES_DATA]
    created_agathions = [LegendaryAgathion.objects.create(**data) for data in LEGENDARY_AGATHIONS_DATA]
    created_books = [InheritorBook.objects.create(name=name) for name in INHERITOR_BOOKS_DATA]
    print(f"Created {len(created_legendary_classes)} Legendary Classes, {len(created_agathions)} Agathions, {len(created_books)} Books.")

    # --- 3. Create Items ---
    print("\n--- Creating new Items from icon files ---")
    image_dir = os.path.join('items', 'static', 'items', 'img')
    icon_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]
    
    created_items = []
    for filename in icon_files:
        item_name = os.path.splitext(filename)[0].replace('_', ' ').title()
        item_slot = parse_slot_from_name(filename)
        item_grade = parse_grade_from_name(filename)
        
        if item_slot == 'Misc': continue

        item = Item.objects.create(
            name=item_name,
            item_type=item_slot,
            icon_file=filename,
            enchant_level=random.randint(3, 8),
            grade=item_grade,
            slot=item_slot,
            attack_power=random.randint(10, 100) * (int(item_grade[1]) if item_grade != 'Common' else 1),
            defense_power=random.randint(10, 100) * (int(item_grade[1]) if item_grade != 'Common' else 1)
        )
        created_items.append(item)
    print(f"--- {len(created_items)} items created successfully. ---")

    # --- 4. Create a Sample Character ---
    print("\n--- Creating a sample character ---")
    if not created_items:
        print("No items were created, cannot create a character.")
        return

    char = Character.objects.create(name="SonOfZeus", level=91, character_class="Spear", clan="Valkyrie")
    print(f"Character '{char.name}' created.")

    # --- 5. Assign M2M Relationships ---
    print("\n--- Assigning M2M relationships ---")
    char.legendary_classes.set(created_legendary_classes[:3])
    char.legendary_agathions.set(created_agathions[:2])
    print(f"Assigned Legendary Classes and Agathions.")
    
    # --- 6. Create and Assign Attributes ---
    print("\n--- Creating Attributes ---")
    attrs = CharacterAttributes.objects.create(
        character=char,
        epic_classes_count='10-19',
        epic_agathions_count='5-9',
        soulshot_level='8',
        valor_level='7',
        enchant_bracelet_holy_prot=5,
        enchant_earring_fire=6,
    )
    attrs.inheritor_books.set(created_books[:5])
    print("Created and assigned attributes, including inheritor books.")

    # --- 7. Equip Items to the Character ---
    print("\n--- Equipping items to the character ---")
    def equip_item(slot_name, field_name):
        item_to_equip = next((item for item in created_items if item.slot == slot_name), None)
        if item_to_equip:
            setattr(char, field_name, item_to_equip)
            print(f"Equipped {slot_name}: {item_to_equip.name}")

    equip_item('Weapon', 'main_weapon')
    equip_item('Helmet', 'helmet')
    equip_item('Armor', 'armor')
    equip_item('Gloves', 'gloves')
    equip_item('Boots', 'boots')
    equip_item('Accessory', 'necklace')
    equip_item('Accessory', 'ring_left')
    right_ring = next((item for item in created_items if item.slot == 'Accessory' and item != char.ring_left), None)
    if right_ring: char.ring_right = right_ring

    char.save()
    print("\nCharacter saved with equipped items.")

    print("\n--- Database seeding complete! ---")

if __name__ == '__main__':
    run_seed()