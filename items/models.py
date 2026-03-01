

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

CLASS_TO_WEAPON_TYPE = {
    'One-Handed Sword Skill': 'one_handed_sword',
    'Dual-Wield Skills': 'two_sword_style',
    'Dagger Skill': 'dagger',
    'Bow Skill': 'bow',
    'Staff Skill': 'cane',
    'Greatsword Skill': 'greatsword',
    'Crossbow Skill': 'crossbow',
    'Chainsword Skill': 'chainsword',
    'Rapier Skill': 'rapier',
    'Magic Cannon Skill': 'magic_cannon',
    'Spear Skill': 'spear',
    'Orb Skill': 'orb',
    'Dual Axe Skill': 'double_axe',
    'Soul Breaker Skill': 'soul_breaker',
}

CLASS_SKILLS_DATA = {
    'One-Handed Sword Skill': {
        'myth': ['Dignity (one-handed sword)', 'Ignore Death', 'Mighty Shock', 'Authority (one-handed sword)'],
        'legend': ['Provoke', 'Aegis', 'Last stance', 'Revenge', 'True Impact', 'Vengeance', 'Chain Strike', 'Brutal Attack'],
        'hero': ['Toughness', 'Retribution', 'Strike Force', 'Holy Strike', 'Double Shock', 'Will of Iron', 'Touch of Life', 'Hate']
    },
    'Dual-Wield Skills': {
        'myth': ['Dignity (dual swordsmanship)', 'Force Blaster', 'Crack Down', 'Authority (dual sword)'],
        'legend': ['Savage Scourge', 'Dance of Might', 'Approach', 'Split slash', 'Cruel Slasher', 'Berserker', 'Breaking Armor', 'Dual Impact'],
        'hero': ['Phoenix', 'Scourge', 'Sonic Mastery', 'Dual parrying', 'Triple slash', 'Sonic Blaster', 'Dance of Fury', 'Detect Weekness']
    },
    'Dagger Skill': {
        'myth': ['Dignity (dagger)', 'flash', 'Betrayal', 'Authority (Dagger)'],
        'legend': ['Flow State', 'swift', 'toxin', 'Death sign', 'Poison Explosion', 'Phantom Blade', 'marionette', 'Shadow Staff'],
        'hero': ['Fatal Blow', 'Poisoning Spring', 'Poison terror', 'Reset movement', 'Vision of Assassin', 'Shadow Blade', 'Venom', 'Hyde']
    },
    'Bow Skill': {
        'myth': ['Dignity (bow)', 'Rock on', 'Eraser', 'Authority (Bow)'],
        'legend': ['Sweep shot', 'Recoil', 'Entangled Field', 'Energy Shield', 'Hyper Draw', 'Elimination', 'Pinpoint shot', 'Absolute Piercing'],
        'hero': ['Sniper Spirit', 'Multi-shot', 'Quick Draw', 'Impact Shot', 'Death Stinger', 'Mana Regain', 'Entangle', 'Real Target']
    },
    'Staff Skill': {
        'myth': ['Dignity (Staff)', 'Portable Gravity', 'Abyss', 'Authority (Staff)'],
        'legend': ['Warp', 'Restore Casting II', 'Glacier Crystal', 'Glacier Storm', 'Stigma', 'Chaos', 'Gravity', 'Meteor'],
        'hero': ['Sage Shield', 'Gust Strike', 'Tempest III', 'Frozen Crystal', 'Blizzard Storm', 'Cancel', 'Restore Casting I', 'Confuse']
    },
    'Orb Skill': {
        'myth': ['Dignity (of)', 'Blessed Field', 'Sacredness', 'Authority (Orb)'],
        'legend': ['Full heel', 'High Cure', 'Double Shield', 'Saint Guillotine', 'Celestial Shield', 'reposal', 'Pain of Karma', 'Frey'],
        'hero': ['Mess Hill', 'Holy Light', 'Last Hill', 'Divine Execution', 'Divine Spark', 'Improved of', 'Judgment', 'Arcane Shield']
    },
    'Spear Skill': {
        'myth': ['Dignity (Spear)', 'Emperor\'s Lore', 'Dive Storm', 'Authority (Spear)'],
        'legend': ['Commander Shout', 'Lightning Bind', 'Helios Strike', 'Untouchable Force', 'Immortal', 'Absolute Spear', 'Rolling Thunder', 'Earthquake Stomp'],
        'hero': ['War Hero', 'Perfect Spear', 'Piece of Mind', 'Giant Stomp', 'Frenzy', 'Vital Destruction', 'Disarm', 'Infinity Strike']
    },
    'Greatsword Skill': {
        'myth': ['Dignity (Greatsword)', 'Paradox', 'Gigantic Bash', 'Authority (Greatsword)'],
        'legend': ['Agent Shield', 'Reflect Ability', 'Hell Flare', 'Disregard', 'drain', 'Force Rage', 'Madness', 'genocide'],
        'hero': ['Crescendo Vitality', 'Quake', 'Reflect stun', 'Hellfire', 'Bash III', 'War Rage', 'Guardian Shield', 'Wave Sword']
    },
    'Crossbow Skill': {
        'myth': ['Dignity (Crossbow)', 'Dimension Void', 'quasar', 'Isoriti (Crossbow)'],
        'legend': ['Gigantic Hunter', 'Nerve cut', 'Disperse', 'Tumble down', 'Focusing', 'Absolute Mirror', 'Proxima', 'Curse Paralyze'],
        'hero': ['Heroic Change', 'Feralize', 'chain bolt', 'Blackout Bolt Shot', 'Escape', 'Back tumbling', 'Disciplin', 'Vampiric Mind']
    },
    'Chainsword Skill': {
        'myth': ['Dignity (Chainsword)', 'Overlord', 'Soul Steel', 'Authority (Chainsword)'],
        'legend': ['Eternal Force', 'binding shock', 'Double Chasing', 'Vampiric Zone', 'Evolution', 'Vampiric Shield', 'Blood Slash III', 'Bloody Steel'],
        'hero': ['Chain Galaxy', 'Overflow', 'binding', 'Bloody Sword', 'Double Whip', 'Rust', 'Chain Chasing', 'Bloody Slash II']
    },
    'Rapier Skill': {
        'myth': ['Dignity (Rapier)', 'Over speed', 'Companion', 'Authority (Rapier)'],
        'legend': ['Feather Shower', 'Awake', 'Shooting Star II', 'Extreme Move', 'Rapierism', 'Blink', 'Raven Claw', 'Darkwing'],
        'hero': ['feather pool', 'Black Feather', 'Shooting Star Ⅰ', 'Sword Blossom', 'Sting III', 'Traceless', 'Parrying Arrow', 'Summon Sword']
    },
    'Magic Cannon Skill': {
        'myth': ['Dignity (Magic Cannon)', 'Hyperion Barrier', 'Chrono Circle', 'Authority (Magic Cannon)'],
        'legend': ['Cross wound', 'Aegis Barrier', 'deep sleep', 'Night Expansion', 'Meta Viper', 'Blast Bomb III', 'Charge barrier', 'Recharge Shot'],
        'hero': ['Canon Night', 'Assemble', 'slip', 'Canon Expansion', 'barrier shot', 'Blast Bomb II', 'Enchant Aiming', 'Magic Trace']
    },
    'Dual Axe Skill': {
        'myth': ['Dignity (Dual Axe)', 'Berserker Wrath', 'Storm Cleave', 'Authority (Dual Axe)'],
        'legend': ['Whirlwind Strike', 'Fury Slash', 'Twin Crusher', 'Savage Spin', 'Rage Impact', 'Power Shatter', 'Double Decimation', 'Cyclone Fury'],
        'hero': ['Rage Strike', 'Power Crush', 'Whirlwind', 'Execute', 'Blood Rage', 'Armor Break', 'Cyclone', 'Berserk Fury']
    },
    'Soul Breaker Skill': {
        'myth': ['Dignity (Soul Breaker)', 'Void Realm', 'Soul Harvest', 'Authority (Soul Breaker)'],
        'legend': ['Soul Rend', 'Dark Pulse', 'Spirit Chains', 'Phantom Strike', 'Soul Absorb', 'Shadow Wave', 'Chaos Rift', 'Nether Blade'],
        'hero': ['Soul Strike', 'Dark Blast', 'Soul Drain', 'Shadow Burst', 'Void Slash', 'Soul Shatter', 'Dark Impulse', 'Annihilation']
    },
}



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

    # JSONFields for myth and legend tier skills (hero skills remain as individual boolean fields below)
    # Structure: {"dualblade": ["Dignity (dual swordsmanship)", "Force Blaster"], "tank": ["Provoke", "Aegis"], ...}
    myth_skills = models.JSONField("Myth Skills", default=dict, blank=True, help_text="Unlocked myth-tier skills per subclass")
    legend_skills = models.JSONField("Legend Skills", default=dict, blank=True, help_text="Unlocked legend-tier skills per subclass")

    # JSONField to store weapon selection from database per subclass
    # Structure: {"dualblade": "two_sword_style|Dark Legion", "tank": "one_handed_sword|Sword of Valhalla", ...}
    subclass_weapons = models.JSONField("Subclass Weapons", default=dict, blank=True, help_text="Selected weapon per subclass from weapon database")

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

    # ====== GREATSWORD SUBCLASS ======
    greatsword_crescendo_vitality = models.BooleanField("Crescendo Vitality", default=False)
    greatsword_quake = models.BooleanField("Quake", default=False)
    greatsword_reflect_stun = models.BooleanField("Reflect Stun", default=False)
    greatsword_hellfire = models.BooleanField("Hellfire", default=False)
    greatsword_bash = models.BooleanField("Bash III", default=False)
    greatsword_war_rage = models.BooleanField("War Rage", default=False)
    greatsword_guardian_shield = models.BooleanField("Guardian Shield", default=False)
    greatsword_wave_sword = models.BooleanField("Wave Sword", default=False)
    greatsword_weapon = models.CharField("Greatsword Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('berserker_blade', "Berserker Blade"),
        ('archangel', 'Archangel Slasher'),
        ('doom_crusher', "Doom Crusher"),
        ('dragon_slayer', "Dragon Slayer"),
        ('black_ore', "Black Ore Greatsword"),
    ], default='none')

    # ====== CROSSBOW SUBCLASS ======
    crossbow_heroic_change = models.BooleanField("Heroic Change", default=False)
    crossbow_feralize = models.BooleanField("Feralize", default=False)
    crossbow_chain_bolt = models.BooleanField("Chain Bolt", default=False)
    crossbow_blackout_bolt = models.BooleanField("Blackout Bolt Shot", default=False)
    crossbow_escape = models.BooleanField("Escape", default=False)
    crossbow_back_tumbling = models.BooleanField("Back Tumbling", default=False)
    crossbow_disciplin = models.BooleanField("Disciplin", default=False)
    crossbow_vampiric_mind = models.BooleanField("Vampiric Mind", default=False)
    crossbow_weapon = models.CharField("Crossbow Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('arbalester', "Arbalester"),
        ('archangel', 'Archangel Shooter'),
        ('ballista', "Ballista"),
        ('death_trigger', "Death Trigger"),
        ('evil_spirit', "Evil Spirit Crossbow"),
    ], default='none')

    # ====== CHAINSWORD SUBCLASS ======
    chainsword_chain_galaxy = models.BooleanField("Chain Galaxy", default=False)
    chainsword_overflow = models.BooleanField("Overflow", default=False)
    chainsword_binding = models.BooleanField("Binding", default=False)
    chainsword_bloody_sword = models.BooleanField("Bloody Sword", default=False)
    chainsword_double_whip = models.BooleanField("Double Whip", default=False)
    chainsword_rust = models.BooleanField("Rust", default=False)
    chainsword_chain_chasing = models.BooleanField("Chain Chasing", default=False)
    chainsword_bloody_slash = models.BooleanField("Bloody Slash II", default=False)
    chainsword_weapon = models.CharField("Chainsword Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('chain_hydra', "Chain Hydra"),
        ('archangel', 'Archangel Chain'),
        ('viper_chain', "Viper Chain"),
        ('bloody_chain', "Bloody Chain"),
        ('demon_chain', "Demon Chain"),
    ], default='none')

    # ====== RAPIER SUBCLASS ======
    rapier_feather_pool = models.BooleanField("Feather Pool", default=False)
    rapier_black_feather = models.BooleanField("Black Feather", default=False)
    rapier_shooting_star = models.BooleanField("Shooting Star", default=False)
    rapier_sword_blossom = models.BooleanField("Sword Blossom", default=False)
    rapier_sting = models.BooleanField("Sting III", default=False)
    rapier_traceless = models.BooleanField("Traceless", default=False)
    rapier_parrying_arrow = models.BooleanField("Parrying Arrow", default=False)
    rapier_summon_sword = models.BooleanField("Summon Sword", default=False)
    rapier_weapon = models.CharField("Rapier Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('needle_rapier', "Needle Rapier"),
        ('archangel', 'Archangel Rapier'),
        ('wind_rider', "Wind Rider"),
        ('phantom_rapier', "Phantom Rapier"),
        ('blood_rapier', "Blood Rapier"),
    ], default='none')

    # ====== MAGIC CANNON SUBCLASS ======
    cannon_canon_night = models.BooleanField("Canon Night", default=False)
    cannon_assemble = models.BooleanField("Assemble", default=False)
    cannon_slip = models.BooleanField("Slip", default=False)
    cannon_canon_expansion = models.BooleanField("Canon Expansion", default=False)
    cannon_barrier_shot = models.BooleanField("Barrier Shot", default=False)
    cannon_blast_bomb = models.BooleanField("Blast Bomb II", default=False)
    cannon_enchant_aiming = models.BooleanField("Enchant Aiming", default=False)
    cannon_magic_trace = models.BooleanField("Magic Trace", default=False)
    cannon_weapon = models.CharField("Magic Cannon Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('spirit_cannon', "Spirit Cannon"),
        ('archangel', 'Archangel Cannon'),
        ('dark_cannon', "Dark Cannon"),
        ('thunder_cannon', "Thunder Cannon"),
        ('demon_cannon', "Demon Cannon"),
    ], default='none')

    # ====== ORB SUBCLASS ======
    orb_mess_hill = models.BooleanField("Mess Hill", default=False)
    orb_holy_light = models.BooleanField("Holy Light", default=False)
    orb_last_hill = models.BooleanField("Last Hill", default=False)
    orb_divine_execution = models.BooleanField("Divine Execution", default=False)
    orb_divine_spark = models.BooleanField("Divine Spark", default=False)
    orb_improved_orb = models.BooleanField("Improved Orb", default=False)
    orb_judgment = models.BooleanField("Judgment", default=False)
    orb_arcane_shield = models.BooleanField("Arcane Shield", default=False)
    orb_weapon = models.CharField("Orb Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('holy_orb', "Holy Orb"),
        ('archangel', 'Archangel Orb'),
        ('spirit_orb', "Spirit Orb"),
        ('divine_orb', "Divine Orb"),
        ('celestial_orb', "Celestial Orb"),
    ], default='none')

    # ====== DUAL AXE SUBCLASS ======
    dualaxe_rage_strike = models.BooleanField("Rage Strike", default=False)
    dualaxe_power_crush = models.BooleanField("Power Crush", default=False)
    dualaxe_whirlwind = models.BooleanField("Whirlwind", default=False)
    dualaxe_execute = models.BooleanField("Execute", default=False)
    dualaxe_blood_rage = models.BooleanField("Blood Rage", default=False)
    dualaxe_armor_break = models.BooleanField("Armor Break", default=False)
    dualaxe_cyclone = models.BooleanField("Cyclone", default=False)
    dualaxe_berserk_fury = models.BooleanField("Berserk Fury", default=False)
    dualaxe_weapon = models.CharField("Dual Axe Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('twin_edge', "Twin Edge"),
        ('archangel', 'Archangel Dual Axe'),
        ('destroyer', "Destroyer"),
        ('blood_axes', "Blood Axes"),
        ('doom_axes', "Doom Axes"),
    ], default='none')

    # ====== SOUL BREAKER SUBCLASS ======
    soulbreaker_soul_strike = models.BooleanField("Soul Strike", default=False)
    soulbreaker_dark_blast = models.BooleanField("Dark Blast", default=False)
    soulbreaker_soul_drain = models.BooleanField("Soul Drain", default=False)
    soulbreaker_shadow_burst = models.BooleanField("Shadow Burst", default=False)
    soulbreaker_void_slash = models.BooleanField("Void Slash", default=False)
    soulbreaker_soul_shatter = models.BooleanField("Soul Shatter", default=False)
    soulbreaker_dark_impulse = models.BooleanField("Dark Impulse", default=False)
    soulbreaker_annihilation = models.BooleanField("Annihilation", default=False)
    soulbreaker_weapon = models.CharField("Soul Breaker Weapon", max_length=50, choices=[
        ('none', 'Blue or lower or none'),
        ('soul_edge', "Soul Edge"),
        ('archangel', 'Archangel Breaker'),
        ('dark_breaker', "Dark Breaker"),
        ('phantom_breaker', "Phantom Breaker"),
        ('chaos_breaker', "Chaos Breaker"),
    ], default='none')

    def calculate_subclass_score(self):
        """Calculate subclass score based on all skill tiers and weapons"""
        score = 0

        # ======== MYTH SKILLS (from JSONField) - 15 points each ========
        myth_data = self.myth_skills or {}
        for prefix, skills in myth_data.items():
            if isinstance(skills, list):
                score += len(skills) * 15

        # ======== LEGEND SKILLS (from JSONField) - 12 points each ========
        legend_data = self.legend_skills or {}
        for prefix, skills in legend_data.items():
            if isinstance(skills, list):
                score += len(skills) * 12

        # ======== HERO SKILLS (Boolean fields) - 10 points each ========
        hero_skill_fields = [
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
            # Greatsword
            self.greatsword_crescendo_vitality, self.greatsword_quake, self.greatsword_reflect_stun,
            self.greatsword_hellfire, self.greatsword_bash, self.greatsword_war_rage,
            self.greatsword_guardian_shield, self.greatsword_wave_sword,
            # Crossbow
            self.crossbow_heroic_change, self.crossbow_feralize, self.crossbow_chain_bolt,
            self.crossbow_blackout_bolt, self.crossbow_escape, self.crossbow_back_tumbling,
            self.crossbow_disciplin, self.crossbow_vampiric_mind,
            # Chainsword
            self.chainsword_chain_galaxy, self.chainsword_overflow, self.chainsword_binding,
            self.chainsword_bloody_sword, self.chainsword_double_whip, self.chainsword_rust,
            self.chainsword_chain_chasing, self.chainsword_bloody_slash,
            # Rapier
            self.rapier_feather_pool, self.rapier_black_feather, self.rapier_shooting_star,
            self.rapier_sword_blossom, self.rapier_sting, self.rapier_traceless,
            self.rapier_parrying_arrow, self.rapier_summon_sword,
            # Magic Cannon
            self.cannon_canon_night, self.cannon_assemble, self.cannon_slip,
            self.cannon_canon_expansion, self.cannon_barrier_shot, self.cannon_blast_bomb,
            self.cannon_enchant_aiming, self.cannon_magic_trace,
            # Orb
            self.orb_mess_hill, self.orb_holy_light, self.orb_last_hill,
            self.orb_divine_execution, self.orb_divine_spark, self.orb_improved_orb,
            self.orb_judgment, self.orb_arcane_shield,
            # Dual Axe
            self.dualaxe_rage_strike, self.dualaxe_power_crush, self.dualaxe_whirlwind,
            self.dualaxe_execute, self.dualaxe_blood_rage, self.dualaxe_armor_break,
            self.dualaxe_cyclone, self.dualaxe_berserk_fury,
            # Soul Breaker
            self.soulbreaker_soul_strike, self.soulbreaker_dark_blast, self.soulbreaker_soul_drain,
            self.soulbreaker_shadow_burst, self.soulbreaker_void_slash, self.soulbreaker_soul_shatter,
            self.soulbreaker_dark_impulse, self.soulbreaker_annihilation,
        ]

        for skill in hero_skill_fields:
            if skill:
                score += 10

        # ======== WEAPONS from subclass_weapons JSONField - 20 points each ========
        weapons_data = self.subclass_weapons or {}
        for prefix, weapon_value in weapons_data.items():
            if weapon_value and weapon_value != '' and weapon_value != 'none':
                score += 20

        return score

    def __str__(self):

        return f"Subclass Info for {self.character.name}"



