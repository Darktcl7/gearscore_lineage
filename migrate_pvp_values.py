import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import CharacterAttributes

# Mapping old choice values to new choice values
OLD_TO_NEW = {
    # Helmet
    "Blue Wolf Helmet": "Crown of the World Tree",
    "Helm of Nightmares": "Nightmare Helmet",
    "Medusa's Helm": "Medusa's Helmet",
    "Paulina's Helmet": "Pauline's Helmet",
    "Nevit's Helmet": "Nebit's Helmet",
    "Ancient Elven Helm": "Ancient Elven Helmet",
    "Draconic Helmet": "Draconic Leather Helmet",
    
    # Gloves
    "Blue Wolf Gloves": "Guardian of Vision",
    "Gauntlets of Nightmare": "Nightmare Gauntlet",
    "Dark Crystal Gloves": "Dark Crystal Globe",
    "Paulina's Gauntlets": "Pauline's Gauntlet",
    "Nevit's Gloves": "Nebit's Globe",
    "Jarngreipr": "Jarngreifr",
    "Vision Guardian": "Guardian of Vision",
    "Forgotten Hero Gloves": "Globe of the Forgotten Hero",
    "Demon's Gauntlets": "Devil's Gauntlet",
    "Ancient Elven Gauntlet": "Ancient Elven Gauntlets",
    "Pa'agrio's Flames": "Paagrio's Flame",
    
    # Boots
    "Blue Wolf Boots": "Boots of Eternal Life",
    "Boots of Nightmares": "Nightmare Boots",
    "Paulina's Boots": "Pauline's Boots",
    "Nevit's Boots": "Nebit's Boots",
    "Demon's Boots": "Devil's Boots",
    "Kaliel's Boots": "Calie's Boots",
    "Forgotten Hero's Boots": "Boots of the Forgotten Hero",
    "Draconic": "Draconic Leather Boots",
    "Sayha's Wind": "Saiha's Wind",
    
    # Gaiters
    "Blue Wolf Gaiters": "Blue Wolf's Leggings",
    "Basila Skin": "Basil's Shell",
    "Blood Gaiters": "Blood Greaves",
    "Gaiters of Light": "Light's Greaves",
    "Gaiters of Ice": "Ice Leggings",
    "Shilen's Breath": "Breath of Silen",
    "Forgotten Hero's Gaiters": "Forgotten Hero's Greaves",
    "Imperial Crusader Gaiters": "Imperial Crusader Legguards",
    
    # Armor
    "Blue Wolf Breastplate": "Breastplate of the Forgotten Hero",
    "Armor of Nightmares": "Nightmare Armor",
    "Paulina's Breastplate": "Polyne's Breastplate",
    "Nevit's Armor": "Nebit's Armor",
    "Savan's Robe": "Saban's Robe",
    "Apella Plate Armor": "Apella's Armor",
    "Forgotten Hero's Breastplate": "Breastplate of the Forgotten Hero",
    "Ancient Elven Armor": "Absolute Tunic",
    "Demon's Armor": "Devil's Armor",
    
    # Cloak
    "Silver Cloak": "Moonlight's Cloak",
    "Cranigg's Cloak": "Cranbel's Cloak",
    "Other blue or green cloak": "Jaqen's Cloak",
    "Dragon's Scale": "Dragon's Scales",
    "Zaken's Cloak": "Jaqen's Cloak",
    "Cloak of Freya": "Freya's Cloak",
    "Queen Ant's Wing": "Queen Ant Wings",
    "Eigis Cloak": "Aegis Cloak",
    "Cloak of Authority": "Cloak of Power",
    "Selihoden's Wing": "Sally Hoden's Wings",
    "Nevit's Cloak of Light": "Nebit's Cloak of Light",
    "Nailop's Cloak": "Niarop's Cloak",
    
    # Sigil
    "Blue": "Eldarach",
    "Paradia's Sigil": "Parody Sigil",
    "Sigil of Flames": "Sniper Sigil",
    "Jaeger's Sigil": "Sniper Sigil",
    "Selihoden's Horn": "Sally Horden's Horn",
    "Tear of Darkness": "Tier of Darkness",
    "Sigil of the Fallen Angel": "The Sigil of the Fallen Angel",
    "Sigil of Karma": "The Sigil of Karma",
}

pvp_fields = ['pvp_helmet', 'pvp_gloves', 'pvp_boots', 'pvp_gaiters', 'pvp_top_armor', 'pvp_cloak', 'pvp_sigil']

updated = 0
for attrs in CharacterAttributes.objects.all():
    changed = False
    for field in pvp_fields:
        val = getattr(attrs, field, '')
        if val in OLD_TO_NEW:
            new_val = OLD_TO_NEW[val]
            setattr(attrs, field, new_val)
            print(f"  Char {attrs.character_id} {field}: [{val}] -> [{new_val}]")
            changed = True
    if changed:
        attrs.save()
        updated += 1

print(f"\nUpdated {updated} character(s)")
