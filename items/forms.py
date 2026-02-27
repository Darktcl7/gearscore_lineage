from django import forms
# IMPOR MODEL BARU
from .models import Item, Character, SubclassStats, LegendaryClass, CharacterAttributes, CharacteristicsStats, LegendaryAgathion, LegendaryMount, MythicClass, InheritorBook, CLASS_CHOICES 
from django.forms import ModelForm
from django.db.models import Case, When, Value, IntegerField

# ----------------------------------------------------
# 1. FORM UNTUK MEMBUAT ITEM BARU (ItemForm)
# ----------------------------------------------------

class ItemForm(forms.ModelForm):
    """
    Formulir berdasarkan model Item.
    Memungkinkan pengguna memasukkan nama, tipe, dan statistik item.
    """
    class Meta:
        model = Item
        fields = ['name', 'item_type', 'icon_file', 'enchant_level', 'grade', 'slot', 'attack_power', 'defense_power']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'item_type': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', '--- Select Type ---'),
                ('Weapon', 'Weapon'),
                ('Helmet', 'Helmet'),
                ('Armor', 'Armor'),
                ('Gloves', 'Gloves'),
                ('Boots', 'Boots'),
                ('Accessory', 'Accessory'),
            ]),
            'icon_file': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Icon filename (e.g. Icon_WP_Sword_G3_001.png)'}),
            'enchant_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 30}),
            'grade': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', '--- Select Grade ---'),
                ('Common', 'Common'),
                ('Uncommon', 'Uncommon'),
                ('Rare', 'Rare'),
                ('Epic', 'Epic'),
                ('Legendary', 'Legendary'),
            ]),
            'slot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Main Hand, Head'}),
            'attack_power': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'defense_power': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

# ----------------------------------------------------
# 2. FORM UNTUK MEMBUAT/MENGEDIT KARAKTER (CharacterForm)
# ----------------------------------------------------