class LegendaryClass(models.Model):

    name = models.CharField("Nama", max_length=100)

    icon_file = models.CharField("File Ikon", max_length=100, blank=True)

    def __str__(self):

        return self.name



class MythicClass(models.Model):

    name = models.CharField("Nama", max_length=100)

    icon_file = models.CharField("File Ikon", max_length=100, blank=True)

    def __str__(self):

        return self.name



class LegendaryAgathion(models.Model):

    name = models.CharField("Nama", max_length=100)

    icon_file = models.CharField("File Ikon", max_length=100, blank=True)

    def __str__(self):

        return self.name


class LegendaryMount(models.Model):

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

    mythic_classes = models.ManyToManyField(MythicClass, verbose_name="Kelas Mythic", blank=True)

    legendary_classes = models.ManyToManyField(LegendaryClass, verbose_name="Kelas Legendaris", blank=True)

    legendary_agathions = models.ManyToManyField(LegendaryAgathion, verbose_name="Agathion Legendaris", blank=True)

    legendary_mounts = models.ManyToManyField(LegendaryMount, verbose_name="Mount Legendaris", blank=True)

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
        characteristics_score = 0.0
        try:
            char_stats = self.characteristics_stats
            characteristics_score = float(char_stats.calculate_total_score())
        except CharacteristicsStats.DoesNotExist:
            pass

        # 2. SUB-CLASS SCORE
        subclass_score = 0.0
        try:
            subclass = self.subclass_stats
            subclass_score = float(subclass.calculate_subclass_score())
        except SubclassStats.DoesNotExist:
            pass

        # 3. MAIN CLASS SCORE (Gear Score Stats - KELOMPOK G)
        mainclass_score = 0.0
        dmg = acc = def_stat = reduc = resist = skill_dmg_boost = wpn_dmg_boost = soulshot = valor = guardian = conquer = 0
        try:
            attrs = self.attributes
            g_score = (
                0.5 * (attrs.g1 + attrs.g2 + attrs.g3 + attrs.g4 + attrs.g5 + attrs.g6 + attrs.g7) +
                0.005 * (attrs.g8 + attrs.g11 + attrs.g12 + attrs.g13 + attrs.g27 + attrs.g28 + attrs.g33) +
                0.0005 * (attrs.g9 + attrs.g10) +
                0.0001 * (attrs.g34) +
                0.05 * (attrs.g14 + attrs.g15 + attrs.g17 + attrs.g18 + attrs.g20 + attrs.g21 + attrs.g29 + attrs.g30 + attrs.g31 + attrs.g32) +
                0.005 * (attrs.g16 + attrs.g19 + attrs.g22 + attrs.g23 + attrs.g24 + attrs.g25 + attrs.g26) +
                0.15 * attrs.g35 + 0.2 * attrs.g36 + 0.2 * attrs.g37 + 0.25 * attrs.g38
            )
            mainclass_score = float(g_score)
            
            # backward compatibility for view returning attributes (though no longer accurate for original intent)
            dmg = attrs.g14
            acc = attrs.g15
            def_stat = attrs.g12
            soulshot = attrs.g35
            valor = attrs.g36
        except CharacterAttributes.DoesNotExist:
            pass

        # TOTAL SCORE
        total_score = characteristics_score + subclass_score + mainclass_score

        return {
            'total_score': total_score,
            'gear_stats_score': mainclass_score,
            'characteristics': characteristics_score,
            'subclass': subclass_score,
            'mainclass': mainclass_score,
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
            'legend_class_point': 0,
            'legend_agathion_point': 0,
            'total_legend_codex': 0,
            'total_epic_mount': 0,
        }

    def calculate_gear_score(self):
        breakdown = self.calculate_gear_score_breakdown()
        return breakdown['total_score']







