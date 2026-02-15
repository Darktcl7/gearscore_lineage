from django import forms
# IMPOR MODEL BARU
from .models import Item, Character, SubclassStats, LegendaryClass, CharacterAttributes, CharacteristicsStats, LegendaryAgathion, InheritorBook, CLASS_CHOICES 
from django.forms import ModelForm

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
            'legendary_classes', # Added this field
            'legendary_agathions',
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
            'legendary_classes': 'What legendary classes do you have?',
            'legendary_agathions': 'What legendary agathions do you have?',
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
            'legendary_classes': forms.CheckboxSelectMultiple, # Use checkboxes
            'legendary_agathions': forms.CheckboxSelectMultiple,
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

        # Tambahkan opsi '----' (None) di awal queryset yang di-filter
        for field_name, field in self.fields.items():
            # Only apply to dropdowns (ModelChoiceField), and explicitly exclude legendary_classes
            if field_name != 'legendary_classes' and isinstance(field, forms.ModelChoiceField):
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
        # Exclude only character field, show all other fields
        exclude = ['character']
        
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
            'pvp_sigil': 'PvP Sigil',
            'pvp_necklace': 'PvP Necklace',
            'pvp_ring_left': 'PvP Ring (Left)',
            'pvp_ring_right': 'PvP Ring (Right)',
            'pvp_belt': 'PvP Belt',
            'weapon': 'Weapon',
            'skill_frenzy': 'Frenzy',
            'skill_vital_destruction': 'Vital Destruction',
            'skill_infinity_strike': 'Infinity Strike',
            'skill_disarm': 'Disarm',
            'skill_giant_stomp': 'Giant Stomp',
            'skill_absolute_spear': 'Absolute Spear',
            'skill_rolling_thunder': 'Rolling Thunder',
            'skill_earthquake_stomp': 'Earthquake Stomp',
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly make these fields optional to prevent "not focusable" browser errors
        self.fields['soulshot_level'].required = False
        self.fields['valor_level'].required = False
        self.fields['stat_guardian'].required = False
        self.fields['stat_conquer'].required = False

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
