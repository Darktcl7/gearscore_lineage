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
    return field_name in ('weapon', 'weapon_enchant', 'pvp_belt', 'pvp_belt_enchant', 'pvp_ring_left', 'pvp_ring_left_enchant', 'pvp_ring_right', 'pvp_ring_right_enchant', 'pvp_necklace', 'pvp_necklace_enchant', 'pvp_sigil', 'pvp_sigil_enchant', 'pvp_helmet', 'pvp_helmet_enchant', 'pvp_gloves', 'pvp_gloves_enchant', 'pvp_boots', 'pvp_boots_enchant', 'pvp_gaiters', 'pvp_gaiters_enchant', 'pvp_top_armor', 'pvp_top_armor_enchant', 'pvp_cloak', 'pvp_cloak_enchant')



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
        'epic_agathions_count', 'total_legend_codex'
    ]
    return field_name in gearscore_fields

@register.filter
def get_image_for_choice(label):
    """Returns the image filename for a given choice label."""
    label_str = str(label).strip()
    
    mapping = {
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
        "Blue Wolf Helmet +6+": "Icon_AR_Helmet_G4_003.png",
        "Other blue or lower": "вопрос_PiWb3ob.png",
        "Majestic Circlet +5 and lower": "Icon_AR_Helmet_G3_001.png",
        "Majestic Circlet +6+": "Icon_AR_Helmet_G3_001_12BgilV.png",
        "Helm of Nightmares +5 and lower": "Icon_AR_Helmet_G3_003.png",
        "Helm of Nightmares +6+": "Icon_AR_Helmet_G3_003_Da4OSr5.png",
        "Dark Crystal Helmet +5 and lower": "Icon_AR_Helmet_G3_002.png",
        "Dark Crystal Helmet +6+": "Icon_AR_Helmet_G3_002_qiXAwPl.png",
        "Medusa's Helm +5 and lower": "Icon_AR_Helmet_G3_004.png",
        "Medusa's Helm +6+": "Icon_AR_Helmet_G3_004_x6k8OQn.png",
        "Paulina's Helmet +7 and lower": "Icon_AR_Helmet_G3_005.png",
        "Paulina's Helmet +8+": "Icon_AR_Helmet_G3_005_8Gob2sb.png",
        "Nevit's Helmet +7 and lower": "Icon_AR_Helmet_G3_006.png",
        "Nevit's Helmet +8+": "Icon_AR_Helmet_G3_006_psXukqD.png",
        "Tersi's Circlet +7 and lower": "Icon_AR_Helmet_G3_007.png",
        "Tersi's Circlet +8+": "Icon_AR_Helmet_G3_007_E2ONqpB.png",
        "Ancient Elven Helm +5 and lower": "Icon_AR_Helmet_G3_009.png",
        "Ancient Elven Helm +6+": "Icon_AR_Helmet_G3_009_8QSGd23.png",
        "Imperial Crusader Helmet": "Icon_AR_Helmet_G2_003.png",
        "Major Arcana Circlet": "Icon_AR_Helmet_G2_002.png",
        "Draconic Helmet": "Icon_AR_Helmet_G2_001.png",
        
        # ============================================
        # PVP GLOVES
        # ============================================
        "Blue Wolf Gloves +6+": "Icon_AR_Gloves_G4_006.png",
        "Majestic Gloves +5 and lower": "Icon_AR_Gloves_G3_001.png",
        "Majestic Gloves +6+": "Icon_AR_Gloves_G3_001_QaM3cf3.png",
        "Gauntlets of Nightmare +5 and lower": "Icon_AR_Gloves_G3_002.png",
        "Gauntlets of Nightmare +6+": "Icon_AR_Gloves_G3_002_a6HUtJf.png",
        "Dark Crystal Gloves +5 and lower": "Icon_AR_Gloves_G3_003.png",
        "Dark Crystal Gloves +6+": "Icon_AR_Gloves_G3_003_0lMiEvB.png",
        "Tersi's Gloves +7 and lower": "Icon_AR_Gloves_G3_004.png",
        "Tersi's Gloves +8+": "Icon_AR_Gloves_G3_004_pf1nYus.png",
        "Paulina's Gauntlets +7 and lower": "Icon_AR_Gloves_G3_005.png",
        "Paulina's Gauntlets +8+": "Icon_AR_Gloves_G3_005_LlGO3gz.png",
        "Nevit's Gloves +7 and lower": "Icon_AR_Gloves_G3_006.png",
        "Nevit's Gloves +8+": "Icon_AR_Gloves_G3_006_gN9Tvux.png",
        "Jarngreipr +5 and lower": "Icon_AR_Gloves_G3_007.png",
        "Jarngreipr +6+": "Icon_AR_Gloves_G3_007_3CSZCRG.png",
        "Vision Guardian +7 and lower": "Icon_AR_Gloves_G3_008.png",
        "Vision Guardian +8+": "Icon_AR_Gloves_G3_008_xqIeU8n.png",
        "Gloves of Blessing +5 and lower": "Icon_AR_Gloves_G3_009.png",
        "Gloves of Blessing +6+": "Icon_AR_Gloves_G3_009_RGaCLCh.png",
        "Forgotten Hero Gloves +7 and lower": "Icon_AR_Gloves_G3_010.png",
        "Forgotten Hero Gloves +8+": "Icon_AR_Gloves_G3_010_LhjNydA.png",
        "Demon's Gauntlets +5 and lower": "Icon_AR_Gloves_G3_011.png",
        "Demon's Gauntlets +6+": "Icon_AR_Gloves_G3_011_Z5XcE6l.png",
        "Ancient Elven Gauntlet +5 and lower": "Icon_AR_Gloves_G3_012.png",
        "Ancient Elven Gauntlet +6+": "Icon_AR_Gloves_G3_012_RMJdCVy.png",
        "Draconic Leather Gloves": "Icon_AR_Gloves_G2_001.png",
        "Pa'agrio's Flames": "Icon_AR_Gloves_G2_002.png",
        
        # ============================================
        # PVP BOOTS
        # ============================================
        "Blue Wolf Boots +6+": "Icon_AR_Boots_G4_006.png",
        "Majestic Boots +5 or lower": "Icon_AR_Boots_G3_001.png",
        "Majestic Boots +6+": "Icon_AR_Boots_G3_001_yojHyx3.png",
        "Boots of Nightmares +5 or lower": "Icon_AR_Boots_G3_002.png",
        "Boots of Nightmares +6+": "Icon_AR_Boots_G3_002_bJTsB6w.png",
        "Dark Crystal Boots +5 or lower": "Icon_AR_Boots_G3_003.png",
        "Dark Crystal Boots +6+": "Icon_AR_Boots_G3_003_9XLJ0Bl.png",
        "Tersi's Boots +7 or lower": "Icon_AR_Boots_G3_004.png",
        "Tersi's Boots +8+": "Icon_AR_Boots_G3_004_c4B8NWF.png",
        "Paulina's Boots +7 or lower": "Icon_AR_Boots_G3_005.png",
        "Paulina's Boots +8+": "Icon_AR_Boots_G3_005_Rl4fZQt.png",
        "Nevit's Boots +7 or lower": "Icon_AR_Boots_G3_006.png",
        "Nevit's Boots +8+": "Icon_AR_Boots_G3_006_qvxjIlC.png",
        "Demon's Boots +5 or lower": "Icon_AR_Boots_G3_007.png",
        "Demon's Boots +6+": "Icon_AR_Boots_G3_007_3z1VnBd.png",
        "Kaliel's Boots +7 or lower": "Icon_AR_Boots_G3_008.png",
        "Kaliel's Boots +8+": "Icon_AR_Boots_G3_008_qmLQJcb.png",
        "Forgotten's Hero Boots +7 and lower": "Icon_AR_Boots_G3_009.png",
        "Forgotten's Hero Boots +8+": "Icon_AR_Boots_G3_009_J5iS6W4.png",
        "Ancient Elven Boots +5 and lower": "Icon_AR_Boots_G3_010.png",
        "Ancient Elven Boots +6+": "Icon_AR_Boots_G3_010_NSejBgl.png",
        "Draconic": "Icon_AR_Boots_G2_001.png",
        "Sayha's Wind": "Icon_AR_Boots_G2_002.png",
        
        # ============================================
        # PVP GAITERS (PANTS)
        # ============================================
        "Blue Wolf Gaiters +6+": "Icon_AR_Pants_G4_003.png",
        "Basila Skin +6+": "Icon_AR_Pants_G4_004.png",
        "Blood Gaiters +5 and lower": "Icon_AR_Pants_G3_001.png",
        "Blood Gaiters +6+": "Icon_AR_Pants_G3_001_mcaXulV.png",
        "Gaiters of Light +5 and lower": "Icon_AR_Pants_G3_002.png",
        "Gaiters of Light +6+": "Icon_AR_Pants_G3_002_zIKnuHJ.png",
        "Gaiters of Ice +5 and lower": "Icon_AR_Pants_G3_003.png",
        "Gaiters of Ice +6+": "Icon_AR_Pants_G3_003_yhjUAYi.png",
        "Shilen's Breath +5 and lower": "Icon_AR_Pants_G3_004.png",
        "Shilen's Breath +6+": "Icon_AR_Pants_G3_004_a8jdSeN.png",
        "Crystal Gaiters +5 and lower": "Icon_AR_Pants_G3_005.png",
        "Crystal Gaiters +6+": "Icon_AR_Pants_G3_005_Uo0dsov.png",
        "Forgotten Hero's Gaiters +5 and lower": "Icon_AR_Pants_G3_006.png",
        "Forgotten Hero's Gaiters +6+": "Icon_AR_Pants_G3_006_23eAWTU.png",
        "Imperial Crusader Gaiters": "Icon_AR_Pants_G2_001.png",
        
        # ============================================
        # PVP ARMOR (TORSO)
        # ============================================
        "Blue Wolf Breastplate +6+": "Icon_AR_Torso_G4_004.png",
        "Majestic Robe +5 and lower": "Icon_AR_Torso_G3_001.png",
        "Majestic Robe +6+": "Icon_AR_Torso_G3_001_sLOin8b.png",
        "Armor of Nightmares +5 and lower": "Icon_AR_Torso_G3_002.png",
        "Armor of Nightmares +6+": "Icon_AR_Torso_G3_002_xOGwcXB.png",
        "Dark Crystal Breastplate +5 and lower": "Icon_AR_Torso_G3_003.png",
        "Dark Crystal Breastplate +6+": "Icon_AR_Torso_G3_003_7Rqn8ca.png",
        "Tersi's Robe +7 and lower": "Icon_AR_Torso_G3_004.png",
        "Tersi's Robe +8+": "Icon_AR_Torso_G3_004_dsf80Kl.png",
        "Paulina's Breastplate +7 and lower": "Icon_AR_Torso_G3_005.png",
        "Paulina's Breastplate +8+": "Icon_AR_Torso_G3_005_Gp54AHt.png",
        "Nevit's Armor +7 and lower": "Icon_AR_Torso_G3_006.png",
        "Nevit's Armor +8+": "Icon_AR_Torso_G3_006_W0k8PmT.png",
        "Savan's Robe +5 and lower": "Icon_AR_Torso_G3_007.png",
        "Savan's Robe +6+": "Icon_AR_Torso_G3_007_8kkO6Yq.png",
        "Absolute Tunic +5 and lower": "Icon_AR_Torso_G3_008.png",
        "Absolute Tunic +6+": "Icon_AR_Torso_G3_008_s9rihDJ.png",
        "Apella Plate Armor +5 and lower": "Icon_AR_Torso_G3_009.png",
        "Apella Plate Armor +6+": "Icon_AR_Torso_G3_009_jZC8lV4.png",
        "Forgotten Hero's Breastplate +7 and lower": "Icon_AR_Torso_G3_010.png",
        "Forgotten Hero's Breastplate +8+": "Icon_AR_Torso_G3_010_9ECFQbt.png",
        "Ancient Elven Armor +5 and lower": "Icon_AR_Torso_G3_011.png",
        "Ancient Elven Armor +6+": "Icon_AR_Torso_G3_011_tjIhiVB.png",
        "Demon's Armor +5 and lower": "Icon_AR_Torso_G3_012.png",
        "Demon's Armor +6+": "Icon_AR_Torso_G3_012_T1bL2wA.png",
        "Draconic Leather Armor": "Icon_AR_Torso_G2_001.png",
        "Major Arcana Robe": "Icon_AR_Torso_G2_002.png",
        "Imperial Crusader Breastplate": "Icon_AR_Torso_G2_003.png",
        
        # ============================================
        # PVP CLOAK (CAPE)
        # ============================================
        "Silver Cloak +7+": "Icon_AR_Cape_G5_003.png",
        "Cranigg's Cloak +6+": "Icon_AR_Cape_G4_006.png",
        "Other blue or green cloak": "вопрос_PiWb3ob.png",
        "Dragon's Scale +5 or lower": "Icon_AR_Cape_G3_001.png",
        "Dragon's Scale +6+": "Icon_AR_Cape_G3_001_SFLdNyU.png",
        "Zaken's Cloak +5 or lower": "Icon_AR_Cape_G3_002.png",
        "Zaken's Cloak +6+": "Icon_AR_Cape_G3_002_EWwkM2B.png",
        "Cloak of Freya +5 or lower": "Icon_AR_Cape_G3_003.png",
        "Cloak of Freya +6+": "Icon_AR_Cape_G3_003_TlWsloP.png",
        "Queen Ant's Wing +5 or lower": "Icon_AR_Cape_G3_004.png",
        "Queen Ant's Wing +6+": "Icon_AR_Cape_G3_004_skqdoKn.png",
        "Cloak of Silence +5 or lower": "Icon_AR_Cape_G3_005.png",
        "Cloak of Silence +6+": "Icon_AR_Cape_G3_005_vObJqD0.png",
        "Eigis Cloak +5 or lower": "Icon_AR_Cape_G3_006.png",
        "Eigis Cloak +6+": "Icon_AR_Cape_G3_006_Xgvr1WM.png",
        "Cloak of Authority +5 or lower": "Icon_AR_Cape_G3_007.png",
        "Cloak of Authority +6+": "Icon_AR_Cape_G3_007_KG43izQ.png",
        "Selihoden's Wing +5 and lower": "Icon_AR_Cape_G3_008.png",
        "Selihoden's Wing +6+": "Icon_AR_Cape_G3_008_x9bE1zn.png",
        "Nevit's Cloak of Light": "Icon_AR_Cape_G2_001.png",
        "Nailop's Cloak": "Icon_AR_Cape_G2_002.png",
        
        # ============================================
        # PVP SIGIL
        # ============================================
        "Dream Sigil +3-4": "Icon_AR_Sigil_G4_001.png",
        "Dream Sigil +5+": "Icon_AR_Sigil_G4_001_b7RRbS3.png",
        "Blue (other) and lower": "вопрос_PiWb3ob.png",
        "Susceptor's Heart +0": "Icon_AR_Sigil_G3_001.png",
        "Susceptor's Heart +1-3": "Icon_AR_Sigil_G3_001_ZdLf7Rk.png",
        "Susceptor's Heart +4+": "Icon_AR_Sigil_G3_001_cjGV7fS.png",
        "Paradia's Sigil +0": "Icon_AR_Sigil_G3_002.png",
        "Paradia's Sigil +1-3": "Icon_AR_Sigil_G3_002_3svNdEv.png",
        "Paradia's Sigil +4+": "Icon_AR_Sigil_G3_002_gm3pIHV.png",
        "Cruma's Shell +0": "Icon_AR_Sigil_G3_003.png",
        "Cruma's Shell +1-3": "Icon_AR_Sigil_G3_003_6G2vZML.png",
        "Cruma's Shell +4+": "Icon_AR_Sigil_G3_003_p0QF4DL.png",
        "Sigil of Flames +0": "Icon_AR_Sigil_G3_004.png",
        "Sigil of Flames +1-3": "Icon_AR_Sigil_G3_004_8shuYnY.png",
        "Sigil of Flames +4+": "Icon_AR_Sigil_G3_004_s6eH0wI.png",
        "Jaeger's Sigil +0": "Icon_AR_Sigil_G3_005.png",
        "Jaeger's Sigil +1-3": "Icon_AR_Sigil_G3_005_a4GBCoO.png",
        "Jaeger's Sigil +4+": "Icon_AR_Sigil_G3_005_uO92b9h.png",
        "Selihoden's Horn +0": "Icon_AR_Sigil_G3_006.png",
        "Selihoden's Horn +1-3": "Icon_AR_Sigil_G3_006_EsorO1X.png",
        "Selihoden's Horn +4+": "Icon_AR_Sigil_G3_006_pXmzZJX.png",
        "Tear of Darkness": "Icon_AR_Sigil_G2_001.png",
        "Draconic Sigil": "Icon_AR_Sigil_G2_002.png",
        "Arcana Sigil": "Icon_AR_Sigil_G2_003.png",
        # Base sigil names (new format)
        "Dream Sigil": "Icon_AR_Sigil_G4_001.png",
        "Blue": "вопрос_PiWb3ob.png",
        "Susceptor's Heart": "Icon_AR_Sigil_G3_001.png",
        "Paradia's Sigil": "Icon_AR_Sigil_G3_002.png",
        "Cruma's Shell": "Icon_AR_Sigil_G3_003.png",
        "Sigil of Flames": "Icon_AR_Sigil_G3_004.png",
        "Jaeger's Sigil": "Icon_AR_Sigil_G3_005.png",
        "Selihoden's Horn": "Icon_AR_Sigil_G3_006.png",
        
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
        
        # Inheritor Books
        "inheritor": "Icon_Item_Usable_SkillBook_04.png",
        "buku inheritor": "Icon_Item_Usable_SkillBook_04.png",
        
        # PvP Equipment Labels
        "pvp helmet": "Icon_AR_Helmet_G3_001.png",
        "pvp gloves": "Icon_AR_Gloves_G3_001.png",
        "pvp boots": "Icon_AR_Boots_G3_001.png",
        "pvp gaiters": "Icon_AR_Pants_G3_001.png",
        "pvp top armor": "Icon_AR_Torso_G3_001.png",
        "pvp cloak": "Icon_AR_Cape_G3_001.png",
        "pvp sigil": "Icon_AR_Sigil_G3_001.png",
        "pvp necklace": "Icon_ACC_Necklace_G3_001.png",
        "pvp ring": "Icon_ACC_Ring_G3_001.png",
        "pvp belt": "Icon_ACC_Belt_G3_001.png",
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