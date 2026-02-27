import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

from items.models import Item

# Fix all remaining items that still use old Icon_AR_ images
FIX_MAP = {
    # Cloak - still using old icons
    1019: "choices/armor_cloak_Moonlight's_Cloak.png",  # Silver Cloak +7+
    1020: "choices/armor_cloak_Cranbel's_Cloak.png",  # Cranigg's Cloak +6+
    1021: "choices/armor_cloak_Jaqen's_Cloak.png",  # Other blue or green cloak
    1022: "choices/armor_cloak_Dragon's_Scales.png",  # Dragon's Scale +5
    1023: "choices/armor_cloak_Dragon's_Scales.png",  # Dragon's Scale +6+
    1024: "choices/armor_cloak_Jaqen's_Cloak.png",  # Zaken's Cloak +5
    1025: "choices/armor_cloak_Jaqen's_Cloak.png",  # Zaken's Cloak +6+
    1026: "choices/armor_cloak_Freya's_Cloak.png",  # Cloak of Freya +5
    1027: "choices/armor_cloak_Freya's_Cloak.png",  # Cloak of Freya +6+
    1028: "choices/armor_cloak_queen_ant_wings.png",  # QA Wing +5
    1029: "choices/armor_cloak_queen_ant_wings.png",  # QA Wing +6+
    1032: "choices/armor_cloak_Aegis_Cloak.png",  # Eigis Cloak +5
    1033: "choices/armor_cloak_Aegis_Cloak.png",  # Eigis Cloak +6+
    1034: "choices/armor_cloak_Cloak_of_Power.png",  # Cloak of Authority +5
    1035: "choices/armor_cloak_Cloak_of_Power.png",  # Cloak of Authority +6+
    1036: "choices/armor_cloak_Sally_Hoden's_Wings.png",  # Selihoden's Wing +5
    1037: "choices/armor_cloak_Sally_Hoden's_Wings.png",  # Selihoden's Wing +6+
    1039: "choices/armor_cloak_Niarop's_Cloak.png",  # Nailop's Cloak
    
    # Sigil - still using old icons
    1046: "choices/armor_sigil_Parody_Sigil.png",  # Paradia's Sigil +0
    1047: "choices/armor_sigil_Parody_Sigil.png",  # Paradia +1-3
    1048: "choices/armor_sigil_Parody_Sigil.png",  # Paradia +4+
    1052: "choices/armor_sigil_Sniper_Sigil.png",  # Sigil of Flames +0
    1053: "choices/armor_sigil_Sniper_Sigil.png",  # Sigil of Flames +1-3
    1054: "choices/armor_sigil_Sniper_Sigil.png",  # Sigil of Flames +4+
    1055: "choices/armor_sigil_Sniper_Sigil.png",  # Jaeger's Sigil +0
    1056: "choices/armor_sigil_Sniper_Sigil.png",  # Jaeger +1-3
    1057: "choices/armor_sigil_Sniper_Sigil.png",  # Jaeger +4+
    1058: "choices/armor_sigil_Sally_Horden's_Horn.png",  # Selihoden's Horn +0
    1059: "choices/armor_sigil_Sally_Horden's_Horn.png",  # Selihoden +1-3
    1060: "choices/armor_sigil_Sally_Horden's_Horn.png",  # Selihoden +4+
    
    # Pants - still using old icons
    976: "choices/armor_bottoms_Blue_Wolf's_Leggings.png",  # Blue Wolf Gaiters
    978: "choices/armor_bottoms_Blood_Greaves.png",
    979: "choices/armor_bottoms_Blood_Greaves.png",
    980: "choices/armor_bottoms_Light's_Greaves.png",
    981: "choices/armor_bottoms_Light's_Greaves.png",
    982: "choices/armor_bottoms_Ice_Leggings.png",
    983: "choices/armor_bottoms_Ice_Leggings.png",
    988: "choices/armor_bottoms_Forgotten_Hero's_Greaves.png",
    989: "choices/armor_bottoms_Forgotten_Hero's_Greaves.png",
    990: "choices/armor_bottoms_Imperial_Crusader_Legguards.png",
    
    # Torso - still using old icons
    991: "choices/armor_armor_Breastplate_of_the_Forgotten_Hero.png",
    994: "choices/armor_armor_Nightmare_Armor.png",
    995: "choices/armor_armor_Nightmare_Armor.png",
    1000: "choices/armor_armor_Polyne's_Breastplate.png",
    1001: "choices/armor_armor_Polyne's_Breastplate.png",
    1004: "choices/armor_armor_Saban's_Robe.png",
    1005: "choices/armor_armor_Saban's_Robe.png",
    1008: "choices/armor_armor_Apella's_Armor.png",
    1009: "choices/armor_armor_Apella's_Armor.png",
    1010: "choices/armor_armor_Breastplate_of_the_Forgotten_Hero.png",
    1011: "choices/armor_armor_Breastplate_of_the_Forgotten_Hero.png",
}

updated = 0
for item_id, new_icon in FIX_MAP.items():
    try:
        item = Item.objects.get(id=item_id)
        item.icon_file = new_icon
        item.save()
        print(f"  FIXED [{item_id}] {item.name} -> {new_icon}")
        updated += 1
    except Item.DoesNotExist:
        print(f"  SKIP [{item_id}] - does not exist")

print(f"\nTotal fixed: {updated}")

# Now check for any remaining items with non-armor icons in these types
for t in ['Helmet', 'Armor', 'Gloves', 'Boots', 'Cloak', 'Sigil', 'Pants', 'Torso']:
    bad = Item.objects.filter(item_type=t).exclude(icon_file__contains='armor_')
    if bad.exists():
        print(f"\n  Still old in {t}:")
        for i in bad:
            print(f"    [{i.id}] {i.name} | {i.icon_file}")
