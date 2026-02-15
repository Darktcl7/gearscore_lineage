"""
Batch Update Script Part 1: MODELS
Updates PVP choices and fields for: Sigil, Helmet, Gloves, Boots, Gaiters, Armor, Cloak.
"""
import re

path = r"D:\Django Project\Alto Project\items\models.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Helper function to replace a block of text
def replace_block(content, old_start, old_end, new_block):
    # This is a bit risky with exact string matching if indentation differs
    # So we used regex to find the variable definition
    pattern = re.compile(f"{old_start}.*?{old_end}", re.DOTALL)
    if pattern.search(content):
        return pattern.sub(new_block, content, count=1)
    else:
        print(f"WARNING: Could not find block {old_start}")
        return content

# 1. SIGIL (Already prepared, but let's include it for completeness)
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
content = replace_block(content, "PVP_SIGIL_CHOICES = \[", "\]", new_sigil_choices)

# 2. HELMET
new_helmet_choices = '''PVP_HELMET_CHOICES = [
    ('', 'No helmet selected'),
    ("Blue Wolf Helmet", "Blue Wolf Helmet"),
    ("Majestic Circlet", "Majestic Circlet"),
    ("Helm of Nightmares", "Helm of Nightmares"),
    ("Dark Crystal Helmet", "Dark Crystal Helmet"),
    ("Medusa's Helm", "Medusa's Helm"),
    ("Paulina's Helmet", "Paulina's Helmet"),
    ("Nevit's Helmet", "Nevit's Helmet"),
    ("Tersi's Circlet", "Tersi's Circlet"),
    ("Ancient Elven Helm", "Ancient Elven Helm"),
    ("Imperial Crusader Helmet", "Imperial Crusader Helmet"),
    ("Major Arcana Circlet", "Major Arcana Circlet"),
    ("Draconic Helmet", "Draconic Helmet"),
]'''
content = replace_block(content, "PVP_HELMET_CHOICES = \[", "\]", new_helmet_choices)

# 3. GLOVES
new_gloves_choices = '''PVP_GLOVES_CHOICES = [
    ('', 'No gloves selected'),
    ("Blue Wolf Gloves", "Blue Wolf Gloves"),
    ("Majestic Gloves", "Majestic Gloves"),
    ("Gauntlets of Nightmare", "Gauntlets of Nightmare"),
    ("Dark Crystal Gloves", "Dark Crystal Gloves"),
    ("Tersi's Gloves", "Tersi's Gloves"),
    ("Paulina's Gauntlets", "Paulina's Gauntlets"),
    ("Nevit's Gloves", "Nevit's Gloves"),
    ("Jarngreipr", "Jarngreipr"),
    ("Vision Guardian", "Vision Guardian"),
    ("Gloves of Blessing", "Gloves of Blessing"),
    ("Forgotten Hero Gloves", "Forgotten Hero Gloves"),
    ("Demon's Gauntlets", "Demon's Gauntlets"),
    ("Ancient Elven Gauntlet", "Ancient Elven Gauntlet"),
    ("Draconic Leather Gloves", "Draconic Leather Gloves"),
    ("Pa'agrio's Flames", "Pa'agrio's Flames"),
]'''
content = replace_block(content, "PVP_GLOVES_CHOICES = \[", "\]", new_gloves_choices)

# 4. BOOTS
new_boots_choices = '''PVP_BOOTS_CHOICES = [
    ('', 'No boots selected'),
    ("Blue Wolf Boots", "Blue Wolf Boots"),
    ("Majestic Boots", "Majestic Boots"),
    ("Boots of Nightmares", "Boots of Nightmares"),
    ("Dark Crystal Boots", "Dark Crystal Boots"),
    ("Tersi's Boots", "Tersi's Boots"),
    ("Paulina's Boots", "Paulina's Boots"),
    ("Nevit's Boots", "Nevit's Boots"),
    ("Demon's Boots", "Demon's Boots"),
    ("Kaliel's Boots", "Kaliel's Boots"),
    ("Forgotten Hero's Boots", "Forgotten Hero's Boots"),
    ("Ancient Elven Boots", "Ancient Elven Boots"),
    ("Draconic", "Draconic"),
    ("Sayha's Wind", "Sayha's Wind"),
]'''
content = replace_block(content, "PVP_BOOTS_CHOICES = \[", "\]", new_boots_choices)