# PvP Gear Choices

PVP_HELMET_CHOICES = [
    ('', 'No helmet selected'),
    ("Ancient Elven Helmet", "Ancient Elven Helmet"),
    ("Crown of the World Tree", "Crown of the World Tree"),
    ("Dark Crystal Helmet", "Dark Crystal Helmet"),
    ("Devil's Helmet", "Devil's Helmet"),
    ("Draconic Leather Helmet", "Draconic Leather Helmet"),
    ("Helmet of the Fallen Angel", "Helmet of the Fallen Angel"),
    ("Hildegrim", "Hildegrim"),
    ("Imperial Crusader Helmet", "Imperial Crusader Helmet"),
    ("Majestic Circlet", "Majestic Circlet"),
    ("Major Arcana Circlet", "Major Arcana Circlet"),
    ("Medusa's Helmet", "Medusa's Helmet"),
    ("Nebit's Helmet", "Nebit's Helmet"),
    ("Nightmare Helmet", "Nightmare Helmet"),
    ("Pauline's Helmet", "Pauline's Helmet"),
    ("Tersi's Circlet", "Tersi's Circlet"),
]

PVP_GLOVES_CHOICES = [
    ('', 'No gloves selected'),
    ("Ancient Elven Gauntlets", "Ancient Elven Gauntlets"),
    ("Dark Crystal Globe", "Dark Crystal Globe"),
    ("Devil's Gauntlet", "Devil's Gauntlet"),
    ("Draconic Leather Gloves", "Draconic Leather Gloves"),
    ("Fallen Angel's Gloves", "Fallen Angel's Gloves"),
    ("Globe of the Forgotten Hero", "Globe of the Forgotten Hero"),
    ("Gloves of Blessing", "Gloves of Blessing"),
    ("Guardian of Vision", "Guardian of Vision"),
    ("Jarngreifr", "Jarngreifr"),
    ("Majestic Gloves", "Majestic Gloves"),
    ("Nebit's Globe", "Nebit's Globe"),
    ("Nightmare Gauntlet", "Nightmare Gauntlet"),
    ("Paagrio's Flame", "Paagrio's Flame"),
    ("Pauline's Gauntlet", "Pauline's Gauntlet"),
    ("Tersi's Gloves", "Tersi's Gloves"),
]

