from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    if not isinstance(dictionary, dict):
        return None
    return dictionary.get(key)

@register.filter
def class_name(obj):
    """Returns the class name of an object."""
    return obj.__class__.__name__

@register.filter
def is_skill_field(field_name):
    """Check if a field is a skill field."""
    skill_fields = [
        'skill_frenzy', 'skill_vital_destruction', 'skill_infinity_strike',
        'skill_disarm', 'skill_giant_stomp', 'skill_absolute_spear',
        'skill_rolling_thunder', 'skill_earthquake_stomp'
    ]
    return field_name in skill_fields

@register.filter
def is_weapon_field(field_name):
    """Check if a field is the weapon field, weapon enchant, or pvp belt fields."""
    return field_name in ('weapon', 'weapon_enchant', 'pvp_belt', 'pvp_belt_enchant', 'pvp_ring_left', 'pvp_ring_left_enchant', 'pvp_ring_right', 'pvp_ring_right_enchant', 'pvp_necklace', 'pvp_necklace_enchant', 'pvp_sigil', 'pvp_sigil_enchant', 'pvp_helmet', 'pvp_helmet_enchant', 'pvp_gloves', 'pvp_gloves_enchant', 'pvp_boots', 'pvp_boots_enchant', 'pvp_gaiters', 'pvp_gaiters_enchant', 'pvp_top_armor', 'pvp_top_armor_enchant', 'pvp_cloak', 'pvp_cloak_enchant', 'pvp_tshirt', 'pvp_tshirt_enchant')



@register.filter
def get_weapon_display_name(value):
    """Returns the display name for a weapon (after the pipe)."""
    if not value or not isinstance(value, str):
        return value
    if '|' in value:
        return value.split('|', 1)[1]
    return value

@register.filter
def get_weapon_media_url(value):
    """Returns the media URL path for a weapon."""
    if not value or not isinstance(value, str) or '|' not in value:
        return None
    
    weapon_type, weapon_name = value.split('|', 1)
    # Return path relative to MEDIA_ROOT
    return f"items/weapons/{weapon_type}/{weapon_name}.png"

@register.filter
def is_gearscore_field(field_name):
    """Check if a field belongs to Gear Score Stats tab."""
    gearscore_fields = [
        'stat_dmg', 'stat_acc', 'stat_def', 'stat_resist', 'stat_reduc',
        'stat_skill_dmg_boost', 'stat_wpn_dmg_boost', 'soulshot_level',
        'valor_level', 'stat_guardian', 'stat_conquer', 'epic_classes_count',
        'epic_agathions_count', 'total_legend_codex', 'total_epic_mount',
    ]
    # Include all G fields (g1 to g38)
    gearscore_fields += [f'g{i}' for i in range(1, 39)]
    return field_name in gearscore_fields

@register.filter
def is_expertise_field(field_name):
    """Check if a field belongs to Expertise section."""
    return str(field_name).startswith('exp_')

