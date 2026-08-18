from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden, JsonResponse
from .models import Item, Character, SubclassStats, LegendaryClass, CharacterAttributes, CharacteristicsStats, LegendaryAgathion, LegendaryMount, MythicClass, InheritorBook, CLASS_CHOICES, CLASS_TO_WEAPON_TYPE, WEAPON_CHOICES, CLASS_SKILLS_DATA, EventCheckInProof, WarPointConfig, WarPointSubmission
import json
from .forms import ItemForm, CharacterForm, SubclassStatsForm, CharacterAttributesForm, CharacteristicsStatsForm

# Helper function to check if user is admin
def is_admin(user):
    """Super Admin only (staff/superuser)"""
    return user.is_staff or user.is_superuser

def is_sub_admin(user):
    """Check if user is in 'Sub Admin' group"""
    return user.groups.filter(name='Sub Admin').exists()

def is_any_admin(user):
    """Super Admin OR Sub Admin"""
    return is_admin(user) or is_sub_admin(user)

def check_event_admin(user):
    """Check if user is allowed to manage events (SuperAdmin or EventAdmin)"""
    if is_admin(user):
        return True
    try:
        return getattr(user, 'admin_role', None) and user.admin_role.is_event_admin
    except Exception:
        return False

# ======================================================
# CHARACTER VIEWS
# ======================================================

# FUNGSI: Daftar Semua Karakter (character_list) -> LANDING PAGE USER (Card View)
@login_required
def character_list(request):
    # Semua user (termasuk admin) hanya melihat karakter mereka sendiri di sini (Card View)
    # Optimized: select_related for OneToOne, prefetch for ManyToMany
    characters = Character.objects.filter(owner=request.user).select_related('attributes', 'subclass_stats', 'characteristics_stats').prefetch_related('mythic_classes', 'legendary_classes', 'legendary_skins', 'legendary_agathions', 'legendary_mounts')
    return render(request, 'items/character_list.html', {'characters': characters, 'is_admin': is_admin(request.user)})

# FUNGSI: Manajemen Karakter (Admin Only) -> Table View
@login_required
def character_management(request):
    if not is_any_admin(request.user):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    # Optimized: select_related for owner and attributes, prefetch for ManyToMany
    characters = Character.objects.all().select_related('owner', 'attributes', 'subclass_stats', 'characteristics_stats').prefetch_related('mythic_classes', 'legendary_classes', 'legendary_skins', 'owner__groups').order_by('name')
    # Get pending users (registered but not yet approved)
    from django.contrib.auth.models import User, Group
    pending_users = User.objects.filter(is_active=False, is_staff=False).order_by('-date_joined')
    
    # Users who are active but have no characters
    users_no_char = User.objects.filter(
        is_active=True, 
        is_staff=False, 
        is_superuser=False,
        characters__isnull=True
    ).order_by('-date_joined')
    
    # Get list of Sub Admin user IDs
    sub_admin_group = Group.objects.filter(name='Sub Admin').first()
    sub_admin_ids = list(sub_admin_group.user_set.values_list('id', flat=True)) if sub_admin_group else []
    
    # Get AdminRole data for role management (Treasury feature)
    from dkp.models import AdminRole
    import json
    admin_roles = {}
    for role in AdminRole.objects.select_related('user').all():
        admin_roles[role.user.pk] = {
            'is_dkp_admin': role.is_dkp_admin,
            'is_event_admin': role.is_event_admin,
            'is_raidboss_admin': role.is_raidboss_admin,
            'is_treasury_admin': role.is_treasury_admin,
            'is_auction_admin': role.is_auction_admin,
            'is_soul_admin': role.is_soul_admin,
            'is_powerrank_admin': role.is_powerrank_admin,
            'is_warpoint_admin': role.is_warpoint_admin,
            'can_give_dkp': role.can_give_dkp,
            'can_remove_dkp': role.can_remove_dkp,
            'can_decay_dkp': role.can_decay_dkp,
        }
    admin_roles_json = json.dumps(admin_roles)
    
    return render(request, 'items/character_management.html', {
        'characters': characters,
        'pending_users': pending_users,
        'users_no_char': users_no_char,
        'is_super_admin': is_admin(request.user),
        'sub_admin_ids': sub_admin_ids,
        'admin_roles_json': admin_roles_json,
    })

# FUNGSI: Halaman Profil Karakter (character_profile)
@login_required
def character_profile(request, pk):
    from django.core.cache import cache

    # Optimized: select_related for OneToOne relations to avoid N+1
    character = get_object_or_404(
        Character.objects.select_related('owner', 'attributes', 'subclass_stats', 'characteristics_stats')
        .prefetch_related('mythic_classes', 'legendary_classes', 'legendary_agathions', 'legendary_mounts'),
        pk=pk
    )

    # Permission check
    if not is_admin(request.user) and character.owner != request.user:
        return HttpResponseForbidden("You don't have permission to view this profile.")

    # Ensure CharacterAttributes exists
    CharacterAttributes.objects.get_or_create(character=character)

    # 1. Get gear score (already optimized with select_related above)
    gear_score = character.calculate_gear_score()

    # 2. Ranking - cached for 60 seconds to avoid recalculating on every page load
    cache_key = 'gearscore_rankings'
    rankings = cache.get(cache_key)
    if rankings is None:
        all_characters = Character.objects.select_related(
            'attributes', 'subclass_stats', 'characteristics_stats'
        ).all()
        char_scores = []
        for char in all_characters:
            score = char.calculate_gear_score()
            char_scores.append({'id': char.id, 'score': score.get('total_score', 0) if isinstance(score, dict) else score})
        char_scores.sort(key=lambda x: x['score'], reverse=True)
        rankings = {item['id']: idx + 1 for idx, item in enumerate(char_scores)}
        cache.set(cache_key, rankings, 60)  # Cache for 1 minute

    rank = rankings.get(character.id, "N/A")

    # Auto delete logs older than 30 days
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    character.gs_logs.filter(timestamp__lt=thirty_days_ago).delete()

    # Retrieve remaining logs (limit to 50 descending just in case)
    gs_logs = character.gs_logs.all().order_by('-timestamp')[:50]
    can_edit = is_admin(request.user) or character.owner == request.user

    context = {
        'character': character,
        'gear_score': gear_score,
        'rank': rank,
        'gs_logs': gs_logs,
        'is_admin': is_admin(request.user),
        'can_edit': can_edit,
    }
    return render(request, 'items/character_profile.html', context)


# FUNGSI BARU: Membuat atau Mengedit Karakter (create_character)
@login_required
def create_character(request, pk=None):

    character_instance = get_object_or_404(Character, pk=pk) if pk else None
    
    # Permission check: admin can edit any, user can only edit their own
    # Also allow editing if character has no owner (e.g., created by admin)
    if character_instance:
        if not is_admin(request.user):
            if character_instance.owner and character_instance.owner != request.user:
                return HttpResponseForbidden("You can only edit your own characters.")
            elif not character_instance.owner:
                pass  # Character has no owner, allow edit
    attributes_instance = CharacterAttributes.objects.get_or_create(character=character_instance)[0] if character_instance else None

    if request.method == 'POST':

        character_form = CharacterForm(request.POST, instance=character_instance)
        attributes_form = CharacterAttributesForm(request.POST, instance=attributes_instance)
        


        if character_form.is_valid() and attributes_form.is_valid():

            character = character_form.save(commit=False)
            # Set owner jika karakter baru
            if not character_instance:
                character.owner = request.user
            character.save()
            character_form.save_m2m()
            
            attributes = attributes_form.save(commit=False)
            attributes.character = character
            attributes.save()
            attributes_form.save_m2m()
            
            # Redirect ke profile karakter yang baru dibuat/diedit
            return redirect('character-profile', pk=character.pk)
    else:
        character_form = CharacterForm(instance=character_instance)
        attributes_form = CharacterAttributesForm(instance=attributes_instance)

    mythic_class_icons = {mc.name: mc.icon_file for mc in MythicClass.objects.all()}
    legendary_class_icons = {lc.name: lc.icon_file for lc in LegendaryClass.objects.all()}
    legendary_agathion_icons = {la.name: la.icon_file for la in LegendaryAgathion.objects.all()}
    legendary_mount_icons = {lm.name: lm.icon_file for lm in LegendaryMount.objects.all()}

    question_icons = {
        'soulshot_level': 's1.webm', 'valor_level': 's2.webm',
        'soul_prog_attack': 'Icon_SoulStone_Option_Icon_01.png', 'soul_prog_defense': 'Icon_SoulStone_Option_Icon_04.png',
        'soul_prog_blessing': 'Icon_SoulStone_Option_Icon_07.png', 'soul_prog_accuracy': 'soul_progression_accuracy-removebg-preview.png',
        'inheritor_books': 'Icon_Item_Usable_SkillBook_04.png',
        'enchant_bracelet_holy_prot': 'Icon_ACC_BMBracelet_G0_003.png', 'enchant_bracelet_influence': 'Icon_ACC_BMBracelet_G0_001.png',
        'enchant_earring_earth': 'Icon_ACC_BMEarring_G0_002.png', 'enchant_earring_fire': 'Icon_ACC_BMEarring_G0_001.png',
        'enchant_seal_eva': 'Icon_ACC_Seal_G0_001.png',
    }

    # Build weapon image mapping: weapon_value -> media image path
    weapon_images = {}
    for value, label in WEAPON_CHOICES:
        if '|' in value:
            weapon_type, weapon_name = value.split('|', 1)
            # Image path matches: items/weapons/<type>/<name>.png
            # Replace spaces for LiteSpeed compatibility
            safe_name = weapon_name.replace(' ', '_') if weapon_name == 'Talum Dual Sword' else weapon_name
            weapon_images[value] = f'items/weapons/{weapon_type}/{safe_name}.png'

    context = {
        'character_form': character_form,
        'attributes_form': attributes_form,
        'is_edit': character_instance is not None,
        'mythic_class_icons': mythic_class_icons,
        'legendary_class_icons': legendary_class_icons,
        'legendary_agathion_icons': legendary_agathion_icons,
        'legendary_mount_icons': legendary_mount_icons,
        'question_icons': question_icons,
        'class_to_weapon_type': json.dumps(CLASS_TO_WEAPON_TYPE),
        'weapon_images': json.dumps(weapon_images),
        'class_skills_data': json.dumps(CLASS_SKILLS_DATA),
    }
    return render(request, 'items/character_form.html', context)



# FUNGSI BARU: Menghapus Karakter (delete_character)
@login_required
def delete_character(request, pk):
    character = get_object_or_404(Character, pk=pk)
    
    # Permission check: admin can delete any, user can only delete their own
    if not is_admin(request.user) and character.owner != request.user:
        return HttpResponseForbidden("You can only delete your own characters.")
    
    if request.method == 'POST':
        character.delete()
        return redirect('character-list')
    
    context = {
        'character': character
    }
    return render(request, 'items/character_confirm_delete.html', context)


# ======================================================
# ITEM VIEWS (Admin only)
# ======================================================

# FUNGSI: Daftar Semua Item (item_list)
@login_required
def item_list(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can access items.")
    items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items})

# FUNGSI: Detail Item (item_detail)
@login_required
def item_detail(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can access items.")
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {'item': item})