PVP_BOOTS_CHOICES = [
    ('', 'No boots selected'),
    ("Ancient Elven Boots", "Ancient Elven Boots"),
    ("Boots of Eternal Life", "Boots of Eternal Life"),
    ("Boots of the Forgotten Hero", "Boots of the Forgotten Hero"),
    ("Calie's Boots", "Calie's Boots"),
    ("Dark Crystal Boots", "Dark Crystal Boots"),
    ("Devil's Boots", "Devil's Boots"),
    ("Draconic Leather Boots", "Draconic Leather Boots"),
    ("Fallen Angel's Boots", "Fallen Angel's Boots"),
    ("Majestic Boots", "Majestic Boots"),
    ("Nebit's Boots", "Nebit's Boots"),
    ("Nightmare Boots", "Nightmare Boots"),
    ("Pauline's Boots", "Pauline's Boots"),
    ("Reaper's Boots", "Reaper's Boots"),
    ("Saiha's Wind", "Saiha's Wind"),
    ("Tersi's Boots", "Tersi's Boots"),
]

PVP_GAITERS_CHOICES = [
    ('', 'No gaiters selected'),
    ("Basil's Shell", "Basil's Shell"),
    ("Blood Greaves", "Blood Greaves"),
    ("Blue Wolf's Leggings", "Blue Wolf's Leggings"),
    ("Breath of Silen", "Breath of Silen"),
    ("Crystal Gaiters", "Crystal Gaiters"),
    ("Devil's Pact", "Devil's Pact"),
    ("Fallen Angel's Legguards", "Fallen Angel's Legguards"),
    ("Flame Greaves", "Flame Greaves"),
    ("Forgotten Hero's Greaves", "Forgotten Hero's Greaves"),
    ("Full Plate Gaiters", "Full Plate Gaiters"),
    ("Ice Leggings", "Ice Leggings"),
    ("Imperial Crusader Legguards", "Imperial Crusader Legguards"),
    ("Light's Greaves", "Light's Greaves"),
    ("Patience Leggings", "Patience Leggings"),
    ("Spirit's Greaves", "Spirit's Greaves"),
]

PVP_ARMOR_CHOICES = [
    ('', 'No armor selected'),
    ("Absolute Tunic", "Absolute Tunic"),
    ("Apella's Armor", "Apella's Armor"),
    ("Breastplate of the Fallen Angel", "Breastplate of the Fallen Angel"),
    ("Breastplate of the Forgotten Hero", "Breastplate of the Forgotten Hero"),
    ("Dark Crystal Breastplate", "Dark Crystal Breastplate"),
    ("Devil's Armor", "Devil's Armor"),
    ("Draconic Leather Armor", "Draconic Leather Armor"),
    ("Imperial Crusader Breastplate", "Imperial Crusader Breastplate"),
    ("Majestic Robe", "Majestic Robe"),
    ("Major Arcana Robe", "Major Arcana Robe"),
    ("Nebit's Armor", "Nebit's Armor"),
    ("Nightmare Armor", "Nightmare Armor"),
    ("Polyne's Breastplate", "Polyne's Breastplate"),
    ("Saban's Robe", "Saban's Robe"),
    ("Tersi's Robe", "Tersi's Robe"),
]

PVP_CLOAK_CHOICES = [
    ('', 'No cloak selected'),
    ("Aegis Cloak", "Aegis Cloak"),
    ("Cloak of Power", "Cloak of Power"),
    ("Cloak of Silence", "Cloak of Silence"),
    ("Cloak of Verdant Green", "Cloak of Verdant Green"),
    ("Cranbel's Cloak", "Cranbel's Cloak"),
    ("Dragon's Scales", "Dragon's Scales"),
    ("Freya's Cloak", "Freya's Cloak"),
    ("Jaqen's Cloak", "Jaqen's Cloak"),
    ("Mantle of the Holy Spirit", "Mantle of the Holy Spirit"),
    ("Moonlight's Cloak", "Moonlight's Cloak"),
    ("Nebit's Cloak of Light", "Nebit's Cloak of Light"),
    ("Niarop's Cloak", "Niarop's Cloak"),
    ("Salamander's Cloak", "Salamander's Cloak"),
    ("Sally Hoden's Wings", "Sally Hoden's Wings"),
    ("Queen Ant Wings", "Queen Ant Wings"),
]

PVP_SIGIL_CHOICES = [
    ('', 'No sigil selected'),
    ("Arcana Sigil", "Arcana Sigil"),
    ("Blood Crystal", "Blood Crystal"),
    ("Cruma's Shell", "Cruma's Shell"),
    ("Crystal of Oblivion", "Crystal of Oblivion"),
    ("Draconic Sigil", "Draconic Sigil"),
    ("Dream Sigil", "Dream Sigil"),
    ("Eldarach", "Eldarach"),
    ("Holy Sigil", "Holy Sigil"),
    ("Parody Sigil", "Parody Sigil"),
    ("Sally Horden's Horn", "Sally Horden's Horn"),
    ("Sniper Sigil", "Sniper Sigil"),
    ("Susceptor's Heart", "Susceptor's Heart"),
    ("The Sigil of the Fallen Angel", "The Sigil of the Fallen Angel"),
    ("The Sigil of Karma", "The Sigil of Karma"),
    ("Tier of Darkness", "Tier of Darkness"),
]

