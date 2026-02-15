"""
Script to update PVP Sigil to use base names + separate enchant field.
Updates: models.py, forms.py, item_extras.py, character_form.html
"""

# ============================================
# 1. UPDATE models.py - PVP_SIGIL_CHOICES + add enchant field
# ============================================
path = r"D:\Django Project\Alto Project\items\models.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define old and new choices
old_sigil_choices = '''PVP_SIGIL_CHOICES = [

    ("Dream Sigil +3-4", "Dream Sigil +3-4"),

    ("Dream Sigil +5+", "Dream Sigil +5+"),

    ("Blue (other) and lower", "Blue (other) and lower"),

    ("Susceptor's Heart +0", "Susceptor's Heart +0"),

    ("Susceptor's Heart +1-3", "Susceptor's Heart +1-3"),

    ("Susceptor's Heart +4+", "Susceptor's Heart +4+"),

    ("Paradia's Sigil +0", "Paradia's Sigil +0"),

    ("Paradia's Sigil +1-3", "Paradia's Sigil +1-3"),

    ("Paradia's Sigil +4+", "Paradia's Sigil +4+"),

    ("Cruma's Shell +0", "Cruma's Shell +0"),

    ("Cruma's Shell +1-3", "Cruma's Shell +1-3"),

    ("Cruma's Shell +4+", "Cruma's Shell +4+"),

    ("Sigil of Flames +0", "Sigil of Flames +0"),

    ("Sigil of Flames +1-3", "Sigil of Flames +1-3"),

    ("Sigil of Flames +4+", "Sigil of Flames +4+"),

    ("Jaeger's Sigil +0", "Jaeger's Sigil +0"),

    ("Jaeger's Sigil +1-3", "Jaeger's Sigil +1-3"),

    ("Jaeger's Sigil +4+", "Jaeger's Sigil +4+"),

    ("Selihoden's Horn +0", "Selihoden's Horn +0"),

    ("Selihoden's Horn +1-3", "Selihoden's Horn +1-3"),

    ("Selihoden's Horn +4+", "Selihoden's Horn +4+"),

    ("Tear of Darkness", "Tear of Darkness"),

    ("Draconic Sigil", "Draconic Sigil"),

    ("Arcana Sigil", "Arcana Sigil"),

]'''

new_sigil_choices = '''PVP_SIGIL_CHOICES = [
    ('', 'No sigil selected'),
    ("Dream Sigil", "Dream Sigil"),
    ("Blue", "Blue"),
    ("Susceptor's Heart", "Susceptor's Heart"),
    ("Paradia's Sigil", "Paradia's Sigil"),
    ("Cruma's Shell", "Cruma's Shell"),
    ("Sigil of Flames", "Sigil of Flames"),
    ("Jaeger's Sigil", "Jaeger's Sigil"),
    ("Selihoden's Horn", "Selihoden's Horn"),
    ("Tear of Darkness", "Tear of Darkness"),
    ("Draconic Sigil", "Draconic Sigil"),
    ("Arcana Sigil", "Arcana Sigil"),
]'''

if old_sigil_choices in content:
    content = content.replace(old_sigil_choices, new_sigil_choices)
    print("1a. Updated PVP_SIGIL_CHOICES")
else:
    print("ERROR: Could not find PVP_SIGIL_CHOICES")

# Add enchant field
old_sigil_field = '''    pvp_sigil = models.CharField("PvP Sigil", max_length=100, choices=PVP_SIGIL_CHOICES, blank=True)'''
new_sigil_field = '''    pvp_sigil = models.CharField("PvP Sigil", max_length=100, choices=PVP_SIGIL_CHOICES, blank=True)
    pvp_sigil_enchant = models.IntegerField("PvP Sigil Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")'''

if old_sigil_field in content:
    content = content.replace(old_sigil_field, new_sigil_field)
    print("1b. Added pvp_sigil_enchant field")
else:
    print("ERROR: Could not find pvp_sigil field")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("   models.py saved.")


# ============================================
# 2. UPDATE forms.py - change sigil widget to Select
# ============================================
path = r"D:\Django Project\Alto Project\items\forms.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'pvp_sigil': forms.RadioSelect,", "'pvp_sigil': forms.Select,")
print("2. Updated forms.py - sigil widget to Select")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)


# ============================================
# 3. UPDATE item_extras.py - filter + mappings
# ============================================
path = r"D:\Django Project\Alto Project\items\templatetags\item_extras.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update filter
old_filter = "    return field_name in ('weapon', 'weapon_enchant', 'pvp_belt', 'pvp_belt_enchant', 'pvp_ring_left', 'pvp_ring_left_enchant', 'pvp_ring_right', 'pvp_ring_right_enchant', 'pvp_necklace', 'pvp_necklace_enchant')"
new_filter = "    return field_name in ('weapon', 'weapon_enchant', 'pvp_belt', 'pvp_belt_enchant', 'pvp_ring_left', 'pvp_ring_left_enchant', 'pvp_ring_right', 'pvp_ring_right_enchant', 'pvp_necklace', 'pvp_necklace_enchant', 'pvp_sigil', 'pvp_sigil_enchant')"
content = content.replace(old_filter, new_filter)
print("3a. Updated is_weapon_field filter")

# Add base name mappings
old_mapping_end = '''        "Arcana Sigil": "Icon_AR_Sigil_G2_003.png",'''
new_mapping_end = '''        "Arcana Sigil": "Icon_AR_Sigil_G2_003.png",
        # Base sigil names (new format)
        "Dream Sigil": "Icon_AR_Sigil_G4_001.png",
        "Blue": "вопрос_PiWb3ob.png",
        "Susceptor's Heart": "Icon_AR_Sigil_G3_001.png",
        "Paradia's Sigil": "Icon_AR_Sigil_G3_002.png",
        "Cruma's Shell": "Icon_AR_Sigil_G3_003.png",
        "Sigil of Flames": "Icon_AR_Sigil_G3_004.png",
        "Jaeger's Sigil": "Icon_AR_Sigil_G3_005.png",
        "Selihoden's Horn": "Icon_AR_Sigil_G3_006.png",'''

if old_mapping_end in content:
    content = content.replace(old_mapping_end, new_mapping_end)
    print("3b. Added base sigil image mappings")
else:
    print("ERROR: Could not find mapping insertion point")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nBackend updated.")
