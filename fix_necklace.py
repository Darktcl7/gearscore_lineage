"""
Script to update PVP Necklace to use base names + separate enchant field.
Updates: models.py, forms.py, item_extras.py, character_form.html
"""

# ============================================
# 1. UPDATE models.py - PVP_NECKLACE_CHOICES + add enchant field
# ============================================
path = r"D:\Django Project\Alto Project\items\models.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define old and new choices
old_necklace_choices = '''PVP_NECKLACE_CHOICES = [

    ("Blue necklace +3-4", "Blue necklace +3-4"),

    ("Blue necklace +5+", "Blue necklace +5+"),

    ("Blue (other) and lower", "Blue (other) and lower"),

    ("Necklace of Immortality +0", "Necklace of Immortality +0"),

    ("Necklace of Immortality +1-3", "Necklace of Immortality +1-3"),

    ("Necklace of Immortality +4+", "Necklace of Immortality +4+"),

    ("Lilith's Soul Necklace +0", "Lilith's Soul Necklace +0"),

    ("Lilith's Soul Necklace +1-3", "Lilith's Soul Necklace +1-3"),

    ("Lilith's Soul Necklace +4+", "Lilith's Soul Necklace +4+"),

    ("Anakeem's Soul Necklace +0", "Anakeem's Soul Necklace +0"),

    ("Anakeem's Soul Necklace +1-3", "Anakeem's Soul Necklace +1-3"),

    ("Anakeem's Soul Necklace +4+", "Anakeem's Soul Necklace +4+"),

    ("Baium's Necklace +0", "Baium's Necklace +0"),

    ("Baium's Necklace +1-3", "Baium's Necklace +1-3"),

    ("Baium's Necklace +4+", "Baium's Necklace +4+"),

    ("Zaken's Necklace +0", "Zaken's Necklace +0"),

    ("Zaken's Necklace +1-3", "Zaken's Necklace +1-3"),

    ("Zaken's Necklace +4+", "Zaken's Necklace +4+"),

    ("Orfen's Necklace +0", "Orfen's Necklace +0"),

    ("Orfen's Necklace +1-3", "Orfen's Necklace +1-3"),

    ("Orfen's Necklace +4+", "Orfen's Necklace +4+"),

    ("Majestic Necklace +0", "Majestic Necklace +0"),

    ("Majestic Necklace +1-3", "Majestic Necklace +1-3"),

    ("Majestic Necklace +4+", "Majestic Necklace +4+"),

    ("Apella Necklace +0", "Apella Necklace +0"),

    ("Apella Necklace +1-3", "Apella Necklace +1-3"),

    ("Apella Necklace +4+", "Apella Necklace +4+"),

    ("Valakas' Necklace +0", "Valakas' Necklace +0"),

    ("Antharas Necklace +0", "Antharas Necklace +0"),

    ("Lindvior's Necklace +0", "Lindvior's Necklace +0"),

    ("Archmage Necklace +0", "Archmage Necklace +0"),

]'''

new_necklace_choices = '''PVP_NECKLACE_CHOICES = [
    ('', 'No necklace selected'),
    ("Blue necklace", "Blue necklace"),
    ("Necklace of Immortality", "Necklace of Immortality"),
    ("Lilith's Soul Necklace", "Lilith's Soul Necklace"),
    ("Anakeem's Soul Necklace", "Anakeem's Soul Necklace"),
    ("Baium's Necklace", "Baium's Necklace"),
    ("Zaken's Necklace", "Zaken's Necklace"),
    ("Orfen's Necklace", "Orfen's Necklace"),
    ("Majestic Necklace", "Majestic Necklace"),
    ("Apella Necklace", "Apella Necklace"),
    ("Valakas' Necklace", "Valakas' Necklace"),
    ("Antharas Necklace", "Antharas Necklace"),
    ("Lindvior's Necklace", "Lindvior's Necklace"),
    ("Archmage Necklace", "Archmage Necklace"),
]'''

if old_necklace_choices in content:
    content = content.replace(old_necklace_choices, new_necklace_choices)
    print("1a. Updated PVP_NECKLACE_CHOICES")
else:
    print("ERROR: Could not find PVP_NECKLACE_CHOICES")

# Add enchant field
old_necklace_field = '''    pvp_necklace = models.CharField("PvP Necklace", max_length=100, choices=PVP_NECKLACE_CHOICES, blank=True)'''
new_necklace_field = '''    pvp_necklace = models.CharField("PvP Necklace", max_length=100, choices=PVP_NECKLACE_CHOICES, blank=True)
    pvp_necklace_enchant = models.IntegerField("PvP Necklace Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")'''

if old_necklace_field in content:
    content = content.replace(old_necklace_field, new_necklace_field)
    print("1b. Added pvp_necklace_enchant field")
else:
    print("ERROR: Could not find pvp_necklace field")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("   models.py saved.")


# ============================================
# 2. UPDATE forms.py - change necklace widget to Select
# ============================================
path = r"D:\Django Project\Alto Project\items\forms.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'pvp_necklace': forms.RadioSelect,", "'pvp_necklace': forms.Select,")
print("2. Updated forms.py - necklace widget to Select")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)


# ============================================
# 3. UPDATE item_extras.py - filter + mappings
# ============================================
path = r"D:\Django Project\Alto Project\items\templatetags\item_extras.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update filter
old_filter = "    return field_name in ('weapon', 'weapon_enchant', 'pvp_belt', 'pvp_belt_enchant', 'pvp_ring_left', 'pvp_ring_left_enchant', 'pvp_ring_right', 'pvp_ring_right_enchant')"
new_filter = "    return field_name in ('weapon', 'weapon_enchant', 'pvp_belt', 'pvp_belt_enchant', 'pvp_ring_left', 'pvp_ring_left_enchant', 'pvp_ring_right', 'pvp_ring_right_enchant', 'pvp_necklace', 'pvp_necklace_enchant')"
content = content.replace(old_filter, new_filter)
print("3a. Updated is_weapon_field filter")

# Add base name mappings
old_mapping_end = '''        "Blessed Valakas' Necklace": "Icon_ACC_Necklace_G2_004.png",'''
new_mapping_end = '''        "Blessed Valakas' Necklace": "Icon_ACC_Necklace_G2_004.png",
        # Base necklace names (new format)
        "Blue necklace": "Icon_ACC_Necklace_G4_007.png",
        "Necklace of Immortality": "Icon_ACC_Necklace_G3_001.png",
        "Lilith's Soul Necklace": "Icon_ACC_Necklace_G3_002.png",
        "Anakeem's Soul Necklace": "Icon_ACC_Necklace_G3_002.png",
        "Baium's Necklace": "Icon_ACC_Necklace_G3_001.png",
        "Zaken's Necklace": "Icon_ACC_Necklace_G3_004.png",
        "Orfen's Necklace": "Icon_ACC_Necklace_G2_002.png",
        "Majestic Necklace": "Icon_ACC_Necklace_G3_001.png",
        "Apella Necklace": "Icon_ACC_Necklace_G3_001.png",
        "Valakas' Necklace": "Icon_ACC_Necklace_G3_003.png",
        "Antharas Necklace": "Icon_ACC_Necklace_G3_006.png",
        "Lindvior's Necklace": "Icon_ACC_Necklace_G3_006.png",
        "Archmage Necklace": "Icon_ACC_Necklace_G3_001.png",'''

if old_mapping_end in content:
    content = content.replace(old_mapping_end, new_mapping_end)
    print("3b. Added base necklace image mappings")
else:
    print("ERROR: Could not find mapping insertion point")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nBackend updated.")
