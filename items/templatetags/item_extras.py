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
        'epic_agathions_count', 'total_legend_codex', 'total_epic_mount'
    ]
    return field_name in gearscore_fields

@register.filter
def is_expertise_field(field_name):
    """Check if a field belongs to Expertise section."""
    return str(field_name).startswith('exp_')

@register.filter
def get_image_for_choice(label):
    """Returns the image filename for a given choice label."""
    label_str = str(label).strip()
    
    mapping = {
        # ============================================
        # MYTHIC CLASSES
        # ============================================
        "No mythic class": "х3.png",
        "Elcadia": "Icon_Classcard_Elcadia.png",
        "Elhwynha": "Icon_Classcard_Elhwynha.png",
        "Raoul": "Icon_Classcard_Raoul.png",

        # ============================================
        # LEGENDARY CLASSES
        # ============================================
        "Demon Slayer": "Zariche.png",
        "Scryde": "Icon_Classcard_Scryde.png",
        "Lionel Hunter": "Icon_Classcard_LionelHunter.png",
        "Aria": "Icon_Classcard_Aria.png",
        "Veora": "Icon_Classcard_Veora.png",
        "Solina": "Icon_Classcard_Solina.png",
        "Regina": "Icon_Classcard_Regina.png",
        "Daphne": "Icon_Classcard_Daphne.png",
        "Amadeo Cadmus": "Icon_Classcard_AmadeoCadmus.png",
        "Bartz": "Icon_Classcard_Bartz.png",
        "Etis Von Etina": "Icon_Classcard_EtisVonEtina.jpg",
        "Frintezza": "Icon_Classcard_Frintezza.jpg",
        "Kranvel": "Icon_Classcard_Kranvel.jpg",
        "No legendary class": "х3.png",

        # ============================================
        # LEGENDARY AGATHIONS
        # ============================================
        "No legendary agathions": "х3.png",
        "Zarich": "Icon_Agathion_Zariche.png",
        "Orfen": "Icon_Agathion_Orfen.png",
        "Baium": "Icon_Agathion_Baium.png",
        "Anakim": "Icon_Agathion_Anakim.png",
        "Lilith": "Icon_Agathion_Lilith.png",
        "Timiniel": "Icon_Agathion_Timiniel.png",
        "Abyssal Death Knight": "Icon_Agathion_AbyssalDeathKnight.png",
        "Akamanah": "Icon_Agathion_Akamanah.png",
        
        # ============================================
        # LEGENDARY MOUNTS
        # ============================================
        "No legendary mount": "х3.png",
        "Cerberus": "Icon_Mount_Cerberus.png",
        "Freyja": "Icon_Mount_Freyja.png",
        "Lucis": "Icon_Mount_Lucis.png",
        
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
        "Blue necklace +3-4": "Icon_ACC_Necklace_G4_007.png",
        "Blue necklace +5+": "Icon_ACC_Necklace_G4_007_OUFSufM.png",
        "Blue (other) and lower": "вопрос_PiWb3ob.png",
        "Necklace of Immortality +0": "Icon_ACC_Necklace_G3_001.png",
        "Necklace of Immortality +1-3": "Icon_ACC_Necklace_G3_001_lAVquC3.png",
        "Necklace of Immortality +4+": "Icon_ACC_Necklace_G3_001_tZ9U10V.png",
        "Lilith's Soul Necklace +0": "Icon_ACC_Necklace_G3_002.png",
        "Lilith's Soul Necklace +1-3": "Icon_ACC_Necklace_G3_002_OS11uSl.png",
        "Lilith's Soul Necklace +4+": "Icon_ACC_Necklace_G3_002_XWs1dCe.png",
        "Anakeem's Soul Necklace +0": "Icon_ACC_Necklace_G3_002.png",
        "Anakeem's Soul Necklace +1-3": "Icon_ACC_Necklace_G3_002_OS11uSl.png",
        "Anakeem's Soul Necklace +4+": "Icon_ACC_Necklace_G3_002_XWs1dCe.png",
        "Necklace of Valakas +0": "Icon_ACC_Necklace_G3_003.png",
        "Necklace of Valakas +1-3": "Icon_ACC_Necklace_G3_003_REExzLz.png",
        "Necklace of Valakas +4+": "Icon_ACC_Necklace_G3_003_wD01uUH.png",
        "Valakas' Necklace +0": "Icon_ACC_Necklace_G3_003.png",
        "Frintezza's Necklace +0": "Icon_ACC_Necklace_G3_004.png",
        "Frintezza's Necklace +1-3": "Icon_ACC_Necklace_G3_004_FiVflic.png",
        "Frintezza's Necklace +4+": "Icon_ACC_Necklace_G3_004_e28xJ1h.png",
        "Necklace of Hrunting +0": "Icon_ACC_Necklace_G3_005.png",
        "Necklace of Hrunting +1-3": "Icon_ACC_Necklace_G3_005_b99XXwc.png",
        "Necklace of Hrunting +4+": "Icon_ACC_Necklace_G3_005_oiY0FLh.png",
        "Antharas' Necklace +0": "Icon_ACC_Necklace_G3_006.png",
        "Antharas' Necklace +1-3": "Icon_ACC_Necklace_G3_006_0S0wnA6.png",
        "Antharas' Necklace +4+": "Icon_ACC_Necklace_G3_006_iaZMJWj.png",
        "Antharas Necklace +0": "Icon_ACC_Necklace_G3_006.png",
        "Blessed Antharas' Necklace +0": "Icon_ACC_Necklace_G3_007.png",
        "Blessed Antharas' Necklace +1-3": "Icon_ACC_Necklace_G3_007_G5dCVLh.png",
        "Blessed Antharas' Necklace +4+": "Icon_ACC_Necklace_G3_007_TA6r7zT.png",
        "Baium's Necklace +0": "Icon_ACC_Necklace_G3_001.png",
        "Baium's Necklace +1-3": "Icon_ACC_Necklace_G3_001_lAVquC3.png",
        "Baium's Necklace +4+": "Icon_ACC_Necklace_G3_001_tZ9U10V.png",
        "Zaken's Necklace +0": "Icon_ACC_Necklace_G3_004.png",
        "Zaken's Necklace +1-3": "Icon_ACC_Necklace_G3_004_FiVflic.png",
        "Zaken's Necklace +4+": "Icon_ACC_Necklace_G3_004_e28xJ1h.png",
        "Orfen's Necklace +0": "Icon_ACC_Necklace_G2_002.png",
        "Orfen's Necklace +1-3": "Icon_ACC_Necklace_G2_002.png",
        "Orfen's Necklace +4+": "Icon_ACC_Necklace_G2_002.png",
        "Majestic Necklace +0": "Icon_ACC_Necklace_G3_001.png",
        "Majestic Necklace +1-3": "Icon_ACC_Necklace_G3_001_lAVquC3.png",
        "Majestic Necklace +4+": "Icon_ACC_Necklace_G3_001_tZ9U10V.png",
        "Apella Necklace +0": "Icon_ACC_Necklace_G3_001.png",
        "Apella Necklace +1-3": "Icon_ACC_Necklace_G3_001_lAVquC3.png",
        "Apella Necklace +4+": "Icon_ACC_Necklace_G3_001_tZ9U10V.png",
        "Lindvior's Necklace +0": "Icon_ACC_Necklace_G3_006.png",
        "Archmage Necklace +0": "Icon_ACC_Necklace_G3_001.png",
        "Queen Ant's Souled Necklace": "Icon_ACC_Necklace_G2_001.png",
        "Orfen's Necklace": "Icon_ACC_Necklace_G2_002.png",
        "Core's Necklace": "Icon_ACC_Necklace_G2_003.png",
        "Blessed Valakas' Necklace": "Icon_ACC_Necklace_G2_004.png",
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
        "Archmage Necklace": "Icon_ACC_Necklace_G3_001.png",
        
        # ============================================
        # PVP RINGS
        # ============================================
        "Blue ring +3-4": "Icon_ACC_Ring_G4_010.png",
        "Blue ring +5+": "Icon_ACC_Ring_G4_010_iKhk3KB.png",
        "Ring of Blessing +3+": "Icon_ACC_Ring_G4_010.png",
        "Other blue or lower": "вопрос_PiWb3ob.png",
        "Ring of Baium +0": "Icon_ACC_Ring_G3_001.png",
        "Ring of Baium +1-3": "Icon_ACC_Ring_G3_001_8kwlekG.png",
        "Ring of Baium +4+": "Icon_ACC_Ring_G3_001_KZGqaKy.png",
        "Baium's Ring +0": "Icon_ACC_Ring_G3_001.png",
        "Baium's Ring +1-3": "Icon_ACC_Ring_G3_001_8kwlekG.png",
        "Baium's Ring +4+": "Icon_ACC_Ring_G3_001_KZGqaKy.png",
        "Antharas' Ring +0": "Icon_ACC_Ring_G3_002.png",
        "Antharas' Ring +1-3": "Icon_ACC_Ring_G3_002_0NZX3nn.png",
        "Antharas' Ring +4+": "Icon_ACC_Ring_G3_002_Lb8Ne6y.png",
        "Frintezza's Ring +0": "Icon_ACC_Ring_G3_003.png",
        "Frintezza's Ring +1-3": "Icon_ACC_Ring_G3_003_65NYCI3.png",
        "Frintezza's Ring +4+": "Icon_ACC_Ring_G3_003_9N9N6dn.png",
        "Queen Ant's Ring +0": "Icon_ACC_Ring_G3_004.png",
        "Queen Ant's Ring +1-3": "Icon_ACC_Ring_G3_004_9WdXrdt.png",
        "Queen Ant's Ring +4+": "Icon_ACC_Ring_G3_004_aOaKpsn.png",
        "Ring of Core +0": "Icon_ACC_Ring_G3_005.png",
        "Ring of Core +1-3": "Icon_ACC_Ring_G3_005_A63H9uZ.png",
        "Ring of Core +4+": "Icon_ACC_Ring_G3_005_EmbEpH0.png",
        "Core Ring +0": "Icon_ACC_Ring_G3_005.png",
        "Core Ring +1-3": "Icon_ACC_Ring_G3_005_A63H9uZ.png",
        "Core Ring +4+": "Icon_ACC_Ring_G3_005_EmbEpH0.png",
        "Ring of Hrunting +0": "Icon_ACC_Ring_G3_006.png",
        "Ring of Hrunting +1-3": "Icon_ACC_Ring_G3_006_AlrIaxF.png",
        "Ring of Hrunting +4+": "Icon_ACC_Ring_G3_006_BeR09N3.png",
        "Blessed Antharas' Ring +0": "Icon_ACC_Ring_G3_007.png",
        "Blessed Antharas' Ring +1-3": "Icon_ACC_Ring_G3_007_Jt1mnj3.png",
        "Blessed Antharas' Ring +4+": "Icon_ACC_Ring_G3_007_ckB2Fpj.png",
        "Ring of Insolence +0": "Icon_ACC_Ring_G3_008.png",
        "Ring of Insolence +1-3": "Icon_ACC_Ring_G3_008_1BUxW3v.png",
        "Ring of Insolence +4+": "Icon_ACC_Ring_G3_008_VJyhEoe.png",
        "Blessed Baium's Ring +0": "Icon_ACC_Ring_G3_009.png",
        "Blessed Baium's Ring +1-3": "Icon_ACC_Ring_G3_009_4AN8uSW.png",
        "Blessed Baium's Ring +4+": "Icon_ACC_Ring_G3_009_6xzYOmn.png",
        "Lilith's Ring +0": "Icon_ACC_Ring_G3_003.png",
        "Lilith's Ring +1-3": "Icon_ACC_Ring_G3_003_65NYCI3.png",
        "Lilith's Ring +4+": "Icon_ACC_Ring_G3_003_9N9N6dn.png",
        "Anakeem's Ring +0": "Icon_ACC_Ring_G3_003.png",
        "Anakeem's Ring +1-3": "Icon_ACC_Ring_G3_003_65NYCI3.png",
        "Anakeem's Ring +4+": "Icon_ACC_Ring_G3_003_9N9N6dn.png",
        "Vereth's Ring +0": "Icon_ACC_Ring_G3_006.png",
        "Vereth's Ring +1-3": "Icon_ACC_Ring_G3_006_AlrIaxF.png",
        "Vereth's Ring +4+": "Icon_ACC_Ring_G3_006_BeR09N3.png",
        "Ring of Passion +0": "Icon_ACC_Ring_G3_008.png",
        "Ring of Passion +1-3": "Icon_ACC_Ring_G3_008_1BUxW3v.png",
        "Ring of Passion +4+": "Icon_ACC_Ring_G3_008_VJyhEoe.png",
        "Majestic Ring +0": "Icon_ACC_Ring_G3_001.png",
        "Majestic Ring +1-3": "Icon_ACC_Ring_G3_001_8kwlekG.png",
        "Majestic Ring +4+": "Icon_ACC_Ring_G3_001_KZGqaKy.png",
        "Forgotten Hero's Ring +0": "Icon_ACC_Ring_G3_009.png",
        "Forgotten Hero's Ring +1-3": "Icon_ACC_Ring_G3_009_4AN8uSW.png",
        "Forgotten Hero's Ring +4+": "Icon_ACC_Ring_G3_009_6xzYOmn.png",
        "Desperion's Ring": "Icon_ACC_Ring_G2_001.png",
        "Ring of Orfen": "Icon_ACC_Ring_G2_001.png",
        # Base ring names (new format without enchant)
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
        
        # ============================================
        # PVP BELT
        # ============================================
        "Blue +3-4": "Icon_ACC_Belt_G3_004.png",
        "Blue +5+": "Icon_ACC_Belt_G3_004_7MqECuK.png",
        "Blue belt +3-4": "Icon_ACC_Belt_G3_004.png",
        "Blue belt +5+": "Icon_ACC_Belt_G3_004_7MqECuK.png",
        "Anakim's Belt +0": "Icon_ACC_Belt_G3_001.png",
        "Anakim's Belt +1-3": "Icon_ACC_Belt_G3_001_GxLx0Kg.png",
        "Anakim's Belt +4+": "Icon_ACC_Belt_G3_001_mgLa9iS.png",
        "Lilith's Belt +0": "Icon_ACC_Belt_G3_002.png",
        "Lilith's Belt +1-3": "Icon_ACC_Belt_G3_002_KCbTg13.png",
        "Lilith's Belt +4+": "Icon_ACC_Belt_G3_002_qCOwpYC.png",
        "Ekimus' Belt +0": "Icon_ACC_Belt_G3_003.png",
        "Ekimus' Belt +1-3": "Icon_ACC_Belt_G3_003_UHLGN0X.png",
        "Ekimus' Belt +4+": "Icon_ACC_Belt_G3_003_yiEO65W.png",
        "Eratone's Belt +0": "Icon_ACC_Belt_G3_003.png",
        "Eratone's Belt +1-3": "Icon_ACC_Belt_G3_003_UHLGN0X.png",
        "Eratone's Belt +4+": "Icon_ACC_Belt_G3_003_yiEO65W.png",
        "Dragon Belt +0": "Icon_ACC_Belt_G3_001.png",
        "Dragon Belt +1-3": "Icon_ACC_Belt_G3_001_GxLx0Kg.png",
        "Dragon Belt +4+": "Icon_ACC_Belt_G3_001_mgLa9iS.png",
        "Tiat's Belt +0": "Icon_ACC_Belt_G3_002.png",
        "Tiat's Belt +1-3": "Icon_ACC_Belt_G3_002_KCbTg13.png",
        "Tiat's Belt +4+": "Icon_ACC_Belt_G3_002_qCOwpYC.png",
        "Lord's Authority": "Icon_ACC_Belt_G2_001.png",
        "Maphr's Belt": "Icon_ACC_Belt_G2_002.png",
        # Base belt names (new format without enchant)
        "Blue": "Icon_ACC_Belt_G3_004.png",
        "Ekimus' Belt": "Icon_ACC_Belt_G3_003.png",
        "Dragon Belt": "Icon_ACC_Belt_G3_001.png",
        "Tiat's Belt": "Icon_ACC_Belt_G3_002.png",
        "Eratone's Belt": "Icon_ACC_Belt_G3_003_UHLGN0X.png",
        
        # ============================================
        
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

        # WEAPONS (from Subclass Information_files)
        # ============================================
        "Blue or lower": "вопрос_PiWb3ob.png",
        # Bow
        "Cabrio's Hand +7 or lower": "Icon_WP_Bow_G3_001.png",
        "Cabrio's Hand +8": "Icon_WP_Bow_G3_002.png",
        "Cabrio's Hand +9": "Icon_WP_Bow_G3_003.png",
        # Orb (Staff weapons)
        "Archangel Orb +7 or lower": "Icon_WP_Staff_G3_001.png",
        "Archangel Orb +8": "Icon_WP_Staff_G3_002.png",
        "Archangel Orb +9": "Icon_WP_Staff_G3_003.png",
        "Flaming Dragon Skull +7 or lower": "Icon_WP_Staff_G3_004.png",
        "Flaming Dragon Skull +8": "Icon_WP_Staff_G3_005.png",
        "Flaming Dragon Skull +9": "Icon_WP_Staff_G2_001.png",
        "Spiritual Eye +7 or lower": "Icon_WP_Staff_G3_001.png",
        "Spiritual Eye +8": "Icon_WP_Staff_G3_002.png",
        "Spiritual Eye +9": "Icon_WP_Staff_G3_003.png",
        "Arcana's Orb": "Icon_WP_Staff_G2_001.png",
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