"""
Batch Update Script Part 2: FORMS & EXTRAS
Updates forms.py and item_extras.py for remaining PVP items.
"""

# === 1. FORMS ===
path = r"D:\Django Project\Alto Project\items\forms.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace RadioSelect with Select for all items
items = ['pvp_sigil', 'pvp_helmet', 'pvp_gloves', 'pvp_boots', 'pvp_gaiters', 'pvp_armor', 'pvp_cloak']
for item in items:
    content = content.replace(f"'{item}': forms.RadioSelect,", f"'{item}': forms.Select,")
    print(f"Updated widget for {item}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("forms.py saved.")


# === 2. ITEM EXTRAS ===
path = r"D:\Django Project\Alto Project\items\templatetags\item_extras.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update is_weapon_field filter
new_filter_items = [
    'weapon', 'weapon_enchant',
    'pvp_belt', 'pvp_belt_enchant',
    'pvp_ring_left', 'pvp_ring_left_enchant',
    'pvp_ring_right', 'pvp_ring_right_enchant',
    'pvp_necklace', 'pvp_necklace_enchant',
    'pvp_sigil', 'pvp_sigil_enchant',
    'pvp_helmet', 'pvp_helmet_enchant',
    'pvp_gloves', 'pvp_gloves_enchant',
    'pvp_boots', 'pvp_boots_enchant',
    'pvp_gaiters', 'pvp_gaiters_enchant',
    'pvp_armor', 'pvp_armor_enchant',
    'pvp_cloak', 'pvp_cloak_enchant'
]
filter_str = ", ".join([f"'{item}'" for item in new_filter_items])
new_filter_code = f"    return field_name in ({filter_str})"
# Regex replacement for the return line
import re
content = re.sub(r"return field_name in \([^\)]+\)", new_filter_code, content)
print("Updated is_weapon_field filter")

# Add Mappings
# We need to find the end of the mapping dict and append new mappings
# Look for the last known mapping or end of dict
# We'll just append before the last known mapping block or similar marker

mapping_code = '''
        # === BATCH ADDED MAPPINGS ===
        # SIGIL
        "Dream Sigil": "Icon_AR_Sigil_G4_001.png",
        "Susceptor's Heart": "Icon_AR_Sigil_G3_001.png",
        "Paradia's Sigil": "Icon_AR_Sigil_G3_002.png",
        "Cruma's Shell": "Icon_AR_Sigil_G3_003.png",
        "Sigil of Flames": "Icon_AR_Sigil_G3_004.png",
        "Jaeger's Sigil": "Icon_AR_Sigil_G3_005.png",
        "Selihoden's Horn": "Icon_AR_Sigil_G3_006.png",
        
        # HELMET
        "Blue Wolf Helmet": "Icon_AR_Helmet_G3_006.png",
        "Majestic Circlet": "Icon_AR_Helmet_G3_001.png",
        "Helm of Nightmares": "Icon_AR_Helmet_G3_002.png",
        "Dark Crystal Helmet": "Icon_AR_Helmet_G3_003.png",
        "Medusa's Helm": "Icon_AR_Helmet_G3_004.png",
        "Paulina's Helmet": "Icon_AR_Helmet_G3_005.png",
"Nevit's Helmet": "Icon_AR_Helmet_G3_007.png",
        "Tersi's Circlet": "Icon_AR_Helmet_G3_009.png",
        "Ancient Elven Helm": "Icon_AR_Helmet_G2_002.png",
        "Imperial Crusader Helmet": "Icon_AR_Helmet_G3_009.png",
        "Major Arcana Circlet": "Icon_AR_Helmet_G3_009.png",
        "Draconic Helmet": "Icon_AR_Helmet_G3_009.png",

        # GLOVES
        "Blue Wolf Gloves": "Icon_AR_Gloves_G3_006.png",
        "Majestic Gloves": "Icon_AR_Gloves_G3_001.png",
        "Gauntlets of Nightmare": "Icon_AR_Gloves_G3_002.png",
        "Dark Crystal Gloves": "Icon_AR_Gloves_G3_003.png",
        "Tersi's Gloves": "Icon_AR_Gloves_G3_008.png",
        "Paulina's Gauntlets": "Icon_AR_Gloves_G3_005.png",
        "Nevit's Gloves": "Icon_AR_Gloves_G3_007.png",
        "Jarngreipr": "Icon_AR_Gloves_G3_004.png",
        "Vision Guardian": "Icon_AR_Gloves_G3_009.png",
        "Gloves of Blessing": "Icon_AR_Gloves_G2_003.png",
        "Forgotten Hero Gloves": "Icon_AR_Gloves_G3_010.png",
        "Demon's Gauntlets": "Icon_AR_Gloves_G2_001.png",
        "Ancient Elven Gauntlet": "Icon_AR_Gloves_G2_002.png",
        "Draconic Leather Gloves": "Icon_AR_Gloves_G3_011.png",
        "Pa'agrio's Flames": "Icon_AR_Gloves_G3_012.png",

        # BOOTS
        "Blue Wolf Boots": "Icon_AR_Boots_G3_006.png",
        "Majestic Boots": "Icon_AR_Boots_G3_001.png",
        "Boots of Nightmares": "Icon_AR_Boots_G3_002.png",
        "Dark Crystal Boots": "Icon_AR_Boots_G3_003.png",
        "Tersi's Boots": "Icon_AR_Boots_G3_008.png",
        "Paulina's Boots": "Icon_AR_Boots_G3_005.png",
        "Nevit's Boots": "Icon_AR_Boots_G3_007.png",
        "Demon's Boots": "Icon_AR_Boots_G2_001.png",
        "Kaliel's Boots": "Icon_AR_Boots_G2_004.png",
        "Forgotten Hero's Boots": "Icon_AR_Boots_G3_009.png",
        "Ancient Elven Boots": "Icon_AR_Boots_G2_002.png",
        "Draconic": "Icon_AR_Boots_G3_010.png",
        "Sayha's Wind": "Icon_AR_Boots_G3_011.png",

        # GAITERS
        "Blue Wolf Gaiters": "Icon_AR_Pants_G3_006.png",
        "Basila Skin": "Icon_AR_Pants_G3_008.png",
        "Blood Gaiters": "Icon_AR_Pants_G3_001.png",
        "Gaiters of Light": "Icon_AR_Pants_G3_002.png",
        "Gaiters of Ice": "Icon_AR_Pants_G3_003.png",
        "Shilen's Breath": "Icon_AR_Pants_G3_004.png",
        "Crystal Gaiters": "Icon_AR_Pants_G3_005.png",
        "Forgotten Hero's Gaiters": "Icon_AR_Pants_G3_007.png",
        "Imperial Crusader Gaiters": "Icon_AR_Pants_G3_009.png",

        # ARMOR
        "Blue Wolf Breastplate": "Icon_AR_Torso_G3_006.png",
        "Majestic Robe": "Icon_AR_Torso_G3_001.png",
        "Armor of Nightmares": "Icon_AR_Torso_G3_002.png",
        "Dark Crystal Breastplate": "Icon_AR_Torso_G3_003.png",
        "Tersi's Robe": "Icon_AR_Torso_G3_008.png",
        "Paulina's Breastplate": "Icon_AR_Torso_G3_005.png",
        "Nevit's Armor": "Icon_AR_Torso_G3_007.png",
        "Savan's Robe": "Icon_AR_Torso_G3_004.png",
        "Absolute Tunic": "Icon_AR_Torso_G2_003.png",
        "Apella Plate Armor": "Icon_AR_Torso_G2_004.png",
        "Forgotten Hero's Breastplate": "Icon_AR_Torso_G3_009.png",
        "Ancient Elven Armor": "Icon_AR_Torso_G2_002.png",
        "Demon's Armor": "Icon_AR_Torso_G2_001.png",
        "Draconic Leather Armor": "Icon_AR_Torso_G3_011.png",
        "Major Arcana Robe": "Icon_AR_Torso_G3_012.png",
        "Imperial Crusader Breastplate": "Icon_AR_Torso_G3_010.png",

        # CLOAK
        "Silver Cloak": "Icon_AR_Cape_G3_001.png",
        "Cranigg's Cloak": "Icon_AR_Cape_G3_002.png",
        "Dragon's Scale": "Icon_AR_Cape_G3_003.png",
        "Zaken's Cloak": "Icon_AR_Cape_G3_004.png",
        "Cloak of Freya": "Icon_AR_Cape_G3_005.png",
        "Queen Ant's Wing": "Icon_AR_Cape_G3_006.png (check suffix)",
        "Cloak of Silence": "Icon_AR_Cape_G3_007.png",
        "Eigis Cloak": "Icon_AR_Cape_G3_008.png",
        "Cloak of Authority": "Icon_AR_Cape_G3_007.png", # Duplicate icon in original mapping?
        "Selihoden's Wing": "Icon_AR_Cape_G3_008.png", # Duplicate icon in original mapping?
        "Nevit's Cloak of Light": "Icon_AR_Cape_G2_001.png",
        "Nailop's Cloak": "Icon_AR_Cape_G2_002.png",
'''

# Use replace on a known safe string to insert
# Inserting before WEAPONS section
search_str = "# WEAPONS (from Subclass Information_files)"
if search_str in content:
    content = content.replace(search_str, mapping_code + "\n        " + search_str)
    print("Added mappings")
else:
    print("WARNING: Could not find mapping insertion point")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("item_extras.py saved.")
