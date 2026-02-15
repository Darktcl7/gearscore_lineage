

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



# ----------------------------------------------------

# PILIHAN (CHOICES) - DALAM BAHASA INDONESIA

# ----------------------------------------------------



CLASS_CHOICES = (
    ('One-Handed Sword Skill', 'One-Handed Sword Skill'),
    ('Dual-Wield Skills', 'Dual-Wield Skills'),
    ('Dagger Skill', 'Dagger Skill'),
    ('Bow Skill', 'Bow Skill'),
    ('Staff Skill', 'Staff Skill'),
    ('Greatsword Skill', 'Greatsword Skill'),
    ('Crossbow Skill', 'Crossbow Skill'),
    ('Chainsword Skill', 'Chainsword Skill'),
    ('Rapier Skill', 'Rapier Skill'),
    ('Magic Cannon Skill', 'Magic Cannon Skill'),
    ('Spear Skill', 'Spear Skill'),
    ('Orb Skill', 'Orb Skill'),
    ('Dual Axe Skill', 'Dual Axe Skill'),
    ('Soul Breaker Skill', 'Soul Breaker Skill'),
)



CLAN_CHOICES = (

    ('Valkyrie', 'Valkyrie'),

)



EPIC_CLASSES_CHOICES = (

    ('0', '0'),

    ('1-4', '1-4'),

    ('5-9', '5-9'),

    ('10-19', '10-19'),

    ('20-29', '20-29'),

    ('30-39', '30-39'),

)



EPIC_AGATHIONS_CHOICES = (

    ('0', '0'),

    ('1-4', '1-4'),

    ('5-9', '5-9'),

    ('10-20', '10-20'),

)



SOULSHOT_VALOR_CHOICES = (

    ('5-3', '5-3 ke bawah'),

    ('6', 'dari 6 sampai 6-3'),

    ('7', 'dari 7 sampai 7-3'),

    ('8', 'dari 8 sampai 8-3'),

    ('9', 'dari 9 sampai 9-3'),

    ('10', 'dari 10 sampai 10-2'),

    ('10-3', '10-3'),

)



SOUL_PROGRESSION_CHOICES = (

    ('0', '0'),

    ('1-4', '1-4'),

    ('5-9', '5-9'),

    ('10-14', '10-14'),

    ('15', '15'),

)



ENCHANT_CHOICES = (

    (0, 'Tidak ada'),

    (1, '+1'), (2, '+2'), (3, '+3'), (4, '+4'),

    (5, '+5'), (6, '+6'), (7, '+7'), (8, '+8'),

)



# ----------------------------------------------------

# MODELS

# ----------------------------------------------------



class DiscordAlarm(models.Model):
    DAYS = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ]
    day = models.IntegerField(choices=DAYS)
    time = models.TimeField()
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_day_display()} - {self.time} - {self.message[:20]}..."

class DiscordAnnouncement(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Announcement ({self.created_at}) - Sent: {self.is_sent}"

class Item(models.Model):

    name = models.CharField("Nama Item", max_length=100)

    item_type = models.CharField("Tipe Item", max_length=50)

    icon_file = models.CharField("File Ikon", max_length=100, blank=True, null=True)

    enchant_level = models.IntegerField("Level Enchant", default=0)

    grade = models.CharField("Grade", max_length=50, blank=True)

    slot = models.CharField("Slot", max_length=50, blank=True)

    attack_power = models.IntegerField("Attack Power", default=0)

    defense_power = models.IntegerField("Defense Power", default=0)




    def __str__(self):

        return self.name



class SubclassStats(models.Model):

    character = models.OneToOneField('Character', on_delete=models.CASCADE, related_name='subclass_stats')

    # ====== DUALBLADE SUBCLASS ======
    dualblade_triple_slash = models.BooleanField("Triple Slash", default=False)
    dualblade_sonic_blaster = models.BooleanField("Sonic Blaster", default=False)
    dualblade_detect_weakness = models.BooleanField("Detect Weakness", default=False)
    dualblade_dance_of_fury = models.BooleanField("Dance of Fury", default=False)
    dualblade_dual_parrying = models.BooleanField("Dual Parrying", default=False)
    dualblade_dual_impact = models.BooleanField("Dual Impact", default=False)
    dualblade_berserker = models.BooleanField("Berserker", default=False)
    dualblade_breaking_armor = models.BooleanField("Breaking Armor", default=False)
    dualblade_weapon = models.CharField("Dualblade Weapon", max_length=50, choices=[
        ('none', 'Blue or lower'),
        ('tallum', 'Tallum Dual Blades'),
        ('archangel', 'Archangel Dual Blades'),
        ('dark_legion', "Dark Legion's Edge"),
        ('mardil', "Mardil's Rage"),
        ('astaroth', "Astaroth's Blades"),
    ], default='none')

    # ====== DAGGER SUBCLASS ======
    dagger_assassin_vision = models.BooleanField("Assassin's Vision", default=False)
    dagger_shadow_blade = models.BooleanField("Shadow Blade", default=False)
    dagger_hide = models.BooleanField("Hide", default=False)
    dagger_venom = models.BooleanField("Venom", default=False)
    dagger_reset_movement = models.BooleanField("Reset Movement", default=False)
    dagger_phantom_blade = models.BooleanField("Phantom Blade", default=False)
    dagger_shadow_step = models.BooleanField("Shadow Step", default=False)
    dagger_marionette = models.BooleanField("Marionette", default=False)
    dagger_weapon = models.CharField("Dagger Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('demon', "Demon's Dagger"),
        ('archangel', 'Archangel Slayer'),
        ('cruma', "Cruma's Horn"),
        ('soul', 'Soul Separator'),
        ('naga', 'Naga Storm'),
    ], default='none')

    # ====== STAFF SUBCLASS ======
    staff_snow_storm = models.BooleanField("Snow Storm", default=False)
    staff_cancellation = models.BooleanField("Cancellation", default=False)
    staff_confuse = models.BooleanField("Confuse", default=False)
    staff_restore_casting = models.BooleanField("Restore Casting", default=False)
    staff_frozen_crystal = models.BooleanField("Frozen Crystal", default=False)
    staff_meteor = models.BooleanField("Meteor", default=False)
    staff_chaos = models.BooleanField("Chaos", default=False)
    staff_gravity = models.BooleanField("Gravity", default=False)
    staff_weapon = models.CharField("Staff Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('daimon', 'Daimon Crystal'),
        ('stakato', "Stakato Queen's Staff"),
        ('archangel', 'Archangel Staff'),
        ('mother_tree', "Mother Tree's Branch"),
        ('spirits', "Spirits' Staff"),
        ('imperial', 'Imperial Staff'),
    ], default='none')

    # ====== BOW SUBCLASS ======
    bow_death_sting = models.BooleanField("Death Sting", default=False)
    bow_mana_seeker = models.BooleanField("Mana Seeker", default=False)
    bow_real_target = models.BooleanField("Real Target", default=False)
    bow_entangle = models.BooleanField("Entangle", default=False)
    bow_impact_shot = models.BooleanField("Impact Shot", default=False)
    bow_absolute_piercing = models.BooleanField("Absolute Piercing", default=False)
    bow_elimination = models.BooleanField("Elimination", default=False)
    bow_pinpoint_shot = models.BooleanField("Pinpoint Shot", default=False)
    bow_weapon = models.CharField("Bow Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('bow_peril', 'Bow of Peril'),
        ('archangel', 'Archangel Bow'),
        ('carnium', 'Carnium Bow'),
        ('soul', 'Soul Bow'),
        ('shyeed', "Shyeed's Bow"),
    ], default='none')

    # ====== TANK (SWORD) SUBCLASS ======
    tank_double_shock = models.BooleanField("Double Shock", default=False)
    tank_iron_will = models.BooleanField("Iron Will", default=False)
    tank_vex = models.BooleanField("Vex", default=False)
    tank_touch_of_life = models.BooleanField("Touch of Life", default=False)
    tank_holy_strike = models.BooleanField("Holy Strike", default=False)
    tank_brutal_attack = models.BooleanField("Brutal Attack", default=False)
    tank_vengeance = models.BooleanField("Vengeance", default=False)
    tank_chain_strike = models.BooleanField("Chain Strike", default=False)
    tank_weapon = models.CharField("Tank Weapon", max_length=50, choices=[
        ('ssaurabi', 'Ssaurabi Long Sword'),
        ('none', 'Other blue or lower or none'),
        ('sirra', "Sirra's Blade"),
        ('archangel', 'Archangel Blade'),
        ('valhalla', 'Sword of Valhalla'),
        ('miracles', 'Sword of Miracles'),
        ('caladbolg', 'Caladbolg'),
    ], default='none')

    # ====== SPEAR SUBCLASS ======
    spear_frenzy = models.BooleanField("Frenzy", default=False)
    spear_vital_destruction = models.BooleanField("Vital Destruction", default=False)
    spear_infinity_strike = models.BooleanField("Infinity Strike", default=False)
    spear_disarm = models.BooleanField("Disarm", default=False)
    spear_giant_stomp = models.BooleanField("Giant Stomp", default=False)
    spear_absolute_spear = models.BooleanField("Absolute Spear", default=False)
    spear_rolling_thunder = models.BooleanField("Rolling Thunder", default=False)
    spear_earthquake_stomp = models.BooleanField("Earthquake Stomp", default=False)
    spear_weapon = models.CharField("Spear Weapon", max_length=50, choices=[
        ('none', 'Other blue or lower'),
        ('body_slasher', 'Body Slasher'),
        ('lance', 'Lance'),
        ('archangel', 'Archangel Halberd'),
        ('tallum', 'Tallum Glaive'),
        ('halberd', 'Halberd'),
        ('saint', 'Saint Spear'),
    ], default='none')

    def calculate_subclass_score(self):
        """Calculate subclass score based on skills and weapons"""
        score = 0
        
        # Count skills (each skill = 10 points)
        skill_fields = [
            # Dualblade
            self.dualblade_triple_slash, self.dualblade_sonic_blaster, self.dualblade_detect_weakness,
            self.dualblade_dance_of_fury, self.dualblade_dual_parrying, self.dualblade_dual_impact,
            self.dualblade_berserker, self.dualblade_breaking_armor,
            # Dagger
            self.dagger_assassin_vision, self.dagger_shadow_blade, self.dagger_hide,
            self.dagger_venom, self.dagger_reset_movement, self.dagger_phantom_blade,
            self.dagger_shadow_step, self.dagger_marionette,
            # Staff
            self.staff_snow_storm, self.staff_cancellation, self.staff_confuse,
            self.staff_restore_casting, self.staff_frozen_crystal, self.staff_meteor,
            self.staff_chaos, self.staff_gravity,
            # Bow
            self.bow_death_sting, self.bow_mana_seeker, self.bow_real_target,
            self.bow_entangle, self.bow_impact_shot, self.bow_absolute_piercing,
            self.bow_elimination, self.bow_pinpoint_shot,
            # Tank
            self.tank_double_shock, self.tank_iron_will, self.tank_vex,
            self.tank_touch_of_life, self.tank_holy_strike, self.tank_brutal_attack,
            self.tank_vengeance, self.tank_chain_strike,
            # Spear
            self.spear_frenzy, self.spear_vital_destruction, self.spear_infinity_strike,
            self.spear_disarm, self.spear_giant_stomp, self.spear_absolute_spear,
            self.spear_rolling_thunder, self.spear_earthquake_stomp,
        ]
        
        for skill in skill_fields:
            if skill:
                score += 10
        
        # Weapon bonus (better weapons = more points)
        weapon_scores = {
            'none': 0, 'tallum': 20, 'archangel': 25, 'dark_legion': 25, 'mardil': 25, 'astaroth': 30,
            'demon': 20, 'cruma': 20, 'soul': 25, 'naga': 30,
            'daimon': 20, 'stakato': 20, 'mother_tree': 20, 'spirits': 25, 'imperial': 30,
            'bow_peril': 20, 'carnium': 20, 'shyeed': 30,
            'ssaurabi': 30, 'sirra': 20, 'valhalla': 20, 'miracles': 25, 'caladbolg': 30,
            'body_slasher': 30, 'lance': 20, 'halberd': 20, 'saint': 30,
        }
        
        for weapon_field in [self.dualblade_weapon, self.dagger_weapon, self.staff_weapon,
                             self.bow_weapon, self.tank_weapon, self.spear_weapon]:
            score += weapon_scores.get(weapon_field, 0)
        
        return score

    def __str__(self):

        return f"Subclass Info for {self.character.name}"