@register.filter
def get_image_for_choice(label):
    """Returns the image filename for a given choice label."""
    label_str = str(label).strip()
    
    # Dynamic lookup for legendary items from database
    from items.models import LegendaryClass, LegendaryAgathion, LegendaryMount
    
    # Check legendary classes
    try:
        lc = LegendaryClass.objects.filter(name=label_str).first()
        if lc and lc.icon_file:
            return lc.icon_file
    except Exception:
        pass
    
    # Check legendary agathions
    try:
        la = LegendaryAgathion.objects.filter(name=label_str).first()
        if la and la.icon_file:
            return la.icon_file
    except Exception:
        pass
    
    # Check legendary mounts
    try:
        lm = LegendaryMount.objects.filter(name=label_str).first()
        if lm and lm.icon_file:
            return lm.icon_file
    except Exception:
        pass
    
    mapping = {
        # ============================================
        # MYTHIC CLASSES
        # ============================================
        "Elcadia": "Icon_Classcard_Elcadia.png",
        "Elhwynha": "Icon_Classcard_Elhwynha.png",
        "Raoul": "Icon_Classcard_Raoul.png",

        # ============================================
        # INHERITOR BOOKS
        # ============================================
        "Increase Strength": "Icon_Item_Usable_SkillBook_04.png",
        "Increase Dexterity": "Icon_Item_Usable_SkillBook_04.png",
        "Increase Intelligence": "Icon_Item_Usable_SkillBook_04.png",
        "Increase Agility": "Icon_Item_Usable_SkillBook_04.png",
        "Increase Wisdom": "Icon_Item_Usable_SkillBook_04.png",
        "Increase Constitution": "Icon_Item_Usable_SkillBook_04.png",
        "Salvation": "Icon_Item_Usable_SkillBook_04.png",
        "Stun Resist": "Icon_Item_Usable_SkillBook_04.png",
        "Hold Resist": "Icon_Item_Usable_SkillBook_04.png",
        "Increase Stun I": "Icon_Item_Usable_SkillBook_04.png",
        "Increase Skill power I": "Icon_Item_Usable_SkillBook_04.png",
        "Increase Reduction": "Icon_Item_Usable_SkillBook_04.png",
        "High Accuracy": "Icon_Item_Usable_SkillBook_04.png",
        "High potion II": "Icon_Item_Usable_SkillBook_04.png",
        "Royal Weapon Mastery": "Icon_Item_Usable_SkillBook_04.png",
        "Piercing Reduction II": "Icon_Item_Usable_SkillBook_04.png",
        "Eternal Life": "Icon_Item_Usable_SkillBook_04.png",
        "Invincible Champion": "Icon_Item_Usable_SkillBook_04.png",
        "Punishment": "Icon_Item_Usable_SkillBook_04.png",
        
        # ============================================
        # PVP HELMETS
        # ============================================
        "Ancient Elven Helmet": "armor_helmet_Ancient_Elven_Helmet.png",
        "Crown of the World Tree": "armor_helmet_Crown_of_the_World_Tree.png",
        "Dark Crystal Helmet": "armor_helmet_Dark_Crystal_Helmet.png",
        "Devil's Helmet": "armor_helmet_Devil's_Helmet.png",
        "Draconic Leather Helmet": "armor_helmet_Draconic_Leather_Helmet.png",
        "Helmet of the Fallen Angel": "armor_helmet_Helmet_of_the_Fallen_Angel.png",
        "Hildegrim": "armor_helmet_Hildegrim.png",
        "Imperial Crusader Helmet": "armor_helmet_Imperial_Crusader_Helmet.png",
        "Majestic Circlet": "armor_helmet_Majestic_Circlet.png",
        "Major Arcana Circlet": "armor_helmet_Major_Arcana_Circlet.png",
        "Medusa's Helmet": "armor_helmet_Medusa's_Helmet.png",
        "Nebit's Helmet": "armor_helmet_Nebit's_Helmet.png",
        "Nightmare Helmet": "armor_helmet_Nightmare_Helmet.png",
        "Pauline's Helmet": "armor_helmet_Pauline's_Helmet.png",
        "Tersi's Circlet": "armor_helmet_Tersi's_Circlet.png",
        
        # ============================================
        # PVP GLOVES
        # ============================================
        "Ancient Elven Gauntlets": "armor_gloves_Ancient_Elven_Gauntlets.png",
        "Dark Crystal Globe": "armor_gloves_Dark_Crystal_Globe.png",
        "Devil's Gauntlet": "armor_gloves_Devil's_Gauntlet.png",
        "Draconic Leather Gloves": "armor_gloves_Draconic_Leather_Gloves.png",
        "Fallen Angel's Gloves": "armor_gloves_Fallen_Angel's_Gloves.png",
        "Globe of the Forgotten Hero": "armor_gloves_Globe_of_the_Forgotten_Hero.png",
        "Gloves of Blessing": "armor_gloves_Gloves_of_Blessing.png",
        "Guardian of Vision": "armor_gloves_Guardian_of_Vision.png",
        "Jarngreifr": "armor_gloves_Jarngreifr.png",
        "Majestic Gloves": "armor_gloves_Majestic_Gloves.png",
        "Nebit's Globe": "armor_gloves_Nebit's_Globe.png",
        "Nightmare Gauntlet": "armor_gloves_Nightmare_Gauntlet.png",
        "Paagrio's Flame": "armor_gloves_Paagrio's_Flame.png",
        "Pauline's Gauntlet": "armor_gloves_Pauline's_Gauntlet.png",
        "Tersi's Gloves": "armor_gloves_Tersi's_Gloves.png",
        
        # ============================================
        # PVP BOOTS
        # ============================================
        "Ancient Elven Boots": "armor_shoes_Ancient_Elven_Boots.png",
        "Boots of Eternal Life": "armor_shoes_Boots_of_Eternal_Life.png",
        "Boots of the Forgotten Hero": "armor_shoes_Boots_of_the_Forgotten_Hero.png",
        "Calie's Boots": "armor_shoes_Calie's_boots.png",
        "Dark Crystal Boots": "armor_shoes_Dark_Crystal_Boots.png",
        "Devil's Boots": "armor_shoes_Devil's_Boots.png",
        "Draconic Leather Boots": "armor_shoes_Draconic_Leather_Boots.png",
        "Fallen Angel's Boots": "armor_shoes_Fallen_Angel's_Boots.png",
        "Majestic Boots": "armor_shoes_Majestic_Boots.png",
        "Nebit's Boots": "armor_shoes_Nebit's_Boots.png",
        "Nightmare Boots": "armor_shoes_Nightmare_Boots.png",
        "Pauline's Boots": "armor_shoes_Pauline's_boots.png",
        "Reaper's Boots": "armor_shoes_Reaper's_Boots.png",
        "Saiha's Wind": "armor_shoes_Saiha's_Wind.png",
        "Tersi's Boots": "armor_shoes_Tersi's_boots.png",
        
        # ============================================
        # PVP GAITERS (PANTS)
        # ============================================
        "Basil's Shell": "armor_bottoms_Basil's_shell.png",
        "Blood Greaves": "armor_bottoms_Blood_Greaves.png",
        "Blue Wolf's Leggings": "armor_bottoms_Blue_Wolf's_Leggings.png",
        "Breath of Silen": "armor_bottoms_Breath_of_Silen.png",
        "Crystal Gaiters": "armor_bottoms_Crystal_gaiters.png",
        "Devil's Pact": "armor_bottoms_Devil's_Pact.png",
        "Fallen Angel's Legguards": "armor_bottoms_Fallen_Angel's_Legguards.png",
        "Flame Greaves": "armor_bottoms_Flame_Greaves.png",
        "Forgotten Hero's Greaves": "armor_bottoms_Forgotten_Hero's_Greaves.png",
        "Full Plate Gaiters": "armor_bottoms_Full_plate_gaiters.png",
        "Ice Leggings": "armor_bottoms_Ice_Leggings.png",
        "Imperial Crusader Legguards": "armor_bottoms_Imperial_Crusader_Legguards.png",
        "Light's Greaves": "armor_bottoms_Light's_Greaves.png",
        "Patience Leggings": "armor_bottoms_Patience_Leggings.png",
        "Spirit's Greaves": "armor_bottoms_Spirit's_Greaves.png",
        
        # ============================================
        # PVP ARMOR (TORSO)
        # ============================================
        "Absolute Tunic": "armor_armor_Absolute_Tunic.png",
        "Apella's Armor": "armor_armor_Apella's_Armor.png",
        "Breastplate of the Fallen Angel": "armor_armor_Breastplate_of_the_Fallen_Angel.png",
        "Breastplate of the Forgotten Hero": "armor_armor_Breastplate_of_the_Forgotten_Hero.png",
        "Dark Crystal Breastplate": "armor_armor_Dark_Crystal_Breastplate.png",
        "Devil's Armor": "armor_armor_Devil's_Armor.png",
        "Draconic Leather Armor": "armor_armor_Draconic_Leather_Armor.png",
        "Imperial Crusader Breastplate": "armor_armor_Imperial_Crusader_Breastplate.png",
        "Majestic Robe": "armor_armor_Majestic_Robe.png",
        "Major Arcana Robe": "armor_armor_Major_Arcana_Robe.png",
        "Nebit's Armor": "armor_armor_Nebit's_Armor.png",
        "Nightmare Armor": "armor_armor_Nightmare_Armor.png",
        "Polyne's Breastplate": "armor_armor_Polyne's_Breastplate.png",
        "Saban's Robe": "armor_armor_Saban's_Robe.png",
        "Tersi's Robe": "armor_armor_Tersi's_Robe.png",
        
        # ============================================
        # PVP CLOAK (CAPE)
        # ============================================
        "Aegis Cloak": "armor_cloak_Aegis_Cloak.png",
        "Cloak of Power": "armor_cloak_Cloak_of_Power.png",
        "Cloak of Silence": "armor_cloak_Cloak_of_Silence.png",
        "Cloak of Verdant Green": "armor_cloak_Cloak_of_Verdant_Green.png",
        "Cranbel's Cloak": "armor_cloak_Cranbel's_Cloak.png",
        "Dragon's Scales": "armor_cloak_Dragon's_Scales.png",
        "Freya's Cloak": "armor_cloak_Freya's_Cloak.png",
        "Jaqen's Cloak": "armor_cloak_Jaqen's_Cloak.png",
        "Mantle of the Holy Spirit": "armor_cloak_Mantle_of_the_Holy_Spirit.png",
        "Moonlight's Cloak": "armor_cloak_Moonlight's_Cloak.png",
        "Nebit's Cloak of Light": "armor_cloak_Nebit's_Cloak_of_Light.png",
        "Niarop's Cloak": "armor_cloak_Niarop's_Cloak.png",
        "Salamander's Cloak": "armor_cloak_Salamander's_Cloak.png",
        "Sally Hoden's Wings": "armor_cloak_Sally_Hoden's_Wings.png",
        "Queen Ant Wings": "armor_cloak_queen_ant_wings.png",
        
        # ============================================
        # PVP SIGIL
        # ============================================
        "Arcana Sigil": "armor_sigil_Arcana_Sigil.png",
        "Blood Crystal": "armor_sigil_Blood_Crystal.png",
        "Cruma's Shell": "armor_sigil_Cruma's_Shell.png",
        "Crystal of Oblivion": "armor_sigil_Crystal_of_Oblivion.png",
        "Draconic Sigil": "armor_sigil_Draconic_Sigil.png",
        "Dream Sigil": "armor_sigil_Dream_Sigil.png",
        "Eldarach": "armor_sigil_Eldarach.png",
        "Holy Sigil": "armor_sigil_Holy_Sigil.png",
        "Parody Sigil": "armor_sigil_Parody_Sigil.png",
        "Sally Horden's Horn": "armor_sigil_Sally_Horden's_Horn.png",
        "Sniper Sigil": "armor_sigil_Sniper_Sigil.png",
        "Susceptor's Heart": "armor_sigil_Susceptor's_Heart.png",
        "The Sigil of the Fallen Angel": "armor_sigil_The_Sigil_of_the_Fallen_Angel.png",
        "The Sigil of Karma": "armor_sigil_The_sigil_of_karma.png",
        "Tier of Darkness": "armor_sigil_Tier_of_Darkness.png",
        
        # ============================================
        # T-SHIRT
        # ============================================
        "Agility's Anonymous Shirt": "armor_tshirt_Agility's_anonymous_shirt.png",
        "Anonymous Shirt of Knowledge": "armor_tshirt_Anonymous_Shirt_of_Knowledge.png",
        "Anonymous Shirt of Strength": "armor_tshirt_Anonymous_shirt_of_strength.png",
        "Focus Shirt": "armor_tshirt_Focus_Shirt.png",
        "Mithril Shirt of Agility": "armor_tshirt_Mithril_Shirt_of_Agility.png",
        "Mithril Shirt of Knowledge": "armor_tshirt_Mithril_Shirt_of_Knowledge.png",
        "Mithril Shirt of Strength": "armor_tshirt_Mithril_Shirt_of_Strength.png",
        "Vigilante Shirt": "armor_tshirt_Vigilante_Shirt.png",
        "Warrior's T-shirt": "armor_tshirt_Warrior's_T-shirt.png",
        
        # ============================================
        # PVP NECKLACE
        # ============================================
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
        "Archmage Necklace": "Icon_ACC_Necklace_G3_001.png",
        
        # ============================================
        # PVP RINGS
        # ============================================
        "Ring of Blessing": "Icon_ACC_Ring_G4_010.png",
        "Lilith's Ring": "Icon_ACC_Ring_G3_003.png",
        "Anakeem's Ring": "Icon_ACC_Ring_G3_003.png",
        "Baium's Ring": "Icon_ACC_Ring_G3_001.png",
        "Vereth's Ring": "Icon_ACC_Ring_G3_006.png",
        "Core Ring": "Icon_ACC_Ring_G3_005.png",
        "Queen Ant's Ring": "Icon_ACC_Ring_G3_004.png",
        "Ring of Passion": "Icon_ACC_Ring_G3_008.png",
        "Majestic Ring": "Icon_ACC_Ring_G3_001.png",
        "Forgotten Hero's Ring": "Icon_ACC_Ring_G3_009.png",
        "Desperion's Ring": "Icon_ACC_Ring_G2_001.png",
        
        # ============================================
        # PVP BELT
        # ============================================
        "Blue": "Icon_ACC_Belt_G3_004.png",
        "Ekimus' Belt": "Icon_ACC_Belt_G3_003.png",
        "Dragon Belt": "Icon_ACC_Belt_G3_001.png",
        "Tiat's Belt": "Icon_ACC_Belt_G3_002.png",
        "Eratone's Belt": "Icon_ACC_Belt_G3_003_UHLGN0X.png",
        "Lord's Authority": "Icon_ACC_Belt_G2_001.png",
        "Maphr's Belt": "Icon_ACC_Belt_G2_002.png",
    }
    
    return mapping.get(label_str)

