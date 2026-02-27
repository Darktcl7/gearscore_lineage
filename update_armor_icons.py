import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

from items.models import Item

# New image mapping: partial item name -> new icon file
# Based on the armor folder files
IMAGE_MAP = {
    # HELMETS
    "ancient elven helm": "choices/armor_helmet_Ancient_Elven_Helmet.png",
    "ancient elven helmet": "choices/armor_helmet_Ancient_Elven_Helmet.png",
    "crown of the world tree": "choices/armor_helmet_Crown_of_the_World_Tree.png",
    "dark crystal helmet": "choices/armor_helmet_Dark_Crystal_Helmet.png",
    "devil's helmet": "choices/armor_helmet_Devil's_Helmet.png",
    "demon's helmet": "choices/armor_helmet_Devil's_Helmet.png",
    "draconic leather helmet": "choices/armor_helmet_Draconic_Leather_Helmet.png",
    "draconic helmet": "choices/armor_helmet_Draconic_Leather_Helmet.png",
    "helmet of the fallen angel": "choices/armor_helmet_Helmet_of_the_Fallen_Angel.png",
    "fallen angel helmet": "choices/armor_helmet_Helmet_of_the_Fallen_Angel.png",
    "hildegrim": "choices/armor_helmet_Hildegrim.png",
    "imperial crusader helmet": "choices/armor_helmet_Imperial_Crusader_Helmet.png",
    "majestic circlet": "choices/armor_helmet_Majestic_Circlet.png",
    "major arcana circlet": "choices/armor_helmet_Major_Arcana_Circlet.png",
    "medusa's helm": "choices/armor_helmet_Medusa's_Helmet.png",
    "medusa's helmet": "choices/armor_helmet_Medusa's_Helmet.png",
    "nebit's helmet": "choices/armor_helmet_Nebit's_Helmet.png",
    "nevit's helmet": "choices/armor_helmet_Nebit's_Helmet.png",
    "helm of nightmares": "choices/armor_helmet_Nightmare_Helmet.png",
    "nightmare helmet": "choices/armor_helmet_Nightmare_Helmet.png",
    "paulina's helmet": "choices/armor_helmet_Pauline's_Helmet.png",
    "pauline's helmet": "choices/armor_helmet_Pauline's_Helmet.png",
    "tersi's circlet": "choices/armor_helmet_Tersi's_Circlet.png",
    "blue wolf helmet": "choices/armor_helmet_Crown_of_the_World_Tree.png",
    
    # ARMOR / TOP ARMOR
    "absolute tunic": "choices/armor_armor_Absolute_Tunic.png",
    "apella's armor": "choices/armor_armor_Apella's_Armor.png",
    "breastplate of the fallen angel": "choices/armor_armor_Breastplate_of_the_Fallen_Angel.png",
    "fallen angel armor": "choices/armor_armor_Breastplate_of_the_Fallen_Angel.png",
    "breastplate of the forgotten hero": "choices/armor_armor_Breastplate_of_the_Forgotten_Hero.png",
    "forgotten hero armor": "choices/armor_armor_Breastplate_of_the_Forgotten_Hero.png",
    "dark crystal breastplate": "choices/armor_armor_Dark_Crystal_Breastplate.png",
    "dark crystal armor": "choices/armor_armor_Dark_Crystal_Breastplate.png",
    "devil's armor": "choices/armor_armor_Devil's_Armor.png",
    "demon's armor": "choices/armor_armor_Devil's_Armor.png",
    "draconic leather armor": "choices/armor_armor_Draconic_Leather_Armor.png",
    "draconic armor": "choices/armor_armor_Draconic_Leather_Armor.png",
    "imperial crusader breastplate": "choices/armor_armor_Imperial_Crusader_Breastplate.png",
    "imperial crusader armor": "choices/armor_armor_Imperial_Crusader_Breastplate.png",
    "majestic robe": "choices/armor_armor_Majestic_Robe.png",
    "majestic armor": "choices/armor_armor_Majestic_Robe.png",
    "major arcana robe": "choices/armor_armor_Major_Arcana_Robe.png",
    "nebit's armor": "choices/armor_armor_Nebit's_Armor.png",
    "nevit's armor": "choices/armor_armor_Nebit's_Armor.png",
    "nightmare armor": "choices/armor_armor_Nightmare_Armor.png",
    "polyne's breastplate": "choices/armor_armor_Polyne's_Breastplate.png",
    "paulina's armor": "choices/armor_armor_Polyne's_Breastplate.png",
    "saban's robe": "choices/armor_armor_Saban's_Robe.png",
    "tersi's robe": "choices/armor_armor_Tersi's_Robe.png",
    "tersi's armor": "choices/armor_armor_Tersi's_Robe.png",
    "ancient elven armor": "choices/armor_armor_Absolute_Tunic.png",
    
    # GLOVES
    "ancient elven gauntlets": "choices/armor_gloves_Ancient_Elven_Gauntlets.png",
    "ancient elven gloves": "choices/armor_gloves_Ancient_Elven_Gauntlets.png",
    "dark crystal globe": "choices/armor_gloves_Dark_Crystal_Globe.png",
    "dark crystal gloves": "choices/armor_gloves_Dark_Crystal_Globe.png",
    "devil's gauntlet": "choices/armor_gloves_Devil's_Gauntlet.png",
    "demon's gauntlets": "choices/armor_gloves_Devil's_Gauntlet.png",
    "draconic leather gloves": "choices/armor_gloves_Draconic_Leather_Gloves.png",
    "fallen angel's gloves": "choices/armor_gloves_Fallen_Angel's_Gloves.png",
    "fallen angel gloves": "choices/armor_gloves_Fallen_Angel's_Gloves.png",
    "globe of the forgotten hero": "choices/armor_gloves_Globe_of_the_Forgotten_Hero.png",
    "forgotten hero gloves": "choices/armor_gloves_Globe_of_the_Forgotten_Hero.png",
    "gloves of blessing": "choices/armor_gloves_Gloves_of_Blessing.png",
    "guardian of vision": "choices/armor_gloves_Guardian_of_Vision.png",
    "jarngreipr": "choices/armor_gloves_Jarngreifr.png",
    "jarngreifr": "choices/armor_gloves_Jarngreifr.png",
    "majestic gloves": "choices/armor_gloves_Majestic_Gloves.png",
    "nebit's globe": "choices/armor_gloves_Nebit's_Globe.png",
    "nevit's gloves": "choices/armor_gloves_Nebit's_Globe.png",
    "nightmare gauntlet": "choices/armor_gloves_Nightmare_Gauntlet.png",
    "gauntlets of nightmare": "choices/armor_gloves_Nightmare_Gauntlet.png",
    "paagrio's flame": "choices/armor_gloves_Paagrio's_Flame.png",
    "paulina's gauntlets": "choices/armor_gloves_Pauline's_Gauntlet.png",
    "pauline's gauntlet": "choices/armor_gloves_Pauline's_Gauntlet.png",
    "tersi's gloves": "choices/armor_gloves_Tersi's_Gloves.png",
    "blue wolf gloves": "choices/armor_gloves_Guardian_of_Vision.png",
    
    # BOOTS
    "ancient elven boots": "choices/armor_shoes_Ancient_Elven_Boots.png",
    "boots of eternal life": "choices/armor_shoes_Boots_of_Eternal_Life.png",
    "boots of the forgotten hero": "choices/armor_shoes_Boots_of_the_Forgotten_Hero.png",
    "forgotten's hero boots": "choices/armor_shoes_Boots_of_the_Forgotten_Hero.png",
    "forgotten hero boots": "choices/armor_shoes_Boots_of_the_Forgotten_Hero.png",
    "calie's boots": "choices/armor_shoes_Calie's_boots.png",
    "kaliel's boots": "choices/armor_shoes_Calie's_boots.png",
    "dark crystal boots": "choices/armor_shoes_Dark_Crystal_Boots.png",
    "devil's boots": "choices/armor_shoes_Devil's_Boots.png",
    "demon's boots": "choices/armor_shoes_Devil's_Boots.png",
    "draconic leather boots": "choices/armor_shoes_Draconic_Leather_Boots.png",
    "fallen angel's boots": "choices/armor_shoes_Fallen_Angel's_Boots.png",
    "fallen angel boots": "choices/armor_shoes_Fallen_Angel's_Boots.png",
    "majestic boots": "choices/armor_shoes_Majestic_Boots.png",
    "nebit's boots": "choices/armor_shoes_Nebit's_Boots.png",
    "nevit's boots": "choices/armor_shoes_Nebit's_Boots.png",
    "nightmare boots": "choices/armor_shoes_Nightmare_Boots.png",
    "boots of nightmares": "choices/armor_shoes_Nightmare_Boots.png",
    "paulina's boots": "choices/armor_shoes_Pauline's_boots.png",
    "pauline's boots": "choices/armor_shoes_Pauline's_boots.png",
    "reaper's boots": "choices/armor_shoes_Reaper's_Boots.png",
    "saiha's wind": "choices/armor_shoes_Saiha's_Wind.png",
    "tersi's boots": "choices/armor_shoes_Tersi's_boots.png",
    "blue wolf boots": "choices/armor_shoes_Boots_of_Eternal_Life.png",
    
    # CLOAK
    "aegis cloak": "choices/armor_cloak_Aegis_Cloak.png",
    "cloak of power": "choices/armor_cloak_Cloak_of_Power.png",
    "cloak of silence": "choices/armor_cloak_Cloak_of_Silence.png",
    "cloak of verdant green": "choices/armor_cloak_Cloak_of_Verdant_Green.png",
    "cranbel's cloak": "choices/armor_cloak_Cranbel's_Cloak.png",
    "dragon's scales": "choices/armor_cloak_Dragon's_Scales.png",
    "freya's cloak": "choices/armor_cloak_Freya's_Cloak.png",
    "jaqen's cloak": "choices/armor_cloak_Jaqen's_Cloak.png",
    "mantle of the holy spirit": "choices/armor_cloak_Mantle_of_the_Holy_Spirit.png",
    "moonlight's cloak": "choices/armor_cloak_Moonlight's_Cloak.png",
    "nebit's cloak": "choices/armor_cloak_Nebit's_Cloak_of_Light.png",
    "nevit's cloak": "choices/armor_cloak_Nebit's_Cloak_of_Light.png",
    "niarop's cloak": "choices/armor_cloak_Niarop's_Cloak.png",
    "salamander's cloak": "choices/armor_cloak_Salamander's_Cloak.png",
    "sally hoden's wings": "choices/armor_cloak_Sally_Hoden's_Wings.png",
    "queen ant wings": "choices/armor_cloak_queen_ant_wings.png",
    
    # SIGIL
    "arcana sigil": "choices/armor_sigil_Arcana_Sigil.png",
    "blood crystal": "choices/armor_sigil_Blood_Crystal.png",
    "cruma's shell": "choices/armor_sigil_Cruma's_Shell.png",
    "crystal of oblivion": "choices/armor_sigil_Crystal_of_Oblivion.png",
    "draconic sigil": "choices/armor_sigil_Draconic_Sigil.png",
    "dream sigil": "choices/armor_sigil_Dream_Sigil.png",
    "eldarach": "choices/armor_sigil_Eldarach.png",
    "holy sigil": "choices/armor_sigil_Holy_Sigil.png",
    "parody sigil": "choices/armor_sigil_Parody_Sigil.png",
    "sally horden's horn": "choices/armor_sigil_Sally_Horden's_Horn.png",
    "sniper sigil": "choices/armor_sigil_Sniper_Sigil.png",
    "susceptor's heart": "choices/armor_sigil_Susceptor's_Heart.png",
    "sigil of the fallen angel": "choices/armor_sigil_The_Sigil_of_the_Fallen_Angel.png",
    "sigil of karma": "choices/armor_sigil_The_sigil_of_karma.png",
    "tier of darkness": "choices/armor_sigil_Tier_of_Darkness.png",
    
    # GAITERS / PANTS / BOTTOMS
    "basil's shell": "choices/armor_bottoms_Basil's_shell.png",
    "blood greaves": "choices/armor_bottoms_Blood_Greaves.png",
    "blue wolf's leggings": "choices/armor_bottoms_Blue_Wolf's_Leggings.png",
    "blue wolf leggings": "choices/armor_bottoms_Blue_Wolf's_Leggings.png",
    "breath of silen": "choices/armor_bottoms_Breath_of_Silen.png",
    "crystal gaiters": "choices/armor_bottoms_Crystal_gaiters.png",
    "devil's pact": "choices/armor_bottoms_Devil's_Pact.png",
    "fallen angel's legguards": "choices/armor_bottoms_Fallen_Angel's_Legguards.png",
    "fallen angel legguards": "choices/armor_bottoms_Fallen_Angel's_Legguards.png",
    "flame greaves": "choices/armor_bottoms_Flame_Greaves.png",
    "forgotten hero's greaves": "choices/armor_bottoms_Forgotten_Hero's_Greaves.png",
    "forgotten hero greaves": "choices/armor_bottoms_Forgotten_Hero's_Greaves.png",
    "full plate gaiters": "choices/armor_bottoms_Full_plate_gaiters.png",
    "ice leggings": "choices/armor_bottoms_Ice_Leggings.png",
    "imperial crusader legguards": "choices/armor_bottoms_Imperial_Crusader_Legguards.png",
    "light's greaves": "choices/armor_bottoms_Light's_Greaves.png",
    "patience leggings": "choices/armor_bottoms_Patience_Leggings.png",
    "spirit's greaves": "choices/armor_bottoms_Spirit's_Greaves.png",
}

# Update items in database
target_types = ['Helmet', 'Armor', 'Gloves', 'Boots', 'Cloak', 'Sigil', 'Pants', 'Torso']
updated = 0
not_found = []

for item in Item.objects.filter(item_type__in=target_types):
    item_name_lower = item.name.lower()
    matched = False
    for key, new_icon in IMAGE_MAP.items():
        if key in item_name_lower:
            old_icon = item.icon_file
            item.icon_file = new_icon
            item.save()
            print(f"  UPDATED [{item.id}] {item.name}: {old_icon} -> {new_icon}")
            updated += 1
            matched = True
            break
    if not matched:
        not_found.append(f"  [{item.id}] {item.name} (type: {item.item_type})")

print(f"\n=== Updated: {updated} items ===")
if not_found:
    print(f"\n=== Not matched ({len(not_found)}) ===")
    for nf in not_found:
        print(nf)