class CharacterForm(forms.ModelForm):
    """
    Formulir berdasarkan model Character.
    Ini akan mencakup semua slot perlengkapan (Foreign Key ke Item).
    """
    class Meta:
        model = Character
        # Masukkan SEMUA field yang bisa diubah pengguna
        fields = [
            'name', 'clan', 'level', 'character_class', 
            'mythic_classes',
            'legendary_classes', # Added this field
            'legendary_agathions',
            'legendary_mounts',
            'main_weapon', 'helmet', 'armor', 
            'gloves', 'boots', 'necklace', 
            'ring_left', 'ring_right', 
            'earring_left', 'earring_right'
        ]
        
        # Labels sesuai referensi
        labels = {
            'name': 'Your Nickname',
            'clan': 'Your Clan',
            'level': 'Your LvL',
            'character_class': 'Your Class',
            'mythic_classes': 'What Mythic classes do you have?',
            'legendary_classes': 'What legendary classes do you have?',
            'legendary_agathions': 'What legendary agathions do you have?',
            'legendary_mounts': 'What legendary mount do you have?',
            'main_weapon': 'Main Weapon',
            'helmet': 'Helmet',
            'armor': 'Armor',
            'gloves': 'Gloves',
            'boots': 'Boots',
            'necklace': 'Necklace',
            'ring_left': 'Ring (Left)',
            'ring_right': 'Ring (Right)',
            'earring_left': 'Earring (Left)',
            'earring_right': 'Earring (Right)',
        }
        
        # Optional: Menggunakan widget Select untuk class choice
        widgets = {
            'character_class': forms.Select(choices=CLASS_CHOICES),
            'mythic_classes': forms.CheckboxSelectMultiple,
            'legendary_classes': forms.CheckboxSelectMultiple, # Use checkboxes
            'legendary_agathions': forms.CheckboxSelectMultiple,
            'legendary_mounts': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        """
        Inisialisasi kustom untuk memfilter Item yang muncul di dropdown.
        Ini adalah versi frontend dari logika di items/admin.py.
        """
        super().__init__(*args, **kwargs)
        
        # Filter Dropdown Slot Utama
        self.fields['main_weapon'].queryset = Item.objects.filter(item_type='Weapon')
        self.fields['helmet'].queryset = Item.objects.filter(item_type='Helmet')
        self.fields['armor'].queryset = Item.objects.filter(item_type='Armor')
        self.fields['gloves'].queryset = Item.objects.filter(item_type='Gloves')
        self.fields['boots'].queryset = Item.objects.filter(item_type='Boots')
        
        # Filter Dropdown Aksesori
        self.fields['necklace'].queryset = Item.objects.filter(item_type='Accessory')
        self.fields['ring_left'].queryset = Item.objects.filter(item_type='Accessory')
        self.fields['ring_right'].queryset = Item.objects.filter(item_type='Accessory')
        self.fields['earring_left'].queryset = Item.objects.filter(item_type='Accessory')
        self.fields['earring_right'].queryset = Item.objects.filter(item_type='Accessory')

        # Order "No ..." items first for CheckboxSelectMultiple fields
        self.fields['mythic_classes'].queryset = MythicClass.objects.annotate(
            sort_order=Case(
                When(name="No mythic class", then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('sort_order', 'id')

        self.fields['legendary_classes'].queryset = LegendaryClass.objects.annotate(
            sort_order=Case(
                When(name="No legendary class", then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('sort_order', 'id')

        self.fields['legendary_agathions'].queryset = LegendaryAgathion.objects.annotate(
            sort_order=Case(
                When(name="No legendary agathions", then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('sort_order', 'id')

        self.fields['legendary_mounts'].queryset = LegendaryMount.objects.annotate(
            sort_order=Case(
                When(name="No legendary mount", then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('sort_order', 'id')

        # Tambahkan opsi '----' (None) di awal queryset yang di-filter
        for field_name, field in self.fields.items():
            field.required = False # MAKE EVERYTHING OPTIONAL SO IT DOES NOT BLOCK SAVE
            # Only apply to dropdowns (ModelChoiceField), and explicitly exclude legendary_classes and agathions
            if field_name not in ['mythic_classes', 'legendary_classes', 'legendary_agathions', 'legendary_mounts'] and isinstance(field, forms.ModelChoiceField):
                field.empty_label = "--- Pilih Item ---"

# ----------------------------------------------------
# 3. FORM UNTUK MENGEDIT SUBCLASS STATS
# ----------------------------------------------------

class SubclassStatsForm(ModelForm):
    """
    Formulir untuk mengedit statistik Subclass yang melekat pada satu karakter.
    Includes skills and weapons for 6 subclasses: Dualblade, Dagger, Staff, Bow, Tank, Spear.
    """
    class Meta:
        model = SubclassStats
        # Exclude character and JSON fields (handled manually in view)
        exclude = ['character', 'myth_skills', 'legend_skills', 'subclass_weapons']
        
        widgets = {
            # Dualblade skills
            'dualblade_triple_slash': forms.CheckboxInput(),
            'dualblade_sonic_blaster': forms.CheckboxInput(),
            'dualblade_detect_weakness': forms.CheckboxInput(),
            'dualblade_dance_of_fury': forms.CheckboxInput(),
            'dualblade_dual_parrying': forms.CheckboxInput(),
            'dualblade_dual_impact': forms.CheckboxInput(),
            'dualblade_berserker': forms.CheckboxInput(),
            'dualblade_breaking_armor': forms.CheckboxInput(),
            'dualblade_weapon': forms.RadioSelect(),
            # Dagger skills
            'dagger_assassin_vision': forms.CheckboxInput(),
            'dagger_shadow_blade': forms.CheckboxInput(),
            'dagger_hide': forms.CheckboxInput(),
            'dagger_venom': forms.CheckboxInput(),
            'dagger_reset_movement': forms.CheckboxInput(),
            'dagger_phantom_blade': forms.CheckboxInput(),
            'dagger_shadow_step': forms.CheckboxInput(),
            'dagger_marionette': forms.CheckboxInput(),
            'dagger_weapon': forms.RadioSelect(),
            # Staff skills
            'staff_snow_storm': forms.CheckboxInput(),
            'staff_cancellation': forms.CheckboxInput(),
            'staff_confuse': forms.CheckboxInput(),
            'staff_restore_casting': forms.CheckboxInput(),
            'staff_frozen_crystal': forms.CheckboxInput(),
            'staff_meteor': forms.CheckboxInput(),
            'staff_chaos': forms.CheckboxInput(),
            'staff_gravity': forms.CheckboxInput(),
            'staff_weapon': forms.RadioSelect(),
            # Bow skills
            'bow_death_sting': forms.CheckboxInput(),
            'bow_mana_seeker': forms.CheckboxInput(),
            'bow_real_target': forms.CheckboxInput(),
            'bow_entangle': forms.CheckboxInput(),
            'bow_impact_shot': forms.CheckboxInput(),
            'bow_absolute_piercing': forms.CheckboxInput(),
            'bow_elimination': forms.CheckboxInput(),
            'bow_pinpoint_shot': forms.CheckboxInput(),
            'bow_weapon': forms.RadioSelect(),
            # Tank skills
            'tank_double_shock': forms.CheckboxInput(),
            'tank_iron_will': forms.CheckboxInput(),
            'tank_vex': forms.CheckboxInput(),
            'tank_touch_of_life': forms.CheckboxInput(),
            'tank_holy_strike': forms.CheckboxInput(),
            'tank_brutal_attack': forms.CheckboxInput(),
            'tank_vengeance': forms.CheckboxInput(),
            'tank_chain_strike': forms.CheckboxInput(),
            'tank_weapon': forms.RadioSelect(),
            # Spear skills
            'spear_frenzy': forms.CheckboxInput(),
            'spear_vital_destruction': forms.CheckboxInput(),
            'spear_infinity_strike': forms.CheckboxInput(),
            'spear_disarm': forms.CheckboxInput(),
            'spear_giant_stomp': forms.CheckboxInput(),
            'spear_absolute_spear': forms.CheckboxInput(),
            'spear_rolling_thunder': forms.CheckboxInput(),
            'spear_earthquake_stomp': forms.CheckboxInput(),
            'spear_weapon': forms.RadioSelect(),
            # Greatsword skills
            'greatsword_crescendo_vitality': forms.CheckboxInput(),
            'greatsword_quake': forms.CheckboxInput(),
            'greatsword_reflect_stun': forms.CheckboxInput(),
            'greatsword_hellfire': forms.CheckboxInput(),
            'greatsword_bash': forms.CheckboxInput(),
            'greatsword_war_rage': forms.CheckboxInput(),
            'greatsword_guardian_shield': forms.CheckboxInput(),
            'greatsword_wave_sword': forms.CheckboxInput(),
            'greatsword_weapon': forms.RadioSelect(),
            # Crossbow skills
            'crossbow_heroic_change': forms.CheckboxInput(),
            'crossbow_feralize': forms.CheckboxInput(),
            'crossbow_chain_bolt': forms.CheckboxInput(),
            'crossbow_blackout_bolt': forms.CheckboxInput(),
            'crossbow_escape': forms.CheckboxInput(),
            'crossbow_back_tumbling': forms.CheckboxInput(),
            'crossbow_disciplin': forms.CheckboxInput(),
            'crossbow_vampiric_mind': forms.CheckboxInput(),
            'crossbow_weapon': forms.RadioSelect(),
            # Chainsword skills
            'chainsword_chain_galaxy': forms.CheckboxInput(),
            'chainsword_overflow': forms.CheckboxInput(),
            'chainsword_binding': forms.CheckboxInput(),
            'chainsword_bloody_sword': forms.CheckboxInput(),
            'chainsword_double_whip': forms.CheckboxInput(),
            'chainsword_rust': forms.CheckboxInput(),
            'chainsword_chain_chasing': forms.CheckboxInput(),
            'chainsword_bloody_slash': forms.CheckboxInput(),
            'chainsword_weapon': forms.RadioSelect(),
            # Rapier skills
            'rapier_feather_pool': forms.CheckboxInput(),
            'rapier_black_feather': forms.CheckboxInput(),
            'rapier_shooting_star': forms.CheckboxInput(),
            'rapier_sword_blossom': forms.CheckboxInput(),
            'rapier_sting': forms.CheckboxInput(),
            'rapier_traceless': forms.CheckboxInput(),
            'rapier_parrying_arrow': forms.CheckboxInput(),
            'rapier_summon_sword': forms.CheckboxInput(),
            'rapier_weapon': forms.RadioSelect(),
            # Magic Cannon skills
            'cannon_canon_night': forms.CheckboxInput(),
            'cannon_assemble': forms.CheckboxInput(),
            'cannon_slip': forms.CheckboxInput(),
            'cannon_canon_expansion': forms.CheckboxInput(),
            'cannon_barrier_shot': forms.CheckboxInput(),
            'cannon_blast_bomb': forms.CheckboxInput(),
            'cannon_enchant_aiming': forms.CheckboxInput(),
            'cannon_magic_trace': forms.CheckboxInput(),
            'cannon_weapon': forms.RadioSelect(),
            # Orb skills
            'orb_mess_hill': forms.CheckboxInput(),
            'orb_holy_light': forms.CheckboxInput(),
            'orb_last_hill': forms.CheckboxInput(),
            'orb_divine_execution': forms.CheckboxInput(),
            'orb_divine_spark': forms.CheckboxInput(),
            'orb_improved_orb': forms.CheckboxInput(),
            'orb_judgment': forms.CheckboxInput(),
            'orb_arcane_shield': forms.CheckboxInput(),
            'orb_weapon': forms.RadioSelect(),
            # Dual Axe skills
            'dualaxe_rage_strike': forms.CheckboxInput(),
            'dualaxe_power_crush': forms.CheckboxInput(),
            'dualaxe_whirlwind': forms.CheckboxInput(),
            'dualaxe_execute': forms.CheckboxInput(),
            'dualaxe_blood_rage': forms.CheckboxInput(),
            'dualaxe_armor_break': forms.CheckboxInput(),
            'dualaxe_cyclone': forms.CheckboxInput(),
            'dualaxe_berserk_fury': forms.CheckboxInput(),
            'dualaxe_weapon': forms.RadioSelect(),
            # Soul Breaker skills
            'soulbreaker_soul_strike': forms.CheckboxInput(),
            'soulbreaker_dark_blast': forms.CheckboxInput(),
            'soulbreaker_soul_drain': forms.CheckboxInput(),
            'soulbreaker_shadow_burst': forms.CheckboxInput(),
            'soulbreaker_void_slash': forms.CheckboxInput(),
            'soulbreaker_soul_shatter': forms.CheckboxInput(),
            'soulbreaker_dark_impulse': forms.CheckboxInput(),
            'soulbreaker_annihilation': forms.CheckboxInput(),
            'soulbreaker_weapon': forms.RadioSelect(),
        }

# ----------------------------------------------------
# 5. FORM FOR CHARACTER ATTRIBUTES
# ----------------------------------------------------

class CharacterAttributesForm(ModelForm):
    class Meta:
        model = CharacterAttributes
        exclude = ['character'] # Exclude the foreign key to the character
        
        # Labels sesuai referensi
        labels = {
            'inheritor_books': 'What are your Inheritor books?',
            'epic_classes_count': 'How many epic classes do you have?',
            'epic_agathions_count': 'How many epic agathions do you have?',
            'soulshot_level': 'What is your Soulshot level?',
            'valor_level': 'What is your Valor level?',
            'soul_prog_attack': 'What are your soul progression attack effects?',
            'soul_prog_defense': 'What are your soul progression defense effects?',
            'soul_prog_blessing': 'What are your soul progression blessings effects?',
            'enchant_bracelet_holy_prot': 'Enchant Bracelet of Holy Protection',
            'enchant_bracelet_influence': 'Enchant Bracelet of Influence',
            'enchant_earring_earth': "Enchant Earth Dragon's Earring",
            'enchant_earring_fire': "Enchant Fire Dragon's Earring",
            'enchant_seal_eva': "Enchant Eva's Seal",
            'pvp_helmet': 'PvP Helmet',
            'pvp_gloves': 'PvP Gloves',
            'pvp_boots': 'PvP Boots',
            'pvp_gaiters': 'PvP Gaiters',
            'pvp_top_armor': 'PvP Top Armor',
            'pvp_cloak': 'PvP Cloak',
            'pvp_tshirt': 'PvP T-Shirt',
            'pvp_sigil': 'PvP Sigil',
            'pvp_necklace': 'PvP Necklace',
            'pvp_ring_left': 'PvP Ring (Left)',
            'pvp_ring_right': 'PvP Ring (Right)',
            'pvp_belt': 'PvP Belt',
            'weapon': 'Weapon',
            'stat_dmg': 'DMG (Damage)',
            'stat_acc': 'ACC (Accuracy)',
            'stat_def': 'DEF (Defense)',
            'stat_reduc': 'REDUC (Damage Reduction)',
            'stat_resist': 'RESIST (Resistance)',
            'stat_skill_dmg_boost': 'Skill DMG Boost',
            'stat_wpn_dmg_boost': 'Weapon DMG Boost',
            'stat_guardian': 'Guardian',
            'stat_conquer': 'Conquer',
            'total_legend_codex': 'Total Legend Codex',
            'total_epic_mount': 'Total Epic Mount',
            'exp_one_handed_sword': 'One-Handed Sword Skill',
            'exp_dual_wield': 'Dual-Wield Skills',
            'exp_dagger': 'Dagger Skill',
            'exp_bow': 'Bow Skill',
            'exp_staff': 'Staff Skill',
            'exp_greatsword': 'Greatsword Skill',
            'exp_crossbow': 'Crossbow Skill',
            'exp_chainsword': 'Chainsword Skill',
            'exp_rapier': 'Rapier Skill',
            'exp_magic_cannon': 'Magic Cannon Skill',
            'exp_spear': 'Spear Skill',
            'exp_orb': 'Orb Skill',
            'exp_dual_axe': 'Dual Axe Skill',
            'exp_soul_breaker': 'Soul Breaker Skill',
            'aster_erafone': 'Aster (Erafone)',
        }
        
        widgets = {
            'inheritor_books': forms.CheckboxSelectMultiple,
            'epic_classes_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'epic_agathions_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'soulshot_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 13}),
            'valor_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 13}),
            'stat_guardian': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 13}),
            'stat_conquer': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 13}),
            'total_legend_codex': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'total_epic_mount': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'aster_erafone': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 30}),
            'unlocked_skills': forms.HiddenInput(attrs={'id': 'unlocked_skills_hidden'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make ALL fields optional to prevent "not focusable" errors and validation blockers
        for field_name in self.fields:
            self.fields[field_name].required = False
            
        if 'unlocked_skills' in self.fields:
            self.fields['unlocked_skills'].label = ''

# ----------------------------------------------------
# 6. FORM FOR DETAIL CHARACTERISTICS (100+ Fields)
# ----------------------------------------------------

class CharacteristicsStatsForm(ModelForm):
    class Meta:
        model = CharacteristicsStats
        exclude = ['character']
        
        # Use simple number inputs for all integer fields
        widgets = {
             field.name: forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'style': 'width: 100px; display: inline-block;'})
             for field in CharacteristicsStats._meta.fields if field.name != 'id' and field.name != 'character'
        }
