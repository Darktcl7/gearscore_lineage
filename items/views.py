from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from .models import Item, Character, SubclassStats, LegendaryClass, CharacterAttributes, CharacteristicsStats, LegendaryAgathion, LegendaryMount, MythicClass, InheritorBook, CLASS_CHOICES, CLASS_TO_WEAPON_TYPE, WEAPON_CHOICES, CLASS_SKILLS_DATA
import json
from .forms import ItemForm, CharacterForm, SubclassStatsForm, CharacterAttributesForm, CharacteristicsStatsForm

# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

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
    if not is_admin(request.user):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    # Optimized: select_related for owner and attributes, prefetch for ManyToMany
    characters = Character.objects.all().select_related('owner', 'attributes', 'subclass_stats', 'characteristics_stats').prefetch_related('mythic_classes', 'legendary_classes', 'legendary_skins')
    # Get pending users (registered but not yet approved)
    from django.contrib.auth.models import User
    pending_users = User.objects.filter(is_active=False, is_staff=False).order_by('-date_joined')
    
    return render(request, 'items/character_management.html', {
        'characters': characters,
        'pending_users': pending_users,
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

    gs_logs = character.gs_logs.all()
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
            weapon_images[value] = f'items/weapons/{weapon_type}/{weapon_name}.png'

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
from django.db.models import Sum, Q
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
    
    # ── MONTHLY RANKING ──
    # Total Score = event points only (EXCLUDE AP adjustments)
    monthly_data = (
        PlayerActivity.objects.filter(
            event__date__year=today.year,
            event__date__month=today.month
        )
        .exclude(event__name__startswith='AP Adjustment:')
        .values('player__id', 'player__name')
        .annotate(
            total_score=Sum('points_earned'),
        )
        .order_by('-total_score')
    )
    
    monthly_ranking = []
    for i, entry in enumerate(monthly_data, 1):
        score = entry['total_score'] or 0
        tier = _get_tier(score)
        
        # Calculate AP adjustments separately
        ap_points = PlayerActivity.objects.filter(
            player__id=entry['player__id'],
            event__name__startswith='AP Adjustment:',
            event__date__year=today.year,
            event__date__month=today.month
        ).aggregate(total=Sum('points_earned'))['total'] or 0
        
        monthly_ranking.append({
            'rank': i,
            'id': entry['player__id'],
            'name': entry['player__name'],
            'total_score': score,
            'ap_points': ap_points,
            'tier': tier,
            'tier_class': tier.lower().replace(' ', '_'),
        })
    
    # ── WEEKLY RANKING ──
    from datetime import timedelta as td
    from .models import LeaderboardConfig
    start_of_week = (today - td(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Respect weekly reset timestamp - only show events after the reset
    lb_config = LeaderboardConfig.get_config()
    weekly_cutoff = start_of_week
    if lb_config.weekly_reset_at and lb_config.weekly_reset_at > start_of_week:
        weekly_cutoff = lb_config.weekly_reset_at
    
    weekly_data = (
        PlayerActivity.objects.filter(
            event__date__gte=weekly_cutoff
        )
        .exclude(event__name__startswith='AP Adjustment:')
        .values('player__id', 'player__name')
        .annotate(
            total_score=Sum('points_earned'),
        )
        .order_by('-total_score')
    )
    
    weekly_ranking = []
    for i, entry in enumerate(weekly_data, 1):
        score = entry['total_score'] or 0
        tier = _get_tier(score)
        
        ap_points = PlayerActivity.objects.filter(
            player__id=entry['player__id'],
            event__name__startswith='AP Adjustment:',
            event__date__gte=weekly_cutoff
        ).aggregate(total=Sum('points_earned'))['total'] or 0
        
        weekly_ranking.append({
            'rank': i,
            'id': entry['player__id'],
            'name': entry['player__name'],
            'total_score': score,
            'ap_points': ap_points,
            'tier': tier,
            'tier_class': tier.lower().replace(' ', '_'),
        })
    
    # ── GUILD STATISTICS ──
    # Use monthly scores for guild stats
    guild_stats = {
        'core': sum(1 for r in monthly_ranking if r['total_score'] > 950),
        'elite': sum(1 for r in monthly_ranking if 675 < r['total_score'] <= 950),
        'active': sum(1 for r in monthly_ranking if 400 < r['total_score'] <= 675),
        'inactive': sum(1 for r in monthly_ranking if r['total_score'] <= 400),
        'total': len(monthly_ranking),
    }
    
    # ── RECENT EVENTS ──
    recent_events = ActivityEvent.objects.filter(date__lte=today).exclude(
        name__startswith='AP Adjustment:'
    ).exclude(
        name__startswith='Score Adjustment:'
    ).order_by('-date')[:10]
    
    context = {
        'monthly_ranking': monthly_ranking,
        'weekly_ranking': weekly_ranking,
        'guild_stats': guild_stats,
        'recent_events': recent_events,
        'current_month': today.strftime('%B %Y'),
        'current_week': f"01 {today.strftime('%b')} - {__import__('calendar').monthrange(today.year, today.month)[1]} {today.strftime('%b %Y')}",
        'is_admin': is_admin(request.user),
    }
    return render(request, 'items/activity_leaderboard.html', context)


def _get_tier(score):
    """Get tier based on total score"""
    if score > 950:
        return 'Core'
    elif score > 675:
        return 'Elite'
    elif score > 400:
        return 'Active'
    else:
        return 'Inactive'


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
        today = timezone.now()
        
        if reset_type == 'weekly':
            # Weekly reset: only update the reset timestamp
            # Data is NOT deleted, so monthly totals stay intact
            from .models import LeaderboardConfig
            config = LeaderboardConfig.get_config()
            config.weekly_reset_at = today
            config.save()
        elif reset_type == 'monthly':
            PlayerActivity.objects.filter(event__date__year=today.year, event__date__month=today.month).delete()
            ActivityEvent.objects.filter(date__year=today.year, date__month=today.month).delete()
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
def my_activity(request):
    """
    Halaman detail aktivitas user sendiri
    """
    # Get current user's characters
    user_characters = Character.objects.filter(owner=request.user)
    
    if not user_characters.exists():
        return render(request, 'items/my_activity.html', {
            'no_character': True,
            'is_admin': is_admin(request.user),
        })
    
    # Get the first character (or allow selection later)
    character = user_characters.first()
    
    # Get current month stats
    today = timezone.now()
    current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    monthly_report = MonthlyReport.objects.filter(
        player=character,
        month__year=today.year,
        month__month=today.month
    ).first()
    
    # Get activity history (last 30 days)
    month_ago = today - timedelta(days=30)
    activities = PlayerActivity.objects.filter(
        player=character,
        event__date__gte=month_ago
    ).select_related('event').order_by('-event__date')
    
    # Calculate quick stats
    total_points = activities.exclude(
        event__name__startswith='AP Adjustment:'
    ).aggregate(total=Sum('points_earned'))['total'] or 0
    
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
        date__gte=month_ago,
        is_completed=True
    ).count()
    
    attendance_rate = (attended_count / total_events * 100) if total_events > 0 else 0
    
    # Calculate tier
    tier = _get_tier(total_points)
    
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
    
    context = {
        'character': character,
        'monthly_report': monthly_report,
        'activities': activities,
        'total_points': total_points,
        'ap_points': ap_points,
        'penalty_total': penalty_total,
        'attended_count': attended_count,
        'total_events': total_events,
        'attendance_rate': attendance_rate,
        'tier': tier,
        'monthly_rewards': monthly_rewards,
        'is_admin': is_admin(request.user),
    }
    return render(request, 'items/my_activity.html', context)


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

@login_required
def manage_events(request):
    """
    Admin page to manage events
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can manage events.")
    
    # Get all actual events (excluding manual point adjustments), ordered by date
    events = ActivityEvent.objects.exclude(
        name__startswith='AP Adjustment:'
    ).exclude(
        name__startswith='Score Adjustment:'
    ).order_by('-date')[:50]
    
    context = {
        'events': events,
        'is_admin': True,
    }
    return render(request, 'items/manage_events.html', context)


@login_required
def create_event(request):
    """
    Admin page to create new event
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can create events.")
    
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
        if request.POST.get('is_mandatory') == 'on':
            try:
                penalty_pts = int(request.POST.get('penalty_points', 5))
            except (ValueError, TypeError):
                penalty_pts = 5
        
        # Build event kwargs
        event_kwargs = {
            'event_type': event_type,
            'name': final_name,
            'date': datetime.strptime(date_str, '%Y-%m-%dT%H:%M'),
            'is_completed': False,
            'is_repeatable': request.POST.get('is_repeatable') == 'on',
            'is_mandatory': request.POST.get('is_mandatory') == 'on',
            'mandatory_penalty': penalty_pts,
            'is_win': False,
            'max_points': event_points,
            'reward_diamond': reward_diamond,
            'reward_diamond_points': reward_diamond_points,
            'reward_key': reward_key,
            'reward_key_points': reward_key_points,
            'reward_membership': reward_membership,
            'reward_membership_points': reward_membership_points,
        }
        
        # For INVASION, set default boss_point_config
        if event_type == 'INVASION':
            event_kwargs['boss_point_config'] = {
                'dragon_beast': 50,
                'carnifex': 25,
                'orfen': 100,
            }
        
        event = ActivityEvent.objects.create(**event_kwargs)
        
        return redirect('manage-events')
    
    import json
    context = {
        'event_types': ActivityEvent.EVENT_TYPE_CHOICES,
        'default_points': json.dumps(ActivityEvent.DEFAULT_POINTS),
        'is_admin': True,
    }
    return render(request, 'items/create_event.html', context)


@login_required
def record_attendance(request, event_pk):
    """
    Admin page to record attendance for an event
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can record attendance.")
    
    event = get_object_or_404(ActivityEvent, pk=event_pk)
    # Optimized: prefetch related data
    all_characters = Character.objects.all().select_related('owner').only('id', 'name', 'level', 'character_class', 'owner_id')
    
    # Get existing attendance details
    attendance_map = {}
    activities = PlayerActivity.objects.filter(event=event)
    for act in activities:
        if act.status == 'ATTENDED':
            attendance_map[act.player_id] = {
                'status': act.status,
                'bosses_killed': act.bosses_killed or {}
            }
    
    if request.method == 'POST':
        # Save boss points if Invasion
        if event.event_type == 'INVASION':
            try:
                db_pts = int(request.POST.get('dragon_beast_points', 50))
            except (ValueError, TypeError):
                db_pts = 50
            try:
                carnifex_pts = int(request.POST.get('carnifex_points', 25))
            except (ValueError, TypeError):
                carnifex_pts = 25
            try:
                orfen_pts = int(request.POST.get('orfen_points', 100))
            except (ValueError, TypeError):
                orfen_pts = 100
            event.boss_point_config = {
                'dragon_beast': db_pts,
                'carnifex': carnifex_pts,
                'orfen': orfen_pts,
            }
            event.save()
        
        # Get selected characters
        selected_ids = request.POST.getlist('characters')
        
        # Create/update attendance records
        for char_id in selected_ids:
            character = Character.objects.get(pk=char_id)
            
            defaults = {'status': 'ATTENDED', 'points_earned': 0}
            
            # For Invasion, capture INDIVIDUAL boss checkboxes
            if event.event_type == 'INVASION':
                bosses = {
                    'dragon_beast': request.POST.get(f'boss_dragon_beast_{char_id}') == 'true',
                    'carnifex': request.POST.get(f'boss_carnifex_{char_id}') == 'true',
                    'orfen': request.POST.get(f'boss_orfen_{char_id}') == 'true',
                }
                defaults['bosses_killed'] = bosses
            
            activity, created = PlayerActivity.objects.update_or_create(
                player=character,
                event=event,
                defaults=defaults
            )
            # Force re-save to trigger point calculation in model's save()
            activity.save()
        
        # Mark absent for unselected
        for char in all_characters:
            if str(char.pk) not in selected_ids:
                PlayerActivity.objects.update_or_create(
                    player=char,
                    event=event,
                    defaults={'status': 'ABSENT', 'points_earned': 0, 'bosses_killed': {}}
                )
        
        # Auto-calculate monthly reports
        from .services import calculate_monthly_reports
        calculate_monthly_reports(event.date.year, event.date.month)
        
        return redirect('manage-events')
    
    
    # Prepare characters with attendance info attached
    processed_characters = []
    for char in all_characters:
        att = attendance_map.get(char.pk)
        char.is_attended = att is not None
        char.bosses_killed = att['bosses_killed'] if att else {}
        processed_characters.append(char)
        
    bosspc = event.boss_point_config or {}
    boss_points = {
        'dragon_beast': bosspc.get('dragon_beast', 50),
        'carnifex': bosspc.get('carnifex', 25),
        'orfen': bosspc.get('orfen', 100),
    }
    
    context = {
        'event': event,
        'characters': processed_characters,
        'boss_points': boss_points,
        'is_admin': True,
    }
    return render(request, 'items/record_attendance.html', context)


@login_required
def duplicate_event(request, event_pk):
    """
    Duplicate an event exactly 7 days later
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can duplicate events.")
    
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
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can manage events.")
    
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
    """Admin only: Reset password for any user"""
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can reset passwords.")
    
    target_user = get_object_or_404(User, pk=user_pk)
    
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
            if message:
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