class LegendaryClass(models.Model):

    name = models.CharField("Nama", max_length=100)

    icon_file = models.CharField("File Ikon", max_length=100, blank=True)

    def __str__(self):

        return self.name



class LegendaryAgathion(models.Model):

    name = models.CharField("Nama", max_length=100)

    icon_file = models.CharField("File Ikon", max_length=100, blank=True)

    def __str__(self):

        return self.name



class InheritorBook(models.Model):

    name = models.CharField("Nama", max_length=100)

    icon_file = models.CharField("File Ikon", max_length=100, blank=True, null=True)

    def __str__(self):

        return self.name



class Character(models.Model):

    # Owner - User yang memiliki karakter ini
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='characters',
        null=True,
        blank=True,
        verbose_name="Pemilik"
    )

    name = models.CharField("Nama Karakter", max_length=100, unique=True)

    clan = models.CharField("Clan", max_length=100, choices=CLAN_CHOICES, default='Valkyrie', blank=True)

    level = models.IntegerField("Level", default=1)

    character_class = models.CharField("Kelas", max_length=100, choices=CLASS_CHOICES, default='Spear Skill')

    legendary_classes = models.ManyToManyField(LegendaryClass, verbose_name="Kelas Legendaris", blank=True)

    legendary_agathions = models.ManyToManyField(LegendaryAgathion, verbose_name="Agathion Legendaris", blank=True)

    main_weapon = models.ForeignKey(Item, verbose_name="Senjata Utama", on_delete=models.SET_NULL, related_name='equipped_weapon', null=True, blank=True)

    helmet = models.ForeignKey(Item, verbose_name="Helm", on_delete=models.SET_NULL, related_name='equipped_helmet', null=True, blank=True)

    armor = models.ForeignKey(Item, verbose_name="Baju Zirah", on_delete=models.SET_NULL, related_name='equipped_armor', null=True, blank=True)

    gloves = models.ForeignKey(Item, verbose_name="Sarung Tangan", on_delete=models.SET_NULL, related_name='equipped_gloves', null=True, blank=True)

    boots = models.ForeignKey(Item, verbose_name="Sepatu", on_delete=models.SET_NULL, related_name='equipped_boots', null=True, blank=True)

    necklace = models.ForeignKey(Item, verbose_name="Kalung", on_delete=models.SET_NULL, related_name='equipped_necklace', null=True, blank=True)

    ring_left = models.ForeignKey(Item, verbose_name="Cincin Kiri", on_delete=models.SET_NULL, related_name='equipped_ring_left', null=True, blank=True)

    ring_right = models.ForeignKey(Item, verbose_name="Cincin Kanan", on_delete=models.SET_NULL, related_name='equipped_ring_right', null=True, blank=True)

    earring_left = models.ForeignKey(Item, verbose_name="Anting Kiri", on_delete=models.SET_NULL, related_name='equipped_earring_left', null=True, blank=True)

    earring_right = models.ForeignKey(Item, verbose_name="Anting Kanan", on_delete=models.SET_NULL, related_name='equipped_earring_right', null=True, blank=True)

    # Discord Integration
    discord_id = models.CharField("Discord ID", max_length=50, blank=True, null=True, unique=True,
        help_text="ID Discord user yang di-link ke karakter ini. Format: 18-digit number.")


    def __str__(self):

        return self.name



    def calculate_gear_score_breakdown(self):

        """

        Menghitung gear score dengan breakdown 3 kategori sesuai l2mgearscore.com:

        - Characteristics: dari CharacterAttributes (stats umum)

        - Sub-class: dari SubclassStats

        - Main class: dari level karakter dan class bonuses

        

        Formula sesuai spreadsheet:

        SCORE = DMG + ACC + DEF + (DMG_REDUCT × 3) + SKILL_RESIST + (SKILL_DMG_BOOST × 2) + 

                WPN_DMG_BOOST + (SOULSHOT × 10) + (VALOR × 10) + (GUARDIAN × 10) +

                (CONQUER × 10) + (LEGEND_CLASS_POINT × 20) + (LEGEND_AGATHION_POINT × 20) +

                (TOTAL_LEGEND_CODEX × 3)

        """

        # ============================================

        # 1. GEAR SCORE STATS

        # Dari CharacterAttributes: DMG, ACC, DEF, REDUC, RESIST, skill/wpn boost

        # ============================================

        characteristics_score = 0.0
        gear_stats_score = 0.0

        dmg = acc = def_stat = reduc = resist = skill_dmg_boost = wpn_dmg_boost = 0

        soulshot = valor = guardian = conquer = 0

        legend_class_point = legend_agathion_point = total_legend_codex = 0

        

        try:

            attrs = self.attributes

            dmg = attrs.stat_dmg or 0

            acc = attrs.stat_acc or 0

            def_stat = attrs.stat_def or 0

            reduc = attrs.stat_reduc or 0

            resist = attrs.stat_resist or 0

            skill_dmg_boost = attrs.stat_skill_dmg_boost or 0

            wpn_dmg_boost = attrs.stat_wpn_dmg_boost or 0

            guardian = attrs.stat_guardian or 0

            conquer = attrs.stat_conquer or 0

            total_legend_codex = attrs.total_legend_codex or 0

            
            # Now these are IntegerField, just get the value directly
            soulshot = attrs.soulshot_level or 0
            valor = attrs.valor_level or 0
            legend_class_point = attrs.epic_classes_count or 0
            legend_agathion_point = attrs.epic_agathions_count or 0

            
            # Gear Score Stats formula from Excel (for Overall Gear Score)
            # =DMG+ACC+DEF+(REDUC*3)+RESIST+(SKILL*2)+WPN+(SOULSHOT*10)+(VALOR*10)+(GUARDIAN*10)+(CONQUER*10)+LEGEND_CLASS+LEGEND_AGATHION+(CODEX*3)+(CONQUER*10)
            gear_stats_score = (
                dmg + acc + def_stat + (reduc * 3) + resist + 
                (skill_dmg_boost * 2) + wpn_dmg_boost +
                (soulshot * 10) + (valor * 10) + (guardian * 10) + (conquer * 10) +
                legend_class_point + legend_agathion_point +
                (total_legend_codex * 3) + (conquer * 10)  # conquer counted twice per Excel formula
            )

        except CharacterAttributes.DoesNotExist:
            gear_stats_score = 0.0

        # Calculate Characteristics Score from CharacteristicsStats (145 fields)
        characteristics_score = 0.0
        try:
            char_stats = self.characteristics_stats
            characteristics_score = float(char_stats.calculate_total_score())
        except:
            pass

        
        # ============================================

        # 2. SUB-CLASS SCORE

        # Dari SubclassStats: level subclass dan bonus HP/MP

        # ============================================



        subclass_score = 0.0

        try:

            subclass = self.subclass_stats

            # Use the new calculate_subclass_score method

            subclass_score = float(subclass.calculate_subclass_score())

        except SubclassStats.DoesNotExist:

            pass

        

        # ============================================

        # 3. MAIN CLASS SCORE

        # Dari Basic Information form (CharacterAttributes)
        # Main Class Score = gear_stats_score (same as Gear Stats from CharacterAttributes)

        # ============================================

        mainclass_score = gear_stats_score  # Main Class = Gear Stats Score from CharacterAttributes

        

        # ============================================

        # TOTAL SCORE - Overall Gear Score = Characteristics + Sub-class + Main class

        # ============================================

        total_score = characteristics_score + subclass_score + mainclass_score

        

        return {

            'total_score': total_score,  # Overall Gear Score

            'gear_stats_score': gear_stats_score,  # From Gear Score Stats tab

            'characteristics': characteristics_score,  # From CharacteristicsStats (145 fields)

            'subclass': subclass_score,

            'mainclass': mainclass_score,

            # Detail breakdown untuk debugging

            'dmg': dmg,

            'acc': acc,

            'def_stat': def_stat,

            'reduc': reduc,

            'resist': resist,

            'skill_dmg_boost': skill_dmg_boost,

            'wpn_dmg_boost': wpn_dmg_boost,

            'soulshot': soulshot,

            'valor': valor,

            'guardian': guardian,

            'conquer': conquer,

            'legend_class_point': legend_class_point,

            'legend_agathion_point': legend_agathion_point,

            'total_legend_codex': total_legend_codex,

        }



    def calculate_gear_score(self):

        """Metode untuk menghitung total gear score. Memanggil breakdown dan mengembalikan totalnya."""

        breakdown = self.calculate_gear_score_breakdown()

        return breakdown['total_score']