# 5. GAITERS
new_gaiters_choices = '''PVP_GAITERS_CHOICES = [
    ('', 'No gaiters selected'),
    ("Blue Wolf Gaiters", "Blue Wolf Gaiters"),
    ("Basila Skin", "Basila Skin"),
    ("Blood Gaiters", "Blood Gaiters"),
    ("Gaiters of Light", "Gaiters of Light"),
    ("Gaiters of Ice", "Gaiters of Ice"),
    ("Shilen's Breath", "Shilen's Breath"),
    ("Crystal Gaiters", "Crystal Gaiters"),
    ("Forgotten Hero's Gaiters", "Forgotten Hero's Gaiters"),
    ("Imperial Crusader Gaiters", "Imperial Crusader Gaiters"),
]'''
content = replace_block(content, "PVP_GAITERS_CHOICES = \[", "\]", new_gaiters_choices)

# 6. ARMOR
new_armor_choices = '''PVP_ARMOR_CHOICES = [
    ('', 'No armor selected'),
    ("Blue Wolf Breastplate", "Blue Wolf Breastplate"),
    ("Majestic Robe", "Majestic Robe"),
    ("Armor of Nightmares", "Armor of Nightmares"),
    ("Dark Crystal Breastplate", "Dark Crystal Breastplate"),
    ("Tersi's Robe", "Tersi's Robe"),
    ("Paulina's Breastplate", "Paulina's Breastplate"),
    ("Nevit's Armor", "Nevit's Armor"),
    ("Savan's Robe", "Savan's Robe"),
    ("Absolute Tunic", "Absolute Tunic"),
    ("Apella Plate Armor", "Apella Plate Armor"),
    ("Forgotten Hero's Breastplate", "Forgotten Hero's Breastplate"),
    ("Ancient Elven Armor", "Ancient Elven Armor"),
    ("Demon's Armor", "Demon's Armor"),
    ("Draconic Leather Armor", "Draconic Leather Armor"),
    ("Major Arcana Robe", "Major Arcana Robe"),
    ("Imperial Crusader Breastplate", "Imperial Crusader Breastplate"),
]'''
content = replace_block(content, "PVP_ARMOR_CHOICES = \[", "\]", new_armor_choices)

# 7. CLOAK
new_cloak_choices = '''PVP_CLOAK_CHOICES = [
    ('', 'No cloak selected'),
    ("Silver Cloak", "Silver Cloak"),
    ("Cranigg's Cloak", "Cranigg's Cloak"),
    ("Dragon's Scale", "Dragon's Scale"),
    ("Zaken's Cloak", "Zaken's Cloak"),
    ("Cloak of Freya", "Cloak of Freya"),
    ("Queen Ant's Wing", "Queen Ant's Wing"),
    ("Cloak of Silence", "Cloak of Silence"),
    ("Eigis Cloak", "Eigis Cloak"),
    ("Cloak of Authority", "Cloak of Authority"),
    ("Selihoden's Wing", "Selihoden's Wing"),
    ("Nevit's Cloak of Light", "Nevit's Cloak of Light"),
    ("Nailop's Cloak", "Nailop's Cloak"),
]'''
content = replace_block(content, "PVP_CLOAK_CHOICES = \[", "\]", new_cloak_choices)

print("CHOICES variables updated.")

# === UPDATE FIELDS ===
# We need to add _enchant field after each existing pvp_ field
# We will use simple replace with regex

def add_enchant_field(content, field_name, verbose_name):
    # Regex look for: pvp_field = models.CharField(...)
    # Replace with: pvp_field = ... \n    pvp_field_enchant = models.IntegerField(...)
    
    pattern = re.compile(f"({field_name} = models\.CharField\(.*?blank=True\))", re.DOTALL)
    
    enchant_field = f'''\\1
    {field_name}_enchant = models.IntegerField("{verbose_name} Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")'''
    
    if pattern.search(content):
        return pattern.sub(enchant_field, content, count=1)
    else:
        print(f"WARNING: Could not find field {field_name}")
        return content

content = add_enchant_field(content, "pvp_sigil", "PvP Sigil")
content = add_enchant_field(content, "pvp_helmet", "PvP Helmet")
content = add_enchant_field(content, "pvp_gloves", "PvP Gloves")
content = add_enchant_field(content, "pvp_boots", "PvP Boots")
content = add_enchant_field(content, "pvp_gaiters", "PvP Gaiters")
content = add_enchant_field(content, "pvp_armor", "PvP Armor")
content = add_enchant_field(content, "pvp_cloak", "PvP Cloak")

print("Fields updated.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("models.py saved.")