PVP_TSHIRT_CHOICES = [
    ('', 'No t-shirt selected'),
    ("Agility's Anonymous Shirt", "Agility's Anonymous Shirt"),
    ("Anonymous Shirt of Knowledge", "Anonymous Shirt of Knowledge"),
    ("Anonymous Shirt of Strength", "Anonymous Shirt of Strength"),
    ("Focus Shirt", "Focus Shirt"),
    ("Mithril Shirt of Agility", "Mithril Shirt of Agility"),
    ("Mithril Shirt of Knowledge", "Mithril Shirt of Knowledge"),
    ("Mithril Shirt of Strength", "Mithril Shirt of Strength"),
    ("Vigilante Shirt", "Vigilante Shirt"),
    ("Warrior's T-shirt", "Warrior's T-shirt"),
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

SKILL_CHOICES = [
    ("Frenzy", "Frenzy"),
    ("Vital Destruction", "Vital Destruction"),
    ("Infinity Strike", "Infinity Strike"),
    ("Disarm", "Disarm"),
    ("Giant Stomp", "Giant Stomp"),
    ("Absolute Spear", "Absolute Spear"),
    ("Rolling Thunder", "Rolling Thunder"),
    ("Earthquake Stomp", "Earthquake Stomp"),
]

EXPERTISE_CHOICES = [
    (0, 'No Expertise'),
    (1, 'Rank 1'),
    (2, 'Rank 2'),
    (3, 'Rank 3'),
    (4, 'Rank 4'),
    (5, 'Rank 5'),
    (6, 'Rank 6'),
    (7, 'Rank 7'),
    (8, 'Rank 8'),
    (9, 'Rank 9'),
]



WEAPON_CHOICES = [
    ('', 'No weapon selected'),
    ('bow|Akatt Longbow', 'Akatt Longbow'), ('bow|Amenance Bow', 'Amenance Bow'), ('bow|Archangel Bow', 'Archangel Bow'), ('bow|Bow of Oblivion', 'Bow of Oblivion'), ('bow|Bow of the Shingung', 'Bow of the Shingung'), ('bow|Bow of the Soul', 'Bow of the Soul'), ('bow|Carnium Bow', 'Carnium Bow'), ('bow|Devils Bow', 'Devils Bow'), ('bow|Elemental Bow', 'Elemental Bow'), ('bow|Giants Bow', 'Giants Bow'), ('bow|Hazard Bow', 'Hazard Bow'), ('bow|Ice Crystal Bow', 'Ice Crystal Bow'), ('bow|Moonlight Bow', 'Moonlight Bow'), ('bow|Plasma Bow', 'Plasma Bow'),
    ('cane|Archangel Staff', 'Archangel Staff'), ('cane|Bloody Nebulite', 'Bloody Nebulite'), ('cane|Branch of Life', 'Branch of Life'), ('cane|Branches of the World Tree', 'Branches of the World Tree'), ('cane|Commander Staff', 'Commander Staff'), ('cane|Crystal Wand', 'Crystal Wand'), ('cane|Dead Man Staff', 'Dead Man Staff'), ('cane|Desperion Staff', 'Desperion Staff'), ('cane|Ghoul Staff', 'Ghoul Staff'), ('cane|Giant Staff', 'Giant Staff'), ('cane|Imperial Sttaff', 'Imperial Sttaff'), ('cane|Inferno Staff', 'Inferno Staff'), ('cane|Spirit Staff', 'Spirit Staff'),
    ('chainsword|Archangel Chainsword', 'Archangel Chainsword'), ('chainsword|Barakiel Chainsword', 'Barakiel Chainsword'), ('chainsword|Berseker Chainsword', 'Berseker Chainsword'), ('chainsword|Bultgang', 'Bultgang'), ('chainsword|Chrono Kitara', 'Chrono Kitara'), ('chainsword|Dismentor', 'Dismentor'), ('chainsword|Dragon Hunter', 'Dragon Hunter'), ('chainsword|Gram', 'Gram'), ('chainsword|Lightning Chainsword', 'Lightning Chainsword'), ('chainsword|Nameless Victory', 'Nameless Victory'), ('chainsword|Pain of Gardenness', 'Pain of Gardenness'), ('chainsword|Schrager', 'Schrager'),
    ('crossbow|Alvarest', 'Alvarest'), ('crossbow|Archangel Crossbow', 'Archangel Crossbow'), ('crossbow|Ballista', 'Ballista'), ('crossbow|Burst Avenger', 'Burst Avenger'), ('crossbow|Crystal Bowgun', 'Crystal Bowgun'), ('crossbow|Doom Singer', 'Doom Singer'), ('crossbow|Giant Crossbow', 'Giant Crossbow'), ('crossbow|Hellhound', 'Hellhound'), ('crossbow|Peacemaker', 'Peacemaker'), ('crossbow|Tasram', 'Tasram'), ('crossbow|Thorn Crossbow', 'Thorn Crossbow'), ('crossbow|antique crossbow', 'antique crossbow'),
    ('dagger|Archangel Slayer', 'Archangel Slayer'), ('dagger|Blood Orchid', 'Blood Orchid'), ('dagger|Crystal Dagger', 'Crystal Dagger'), ('dagger|Dagger of Contamination', 'Dagger of Contamination'), ('dagger|Dagger of Mana', 'Dagger of Mana'), ('dagger|Devil Dagger', 'Devil Dagger'), ('dagger|Flame Breaker', 'Flame Breaker'), ('dagger|Giant Dagger', 'Giant Dagger'), ('dagger|Hell Knife', 'Hell Knife'), ("dagger|Kruma's Horn", "Kruma's Horn"), ('dagger|Soul Separator', 'Soul Separator'), ('dagger|chris', 'chris'), ('dagger|stiletto', 'stiletto'),
    ('double_axe|Archangel Twin Axe', 'Archangel Twin Axe'), ('double_axe|Bloody Angish', 'Bloody Angish'), ('double_axe|Bloody Cross', 'Bloody Cross'), ('double_axe|Clarent', 'Clarent'), ('double_axe|Cursed Twin Axe', 'Cursed Twin Axe'), ('double_axe|Furious Berserker', 'Furious Berserker'), ('double_axe|Gallatin', 'Gallatin'), ("double_axe|Giant's Twin Axes", "Giant's Twin Axes"), ('double_axe|Ice Storm Twin Axe', 'Ice Storm Twin Axe'), ('double_axe|Madness Twin Axe', 'Madness Twin Axe'), ('double_axe|Meteor Impact', 'Meteor Impact'), ('double_axe|Warpeak', 'Warpeak'), ('double_axe|Yaksha Twin Axe', 'Yaksha Twin Axe'),
    ('greatsword|Archangel Buster', 'Archangel Buster'), ("greatsword|Berserker's Greatsword", "Berserker's Greatsword"), ("greatsword|Commander's Greatsword", "Commander's Greatsword"), ('greatsword|Dragon Slayer', 'Dragon Slayer'), ('greatsword|First Blood', 'First Blood'), ('greatsword|Flamberge', 'Flamberge'), ("greatsword|Guardian's Two-Handed Greatsword", "Guardian's Two-Handed Greatsword"), ("greatsword|Heaven's Wingblade", "Heaven's Wingblade"), ('greatsword|Inferno Master', 'Inferno Master'), ('greatsword|Sword of Iphos', 'Sword of Iphos'),
    ('magic_cannon|Archangel Blaster', 'Archangel Blaster'), ('magic_cannon|Assault Cannon', 'Assault Cannon'), ('magic_cannon|Basilisk Culverin', 'Basilisk Culverin'), ('magic_cannon|Deathbringer', 'Deathbringer'), ('magic_cannon|Divine Blaster', 'Divine Blaster'), ('magic_cannon|Doom Crusher', 'Doom Crusher'), ("magic_cannon|Giant's Blaster", "Giant's Blaster"), ('magic_cannon|Mine Buster', 'Mine Buster'), ('magic_cannon|Pata', 'Pata'), ('magic_cannon|Sarakael Magic Cannon', 'Sarakael Magic Cannon'), ('magic_cannon|Schofield', 'Schofield'), ('magic_cannon|Star Buster', 'Star Buster'), ('magic_cannon|Zephyrus', 'Zephyrus'),
    ('one_handed_sword|Archangel Blade', 'Archangel Blade'), ('one_handed_sword|Elemental Sword', 'Elemental Sword'), ("one_handed_sword|Fighting Father's Sword", "Fighting Father's Sword"), ("one_handed_sword|Giant's Sword", "Giant's Sword"), ("one_handed_sword|Guardian's Sword", "Guardian's Sword"), ('one_handed_sword|Kshanberg', 'Kshanberg'), ('one_handed_sword|Raid Sword', 'Raid Sword'), ('one_handed_sword|Sir Blade', 'Sir Blade'), ('one_handed_sword|Spirits Sword', 'Spirits Sword'), ('one_handed_sword|Sword of Eclipse', 'Sword of Eclipse'), ('one_handed_sword|Sword of Miracle', 'Sword of Miracle'), ('one_handed_sword|Sword of Nightmare', 'Sword of Nightmare'), ('one_handed_sword|Sword of Valhalla', 'Sword of Valhalla'), ('one_handed_sword|Tsurugi', 'Tsurugi'),
    ('orb|Archangel Orb', 'Archangel Orb'), ("orb|Devil's Orb", "Devil's Orb"), ('orb|Dragon Flame Head', 'Dragon Flame Head'), ('orb|Eclipse of', 'Eclipse of'), ('orb|Elysion', 'Elysion'), ('orb|Fairy Queen', 'Fairy Queen'), ("orb|Giant's Orb", "Giant's Orb"), ('orb|Hall of Faith', 'Hall of Faith'), ('orb|Hand of Cabrio', 'Hand of Cabrio'), ('orb|Nirvana', 'Nirvana'), ('orb|Spell Breaker', 'Spell Breaker'), ('orb|The Bones of Kaim Banul', 'The Bones of Kaim Banul'),
    ('rapier|Archangel Rapier', 'Archangel Rapier'), ('rapier|Assault Rapier', 'Assault Rapier'), ('rapier|Blink Rapier', 'Blink Rapier'), ('rapier|Eclair Bijou', 'Eclair Bijou'), ("rapier|Giant's Rapier", "Giant's Rapier"), ('rapier|Glorious', 'Glorious'), ('rapier|Grid Rapier', 'Grid Rapier'), ('rapier|Hauteclair', 'Hauteclair'), ('rapier|Kolishmard', 'Kolishmard'), ('rapier|Levatein', 'Levatein'), ('rapier|Soldat Estark', 'Soldat Estark'), ("rapier|Tromba's Fang", "Tromba's Fang"),
    ('soul_breaker|Archangel Soul Breaker', 'Archangel Soul Breaker'), ('soul_breaker|Blade of Madness', 'Blade of Madness'), ('soul_breaker|Crystal Soul Breaker', 'Crystal Soul Breaker'), ('soul_breaker|Dark Shadow', 'Dark Shadow'), ('soul_breaker|Frostbite', 'Frostbite'), ("soul_breaker|Giant's Soul Breaker", "Giant's Soul Breaker"), ('soul_breaker|Hrunting', 'Hrunting'), ('soul_breaker|Judge of the Sun', 'Judge of the Sun'), ('soul_breaker|Sword of the Soul', 'Sword of the Soul'), ('soul_breaker|Wisdom of our ancestors', 'Wisdom of our ancestors'),
    ('spear|Archangel Halberd', 'Archangel Halberd'), ('spear|Ascalon', 'Ascalon'), ('spear|Battle Spear', 'Battle Spear'), ('spear|Body Slasher', 'Body Slasher'), ("spear|Giant's Spear", "Giant's Spear"), ('spear|Great Axe', 'Great Axe'), ('spear|Halberd', 'Halberd'), ('spear|Heavy War Axe', 'Heavy War Axe'), ('spear|Lancia', 'Lancia'), ('spear|Saint Spear', 'Saint Spear'), ('spear|Scorpion', 'Scorpion'), ('spear|Side', 'Side'), ('spear|Tallum Glaive', 'Tallum Glaive'), ('spear|Typhon Spear', 'Typhon Spear'), ('spear|Widowmaker', 'Widowmaker'),
    ('two_sword_style|Archangel Dual Swords', 'Archangel Dual Swords'), ('two_sword_style|Caribs Dual Swords', 'Caribs Dual Swords'), ('two_sword_style|Damascus Dual Sword', 'Damascus Dual Sword'), ('two_sword_style|Dark Legion', 'Dark Legion'), ('two_sword_style|Death Lord Dual Swords', 'Death Lord Dual Swords'), ("two_sword_style|Giant's Dual Swords", "Giant's Dual Swords"), ('two_sword_style|Homunculus Dual Sword', 'Homunculus Dual Sword'), ("two_sword_style|Mardil's Wrath", "Mardil's Wrath"), ('two_sword_style|Mystery Dual Swords', 'Mystery Dual Swords'), ('two_sword_style|Saint Dual Sword', 'Saint Dual Sword'), ('two_sword_style|Tears of Warrior', 'Tears of Warrior'), ("two_sword_style|Themis's Tongue", "Themis's Tongue"),
]


class CharacterAttributes(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='attributes')
    inheritor_books = models.ManyToManyField(InheritorBook, verbose_name="Buku Inheritor", blank=True)
    epic_classes_count = models.IntegerField("Legend Class Point", default=0)
    epic_agathions_count = models.IntegerField("Legend Agathion Point", default=0)

    soul_prog_attack = models.CharField("Soul Progression Attack", max_length=10, choices=SOUL_PROGRESSION_CHOICES, blank=True)
    soul_prog_defense = models.CharField("Soul Progression Defense", max_length=10, choices=SOUL_PROGRESSION_CHOICES, blank=True)
    soul_prog_blessing = models.CharField("Soul Progression Blessing", max_length=10, choices=SOUL_PROGRESSION_CHOICES, blank=True)

    enchant_bracelet_holy_prot = models.IntegerField("Enchant Bracelet of Holy Protection", choices=ENCHANT_CHOICES, default=0)
    enchant_bracelet_influence = models.IntegerField("Enchant Bracelet of Influence", choices=ENCHANT_CHOICES, default=0)
    enchant_earring_earth = models.IntegerField("Enchant Earth Dragon's Earring", choices=ENCHANT_CHOICES, default=0)
    enchant_earring_fire = models.IntegerField("Enchant Fire Dragon's Earring", choices=ENCHANT_CHOICES, default=0)
    enchant_seal_eva = models.IntegerField("Enchant Eva's Seal", choices=ENCHANT_CHOICES, default=0)
    aster_erafone = models.IntegerField("Aster", default=0, validators=[MinValueValidator(0), MaxValueValidator(30)], help_text="Maksimal 30 Node")

    # Expertise Fields
    exp_one_handed_sword = models.IntegerField("One-Handed Sword Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_dual_wield = models.IntegerField("Dual-Wield Skills", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_dagger = models.IntegerField("Dagger Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_bow = models.IntegerField("Bow Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_staff = models.IntegerField("Staff Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_greatsword = models.IntegerField("Greatsword Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_crossbow = models.IntegerField("Crossbow Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_chainsword = models.IntegerField("Chainsword Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_rapier = models.IntegerField("Rapier Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_magic_cannon = models.IntegerField("Magic Cannon Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_spear = models.IntegerField("Spear Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_orb = models.IntegerField("Orb Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_dual_axe = models.IntegerField("Dual Axe Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)
    exp_soul_breaker = models.IntegerField("Soul Breaker Skill", choices=EXPERTISE_CHOICES, default=0, blank=True)

    # PvP Equipment Fields
    pvp_helmet = models.CharField("PvP Helmet", max_length=100, choices=PVP_HELMET_CHOICES, blank=True)
    pvp_helmet_enchant = models.IntegerField("PvP Helmet Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_gloves = models.CharField("PvP Gloves", max_length=100, choices=PVP_GLOVES_CHOICES, blank=True)
    pvp_gloves_enchant = models.IntegerField("PvP Gloves Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_boots = models.CharField("PvP Boots", max_length=100, choices=PVP_BOOTS_CHOICES, blank=True)
    pvp_boots_enchant = models.IntegerField("PvP Boots Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_gaiters = models.CharField("PvP Gaiters", max_length=100, choices=PVP_GAITERS_CHOICES, blank=True)
    pvp_gaiters_enchant = models.IntegerField("PvP Gaiters Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_top_armor = models.CharField("PvP Top Armor", max_length=100, choices=PVP_ARMOR_CHOICES, blank=True)
    pvp_top_armor_enchant = models.IntegerField("PvP Armor Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_cloak = models.CharField("PvP Cloak", max_length=100, choices=PVP_CLOAK_CHOICES, blank=True)
    pvp_cloak_enchant = models.IntegerField("PvP Cloak Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_tshirt = models.CharField("PvP T-Shirt", max_length=100, choices=PVP_TSHIRT_CHOICES, blank=True)
    pvp_tshirt_enchant = models.IntegerField("PvP T-Shirt Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_sigil = models.CharField("PvP Sigil", max_length=100, choices=PVP_SIGIL_CHOICES, blank=True)
    pvp_sigil_enchant = models.IntegerField("PvP Sigil Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_necklace = models.CharField("PvP Necklace", max_length=100, choices=PVP_NECKLACE_CHOICES, blank=True)
    pvp_necklace_enchant = models.IntegerField("PvP Necklace Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_ring_left = models.CharField("PvP Ring (Left)", max_length=100, choices=PVP_RING_CHOICES, blank=True)
    pvp_ring_left_enchant = models.IntegerField("PvP Ring (Left) Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_ring_right = models.CharField("PvP Ring (Right)", max_length=100, choices=PVP_RING_CHOICES, blank=True)
    pvp_ring_right_enchant = models.IntegerField("PvP Ring (Right) Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    pvp_belt = models.CharField("PvP Belt", max_length=100, choices=PVP_BELT_CHOICES, blank=True)
    pvp_belt_enchant = models.IntegerField("PvP Belt Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])

    # OLD STAT FIELDS (kept for DB compatibility - will be removed after migration)
    soulshot_level = models.IntegerField("Soulshot Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(13)], blank=True)
    valor_level = models.IntegerField("Valor Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(13)], blank=True)
    stat_dmg = models.IntegerField("DMG (Damage)", default=0)
    stat_acc = models.IntegerField("ACC (Accuracy)", default=0)
    stat_def = models.IntegerField("DEF (Defense)", default=0)
    stat_reduc = models.IntegerField("REDUC (Damage Reduction)", default=0)
    stat_resist = models.IntegerField("RESIST (Resistance)", default=0)
    stat_skill_dmg_boost = models.IntegerField("Skill DMG Boost", default=0)
    stat_wpn_dmg_boost = models.IntegerField("Weapon DMG Boost", default=0)
    stat_guardian = models.IntegerField("Guardian", default=0, validators=[MinValueValidator(0), MaxValueValidator(13)], blank=True)
    stat_conquer = models.IntegerField("Conquer", default=0, validators=[MinValueValidator(0), MaxValueValidator(13)], blank=True)
    total_legend_codex = models.IntegerField("Total Legend Codex", default=0)
    total_epic_mount = models.IntegerField("Total Epic Mount", default=0)

    # KELOMPOK G - BASE STATS
    g1 = models.IntegerField("Melee Damage Reduction", default=0)
    g2 = models.IntegerField("Ranged Damage Reduction", default=0)
    g3 = models.IntegerField("Magic Damage Reduction", default=0)
    g4 = models.IntegerField("Melee Evasion", default=0)
    g5 = models.IntegerField("Ranged Evasion", default=0)
    g6 = models.IntegerField("Magic Evasion", default=0)
    g7 = models.IntegerField("Skill Resistance", default=0)
    g8 = models.IntegerField("Movement Speed (%)", default=0)
    g9 = models.IntegerField("Max HP", default=0)
    g10 = models.IntegerField("Max MP", default=0)
    g11 = models.IntegerField("Weapon Block (%)", default=0)
    g12 = models.IntegerField("Defense", default=0)
    g13 = models.IntegerField("Cooldown Reduction (%)", default=0)
    g14 = models.IntegerField("Melee Damage", default=0)
    g15 = models.IntegerField("Melee Accuracy", default=0)
    g16 = models.IntegerField("Melee Critical Hit (%)", default=0)
    g17 = models.IntegerField("Ranged Damage", default=0)
    g18 = models.IntegerField("Ranged Accuracy", default=0)
    g19 = models.IntegerField("Ranged Critical Hit (%)", default=0)
    g20 = models.IntegerField("Magic Damage", default=0)
    g21 = models.IntegerField("Magic Accuracy", default=0)
    g22 = models.IntegerField("Magic Critical Hit (%)", default=0)
    g23 = models.IntegerField("Weapon Damage Boost (%)", default=0)
    g24 = models.IntegerField("Weapon Defense (%)", default=0)
    g25 = models.IntegerField("Skill Damage Boost (%)", default=0)
    g26 = models.IntegerField("Skill Defense (%)", default=0)
    g27 = models.IntegerField("Attack Speed (%)", default=0)
    g28 = models.IntegerField("Cast Speed (%)", default=0)
    g29 = models.IntegerField("Weapon Damage", default=0)
    g30 = models.IntegerField("Extra Damage", default=0)
    g31 = models.IntegerField("HP Recovery (Tick)", default=0)
    g32 = models.IntegerField("MP Recovery (Tick)", default=0)
    g33 = models.IntegerField("MP Consumption Reduction (%)", default=0)
    g34 = models.IntegerField("Weight Limit", default=0)
    g35 = models.IntegerField("SOULSHOT Level", default=0)
    g36 = models.IntegerField("VALOR Level", default=0)
    g37 = models.IntegerField("GUARDIAN Level", default=0)
    g38 = models.IntegerField("CONQUER Level", default=0)

    # Weapon and Skills
    weapon = models.CharField("Weapon", max_length=100, choices=WEAPON_CHOICES, blank=True)
    weapon_enchant = models.IntegerField("Weapon Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    unlocked_skills = models.JSONField("Unlocked Skills", default=list, blank=True)

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
    reason = models.CharField(max_length=255, default='Character update')
    total_score = models.FloatField()
    gear_stats_score = models.FloatField("Gear Stats Score", default=0)
    characteristics_score = models.FloatField("Characteristics Score", default=0)
    subclass_score = models.FloatField("Subclass Score", default=0)
    mainclass_score = models.FloatField("Mainclass Score", default=0)
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
        return f"GS Log {self.character.name}: {self.total_score} ({self.timestamp})"


# (GearScoreLog model omitted for brevity)

class CharacteristicsStats(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='characteristics_stats')

    # KELOMPOK A - CORE PVP DEFENSE
    a1 = models.IntegerField("PvP Melee Damage Reduction", default=0)
    a2 = models.IntegerField("PvP Ranged Damage Reduction", default=0)
    a3 = models.IntegerField("PvP Magic Damage Reduction", default=0)
    a4 = models.IntegerField("PvP Melee Evasion", default=0)
    a5 = models.IntegerField("PvP Ranged Evasion", default=0)
    a6 = models.IntegerField("PvP Magic Evasion", default=0)
    a7 = models.IntegerField("PvP Skill Defense (%)", default=0)
    a8 = models.IntegerField("PvP Weapon Defense (%)", default=0)
    a9 = models.IntegerField("PvP Melee Damage Resistance (%)", default=0)
    a10 = models.IntegerField("PvP Ranged Damage Resistance (%)", default=0)
    a11 = models.IntegerField("PvP Magic Damage Resistance (%)", default=0)
    a12 = models.IntegerField("PvP Critical Hit Resistance (%)", default=0)

    # KELOMPOK B - CORE PVP OFFENSE
    b1 = models.IntegerField("Extra PvP Melee Damage", default=0)
    b2 = models.IntegerField("Extra PvP Ranged Damage", default=0)
    b3 = models.IntegerField("Extra PvP Magic Damage", default=0)
    b4 = models.IntegerField("PvP Melee Accuracy", default=0)
    b5 = models.IntegerField("PvP Ranged Accuracy", default=0)
    b6 = models.IntegerField("PvP Magic Accuracy", default=0)
    b7 = models.IntegerField("PvP Critical Hit (%)", default=0)
    b8 = models.IntegerField("PvP Double Chance (%)", default=0)
    b9 = models.IntegerField("PvP Triple Chance (%)", default=0)

    # KELOMPOK C - CROWD CONTROL
    c1 = models.IntegerField("Stun Accuracy (%)", default=0)
    c2 = models.IntegerField("Stun Resistance (%)", default=0)
    c3 = models.IntegerField("Hold Accuracy (%)", default=0)
    c4 = models.IntegerField("Hold Resistance (%)", default=0)
    c5 = models.IntegerField("CC Accuracy (%)", default=0)
    c6 = models.IntegerField("CC Resistance (%)", default=0)
    c7 = models.IntegerField("CC Duration Reduction (%)", default=0)
    c8 = models.IntegerField("Increases CC Duration (%)", default=0)
    c9 = models.IntegerField("Extra Accuracy (to Stunned)", default=0)
    c10 = models.IntegerField("Ignore Extra Reduction (to Stunned)", default=0)
    c11 = models.IntegerField("Hold Defense", default=0)
    c12 = models.IntegerField("Stun Reduction", default=0)
    c13 = models.IntegerField("Stun Defense", default=0)
    c14 = models.IntegerField("Vex Accuracy (%)", default=0)
    c15 = models.IntegerField("Aggression Resistance (%)", default=0)
    c16 = models.IntegerField("Silence Accuracy (%)", default=0)
    c17 = models.IntegerField("Silence Resistance (%)", default=0)

    # KELOMPOK D - SURVIVAL
    d1 = models.IntegerField("Heal Boost (%)", default=0)
    d2 = models.IntegerField("Received Heal Increase (%)", default=0)
    d3 = models.IntegerField("Potion Recovery Rate (%)", default=0)
    d4 = models.IntegerField("Potion Recovery Amount", default=0)
    d5 = models.IntegerField("Fixed HP Recovery", default=0)
    d6 = models.IntegerField("Fixed MP Recovery", default=0)
    d7 = models.IntegerField("Ignore HP Recovery Penalty (%)", default=0)
    d8 = models.IntegerField("Ignore MP Recovery Penalty (%)", default=0)

    # KELOMPOK E - SECONDARY DEFENSE
    e1 = models.IntegerField("Critical Hit Reduction", default=0)
    e2 = models.IntegerField("Melee Critical Hit Resistance (%)", default=0)
    e3 = models.IntegerField("Ranged Critical Hit Resistance (%)", default=0)
    e4 = models.IntegerField("Magic Critical Hit Resistance (%)", default=0)
    e5 = models.IntegerField("Double Resistance (%)", default=0)
    e6 = models.IntegerField("Triple Resistance (%)", default=0)
    e7 = models.IntegerField("PvP Double Resistance (%)", default=0)
    e8 = models.IntegerField("PvP Triple Resistance (%)", default=0)
    e9 = models.IntegerField("Skill Double Resistance (%)", default=0)
    e10 = models.IntegerField("Skill Triple Resistance (%)", default=0)

    # KELOMPOK F - SECONDARY OFFENSE
    f1 = models.IntegerField("Block Penetration (%)", default=0)
    f2 = models.IntegerField("Ignore Damage Reduction", default=0)
    f3 = models.IntegerField("Extra Damage (on Critical Hit)", default=0)
    f4 = models.IntegerField("Soulshot Weapon Damage Boost (%)", default=0)
    f5 = models.IntegerField("Extra Soulshot Damage", default=0)
    f6 = models.IntegerField("Greater Soulshot Weapon Damage Boost (%)", default=0)
    f7 = models.IntegerField("Extra Greater Soulshot Damage", default=0)
    f8 = models.IntegerField("Double Chance (%)", default=0)
    f9 = models.IntegerField("Triple Chance (%)", default=0)
    f10 = models.IntegerField("Soulshot Accuracy", default=0)
    f11 = models.IntegerField("Soulshot Weapon Damage", default=0)
    f12 = models.IntegerField("Greater Soulshot Accuracy", default=0)
    f13 = models.IntegerField("Greater Soulshot Weapon Damage", default=0)

    def calculate_total_score(self):
        A = 2 * (self.a1 + self.a2 + self.a3 + self.a4 + self.a5 + self.a6) + 0.02 * (self.a7 + self.a8 + self.a9 + self.a10 + self.a11 + self.a12)
        B = 1.8 * (self.b1 + self.b2 + self.b3 + self.b4 + self.b5 + self.b6) + 0.018 * (self.b7 + self.b8 + self.b9)
        C = 0.015 * (self.c1 + self.c2 + self.c3 + self.c4 + self.c5 + self.c6 + self.c7 + self.c8 + self.c14 + self.c15 + self.c16 + self.c17) + 1.5 * (self.c9 + self.c10 + self.c11 + self.c12 + self.c13)
        D = 0.012 * (self.d1 + self.d2 + self.d3 + self.d7 + self.d8) + 1.2 * (self.d4 + self.d5 + self.d6)
        E = 1.0 * self.e1 + 0.01 * (self.e2 + self.e3 + self.e4 + self.e5 + self.e6 + self.e7 + self.e8 + self.e9 + self.e10)
        F = 0.01 * (self.f1 + self.f4 + self.f6 + self.f8 + self.f9) + 1.0 * (self.f2 + self.f3 + self.f5 + self.f7 + self.f10 + self.f11 + self.f12 + self.f13)
        return A + B + C + D + E + F

    def __str__(self):
        return f"Characteristics Stats for {self.character.name}"


# ======================================================
# ACTIVITY TRACKING MODELS
# ======================================================

class ActivityEvent(models.Model):
    """Model untuk menyimpan data event guild (Invasion, Boss Rush, Catacombs)"""
    EVENT_TYPE_CHOICES = (
        ('INVASION', 'Invasion'),
        ('BOSS_RUSH', 'Boss Rush'),
        ('CATACOMBS', 'Catacombs'),
        ('DIMENSIONAL_SIEGE', 'Dimensional Siege'),
        ('CUSTOM', 'Custom Event'),
    )

    event_id = models.CharField("Event ID", max_length=50, unique=True, blank=True, help_text="Unique ID dari Discord/System")
    name = models.CharField("Nama Event", max_length=100)
    event_type = models.CharField("Tipe Event", max_length=20, choices=EVENT_TYPE_CHOICES)
    date = models.DateTimeField("Waktu Event")
    is_completed = models.BooleanField("Selesai", default=False)
    is_win = models.BooleanField("Menang", default=False, help_text="Untuk Boss Rush & Catacombs")
    is_finalized = models.BooleanField("Finalized", default=False)
    bosses_killed = models.JSONField("Boss Terbunuh", default=dict, blank=True,
        help_text="Format: {'dragon_beast': true, 'carnifex': true, 'orfen': false}")
    custom_points = models.IntegerField("Custom Points", default=0, blank=True)

    # Boss-specific points
    carnifex_points = models.IntegerField("Carnifex Points", default=2)
    orfen_points = models.IntegerField("Orfen Points", default=2)
    dragon_beast_points = models.IntegerField("Dragon Beast Points", default=2)
    latana_points = models.IntegerField("Latana Points", default=2)
    kain_van_halter_points = models.IntegerField("Kain Van Halter Points", default=3)
    balthazar_points = models.IntegerField("Balthazar Points", default=3)
    core_points = models.IntegerField("Core Points", default=3)

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
        if not self.event_id:
            import uuid
            self.event_id = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_event_type_display()}) - {self.date.strftime('%Y-%m-%d')}"

    def calculate_max_points(self):
        """Hitung poin maksimal yang bisa didapat dari event ini"""
        if self.event_type == 'INVASION':
            base = 5
            boss_points = 0
            boss_point_map = {
                'carnifex': self.carnifex_points,
                'orfen': self.orfen_points,
                'dragon_beast': self.dragon_beast_points,
                'latana': self.latana_points,
                'kain_van_halter': self.kain_van_halter_points,
                'balthazar': self.balthazar_points,
                'core': self.core_points,
            }
            if self.bosses_killed:
                for boss, killed in self.bosses_killed.items():
                    if killed:
                        boss_points += boss_point_map.get(boss, 0)
            return base + boss_points
        elif self.event_type == 'BOSS_RUSH':
            return 10 if self.is_win else 5
        elif self.event_type == 'CATACOMBS':
            return 10 if self.is_win else 5
        elif self.event_type == 'DIMENSIONAL_SIEGE':
            return 15 if self.is_win else 8
        elif self.event_type == 'CUSTOM':
            return self.custom_points
        return 5


class PlayerActivity(models.Model):
    """Model untuk tracking partisipasi player di setiap event"""
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
    discord_user_id = models.CharField("Discord User ID", max_length=50, blank=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='ATTENDED')
    points_earned = models.IntegerField("Poin Didapat", default=0)
    checked_in_at = models.DateTimeField("Waktu Check-In", auto_now_add=True)
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
        if self.status == 'ATTENDED' and self.points_earned == 0:
            self.points_earned = self.event.calculate_max_points()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player.name} - {self.event.name} ({self.get_status_display()})"


class PrizePoolConfig(models.Model):
    """Configuration for Prize Pool calculation."""
    total_pool = models.IntegerField("Total Prize Pool", default=10000)
    elite_percentage = models.FloatField("Elite %", default=0.70)
    core_percentage = models.FloatField("Core %", default=0.20)
    active_percentage = models.FloatField("Active %", default=0.10)
    casual_percentage = models.FloatField("Casual %", default=0.00)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        total = self.elite_percentage + self.core_percentage + self.active_percentage + self.casual_percentage
        if abs(total - 1.0) > 0.01:
            pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Prize Pool Configuration"
        verbose_name_plural = "Prize Pool Configurations"

    def __str__(self):
        return f"Prize Pool: {self.total_pool}"


# ======================================================
# MONTHLY RECAPS FOR DKP SYSTEM
# ======================================================

class MonthlyReport(models.Model):
    """Model untuk menyimpan rekap bulanan per player"""
    TIER_CHOICES = (
        ('ELITE', '🏆 Elite'),
        ('CORE', '⚔️ Core'),
        ('ACTIVE', '🛡️ Active'),
        ('CASUAL', '🌱 Casual'),
    )

    player = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='monthly_reports', verbose_name="Karakter")
    month = models.DateField("Bulan", help_text="Tanggal bulan (hari=1)")
    total_events = models.IntegerField("Total Event", default=0)
    attended_events = models.IntegerField("Event Dihadiri", default=0)
    attendance_rate = models.FloatField("Attendance Rate", default=0.0)
    activity_score = models.IntegerField("Skor Aktivitas", default=0)
    consistency_bonus = models.IntegerField("Bonus Konsistensi", default=0)
    decay_penalty = models.IntegerField("Decay Penalty", default=0)
    total_score = models.IntegerField("Total Skor", default=0)
    tier = models.CharField("Tier", max_length=20, choices=TIER_CHOICES, default='CASUAL')
    is_qualified = models.BooleanField("Qualified untuk Reward", default=False)
    prize_amount = models.IntegerField("Jumlah Hadiah", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_tier(self):
        """Determine tier based on total score"""
        if self.attendance_rate >= 0.8 and self.total_score >= 80:
            return 'ELITE'
        elif self.attendance_rate >= 0.6 and self.total_score >= 50:
            return 'CORE'
        elif self.attendance_rate >= 0.3:
            return 'ACTIVE'
        return 'CASUAL'

    def calculate_consistency_bonus(self):
        """Calculate consistency bonus based on attendance rate"""
        if self.attendance_rate >= 0.9:
            return 20
        elif self.attendance_rate >= 0.8:
            return 15
        elif self.attendance_rate >= 0.7:
            return 10
        elif self.attendance_rate >= 0.5:
            return 5
        return 0

    def save(self, *args, **kwargs):
        self.tier = self.calculate_tier()
        self.consistency_bonus = self.calculate_consistency_bonus()
        self.total_score = self.activity_score + self.consistency_bonus - self.decay_penalty
        self.is_qualified = self.tier in ['ELITE', 'CORE', 'ACTIVE']
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player.name} - {self.month.strftime('%B %Y')} ({self.get_tier_display()})"

    class Meta:
        unique_together = ['month', 'player']
        ordering = ['-month', '-total_score']
        verbose_name = "Monthly Report"
        verbose_name_plural = "Monthly Reports"