# PvP Gear Choices

PVP_HELMET_CHOICES = [
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
]



PVP_GLOVES_CHOICES = [
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
]



PVP_BOOTS_CHOICES = [
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
]



PVP_GAITERS_CHOICES = [
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
]



PVP_ARMOR_CHOICES = [
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
]



PVP_CLOAK_CHOICES = [
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
]



PVP_SIGIL_CHOICES = [
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
]



PVP_NECKLACE_CHOICES = [
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
]



PVP_RING_CHOICES = [
    ('', 'No ring selected'),
    ("Ring of Blessing", "Ring of Blessing"),
    ("Lilith's Ring", "Lilith's Ring"),
    ("Anakeem's Ring", "Anakeem's Ring"),
    ("Baium's Ring", "Baium's Ring"),
    ("Vereth's Ring", "Vereth's Ring"),
    ("Core Ring", "Core Ring"),
    ("Queen Ant's Ring", "Queen Ant's Ring"),
    ("Ring of Passion", "Ring of Passion"),
    ("Majestic Ring", "Majestic Ring"),
    ("Forgotten Hero's Ring", "Forgotten Hero's Ring"),
    ("Desperion's Ring", "Desperion's Ring"),
]



PVP_BELT_CHOICES = [
    ('', 'No belt selected'),
    ("Blue", "Blue"),
    ("Ekimus' Belt", "Ekimus' Belt"),
    ("Dragon Belt", "Dragon Belt"),
    ("Tiat's Belt", "Tiat's Belt"),
    ("Eratone's Belt", "Eratone's Belt"),
    ("Lord's Authority", "Lord's Authority"),
    ("Maphr's Belt", "Maphr's Belt"),
]



