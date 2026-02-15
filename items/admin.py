from django.contrib import admin
from .models import Item, Character, SubclassStats, ActivityEvent, PlayerActivity, MonthlyReport
from django.contrib import messages
from django.utils import timezone
from django import forms

# ----------------------------------------------------
# 1. CUSTOM ADMIN FORM (Untuk memfilter Item berdasarkan slot)
# ----------------------------------------------------
class CharacterAdminForm(forms.ModelForm):
    """
    Menimpa field Foreign Key standar untuk hanya menampilkan Item 
    yang sesuai dengan tipe perlengkapan.
    """
    # SLOT UTAMA
    main_weapon = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Weapon'),
        required=False
    )
    helmet = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Helmet'),
        required=False
    )
    armor = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Armor'),
        required=False
    )
    gloves = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Gloves'),
        required=False
    )
    boots = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Boots'),
        required=False
    )
    
    # SLOT AKSESORIS (Diasumsikan item_type mereka adalah 'Accessory' atau sejenisnya)
    # Anda mungkin perlu menyesuaikan item_type di filter ini sesuai data Anda
    necklace = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Accessory'),
        required=False
    )
    ring_left = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Accessory'),
        required=False
    )
    ring_right = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Accessory'),
        required=False
    )
    earring_left = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Accessory'),
        required=False
    )
    earring_right = forms.ModelChoiceField(
        queryset=Item.objects.filter(item_type='Accessory'),
        required=False
    )
    
    class Meta:
        model = Character
        fields = '__all__'

# ----------------------------------------------------
# 2. CUSTOM ADMIN CLASS UNTUK CHARACTER
# ----------------------------------------------------
class CharacterAdmin(admin.ModelAdmin):
    form = CharacterAdminForm
    # Menambahkan calculate_gear_score ke daftar tampilan di Admin
    list_display = ('name', 'level', 'character_class', 'calculate_gear_score')
    list_filter = ('character_class', 'level')
    search_fields = ('name',)


# ----------------------------------------------------
# 3. ACTIVITY ADMIN CLASSES
# ----------------------------------------------------
class ActivityEventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'name', 'event_type', 'date', 'is_completed', 'is_finalized')
    list_filter = ('event_type', 'is_completed', 'is_finalized', 'date')
    search_fields = ('event_id', 'name')
    date_hierarchy = 'date'
    ordering = ['-date']


class PlayerActivityAdmin(admin.ModelAdmin):
    list_display = ('player', 'event', 'status', 'points_earned', 'is_verified', 'checked_in_at')
    list_filter = ('status', 'is_verified', 'event__event_type', 'event__date')
    list_editable = ('is_verified',)
    search_fields = ('player__name', 'event__name', 'discord_user_id')
    autocomplete_fields = ['player', 'event']
    ordering = ['-event__date']


class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('player', 'month', 'total_score', 'tier', 'is_qualified', 'prize_amount')
    list_filter = ('tier', 'is_qualified', 'month')
    search_fields = ('player__name',)
    ordering = ['-month', '-total_score']
    readonly_fields = ('tier', 'is_qualified')


# ----------------------------------------------------
# 4. PENDAFTARAN MODEL
# ----------------------------------------------------

# Pendaftaran model Item standar
admin.site.register(Item)

# Pendaftaran model Character dengan form kustom
admin.site.register(Character, CharacterAdmin) 

# Pendaftaran model pendukung untuk data kompleks
admin.site.register(SubclassStats)

# Pendaftaran model Activity
admin.site.register(ActivityEvent, ActivityEventAdmin)
admin.site.register(PlayerActivity, PlayerActivityAdmin)

# Register other models if needed
admin.site.register(MonthlyReport, MonthlyReportAdmin)