@register.filter
def get_field_image(field_label):
    """Returns the question image for a specific field label."""
    label_str = str(field_label).strip().lower()
    
    mapping = {
        # Soul Progression
        "soul progression attack": "Icon_SoulStone_Option_Icon_01.png",
        "soul progression defense": "Icon_SoulStone_Option_Icon_04.png",
        "soul progression blessing": "Icon_SoulStone_Option_Icon_07.png",
        
        # Enchant Accessories
        "bracelet of holy protection": "Icon_ACC_BMBracelet_G0_003.png",
        "bracelet of influence": "Icon_ACC_BMBracelet_G0_001.png",
        "earth dragon's earring": "Icon_ACC_BMEarring_G0_002.png",
        "fire dragon's earring": "Icon_ACC_BMEarring_G0_001.png",
        "eva's seal": "Icon_ACC_Seal_G0_001.png",
        "aster": "вопрос_PiWb3ob.png",
        
        # Inheritor Books
        "inheritor": "Icon_Item_Usable_SkillBook_04.png",
        "buku inheritor": "Icon_Item_Usable_SkillBook_04.png",
        
        # PvP Equipment Labels
        "pvp helmet": "armor_helmet_Majestic_Circlet.png",
        "pvp gloves": "armor_gloves_Majestic_Gloves.png",
        "pvp boots": "armor_shoes_Majestic_Boots.png",
        "pvp gaiters": "armor_bottoms_Crystal_gaiters.png",
        "pvp top armor": "armor_armor_Majestic_Robe.png",
        "pvp cloak": "armor_cloak_Freya's_Cloak.png",
        "pvp sigil": "armor_sigil_Dream_Sigil.png",
        "pvp necklace": "Icon_ACC_Necklace_G3_001.png",
        "pvp ring": "Icon_ACC_Ring_G3_001.png",
        "pvp belt": "Icon_ACC_Belt_G3_001.png",
        "pvp t-shirt": "armor_tshirt_Focus_Shirt.png",
        "weapon": "Icon_WP_Spear_G3_001.png",
    }
    
    # Partial match check
    for key, val in mapping.items():
        if key in label_str:
            return val
    return None

@register.filter
def is_video(filename):
    """Checks if filename ends with webm or mp4"""
    if not filename: return False
    return filename.lower().endswith(('.webm', '.mp4'))