WEAPON_CHOICES = [
    ('', 'No weapon selected'),
    # Bow
    ('bow|Akatt Longbow', 'Akatt Longbow'),
    ('bow|Amenance Bow', 'Amenance Bow'),
    ('bow|Archangel Bow', 'Archangel Bow'),
    ('bow|Bow of Oblivion', 'Bow of Oblivion'),
    ('bow|Bow of the Shingung', 'Bow of the Shingung'),
    ('bow|Bow of the Soul', 'Bow of the Soul'),
    ('bow|Carnium Bow', 'Carnium Bow'),
    ('bow|Devils Bow', 'Devils Bow'),
    ('bow|Elemental Bow', 'Elemental Bow'),
    ('bow|Giants Bow', 'Giants Bow'),
    ('bow|Hazard Bow', 'Hazard Bow'),
    ('bow|Ice Crystal Bow', 'Ice Crystal Bow'),
    ('bow|Moonlight Bow', 'Moonlight Bow'),
    ('bow|Plasma Bow', 'Plasma Bow'),
    # Cane (Staff)
    ('cane|Archangel Staff', 'Archangel Staff'),
    ('cane|Bloody Nebulite', 'Bloody Nebulite'),
    ('cane|Branch of Life', 'Branch of Life'),
    ('cane|Branches of the World Tree', 'Branches of the World Tree'),
    ('cane|Commander Staff', 'Commander Staff'),
    ('cane|Crystal Wand', 'Crystal Wand'),
    ('cane|Dead Man Staff', 'Dead Man Staff'),
    ('cane|Desperion Staff', 'Desperion Staff'),
    ('cane|Ghoul Staff', 'Ghoul Staff'),
    ('cane|Giant Staff', 'Giant Staff'),
    ('cane|Imperial Sttaff', 'Imperial Sttaff'),
    ('cane|Inferno Staff', 'Inferno Staff'),
    ('cane|Spirit Staff', 'Spirit Staff'),
    # Chainsword
    ('chainsword|Archangel Chainsword', 'Archangel Chainsword'),
    ('chainsword|Barakiel Chainsword', 'Barakiel Chainsword'),
    ('chainsword|Berseker Chainsword', 'Berseker Chainsword'),
    ('chainsword|Bultgang', 'Bultgang'),
    ('chainsword|Chrono Kitara', 'Chrono Kitara'),
    ('chainsword|Dismentor', 'Dismentor'),
    ('chainsword|Dragon Hunter', 'Dragon Hunter'),
    ('chainsword|Gram', 'Gram'),
    ('chainsword|Lightning Chainsword', 'Lightning Chainsword'),
    ('chainsword|Nameless Victory', 'Nameless Victory'),
    ('chainsword|Pain of Gardenness', 'Pain of Gardenness'),
    ('chainsword|Schrager', 'Schrager'),
    # Crossbow
    ('crossbow|Alvarest', 'Alvarest'),
    ('crossbow|Archangel Crossbow', 'Archangel Crossbow'),
    ('crossbow|Ballista', 'Ballista'),
    ('crossbow|Burst Avenger', 'Burst Avenger'),
    ('crossbow|Crystal Bowgun', 'Crystal Bowgun'),
    ('crossbow|Doom Singer', 'Doom Singer'),
    ('crossbow|Giant Crossbow', 'Giant Crossbow'),
    ('crossbow|Hellhound', 'Hellhound'),
    ('crossbow|Peacemaker', 'Peacemaker'),
    ('crossbow|Tasram', 'Tasram'),
    ('crossbow|Thorn Crossbow', 'Thorn Crossbow'),
    ('crossbow|antique crossbow', 'antique crossbow'),
    # Dagger
    ('dagger|Archangel Slayer', 'Archangel Slayer'),
    ('dagger|Blood Orchid', 'Blood Orchid'),
    ('dagger|Crystal Dagger', 'Crystal Dagger'),
    ('dagger|Dagger of Contamination', 'Dagger of Contamination'),
    ('dagger|Dagger of Mana', 'Dagger of Mana'),
    ('dagger|Devil Dagger', 'Devil Dagger'),
    ('dagger|Flame Breaker', 'Flame Breaker'),
    ('dagger|Giant Dagger', 'Giant Dagger'),
    ('dagger|Hell Knife', 'Hell Knife'),
    ("dagger|Kruma's Horn", "Kruma's Horn"),
    ('dagger|Soul Separator', 'Soul Separator'),
    ('dagger|chris', 'chris'),
    ('dagger|stiletto', 'stiletto'),
    # Double Axe
    ('double_axe|Archangel Twin Axe', 'Archangel Twin Axe'),
    ('double_axe|Bloody Angish', 'Bloody Angish'),
    ('double_axe|Bloody Cross', 'Bloody Cross'),
    ('double_axe|Clarent', 'Clarent'),
    ('double_axe|Cursed Twin Axe', 'Cursed Twin Axe'),
    ('double_axe|Furious Berserker', 'Furious Berserker'),
    ('double_axe|Gallatin', 'Gallatin'),
    ("double_axe|Giant's Twin Axes", "Giant's Twin Axes"),
    ('double_axe|Ice Storm Twin Axe', 'Ice Storm Twin Axe'),
    ('double_axe|Madness Twin Axe', 'Madness Twin Axe'),
    ('double_axe|Meteor Impact', 'Meteor Impact'),
    ('double_axe|Warpeak', 'Warpeak'),
    ('double_axe|Yaksha Twin Axe', 'Yaksha Twin Axe'),
    # Greatsword
    ('greatsword|Archangel Buster', 'Archangel Buster'),
    ("greatsword|Berserker's Greatsword", "Berserker's Greatsword"),
    ("greatsword|Commander's Greatsword", "Commander's Greatsword"),
    ('greatsword|Dragon Slayer', 'Dragon Slayer'),
    ('greatsword|First Blood', 'First Blood'),
    ('greatsword|Flamberge', 'Flamberge'),
    ("greatsword|Guardian's Two-Handed Greatsword", "Guardian's Two-Handed Greatsword"),
    ("greatsword|Heaven's Wingblade", "Heaven's Wingblade"),
    ('greatsword|Inferno Master', 'Inferno Master'),
    ('greatsword|Sword of Iphos', 'Sword of Iphos'),
    # Magic Cannon
    ('magic_cannon|Archangel Blaster', 'Archangel Blaster'),
    ('magic_cannon|Assault Cannon', 'Assault Cannon'),
    ('magic_cannon|Basilisk Culverin', 'Basilisk Culverin'),
    ('magic_cannon|Deathbringer', 'Deathbringer'),
    ('magic_cannon|Divine Blaster', 'Divine Blaster'),
    ('magic_cannon|Doom Crusher', 'Doom Crusher'),
    ("magic_cannon|Giant's Blaster", "Giant's Blaster"),
    ('magic_cannon|Mine Buster', 'Mine Buster'),
    ('magic_cannon|Pata', 'Pata'),
    ('magic_cannon|Sarakael Magic Cannon', 'Sarakael Magic Cannon'),
    ('magic_cannon|Schofield', 'Schofield'),
    ('magic_cannon|Star Buster', 'Star Buster'),
    ('magic_cannon|Zephyrus', 'Zephyrus'),
    # One-Handed Sword
    ('one_handed_sword|Archangel Blade', 'Archangel Blade'),
    ('one_handed_sword|Elemental Sword', 'Elemental Sword'),
    ("one_handed_sword|Fighting Father's Sword", "Fighting Father's Sword"),
    ("one_handed_sword|Giant's Sword", "Giant's Sword"),
    ("one_handed_sword|Guardian's Sword", "Guardian's Sword"),
    ('one_handed_sword|Kshanberg', 'Kshanberg'),
    ('one_handed_sword|Raid Sword', 'Raid Sword'),
    ('one_handed_sword|Sir Blade', 'Sir Blade'),
    ('one_handed_sword|Spirits Sword', 'Spirits Sword'),
    ('one_handed_sword|Sword of Eclipse', 'Sword of Eclipse'),
    ('one_handed_sword|Sword of Miracle', 'Sword of Miracle'),
    ('one_handed_sword|Sword of Nightmare', 'Sword of Nightmare'),
    ('one_handed_sword|Sword of Valhalla', 'Sword of Valhalla'),
    ('one_handed_sword|Tsurugi', 'Tsurugi'),
    # Orb
    ('orb|Archangel Orb', 'Archangel Orb'),
    ("orb|Devil's Orb", "Devil's Orb"),
    ('orb|Dragon Flame Head', 'Dragon Flame Head'),
    ('orb|Eclipse of', 'Eclipse of'),
    ('orb|Elysion', 'Elysion'),
    ('orb|Fairy Queen', 'Fairy Queen'),
    ("orb|Giant's Orb", "Giant's Orb"),
    ('orb|Hall of Faith', 'Hall of Faith'),
    ('orb|Hand of Cabrio', 'Hand of Cabrio'),
    ('orb|Nirvana', 'Nirvana'),
    ('orb|Spell Breaker', 'Spell Breaker'),
    ('orb|The Bones of Kaim Banul', 'The Bones of Kaim Banul'),
    # Rapier
    ('rapier|Archangel Rapier', 'Archangel Rapier'),
    ('rapier|Assault Rapier', 'Assault Rapier'),
    ('rapier|Blink Rapier', 'Blink Rapier'),
    ('rapier|Eclair Bijou', 'Eclair Bijou'),
    ("rapier|Giant's Rapier", "Giant's Rapier"),
    ('rapier|Glorious', 'Glorious'),
    ('rapier|Grid Rapier', 'Grid Rapier'),
    ('rapier|Hauteclair', 'Hauteclair'),
    ('rapier|Kolishmard', 'Kolishmard'),
    ('rapier|Levatein', 'Levatein'),
    ('rapier|Soldat Estark', 'Soldat Estark'),
    ("rapier|Tromba's Fang", "Tromba's Fang"),
    # Soul Breaker
    ('soul_breaker|Archangel Soul Breaker', 'Archangel Soul Breaker'),
    ('soul_breaker|Blade of Madness', 'Blade of Madness'),
    ('soul_breaker|Crystal Soul Breaker', 'Crystal Soul Breaker'),
    ('soul_breaker|Dark Shadow', 'Dark Shadow'),
    ('soul_breaker|Frostbite', 'Frostbite'),
    ("soul_breaker|Giant's Soul Breaker", "Giant's Soul Breaker"),
    ('soul_breaker|Hrunting', 'Hrunting'),
    ('soul_breaker|Judge of the Sun', 'Judge of the Sun'),
    ('soul_breaker|Sword of the Soul', 'Sword of the Soul'),
    ('soul_breaker|Wisdom of our ancestors', 'Wisdom of our ancestors'),
    # Spear
    ('spear|Archangel Halberd', 'Archangel Halberd'),
    ('spear|Ascalon', 'Ascalon'),
    ('spear|Battle Spear', 'Battle Spear'),
    ('spear|Body Slasher', 'Body Slasher'),
    ("spear|Giant's Spear", "Giant's Spear"),
    ('spear|Great Axe', 'Great Axe'),
    ('spear|Halberd', 'Halberd'),
    ('spear|Heavy War Axe', 'Heavy War Axe'),
    ('spear|Lancia', 'Lancia'),
    ('spear|Saint Spear', 'Saint Spear'),
    ('spear|Scorpion', 'Scorpion'),
    ('spear|Side', 'Side'),
    ('spear|Tallum Glaive', 'Tallum Glaive'),
    ('spear|Typhon Spear', 'Typhon Spear'),
    ('spear|Widowmaker', 'Widowmaker'),
    # Two Sword Style (Dual-Wield)
    ('two_sword_style|Archangel Dual Swords', 'Archangel Dual Swords'),
    ('two_sword_style|Caribs Dual Swords', 'Caribs Dual Swords'),
    ('two_sword_style|Damascus Dual Sword', 'Damascus Dual Sword'),
    ('two_sword_style|Dark Legion', 'Dark Legion'),
    ('two_sword_style|Death Lord Dual Swords', 'Death Lord Dual Swords'),
    ("two_sword_style|Giant's Dual Swords", "Giant's Dual Swords"),
    ('two_sword_style|Homunculus Dual Sword', 'Homunculus Dual Sword'),
    ("two_sword_style|Mardil's Wrath", "Mardil's Wrath"),
    ('two_sword_style|Mystery Dual Swords', 'Mystery Dual Swords'),
    ('two_sword_style|Saint Dual Sword', 'Saint Dual Sword'),
    ('two_sword_style|Tears of Warrior', 'Tears of Warrior'),
    ("two_sword_style|Themis's Tongue", "Themis's Tongue"),
]

