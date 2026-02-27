import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

from items.models import Item

# 1. Delete old "Icon Ar ..." duplicate items
old_items = Item.objects.filter(name__startswith="Icon Ar ")
count = old_items.count()
print(f"Deleting {count} old 'Icon Ar ...' items...")
old_items.delete()
print(f"Done deleting.")

# 2. Add T-Shirt as a new item_type choice and create t-shirt items
tshirt_items = [
    ("Agility's Anonymous Shirt", "choices/armor_tshirt_Agility's_anonymous_shirt.png"),
    ("Anonymous Shirt of Knowledge", "choices/armor_tshirt_Anonymous_Shirt_of_Knowledge.png"),
    ("Anonymous Shirt of Strength", "choices/armor_tshirt_Anonymous_shirt_of_strength.png"),
    ("Focus Shirt", "choices/armor_tshirt_Focus_Shirt.png"),
    ("Mithril Shirt of Agility", "choices/armor_tshirt_Mithril_Shirt_of_Agility.png"),
    ("Mithril Shirt of Knowledge", "choices/armor_tshirt_Mithril_Shirt_of_Knowledge.png"),
    ("Mithril Shirt of Strength", "choices/armor_tshirt_Mithril_Shirt_of_Strength.png"),
    ("Vigilante Shirt", "choices/armor_tshirt_Vigilante_Shirt.png"),
    ("Warrior's T-shirt", "choices/armor_tshirt_Warrior's_T-shirt.png"),
]

for name, icon in tshirt_items:
    obj, created = Item.objects.get_or_create(
        name=name,
        defaults={
            'item_type': 'T-Shirt',
            'icon_file': icon,
            'enchant_level': 0,
            'grade': 'Epic',
        }
    )
    status = "CREATED" if created else "EXISTS"
    print(f"  T-Shirt: {name} -> {status}")

# 3. Also create new armor items that are missing (from new armor folder)
# Helmet new items
new_helmets = [
    ("Crown of the World Tree", "choices/armor_helmet_Crown_of_the_World_Tree.png"),
    ("Devil's Helmet", "choices/armor_helmet_Devil's_Helmet.png"),
    ("Hildegrim", "choices/armor_helmet_Hildegrim.png"),
    ("Helmet of the Fallen Angel", "choices/armor_helmet_Helmet_of_the_Fallen_Angel.png"),
]
for name, icon in new_helmets:
    obj, created = Item.objects.get_or_create(name=name, defaults={'item_type': 'Helmet', 'icon_file': icon, 'enchant_level': 0, 'grade': 'Legendary'})
    if created: print(f"  Helmet: {name} -> CREATED")

# Armor new items
new_armors = [
    ("Breastplate of the Fallen Angel", "choices/armor_armor_Breastplate_of_the_Fallen_Angel.png"),
    ("Breastplate of the Forgotten Hero", "choices/armor_armor_Breastplate_of_the_Forgotten_Hero.png"),
    ("Devil's Armor", "choices/armor_armor_Devil's_Armor.png"),
]
for name, icon in new_armors:
    obj, created = Item.objects.get_or_create(name=name, defaults={'item_type': 'Armor', 'icon_file': icon, 'enchant_level': 0, 'grade': 'Legendary'})
    if created: print(f"  Armor: {name} -> CREATED")

# Gloves new items
new_gloves = [
    ("Fallen Angel's Gloves", "choices/armor_gloves_Fallen_Angel's_Gloves.png"),
    ("Pa'agrio's Flame", "choices/armor_gloves_Paagrio's_Flame.png"),
]
for name, icon in new_gloves:
    obj, created = Item.objects.get_or_create(name=name, defaults={'item_type': 'Gloves', 'icon_file': icon, 'enchant_level': 0, 'grade': 'Legendary'})
    if created: print(f"  Gloves: {name} -> CREATED")

# Boots new items
new_boots = [
    ("Fallen Angel's Boots", "choices/armor_shoes_Fallen_Angel's_Boots.png"),
    ("Reaper's Boots", "choices/armor_shoes_Reaper's_Boots.png"),
    ("Boots of Eternal Life", "choices/armor_shoes_Boots_of_Eternal_Life.png"),
]
for name, icon in new_boots:
    obj, created = Item.objects.get_or_create(name=name, defaults={'item_type': 'Boots', 'icon_file': icon, 'enchant_level': 0, 'grade': 'Legendary'})
    if created: print(f"  Boots: {name} -> CREATED")

# Cloak new items  
new_cloaks = [
    ("Cloak of Verdant Green", "choices/armor_cloak_Cloak_of_Verdant_Green.png"),
    ("Mantle of the Holy Spirit", "choices/armor_cloak_Mantle_of_the_Holy_Spirit.png"),
    ("Salamander's Cloak", "choices/armor_cloak_Salamander's_Cloak.png"),
    ("Moonlight's Cloak", "choices/armor_cloak_Moonlight's_Cloak.png"),
    ("Cranbel's Cloak", "choices/armor_cloak_Cranbel's_Cloak.png"),
    ("Jaqen's Cloak", "choices/armor_cloak_Jaqen's_Cloak.png"),
]
for name, icon in new_cloaks:
    obj, created = Item.objects.get_or_create(name=name, defaults={'item_type': 'Cloak', 'icon_file': icon, 'enchant_level': 0, 'grade': 'Legendary'})
    if created: print(f"  Cloak: {name} -> CREATED")

# Sigil new items
new_sigils = [
    ("Holy Sigil", "choices/armor_sigil_Holy_Sigil.png"),
    ("Blood Crystal", "choices/armor_sigil_Blood_Crystal.png"),
    ("Crystal of Oblivion", "choices/armor_sigil_Crystal_of_Oblivion.png"),
    ("Eldarach", "choices/armor_sigil_Eldarach.png"),
    ("Sigil of the Fallen Angel", "choices/armor_sigil_The_Sigil_of_the_Fallen_Angel.png"),
    ("Sigil of Karma", "choices/armor_sigil_The_sigil_of_karma.png"),
    ("Sniper Sigil", "choices/armor_sigil_Sniper_Sigil.png"),
]
for name, icon in new_sigils:
    obj, created = Item.objects.get_or_create(name=name, defaults={'item_type': 'Sigil', 'icon_file': icon, 'enchant_level': 0, 'grade': 'Legendary'})
    if created: print(f"  Sigil: {name} -> CREATED")

# Bottoms new items
new_bottoms = [
    ("Fallen Angel's Legguards", "choices/armor_bottoms_Fallen_Angel's_Legguards.png"),
    ("Full Plate Gaiters", "choices/armor_bottoms_Full_plate_gaiters.png"),
    ("Flame Greaves", "choices/armor_bottoms_Flame_Greaves.png"),
    ("Spirit's Greaves", "choices/armor_bottoms_Spirit's_Greaves.png"),
    ("Patience Leggings", "choices/armor_bottoms_Patience_Leggings.png"),
    ("Devil's Pact", "choices/armor_bottoms_Devil's_Pact.png"),
]
for name, icon in new_bottoms:
    obj, created = Item.objects.get_or_create(name=name, defaults={'item_type': 'Pants', 'icon_file': icon, 'enchant_level': 0, 'grade': 'Legendary'})
    if created: print(f"  Pants: {name} -> CREATED")

print("\nAll done!")

# Print summary
for t in ['Helmet', 'Armor', 'Gloves', 'Boots', 'Cloak', 'Sigil', 'Pants', 'T-Shirt']:
    c = Item.objects.filter(item_type=t).count()
    print(f"  {t}: {c} items")