# FUNGSI BARU: Membuat Item Baru (create_item)
@login_required
def create_item(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can create items.")
    
    # Get list of available icons
    import os
    from django.conf import settings
    icons_path = os.path.join(settings.BASE_DIR, 'items', 'static', 'items', 'images', 'choices')
    available_icons = []
    if os.path.exists(icons_path):
        available_icons = sorted([f for f in os.listdir(icons_path) if f.endswith(('.png', '.jpg', '.webp'))])
    
    if request.method == 'POST':
        # Proses form yang dikirim
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect ke daftar item setelah berhasil
            return redirect('item-list') 
    else:
        # Tampilkan form kosong
        form = ItemForm()
    
    context = {
        'form': form, 
        'title': 'Add New Item',
        'available_icons': available_icons,
    }
    return render(request, 'items/item_form.html', context)

# FUNGSI BARU: Mengedit Item
@login_required
def edit_item(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can edit items.")
    
    # Get list of available icons
    import os
    from django.conf import settings
    icons_path = os.path.join(settings.BASE_DIR, 'items', 'static', 'items', 'images', 'choices')
    available_icons = []
    if os.path.exists(icons_path):
        available_icons = sorted([f for f in os.listdir(icons_path) if f.endswith(('.png', '.jpg', '.webp'))])
    
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item-list')
    else:
        form = ItemForm(instance=item)
    
    context = {
        'form': form,
        'title': f'Edit {item.name}',
        'available_icons': available_icons,
    }
    return render(request, 'items/item_form.html', context)

# FUNGSI BARU: Menghapus Item
@login_required
def delete_item(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can delete items.")
    
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item-list')
    
    context = {
        'item': item
    }
    return render(request, 'items/item_confirm_delete.html', context)



# FUNGSI BARU: Mengedit Subclass Stats
@login_required
def edit_subclass_stats(request, character_pk):
    character = get_object_or_404(Character, pk=character_pk)
    
    # Permission check: admin can edit any, user can only edit their own
    if not is_admin(request.user) and character.owner != request.user:
        return HttpResponseForbidden("You can only edit your own characters.")
    
    # Dapatkan atau buat objek SubclassStats yang terikat pada karakter ini
    stats, created = SubclassStats.objects.get_or_create(character=character)
    
    if request.method == 'POST':
        form = SubclassStatsForm(request.POST, instance=stats)
        if form.is_valid():
            obj = form.save(commit=False)
            # Parse myth skills JSON from hidden input
            myth_raw = request.POST.get('myth_skills_json', '{}')
            legend_raw = request.POST.get('legend_skills_json', '{}')
            weapons_raw = request.POST.get('subclass_weapons_json', '{}')
            try:
                obj.myth_skills = json.loads(myth_raw)
            except (json.JSONDecodeError, TypeError):
                obj.myth_skills = {}
            try:
                obj.legend_skills = json.loads(legend_raw)
            except (json.JSONDecodeError, TypeError):
                obj.legend_skills = {}
            try:
                obj.subclass_weapons = json.loads(weapons_raw)
            except (json.JSONDecodeError, TypeError):
                obj.subclass_weapons = {}
            obj.save()
            return redirect('character-profile', pk=character_pk)
    else:
        form = SubclassStatsForm(instance=stats)
        
    # Build weapon data by type for subclass use
    weapons_by_type = {}
    for value, label in WEAPON_CHOICES:
        if '|' in value:
            weapon_type, weapon_name = value.split('|', 1)
            if weapon_type not in weapons_by_type:
                weapons_by_type[weapon_type] = []
            weapons_by_type[weapon_type].append({'value': value, 'label': label})

    # Build reverse map: subclass prefix -> weapon type
    subclass_to_weapon_type = {
        'tank': 'one_handed_sword',
        'dualblade': 'two_sword_style',
        'dagger': 'dagger',
        'bow': 'bow',
        'staff': 'cane',
        'spear': 'spear',
        'greatsword': 'greatsword',
        'crossbow': 'crossbow',
        'chainsword': 'chainsword',
        'rapier': 'rapier',
        'cannon': 'magic_cannon',
        'orb': 'orb',
        'dualaxe': 'double_axe',
        'soulbreaker': 'soul_breaker',
    }

    # Map class name to subclass prefix for hiding
    class_to_prefix = {
        'One-Handed Sword Skill': 'tank',
        'Dual-Wield Skills': 'dualblade',
        'Dagger Skill': 'dagger',
        'Bow Skill': 'bow',
        'Staff Skill': 'staff',
        'Spear Skill': 'spear',
        'Greatsword Skill': 'greatsword',
        'Crossbow Skill': 'crossbow',
        'Chainsword Skill': 'chainsword',
        'Rapier Skill': 'rapier',
        'Magic Cannon Skill': 'cannon',
        'Orb Skill': 'orb',
        'Dual Axe Skill': 'dualaxe',
        'Soul Breaker Skill': 'soulbreaker',
    }

    context = {
        'form': form,
        'character': character,
        'title': f'Subclass Information for {character.name}',
        'form_description': 'Fill out information about your subclass skills and weapons.',
        'main_class': character.character_class,
        'main_class_prefix': class_to_prefix.get(character.character_class, ''),
        'class_skills_data': json.dumps(CLASS_SKILLS_DATA),
        'weapons_by_type': json.dumps(weapons_by_type),
        'subclass_to_weapon_type': json.dumps(subclass_to_weapon_type),
        'current_myth_skills': json.dumps(stats.myth_skills or {}),
        'current_legend_skills': json.dumps(stats.legend_skills or {}),
        'current_subclass_weapons': json.dumps(stats.subclass_weapons or {}),
    }
    return render(request, 'items/subclass_form.html', context)

# FUNGSI BARU: Mengedit Characteristics Stats (100+ Fields)
@login_required
def edit_characteristics_stats(request, character_pk):
    character = get_object_or_404(Character, pk=character_pk)
    
    if not is_admin(request.user) and character.owner != request.user:
        return HttpResponseForbidden("You can only edit your own characters.")
    
    stats, created = CharacteristicsStats.objects.get_or_create(character=character)
    
    if request.method == 'POST':
        form = CharacteristicsStatsForm(request.POST, instance=stats)
        if form.is_valid():
            form.save()
            return redirect('character-profile', pk=character_pk)
    else:
        form = CharacteristicsStatsForm(instance=stats)
        
    # Group fields for rendering
    field_groups = [
        ('KELOMPOK A - CORE PVP DEFENSE (Bobot: 2.0)', [form[f'a{i}'] for i in range(1, 13)]),
        ('KELOMPOK B - CORE PVP OFFENSE (Bobot: 1.8)', [form[f'b{i}'] for i in range(1, 10)]),
        ('KELOMPOK C - CROWD CONTROL (Bobot: 1.5)', [form[f'c{i}'] for i in range(1, 18)]),
        ('KELOMPOK D - SURVIVAL (Bobot: 1.2)', [form[f'd{i}'] for i in range(1, 9)]),
        ('KELOMPOK E - SECONDARY DEFENSE (Bobot: 1.0)', [form[f'e{i}'] for i in range(1, 11)]),
        ('KELOMPOK F - SECONDARY OFFENSE (Bobot: 1.0)', [form[f'f{i}'] for i in range(1, 14)]),
    ]
        
    context = {
        'form': form,
        'field_groups': field_groups,
        'character': character,
        'title': f'Edit Characteristics for {character.name}',
        'form_description': 'Detailed breakdown of all combat statistics.'
    }
    return render(request, 'items/characteristics_form.html', context)


# ======================================================
# ACTIVITY VIEWS
# ======================================================
from .models import ActivityEvent, PlayerActivity, MonthlyReport
from django.db.models import Sum, Q, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def gearscore_leaderboard(request):
    """
    Halaman Leaderboard khusus Gear Score - cached for performance
    """
    from django.core.cache import cache

    cache_key = 'gearscore_leaderboard_data'
    char_scores = cache.get(cache_key)

    if char_scores is None:
        all_characters = Character.objects.select_related(
            'owner', 'attributes', 'subclass_stats', 'characteristics_stats'
        ).all()
        char_scores = []
        for char in all_characters:
            score = char.calculate_gear_score()
            char_scores.append({
                'character': char,
                'score': score
            })
        char_scores.sort(key=lambda x: (
            x['score'].get('total_score', 0) if isinstance(x['score'], dict) else x['score']
        ), reverse=True)
        for index, item in enumerate(char_scores):
            item['rank'] = index + 1
        cache.set(cache_key, char_scores, 60)  # Cache 1 minute

    context = {
        'leaderboard': char_scores,
        'is_admin': is_admin(request.user),
    }
    return render(request, 'items/gearscore_leaderboard.html', context)

@login_required
def activity_leaderboard(request):
    """
    Halaman Activity Leaderboard - Monthly & Weekly Rankings + Guild Stats
    """
    today = timezone.now()
    
    # ── CLAN FILTER ──
    selected_clan = request.GET.get('clan', 'Valkyrie')
    clan_choices = ['Valkyrie', 'Valhalla']
    
    from .models import LeaderboardConfig
    lb_config = LeaderboardConfig.get_config()

    # Raid Boss CUSTOM events have boss type prefix in their name
    _raid_boss_name_q = (
        Q(event__name__contains='[Raid Boss]') |
        Q(event__name__contains='[Territory Boss]') |
        Q(event__name__contains='[World Boss]') |
        Q(event__name__contains='[Rift Boss]') |
        Q(event__name__contains='[Arena Boss]') |
        Q(event__name__contains='War Day:')
    )
    # Event Points = everything EXCEPT raid-boss CUSTOM events and AP adjustments
    tier_event_filter = (
        ~Q(event__event_type='CUSTOM') |
        Q(event__name__startswith='Score Adjustment:') |
        (Q(event__event_type='CUSTOM') & ~_raid_boss_name_q & ~Q(event__name__startswith='Score Adjustment:') & ~Q(event__name__startswith='AP Adjustment:'))
    )
    # Raid Boss Points = only CUSTOM events WITH raid boss prefix
    tier_raid_filter = Q(event__event_type='CUSTOM') & _raid_boss_name_q & ~Q(event__name__startswith='AP Adjustment:')
    
    # ── MONTHLY RANKING ──
    # Total Score = event points only (EXCLUDE AP adjustments)
    monthly_qs = PlayerActivity.objects.filter(event__is_completed=True)
    if lb_config.monthly_reset_at:
        monthly_qs = monthly_qs.filter(event__date__gte=lb_config.monthly_reset_at)
    monthly_qs = monthly_qs.exclude(event__name__startswith='AP Adjustment:')
    
    if selected_clan == 'Valkyrie':
        monthly_qs = monthly_qs.filter(Q(player__clan='Valkyrie') | Q(player__clan='') | Q(player__clan__isnull=True))
    else:
        monthly_qs = monthly_qs.filter(player__clan=selected_clan)
    
    monthly_data = (
        monthly_qs
        .values('player__id', 'player__name')
        .annotate(
            event_points=Coalesce(Sum('points_earned', filter=tier_event_filter), Value(0)) + Coalesce(Sum('win_streak_bonus', filter=tier_event_filter), Value(0)),
            raid_boss_points=Coalesce(Sum('points_earned', filter=tier_raid_filter), Value(0)) + Coalesce(Sum('win_streak_bonus', filter=tier_raid_filter), Value(0)),
            total_score=Coalesce(Sum('points_earned'), Value(0)) + Coalesce(Sum('win_streak_bonus'), Value(0)),
        )
        .order_by('-total_score')
    )
    
    monthly_ranking = []
    for i, entry in enumerate(monthly_data, 1):
        score = entry['total_score'] or 0
        event_points = entry['event_points'] or 0
        raid_boss_points = entry['raid_boss_points'] or 0
        tier = _get_tier(event_points, raid_boss_points)
        
        # Calculate AP adjustments separately
        ap_qs = PlayerActivity.objects.filter(
            player__id=entry['player__id'],
            event__name__startswith='AP Adjustment:'
        )
        if lb_config.monthly_reset_at:
            ap_qs = ap_qs.filter(event__date__gte=lb_config.monthly_reset_at)
        
        ap_points = ap_qs.aggregate(total=Sum('points_earned'))['total'] or 0
        
        monthly_ranking.append({
            'rank': i,
            'id': entry['player__id'],
            'name': entry['player__name'],
            'total_score': score,
            'event_points': event_points,
            'raid_boss_points': raid_boss_points,
            'ap_points': ap_points,
            'tier': tier,
            'tier_class': tier.lower().replace(' ', '_'),
        })
    
    # ── WEEKLY RANKING ──
    weekly_qs = PlayerActivity.objects.filter(event__is_completed=True)
    weekly_cutoff = None
    if lb_config.weekly_reset_at:
        weekly_cutoff = lb_config.weekly_reset_at
        weekly_qs = weekly_qs.filter(event__date__gte=weekly_cutoff)
    weekly_qs = weekly_qs.exclude(event__name__startswith='AP Adjustment:')
    
    if selected_clan == 'Valkyrie':
        weekly_qs = weekly_qs.filter(Q(player__clan='Valkyrie') | Q(player__clan='') | Q(player__clan__isnull=True))
    else:
        weekly_qs = weekly_qs.filter(player__clan=selected_clan)
    
    weekly_data = (
        weekly_qs
        .values('player__id', 'player__name')
        .annotate(
            event_points=Coalesce(Sum('points_earned', filter=tier_event_filter), Value(0)) + Coalesce(Sum('win_streak_bonus', filter=tier_event_filter), Value(0)),
            raid_boss_points=Coalesce(Sum('points_earned', filter=tier_raid_filter), Value(0)) + Coalesce(Sum('win_streak_bonus', filter=tier_raid_filter), Value(0)),
            total_score=Coalesce(Sum('points_earned'), Value(0)) + Coalesce(Sum('win_streak_bonus'), Value(0)),
        )
        .order_by('-total_score')
    )
    
    weekly_ranking = []
    for i, entry in enumerate(weekly_data, 1):
        score = entry['total_score'] or 0
        event_points = entry['event_points'] or 0
        raid_boss_points = entry['raid_boss_points'] or 0
        tier = _get_tier(event_points, raid_boss_points)
        
        ap_weekly_qs = PlayerActivity.objects.filter(
            player__id=entry['player__id'],
            event__name__startswith='AP Adjustment:'
        )
        if weekly_cutoff:
            ap_weekly_qs = ap_weekly_qs.filter(event__date__gte=weekly_cutoff)
            
        ap_points = ap_weekly_qs.aggregate(total=Sum('points_earned'))['total'] or 0
        
        weekly_ranking.append({
            'rank': i,
            'id': entry['player__id'],
            'name': entry['player__name'],
            'total_score': score,
            'event_points': event_points,
            'raid_boss_points': raid_boss_points,
            'ap_points': ap_points,
            'tier': tier,
            'tier_class': tier.lower().replace(' ', '_'),
        })
    # Apply tier rules in ranking order with slot caps.
    w_core_count = 0
    w_elite_count = 0
    w_active_count = 0
    
    for r in weekly_ranking:
        if r['event_points'] >= lb_config.core_event_points and r['raid_boss_points'] >= lb_config.core_raid_points and w_core_count < lb_config.core_max_slots:
            r['tier'] = 'Core'
            r['tier_class'] = 'core'
            w_core_count += 1
        elif r['event_points'] >= lb_config.elite_event_points and (lb_config.elite_raid_points == 0 or r['raid_boss_points'] >= lb_config.elite_raid_points) and w_elite_count < lb_config.elite_max_slots:
            r['tier'] = 'Elite'
            r['tier_class'] = 'elite'
            w_elite_count += 1
        elif r['event_points'] >= lb_config.active_event_points and r['raid_boss_points'] >= lb_config.active_raid_points and w_active_count < lb_config.active_max_slots:
            r['tier'] = 'Active'
            r['tier_class'] = 'active'
            w_active_count += 1
        else:
            r['tier'] = 'Inactive'
            r['tier_class'] = 'inactive'

    weekly_guild_stats = {
        'core': sum(1 for r in weekly_ranking if r['tier'] == 'Core'),
        'elite': sum(1 for r in weekly_ranking if r['tier'] == 'Elite'),
        'active': sum(1 for r in weekly_ranking if r['tier'] == 'Active'),
        'inactive': sum(1 for r in weekly_ranking if r['tier'] == 'Inactive'),
        'total': len(weekly_ranking),
    }
    # ── GUILD STATISTICS (slot-based tiers) ──
    # Core: event >= 2050 + raid >= 300, max 15 | Elite: event >= 2050, max 15 | Active: event >= 1200 + raid >= 300, max 20 | Inactive: rest
    core_count = 0
    elite_count = 0
    active_count = 0
    for r in monthly_ranking:
        if r['event_points'] >= lb_config.core_event_points and r['raid_boss_points'] >= lb_config.core_raid_points and core_count < lb_config.core_max_slots:
            r['tier'] = 'Core'
            r['tier_class'] = 'core'
            core_count += 1
        elif r['event_points'] >= lb_config.elite_event_points and (lb_config.elite_raid_points == 0 or r['raid_boss_points'] >= lb_config.elite_raid_points) and elite_count < lb_config.elite_max_slots:
            r['tier'] = 'Elite'
            r['tier_class'] = 'elite'
            elite_count += 1
        elif r['event_points'] >= lb_config.active_event_points and r['raid_boss_points'] >= lb_config.active_raid_points and active_count < lb_config.active_max_slots:
            r['tier'] = 'Active'
            r['tier_class'] = 'active'
            active_count += 1
        else:
            r['tier'] = 'Inactive'
            r['tier_class'] = 'inactive'
    
    guild_stats = {
        'core': sum(1 for r in monthly_ranking if r['tier'] == 'Core'),
        'elite': sum(1 for r in monthly_ranking if r['tier'] == 'Elite'),
        'active': sum(1 for r in monthly_ranking if r['tier'] == 'Active'),
        'inactive': sum(1 for r in monthly_ranking if r['tier'] == 'Inactive'),
        'total': len(monthly_ranking),
    }
    
    # ── RECENT EVENTS ──
    recent_events_query = ActivityEvent.objects.filter(date__lte=today).exclude(
        name__startswith='AP Adjustment:'
    ).exclude(
        name__startswith='Score Adjustment:'
    ).order_by('-date')
    
    from django.core.paginator import Paginator
    paginator = Paginator(recent_events_query, 20)
    page_number = request.GET.get('page')
    recent_events = paginator.get_page(page_number)
    
    context = {
        'monthly_ranking': monthly_ranking,
        'weekly_ranking': weekly_ranking,
        'guild_stats': guild_stats,
        'weekly_guild_stats': weekly_guild_stats,
        'recent_events': recent_events,
        'tier_config': lb_config,
        'current_month': today.strftime('%B %Y'),
        'current_week': f"01 {today.strftime('%b')} - {__import__('calendar').monthrange(today.year, today.month)[1]} {today.strftime('%b %Y')}",
        'is_admin': is_admin(request.user),
        'selected_clan': selected_clan,
        'clan_choices': clan_choices,
    }
    return render(request, 'items/activity_leaderboard.html', context)


def _get_tier(event_points, raid_boss_points=0, config=None):
    """Get tier from separate event and raid boss point requirements."""
    if config is None:
        from .models import LeaderboardConfig
        config = LeaderboardConfig.get_config()
    if event_points >= config.core_event_points and raid_boss_points >= config.core_raid_points:
        return 'Core'
    elif event_points >= config.elite_event_points and (config.elite_raid_points == 0 or raid_boss_points >= config.elite_raid_points):
        return 'Elite'
    elif event_points >= config.active_event_points and raid_boss_points >= config.active_raid_points:
        return 'Active'
    else:
        return 'Inactive'


@login_required
def save_tier_config(request):
    """Save tier configuration settings."""
    if not is_admin(request.user):
        return HttpResponseForbidden("Unauthorized")
    
    if request.method == 'POST':
        from .models import LeaderboardConfig
        config = LeaderboardConfig.get_config()
        
        try:
            config.core_event_points = int(request.POST.get('core_event_points', 2050))
            config.core_raid_points = int(request.POST.get('core_raid_points', 300))
            config.core_max_slots = int(request.POST.get('core_max_slots', 15))
            
            config.elite_event_points = int(request.POST.get('elite_event_points', 2050))
            config.elite_raid_points = int(request.POST.get('elite_raid_points', 0))
            config.elite_max_slots = int(request.POST.get('elite_max_slots', 15))
            
            config.active_event_points = int(request.POST.get('active_event_points', 1200))
            config.active_raid_points = int(request.POST.get('active_raid_points', 300))
            config.active_max_slots = int(request.POST.get('active_max_slots', 20))
            
            config.save()
        except (ValueError, TypeError):
            pass
    
    return redirect('activity-leaderboard')


@login_required
def update_prize_config(request):
    """
    API View to update prize configuration.
    Called via Ajax from Leaderboard page.
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Unauthorized")
    
    if request.method == 'POST':
        try:
            total_pool_val = int(request.POST.get('total_pool', 10000))
            elite = float(request.POST.get('elite', 0))
            core = float(request.POST.get('core', 0)) 
            casual = float(request.POST.get('casual', 0))
            
            # Basic validation
            total = elite + core + casual
            if total != 100:
                 pass 
                 
            # Convert to 0.70 format
            from .models import PrizePoolConfig
            config = PrizePoolConfig.objects.create(
                total_pool=total_pool_val,
                elite_percentage=elite/100.0,
                core_percentage=core/100.0,
                casual_percentage=casual/100.0,
                updated_by=request.user.username
            )
            
            # Recalculate current month's prizes immediately?
            from .services import calculate_prize_distribution
            today = timezone.now()
            calculate_prize_distribution(today.year, today.month)
            
            return redirect('activity-leaderboard')
            
        except ValueError:
            pass # Invalid numbers
            
    return redirect('activity-leaderboard')


@login_required
@require_http_methods(["POST"])
def adjust_ap(request):
    """
    Adjust Activity Points for a user (Give/Remove AP)
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Unauthorized")
        
    player_id = request.POST.get('player_id')
    points = int(request.POST.get('points', 0))
    action = request.POST.get('action') # 'give' or 'remove'
    reason = request.POST.get('reason', 'Manual Adjustment')
    
    if action == 'remove':
        points = -abs(points)
    else:
        points = abs(points)
        
    if points != 0:
        player = get_object_or_404(Character, id=player_id)
        
        event = ActivityEvent.objects.create(
            name=f"AP Adjustment: {reason}",
            event_type='CUSTOM',
            date=timezone.now(),
            max_points=abs(points),
            base_points=abs(points),
            is_completed=True,
            input_by=request.user,
        )
        
        PlayerActivity.objects.create(
            player=player,
            event=event,
            status='ATTENDED' if points > 0 else 'ABSENT',
            points_earned=points,
        )
        
        from .services import calculate_monthly_reports
        calculate_monthly_reports(event.date.year, event.date.month)
        
        from django.contrib import messages
        messages.success(request, f"Successfully {'gave' if points > 0 else 'removed'} {abs(points)} AP for {player.name}")
        
    return redirect(request.META.get('HTTP_REFERER', 'activity-leaderboard'))


@login_required
@require_http_methods(["POST"])
def adjust_score(request):
    """
    Admin can manually adjust a player's Total Score (add/subtract event points).
    This creates a hidden CUSTOM event that goes into the main score calculation.
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Unauthorized")
        
    player_id = request.POST.get('player_id')
    points = int(request.POST.get('points', 0))
    action = request.POST.get('action')  # 'add' or 'subtract'
    reason = request.POST.get('reason', 'Score Adjustment')
    
    if action == 'subtract':
        points = -abs(points)
    else:
        points = abs(points)
        
    if points != 0:
        player = get_object_or_404(Character, id=player_id)
        
        event = ActivityEvent.objects.create(
            name=f"Score Adjustment: {reason}",
            event_type='CUSTOM',
            date=timezone.now(),
            max_points=abs(points),
            base_points=abs(points),
            is_completed=True,
            input_by=request.user,
        )
        
        PlayerActivity.objects.create(
            player=player,
            event=event,
            status='ATTENDED' if points > 0 else 'ABSENT',
            points_earned=points,
        )
        
        from django.contrib import messages
        messages.success(request, f"Successfully {'added' if points > 0 else 'subtracted'} {abs(points)} score for {player.name}")
        
    return redirect(request.META.get('HTTP_REFERER', 'activity-leaderboard'))


@login_required
def reset_leaderboard_data(request):
    """
    Admin action to wipe Leaderboard data (Weekly, Monthly, or All).
    Weekly reset: only resets weekly ranking display (data preserved for monthly).
    Monthly/All reset: actually deletes data.
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Unauthorized")
        
    if request.method == 'POST':
        reset_type = request.POST.get('type', 'all')
        
        # We subtract 1 minute and strip seconds to ensure that any events created
        # immediately after resetting (which default to the current minute without seconds)
        # are safely evaluated as being >= the reset timestamp.
        from datetime import timedelta
        reset_timestamp = timezone.now().replace(second=0, microsecond=0) - timedelta(minutes=1)
        
        if reset_type == 'weekly':
            # Weekly reset: only update the reset timestamp
            # Data is NOT deleted, so monthly totals stay intact
            from .models import LeaderboardConfig
            config = LeaderboardConfig.get_config()
            config.weekly_reset_at = reset_timestamp
            config.save()
        elif reset_type == 'monthly':
            # Monthly reset: only update the monthly reset timestamp
            from .models import LeaderboardConfig
            config = LeaderboardConfig.get_config()
            config.monthly_reset_at = reset_timestamp
            config.save()
        else:
            PlayerActivity.objects.all().delete()
            ActivityEvent.objects.all().delete()
            
        return redirect('activity-leaderboard')
        
    return redirect('activity-leaderboard')


@login_required
def admin_adjust_score(request):
    """
    Admin can manually adjust a player's score.
    POST: report_id, adjustment (integer, can be negative)
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Unauthorized")
    
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            report_id = data.get('report_id')
            new_adjustment = int(data.get('adjustment', 0))
            
            report = MonthlyReport.objects.get(pk=report_id)
            report.score_adjustment = new_adjustment
            report.save()  # This triggers recalculation of total_score
            
            from django.http import JsonResponse
            return JsonResponse({
                'success': True,
                'total_score': report.total_score,
                'score_adjustment': report.score_adjustment,
            })
        except MonthlyReport.DoesNotExist:
            from django.http import JsonResponse
            return JsonResponse({'error': 'Report not found'}, status=404)
        except (ValueError, TypeError) as e:
            from django.http import JsonResponse
            return JsonResponse({'error': str(e)}, status=400)
    
    from django.http import JsonResponse
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required
def my_activity(request, character_pk=None):
    """
    Halaman detail aktivitas user sendiri, atau admin melihat member lain
    """
    # If character_pk is provided, super admin can view any member
    if character_pk:
        if not is_admin(request.user):
            return HttpResponseForbidden("Only super administrators can view other members' activity.")
        character = get_object_or_404(Character, pk=character_pk)
        viewing_other = True
    else:
        # Get current user's characters
        user_characters = Character.objects.filter(owner=request.user)
        
        if not user_characters.exists():
            return render(request, 'items/my_activity.html', {
                'no_character': True,
                'is_admin': is_admin(request.user),
            })
        
        character = user_characters.first()
        viewing_other = False
    
    # Get current month stats
    today = timezone.now()
    current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    monthly_report = MonthlyReport.objects.filter(
        player=character,
        month__year=today.year,
        month__month=today.month
    ).first()
    
    from .models import LeaderboardConfig
    lb_config = LeaderboardConfig.get_config()
    
    # Get activity history since the last weekly reset (to match leaderboard)
    # If no reset point, default to last 7 days
    start_date = lb_config.weekly_reset_at or (today - timedelta(days=7))
    
    activities = PlayerActivity.objects.filter(
        player=character,
        event__date__gte=start_date,
        event__is_completed=True
    ).select_related('event').order_by('-event__date')
    
    # Calculate quick stats
    total_points_base = activities.exclude(
        event__name__startswith='AP Adjustment:'
    ).aggregate(total=Sum('points_earned'))['total'] or 0
    
    total_streak_bonus = activities.exclude(
        event__name__startswith='AP Adjustment:'
    ).aggregate(total=Sum('win_streak_bonus'))['total'] or 0
    
    total_points = total_points_base + total_streak_bonus

    # Raid boss CUSTOM events have boss type prefix
    from django.db.models import Q as Qmy
    _rb_q = (
        Qmy(event__name__contains='[Raid Boss]') |
        Qmy(event__name__contains='[Territory Boss]') |
        Qmy(event__name__contains='[World Boss]') |
        Qmy(event__name__contains='[Rift Boss]') |
        Qmy(event__name__contains='[Arena Boss]') |
        Qmy(event__name__contains='War Day:')
    )
    # Event Points = non-CUSTOM + Score Adjustments + CUSTOM without raid boss prefix
    tier_event_activities = (
        activities.exclude(event__event_type='CUSTOM') |
        activities.filter(event__event_type='CUSTOM', event__name__startswith='Score Adjustment:') |
        activities.filter(event__event_type='CUSTOM').filter(~_rb_q).exclude(event__name__startswith='Score Adjustment:').exclude(event__name__startswith='AP Adjustment:')
    )
    tier_event_activities = tier_event_activities.exclude(event__name__startswith='AP Adjustment:')
    event_points = (tier_event_activities.aggregate(
        total=Sum('points_earned'))['total'] or 0) + (tier_event_activities.aggregate(
        total=Sum('win_streak_bonus'))['total'] or 0)

    # Raid Boss Points = only CUSTOM events WITH raid boss prefix
    tier_raid_activities = activities.filter(event__event_type='CUSTOM').filter(_rb_q).exclude(
        event__name__startswith='AP Adjustment:'
    )
    raid_boss_points = (tier_raid_activities.aggregate(
        total=Sum('points_earned'))['total'] or 0) + (tier_raid_activities.aggregate(
        total=Sum('win_streak_bonus'))['total'] or 0)
    
    ap_points = activities.filter(
        event__name__startswith='AP Adjustment:'
    ).aggregate(total=Sum('points_earned'))['total'] or 0
    
    penalty_total = activities.exclude(
        event__name__startswith='AP Adjustment:'
    ).filter(points_earned__lt=0).aggregate(
        total=Sum('points_earned')
    )['total'] or 0
    
    attended_count = activities.exclude(
        event__name__startswith='AP Adjustment:'
    ).exclude(
        event__name__startswith='Score Adjustment:'
    ).filter(status='ATTENDED').count()
    
    total_events = ActivityEvent.objects.exclude(
        name__startswith='AP Adjustment:'
    ).exclude(
        name__startswith='Score Adjustment:'
    ).filter(
        date__gte=start_date,
        is_completed=True
    ).count()
    
    attendance_rate = (attended_count / total_events * 100) if total_events > 0 else 0
    
    # Calculate tier
    tier = _get_tier(event_points, raid_boss_points)
    
    # Calculate monthly rewards from custom events
    monthly_custom_events = PlayerActivity.objects.filter(
        player=character,
        event__date__year=today.year,
        event__date__month=today.month,
        event__event_type='CUSTOM',
        status='ATTENDED',
    ).select_related('event').exclude(
        event__name__startswith='AP Adjustment:'
    ).exclude(
        event__name__startswith='Score Adjustment:'
    )
    
    diamond_total = 0
    diamond_count = 0
    key_total = 0
    key_count = 0
    membership_total = 0
    membership_count = 0
    
    for act in monthly_custom_events:
        ev = act.event
        if ev.reward_diamond:
            diamond_total += ev.reward_diamond_points
            diamond_count += 1
        if ev.reward_key:
            key_total += ev.reward_key_points
            key_count += 1
        if ev.reward_membership:
            membership_total += ev.reward_membership_points
            membership_count += 1
    
    monthly_rewards = {
        'diamond_total': diamond_total,
        'diamond_count': diamond_count,
        'key_total': key_total,
        'key_count': key_count,
        'membership_total': membership_total,
        'membership_count': membership_count,
    }
    
    # All history should not be affected by the weekly reset start_date
    all_activities = PlayerActivity.objects.filter(
        player=character,
        event__is_completed=True
    ).select_related('event').order_by('-event__date')

    # Raid boss detection: CUSTOM events with boss type prefix
    from django.db.models import Q as Qhist
    _rb_hist_q = (
        Qhist(event__name__contains='[Raid Boss]') |
        Qhist(event__name__contains='[Territory Boss]') |
        Qhist(event__name__contains='[World Boss]') |
        Qhist(event__name__contains='[Rift Boss]') |
        Qhist(event__name__contains='[Arena Boss]') |
        Qhist(event__name__contains='War Day:')
    )
    # Activity Events History = non-CUSTOM + Score/AP Adjustments + CUSTOM without raid boss prefix
    regular_activities = (
        all_activities.exclude(event__event_type='CUSTOM') |
        all_activities.filter(event__event_type='CUSTOM', event__name__startswith='Score Adjustment:') |
        all_activities.filter(event__event_type='CUSTOM', event__name__startswith='AP Adjustment:') |
        all_activities.filter(event__event_type='CUSTOM').filter(~_rb_hist_q).exclude(event__name__startswith='Score Adjustment:').exclude(event__name__startswith='AP Adjustment:')
    )
    regular_activities = regular_activities.order_by('-event__date')
    
    # Raid Boss History = only CUSTOM events WITH raid boss prefix
    raid_activities = all_activities.filter(event__event_type='CUSTOM').filter(_rb_hist_q).exclude(
        event__name__startswith='AP Adjustment:'
    )

    from django.core.paginator import Paginator
    paginator_regular = Paginator(regular_activities, 20)
    page_number_regular = request.GET.get('page')
    paginated_regular = paginator_regular.get_page(page_number_regular)
    
    paginator_raid = Paginator(raid_activities, 20)
    page_number_raid = request.GET.get('page_raid')
    paginated_raid = paginator_raid.get_page(page_number_raid)
    
    context = {
        'character': character,
        'monthly_report': monthly_report,
        'activities': paginated_regular,
        'raid_activities': paginated_raid,
        'total_points': total_points,
        'event_points': event_points,
        'raid_boss_points': raid_boss_points,
        'ap_points': ap_points,
        'penalty_total': penalty_total,
        'attended_count': attended_count,
        'total_events': total_events,
        'attendance_rate': attendance_rate,
        'tier': tier,
        'monthly_rewards': monthly_rewards,
        'is_admin': is_admin(request.user),
        'viewing_other': viewing_other,
    }
    return render(request, 'items/my_activity.html', context)


@login_required
def admin_all_members_activity(request):
    """
    Super Admin only: View list of all members to inspect their activity.
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Only super administrators can access this page.")
    
    today = timezone.now()
    month_ago = today - timedelta(days=30)
    
    characters = Character.objects.select_related('owner').all().order_by('name')
    
    members = []
    for char in characters:
        activities = PlayerActivity.objects.filter(
            player=char,
            event__date__gte=month_ago,
            event__is_completed=True
        ).exclude(event__name__startswith='AP Adjustment:').exclude(event__name__startswith='Score Adjustment:')
        
        total_points = (activities.aggregate(
            total=Sum('points_earned'))['total'] or 0) + (activities.aggregate(
            total=Sum('win_streak_bonus'))['total'] or 0)

        event_activities = activities.exclude(event__event_type='CUSTOM') | activities.filter(
            event__event_type='CUSTOM',
            event__name__startswith='Score Adjustment:'
        )
        event_points = (event_activities.aggregate(
            total=Sum('points_earned'))['total'] or 0) + (event_activities.aggregate(
            total=Sum('win_streak_bonus'))['total'] or 0)

        raid_activities = activities.filter(event__event_type='CUSTOM').exclude(
            event__name__startswith='Score Adjustment:'
        )
        raid_boss_points = (raid_activities.aggregate(
            total=Sum('points_earned'))['total'] or 0) + (raid_activities.aggregate(
            total=Sum('win_streak_bonus'))['total'] or 0)
        
        attended = activities.filter(status='ATTENDED').count()
        
        members.append({
            'character': char,
            'total_points': total_points,
            'attended': attended,
            'tier': _get_tier(event_points, raid_boss_points),
        })
    
    members.sort(key=lambda x: x['total_points'], reverse=True)
    
    context = {
        'members': members,
        'is_admin': True,
    }
    return render(request, 'items/admin_all_members_activity.html', context)


@login_required
@require_http_methods(["POST"])
def reset_monthly_rewards(request):
    """
    Admin action to reset all monthly reward data (diamond/key/membership)
    from custom events in the current month.
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can reset rewards.")
    
    today = timezone.now()
    
    # Reset reward flags on all custom events this month
    updated = ActivityEvent.objects.filter(
        date__year=today.year,
        date__month=today.month,
        event_type='CUSTOM',
    ).exclude(
        name__startswith='AP Adjustment:'
    ).exclude(
        name__startswith='Score Adjustment:'
    ).update(
        reward_diamond=False,
        reward_diamond_points=0,
        reward_key=False,
        reward_key_points=0,
        reward_membership=False,
        reward_membership_points=0,
    )
    
    from django.contrib import messages
    messages.success(request, f"Monthly rewards reset successfully. ({updated} events updated)")
    
    return redirect('my-activity')


def _generate_due_repeatable_events():
    """
    Auto-generate repeatable events when their scheduled date has arrived.
    Only creates the NEXT occurrence from a completed repeatable event,
    and only if today >= the next scheduled date (hari H jam 00:00).
    """
    from django.utils import timezone
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Find all completed repeatable events
    completed_repeatables = ActivityEvent.objects.filter(
        is_repeatable=True,
        is_completed=True,
    ).order_by('-date')
    
    # Track which event names we've already processed to avoid duplicates
    processed = set()
    
    for event in completed_repeatables:
        # Use name as key to avoid processing same event chain multiple times
        if event.name in processed:
            continue
        processed.add(event.name)
        
        # Calculate next occurrence date (7 days after this event)
        next_date = event.date + timedelta(days=7)
        
        # Only generate if today >= next_date (hari H sudah tiba)
        if timezone.now() < next_date.replace(hour=0, minute=0, second=0, microsecond=0):
            continue
        
        # Check if event for this date already exists
        already_exists = ActivityEvent.objects.filter(
            name=event.name,
            date__year=next_date.year,
            date__month=next_date.month,
            date__day=next_date.day,
        ).exists()
        
        if not already_exists:
            ActivityEvent.objects.create(
                name=event.name,
                event_type=event.event_type,
                date=next_date,
                is_completed=False,
                is_repeatable=True,
                is_mandatory=event.is_mandatory,
                mandatory_penalty=event.mandatory_penalty,
                is_win=False,
                max_points=event.max_points,
                base_points=event.base_points,
                boss_point_config=event.boss_point_config or {},
                reward_diamond=event.reward_diamond,
                reward_diamond_points=event.reward_diamond_points,
                reward_key=event.reward_key,
                reward_key_points=event.reward_key_points,
                reward_membership=event.reward_membership,
                reward_membership_points=event.reward_membership_points,
            )


@login_required
def manage_events(request):
    """
    Admin page to manage events
    """
    if not check_event_admin(request.user):
        return HttpResponseForbidden("Only Event administrators can manage events.")
    
    # AUTO-GENERATE repeatable events that are due today (hari H jam 00:00)
    _generate_due_repeatable_events()
    
    # Get all actual events (excluding manual point adjustments & Raid Boss page events)
    from django.db.models import Q
    # Raid Boss page creates CUSTOM events with [Boss Type] prefix or War Day prefix
    raid_boss_prefixes = ['[Raid Boss]', '[Territory Boss]', '[World Boss]', '[Rift Boss]', '[Arena Boss]']
    raid_boss_q = Q()
    for prefix in raid_boss_prefixes:
        raid_boss_q |= Q(name__contains=prefix)
    
    events = ActivityEvent.objects.exclude(
        name__startswith='AP Adjustment:'
    ).exclude(
        name__startswith='Score Adjustment:'
    ).exclude(
        # Exclude Raid Boss page events (CUSTOM with boss type prefix)
        Q(event_type='CUSTOM') & raid_boss_q
    ).exclude(
        # Exclude War Day raid boss events
        Q(event_type='CUSTOM') & Q(name__contains='War Day:')
    ).order_by('-date')[:50]
    
    context = {
        'events': events,
        'is_admin': True,
    }
    return render(request, 'items/manage_events.html', context)


@login_required
def complete_event(request, event_pk):
    """Complete event with Win/Lose result via form POST."""
    if not check_event_admin(request.user):
        return HttpResponseForbidden("Only Event administrators can manage events.")
    
    if request.method == 'POST':
        from items.models import ActivityEvent, PlayerActivity, DiscordAnnouncement
        event = get_object_or_404(ActivityEvent, pk=event_pk)
        # Per-clan results for Boss Rush, Catacombs, Dimensional Siege
        if event.event_type in ActivityEvent.CLAN_RESULT_EVENT_TYPES:
            result_valkyrie = request.POST.get('result_valkyrie', 'win')
            result_valhalla = request.POST.get('result_valhalla', 'win')
            event.is_win_valkyrie = (result_valkyrie == 'win')
            event.is_win_valhalla = (result_valhalla == 'win')
            event.is_win = event.is_win_valkyrie or event.is_win_valhalla
        else:
            result = request.POST.get('result', 'win')
            event.is_win = (result == 'win')
            event.is_win_valkyrie = event.is_win
            event.is_win_valhalla = event.is_win
        event.is_completed = True
        event.save()

        from .services import sync_event_dkp_penalties
        sync_event_dkp_penalties(event)
        
        # Count participants (only ATTENDED)
        participant_count = PlayerActivity.objects.filter(event=event, status='ATTENDED').count()
        # Build result text per clan
        if event.event_type in ActivityEvent.CLAN_RESULT_EVENT_TYPES:
            vk_r = "✅ WIN" if event.is_win_valkyrie else "❌ LOSE"
            vh_r = "✅ WIN" if event.is_win_valhalla else "❌ LOSE"
            result_text = f"Valkyrie: {vk_r} | Valhalla: {vh_r}"
        else:
            result_text = "✅ WIN" if event.is_win else "❌ LOSE"
        
        # Create Discord announcement
        announcement_msg = (
            f"[EVENT_COMPLETED]\n"
            f"@everyone 📢 **The event has ended!**\n\n"
            f"🏆 **EVENT COMPLETED!**\n"
            f"**{event.name}** has been completed.\n\n"
            f"🔴 **Status:** COMPLETED - Check-in closed\n"
            f"⭐ **Max Points:** {event.max_points} pts\n"
            f"👥 **Participants:** {participant_count} players\n"
            f"🏅 **Result:** {result_text}\n\n"
            f"Points have been calculated and added to the leaderboard!"
        )
        try:
            DiscordAnnouncement.objects.create(message=announcement_msg)
        except Exception:
            pass
        
        # Recalculate win streak bonuses
        try:
            from items.api_views import recalculate_win_streak_bonuses
            recalculate_win_streak_bonuses()
        except Exception:
            pass
    
    return redirect('manage-events')

@login_required
def create_event(request):
    """
    Admin page to create new event
    """
    if not check_event_admin(request.user):
        return HttpResponseForbidden("Only Event administrators can create events.")
    
    if request.method == 'POST':
        event_type = request.POST.get('event_type')
        name = request.POST.get('name')
        custom_name = request.POST.get('custom_name', '').strip()
        date_str = request.POST.get('date')
        
        # Handle custom event reward checkboxes
        reward_diamond = False
        reward_diamond_points = 0
        reward_key = False
        reward_key_points = 0
        reward_membership = False
        reward_membership_points = 0
        
        if event_type == 'CUSTOM':
            reward_diamond = request.POST.get('reward_diamond') == 'on'
            reward_key = request.POST.get('reward_key') == 'on'
            reward_membership = request.POST.get('reward_membership') == 'on'
            
            if reward_diamond:
                try:
                    reward_diamond_points = int(request.POST.get('reward_diamond_points', 0))
                except (ValueError, TypeError):
                    reward_diamond_points = 0
            if reward_key:
                try:
                    reward_key_points = int(request.POST.get('reward_key_points', 0))
                except (ValueError, TypeError):
                    reward_key_points = 0
            if reward_membership:
                try:
                    reward_membership_points = int(request.POST.get('reward_membership_points', 0))
                except (ValueError, TypeError):
                    reward_membership_points = 0
        
        # For custom events, use the custom name and build reward summary
        if event_type == 'CUSTOM' and custom_name:
            reward_parts = []
            if reward_diamond:
                reward_parts.append(f"💎 Diamond: {reward_diamond_points}pts")
            if reward_key:
                reward_parts.append(f"🔑 Key: {reward_key_points}pts")
            if reward_membership:
                reward_parts.append(f"👑 Membership: {reward_membership_points}pts")
            
            if reward_parts:
                final_name = f"{custom_name} ({', '.join(reward_parts)})"
            else:
                final_name = custom_name
        elif name:
            final_name = name
        else:
            final_name = f"{event_type} Event"
        
        # Get default points for this event type
        default_pts = ActivityEvent.DEFAULT_POINTS.get(event_type, 10)
        
        # Parse editable points (user can override default)
        try:
            event_points = int(request.POST.get('event_points', default_pts))
        except (ValueError, TypeError):
            event_points = default_pts

        # Parse penalty points for mandatory events
        penalty_pts = 0
        dkp_penalty_pts = 0
        is_dkp_penalty = request.POST.get('is_dkp_penalty') == 'on'
        
        if request.POST.get('is_mandatory') == 'on':
            try:
                penalty_pts = int(request.POST.get('penalty_points', 5))
            except (ValueError, TypeError):
                penalty_pts = 5
                
            if is_dkp_penalty:
                try:
                    dkp_penalty_pts = int(request.POST.get('dkp_penalty_points', 5))
                except (ValueError, TypeError):
                    dkp_penalty_pts = 5
        
        # Build event kwargs
        event_kwargs = {
            'event_type': event_type,
            'name': final_name,
            'date': datetime.strptime(date_str, '%Y-%m-%dT%H:%M'),
            'is_completed': False,
            'is_repeatable': request.POST.get('is_repeatable') == 'on',
            'is_mandatory': request.POST.get('is_mandatory') == 'on',
            'mandatory_penalty': penalty_pts,
            'is_dkp_penalty': is_dkp_penalty,
            'dkp_mandatory_penalty': dkp_penalty_pts,
            'is_win': False,
            'max_points': event_points,
            'reward_diamond': reward_diamond,
            'reward_diamond_points': reward_diamond_points,
            'reward_key': reward_key,
            'reward_key_points': reward_key_points,
            'reward_membership': reward_membership,
            'reward_membership_points': reward_membership_points,
        }
        

        if event_type.startswith('INV_') or event_type == 'INVASION':
            event_kwargs['boss_point_config'] = {
                'dragon_beast': 50,
                'carnifex': 25,
                'orfen': 100,
            }
            
            if request.POST.get('is_mandatory') == 'on':
                mandatory_penalties = {}
                dkp_mandatory_penalties = {}
                
                if request.POST.get('mandatory_dragon_beast') == 'on':
                    try:
                        mandatory_penalties['dragon_beast'] = int(request.POST.get('penalty_dragon_beast', 5))
                    except (ValueError, TypeError):
                        pass
                    if is_dkp_penalty:
                        try:
                            dkp_mandatory_penalties['dragon_beast'] = int(request.POST.get('dkp_penalty_dragon_beast', 5))
                        except (ValueError, TypeError):
                            pass
                            
                if request.POST.get('mandatory_carnifex') == 'on':
                    try:
                        mandatory_penalties['carnifex'] = int(request.POST.get('penalty_carnifex', 5))
                    except (ValueError, TypeError):
                        pass
                    if is_dkp_penalty:
                        try:
                            dkp_mandatory_penalties['carnifex'] = int(request.POST.get('dkp_penalty_carnifex', 5))
                        except (ValueError, TypeError):
                            pass
                            
                if request.POST.get('mandatory_orfen') == 'on':
                    try:
                        mandatory_penalties['orfen'] = int(request.POST.get('penalty_orfen', 5))
                    except (ValueError, TypeError):
                        pass
                    if is_dkp_penalty:
                        try:
                            dkp_mandatory_penalties['orfen'] = int(request.POST.get('dkp_penalty_orfen', 5))
                        except (ValueError, TypeError):
                            pass
                
                if not mandatory_penalties:
                    temp_event = ActivityEvent(event_type=event_type, is_mandatory=True)
                    mandatory_penalties = temp_event.get_default_mandatory_boss_penalties()

                event_kwargs['mandatory_boss_penalties'] = mandatory_penalties
                event_kwargs['dkp_mandatory_boss_penalties'] = dkp_mandatory_penalties
        
        event_kwargs['input_by'] = request.user
        event = ActivityEvent.objects.create(**event_kwargs)
        
        return redirect('manage-events')
    
    import json
    context = {
        'event_types': [(v, l) for v, l in ActivityEvent.EVENT_TYPE_CHOICES if v != 'WAR_DAY'],
        'default_points': json.dumps(ActivityEvent.DEFAULT_POINTS),
        'is_admin': True,
    }
    return render(request, 'items/create_event.html', context)


@login_required
def record_attendance(request, event_pk):
    """
    Admin page to record attendance for an event
    """
    if not check_event_admin(request.user):
        return HttpResponseForbidden("Only Event administrators can record attendance.")
    
    event = get_object_or_404(ActivityEvent, pk=event_pk)
    invasion_boss_keys = event.get_invasion_boss_keys()
    # Optimized: prefetch related data
    all_characters = Character.objects.all().select_related('owner').only('id', 'name', 'level', 'character_class', 'clan', 'owner_id').order_by('name')
    
    # Get existing attendance details
    attendance_map = {}
    activities = PlayerActivity.objects.filter(event=event)
    for act in activities:
        attendance_map[act.player_id] = {
            'status': act.status,
            'bosses_killed': act.bosses_killed or {},
            'checkin_verified': act.checkin_verified,
            'party_scan_verified': act.party_scan_verified,
        }
    
    if request.method == 'POST':
        # Save boss points if Invasion
        if event.uses_boss_attendance:
            boss_defaults = {
                'dragon_beast': 50,
                'carnifex': 25,
                'orfen': 100,
            }
            boss_point_config = {}
            for boss_key in invasion_boss_keys:
                try:
                    boss_point_config[boss_key] = int(request.POST.get(f'{boss_key}_points', boss_defaults.get(boss_key, 0)))
                except (ValueError, TypeError):
                    boss_point_config[boss_key] = boss_defaults.get(boss_key, 0)
            event.boss_point_config = boss_point_config
            event.save()
        
        party_scan_ids = set(request.POST.getlist('party_scan_verified'))

        # Create/update validation records. Final attendance is now derived
        # only from the Party Scan verification.
        for char in all_characters:
            char_id = str(char.pk)
            party_scan_verified = char_id in party_scan_ids

            defaults = {
                'status': 'ATTENDED' if party_scan_verified else 'ABSENT',
                'points_earned': 0,
                'checkin_verified': party_scan_verified, # Deprecated, sync with party scan
                'party_scan_verified': party_scan_verified,
            }

            # For Invasion, capture INDIVIDUAL boss checkboxes
            if event.uses_boss_attendance:
                defaults['bosses_killed'] = {
                    boss_key: request.POST.get(f'boss_{boss_key}_{char.pk}') == 'true'
                    for boss_key in invasion_boss_keys
                }
            else:
                defaults['bosses_killed'] = {}

            activity, created = PlayerActivity.objects.update_or_create(
                player=char,
                event=event,
                defaults=defaults
            )
            # Force re-save to trigger point calculation in model's save().
            activity.save()
        
        # Recalculate win streak bonuses since attendance status changed
        from items.api_views import recalculate_win_streak_bonuses
        recalculate_win_streak_bonuses()

        from .services import sync_event_dkp_penalties
        sync_event_dkp_penalties(event)
        
        # Auto-calculate monthly reports
        from .services import calculate_monthly_reports
        calculate_monthly_reports(event.date.year, event.date.month)
        
        return redirect('manage-events')
    
    
    # Prepare characters with attendance info attached
    processed_characters = []
    for char in all_characters:
        att = attendance_map.get(char.pk)
        char.checkin_verified = att['checkin_verified'] if att else False
        char.party_scan_verified = att['party_scan_verified'] if att else False
        char.is_attended = bool(att and att['status'] == 'ATTENDED')
        char.bosses_killed = att['bosses_killed'] if att else {}
        char.invasion_bosses = [
            {
                'key': boss_key,
                'label': ActivityEvent.INVASION_BOSS_LABELS.get(boss_key, boss_key.replace('_', ' ').title()),
                'checked': char.bosses_killed.get(boss_key, False),
            }
            for boss_key in invasion_boss_keys
        ]
        processed_characters.append(char)
        
    bosspc = event.boss_point_config or {}
    boss_defaults = {
        'dragon_beast': 50,
        'carnifex': 25,
        'orfen': 100,
    }
    boss_points = [
        {
            'key': boss_key,
            'label': ActivityEvent.INVASION_BOSS_LABELS.get(boss_key, boss_key.replace('_', ' ').title()),
            'value': bosspc.get(boss_key, boss_defaults.get(boss_key, 0)),
        }
        for boss_key in invasion_boss_keys
    ]
    
    # Split characters by clan
    valkyrie_chars = [c for c in processed_characters if getattr(c, 'clan', 'Valkyrie') == 'Valkyrie']
    
    context = {
        'event': event,
        'characters': processed_characters,
        'valkyrie_chars': valkyrie_chars,
        'boss_points': boss_points,
        'is_admin': True,
    }
    return render(request, 'items/record_attendance.html', context)


@login_required
@require_http_methods(["POST"])
def scan_party_for_event(request, event_pk):
    """
    Scan one clan's party screenshot and store party-scan validation for the event.
    ADDITIVE MODE: Multiple scans will ADD members, not replace previous scans.
    """
    if not check_event_admin(request.user):
        return JsonResponse({'error': 'Only Event administrators can scan party attendance.'}, status=403)

    event = get_object_or_404(ActivityEvent, pk=event_pk)
    clan = request.POST.get('clan')
    screenshot = request.FILES.get('screenshot')

    if clan not in ('Valkyrie', 'Valhalla'):
        return JsonResponse({'error': 'Invalid clan selected.'}, status=400)
    if not screenshot:
        return JsonResponse({'error': 'No image provided'}, status=400)

    try:
        scan_result = _scan_party_members_from_image(screenshot)
        if not scan_result.get('success'):
            return JsonResponse({'error': scan_result.get('error', 'Unable to scan image')}, status=scan_result.get('status', 500))

        detected_names = scan_result.get('all_names', [])
        detected_lookup = {name.lower(): name for name in detected_names}

        clan_characters = Character.objects.filter(clan=clan).only('id', 'name', 'clan')
        matched = []
        unmatched_detected = []
        matched_name_keys = set()

        # ADDITIVE MODE: Hanya update member yang ditemukan di scan ini
        # Member yang sudah ter-scan sebelumnya TIDAK di-reset
        for character in clan_characters:
            activity, _created = PlayerActivity.objects.get_or_create(
                player=character,
                event=event,
                defaults={'status': 'ABSENT', 'points_earned': 0}
            )

            # Cek apakah character ini ditemukan di scan saat ini
            # Pertama: exact match terhadap detected names (sudah di-normalize via fuzzy)
            is_matched_now = character.name.lower() in detected_lookup
            # Fallback: fuzzy match terhadap raw OCR results (jika normalize belum ter-catch)
            if not is_matched_now:
                from difflib import SequenceMatcher
                for det_name in detected_lookup:
                    ratio = SequenceMatcher(None, character.name.lower(), det_name).ratio()
                    if ratio >= 0.75:
                        is_matched_now = True
                        break
            
            # ADDITIVE: Jika sudah ter-scan sebelumnya ATAU ditemukan di scan ini, set True
            if is_matched_now:
                activity.party_scan_verified = True
                activity.checkin_verified = True # Deprecated, sync with party scan
                activity.status = 'ATTENDED' if activity.party_scan_verified else 'ABSENT'
                activity.save()

            # Return semua member yang ter-scan (baik dari scan sebelumnya maupun scan ini)
            if activity.party_scan_verified:
                matched.append({
                    'id': character.pk,
                    'name': character.name,
                    'checkin_verified': activity.checkin_verified,
                    'party_scan_verified': activity.party_scan_verified,
                    'is_attended': activity.status == 'ATTENDED',
                })
                matched_name_keys.add(character.name.lower())

        clan_name_lookup = {c.name.lower() for c in clan_characters}
        for detected in detected_names:
            detected_key = detected.lower()
            if detected_key not in clan_name_lookup and detected_key not in matched_name_keys:
                unmatched_detected.append(detected)

        from .services import sync_event_dkp_penalties
        sync_event_dkp_penalties(event)

        # Update scan_info dengan total yang ter-scan (bukan hanya scan ini)
        total_scanned = len(matched)
        if not event.scan_info:
            event.scan_info = {}
        event.scan_info[clan.lower()] = {
            'detected_count': len(detected_names),
            'matched_count': len([m for m in matched if m['name'].lower() in detected_lookup]),  # Hanya yang baru di-scan
            'total_scanned': total_scanned  # Total keseluruhan
        }
        event.save(update_fields=['scan_info'])


        return JsonResponse({
            'success': True,
            'clan': clan,
            'detected_count': len(detected_names),
            'matched_count': len([m for m in matched if m['name'].lower() in detected_lookup]),  # Yang baru di-scan
            'total_scanned': total_scanned,  # Total keseluruhan
            'matched': matched,  # Semua yang ter-scan (termasuk scan sebelumnya)
            'unmatched_detected': unmatched_detected[:50],
            'scan': scan_result,
        })
    except ImportError:
        return JsonResponse({'error': 'EasyOCR is not installed on this server. Please install it with: pip install easyocr'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def duplicate_event(request, event_pk):
    """
    Duplicate an event exactly 7 days later
    """
    if not check_event_admin(request.user):
        return HttpResponseForbidden("Only Event administrators can duplicate events.")
    
    event = get_object_or_404(ActivityEvent, pk=event_pk)
    
    if request.method == 'POST':
        # Create a new event 7 days later
        new_event = ActivityEvent.objects.create(
            name=event.name,
            event_type=event.event_type,
            date=event.date + timedelta(days=7),
            is_completed=False,
            is_repeatable=getattr(event, 'is_repeatable', False),
            is_mandatory=getattr(event, 'is_mandatory', False),
            mandatory_penalty=getattr(event, 'mandatory_penalty', 5),
            is_win=False,
            max_points=event.max_points,
            base_points=event.base_points,
            boss_point_config=event.boss_point_config,
        )
        return redirect('manage-events')
        
    # If not POST, just redirect back
    return redirect('manage-events')


@login_required
def toggle_event_repeatable(request, event_pk):
    """
    Toggle the is_repeatable status of an event
    """
    if not check_event_admin(request.user):
        return HttpResponseForbidden("Only Event administrators can manage events.")
    
    event = get_object_or_404(ActivityEvent, pk=event_pk)
    
    if request.method == 'POST':
        event.is_repeatable = not event.is_repeatable
        event.save()
        
    return redirect('manage-events')


# ======================================================
# DISCORD LINK VIEW
# ======================================================

@login_required
def link_discord(request, character_pk):
    """Allow users to link their Discord ID to their character"""
    character = get_object_or_404(Character, pk=character_pk)
    
    # Check ownership or admin
    if character.owner != request.user and not is_admin(request.user):
        return HttpResponseForbidden("You can only link Discord to your own character.")
    
    if request.method == 'POST':
        discord_id = request.POST.get('discord_id', '').strip()
        
        # Validate Discord ID (should be 17-19 digits)
        if discord_id and discord_id.isdigit() and 17 <= len(discord_id) <= 19:
            # Check if already used by another character
            existing = Character.objects.filter(discord_id=discord_id).exclude(pk=character.pk).first()
            if existing:
                return render(request, 'items/link_discord.html', {
                    'character': character,
                    'error': f'Discord ID sudah digunakan oleh karakter: {existing.name}'
                })
            
            character.discord_id = discord_id
            character.save()
            return redirect('character-profile', pk=character.pk)
        elif discord_id == '':
            # Clear Discord ID
            character.discord_id = None
            character.save()
            return redirect('character-profile', pk=character.pk)
        else:
            return render(request, 'items/link_discord.html', {
                'character': character,
                'error': 'Discord ID tidak valid. Harus berupa 17-19 digit angka.'
            })
    
    return render(request, 'items/link_discord.html', {'character': character})

# ======================================================
# ADMIN USER MANAGEMENT
# ======================================================

from django.contrib.auth.models import User

@login_required
def reset_password_admin(request, user_pk):
    """Admin/Sub Admin: Reset password for users"""
    if not is_any_admin(request.user):
        return HttpResponseForbidden("Only administrators can reset passwords.")
    
    target_user = get_object_or_404(User, pk=user_pk)
    
    # Sub Admin cannot reset Super Admin passwords
    if not is_admin(request.user) and target_user.is_staff:
        return HttpResponseForbidden("Sub Admins cannot reset Super Admin passwords.")
    
    # Redirect back to management page
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        if new_password and len(new_password) >= 4:
            target_user.set_password(new_password)
            target_user.save()
            messages.success(request, f"Password reset successfully for {target_user.username}")
    
    return redirect('character-management')

@login_required
def toggle_admin(request, user_pk):
    """Admin only: Toggle is_staff status for a user (make/remove admin)"""
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can change admin status.")
    
    target_user = get_object_or_404(User, pk=user_pk)
    
    # Prevent demoting yourself
    if target_user == request.user:
        messages.error(request, "You cannot change your own admin status.")
        return redirect('character-management')
    
    # Prevent demoting superusers (only superuser can demote another admin)
    if target_user.is_staff and not request.user.is_superuser:
        messages.error(request, "Only superusers can remove admin status from other admins.")
        return redirect('character-management')
    
    # Toggle is_staff
    target_user.is_staff = not target_user.is_staff
    target_user.save()
    
    action = "promoted to Admin" if target_user.is_staff else "demoted from Admin"
    messages.success(request, f"{target_user.username} has been {action}.")
    
    return redirect('character-management')

@login_required
def toggle_sub_admin(request, user_pk):
    """Super Admin only: Toggle Sub Admin group for a user"""
    if not is_admin(request.user):
        return HttpResponseForbidden("Only super administrators can manage Sub Admin status.")
    
    from django.contrib.auth.models import Group
    target_user = get_object_or_404(User, pk=user_pk)
    
    # Don't allow on yourself
    if target_user == request.user:
        messages.error(request, "You cannot change your own Sub Admin status.")
        return redirect('character-management')
    
    # Don't allow on super admins
    if target_user.is_staff:
        messages.error(request, "Super Admins don't need Sub Admin role.")
        return redirect('character-management')
    
    sub_admin_group, _ = Group.objects.get_or_create(name='Sub Admin')
    
    if sub_admin_group in target_user.groups.all():
        target_user.groups.remove(sub_admin_group)
        
        # Also clear all admin roles when removing Sub Admin
        from dkp.models import AdminRole
        try:
            role = AdminRole.objects.get(user=target_user)
            role.is_dkp_admin = False
            role.is_event_admin = False
            role.is_raidboss_admin = False
            role.is_treasury_admin = False
            role.is_auction_admin = False
            role.save()
        except AdminRole.DoesNotExist:
            pass
        
        messages.success(request, f"{target_user.username} removed from Sub Admin.")
    else:
        target_user.groups.add(sub_admin_group)
        messages.success(request, f"{target_user.username} promoted to Sub Admin.")
    
    return redirect('character-management')

@login_required
def toggle_admin_role(request, user_pk):
    """Super Admin only: Toggle granular admin roles (DKP, Event, Treasury, Auction)"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    if request.method == 'POST':
        from dkp.models import AdminRole
        import json
        
        target_user = get_object_or_404(User, pk=user_pk)
        data = json.loads(request.body)
        
        # Don't allow changing own permissions unless superuser
        if target_user == request.user and not request.user.is_superuser:
            return JsonResponse({'error': 'Cannot change own roles'}, status=400)
            
        role, _ = AdminRole.objects.get_or_create(user=target_user)
        role.is_dkp_admin = data.get('is_dkp_admin', role.is_dkp_admin)
        role.is_event_admin = data.get('is_event_admin', role.is_event_admin)
        role.is_raidboss_admin = data.get('is_raidboss_admin', role.is_raidboss_admin)
        role.is_treasury_admin = data.get('is_treasury_admin', role.is_treasury_admin)
        role.is_auction_admin = data.get('is_auction_admin', role.is_auction_admin)
        role.is_soul_admin = data.get('is_soul_admin', role.is_soul_admin)
        role.is_powerrank_admin = data.get('is_powerrank_admin', role.is_powerrank_admin)
        role.is_warpoint_admin = data.get('is_warpoint_admin', role.is_warpoint_admin)
        role.can_give_dkp = data.get('can_give_dkp', role.can_give_dkp)
        role.can_remove_dkp = data.get('can_remove_dkp', role.can_remove_dkp)
        role.can_decay_dkp = data.get('can_decay_dkp', role.can_decay_dkp)
        role.save()
        
        return JsonResponse({'success': True, 'message': f'Roles updated for {target_user.username}'})
        
    return JsonResponse({'error': 'POST required'}, status=405)

# ======================================================
# DISCORD MANAGEMENT
# ======================================================

from .models import DiscordAlarm, DiscordAnnouncement

@login_required
def discord_dashboard(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("Admin only.")
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_alarm':
            day = int(request.POST.get('day'))
            time = request.POST.get('time')
            msg = request.POST.get('message')
            DiscordAlarm.objects.create(day=day, time=time, message=msg)
            
        elif action == 'delete_alarm':
            alarm_id = request.POST.get('alarm_id')
            DiscordAlarm.objects.filter(id=alarm_id).delete()
            
        elif action == 'send_broadcast':
            message = request.POST.get('broadcast_message')
            mention = request.POST.get('mention_everyone')
            if message:
                if mention:
                    message = '@everyone\n' + message
                DiscordAnnouncement.objects.create(message=message)
                
        return redirect('discord-dashboard')
    
    alarms = DiscordAlarm.objects.order_by('day', 'time')
    announcements = DiscordAnnouncement.objects.order_by('-created_at')[:10]
    
    context = {
        'alarms': alarms,
        'announcements': announcements,
        'days': DiscordAlarm.DAYS,
    }
    return render(request, 'items/discord_dashboard.html', context)


# ======================================================
# UNIVERSAL POWER RANK VIEWS
# ======================================================
from .models import UniversalPowerRank

@login_required
def power_rank_leaderboard(request):
    """
    Universal Power Rank leaderboard - shows all characters ranked by gear score combined.
    Supports clan tab filter via ?tab= parameter.
    """
    clan_tab = request.GET.get('tab', 'overall')
    
    rankings_qs = UniversalPowerRank.objects.select_related('character').prefetch_related('screenshots').all()
    rankings_qs = rankings_qs.order_by('-gear_score')

    # Build overall leaderboard
    all_rankings = list(rankings_qs)
    
    # Filter by clan tab
    if clan_tab == 'valkyrie':
        filtered = [pr for pr in all_rankings if pr.character.clan == 'Valkyrie']
    elif clan_tab == 'valhalla':
        filtered = [pr for pr in all_rankings if pr.character.clan == 'Valhalla']
    else:
        filtered = all_rankings
    
    leaderboard = []
    for i, pr in enumerate(filtered, 1):
        leaderboard.append({
            'rank': i,
            'power_rank': pr,
            'character': pr.character,
        })

    # Check if current user has characters in the leaderboard
    user_rankings = []
    user_power_rank = None # maintain for fallback reference
    user_characters = Character.objects.filter(owner=request.user)
    user_char_ids = set(user_characters.values_list('pk', flat=True))
    
    for item in leaderboard:
        if item['character'].pk in user_char_ids:
            user_rankings.append(item)
            if not user_power_rank:
                user_power_rank = item['power_rank']

    is_pr_admin = False
    if request.user.is_authenticated:
        from dkp.models import AdminRole
        role = AdminRole.objects.filter(user=request.user).first()
        if role and role.is_powerrank_admin:
            is_pr_admin = True

    is_user_admin = is_admin(request.user) or is_pr_admin

    unverified_names = []
    if is_user_admin:
        unverified_names = [pr.character.name for pr in all_rankings if not pr.is_validated]

    overall_has_pending_updates = any(pr.pending_changes for pr in all_rankings)
    overall_pending_names = [pr.character.name for pr in all_rankings if pr.pending_changes]

    farm_spot_groups, farm_spot_unassigned, farm_snapshot_meta = _get_farm_snapshot_display(clan_tab)

    context = {
        'leaderboard': leaderboard,
        'user_power_rank': user_power_rank,
        'user_rankings': user_rankings,
        'is_admin': is_user_admin,
        'clan_tab': clan_tab,
        'unverified_names': unverified_names,
        'farm_spot_groups': farm_spot_groups,
        'farm_spot_unassigned': farm_spot_unassigned,
        'farm_snapshot_meta': farm_snapshot_meta,
        'overall_has_pending_updates': overall_has_pending_updates,
        'overall_pending_names': overall_pending_names,
    }
    return render(request, 'items/power_rank_leaderboard.html', context)


def _farm_spot_zones():
    return [
        {'name': 'The Last Ground', 'start': 1, 'end': 2},
        {'name': 'Fields of Massacre', 'start': 3, 'end': 21},
        {'name': 'National Cemetery (Top)', 'start': 22, 'end': 25},
        {'name': 'National Cemetery', 'start': 26, 'end': 37},
        {'name': 'Forsaken Plains', 'start': 38, 'end': 45},
        {'name': 'War-Torn Plains', 'start': 46, 'end': 52},
    ]


def _build_power_rank_snapshot(tab):
    from .models import UniversalPowerRank

    rankings_qs = UniversalPowerRank.objects.select_related('character').all().order_by('-gear_score')
    all_rankings = list(rankings_qs)

    if tab == 'valkyrie':
        filtered = [pr for pr in all_rankings if pr.character.clan == 'Valkyrie']
    elif tab == 'valhalla':
        filtered = [pr for pr in all_rankings if pr.character.clan == 'Valhalla']
    else:
        filtered = all_rankings

    # Only validated entries are allowed into the saved farm snapshot.
    filtered = [pr for pr in filtered if pr.is_validated]

    snapshot = []
    for idx, pr in enumerate(filtered[:52], 1):
        snapshot.append({
            'spot_no': idx,
            'rank': idx,
            'character_id': pr.character.pk,
            'character_name': pr.character.name,
            'clan': pr.character.clan or '',
            'gear_score': pr.gear_score,
            'power_class': pr.power_class or '',
        })
    return snapshot, max(0, len(filtered) - 52)


def _get_farm_snapshot_display(tab):
    from .models import PowerRankFarmSnapshot

    snapshot = PowerRankFarmSnapshot.objects.filter(tab=tab).first()
    snapshot_data = snapshot.snapshot_data if snapshot else []

    farm_spot_groups = []
    for zone in _farm_spot_zones():
        slots = [slot for slot in snapshot_data if zone['start'] <= slot.get('spot_no', 0) <= zone['end']]
        if slots:
            farm_spot_groups.append({
                'name': zone['name'],
                'start': zone['start'],
                'end': zone['end'],
                'slots': slots,
            })

    assigned_count = len(snapshot_data)
    farm_spot_unassigned = max(0, assigned_count - 52)
    farm_snapshot_meta = {
        'updated_at': snapshot.updated_at if snapshot else None,
        'updated_by': snapshot.updated_by if snapshot else None,
        'has_data': bool(snapshot_data),
    }
    return farm_spot_groups, farm_spot_unassigned, farm_snapshot_meta


@login_required
@require_http_methods(["POST"])
def update_power_rank_farm_snapshot(request):
    from .models import PowerRankFarmSnapshot, UniversalPowerRank
    from dkp.models import AdminRole

    role = AdminRole.objects.filter(user=request.user).first()
    if not (is_admin(request.user) or (role and role.is_powerrank_admin)):
        return HttpResponseForbidden("Only Power Rank administrators can update the farm spot snapshot.")

    tab = request.POST.get('tab', 'overall')
    if tab not in {'overall', 'valkyrie', 'valhalla'}:
        tab = 'overall'

    overall_pending = list(
        UniversalPowerRank.objects.select_related('character')
        .filter(pending_changes__isnull=False)
        .exclude(pending_changes='')
        .order_by('-gear_score')
    )
    if overall_pending:
        names = ", ".join(pr.character.name for pr in overall_pending[:5])
        extra = "" if len(overall_pending) <= 5 else f" and {len(overall_pending) - 5} more"
        messages.error(
            request,
            f"Spot Rank snapshot cannot be updated while the Overall ranking still has pending UPDATE entries: {names}{extra}."
        )
        return redirect(f"/portal/power-rank/?tab={tab}")

    snapshot_data, overflow_count = _build_power_rank_snapshot(tab)
    snapshot, _ = PowerRankFarmSnapshot.objects.get_or_create(tab=tab)
    snapshot.snapshot_data = snapshot_data
    snapshot.updated_by = request.user
    snapshot.save()

    messages.success(
        request,
        f"Spot Rank snapshot for {tab.title()} updated successfully. "
        f"{len(snapshot_data)} validated members saved" + (f", {overflow_count} validated members outside the map." if overflow_count else ".")
    )
    return redirect(f"/portal/power-rank/?tab={tab}")


@login_required
def edit_power_rank(request, character_pk):
    """
    Edit Universal Power Rank stats for a character.
    Members input their own data.
    """
    character = get_object_or_404(Character, pk=character_pk)

    # Permission check: admin can edit any, user can only edit their own
    if not is_admin(request.user) and character.owner != request.user:
        return HttpResponseForbidden("You can only edit your own characters.")

    power_rank, created = UniversalPowerRank.objects.get_or_create(character=character)

    if request.method == 'POST':
        try:
            original_server = power_rank.server
            original_power_class = power_rank.power_class
            original_level = power_rank.level
            original_dmg = power_rank.dmg
            original_acc = power_rank.acc
            original_defense = power_rank.defense
            original_dmg_reduct = power_rank.dmg_reduct
            original_skill_resist = power_rank.skill_resist
            original_skill_dmg_boost = power_rank.skill_dmg_boost
            original_weapon_dmg_boost = power_rank.weapon_dmg_boost
            original_soulshot = power_rank.soulshot
            original_valor = power_rank.valor
            original_guardian = power_rank.guardian
            original_conquer = power_rank.conquer
            original_duel = power_rank.duel
            original_purple_class_aga = power_rank.purple_class_aga

            power_rank.server = request.POST.get('server', power_rank.server)
            power_rank.power_class = request.POST.get('power_class', '')
            power_rank.level = float(request.POST.get('level', 0) or 0)
            power_rank.dmg = float(request.POST.get('dmg', 0) or 0)
            power_rank.acc = float(request.POST.get('acc', 0) or 0)
            power_rank.defense = float(request.POST.get('defense', 0) or 0)
            power_rank.dmg_reduct = float(request.POST.get('dmg_reduct', 0) or 0)
            power_rank.skill_resist = float(request.POST.get('skill_resist', 0) or 0)
            power_rank.skill_dmg_boost = float(request.POST.get('skill_dmg_boost', 0) or 0)
            power_rank.weapon_dmg_boost = float(request.POST.get('weapon_dmg_boost', 0) or 0)
            power_rank.soulshot = float(request.POST.get('soulshot', 0) or 0)
            power_rank.valor = float(request.POST.get('valor', 0) or 0)
            power_rank.guardian = float(request.POST.get('guardian', 0) or 0)
            power_rank.conquer = float(request.POST.get('conquer', 0) or 0)
            power_rank.duel = float(request.POST.get('duel', 0) or 0)
            power_rank.purple_class_aga = float(request.POST.get('purple_class_aga', 0) or 0)

            change_logs = []
            if original_server != power_rank.server: change_logs.append(f"Server: {original_server} -> {power_rank.server}")
            if original_power_class != power_rank.power_class: change_logs.append(f"Class: {original_power_class} -> {power_rank.power_class}")
            if original_level != power_rank.level: change_logs.append(f"Level: {int(original_level)} -> {int(power_rank.level)}")
            if original_dmg != power_rank.dmg: change_logs.append(f"DMG: {int(original_dmg)} -> {int(power_rank.dmg)}")
            if original_acc != power_rank.acc: change_logs.append(f"ACC: {int(original_acc)} -> {int(power_rank.acc)}")
            if original_defense != power_rank.defense: change_logs.append(f"DEF: {int(original_defense)} -> {int(power_rank.defense)}")
            if original_dmg_reduct != power_rank.dmg_reduct: change_logs.append(f"Reduc: {int(original_dmg_reduct)} -> {int(power_rank.dmg_reduct)}")
            if original_skill_resist != power_rank.skill_resist: change_logs.append(f"Skill Resist: {int(original_skill_resist)} -> {int(power_rank.skill_resist)}")
            if original_skill_dmg_boost != power_rank.skill_dmg_boost: change_logs.append(f"Skill DMG: {int(original_skill_dmg_boost)} -> {int(power_rank.skill_dmg_boost)}")
            if original_weapon_dmg_boost != power_rank.weapon_dmg_boost: change_logs.append(f"Wpn DMG: {int(original_weapon_dmg_boost)} -> {int(power_rank.weapon_dmg_boost)}")
            if original_soulshot != power_rank.soulshot: change_logs.append(f"SS: {original_soulshot:.1f} -> {power_rank.soulshot:.1f}")
            if original_valor != power_rank.valor: change_logs.append(f"Valor: {original_valor:.1f} -> {power_rank.valor:.1f}")
            if original_guardian != power_rank.guardian: change_logs.append(f"Guardian: {original_guardian:.1f} -> {power_rank.guardian:.1f}")
            if original_conquer != power_rank.conquer: change_logs.append(f"Conq: {original_conquer:.1f} -> {power_rank.conquer:.1f}")
            if original_duel != power_rank.duel: change_logs.append(f"Duel: {original_duel:.1f} -> {power_rank.duel:.1f}")
            if original_purple_class_aga != power_rank.purple_class_aga: change_logs.append(f"Purple: {int(original_purple_class_aga)} -> {int(power_rank.purple_class_aga)}")

            # Handle multiple stat screenshot uploads (max 2MB each)
            from .models import PowerRankScreenshot
            uploaded_files = request.FILES.getlist('stat_screenshots')
            valid_uploads = 0
            for uploaded in uploaded_files:
                if uploaded.size > 2 * 1024 * 1024:  # 2MB limit
                    messages.error(request, f"'{uploaded.name}' too large! Max 2MB per file.")
                else:
                    PowerRankScreenshot.objects.create(
                        power_rank=power_rank,
                        image=uploaded
                    )
                    valid_uploads += 1

            # Handle screenshot removal (individual by ID) - kept for backward compat
            delete_ids = request.POST.getlist('delete_screenshots')
            if delete_ids:
                PowerRankScreenshot.objects.filter(
                    id__in=delete_ids,
                    power_rank=power_rank
                ).delete()
                
            if valid_uploads > 0: change_logs.append(f"Uploaded {valid_uploads} new screenshots")
            if delete_ids: change_logs.append(f"Deleted {len(delete_ids)} screenshots")

            # If member uploads new screenshot OR changes any stat, clear validation status
            if change_logs:
                power_rank.is_validated = False
                power_rank.validation_notes = None
                
                # Replace pending changes with latest changes only
                power_rank.pending_changes = " | ".join(change_logs)

            # Validate: must have at least 1 screenshot after save
            remaining_count = power_rank.screenshots.count()
            if remaining_count == 0:
                messages.error(request, "Screenshot wajib! Upload minimal 1 screenshot In-Game Stat sebagai bukti.")
                context = {
                    'character': character,
                    'power_rank': power_rank,
                    'screenshots': power_rank.screenshots.all(),
                    'server_choices': [('K1', 'K1'), ('K5', 'K5'), ('K9', 'K9'), ('T8', 'T8')],
                }
                return render(request, 'items/power_rank_form.html', context)

            power_rank.save()  # gear_score auto-calculated in save()
            messages.success(request, f"Power stats for {character.name} updated successfully!")
            return redirect('power-rank-leaderboard')
        except (ValueError, TypeError) as e:
            messages.error(request, f"Invalid input: {e}")

    context = {
        'character': character,
        'power_rank': power_rank,
        'screenshots': power_rank.screenshots.all(),
        'server_choices': [('K1', 'K1'), ('K5', 'K5'), ('K9', 'K9'), ('T8', 'T8')],
    }
    return render(request, 'items/power_rank_form.html', context)


@login_required
@require_http_methods(["POST"])
def delete_power_rank_screenshot(request):
    """
    AJAX endpoint: Instantly delete a power rank screenshot.
    Super admin can delete any, users can only delete their own.
    """
    from django.http import JsonResponse
    from .models import PowerRankScreenshot

    screenshot_id = request.POST.get('screenshot_id')
    if not screenshot_id:
        return JsonResponse({'error': 'No screenshot_id provided'}, status=400)

    screenshot = get_object_or_404(PowerRankScreenshot, pk=screenshot_id)
    character = screenshot.power_rank.character

    # Permission check: Super Admin, Power Rank Admin, or Owner
    is_pr_admin = False
    if request.user.is_authenticated:
        from dkp.models import AdminRole
        role = AdminRole.objects.filter(user=request.user).first()
        if role and role.is_powerrank_admin:
            is_pr_admin = True

    if not (is_admin(request.user) or is_pr_admin) and character.owner != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # Check if this is the last screenshot - don't allow deletion
    remaining = screenshot.power_rank.screenshots.count()
    if remaining <= 1:
        return JsonResponse({'error': 'Tidak bisa hapus! Minimal 1 screenshot wajib ada.'}, status=400)

    # Delete the file and record
    screenshot.image.delete(save=False)
    screenshot.delete()

    return JsonResponse({'success': True, 'remaining': remaining - 1})

@login_required
@require_http_methods(["POST"])
def update_power_rank_validation(request):
    """
    AJAX endpoint: Update power rank validation status. Admin only.
    """
    from django.http import JsonResponse
    # Permission: Super Admin or Power Rank Admin
    is_pr_admin = False
    if request.user.is_authenticated:
        from dkp.models import AdminRole
        role = AdminRole.objects.filter(user=request.user).first()
        if role and role.is_powerrank_admin:
            is_pr_admin = True
            
    if not (is_admin(request.user) or is_pr_admin):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    pk = request.POST.get('pk')
    is_validated = request.POST.get('is_validated') == 'true'
    notes = request.POST.get('validation_notes', '')

    if not pk:
        return JsonResponse({'error': 'No PK provided'}, status=400)

    power_rank = get_object_or_404(UniversalPowerRank, pk=pk)
    power_rank.is_validated = is_validated
    power_rank.validation_notes = notes
    if is_validated:
        power_rank.pending_changes = ""
    power_rank.save()

    return JsonResponse({'success': True})


# ======================================================
# HALL OF FAME VIEW
# ======================================================
from .models import HallOfFame

def hall_of_fame_view(request):
    members = HallOfFame.objects.filter(is_active=True).order_for_presentation() if hasattr(HallOfFame.objects, 'order_for_presentation') else HallOfFame.objects.filter(is_active=True).order_by('-contribution', 'name')
    context = {
        'members': members,
    }
    return render(request, 'items/hall_of_fame.html', context)

# ======================================================
# HALL OF FAME MANAGEMENT (ADMIN)
# ======================================================
@login_required
def manage_hall_of_fame(request):
    if not request.user.is_staff and not request.user.groups.filter(name='Sub Admin').exists():
        messages.error(request, 'You do not have permission to manage the Hall of Fame.')
        return redirect('item-list')
        
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "add":
            name = request.POST.get('name')
            rank = request.POST.get('rank')
            clan = request.POST.get('clan')
            contribution = request.POST.get('contribution', 0)
            image = request.FILES.get('image')
            
            if image and image.size > 2 * 1024 * 1024:
                messages.error(request, 'Image file size must be under 2MB.')
                return redirect('manage-hall-of-fame')
            
            if name:
                HallOfFame.objects.create(
                    name=name,
                    rank=rank,
                    clan=clan,
                    contribution=contribution,
                    image=image
                )
                messages.success(request, f"Successfully added {name} to Hall of Fame!")
            return redirect('manage-hall-of-fame')
            
        elif action == "delete":
            pk = request.POST.get('member_id')
            member = get_object_or_404(HallOfFame, pk=pk)
            member.delete()
            messages.success(request, "Member successfully deleted from Hall of Fame.")
            return redirect('manage-hall-of-fame')
            
    members = HallOfFame.objects.all().order_by('-created_at')
    from items.models import Character
    characters = Character.objects.values_list('name', flat=True).order_by('name')
    context = {
        'members': members,
        'characters': characters,
    }
    return render(request, 'items/manage_hall_of_fame.html', context)


# ======================================================
# SOUL PAGE (RAID BOSS SOULS)
# ======================================================
from .models import CharacterSoul, CharacterSoulProof

def _is_soul_admin(user):
    if is_admin(user):
        return True
    from dkp.models import AdminRole
    role = AdminRole.objects.filter(user=user).first()
    return role and role.is_soul_admin

@login_required
def soul_page(request):
    """Soul page - shows raid boss souls for all members"""
    clan_filter = request.GET.get('clan', 'Valkyrie')
    
    from django.db.models.functions import Coalesce
    from django.db.models import Value
    characters = Character.objects.all().annotate(
        pr_score=Coalesce('power_rank__gear_score', Value(0))
    ).order_by('-pr_score', 'name')
    if clan_filter == 'Valkyrie':
        characters = characters.filter(clan='Valkyrie')
    elif clan_filter == 'Valhalla':
        characters = characters.filter(clan='Valhalla')
    # If Overall, no filtering by clan
    
    # Get all souls grouped by character
    all_souls = CharacterSoul.objects.select_related('character').all()
    soul_map = {}
    for soul in all_souls:
        if soul.character_id not in soul_map:
            soul_map[soul.character_id] = {}
        soul_map[soul.character_id][soul.boss_name] = {
            'id': soul.id,
            'is_verified': soul.is_verified,
        }
    
    # Get all soul proofs grouped by character
    all_proofs = CharacterSoulProof.objects.select_related('character').all()
    proof_map = {}
    for proof in all_proofs:
        if proof.character_id not in proof_map:
            proof_map[proof.character_id] = []
        proof_map[proof.character_id].append({
            'id': proof.id,
            'url': proof.image.url,
        })
    
    # Build boss list grouped by category
    boss_groups = [
        {
            'name': 'Raid Boss',
            'bosses': sorted([
                'Chertuba', 'Kelsus', 'Basilla', 'Savan', 'Tromba',
                'Felis', 'Sarka', 'Timitris', 'Talakin', 'Enkura',
                'Contaminated Cruma', 'Katan', 'Stonegheist', 'Pan Dryad', 'Gahareth', 'Valefal',
                'Breka', 'Medusa', 'Pan Narod', 'Matura', 'Black Lily', 'Behemoth',
                'Balbo', 'Talkin', 'Timiniel', 'Selu', 'Repiro', 'Coroon', 'Samuel',
                'Hisilrome', 'Mirror of Oblivion', 'Randor', 'Glaki', 'Cabrio', 'Flynt', 'Haff',
                'Phoenix', 'Andras', 'Thanatos', 'Rahha',
            ]),
        },
        {
            'name': 'Territory Boss',
            'bosses': sorted(['Queen Ant', 'Mutated Cruma', 'Core Susceptor', 'Dragon Beast', 'Orfen', 'Olkuth']),
        },
        {
            'name': 'World Boss',
            'bosses': sorted([
                'Shila', 'Moof', 'Normus', 'Ukanba', 'Selihoden',
                'Ramdal', 'Mardil', 'Kernon', 'Tarim', 'Halate', 'Vella', 'Shuriel', 'Galaxia',
            ]),
        },
        {
            'name': 'Arena Boss',
            'bosses': sorted(['Anaxa', 'Kustor']),
        },
    ]
    
    all_bosses = []
    for group in boss_groups:
        all_bosses.extend(group['bosses'])
    
    # Build character data with soul info
    char_data = []
    for char in characters:
        souls = soul_map.get(char.id, {})
        proofs = proof_map.get(char.id, [])
        total = len(all_bosses)
        owned = sum(1 for b in all_bosses if b in souls and souls[b]['is_verified'])
        char_data.append({
            'character': char,
            'souls': souls,
            'proofs': proofs,
            'total': total,
            'owned': owned,
            'verified_bosses': sorted([b for b in all_bosses if b in souls and souls[b]['is_verified']]),
            'pending_bosses': sorted([b for b in all_bosses if b in souls and not souls[b]['is_verified']]),
            'all_soul_bosses': sorted([b for b in all_bosses if b in souls]),
        })
    
    # Get current user's soul count
    user_soul_count = 0
    user_chars = Character.objects.filter(owner=request.user)
    for uc in user_chars:
        uc_souls = soul_map.get(uc.id, {})
        user_soul_count += sum(1 for s in uc_souls.values() if s['is_verified'])
    
    # Collect unverified members for admin
    unverified_names = set()
    is_admin_user = _is_soul_admin(request.user)
    if is_admin_user:
        for soul in all_souls:
            if not soul.is_verified:
                unverified_names.add(soul.character.name)
    unverified_names = sorted(list(unverified_names))
    
    # User's own characters for the update button
    user_characters = Character.objects.filter(owner=request.user)
    
    # Build JSON-safe boss data for the modal
    import json
    boss_groups_json = json.dumps(boss_groups)
    
    # Build data for user's own characters (for the universal update buttons)
    user_char_data = []
    for uc in user_characters:
        souls = soul_map.get(uc.id, {})
        proofs = proof_map.get(uc.id, [])
        user_char_data.append({
            'character_pk': uc.pk,
            'character_name': uc.name,
            'souls': souls,
            'proofs': proofs,
        })
    
    context = {
        'char_data': char_data,
        'user_char_data': user_char_data,  # Essential for universal update
        'boss_groups': boss_groups,
        'boss_groups_json': boss_groups_json,
        'all_bosses': all_bosses,
        'clan_filter': clan_filter,
        'is_admin': is_admin_user,
        'user_soul_count': user_soul_count,
        'unverified_names': unverified_names,
        'user_characters': user_characters,
    }
    return render(request, 'items/soul_page.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_soul(request):
    """AJAX: Toggle a soul for a character (add/remove). Simple toggle."""
    import json
    data = json.loads(request.body)
    character_id = data.get('character_id')
    boss_name = data.get('boss_name')
    
    character = get_object_or_404(Character, pk=character_id)
    
    # Permission: soul admin can toggle any, user can only toggle their own
    if not _is_soul_admin(request.user) and character.owner != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Requirement: Must have at least 1 proof to toggle (unless admin)
    if not _is_soul_admin(request.user) and not character.soul_proofs.exists():
        return JsonResponse({'error': 'Proof Required: You must upload at least one screenshot of your soul collection before you can mark any boss souls.'}, status=400)
    
    soul, created = CharacterSoul.objects.get_or_create(
        character=character,
        boss_name=boss_name,
        defaults={'is_verified': False}
    )
    
    if not created:
        soul.delete()
        return JsonResponse({'success': True, 'action': 'removed'})
    
    return JsonResponse({'success': True, 'action': 'added', 'soul_id': soul.id})


@login_required
@require_http_methods(["POST"])
def upload_soul_proof(request):
    """AJAX: Upload a soul collection screenshot as proof for all bosses"""
    character_id = request.POST.get('character_id')
    screenshot = request.FILES.get('screenshot')
    
    if not screenshot:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    character = get_object_or_404(Character, pk=character_id)
    
    if not _is_soul_admin(request.user) and character.owner != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    proof = CharacterSoulProof.objects.create(character=character, image=screenshot)
    
    return JsonResponse({'success': True, 'proof_id': proof.id, 'proof_url': proof.image.url})


@login_required
@require_http_methods(["POST"])
def delete_soul_proof(request):
    """AJAX: Delete a soul proof screenshot"""
    import json
    data = json.loads(request.body)
    proof_id = data.get('proof_id')
    
    proof = get_object_or_404(CharacterSoulProof, pk=proof_id)
    
    if not _is_soul_admin(request.user) and proof.character.owner != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    proof.image.delete(save=False)
    proof.delete()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def verify_soul(request):
    """AJAX: Admin or Soul Admin verifies/unverifies a soul"""
    if not _is_soul_admin(request.user):
        return JsonResponse({'error': 'Admin only'}, status=403)
    
    import json
    data = json.loads(request.body)
    soul_id = data.get('soul_id')
    
    soul = get_object_or_404(CharacterSoul, pk=soul_id)
    soul.is_verified = not soul.is_verified
    soul.save()
    
    return JsonResponse({'success': True, 'is_verified': soul.is_verified})


@login_required
@require_http_methods(["POST"])
def bulk_verify_souls(request):
    """AJAX: Admin or Soul Admin bulk verify/unverify all souls for a character"""
    if not _is_soul_admin(request.user):
        return JsonResponse({'error': 'Admin only'}, status=403)
    
    import json
    data = json.loads(request.body)
    character_id = data.get('character_id')
    action = data.get('action', 'verify')
    
    character = get_object_or_404(Character, pk=character_id)
    souls = CharacterSoul.objects.filter(character=character)
    
    if action == 'verify':
        souls.update(is_verified=True)
    else:
        souls.update(is_verified=False)
    
    return JsonResponse({'success': True, 'action': action, 'count': souls.count()})


@login_required
@require_http_methods(["POST"])
def batch_update_souls(request):
    """AJAX: Batch update all souls for a character. Requires proof image upload.
    Accepts multipart form: character_id, screenshot (file), boss_names (JSON array of boss names checked).
    """
    import json
    character_id = request.POST.get('character_id')
    screenshot = request.FILES.get('screenshot')
    boss_names_json = request.POST.get('boss_names', '[]')
    
    try:
        boss_names = json.loads(boss_names_json)
    except (json.JSONDecodeError, TypeError):
        boss_names = []
    
    if not character_id:
        return JsonResponse({'error': 'No character specified'}, status=400)
    
    character = get_object_or_404(Character, pk=character_id)
    
    # Permission check
    if not _is_soul_admin(request.user) and character.owner != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Regular user must have at least one proof (new or existing)
    if not screenshot and not _is_soul_admin(request.user) and not character.soul_proofs.exists():
        return JsonResponse({'error': 'Proof screenshot is required.'}, status=400)
    
    # 1. Save proof image (only if provided)
    proof = None
    if screenshot:
        proof = CharacterSoulProof.objects.create(character=character, image=screenshot)
    
    # 2. Sync souls: add new ones, remove unchecked ones
    existing_souls = CharacterSoul.objects.filter(character=character)
    existing_boss_set = set(existing_souls.values_list('boss_name', flat=True))
    new_boss_set = set(boss_names)
    
    is_admin = _is_soul_admin(request.user)

    if is_admin:
        # Admin mode: Ensure all checked bosses exist and are verified
        for boss in new_boss_set:
            soul, created = CharacterSoul.objects.get_or_create(
                character=character, boss_name=boss,
                defaults={'is_verified': True}
            )
            if not soul.is_verified:
                soul.is_verified = True
                soul.save()
        
        # Remove unchecked bosses (admin can remove anything)
        to_remove = existing_boss_set - new_boss_set
        CharacterSoul.objects.filter(character=character, boss_name__in=to_remove).delete()
        
        added_count = len(new_boss_set - existing_boss_set)
        removed_count = len(to_remove)
    else:
        # User mode:
        # 1. Add new bosses as unverified
        to_add = new_boss_set - existing_boss_set
        for boss in to_add:
            CharacterSoul.objects.create(character=character, boss_name=boss, is_verified=False)
        
        # 2. Remove unchecked bosses (only if they were not already verified)
        to_remove = existing_boss_set - new_boss_set
        removed_souls = CharacterSoul.objects.filter(
            character=character, 
            boss_name__in=to_remove, 
            is_verified=False
        )
        removed_count = removed_souls.count()
        removed_souls.delete()
        added_count = len(to_add)

    return JsonResponse({
        'success': True,
        'added': added_count,
        'removed': removed_count,
        'proof_id': proof.id if proof else None,
        'proof_url': proof.image.url if proof else None,
    })

def check_raidboss_admin(user):
    """Check if user is allowed to manage raid boss (SuperAdmin or RaidBossAdmin)"""
    if is_admin(user):
        return True
    try:
        return getattr(user, 'admin_role', None) and user.admin_role.is_raidboss_admin
    except Exception:
        return False

@login_required(login_url='/login/')
def raid_boss_activity(request):
    if not check_raidboss_admin(request.user):
        return HttpResponseForbidden("You do not have access to manage Activity.")
    
    from items.models import ActivityEvent, PlayerActivity, Character
    from django.utils import timezone
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            name = request.POST.get('name', '').strip()
            boss_type = request.POST.get('boss_type', '').strip()
            value = request.POST.get('value')
            participant_ids = request.POST.getlist('participant_ids')
            is_war_day = request.POST.get('war_day') == 'on'
            activity_note = request.POST.get('activity_note', '').strip()

            if name and value:
                try:
                    points = int(value)
                except (ValueError, TypeError):
                    points = 0
                
                # Apply War Day multiplier
                if is_war_day:
                    points = points * 2

                final_name = f"[{boss_type}] {name}" if boss_type else name
                if is_war_day:
                    final_name = f"⚔️ War Day: {final_name}"

                # Create ActivityEvent
                activity_event = ActivityEvent.objects.create(
                    name=final_name,
                    event_type='CUSTOM',
                    date=timezone.now(),
                    base_points=points,
                    max_points=points,
                    is_completed=True,
                    is_finalized=True,
                    description=activity_note,
                    input_by=request.user
                )

                if participant_ids and points > 0:
                    for pid in participant_ids:
                        try:
                            character = Character.objects.get(id=int(pid))
                            PlayerActivity.objects.create(
                                player=character,
                                event=activity_event,
                                status='ATTENDED',
                                points_earned=points,
                            )
                        except (Character.DoesNotExist, ValueError):
                            pass

        elif action == 'delete':
            event_id = request.POST.get('event_id')
            ActivityEvent.objects.filter(id=event_id).delete()

        elif action == 'update':
            event_id = request.POST.get('event_id')
            name = request.POST.get('name', '').strip()
            boss_type = request.POST.get('boss_type', '').strip()
            value = request.POST.get('value')
            participant_ids = request.POST.getlist('participant_ids')
            is_war_day = request.POST.get('war_day') == 'on'
            activity_note = request.POST.get('activity_note', '').strip()

            activity_event = ActivityEvent.objects.filter(id=event_id, event_type='CUSTOM').first()
            if activity_event and name and value:
                try:
                    points = int(value)
                except (ValueError, TypeError):
                    points = 0

                if is_war_day:
                    points = points * 2

                final_name = f"[{boss_type}] {name}" if boss_type else name
                if is_war_day:
                    final_name = f"⚔️ War Day: {final_name}"

                activity_event.name = final_name
                activity_event.base_points = points
                activity_event.max_points = points
                activity_event.description = activity_note
                activity_event.save()

                activity_event.participants.all().delete()
                if participant_ids and points > 0:
                    for pid in participant_ids:
                        try:
                            character = Character.objects.get(id=int(pid))
                            PlayerActivity.objects.create(
                                player=character,
                                event=activity_event,
                                status='ATTENDED',
                                points_earned=points,
                            )
                        except (Character.DoesNotExist, ValueError):
                            pass

        elif action == 'bulk_delete':
            event_ids_str = request.POST.get('event_ids', '')
            if event_ids_str:
                ids = [int(x.strip()) for x in event_ids_str.split(',') if x.strip().isdigit()]
                if ids:
                    ActivityEvent.objects.filter(id__in=ids).delete()

        return redirect('raid-boss-activity')
            
    # Only show CUSTOM events with boss type prefix (from Raid Boss page)
    from django.db.models import Q
    raid_boss_prefixes_q = Q()
    for prefix in ['[Raid Boss]', '[Territory Boss]', '[World Boss]', '[Rift Boss]', '[Arena Boss]']:
        raid_boss_prefixes_q |= Q(name__contains=prefix)
    all_events = ActivityEvent.objects.filter(
        Q(event_type='CUSTOM') & (raid_boss_prefixes_q | Q(name__contains='War Day:'))
    ).exclude(name__startswith='Score Adjustment:').exclude(name__startswith='AP Adjustment:').prefetch_related('participants__player').order_by('-date')
    from django.core.paginator import Paginator
    paginator = Paginator(all_events, 20)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    boss_type_to_tab = {
        'Raid Boss': 'raid',
        'Territory Boss': 'territory',
        'World Boss': 'world',
        'Rift Boss': 'rift',
        'Arena Boss': 'arena',
    }
    for event in events:
        clean_name = event.name
        is_war_day = 'War Day:' in clean_name
        if is_war_day:
            clean_name = clean_name.split('War Day:', 1)[1].strip()

        boss_type = ''
        boss_name = clean_name
        if clean_name.startswith('[') and ']' in clean_name:
            boss_type = clean_name[1:clean_name.index(']')]
            boss_name = clean_name[clean_name.index(']') + 1:].strip()

        event.edit_boss_type = boss_type
        event.edit_boss_name = boss_name
        event.edit_tab = boss_type_to_tab.get(boss_type, 'raid')
        event.edit_is_war_day = is_war_day
        event.edit_base_points = event.base_points // 2 if is_war_day else event.base_points
        event.edit_participant_ids = json.dumps([
            act.player_id for act in event.participants.all()
        ])
    
    profiles = Character.objects.all().order_by('name')
    return render(request, 'items/raid_boss_activity.html', {
        'events': events,
        'profiles': profiles,
        'is_super_admin': is_admin(request.user),
    })


# ============================================================
# WAR POINT SYSTEM
# ============================================================

from django.views.decorators.csrf import csrf_exempt

_EASYOCR_READER = None


def _get_easyocr_reader():
    """
    Lazily load EasyOCR once per Django worker. Loading the model on every scan
    makes OCR requests much slower, especially on CPU-only Windows machines.
    """
    global _EASYOCR_READER
    if _EASYOCR_READER is None:
        import easyocr
        _EASYOCR_READER = easyocr.Reader(['en'], gpu=False, verbose=False)
    return _EASYOCR_READER


def _scan_party_members_from_image(image_file):
    """
    Read party screenshot and return grouped party data plus a flat detected name list.
    Supports cropped screenshots where Party 1-4 headers are missing but Party 5-8
    headers are visible.
    """
    import numpy as np
    from PIL import Image, ImageOps
    import re

    img = ImageOps.exif_transpose(Image.open(image_file)).convert('RGB')
    img_np = np.array(img)
    img_width, img_height = img.size
    character_name_lookup = {
        name.lower(): name
        for name in Character.objects.values_list('name', flat=True)
    }

    def _fuzzy_match_name(name):
        """Try exact match first, then fuzzy match against all registered character names."""
        from difflib import SequenceMatcher
        name_lower = name.lower().strip()
        # Exact match
        if name_lower in character_name_lookup:
            return character_name_lookup[name_lower]
        # Fuzzy match — find best match above threshold
        best_match = None
        best_ratio = 0.0
        for db_name_lower, db_name_original in character_name_lookup.items():
            ratio = SequenceMatcher(None, name_lower, db_name_lower).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = db_name_original
        # Threshold 0.75 (75% similarity) — high enough to avoid false positives
        if best_match and best_ratio >= 0.75:
            return best_match
        return name

    def normalize_member_name(name):
        return _fuzzy_match_name(name)

    reader = _get_easyocr_reader()
    results = reader.readtext(img_np, detail=1, paragraph=False)

    if not results:
        return {
            'success': False,
            'error': 'No text detected in image',
            'status': 400,
        }

    text_items = []
    for coords, text, confidence in results:
        center_x = sum(p[0] for p in coords) / 4
        center_y = sum(p[1] for p in coords) / 4
        text_items.append({
            'text': text.strip(),
            'x': center_x,
            'y': center_y,
            'confidence': confidence
        })

    text_items.sort(key=lambda t: (t['y'], t['x']))

    party_pattern = re.compile(r'[Pp]art[yv]\s*(\d+)', re.IGNORECASE)
    party_headers = []
    other_texts = []

    for item in text_items:
        match = party_pattern.search(item['text'])
        if match:
            party_headers.append({
                'party_number': int(match.group(1)),
                'x': item['x'],
                'y': item['y']
            })
        else:
            other_texts.append(item)

    party_headers.sort(key=lambda p: (p['y'], p['x']))

    header_rows = []
    for header in party_headers:
        for row in header_rows:
            if abs(row['y'] - header['y']) <= 40:
                row['headers'].append(header)
                row['y'] = sum(h['y'] for h in row['headers']) / len(row['headers'])
                break
        else:
            header_rows.append({'y': header['y'], 'headers': [header]})

    for row in header_rows:
        row['headers'].sort(key=lambda p: p['x'])
    header_rows.sort(key=lambda r: r['y'])

    if header_rows:
        first_row = header_rows[0]
        first_numbers = [h['party_number'] for h in first_row['headers']]
        min_number = min(first_numbers)
        row_size = len(first_row['headers'])
        if row_size > 1 and min_number > 1:
            inferred_start = min_number - row_size
            if inferred_start >= 1:
                inferred_headers = []
                for idx, header in enumerate(first_row['headers']):
                    inferred_headers.append({
                        'party_number': inferred_start + idx,
                        'x': header['x'],
                        'y': -1,
                        'inferred': True
                    })
                header_rows.insert(0, {'y': -1, 'headers': inferred_headers, 'inferred': True})

    party_headers = [header for row in header_rows for header in row['headers']]
    party_headers.sort(key=lambda p: p['party_number'])

    if not party_headers:
        names = [normalize_member_name(t['text']) for t in other_texts
                 if len(t['text']) >= 2
                 and not t['text'].replace(' ', '').isdigit()
                 and t['confidence'] > 0.5]
        return {
            'success': True,
            'mode': 'flat',
            'parties': [],
            'all_names': names,
            'raw_count': len(names),
        }

    columns = []
    for row_index, row in enumerate(header_rows):
        row_y = row['y']
        next_row_y = header_rows[row_index + 1]['y'] if row_index + 1 < len(header_rows) else img_height + 1
        for header in row['headers']:
            columns.append({
                'party_number': header['party_number'],
                'x_center': header['x'],
                'y_start': row_y,
                'y_end': next_row_y,
                'members': []
            })

    for item in other_texts:
        text = item['text'].strip()
        if len(text) < 2 or text.replace(' ', '').isdigit():
            continue
        if item['confidence'] < 0.4:
            continue
        skip_words = ['lv', 'level', 'hp', 'mp', 'party', 'guild', 'clan', 'member']
        if text.lower() in skip_words:
            continue

        min_dist = float('inf')
        best_col = None
        for col in columns:
            dist = abs(item['x'] - col['x_center'])
            in_row = item['y'] > col['y_start'] and item['y'] < col['y_end']
            if in_row and dist < min_dist:
                min_dist = dist
                best_col = col

        if best_col is not None:
            best_col['members'].append({
                'name': text,
                'y': item['y'],
                'confidence': round(item['confidence'], 2)
            })

    parties = []
    for col in columns:
        col['members'].sort(key=lambda m: m['y'])
        party_data = {
            'party_number': col['party_number'],
            'members': []
        }
        for i, member in enumerate(col['members']):
            party_data['members'].append({
                'name': normalize_member_name(member['name']),
                'is_leader': i == 0,
                'confidence': member['confidence']
            })
        parties.append(party_data)

    all_names = [member['name'] for party in parties for member in party['members']]
    return {
        'success': True,
        'mode': 'structured',
        'parties': parties,
        'all_names': all_names,
        'total_parties': len(parties),
        'total_players': len(all_names),
        'raw_texts': [t['text'] for t in text_items[:50]],
    }


@login_required
@require_http_methods(["POST"])
def analyze_war_image(request):
    """
    API Endpoint to scan image via EasyOCR and return detected Date, Kills, Assists.
    Called via AJAX when player selects an image.
    """
    screenshot = request.FILES.get('screenshot')
    if not screenshot:
        return JsonResponse({'error': 'No image provided'}, status=400)
        
    try:
        import numpy as np
        from PIL import Image, ImageOps
        import re
        
        # Load the image
        img = ImageOps.exif_transpose(Image.open(screenshot)).convert('RGB')
        img_np = np.array(img)
        
        # Read text
        reader = _get_easyocr_reader()
        results = reader.readtext(img_np, detail=1, paragraph=False)
        extracted_texts = [text for _coords, text, _confidence in results]
        
        # 1. Find Date (Format YYYY.MM.DD)
        # Regex to match 2026.05.04 or similar, allowing spaces or typos in dots
        date_pattern = re.compile(r'20\d{2}[.\- ]\d{2}[.\- ]\d{2}')
        found_date = ""
        
        # 2. Count Kills and Assists
        ocr_kill_count = 0
        ocr_assist_count = 0
        
        for text in extracted_texts:
            # Check for date
            if not found_date:
                match = date_pattern.search(text)
                if match:
                    # Clean up to standard format YYYY-MM-DD
                    raw_date = match.group()
                    clean_date = raw_date.replace('.', '-').replace(' ', '-')
                    found_date = clean_date
            
            # Check for kill/assist (more forgiving string matching)
            text_lower = text.lower()
            # Remove all spaces and common symbols to improve match
            clean_text = re.sub(r'[^a-z]', '', text_lower)
            
            if 'kill' in clean_text or 'kil' in clean_text or 'kll' in clean_text:
                # To prevent matching random words, make sure the box literally says "Kill" or similar
                if len(clean_text) <= 5: # "kill" is 4 chars, allow a little noise
                    ocr_kill_count += 1
            if 'assist' in clean_text or 'asist' in clean_text or 'assis' in clean_text:
                if len(clean_text) <= 7: # "assist" is 6 chars
                    ocr_assist_count += 1
                
        return JsonResponse({
            'success': True,
            'date': found_date,
            'kills': ocr_kill_count,
            'assists': ocr_assist_count,
            'raw_texts': extracted_texts[:20] # For debug if needed
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def war_point_page(request, sub_id=None):
    """
    Main War Point page - Leaderboard + Player's own submissions
    """
    from django.db.models import Sum, Count
    from datetime import date, timedelta
    
    config = WarPointConfig.get_config()
    user_characters = Character.objects.filter(owner=request.user)
    from .models import WarWorld
    worlds = WarWorld.objects.all()
    
    edit_sub = None
    if sub_id:
        edit_sub = get_object_or_404(WarPointSubmission, pk=sub_id, character__owner=request.user)
        if edit_sub.status == 'APPROVED':
            messages.error(request, 'Cannot edit an approved submission.')
            return redirect('war-point')

    # Handle submission
    if request.method == 'POST':
        character_id = request.POST.get('character')
        world_id = request.POST.get('world')
        server = request.POST.get('server')
        screenshots = request.FILES.getlist('screenshot')
        
        kill_top1 = int(request.POST.get('kill_top1', 0) or 0)
        assist_top1 = int(request.POST.get('assist_top1', 0) or 0)
        kill_top2 = int(request.POST.get('kill_top2', 0) or 0)
        assist_top2 = int(request.POST.get('assist_top2', 0) or 0)
        kill_top3 = int(request.POST.get('kill_top3', 0) or 0)
        assist_top3 = int(request.POST.get('assist_top3', 0) or 0)
        kill_top4 = int(request.POST.get('kill_top4', 0) or 0)
        assist_top4 = int(request.POST.get('assist_top4', 0) or 0)
        kill_top5 = int(request.POST.get('kill_top5', 0) or 0)
        assist_top5 = int(request.POST.get('assist_top5', 0) or 0)
        kill_normal = int(request.POST.get('kill_normal', 0) or 0)
        assist_normal = int(request.POST.get('assist_normal', 0) or 0)
        
        if not character_id or not world_id or not server:
            messages.error(request, 'Please fill in all fields.')
            return redirect('war-point')
            
        if not sub_id and not screenshots:
            messages.error(request, 'Please upload a screenshot.')
            return redirect('war-point')
        
        character = get_object_or_404(Character, pk=character_id, owner=request.user)
        world = get_object_or_404(WarWorld, pk=world_id)
        try:
            server = int(server)
        except ValueError:
            server = 1
        
        from django.utils import timezone
            
        from .models import WarPointProofImage
        if sub_id:
            # Edit existing
            submission = edit_sub
            submission.character = character
            submission.world = world
            submission.server = server
            submission.kill_top1 = kill_top1
            submission.assist_top1 = assist_top1
            submission.kill_top2 = kill_top2
            submission.assist_top2 = assist_top2
            submission.kill_top3 = kill_top3
            submission.assist_top3 = assist_top3
            submission.kill_top4 = kill_top4
            submission.assist_top4 = assist_top4
            submission.kill_top5 = kill_top5
            submission.assist_top5 = assist_top5
            submission.kill_normal = kill_normal
            submission.assist_normal = assist_normal
            submission.status = 'PENDING' # Reset to pending
            submission.calculate_points()
            submission.save()
            
            if screenshots:
                # Replace images if new ones provided
                submission.proof_images.all().delete()
                submission.screenshot = screenshots[0]
                submission.save()
                for img in screenshots:
                    WarPointProofImage.objects.create(submission=submission, image=img)
                    
            messages.success(request, f'Submission updated! ({submission.kill_count} Kills, {submission.assist_count} Assists = {submission.total_points} pts). Status reset to Pending.')
        else:
            # Create new
            submission = WarPointSubmission(
                character=character,
                screenshot=screenshots[0] if screenshots else None,
                world=world,
                server=server,
                kill_top1=kill_top1,
                assist_top1=assist_top1,
                kill_top2=kill_top2,
                assist_top2=assist_top2,
                kill_top3=kill_top3,
                assist_top3=assist_top3,
                kill_top4=kill_top4,
                assist_top4=assist_top4,
                kill_top5=kill_top5,
                assist_top5=assist_top5,
                kill_normal=kill_normal,
                assist_normal=assist_normal,
                admin_notes="",
            )
            submission.calculate_points()
            submission.save()
            
            for img in screenshots:
                WarPointProofImage.objects.create(submission=submission, image=img)
                
            messages.success(request, f'Screenshot submitted successfully! ({submission.kill_count} Kills, {submission.assist_count} Assists = {submission.total_points} pts). Waiting for admin verification.')
            
        return redirect('war-point')
    
    # GET - Leaderboard (this month)
    today = date.today()
    first_day = today.replace(day=1)
    
    leaderboard = (
        WarPointSubmission.objects
        .filter(status='APPROVED', submitted_at__gte=first_day)
        .values('character__name', 'character__clan')
        .annotate(
            total_kills=Sum('kill_count'),
            total_assists=Sum('assist_count'),
            total_points=Sum('total_points'),
            submissions=Count('id'),
        )
        .order_by('-total_points')
    )
    
    # My submissions
    my_submissions = []
    if user_characters.exists():
        my_submissions = WarPointSubmission.objects.filter(
            character__in=user_characters
        ).order_by('-submitted_at')[:30]
    
    has_wp_access = is_admin(request.user)
    if not has_wp_access and getattr(request.user, 'admin_role', None):
        has_wp_access = request.user.admin_role.is_warpoint_admin

    context = {
        'config': config,
        'worlds': worlds,
        'my_submissions': my_submissions,
        'user_characters': user_characters,
        'is_admin_user': has_wp_access,
        'edit_sub': edit_sub,
    }
    return render(request, 'items/war_point.html', context)


@login_required
def war_point_leaderboard(request):
    from django.db.models import Sum, Count
    from datetime import date
    
    today = date.today()
    first_day = today.replace(day=1)
    
    leaderboard = (
        WarPointSubmission.objects
        .filter(status='APPROVED', submitted_at__gte=first_day)
        .values('character__name', 'character__clan')
        .annotate(
            total_kills=Sum('kill_count'),
            total_assists=Sum('assist_count'),
            total_points=Sum('total_points'),
            submissions=Count('id'),
            top1_kills=Sum('kill_top1'),
            top2_kills=Sum('kill_top2'),
            top3_kills=Sum('kill_top3'),
            top4_kills=Sum('kill_top4'),
            top5_kills=Sum('kill_top5'),
            normal_kills=Sum('kill_normal'),
            top1_assists=Sum('assist_top1'),
            top2_assists=Sum('assist_top2'),
            top3_assists=Sum('assist_top3'),
            top4_assists=Sum('assist_top4'),
            top5_assists=Sum('assist_top5'),
            normal_assists=Sum('assist_normal'),
        )
        .order_by('-total_points')
    )
    
    # Calculate Top 2-5 combined for kills and assists
    char_names = [p['character__name'] for p in leaderboard]
    
    # Collect proof images
    submissions = WarPointSubmission.objects.filter(
        character__name__in=char_names,
        status='APPROVED',
        submitted_at__gte=first_day
    ).prefetch_related('proof_images')
    
    char_images = {}
    for sub in submissions:
        name = sub.character.name
        if name not in char_images:
            char_images[name] = []
        if sub.screenshot and hasattr(sub.screenshot, 'url'):
            char_images[name].append(sub.screenshot.url)
        for proof in sub.proof_images.all():
            if proof.image and hasattr(proof.image, 'url'):
                char_images[name].append(proof.image.url)
    
    for p in leaderboard:
        p['top2_5_kills'] = (p['top2_kills'] or 0) + (p['top3_kills'] or 0) + (p['top4_kills'] or 0) + (p['top5_kills'] or 0)
        p['top2_5_assists'] = (p['top2_assists'] or 0) + (p['top3_assists'] or 0) + (p['top4_assists'] or 0) + (p['top5_assists'] or 0)
        p['images'] = char_images.get(p['character__name'], [])
    
    has_wp_access = is_admin(request.user)
    if not has_wp_access and getattr(request.user, 'admin_role', None):
        has_wp_access = request.user.admin_role.is_warpoint_admin
        
    context = {
        'leaderboard': leaderboard,
        'current_month': today.strftime('%B %Y'),
        'is_admin_user': has_wp_access,
    }
    return render(request, 'items/war_point_leaderboard.html', context)


@login_required
def war_point_manage(request):
    """
    Admin page to manage War Point settings and review submissions
    """
    has_access = is_admin(request.user)
    if not has_access and getattr(request.user, 'admin_role', None):
        has_access = request.user.admin_role.is_warpoint_admin
        
    if not has_access:
        return HttpResponseForbidden("Only administrators can access this page.")
    
    from django.utils import timezone
    from .models import WarWorld, WarTargetConfig
    
    config = WarPointConfig.get_config()
    worlds = WarWorld.objects.all()
    
    selected_world_id = request.GET.get('world')
    selected_server = request.GET.get('server', 1)
    
    if selected_world_id:
        selected_world = get_object_or_404(WarWorld, pk=selected_world_id)
    else:
        selected_world = worlds.first()
        
    try:
        selected_server = int(selected_server)
    except ValueError:
        selected_server = 1
        
    target_config = None
    if selected_world:
        target_config, _ = WarTargetConfig.objects.get_or_create(world=selected_world, server=selected_server)
    
    # Handle settings update
    if request.method == 'POST' and 'update_settings' in request.POST:
        world_id_post = request.POST.get('world_id')
        server_post = request.POST.get('server_id')
        
        if world_id_post and server_post:
            tc, _ = WarTargetConfig.objects.get_or_create(world_id=world_id_post, server=server_post)
            tc.top1_name = request.POST.get('top1_name', '')
            tc.top1_kill_points = int(request.POST.get('top1_kill', 100))
            tc.top1_assist_points = int(request.POST.get('top1_assist', 10))
            
            tc.top2_name = request.POST.get('top2_name', '')
            tc.top2_kill_points = int(request.POST.get('top2_kill', 50))
            tc.top2_assist_points = int(request.POST.get('top2_assist', 5))
            
            tc.top3_name = request.POST.get('top3_name', '')
            tc.top3_kill_points = int(request.POST.get('top3_kill', 50))
            tc.top3_assist_points = int(request.POST.get('top3_assist', 5))
            
            tc.top4_name = request.POST.get('top4_name', '')
            tc.top4_kill_points = int(request.POST.get('top4_kill', 50))
            tc.top4_assist_points = int(request.POST.get('top4_assist', 5))
            
            tc.top5_name = request.POST.get('top5_name', '')
            tc.top5_kill_points = int(request.POST.get('top5_kill', 50))
            tc.top5_assist_points = int(request.POST.get('top5_assist', 5))
            tc.save()
            
        try:
            config.normal_kill_points = int(request.POST.get('normal_kill', 10))
            config.normal_assist_points = int(request.POST.get('normal_assist', 2))
            config.auto_delete_days = int(request.POST.get('auto_delete_days', 0))
            config.save()
            messages.success(request, 'War Point settings berhasil diperbarui!')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid input.')
            
        return redirect(f"/portal/war-point/manage/?world={world_id_post}&server={server_post}")
    
    # Auto-cleanup old submissions based on config
    if config.auto_delete_days > 0:
        threshold_date = timezone.now() - timezone.timedelta(days=config.auto_delete_days)
        # Hapus submission yang sudah lewat hari (berdasarkan war_date atau submitted_at, kita pakai submitted_at)
        WarPointSubmission.objects.filter(submitted_at__lt=threshold_date).delete()
    
    # Handle approve/reject
    if request.method == 'POST' and 'review_submission' in request.POST:
        sub_id = request.POST.get('submission_id')
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')
        
        submission = get_object_or_404(WarPointSubmission, pk=sub_id)
        
        if action == 'approve':
            try:
                if 'kill_top1' in request.POST: submission.kill_top1 = int(request.POST.get('kill_top1', submission.kill_top1))
                if 'assist_top1' in request.POST: submission.assist_top1 = int(request.POST.get('assist_top1', submission.assist_top1))
                if 'kill_top2' in request.POST: submission.kill_top2 = int(request.POST.get('kill_top2', submission.kill_top2))
                if 'assist_top2' in request.POST: submission.assist_top2 = int(request.POST.get('assist_top2', submission.assist_top2))
                if 'kill_top3' in request.POST: submission.kill_top3 = int(request.POST.get('kill_top3', submission.kill_top3))
                if 'assist_top3' in request.POST: submission.assist_top3 = int(request.POST.get('assist_top3', submission.assist_top3))
                if 'kill_top4' in request.POST: submission.kill_top4 = int(request.POST.get('kill_top4', submission.kill_top4))
                if 'assist_top4' in request.POST: submission.assist_top4 = int(request.POST.get('assist_top4', submission.assist_top4))
                if 'kill_top5' in request.POST: submission.kill_top5 = int(request.POST.get('kill_top5', submission.kill_top5))
                if 'assist_top5' in request.POST: submission.assist_top5 = int(request.POST.get('assist_top5', submission.assist_top5))
                if 'kill_normal' in request.POST: submission.kill_normal = int(request.POST.get('kill_normal', submission.kill_normal))
                if 'assist_normal' in request.POST: submission.assist_normal = int(request.POST.get('assist_normal', submission.assist_normal))
            except ValueError:
                pass
                
            submission.calculate_points()
            submission.status = 'APPROVED'
            submission.admin_notes = admin_notes
            submission.reviewed_at = timezone.now()
            submission.reviewed_by = request.user
            submission.save()
            
            # Sync to activity if enabled
            if config.sync_to_activity and not submission.synced_to_activity:
                from .models import ActivityEvent, PlayerActivity
                # We won't create an ActivityEvent for war points
                # Instead, directly adjust the player's activity score
                try:
                    char = submission.character
                    # Add points via existing mechanism if available
                    submission.synced_to_activity = True
                    submission.save()
                except Exception:
                    pass
            
            messages.success(request, f'Submission from {submission.character.name} has been APPROVED! (+{submission.total_points} pts)')
            
        elif action == 'reject':
            submission.status = 'REJECTED'
            submission.admin_notes = admin_notes
            submission.reviewed_at = timezone.now()
            submission.reviewed_by = request.user
            submission.save()
            messages.warning(request, f'Submission from {submission.character.name} has been REJECTED.')
        
        return redirect('war-point-manage')
        
    if request.method == 'POST' and request.POST.get('action') == 'bulk_delete':
        sub_ids_str = request.POST.get('submission_ids', '')
        if sub_ids_str:
            ids = [int(x.strip()) for x in sub_ids_str.split(',') if x.strip().isdigit()]
            if ids:
                WarPointSubmission.objects.filter(id__in=ids).delete()
                messages.success(request, f'{len(ids)} War Point submission(s) deleted permanently.')
        
        return redirect('war-point-manage')

    # GET - Show pending submissions + all recent
    pending = WarPointSubmission.objects.filter(status='PENDING').order_by('-submitted_at')
    recent_qs = WarPointSubmission.objects.exclude(status='PENDING').order_by('-reviewed_at')
    
    from django.core.paginator import Paginator
    paginator = Paginator(recent_qs, 20)  # Show 20 records per page
    page_number = request.GET.get('page')
    recent = paginator.get_page(page_number)
    
    from .models import WarTargetConfig
    for sub in pending:
        try:
            sub.target_cfg = WarTargetConfig.objects.get(world=sub.world, server=sub.server)
        except WarTargetConfig.DoesNotExist:
            sub.target_cfg = None
    
    context = {
        'config': config,
        'target_config': target_config,
        'worlds': worlds,
        'selected_world': selected_world,
        'selected_server': selected_server,
        'pending': pending,
        'recent': recent,
    }
    return render(request, 'items/war_point_manage.html', context)


@login_required
def delete_war_point_sub(request, sub_id):
    """
    Allow players to delete their own pending/rejected submissions
    """
    submission = get_object_or_404(WarPointSubmission, pk=sub_id, character__owner=request.user)
    if submission.status == 'APPROVED':
        messages.error(request, 'Cannot delete an approved submission.')
    else:
        submission.delete()
        messages.success(request, 'Submission deleted successfully.')
    return redirect('war-point')

@login_required
def war_point_delete_all(request):
    """
    Admin only: Delete ALL completed war point data (APPROVED + REJECTED)
    """
    has_access = is_admin(request.user)
    if not has_access and getattr(request.user, 'admin_role', None):
        has_access = request.user.admin_role.is_warpoint_admin
        
    if not has_access:
        return HttpResponseForbidden("Only administrators can perform this action.")
        
    if request.method == 'POST':
        qs = WarPointSubmission.objects.filter(status__in=['APPROVED', 'REJECTED'])
        count = qs.count()
        qs.delete()
        messages.success(request, f'Successfully deleted {count} completed War Point submissions & images (Approved + Recent Reviews).')
    return redirect('war-point-leaderboard')

@login_required
def war_point_export_pdf(request):
    """
    Admin only: Export leaderboard as PDF
    """
    from django.http import HttpResponse
    from django.db.models import Sum
    from datetime import date
    import io
    
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    
    has_access = is_admin(request.user)
    if not has_access and getattr(request.user, 'admin_role', None):
        has_access = request.user.admin_role.is_warpoint_admin
        
    if not has_access:
        return HttpResponseForbidden("Only administrators can perform this action.")
    
    today = date.today()
    month_str = today.strftime('%B %Y')
    
    leaderboard = (
        WarPointSubmission.objects
        .filter(status='APPROVED')
        .values('character__name', 'character__clan')
        .annotate(
            total_kills=Sum('kill_count'),
            total_assists=Sum('assist_count'),
            total_points=Sum('total_points'),
            top1_kills=Sum('kill_top1'),
            top2_kills=Sum('kill_top2'),
            top3_kills=Sum('kill_top3'),
            top4_kills=Sum('kill_top4'),
            top5_kills=Sum('kill_top5'),
            normal_kills=Sum('kill_normal'),
            top1_assists=Sum('assist_top1'),
            top2_assists=Sum('assist_top2'),
            top3_assists=Sum('assist_top3'),
            top4_assists=Sum('assist_top4'),
            top5_assists=Sum('assist_top5'),
            normal_assists=Sum('assist_normal'),
        )
        .order_by('-total_points')
    )
    
    # Create PDF (landscape for wider table)
    from reportlab.lib.pagesizes import landscape
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=15*mm, bottomMargin=15*mm, leftMargin=15*mm, rightMargin=15*mm)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=22, textColor=colors.HexColor('#DAA520'), alignment=TA_CENTER, spaceAfter=4*mm)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#888888'), alignment=TA_CENTER, spaceAfter=8*mm)
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#999999'), alignment=TA_CENTER, spaceBefore=10*mm)
    
    elements = []
    
    # Header
    elements.append(Paragraph('⚔ VALKYRIE GUILD', title_style))
    elements.append(Paragraph(f'War Point Leaderboard — {month_str}', subtitle_style))
    
    # Table data
    header_row = ['Rank', 'Player', 'Clan', 'T1 Kill', 'T1 Ast', 'T2-5 Kill', 'T2-5 Ast', 'Norm Kill', 'Norm Ast', 'Total Kill', 'Total Ast', 'Points']
    table_data = [header_row]
    
    for idx, p in enumerate(leaderboard, 1):
        rank_label = f'#{idx}' if idx > 3 else f'#{idx}'
        top2_5_kills = (p['top2_kills'] or 0) + (p['top3_kills'] or 0) + (p['top4_kills'] or 0) + (p['top5_kills'] or 0)
        top2_5_assists = (p['top2_assists'] or 0) + (p['top3_assists'] or 0) + (p['top4_assists'] or 0) + (p['top5_assists'] or 0)
        table_data.append([
            rank_label,
            p['character__name'],
            p['character__clan'] or '-',
            str(p['top1_kills'] or 0),
            str(p['top1_assists'] or 0),
            str(top2_5_kills),
            str(top2_5_assists),
            str(p['normal_kills'] or 0),
            str(p['normal_assists'] or 0),
            str(p['total_kills']),
            str(p['total_assists']),
            str(p['total_points']),
        ])
    
    if len(table_data) == 1:
        elements.append(Paragraph('No data available for this month.', subtitle_style))
    else:
        # 12 columns total: 800 roughly max points across landscape
        col_widths = [35, 110, 80, 45, 45, 55, 55, 55, 55, 60, 55, 55]
        table = Table(table_data, colWidths=col_widths)
        
        # Table style
        style_cmds = [
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#DAA520')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#333333')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#DAA520')),
            
            # Alignment
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (3, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Points column bold + gold (col 11)
            ('FONTNAME', (11, 1), (11, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (11, 1), (11, -1), colors.HexColor('#DAA520')),
            
            # Top 1 Kill (3) - red bold
            ('TEXTCOLOR', (3, 1), (3, -1), colors.HexColor('#C0392B')),
            ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
            # Top 1 Assist (4) - blue
            ('TEXTCOLOR', (4, 1), (4, -1), colors.HexColor('#2980B9')),
            
            # Top 2-5 Kill (5) - orange
            ('TEXTCOLOR', (5, 1), (5, -1), colors.HexColor('#E67E22')),
            # Top 2-5 Assist (6) - blue
            ('TEXTCOLOR', (6, 1), (6, -1), colors.HexColor('#2980B9')),
            
            # Normal Kill (7) - grey
            ('TEXTCOLOR', (7, 1), (7, -1), colors.HexColor('#7F8C8D')),
            # Normal Assist (8) - blue
            ('TEXTCOLOR', (8, 1), (8, -1), colors.HexColor('#2980B9')),
            
            # Total Kill (9) - red
            ('TEXTCOLOR', (9, 1), (9, -1), colors.HexColor('#C0392B')),
            # Total Assist (10) - blue
            ('TEXTCOLOR', (10, 1), (10, -1), colors.HexColor('#2980B9')),
        ]
        
        # Alternating row colors
        for i in range(1, len(table_data)):
            bg = colors.HexColor('#f9f9f9') if i % 2 == 0 else colors.HexColor('#ffffff')
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
        
        # Top 3 highlight
        for i in range(1, min(4, len(table_data))):
            style_cmds.append(('FONTNAME', (0, i), (1, i), 'Helvetica-Bold'))
        
        table.setStyle(TableStyle(style_cmds))
        elements.append(table)
    
    # Footer
    elements.append(Spacer(1, 10*mm))
    elements.append(Paragraph(f'Generated on {today.strftime("%d %B %Y")} • Valkyrie Guild Management System', footer_style))
    
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="war_point_leaderboard_{today.strftime("%Y_%m")}.pdf"'
    return response


@login_required

def check_in_event(request):
    """
    Player page to upload screenshot for checking in.
    """
    import re
    from django.utils import timezone
    from PIL import Image
    
    if request.method == 'POST':
        event_id = request.POST.get('event')
        submitter_id = request.POST.get('submitter')
        image = request.FILES.get('screenshot')
        
        if not event_id or not submitter_id or not image:
            messages.error(request, 'Mohon lengkapi semua data dan upload gambar.')
            return redirect('check-in-event')
            
        event = get_object_or_404(ActivityEvent, pk=event_id)
        submitter = get_object_or_404(Character, pk=submitter_id)
        
        # Check if event is active
        if event.is_completed:
            messages.error(request, 'Event ini sudah selesai.')
            return redirect('check-in-event')
            
        # Create proof record
        proof = EventCheckInProof.objects.create(
            event=event,
            submitter=submitter,
            image=image,
            is_valid=False
        )
        
        # Process OCR
        try:
            import pytesseract
        except ImportError:
            pytesseract = None
        
        try:
            if pytesseract is None:
                raise Exception("Tesseract is not installed - using simulation mode")
            
            # We will open the image and run OCR
            img = Image.open(proof.image.path)
            extracted_text = pytesseract.image_to_string(img)
            proof.extracted_text = extracted_text
            
            # 1. Check token
            token = event.checkin_token
            if not token:
                proof.error_reason = "Event ini tidak membutuhkan verifikasi token."
                proof.save()
            elif token not in extracted_text:
                proof.error_reason = f"Token '{token}' tidak ditemukan di gambar."
                proof.save()
            else:
                # 2. Check Party Members
                # Look for patterns like "1P Name", "2P Name", "3P Name", "4P Name"
                # This regex looks for 1P, 2P, 3P, 4P followed by a space and then a word (the name)
                party_members = []
                # A simple regex to catch party members on the left side
                matches = re.finditer(r'([1-4]P)\s+([A-Za-z0-9_]+)', extracted_text)
                for match in matches:
                    party_members.append(match.group(2))
                
                # Also include submitter just in case 1P is not perfectly caught
                if submitter.name not in party_members:
                    party_members.append(submitter.name)
                    
                # Remove duplicates
                party_members = list(set(party_members))
                proof.detected_party_members = ", ".join(party_members)
                
                if len(party_members) < 2:
                    proof.error_reason = "Party tidak valid. Ditemukan kurang dari 2 anggota party di layar."
                    proof.save()
                else:
                    # Valid! Mark attended
                    proof.is_valid = True
                    proof.save()
                    
                    # Mark attendance for all matched members
                    for member_name in party_members:
                        character = Character.objects.filter(name__iexact=member_name).first()
                        if character:
                            # Create or update activity
                            activity, created = PlayerActivity.objects.get_or_create(
                                player=character,
                                event=event,
                                defaults={
                                    'status': 'ABSENT',
                                    'points_earned': 0
                                }
                            )
                            activity.checkin_verified = True
                            activity.checked_in_at = timezone.now()
                            activity.status = 'ATTENDED' if activity.party_scan_verified else 'ABSENT'
                            activity.save()
                    
                    messages.success(request, f'Sukses! Kehadiran {len(party_members)} member party telah dikonfirmasi.')
                    return redirect('my-activity')
                    
        except Exception as e:
            # Fallback if OCR fails or Tesseract is not installed
            # For demonstration, we will mock it if Tesseract is not found
            if 'tesseract is not installed' in str(e).lower():
                proof.error_reason = "Simulasi: Sukses (Tesseract tidak terinstall, tapi sistem pura-pura sukses untuk demo)."
                proof.is_valid = True
                proof.save()
                
                # Auto-attend submitter for demo
                PlayerActivity.objects.update_or_create(
                    player=submitter,
                    event=event,
                    defaults={
                        'status': 'ABSENT',
                        'points_earned': 0,
                        'checkin_verified': True,
                        'checked_in_at': timezone.now(),
                    }
                )
                messages.warning(request, 'Mode Simulasi: Tesseract tidak terinstall di server. Kehadiran Anda dicatat sebagai simulasi.')
                return redirect('my-activity')
            else:
                proof.error_reason = f"OCR Error: {str(e)}"
                proof.save()
                messages.error(request, 'Gagal memproses gambar. Pastikan kualitas gambar jelas.')
        
        return redirect('check-in-event')

    # GET Request
    active_events = ActivityEvent.objects.filter(is_completed=False).order_by('-date')
    user_characters = Character.objects.filter(owner=request.user)
    
    # Preselect event from URL
    preselected_token = request.GET.get('event_id')
    preselected_event = None
    if preselected_token:
        preselected_event = ActivityEvent.objects.filter(checkin_token=preselected_token, is_completed=False).first()
    
    context = {
        'active_events': active_events,
        'user_characters': user_characters,
        'preselected_event': preselected_event,
    }
    return render(request, 'items/check_in_event.html', context)


# ======================================================
# PARTY SCANNER
# ======================================================
@login_required
def party_scanner_page(request):
    """
    Party Scanner page - Upload party screenshot and extract data to JSON.
    """
    return render(request, 'items/party_scanner.html')


@login_required
def analyze_party_image(request):
    """
    API Endpoint to scan party screenshot via EasyOCR and return structured JSON.
    Reads party groups and player names from the uploaded image.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    screenshot = request.FILES.get('screenshot')
    if not screenshot:
        return JsonResponse({'error': 'No image provided'}, status=400)

    try:
        result = _scan_party_members_from_image(screenshot)
        if not result.get('success'):
            return JsonResponse({'error': result.get('error', 'Unable to scan image')}, status=result.get('status', 500))
        return JsonResponse(result)

    except ImportError:
        return JsonResponse({'error': 'EasyOCR is not installed'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@login_required

def check_in_event(request):
    """
    Player page to upload screenshot for checking in.
    """
    import re
    from django.utils import timezone
    from PIL import Image
    
    if request.method == 'POST':
        event_id = request.POST.get('event')
        submitter_id = request.POST.get('submitter')
        image = request.FILES.get('screenshot')
        
        if not event_id or not submitter_id or not image:
            messages.error(request, 'Mohon lengkapi semua data dan upload gambar.')
            return redirect('check-in-event')
            
        event = get_object_or_404(ActivityEvent, pk=event_id)
        submitter = get_object_or_404(Character, pk=submitter_id)
        
        # Check if event is active
        if event.is_completed:
            messages.error(request, 'Event ini sudah selesai.')
            return redirect('check-in-event')
            
        # Create proof record
        proof = EventCheckInProof.objects.create(
            event=event,
            submitter=submitter,
            image=image,
            is_valid=False
        )
        
        # Process OCR
        try:
            import pytesseract
        except ImportError:
            pytesseract = None
        
        try:
            if pytesseract is None:
                raise Exception("Tesseract is not installed - using simulation mode")
            
            # We will open the image and run OCR
            img = Image.open(proof.image.path)
            extracted_text = pytesseract.image_to_string(img)
            proof.extracted_text = extracted_text
            
            # 1. Check token
            token = event.checkin_token
            if not token:
                proof.error_reason = "Event ini tidak membutuhkan verifikasi token."
                proof.save()
            elif token not in extracted_text:
                proof.error_reason = f"Token '{token}' tidak ditemukan di gambar."
                proof.save()
            else:
                # 2. Check Party Members
                # Look for patterns like "1P Name", "2P Name", "3P Name", "4P Name"
                # This regex looks for 1P, 2P, 3P, 4P followed by a space and then a word (the name)
                party_members = []
                # A simple regex to catch party members on the left side
                matches = re.finditer(r'([1-4]P)\s+([A-Za-z0-9_]+)', extracted_text)
                for match in matches:
                    party_members.append(match.group(2))
                
                # Also include submitter just in case 1P is not perfectly caught
                if submitter.name not in party_members:
                    party_members.append(submitter.name)
                    
                # Remove duplicates
                party_members = list(set(party_members))
                proof.detected_party_members = ", ".join(party_members)
                
                if len(party_members) < 2:
                    proof.error_reason = "Party tidak valid. Ditemukan kurang dari 2 anggota party di layar."
                    proof.save()
                else:
                    # Valid! Mark attended
                    proof.is_valid = True
                    proof.save()
                    
                    # Mark attendance for all matched members
                    for member_name in party_members:
                        character = Character.objects.filter(name__iexact=member_name).first()
                        if character:
                            # Create or update activity
                            activity, created = PlayerActivity.objects.get_or_create(
                                player=character,
                                event=event,
                                defaults={
                                    'status': 'ABSENT',
                                    'points_earned': 0
                                }
                            )
                            activity.checkin_verified = True
                            activity.checked_in_at = timezone.now()
                            activity.status = 'ATTENDED' if activity.party_scan_verified else 'ABSENT'
                            activity.save()
                    
                    messages.success(request, f'Sukses! Kehadiran {len(party_members)} member party telah dikonfirmasi.')
                    return redirect('my-activity')
                    
        except Exception as e:
            # Fallback if OCR fails or Tesseract is not installed
            # For demonstration, we will mock it if Tesseract is not found
            if 'tesseract is not installed' in str(e).lower():
                proof.error_reason = "Simulasi: Sukses (Tesseract tidak terinstall, tapi sistem pura-pura sukses untuk demo)."
                proof.is_valid = True
                proof.save()
                
                # Auto-attend submitter for demo
                PlayerActivity.objects.update_or_create(
                    player=submitter,
                    event=event,
                    defaults={
                        'status': 'ABSENT',
                        'points_earned': 0,
                        'checkin_verified': True,
                        'checked_in_at': timezone.now(),
                    }
                )
                messages.warning(request, 'Mode Simulasi: Tesseract tidak terinstall di server. Kehadiran Anda dicatat sebagai simulasi.')
                return redirect('my-activity')
            else:
                proof.error_reason = f"OCR Error: {str(e)}"
                proof.save()
                messages.error(request, 'Gagal memproses gambar. Pastikan kualitas gambar jelas.')
        
        return redirect('check-in-event')

    # GET Request
    active_events = ActivityEvent.objects.filter(is_completed=False).order_by('-date')
    user_characters = Character.objects.filter(owner=request.user)
    
    # Preselect event from URL
    preselected_token = request.GET.get('event_id')
    preselected_event = None
    if preselected_token:
        preselected_event = ActivityEvent.objects.filter(checkin_token=preselected_token, is_completed=False).first()
    
    context = {
        'active_events': active_events,
        'user_characters': user_characters,
        'preselected_event': preselected_event,
    }
    return render(request, 'items/check_in_event.html', context)


# ======================================================
# PARTY SCANNER
# ======================================================
@login_required
def party_scanner_page(request):
    """
    Party Scanner page - Upload party screenshot and extract data to JSON.
    """
    return render(request, 'items/party_scanner.html')


@login_required
def analyze_party_image(request):
    """
    API Endpoint to scan party screenshot via EasyOCR and return structured JSON.
    Reads party groups and player names from the uploaded image.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    screenshot = request.FILES.get('screenshot')
    if not screenshot:
        return JsonResponse({'error': 'No image provided'}, status=400)

    try:
        result = _scan_party_members_from_image(screenshot)
        if not result.get('success'):
            return JsonResponse({'error': result.get('error', 'Unable to scan image')}, status=result.get('status', 500))
        return JsonResponse(result)

    except ImportError:
        return JsonResponse({'error': 'EasyOCR is not installed'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ======================================================
# BUYOUT CRITERIA
# ======================================================
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from items.models import Character, PlayerActivity, ActivityEvent

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())

@login_required
def buyout_criteria_page(request):
    """
    Public leaderboard for Buyout Criteria (Dynamic from PlayerActivity)
    """
    characters = Character.objects.select_related('power_rank').all()
    
    # Pre-fetch all activities that are ATTENDED and not archived
    activities = PlayerActivity.objects.filter(
        status='ATTENDED', 
        event__is_buyout_archived=False
    ).select_related('event')
    
    # Map them by character
    activity_map = {}
    for act in activities:
        if act.player_id not in activity_map:
            activity_map[act.player_id] = []
        activity_map[act.player_id].append(act)
        
    criteria = []
    
    for char in characters:
        char_acts = activity_map.get(char.id, [])
        
        br_cc_pts = 0
        invasion_pts = 0
        veora_pts = 0
        kustor_pts = 0
        
        for act in char_acts:
            e_type = act.event.event_type
            # 1. BR + CC
            if e_type in ['BOSS_RUSH', 'CATACOMBS']:
                br_cc_pts += act.event.max_points if act.event.max_points else ActivityEvent.DEFAULT_POINTS.get(e_type, 0)
            # 2. INVASION
            elif e_type in ['INV_DRAGON_BEAST', 'INV_CARNIFEX', 'INV_ORFEN', 'INVASION']:
                if act.event.uses_boss_attendance:
                    for boss_key, killed in act.bosses_killed.items():
                        if killed:
                            invasion_pts += act.event.boss_point_config.get(boss_key, 100)
                else:
                    invasion_pts += act.event.max_points if act.event.max_points else 100
            # 3. VEORA
            elif e_type == 'VEORA':
                veora_pts += act.event.max_points if act.event.max_points else 100
            # 4. KUSTOR, ZHEPAR, HARNAK — dari Raid Boss Activity page (event_type CUSTOM, prefix [Arena Boss])
            elif e_type == 'CUSTOM':
                event_name = act.event.name or ''
                # Format dari halaman Raid Boss Activity: "[Arena Boss] Kustor", "[Arena Boss] Zhepar", "[Arena Boss] Harnak"
                is_arena_boss = '[Arena Boss]' in event_name
                is_target_boss = 'Kustor' in event_name or 'Zhepar' in event_name or 'Harnak' in event_name
                if is_arena_boss and is_target_boss:
                    kustor_pts += act.points_earned if act.points_earned else (act.event.max_points if act.event.max_points else 1000)
                
        # Calculate 50% power rank
        pr_50 = 0
        if hasattr(char, 'power_rank') and char.power_rank:
            try:
                pr_50 = int(float(char.power_rank.gear_score) / 2)
            except:
                pass
                
        total_point = pr_50 + br_cc_pts + invasion_pts + veora_pts + kustor_pts
        
        class DummyCriteria:
            pass
        
        c = DummyCriteria()
        c.character = char
        c.boss_rush_cacomb_pts = br_cc_pts
        c.invasion_boss_pts = invasion_pts
        c.veora_pts = veora_pts
        c.kustor_pts = kustor_pts
        c.total_point = total_point
        c.power_rank_point = pr_50
        
        criteria.append(c)
        
    # Rank diurutkan berdasarkan 50% Power Rank (bukan total point)
    criteria.sort(key=lambda x: x.power_rank_point, reverse=True)
    
    return render(request, 'items/buyout_criteria_leaderboard.html', {
        'criteria': criteria,
    })

@login_required
def buyout_criteria_manage(request):
    """
    Admin page to Reset Buyout Criteria
    """
    if not is_admin(request.user):
        messages.error(request, "Akses ditolak.")
        return redirect('buyout-criteria-leaderboard')
        
    active_events = ActivityEvent.objects.filter(is_buyout_archived=False).order_by('-date')
    
    return render(request, 'items/buyout_criteria_manage.html', {
        'active_events': active_events
    })

@login_required
@require_http_methods(["POST"])
def reset_buyout_criteria(request):
    """
    API Endpoint to archive current events, effectively resetting the buyout criteria
    """
    if not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    try:
        # Mark all currently unarchived events as archived
        updated = ActivityEvent.objects.filter(is_buyout_archived=False).update(is_buyout_archived=True)
        return JsonResponse({'success': True, 'archived_count': updated})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