# Mapping dari Character Class ke Weapon Type key
CLASS_TO_WEAPON_TYPE = {
    'Bow Skill': 'bow',
    'Chainsword Skill': 'chainsword',
    'Crossbow Skill': 'crossbow',
    'Dagger Skill': 'dagger',
    'Dual Axe Skill': 'double_axe',
    'Dual-Wield Skills': 'two_sword_style',
    'Greatsword Skill': 'greatsword',
    'Magic Cannon Skill': 'magic_cannon',
    'One-Handed Sword Skill': 'one_handed_sword',
    'Orb Skill': 'orb',
    'Rapier Skill': 'rapier',
    'Soul Breaker Skill': 'soul_breaker',
    'Spear Skill': 'spear',
    'Staff Skill': 'cane',
}




SKILL_CHOICES = [

    # Spear class skills (from reference)

    ("Frenzy", "Frenzy"),

    ("Vital Destruction", "Vital Destruction"),

    ("Infinity Strike", "Infinity Strike"),

    ("Disarm", "Disarm"),

    ("Giant Stomp", "Giant Stomp"),

    ("Absolute Spear", "Absolute Spear"),

    ("Rolling Thunder", "Rolling Thunder"),

    ("Earthquake Stomp", "Earthquake Stomp"),

]



class CharacterAttributes(models.Model):

    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='attributes')

    inheritor_books = models.ManyToManyField(InheritorBook, verbose_name="Buku Inheritor", blank=True)

    epic_classes_count = models.IntegerField("Legend Class Point", default=0)

    epic_agathions_count = models.IntegerField("Legend Agathion Point", default=0)

    soulshot_level = models.IntegerField("Soulshot Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(13)], blank=True)

    valor_level = models.IntegerField("Valor Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(13)], blank=True)

    soul_prog_attack = models.CharField("Soul Progression Attack", max_length=10, choices=SOUL_PROGRESSION_CHOICES, blank=True)

    soul_prog_defense = models.CharField("Soul Progression Defense", max_length=10, choices=SOUL_PROGRESSION_CHOICES, blank=True)

    soul_prog_blessing = models.CharField("Soul Progression Blessing", max_length=10, choices=SOUL_PROGRESSION_CHOICES, blank=True)

    enchant_bracelet_holy_prot = models.IntegerField("Enchant Bracelet of Holy Protection", choices=ENCHANT_CHOICES, default=0)

    enchant_bracelet_influence = models.IntegerField("Enchant Bracelet of Influence", choices=ENCHANT_CHOICES, default=0)

    enchant_earring_earth = models.IntegerField("Enchant Earth Dragon's Earring", choices=ENCHANT_CHOICES, default=0)

    enchant_earring_fire = models.IntegerField("Enchant Fire Dragon's Earring", choices=ENCHANT_CHOICES, default=0)

    enchant_seal_eva = models.IntegerField("Enchant Eva's Seal", choices=ENCHANT_CHOICES, default=0)



    # New PvP Fields

    pvp_helmet = models.CharField("PvP Helmet", max_length=100, choices=PVP_HELMET_CHOICES, blank=True)
    pvp_helmet_enchant = models.IntegerField("PvP Helmet Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_gloves = models.CharField("PvP Gloves", max_length=100, choices=PVP_GLOVES_CHOICES, blank=True)
    pvp_gloves_enchant = models.IntegerField("PvP Gloves Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_boots = models.CharField("PvP Boots", max_length=100, choices=PVP_BOOTS_CHOICES, blank=True)
    pvp_boots_enchant = models.IntegerField("PvP Boots Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_gaiters = models.CharField("PvP Gaiters", max_length=100, choices=PVP_GAITERS_CHOICES, blank=True)
    pvp_gaiters_enchant = models.IntegerField("PvP Gaiters Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_top_armor = models.CharField("PvP Top Armor", max_length=100, choices=PVP_ARMOR_CHOICES, blank=True)
    pvp_top_armor_enchant = models.IntegerField("PvP Armor Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_cloak = models.CharField("PvP Cloak", max_length=100, choices=PVP_CLOAK_CHOICES, blank=True)
    pvp_cloak_enchant = models.IntegerField("PvP Cloak Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_sigil = models.CharField("PvP Sigil", max_length=100, choices=PVP_SIGIL_CHOICES, blank=True)
    pvp_sigil_enchant = models.IntegerField("PvP Sigil Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")
    pvp_sigil_enchant = models.IntegerField("PvP Sigil Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_necklace = models.CharField("PvP Necklace", max_length=100, choices=PVP_NECKLACE_CHOICES, blank=True)
    pvp_necklace_enchant = models.IntegerField("PvP Necklace Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_ring_left = models.CharField("PvP Ring (Left)", max_length=100, choices=PVP_RING_CHOICES, blank=True)
    pvp_ring_left_enchant = models.IntegerField("PvP Ring (Left) Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_ring_right = models.CharField("PvP Ring (Right)", max_length=100, choices=PVP_RING_CHOICES, blank=True)
    pvp_ring_right_enchant = models.IntegerField("PvP Ring (Right) Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    pvp_belt = models.CharField("PvP Belt", max_length=100, choices=PVP_BELT_CHOICES, blank=True)
    pvp_belt_enchant = models.IntegerField("PvP Belt Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    

    # ============================================

    # NEW STAT FIELDS FOR GEAR SCORE CALCULATION

    # Based on spreadsheet formula:

    # SCORE = DMG + ACC + DEF + (REDUC×3) + RESIST + (SKILL_DMG_BOOST×2) + 

    #         WPN_DMG_BOOST + (SOULSHOT×10) + (VALOR×10) + (GUARDIAN×10)

    # ============================================

    stat_dmg = models.IntegerField("DMG (Damage)", default=0, help_text="Total damage stat")

    stat_acc = models.IntegerField("ACC (Accuracy)", default=0, help_text="Total accuracy stat")

    stat_def = models.IntegerField("DEF (Defense)", default=0, help_text="Total defense stat")

    stat_reduc = models.IntegerField("REDUC (Damage Reduction)", default=0, help_text="Damage reduction stat (multiplied by 3 in score)")

    stat_resist = models.IntegerField("RESIST (Resistance)", default=0, help_text="Magic/status resistance stat")

    stat_skill_dmg_boost = models.IntegerField("Skill DMG Boost", default=0, help_text="Skill damage boost (multiplied by 2 in score)")

    stat_wpn_dmg_boost = models.IntegerField("Weapon DMG Boost", default=0, help_text="Weapon damage boost stat")

    stat_guardian = models.IntegerField("Guardian", default=0, validators=[MinValueValidator(0), MaxValueValidator(13)], help_text="Guardian level (max 13, multiplied by 10 in score)", blank=True)

    stat_conquer = models.IntegerField("Conquer", default=0, validators=[MinValueValidator(0), MaxValueValidator(13)], help_text="Conquer level (max 13, multiplied by 10 in score)", blank=True)

    total_legend_codex = models.IntegerField("Total Legend Codex", default=0, help_text="Total Legend Class & Agathion Codex (multiplied by 3 in score)")

    

    # Weapon and Skills

    weapon = models.CharField("Weapon", max_length=100, choices=WEAPON_CHOICES, blank=True)
    weapon_enchant = models.IntegerField("Weapon Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")

    

    # Individual skill fields for Spear class

    skill_frenzy = models.BooleanField("Frenzy", default=False)

    skill_vital_destruction = models.BooleanField("Vital Destruction", default=False)

    skill_infinity_strike = models.BooleanField("Infinity Strike", default=False)

    skill_disarm = models.BooleanField("Disarm", default=False)

    skill_giant_stomp = models.BooleanField("Giant Stomp", default=False)

    skill_absolute_spear = models.BooleanField("Absolute Spear", default=False)

    skill_rolling_thunder = models.BooleanField("Rolling Thunder", default=False)

    skill_earthquake_stomp = models.BooleanField("Earthquake Stomp", default=False)





    def __str__(self):

        return f"Atribut untuk {self.character.name}"



class Skill(models.Model):

    name = models.CharField(max_length=100, unique=True)

    icon_file = models.CharField(max_length=100, blank=True, null=True)



    def __str__(self):

        return self.name







class GearScoreLog(models.Model):

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='gs_logs')

    timestamp = models.DateTimeField(auto_now_add=True)

    reason = models.CharField("Alasan", max_length=255, default='Pembaruan Karakter')

    total_score = models.FloatField()

    # New stat fields matching the spreadsheet formula

    dmg = models.IntegerField("DMG", default=0)

    acc = models.IntegerField("ACC", default=0)

    def_stat = models.IntegerField("DEF", default=0)

    reduc = models.IntegerField("REDUC", default=0)

    resist = models.IntegerField("RESIST", default=0)

    skill_dmg_boost = models.IntegerField("Skill DMG Boost", default=0)

    wpn_dmg_boost = models.IntegerField("Wpn DMG Boost", default=0)

    soulshot = models.IntegerField("Soulshot", default=0)

    valor = models.IntegerField("Valor", default=0)

    guardian = models.IntegerField("Guardian", default=0)



    class Meta:

        ordering = ['-timestamp']



    def __str__(self):

        return f'{self.character.name} GS Log @ {self.timestamp.strftime("%Y-%m-%d %H:%M")}'



# (GearScoreLog model omitted for brevity)

class CharacteristicsStats(models.Model):



    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='characteristics_stats')







    uron_char_mag = models.IntegerField("Magic Damage", default=0)



    acc_char_mag = models.IntegerField("Magic Accuracy", default=0)



    crit_char_mag = models.IntegerField("Magic Critical Hit", default=0)



    uron_char_mele = models.IntegerField("Melee Damage", default=0)



    acc_char_mele = models.IntegerField("Melee Accuracy", default=0)



    crit_char_mele = models.IntegerField("Melee Critical Hit", default=0)



    uron_char_range = models.IntegerField("Ranged Damage", default=0)



    acc_char_range = models.IntegerField("Ranged Accuracy", default=0)



    crit_char_range = models.IntegerField("Ranged Critical Hit", default=0)



    uror_char = models.IntegerField("Weapon Damage", default=0)



    dopur_char = models.IntegerField("Extra Damage", default=0)



    dopurcrit_char = models.IntegerField("Extra Damage (on Critical Hit)", default=0)



    shdvur_char = models.IntegerField("Double Chance", default=0)



    shtrur_char = models.IntegerField("Triple Chance", default=0)



    blockor_char = models.IntegerField("Weapon Block", default=0)



    scoratk_char = models.IntegerField("Attack Speed", default=0)



    scor_char = models.IntegerField("Movement Speed", default=0)



    scormag_char = models.IntegerField("Cast Speed", default=0)



    snih_char = models.IntegerField("Damage Reduction", default=0)



    snihurvmili = models.IntegerField("Melee Damage Reduction", default=0)



    snihurvdal = models.IntegerField("Ranged Damage Reduction", default=0)



    snihurmag = models.IntegerField("Magic Damage Reduction", default=0)



    def_char = models.IntegerField("Defence", default=0)



    uklvblis = models.IntegerField("Melee Evasion", default=0)



    uklvdal = models.IntegerField("Ranged Evasion", default=0)



    uklvmag = models.IntegerField("Magic Evasion", default=0)



    sopr_char = models.IntegerField("Skill Resistance", default=0)



    maxhp = models.IntegerField("Max HP", default=0)



    maxmp = models.IntegerField("Max MP", default=0)



    vosthp = models.IntegerField("HP Recovery (Tick)", default=0)



    vostmp = models.IntegerField("MP Recovery (Tick)", default=0)



    umenmp = models.IntegerField("MP Consumption Reduction", default=0)



    umenper = models.IntegerField("Coldown Reduction", default=0)



    maksgruz = models.IntegerField("Weigt Limit", default=0)



    uveluror = models.IntegerField("Weapon Damage Boost", default=0)



    sopruror = models.IntegerField("Weapon Defence", default=0)



    uvelurumen = models.IntegerField("Skill Damage Boost", default=0)



    soprurumen = models.IntegerField("Skill Defence", default=0)



    snihkrit = models.IntegerField("Critical Hit Reduction", default=0)



    soprkritmili = models.IntegerField("Mele Critical Hit Resistance", default=0)



    soprktitreng = models.IntegerField("Ranged Critical Hit Resistance", default=0)



    soprkritmag = models.IntegerField("Magic Critical Hit Resistance", default=0)



    soprdvoinur = models.IntegerField("Double Resistance", default=0)



    soprtroinur = models.IntegerField("Triple Resistance", default=0)



    probivblock = models.IntegerField("Block Penetration", default=0)



    ignrsnishur = models.IntegerField("Ignore Damage Reduction", default=0)



    shansogl = models.IntegerField("Stun Accuracy", default=0)



    soprogl = models.IntegerField("Stun Resistance", default=0)



    snishurogl = models.IntegerField("Stun Reduction", default=0)



    zashvogl = models.IntegerField("Stun Defence", default=0)



    doptochogl = models.IntegerField("Extra Accuracy (to Stunned)", default=0)



    ignordopsnishogl = models.IntegerField("Ignore Extra Reduction (to Stunned)", default=0)



    shansuder = models.IntegerField("Hold Accuracy", default=0)



    soprudersh = models.IntegerField("Hold Resistance", default=0)



    snishurvsostuder = models.IntegerField("Hold Reduction", default=0)



    zashvsostuder = models.IntegerField("Hold Defence", default=0)



    doptchpouder = models.IntegerField("Extra Accuracy (to Held)", default=0)



    ignordopshishpouder = models.IntegerField("Ignore Extra Reduction (to Held)", default=0)



    shansagro = models.IntegerField("Vex Accuracy", default=0)



    sopragro = models.IntegerField("Aggression Resistance", default=0)



    shansbezmolv = models.IntegerField("Silence Accuracy", default=0)



    soprbezmolv = models.IntegerField("Silence Resistance", default=0)



    shansanomal = models.IntegerField("CC Accuracy", default=0)



    sopranomal = models.IntegerField("CC Resistance", default=0)



    umendlitanomal = models.IntegerField("CC Duration Reduction", default=0)



    uveldlitanomalsost = models.IntegerField("Increases CC Duration", default=0)



    moshzelvost = models.IntegerField("Potion Recovery Rate", default=0)



    effectzelvost = models.IntegerField("Potion Recovery Amount", default=0)



    effectlech = models.IntegerField("Heal Boost", default=0)



    effectpollech = models.IntegerField("Received Heal Increase", default=0)



    absolutvosthp = models.IntegerField("Fixed HP Recovery", default=0)



    absolutvostmp = models.IntegerField("Fixed MP Recovery", default=0)



    ignorshtrafvosthp = models.IntegerField("Ignore HP Recovery Penalty", default=0)



    ignorshtrafvostmp = models.IntegerField("Ignore MP Recovery Penalty", default=0)



    tochobichattak = models.IntegerField("Basic Attack Accuracy", default=0)



    uronobichattak = models.IntegerField("Basic Attack Damage", default=0)



    snishuronaotobichattak = models.IntegerField("Basic Attack Damage Reduction", default=0)



    uveluronaotobichattak = models.IntegerField("Basic Attack Damage Boost", default=0)



    sopruronuotobichattak = models.IntegerField("Basic Attack Damage Resistance", default=0)



    tochnumen = models.IntegerField("Skill Accuracy", default=0)



    zashotumen = models.IntegerField("Skill Evasion", default=0)



    shansdvurotumen = models.IntegerField("Skill Double Chance", default=0)



    soprdvoinurotumen = models.IntegerField("Skill Double Resistance", default=0)



    shanstroinurotumen = models.IntegerField("Skill Triple Chance", default=0)



    soprtroinurotumen = models.IntegerField("Skill Triple Resistance", default=0)



    dopurvpvp_mele = models.IntegerField("Extra PvP Melee Damage", default=0)



    tochnvpvp_mele = models.IntegerField("PvP Melee Accuracy", default=0)



    dopurvpvp_range = models.IntegerField("Extra PvP Range Damage", default=0)



    tochnvpvp_range = models.IntegerField("PvP Range Accuracy", default=0)



    dopurvpvp_mag = models.IntegerField("Extra PvP Magic Damage", default=0)



    tochnvpvp_mag = models.IntegerField("PvP Magic Accuracy", default=0)



    kritatkpvp = models.IntegerField("PvP Critical Hit", default=0)



    uklvmilipvp = models.IntegerField("PvP Melee Evasion", default=0)



    uklvrengepvp = models.IntegerField("PvP Ranged Evasion", default=0)



    uklmagpvp = models.IntegerField("PvP Magic Evasion", default=0)



    snishurvmilipvp = models.IntegerField("PvP Melee Damage Reduction", default=0)



    snishurvrengepvp = models.IntegerField("PvP Ranged Damage Reduction", default=0)



    snishurvmagpvp = models.IntegerField("PvP Magic Damage Reduction", default=0)



    soprurvblishpvp = models.IntegerField("PvP Melee Damage Resistance", default=0)



    soprurvdalnpvp = models.IntegerField("PvP Ranged Damage Resistance", default=0)



    soprmagurvpvp = models.IntegerField("PvP Magic Damage Resistance", default=0)



    soprurotumenvpvp = models.IntegerField("PvP Skill Defence", default=0)



    soprurotoruvpvp = models.IntegerField("PvP Weapon Defence", default=0)



    shansdvoinurpvp = models.IntegerField("PvP Double Chance", default=0)



    soprdvoinurvpvp = models.IntegerField("PvP Double Resistance", default=0)



    shanstroinurvpvp = models.IntegerField("PvP Triple Chance", default=0)



    soprtroinurvpvp = models.IntegerField("PvP Triple Resistance", default=0)



    soprkritatkvpvp = models.IntegerField("PvP Critical Hit Resistance", default=0)



    dopurvpve = models.IntegerField("Extra PvE Damage", default=0)



    tochnvpve = models.IntegerField("PvE Accuracy", default=0)



    zashvpve = models.IntegerField("PvE Defence", default=0)



    snishurvpve = models.IntegerField("PvE Damage Reduction", default=0)



    soproglvpve = models.IntegerField("PvE Stun Resistance", default=0)



    uronvodoi = models.IntegerField("Water Type Damage", default=0)



    uronognem = models.IntegerField("Fire Type Damage", default=0)



    uronvetrom = models.IntegerField("Wind Type Damage", default=0)



    uronzemlei = models.IntegerField("Eart Type Damage", default=0)



    uronsvyat = models.IntegerField("Light Type Damage", default=0)



    urontmoi = models.IntegerField("Dark Type Damage", default=0)



    uveluronavodoi = models.IntegerField("Water Type Damage Boost", default=0)



    uveluronaognem = models.IntegerField("Fire Type Damage Boost", default=0)



    uvelurovavetrom = models.IntegerField("Wind Type Damage Boost", default=0)



    uveluronazemlei = models.IntegerField("Eart Type Damage Boost", default=0)



    uveluronasvyat = models.IntegerField("Light Type Damage Boost", default=0)



    uveluronatmoi = models.IntegerField("Dark Type Damage Boost", default=0)



    soprotvode = models.IntegerField("Water Type Resistance", default=0)



    soprotogny = models.IntegerField("Fire Type Resistance", default=0)



    soprotvetry = models.IntegerField("Wind Type Resistance", default=0)



    soprotzemle = models.IntegerField("Eart Type Resistance", default=0)



    soprotsvyat = models.IntegerField("Light Type Resistance", default=0)



    soprottme = models.IntegerField("Dark Type Resistance", default=0)



    tochnostszardushi = models.IntegerField("Soulshot Accuracy", default=0)



    urotorushszardushi = models.IntegerField("Soulshot Weapon Damage", default=0)



    uveluronaszardushi = models.IntegerField("Soulshot Weapon Damage Boost", default=0)



    dopurszaryaddushi = models.IntegerField("Extra Soulshot Damage", default=0)



    tochszaryaddushiviskach = models.IntegerField("Greated Soulshot Accuracy", default=0)



    uronotorushszarviskach = models.IntegerField("Greated Soulshot Weapon Damage", default=0)



    uveluronotorushsvishkach = models.IntegerField("Greated Soulshot weapon Damage Boost", default=0)



    dopurszardushiviskach = models.IntegerField("Extra Greated Soulshot Damage", default=0)



    urotstreli = models.IntegerField("Arrow Damage", default=0)



    dalnstreli = models.IntegerField("Extra Range", default=0)



    uvelnapoeng = models.IntegerField("Blessing Recharge Increase", default=0)



    uvelpoluchengzaporysh = models.IntegerField("Oracle Quest Blessing Reward Increase", default=0)



    umenshrasheng = models.IntegerField("Blessing Conservation", default=0)



    bonuskopyt = models.IntegerField("Bonus EXP", default=0)





    def calculate_total_score(self):
        """
        Calculate the total characteristics score by summing all stat fields.
        Returns the sum of all 145 integer fields.
        """
        total = 0
        for field in self._meta.fields:
            if field.name not in ['id', 'character'] and isinstance(field, models.IntegerField):
                value = getattr(self, field.name, 0) or 0
                total += value
        return total


    def __str__(self):



        return f"Characteristics for {self.character.name}"


# ======================================================
# ACTIVITY TRACKING MODELS
# ======================================================

class ActivityEvent(models.Model):
    """
    Model untuk menyimpan data event guild (Invasion, Boss Rush, Catacombs)
    """
    EVENT_TYPE_CHOICES = (
        ('INVASION', 'Invasion'),
        ('BOSS_RUSH', 'Boss Rush'),
        ('CATACOMBS', 'Catacombs'),
        ('CUSTOM', 'Custom Event'),
    )
    
    event_id = models.CharField(
        "Event ID", 
        max_length=50, 
        unique=True, 
        blank=True,
        help_text="Unique ID dari Discord/System"
    )
    name = models.CharField("Nama Event", max_length=100)
    event_type = models.CharField(
        "Tipe Event", 
        max_length=20, 
        choices=EVENT_TYPE_CHOICES
    )
    date = models.DateTimeField("Waktu Event")
    
    # Result fields
    is_completed = models.BooleanField("Selesai (Fisik)", default=False)
    is_finalized = models.BooleanField("Finalized (Poin Dibagi)", default=False, help_text="Set True setelah verifikasi kehadiran")
    is_win = models.BooleanField(
        "Menang", 
        default=False, 
        help_text="Untuk Boss Rush & Catacombs"
    )
    
    # Invasion specific - JSON field untuk boss yang dibunuh
    bosses_killed = models.JSONField(
        "Boss Terbunuh", 
        default=dict, 
        blank=True,
        help_text="Format: {'dragon_beast': true, 'carnifex': true, 'orfen': false}"
    )
    
    # Invasion boss points (editable by admin)
    dragon_beast_points = models.IntegerField(
        "Poin Dragon Beast",
        default=10,
        help_text="Poin bonus jika Dragon Beast terbunuh"
    )
    carnifex_points = models.IntegerField(
        "Poin Carnifex",
        default=15,
        help_text="Poin bonus jika Carnifex terbunuh"
    )
    orfen_points = models.IntegerField(
        "Poin Orfen",
        default=25,
        help_text="Poin bonus jika Orfen terbunuh"
    )
    
    # Custom event specific
    custom_points = models.IntegerField(
        "Poin Custom Event",
        default=10,
        help_text="Poin untuk Custom Event (diisi admin)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Activity Event"
        verbose_name_plural = "Activity Events"
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['is_completed', '-date']),
            models.Index(fields=['event_type', '-date']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate event_id if not provided
        if not self.event_id:
            import uuid
            self.event_id = f"{self.event_type}_{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_event_type_display()} - {self.date.strftime('%Y-%m-%d %H:%M')}"
    
    def calculate_max_points(self):
        """Hitung poin maksimal yang bisa didapat dari event ini"""
        if self.event_type == 'INVASION':
            # DB=10, Carnifex=15, Orfen=25
            points = 5  # Base attendance points
            
            bosses = self.bosses_killed
            
            # Safety check: if stored as string (rare but possible with SQLite/old data)
            if isinstance(bosses, str):
                import json
                try:
                    bosses = json.loads(bosses.replace("'", '"')) # Simple fix for python dict string
                except:
                    bosses = {}
            
            if not isinstance(bosses, dict):
                bosses = {}

            if bosses.get('dragon_beast'):
                points += self.dragon_beast_points or 10
            if bosses.get('carnifex'):
                points += self.carnifex_points or 15
            if bosses.get('orfen'):
                points += self.orfen_points or 25
            return points
        elif self.event_type == 'BOSS_RUSH':
            # Join=20, Win=+10
            return 30 if self.is_win else 20
        elif self.event_type == 'CATACOMBS':
            # Join=15, Win=+10
            return 25 if self.is_win else 15
        elif self.event_type == 'CUSTOM':
            return self.custom_points or 10
        return 0


class PlayerActivity(models.Model):
    """
    Model untuk tracking partisipasi player di setiap event
    """
    STATUS_CHOICES = (
        ('ATTENDED', 'Hadir'),
        ('ABSENT', 'Tidak Hadir'),
    )
    
    player = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name="Karakter"
    )
    event = models.ForeignKey(
        ActivityEvent,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name="Event"
    )
    discord_user_id = models.CharField(
        "Discord User ID", 
        max_length=50, 
        blank=True,
        help_text="Untuk mapping jika check-in via Discord"
    )
    status = models.CharField(
        "Status", 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ATTENDED'
    )
    is_verified = models.BooleanField("Verified", default=False, help_text="Centang jika valid hadir")
    points_earned = models.IntegerField("Poin Didapat", default=0)
    checked_in_at = models.DateTimeField("Waktu Check-In", auto_now_add=True)
    
    # New field: Store per-player boss participation for Invasion
    bosses_killed = models.JSONField(
        "Boss Terbunuh (Individual)", 
        default=dict, 
        blank=True,
        help_text="Spesifik untuk player ini: {'dragon_beast': true, 'carnifex': false, ...}"
    )

    class Meta:
        unique_together = ['player', 'event']
        ordering = ['-event__date']
        verbose_name = "Player Activity"
        verbose_name_plural = "Player Activities"
        indexes = [
            models.Index(fields=['player', 'status']),
            models.Index(fields=['event', 'status']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-calculate points based on event and status
        if self.status == 'ATTENDED':
            if self.event.event_type == 'INVASION':
                # Calculate points from per-player boss kills
                points = 5  # Base attendance
                my_bosses = self.bosses_killed or {}
                if my_bosses.get('dragon_beast') is True or str(my_bosses.get('dragon_beast', '')).lower() == 'true':
                    points += self.event.dragon_beast_points or 10
                if my_bosses.get('carnifex') is True or str(my_bosses.get('carnifex', '')).lower() == 'true':
                    points += self.event.carnifex_points or 15
                if my_bosses.get('orfen') is True or str(my_bosses.get('orfen', '')).lower() == 'true':
                    points += self.event.orfen_points or 25
                self.points_earned = points
            else:
                self.points_earned = self.event.calculate_max_points()
        else:
            self.points_earned = 0
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.player.name} - {self.event.name} ({self.points_earned} pts)"


class PrizePoolConfig(models.Model):
    """
    Configuration for Prize Pool calculation.
    Allows admins to adjust percentages and total pool dynamically.
    """
    total_pool = models.IntegerField("Total Prize Pool", default=10000)
    
    # Percentages (stored as 0.70 for 70%)
    elite_percentage = models.FloatField("Elite %", default=0.20)
    core_percentage = models.FloatField("Core %", default=0.70)
    active_percentage = models.FloatField("Active %", default=0.10)
    casual_percentage = models.FloatField("Casual %", default=0.00)
    
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        # Validate total is 1.0 (allow small float error)
        total = self.elite_percentage + self.core_percentage + self.active_percentage + self.casual_percentage
        if not (0.99 <= total <= 1.01):
            # We won't raise error to avoid breaking admin saving, but backend logic should be careful
            pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Prize Pool Configuration"
        verbose_name_plural = "Prize Pool Configurations" 
        
    def __str__(self):
        return f"Config (Pool: {self.total_pool})"


class MonthlyReport(models.Model):
    """
    Model untuk menyimpan rekap bulanan per player
    """
    TIER_CHOICES = (
        ('ELITE', '🏆 Elite'),
        ('CORE', '⚔️ Core'),
        ('ACTIVE', '🛡️ Active'),
        ('CASUAL', '🌱 Casual'),
    )
    
    month = models.DateField("Bulan", help_text="Tanggal bulan (hari=1)")
    player = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='monthly_reports',
        verbose_name="Karakter"
    )
    
    # Calculated fields
    total_events = models.IntegerField("Total Event", default=0)
    attended_events = models.IntegerField("Event Dihadiri", default=0)
    attendance_rate = models.FloatField("Attendance Rate", default=0.0)
    
    activity_score = models.IntegerField("Skor Aktivitas", default=0)
    consistency_bonus = models.IntegerField("Bonus Konsistensi", default=0)
    decay_penalty = models.IntegerField("Decay Penalty", default=0)
    manual_adjustment = models.IntegerField("Manual Adjustment", default=0)
    total_score = models.IntegerField("Total Skor", default=0)
    
    tier = models.CharField(
        "Tier", 
        max_length=20, 
        choices=TIER_CHOICES, 
        default='CASUAL'
    )
    is_qualified = models.BooleanField("Qualified untuk Reward", default=False)
    prize_amount = models.IntegerField("Jumlah Hadiah", default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['month', 'player']
        ordering = ['-month', '-total_score']
        verbose_name = "Monthly Report"
        verbose_name_plural = "Monthly Reports"
        indexes = [
            models.Index(fields=['month', 'tier']),
            models.Index(fields=['-total_score']),
            models.Index(fields=['player', 'month']),
        ]
    
    def calculate_tier(self):
        """Determine tier based on total score"""
        if self.total_score >= 900:
            return 'ELITE'
        elif self.total_score >= 600:
            return 'CORE'
        elif self.total_score >= 300:
            return 'ACTIVE'
        return 'CASUAL'
    
    def calculate_consistency_bonus(self):
        """Calculate consistency bonus based on attendance rate"""
        if self.attendance_rate >= 0.9:
            return 150
        elif self.attendance_rate >= 0.7:
            return 100
        elif self.attendance_rate >= 0.5:
            return 50
        return 0
    
    def save(self, *args, **kwargs):
        # Auto-calculate tier and qualification
        self.tier = self.calculate_tier()
        self.is_qualified = self.tier != 'CASUAL'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.player.name} - {self.month.strftime('%B %Y')} ({self.get_tier_display()})"



