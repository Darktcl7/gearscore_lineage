from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Item, Character, SubclassStats, LegendaryClass, CharacterAttributes, CharacteristicsStats, LegendaryAgathion, InheritorBook, CLASS_CHOICES, CLASS_TO_WEAPON_TYPE, WEAPON_CHOICES
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
    characters = Character.objects.filter(owner=request.user).select_related('attributes', 'subclass_stats', 'characteristics_stats').prefetch_related('legendary_classes', 'legendary_agathions')
    return render(request, 'items/character_list.html', {'characters': characters, 'is_admin': is_admin(request.user)})

# FUNGSI: Manajemen Karakter (Admin Only) -> Table View
@login_required
def character_management(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    # Optimized: select_related for owner and attributes, prefetch for ManyToMany
    characters = Character.objects.all().select_related('owner', 'attributes', 'subclass_stats', 'characteristics_stats').prefetch_related('legendary_classes')
    
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
    from .models import CharacterAttributes
    
    # Optimized: select_related for OneToOne relations to avoid N+1
    character = get_object_or_404(Character.objects.select_related('attributes', 'subclass_stats', 'characteristics_stats').prefetch_related('legendary_classes', 'legendary_agathions'), pk=pk)
    
    # Permission check: user biasa hanya bisa lihat profil sendiri
    if not is_admin(request.user) and character.owner != request.user:
        return HttpResponseForbidden("You don't have permission to view this profile.")
    
    # Pastikan CharacterAttributes ada untuk karakter ini
    CharacterAttributes.objects.get_or_create(character=character)
    
    # 1. Hitung Gear Score karakter ini
    gear_score = character.calculate_gear_score()
    
    # 2. Hitung Ranking
    # Ambil semua karakter, hitung GS mereka, lalu urutkan
    # Optimized: Fetch all characters WITH related data for scoring loop
    all_characters = Character.objects.select_related('attributes', 'subclass_stats', 'characteristics_stats').all()
    char_scores = []
    for char in all_characters:
        score = char.calculate_gear_score()
        char_scores.append({'id': char.id, 'score': score})
    
    # Urutkan dari score tertinggi ke terendah
    char_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Cari posisi karakter ini (1-based index)
    rank = "N/A"
    for index, item in enumerate(char_scores):
        if item['id'] == character.id:
            rank = index + 1
            break
            
    gs_logs = character.gs_logs.all() # Fetch all related logs
    
    # Check if user can edit this character (owner or admin)
    can_edit = is_admin(request.user) or character.owner == request.user
    
    context = {
        'character': character,
        'gear_score': gear_score,
        'rank': rank, # Pass rank to template
        'gs_logs': gs_logs,
        'is_admin': is_admin(request.user),
        'can_edit': can_edit,
    }
    return render(request, 'items/character_profile.html', context)


# FUNGSI BARU: Membuat atau Mengedit Karakter (create_character)
@login_required
def create_character(request, pk=None):
    # DEBUG: Print user info
    print(f"DEBUG EDIT CHAR: PK={pk}, User={request.user} (ID: {request.user.id})")
    print(f"Is Admin? {is_admin(request.user)}")

    character_instance = get_object_or_404(Character, pk=pk) if pk else None
    
    # Permission check: admin can edit any, user can only edit their own
    # Also allow editing if character has no owner (e.g., created by admin)
    if character_instance:
        print(f"Char Owner: {character_instance.owner} (ID: {character_instance.owner.id if character_instance.owner else 'None'})")
        if not is_admin(request.user):
            # Allow if user owns the character OR character has no owner
            if character_instance.owner and character_instance.owner != request.user:
                print("PERMISSION DENIED")
                return HttpResponseForbidden("You can only edit your own characters.")
            elif not character_instance.owner:
                print("CHARACTER HAS NO OWNER - ALLOWING EDIT")
        else:
            print("PERMISSION GRANTED (ADMIN)")
    
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

    legendary_class_icons = {lc.name: lc.icon_file for lc in LegendaryClass.objects.all()}
    legendary_agathion_icons = {la.name: la.icon_file for la in LegendaryAgathion.objects.all()}

    question_icons = {
        'soulshot_level': 's1.webm', 'valor_level': 's2.webm',
        'soul_prog_attack': 'Icon_SoulStone_Option_Icon_01.png', 'soul_prog_defense': 'Icon_SoulStone_Option_Icon_04.png',
        'soul_prog_blessing': 'Icon_SoulStone_Option_Icon_07.png', 'inheritor_books': 'Icon_Item_Usable_SkillBook_04.png',
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
        'legendary_class_icons': legendary_class_icons,
        'legendary_agathion_icons': legendary_agathion_icons,
        'question_icons': question_icons,
        'class_to_weapon_type': json.dumps(CLASS_TO_WEAPON_TYPE),
        'weapon_images': json.dumps(weapon_images),
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
            form.save()
            # Redirect kembali ke halaman profil karakter setelah save
            return redirect('character-profile', pk=character_pk)
    else:
        form = SubclassStatsForm(instance=stats)
        
    context = {
        'form': form,
        'character': character,
        'title': f'Subclass Information for {character.name}',
        'form_description': 'Fill out information about your subclass skills and weapons.'
    }
    return render(request, 'items/subclass_form.html', context)  # Use dedicated subclass template

# FUNGSI BARU: Mengedit Characteristics Stats (100+ Fields)
@login_required
def edit_characteristics_stats(request, character_pk):
    character = get_object_or_404(Character, pk=character_pk)
    
    # Permission check: admin can edit any, user can only edit their own
    if not is_admin(request.user) and character.owner != request.user:
        return HttpResponseForbidden("You can only edit your own characters.")
    
    # Dapatkan atau buat objek CharacteristicsStats yang terikat pada karakter ini
    stats, created = CharacteristicsStats.objects.get_or_create(character=character)
    
    if request.method == 'POST':
        form = CharacteristicsStatsForm(request.POST, instance=stats)
        if form.is_valid():
            form.save()
            return redirect('character-profile', pk=character_pk)
    else:
        form = CharacteristicsStatsForm(instance=stats)
        
    context = {
        'form': form,
        'character': character,
        'title': f'Edit Characteristics for {character.name}',
        'form_description': 'Detailed breakdown of all combat statistics.'
    }
    return render(request, 'items/characteristics_form.html', context)


# ======================================================
# ACTIVITY VIEWS
# ======================================================
from .models import ActivityEvent, PlayerActivity, MonthlyReport
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def activity_leaderboard(request):
    """
    Halaman Activity Leaderboard - tampilan utama untuk semua user
    """
    # Get current month
    today = timezone.now()
    current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get monthly reports for current month
    monthly_reports = MonthlyReport.objects.filter(
        month__year=today.year,
    ).select_related('player').order_by('-total_score')
    
    # Get recent events (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_events = ActivityEvent.objects.filter(
        date__gte=week_ago
    ).order_by('-date')[:10]
    
    # Get user's character and their stats (if logged in as regular user)
    user_report = None
    user_character = None
    if not is_admin(request.user):
        user_character = Character.objects.filter(owner=request.user).first()
        if user_character:
            user_report = MonthlyReport.objects.filter(
                player=user_character,
                month__year=today.year,
                month__month=today.month
            ).first()
    
    # Calculate tier statistics
    tier_counts = {
        'ELITE': monthly_reports.filter(tier='ELITE').count(),
        'CORE': monthly_reports.filter(tier='CORE').count(),
        'ACTIVE': monthly_reports.filter(tier='ACTIVE').count(),
        'CASUAL': monthly_reports.filter(tier='CASUAL').count(),
    }
    
    # Get Config for UI (percentages)
    from .services import get_active_config
    config = get_active_config()
    
    # Pre-calculate percentage integers for display
    # The config has floats like 0.7, template wants "70%"
    tier_percentages = {
        'ELITE': int(config['tier_allocation']['ELITE'] * 100),
        'CORE': int(config['tier_allocation']['CORE'] * 100),
        'ACTIVE': int(config['tier_allocation']['ACTIVE'] * 100),
        'CASUAL': int(config['tier_allocation']['CASUAL'] * 100),
    }

    context = {
        'monthly_reports': monthly_reports,
        'recent_events': recent_events,
        'user_report': user_report,
        'user_character': user_character,
        'tier_counts': tier_counts,
        'current_month': current_month,
        'is_admin': is_admin(request.user),
        'tier_percentages': tier_percentages, # Pass to template
    }
    return render(request, 'items/activity_leaderboard.html', context)


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
            elite = float(request.POST.get('elite', 0))
            core = float(request.POST.get('core', 0)) 
            active = float(request.POST.get('active', 0))
            casual = float(request.POST.get('casual', 0))
            
            # Basic validation
            total = elite + core + active + casual
            if total != 100:
                 # Allow small margin of user error or just normalize?
                 # For now, strict 100% check
                 pass 
                 
            # Convert to 0.70 format
            from .models import PrizePoolConfig
            config = PrizePoolConfig.objects.create(
                elite_percentage=elite/100.0,
                core_percentage=core/100.0,
                active_percentage=active/100.0,
                casual_percentage=casual/100.0,
                updated_by=request.user.username
            )
            # You might want to update total_pool too if needed
            
            # Recalculate current month's prizes immediately?
            # User requirement: "results in existing/previous leaderboard not affected"
            # But the CURRENT month is usually considered "live".
            # If we want the change to apply immediately to the CURRENT displaying month:
            from .services import calculate_prize_distribution
            today = timezone.now()
            calculate_prize_distribution(today.year, today.month)
            
            return redirect('activity-leaderboard')
            
        except ValueError:
            pass # Invalid numbers
            
    return redirect('activity-leaderboard')


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
    total_points = activities.filter(status='ATTENDED').aggregate(
        total=Sum('points_earned')
    )['total'] or 0
    
    attended_count = activities.filter(status='ATTENDED').count()
    total_events = ActivityEvent.objects.filter(
        date__gte=month_ago,
        is_completed=True
    ).count()
    
    attendance_rate = (attended_count / total_events * 100) if total_events > 0 else 0
    
    context = {
        'character': character,
        'monthly_report': monthly_report,
        'activities': activities,
        'total_points': total_points,
        'attended_count': attended_count,
        'total_events': total_events,
        'attendance_rate': attendance_rate,
        'is_admin': is_admin(request.user),
    }
    return render(request, 'items/my_activity.html', context)


@login_required
def manage_events(request):
    """
    Admin page to manage events
    """
    if not is_admin(request.user):
        return HttpResponseForbidden("Only administrators can manage events.")
    
    # Get all events, ordered by date
    events = ActivityEvent.objects.all().order_by('-date')[:50]
    
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
        is_win = request.POST.get('is_win') == 'on'
        
        # For custom events, use the custom name
        if event_type == 'CUSTOM' and custom_name:
            reward = request.POST.get('name')
            if reward:
                final_name = f"{custom_name} ({reward})"
            else:
                final_name = custom_name
        elif name:
            final_name = name
        else:
            final_name = f"{event_type} Event"
        
        # Parse bosses killed for Invasion
        bosses_killed = {}
        if event_type == 'INVASION':
            bosses_killed = {
                'dragon_beast': request.POST.get('dragon_beast') == 'on',
                'carnifex': request.POST.get('carnifex') == 'on',
                'orfen': request.POST.get('orfen') == 'on',
            }
        
        # Parse custom points for Custom events
        custom_pts = 10
        if event_type == 'CUSTOM':
            try:
                custom_pts = int(request.POST.get('custom_points', 10))
            except (ValueError, TypeError):
                custom_pts = 10
        
        # Create event
        event = ActivityEvent.objects.create(
            event_type=event_type,
            name=final_name,
            date=datetime.strptime(date_str, '%Y-%m-%dT%H:%M'),
            is_completed=request.POST.get('is_completed') == 'on',
            is_win=False,
            bosses_killed={},
            custom_points=custom_pts,
        )
        
        return redirect('manage-events')
    
    context = {
        'event_types': ActivityEvent.EVENT_TYPE_CHOICES,
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
                event.dragon_beast_points = int(request.POST.get('dragon_beast_points', 10))
            except (ValueError, TypeError):
                event.dragon_beast_points = 10
            try:
                event.carnifex_points = int(request.POST.get('carnifex_points', 15))
            except (ValueError, TypeError):
                event.carnifex_points = 15
            try:
                event.orfen_points = int(request.POST.get('orfen_points', 25))
            except (ValueError, TypeError):
                event.orfen_points = 25
            event.save()
        
        # Get selected characters
        selected_ids = request.POST.getlist('characters')
        
        # Create/update attendance records
        for char_id in selected_ids:
            character = Character.objects.get(pk=char_id)
            
            defaults = {'status': 'ATTENDED'}
            
            # For Invasion, capture INDIVIDUAL boss checkboxes
            if event.event_type == 'INVASION':
                bosses = {
                    'dragon_beast': request.POST.get(f'boss_dragon_beast_{char_id}') == 'true',
                    'carnifex': request.POST.get(f'boss_carnifex_{char_id}') == 'true',
                    'orfen': request.POST.get(f'boss_orfen_{char_id}') == 'true',
                }
                defaults['bosses_killed'] = bosses
            
            PlayerActivity.objects.update_or_create(
                player=character,
                event=event,
                defaults=defaults
            )
        
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
    
    context = {
        'event': event,
        'characters': processed_characters,
        # 'existing_attendance' removed as it's now char.is_attended
        'is_admin': True,
    }
    return render(request, 'items/record_attendance.html', context)


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
