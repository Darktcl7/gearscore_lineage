from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import DKPEvent, DKPAttendance, DKPProfile, DKPLog, BossPointConfig, AdminRole, TreasuryItemConfig, TreasuryTransaction, Auction, AuctionBid
from items.models import Character, DiscordAnnouncement
import json
import os

API_KEY = "alto-discord-bot-key-2026"

def verify_api_key(request):
    key = request.headers.get('X-API-Key')
    return key == API_KEY

@csrf_exempt
def api_dkp_active_events(request):
    if not verify_api_key(request): return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    events = DKPEvent.objects.filter(is_active=True).order_by('date')
    data = []
    for e in events:
        data.append({
            'id': e.id,
            'name': e.name,
            'points': e.points_to_award,
            'participants': e.attendances.count()
        })
    return JsonResponse({'success': True, 'events': data})

@csrf_exempt
def api_dkp_checkin(request):
    if request.method != 'POST': return JsonResponse({'error': 'Method not allowed'}, status=405)
    if not verify_api_key(request): return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        data = json.loads(request.body)
        event_id = data.get('event_id')
        discord_id = data.get('discord_user_id')
        
        try:
            event = DKPEvent.objects.get(id=event_id)
        except DKPEvent.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        
        if event.is_closed or not event.is_active:
            return JsonResponse({'error': 'Check-in CLOSED'}, status=400)
            
        # Find Character
        character = Character.objects.filter(discord_id=discord_id).first()
        if not character:
            return JsonResponse({'error': 'Discord not linked to any Character'}, status=404)
            
        # Checkin
        att, created = DKPAttendance.objects.get_or_create(event=event, character=character)
        
        if not created:
             return JsonResponse({
                 'success': True, 
                 'message': 'Already checked in.', 
                 'already_checked_in': True,
                 'status': 'Verified' if att.is_verified else 'Pending Verification',
                 'character': character.name
             })
             
        return JsonResponse({
            'success': True,
            'message': 'Check-in recorded! Waiting for Admin verification.',
            'character': character.name
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def api_dkp_me(request, character_name):
    if not verify_api_key(request): return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    character = Character.objects.filter(name__iexact=character_name).first()
    if not character:
        return JsonResponse({'error': 'Character not found'}, status=404)
        
    profile, _ = DKPProfile.objects.get_or_create(character=character)
    
    return JsonResponse({
        'success': True,
        'character': character.name,
        'current_dkp': profile.current_dkp,
        'total_earned': profile.total_earned
    })

@csrf_exempt
def api_dkp_me_discord(request, discord_id):
    if not verify_api_key(request): return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    character = Character.objects.filter(discord_id=discord_id).first()
    if not character:
        return JsonResponse({'error': 'Discord not linked to any Character'}, status=404)
        
    profile, _ = DKPProfile.objects.get_or_create(character=character)
    
    return JsonResponse({
        'success': True,
        'character': character.name,
        'current_dkp': profile.current_dkp,
        'total_earned': profile.total_earned
    })

@csrf_exempt
def api_dkp_leaderboard(request):
    if not verify_api_key(request): return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    from django.db.models import Q
    profiles = DKPProfile.objects.select_related('character').order_by('-current_dkp')
    
    leaderboards_by_clan = {
        'Valkyrie': [],
        'Valhalla': []
    }
    
    for clan_name in leaderboards_by_clan.keys():
        if clan_name == 'Valkyrie':
            clan_profiles = profiles.filter(Q(character__clan='Valkyrie') | Q(character__clan='') | Q(character__clan__isnull=True))
        else:
            clan_profiles = profiles.filter(character__clan=clan_name)
            
        rank = 1
        for p in clan_profiles:
            leaderboards_by_clan[clan_name].append({
                'rank': rank,
                'character': p.character.name,
                'dkp': p.current_dkp
            })
            rank += 1

    return JsonResponse({
        'success': True,
        'leaderboards_by_clan': leaderboards_by_clan
    })

def dkp_leaderboard_web(request):
    selected_clan = request.GET.get('clan', 'Valkyrie')
    clan_choices = ['Valkyrie', 'Valhalla']
    
    from django.db.models import Q
    profiles = DKPProfile.objects.select_related('character')
    if selected_clan == 'Valkyrie':
        profiles = profiles.filter(Q(character__clan='Valkyrie') | Q(character__clan='') | Q(character__clan__isnull=True))
    else:
        profiles = profiles.filter(character__clan=selected_clan)
    profiles = profiles.order_by('-current_dkp')
    
    # Granular DKP board permissions
    user_can_give = can_give_dkp(request.user) if request.user.is_authenticated else False
    user_can_remove = can_remove_dkp(request.user) if request.user.is_authenticated else False
    user_can_decay = can_decay_dkp(request.user) if request.user.is_authenticated else False
    
    is_admin = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser or user_can_give or user_can_remove or user_can_decay)
    
    return render(request, 'dkp/leaderboard.html', {
        'profiles': profiles,
        'is_admin': is_admin,
        'can_give': user_can_give,
        'can_remove': user_can_remove,
        'can_decay': user_can_decay,
        'selected_clan': selected_clan,
        'clan_choices': clan_choices,
    })

@login_required(login_url='/login/')
def dkp_decay(request):
    """Apply DKP decay to a single player - max 5%"""
    if not can_decay_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        try:
            decay_pct = float(request.POST.get('decay_percent', 0))
        except (ValueError, TypeError):
            decay_pct = 0
        
        reason = request.POST.get('reason', '').strip()
        if not reason:
            reason = f"DKP Decay ({decay_pct}%)"
        
        # Clamp between 0.1 and 5
        if decay_pct < 0.1:
            decay_pct = 0.1
        if decay_pct > 5:
            decay_pct = 5
        
        try:
            profile = DKPProfile.objects.get(id=profile_id)
            if profile.current_dkp > 0:
                decay_amount = int(profile.current_dkp * (decay_pct / 100))
                if decay_amount < 1:
                    decay_amount = 1
                
                profile.current_dkp -= decay_amount
                if profile.current_dkp < 0:
                    profile.current_dkp = 0
                profile.last_decay_percent = decay_pct
                profile.save()
                
                DKPLog.objects.create(
                    profile=profile,
                    amount=-decay_amount,
                    reason=reason,
                    created_by=request.user
                )
        except DKPProfile.DoesNotExist:
            pass
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_adjust(request):
    """Give or remove DKP points for a single player"""
    action = request.POST.get('adjust_action')

    if action == 'give' and not can_give_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    if action == 'remove' and not can_remove_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('adjust_action')  # 'give' or 'remove'
        try:
            amount = int(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0
        
        reason = request.POST.get('reason', '').strip()
        if not reason:
            if action == 'give':
                reason = f"Admin Give (+{amount})"
            else:
                reason = f"Admin Remove (-{amount})"
        
        if amount > 0:
            try:
                profile = DKPProfile.objects.get(id=profile_id)
                if action == 'give':
                    profile.current_dkp += amount
                    profile.total_earned += amount
                    profile.save()
                    DKPLog.objects.create(
                        profile=profile,
                        amount=amount,
                        reason=reason,
                        created_by=request.user
                    )
                elif action == 'remove':
                    profile.current_dkp -= amount
                    if profile.current_dkp < 0:
                        profile.current_dkp = 0
                    profile.save()
                    DKPLog.objects.create(
                        profile=profile,
                        amount=-amount,
                        reason=reason,
                        created_by=request.user
                    )
            except DKPProfile.DoesNotExist:
                pass
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_give_all(request):
    """Give DKP points to all players"""
    if not can_give_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0
        
        reason = request.POST.get('reason', '').strip()
        if not reason:
            reason = f"Bulk Give (+{amount})"
        
        if amount > 0:
            profiles = DKPProfile.objects.all()
            for profile in profiles:
                profile.current_dkp += amount
                profile.total_earned += amount
                profile.save()
                DKPLog.objects.create(
                    profile=profile,
                    amount=amount,
                    reason=reason,
                    created_by=request.user
                )
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_remove_all(request):
    """Remove DKP points from all players"""
    if not can_remove_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0
        
        reason = request.POST.get('reason', '').strip()
        if not reason:
            reason = f"Bulk Remove (-{amount})"
        
        if amount > 0:
            profiles = DKPProfile.objects.all()
            for profile in profiles:
                profile.current_dkp -= amount
                if profile.current_dkp < 0:
                    profile.current_dkp = 0
                profile.save()
                DKPLog.objects.create(
                    profile=profile,
                    amount=-amount,
                    reason=reason,
                    created_by=request.user
                )
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_reset_lifetime(request):
    """Reset Lifetime Earned for all players"""
    if not can_decay_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        profiles = DKPProfile.objects.all()
        for profile in profiles:
            profile.total_earned = 0
            profile.save()
            DKPLog.objects.create(
                profile=profile,
                amount=0,
                reason='Lifetime Earned Reset',
                created_by=request.user
            )
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_decay_all(request):
    """Apply DKP decay to all players"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        try:
            decay_pct = float(request.POST.get('decay_percent', 0))
        except (ValueError, TypeError):
            decay_pct = 0
        
        if decay_pct < 0.1:
            decay_pct = 0.1
        if decay_pct > 5:
            decay_pct = 5
        
        reason = request.POST.get('reason', '').strip()
        if not reason:
            reason = f"Bulk DKP Decay ({decay_pct}%)"
        
        profiles = DKPProfile.objects.all()
        for profile in profiles:
            if profile.current_dkp > 0:
                decay_amount = int(profile.current_dkp * (decay_pct / 100))
                if decay_amount < 1:
                    decay_amount = 1
                
                profile.current_dkp -= decay_amount
                if profile.current_dkp < 0:
                    profile.current_dkp = 0
                profile.last_decay_percent = decay_pct
                profile.save()
                
                DKPLog.objects.create(
                    profile=profile,
                    amount=-decay_amount,
                    reason=reason,
                    created_by=request.user
                )
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_give_selected(request):
    """Give DKP points to selected players"""
    if not can_give_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        profile_ids = request.POST.get('profile_ids', '')
        try:
            amount = int(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0
        
        reason = request.POST.get('reason', '').strip()
        if not reason:
            reason = f"Bulk Give (+{amount})"
        
        if amount > 0 and profile_ids:
            ids = [int(x.strip()) for x in profile_ids.split(',') if x.strip().isdigit()]
            profiles = DKPProfile.objects.filter(id__in=ids)
            for profile in profiles:
                profile.current_dkp += amount
                profile.total_earned += amount
                profile.save()
                DKPLog.objects.create(
                    profile=profile,
                    amount=amount,
                    reason=reason,
                    created_by=request.user
                )
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_remove_selected(request):
    """Remove DKP points from selected players"""
    if not can_remove_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        profile_ids = request.POST.get('profile_ids', '')
        try:
            amount = int(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0
        
        reason = request.POST.get('reason', '').strip()
        if not reason:
            reason = f"Bulk Remove (-{amount})"
        
        if amount > 0 and profile_ids:
            ids = [int(x.strip()) for x in profile_ids.split(',') if x.strip().isdigit()]
            profiles = DKPProfile.objects.filter(id__in=ids)
            for profile in profiles:
                profile.current_dkp -= amount
                if profile.current_dkp < 0:
                    profile.current_dkp = 0
                profile.save()
                DKPLog.objects.create(
                    profile=profile,
                    amount=-amount,
                    reason=reason,
                    created_by=request.user
                )
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_decay_selected(request):
    """Apply DKP decay to selected players"""
    if not can_decay_dkp(request.user):
        return redirect('web-dkp-leaderboard')
    
    if request.method == 'POST':
        profile_ids = request.POST.get('profile_ids', '')
        try:
            decay_pct = float(request.POST.get('decay_percent', 0))
        except (ValueError, TypeError):
            decay_pct = 0
        
        if decay_pct < 0.1:
            decay_pct = 0.1
        if decay_pct > 5:
            decay_pct = 5
        
        reason = request.POST.get('reason', '').strip()
        if not reason:
            reason = f"Bulk DKP Decay ({decay_pct}%)"
        
        if profile_ids:
            ids = [int(x.strip()) for x in profile_ids.split(',') if x.strip().isdigit()]
            profiles = DKPProfile.objects.filter(id__in=ids)
            for profile in profiles:
                if profile.current_dkp > 0:
                    decay_amount = int(profile.current_dkp * (decay_pct / 100))
                    if decay_amount < 1:
                        decay_amount = 1
                    
                    profile.current_dkp -= decay_amount
                    if profile.current_dkp < 0:
                        profile.current_dkp = 0
                    profile.last_decay_percent = decay_pct
                    profile.save()
                    
                    DKPLog.objects.create(
                        profile=profile,
                        amount=-decay_amount,
                        reason=reason,
                        created_by=request.user
                    )
    
    return redirect('web-dkp-leaderboard')

@login_required(login_url='/login/')
def dkp_my_profile(request):
    user_chars = Character.objects.filter(owner=request.user)
    
    # Auto-cleanup logs older than 3 days
    from django.utils import timezone
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    DKPLog.objects.filter(created_at__lt=three_days_ago).delete()
    
    profiles = []
    if user_chars.exists():
        for char in user_chars:
            p, _ = DKPProfile.objects.get_or_create(character=char)
            all_logs = p.logs.order_by('-created_at')
            from django.core.paginator import Paginator
            paginator = Paginator(all_logs, 20)
            page_number = request.GET.get('page')
            p.recent_logs = paginator.get_page(page_number)
            profiles.append(p)
            
            
    return render(request, 'dkp/my_profile.html', {'profiles': profiles})


@login_required(login_url='/login/')
def dkp_user_profile(request, user_id):
    """Admin view: show DKP wallet for a specific user by user_id."""
    from django.contrib.auth.models import User
    from django.shortcuts import get_object_or_404
    from django.http import HttpResponseForbidden
    
    # Only admin/staff can view other users' wallets
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Only admins can view other users' wallets.")
    
    target_user = get_object_or_404(User, pk=user_id)
    user_chars = Character.objects.filter(owner=target_user)
    
    profiles = []
    if user_chars.exists():
        for char in user_chars:
            p, _ = DKPProfile.objects.get_or_create(character=char)
            all_logs = p.logs.order_by('-created_at')
            from django.core.paginator import Paginator
            paginator = Paginator(all_logs, 20)
            page_number = request.GET.get('page')
            p.recent_logs = paginator.get_page(page_number)
            profiles.append(p)
    
    return render(request, 'dkp/my_profile.html', {
        'profiles': profiles,
        'viewing_user': target_user,
    })

@login_required(login_url='/login/')
def dkp_all_wallets(request):
    if not request.user.is_staff:
        return redirect('index')
    
    profiles = DKPProfile.objects.select_related('character', 'character__owner').order_by('-current_dkp')
    
    for p in profiles:
        p.recent_logs = p.logs.order_by('-created_at')
    
    return render(request, 'dkp/all_wallets.html', {'profiles': profiles})




def is_dkp_admin(user):
    from items.views import is_admin
    if is_admin(user):
        return True
    try:
        return user.admin_role.is_dkp_admin
    except Exception:
        return False

def can_give_dkp(user):
    """Check if user can Give DKP on the board"""
    from items.views import is_admin
    if is_admin(user):
        return True
    try:
        role = user.admin_role
        return role.is_dkp_admin and role.can_give_dkp
    except Exception:
        return False

def can_remove_dkp(user):
    """Check if user can Remove DKP on the board"""
    from items.views import is_admin
    if is_admin(user):
        return True
    try:
        role = user.admin_role
        return role.is_dkp_admin and role.can_remove_dkp
    except Exception:
        return False

def can_decay_dkp(user):
    """Check if user can Decay DKP on the board"""
    from items.views import is_admin
    if is_admin(user):
        return True
    try:
        role = user.admin_role
        return role.is_dkp_admin and role.can_decay_dkp
    except Exception:
        return False

@login_required(login_url='/login/')
def dkp_manage(request):
    if not is_dkp_admin(request.user):
        return HttpResponseForbidden("You do not have access to manage DKP.")
    
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

                # Build final event name
                final_name = f"[{boss_type}] {name}" if boss_type else name

                # Create event — already finalized (direct award, no check-in needed)
                event = DKPEvent.objects.create(
                    name=final_name,
                    points_to_award=points,
                    is_active=False,
                    is_closed=True,
                    is_finalized=True,
                    is_war_day=is_war_day,
                    note=activity_note,
                    created_by=request.user,
                )

                # WAR DAY: Also create Activity event if checked (Raid Boss & Territory Boss only)
                activity_event = None
                if is_war_day and boss_type in ('Raid Boss', 'Territory Boss', 'World Boss'):
                    from items.models import ActivityEvent, PlayerActivity
                    activity_event = ActivityEvent.objects.create(
                        name=f"⚔️ War Day: {final_name}",
                        event_type='WAR_DAY',
                        date=timezone.now(),
                        base_points=points,
                        max_points=points,
                        is_completed=True,
                        is_finalized=True,
                    )

                # Distribute points immediately to selected participants
                if participant_ids and points > 0:
                    for pid in participant_ids:
                        try:
                            profile = DKPProfile.objects.get(id=int(pid))
                            DKPAttendance.objects.get_or_create(
                                event=event,
                                character=profile.character,
                                defaults={'is_verified': True}
                            )
                            profile.current_dkp += points
                            profile.total_earned += points
                            profile.save()
                            DKPLog.objects.create(
                                profile=profile,
                                amount=points,
                                reason=f"Activity: {final_name}",
                                note=activity_note,
                                is_war_day=is_war_day,
                                created_by=request.user
                            )
                            
                            # WAR DAY: Also add to Activity Leaderboard
                            if activity_event:
                                from items.models import PlayerActivity
                                PlayerActivity.objects.create(
                                    player=profile.character,
                                    event=activity_event,
                                    status='ATTENDED',
                                    points_earned=points,
                                )
                        except (DKPProfile.DoesNotExist, ValueError):
                            pass

        elif action == 'toggle':
            event_id = request.POST.get('event_id')
            try:
                event = DKPEvent.objects.get(id=event_id)
                event.is_active = not event.is_active
                event.save()
            except DKPEvent.DoesNotExist:
                pass
        
        elif action == 'delete':
            event_id = request.POST.get('event_id')
            DKPEvent.objects.filter(id=event_id).delete()

        elif action == 'bulk_delete':
            event_ids_str = request.POST.get('event_ids', '')
            if event_ids_str:
                ids = [int(x.strip()) for x in event_ids_str.split(',') if x.strip().isdigit()]
                if ids:
                    DKPEvent.objects.filter(id__in=ids).delete()

        return redirect('web-dkp-manage')
            
    # Auto-cleanup events older than 3 days
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    DKPEvent.objects.filter(date__lt=three_days_ago).delete()

    all_events = DKPEvent.objects.order_by('-date')
    from django.core.paginator import Paginator
    paginator = Paginator(all_events, 20)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    profiles = DKPProfile.objects.select_related('character').order_by('character__name')
    from items.views import is_admin
    return render(request, 'dkp/manage.html', {
        'events': events,
        'profiles': profiles,
        'is_super_admin': is_admin(request.user),
    })

@login_required(login_url='/login/')
def dkp_attendance_list(request, event_id):
    if not request.user.is_staff:
        return redirect('index')
    
    event = DKPEvent.objects.get(id=event_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve_all':
            pending_list = DKPAttendance.objects.filter(event=event, is_verified=False)
            points = event.points_to_award
            
            # Note: No bulk public notification, individual DMs sent in loop below
            
            for att in pending_list:
                att.is_verified = True
                att.save()
                
                # Add Points
                profile, _ = DKPProfile.objects.get_or_create(character=att.character)
                profile.current_dkp += points
                profile.total_earned += points
                profile.save()
                
                
                # Log
                DKPLog.objects.create(
                    profile=profile,
                    amount=points,
                    reason=f"Event: {event.name}",
                    created_by=request.user
                )
                
                # Notification (DM if linked)
                if att.character.discord_id:
                    DiscordAnnouncement.objects.create(
                        message=f"[DM:{att.character.discord_id}] ✅ **{att.character.name}**, kehadiran kamu di event **{event.name}** sudah diverifikasi Admin!"
                    )
                
        elif action == 'approve':
            att_id = request.POST.get('attendance_id')
            try:
                att = DKPAttendance.objects.get(id=att_id)
                if not att.is_verified:
                    att.is_verified = True
                    att.save()
                    
                    # Add Points
                    profile, _ = DKPProfile.objects.get_or_create(character=att.character)
                    points = event.points_to_award
                    profile.current_dkp += points
                    profile.total_earned += points
                    profile.save()
                    
                    # Log
                    DKPLog.objects.create(
                        profile=profile,
                        amount=points,
                        reason=f"Event: {event.name}",
                        created_by=request.user
                    )
                    
                    # Notification (DM if linked)
                    if att.character.discord_id:
                         DiscordAnnouncement.objects.create(
                            message=f"[DM:{att.character.discord_id}] ✅ **{att.character.name}**, kehadiran kamu di event **{event.name}** sudah diverifikasi Admin!"
                        )
            except DKPAttendance.DoesNotExist:
                pass
                
        elif action == 'reject':
            att_id = request.POST.get('attendance_id')
            DKPAttendance.objects.filter(id=att_id).delete()

    attendances = DKPAttendance.objects.filter(event=event).select_related('character').order_by('is_verified', '-check_in_time')
    return render(request, 'dkp/attendance.html', {'event': event, 'attendances': attendances})

@login_required(login_url='/login/')
def boss_point_config_get(request):
    """Load boss point config from database"""
    config = BossPointConfig.get_config()
    return JsonResponse({'success': True, 'config': config.config})

@login_required(login_url='/login/')
def boss_point_config_save(request):
    """Save boss point config to database"""
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            config = BossPointConfig.get_config()
            config.config = data.get('config', {})
            config.updated_by = request.user.username
            config.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required
def dkp_reset_data(request):
    """Reset all DKP history data (admin only)."""
    if not request.user.is_staff:
        return redirect('index')
    
    if request.method == 'POST':
        reset_type = request.POST.get('reset_type', '')
        
        if reset_type == 'all_history':
            # Only delete transaction logs (preserve points, events, leaderboard)
            DKPLog.objects.all().delete()
        
        return redirect('web-dkp-my-profile')
    
    return redirect('web-dkp-my-profile')


# ======================================================
# TREASURY VIEWS
# ======================================================

from items.views import is_admin

def is_treasury_admin(user):
    """Check if user has treasury admin access (including Sub Admins)"""
    if is_admin(user):
        return True
    try:
        return user.admin_role.is_treasury_admin
    except AdminRole.DoesNotExist:
        return False


@login_required(login_url='/login/')
def treasury_page(request):
    """Main Treasury page - item distribution hub"""
    has_treasury_access = is_treasury_admin(request.user)

    # Get current user's profile and clan
    user_chars = Character.objects.filter(owner=request.user)
    user_profile = None
    user_clan = 'Valkyrie'
    
    if user_chars.exists():
        char = user_chars.first()
        user_profile, _ = DKPProfile.objects.get_or_create(character=char)
        if char.clan:
            user_clan = char.clan

    # Determine which clan is being viewed
    clan_choices = ['Valkyrie', 'Valhalla']
    selected_clan = request.GET.get('clan')

    if not has_treasury_access:
        # Non-admins can ONLY view their own clan
        selected_clan = user_clan
    else:
        # Admins can view any clan, but default to their own clan
        if not selected_clan or selected_clan not in clan_choices:
            selected_clan = user_clan

    from django.db.models import Q
    profiles = DKPProfile.objects.select_related('character')
    if selected_clan == 'Valkyrie':
        profiles = profiles.filter(Q(character__clan='Valkyrie') | Q(character__clan='') | Q(character__clan__isnull=True))
    else:
        profiles = profiles.filter(character__clan=selected_clan)
    profiles = profiles.order_by('character__name')

    # Get treasury config (clan-specific)
    config_obj = TreasuryItemConfig.get_config()
    full_config = config_obj.config
    clan_config = full_config.get(selected_clan, {
        'blue_books': [], 'blue_equipment': [], 'other_items': [], 'diamond_items': []
    })

    # Auto-cleanup logs older than 3 days
    from django.utils import timezone
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    TreasuryTransaction.objects.filter(created_at__lt=three_days_ago).delete()

    # Calculate available DKP based on locked requests
    frozen_dkp = 0
    if user_profile:
        for c_name, c_cats in full_config.items():
            for cat_name, cat_items in c_cats.items():
                for item in cat_items:
                    if item.get('currency', 'DKP') == 'DKP':
                        for req in item.get('requests', []):
                            if req.get('profile_id') == user_profile.id:
                                frozen_dkp += int(item.get('price', 0)) * int(req.get('quantity', 1))
    available_dkp = user_profile.current_dkp - frozen_dkp if user_profile else 0

    # Recent treasury transactions (Paginated)
    from django.core.paginator import Paginator
    recent_transactions = TreasuryTransaction.objects.select_related('profile__character', 'created_by').order_by('-created_at')
    
    if selected_clan in clan_choices:
        recent_transactions = recent_transactions.filter(clan=selected_clan)

    paginator = Paginator(recent_transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    from items.views import is_admin
    return render(request, 'dkp/treasury.html', {
        'profiles': profiles,
        'config': json.dumps(clan_config),
        'selected_clan': selected_clan,
        'clan_choices': clan_choices,
        'recent_transactions': page_obj,
        'is_super_admin': is_admin(request.user),
        'is_treasury_admin': has_treasury_access,
        'user_profile': user_profile,
        'user_clan': user_clan,
        'available_dkp': available_dkp,
    })


@login_required(login_url='/login/')
def treasury_config_get(request):
    """Load treasury item config from database (clan-specific)"""
    clan = request.GET.get('clan', 'Valkyrie')
    config_obj = TreasuryItemConfig.get_config()
    clan_config = config_obj.config.get(clan, {})
    return JsonResponse({'success': True, 'config': clan_config})


def get_available_dkp_for_profile(profile):
    from .models import TreasuryItemConfig
    config_obj = TreasuryItemConfig.get_config()
    frozen_dkp = 0
    full_config = config_obj.config
    for c_name, c_cats in full_config.items():
        for cat_name, cat_items in c_cats.items():
            for config_item in cat_items:
                if config_item.get('currency', 'DKP') == 'DKP':
                    for r in config_item.get('requests', []):
                        if r.get('profile_id') == profile.id:
                            frozen_dkp += int(config_item.get('price', 0)) * int(r.get('quantity', 1))
    return profile.current_dkp - frozen_dkp

@login_required(login_url='/login/')
def treasury_config_save(request):
    """Save treasury item config to database (clan-specific)"""
    if not is_treasury_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clan = data.get('clan', 'Valkyrie')
            new_clan_config = data.get('config', {})
            
            config_obj = TreasuryItemConfig.get_config()
            config_obj.config[clan] = new_clan_config
            config_obj.updated_by = request.user.username
            config_obj.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST required'}, status=405)


@login_required(login_url='/login/')
def treasury_request_item(request):
    """Add a member to the item request list if stock permits (with quantity)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_category = data.get('item_category')
            item_idx = data.get('item_idx')
            clan = data.get('clan', 'Valkyrie')
            quantity = int(data.get('quantity', 1))

            if item_category is None or item_idx is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            if quantity < 1:
                return JsonResponse({'error': 'Quantity must be at least 1.'}, status=400)

            # Get user profile
            user_chars = Character.objects.filter(owner=request.user)
            if not user_chars.exists():
                return JsonResponse({'error': 'You do not have a Character linked to your account to make requests.'}, status=403)
            
            char = user_chars.first()
            user_profile, _ = DKPProfile.objects.get_or_create(character=char)

            # Validate that EVERYONE (including admins) can only request items for their own clan
            user_clan = char.clan or 'Valkyrie'
            if clan != user_clan:
                return JsonResponse({'error': f'You can only request items for your own clan ({user_clan}).'}, status=403)

            config_obj = TreasuryItemConfig.get_config()
            clan_config = config_obj.config.get(clan, {})
            cat_list = clan_config.get(item_category, [])
            if not (0 <= int(item_idx) < len(cat_list)):
                return JsonResponse({'error': 'Item not found'}, status=404)

            item = cat_list[int(item_idx)]
            requests_list = item.get('requests', [])
            stock = int(item.get('max_per_person', 0))
            price = int(item.get('price', 0))
            currency = item.get('currency', 'DKP')

            # Prevent duplicate request
            for req in requests_list:
                if req.get('profile_id') == user_profile.id:
                    return JsonResponse({'error': 'You have already requested this item.'}, status=400)

            # Calculate total already requested quantity
            total_requested = sum(int(r.get('quantity', 1)) for r in requests_list)

            # Check stock limit
            if stock <= 0:
                return JsonResponse({'error': 'This item is out of stock.'}, status=400)

            remaining = stock - total_requested
            if remaining <= 0:
                return JsonResponse({'error': 'Request list is full for this item.'}, status=400)

            if quantity > remaining:
                return JsonResponse({'error': f'Only {remaining} unit(s) remaining. Please reduce your quantity.'}, status=400)

            # Calculate total cost
            total_cost = price * quantity

            # Calculate available DKP (Current DKP minus locked requests)
            available_dkp = get_available_dkp_for_profile(user_profile)

            # Prevent request if available DKP is insufficient
            if currency == 'DKP' and available_dkp < total_cost:
                return JsonResponse({'error': f'Insufficient Available DKP. You need {total_cost} DKP ({price} x {quantity}), but your available DKP is {available_dkp}.'}, status=400)

            item.setdefault('requests', []).append({
                "profile_id": user_profile.id,
                "character_name": user_profile.character.name,
                "dkp": user_profile.current_dkp,
                "user_id": request.user.id,
                "quantity": quantity
            })
            config_obj.save()

            # Refresh profile to sync any parallel updates before returning available_dkp
            user_profile.refresh_from_db()
            new_available_dkp = get_available_dkp_for_profile(user_profile)

            return JsonResponse({'success': True, 'message': f'Request submitted! ({quantity}x {item["name"]})', 'item': item, 'available_dkp': new_available_dkp})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST required'}, status=405)


@login_required(login_url='/login/')
def treasury_reject_request(request):
    """Reject an item request (Admins can reject any, Users can cancel their own)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_category = data.get('item_category')
            item_idx = data.get('item_idx')
            profile_id = data.get('profile_id')
            clan = data.get('clan', 'Valkyrie')

            if item_category is None or item_idx is None or profile_id is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Determine authorization
            owner = None
            user_chars = Character.objects.filter(owner=request.user)
            if user_chars.exists():
                owner, _ = DKPProfile.objects.get_or_create(character=user_chars.first())

            is_self_removal = owner and owner.id == int(profile_id)
            if not is_treasury_admin(request.user) and not is_self_removal:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            config_obj = TreasuryItemConfig.get_config()
            clan_config = config_obj.config.get(clan, {})
            cat_list = clan_config.get(item_category, [])
            if not (0 <= int(item_idx) < len(cat_list)):
                return JsonResponse({'error': 'Item not found'}, status=404)

            item = cat_list[int(item_idx)]
            requests = item.get('requests', [])
            item['requests'] = [r for r in requests if r.get('profile_id') != int(profile_id)]
            config_obj.save()

            # Refresh profile and calculate new available DKP if owner exists
            new_available_dkp = 0
            if owner:
                owner.refresh_from_db()
                new_available_dkp = get_available_dkp_for_profile(owner)

            return JsonResponse({'success': True, 'message': 'Request rejected.', 'item': item, 'available_dkp': new_available_dkp})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST required'}, status=405)


@login_required(login_url='/login/')
def treasury_assign(request):
    """Assign an item to a member - deduct DKP/Diamond (with quantity support)"""
    if not is_treasury_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_id = data.get('profile_id')
            item_name = data.get('item_name', '')
            item_category = data.get('item_category', '')
            item_idx = data.get('item_idx')
            unit_price = int(data.get('price', 0))
            currency = data.get('currency', 'DKP')
            clan = data.get('clan', 'all')
            note = data.get('note', '')

            if not profile_id or not item_name or unit_price <= 0:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            try:
                profile = DKPProfile.objects.select_related('character').get(id=profile_id)
            except DKPProfile.DoesNotExist:
                return JsonResponse({'error': 'Profile not found'}, status=404)

            # Look up request quantity from config
            req_quantity = 1
            config_obj = None
            item_ref = None
            if item_idx is not None:
                try:
                    config_obj = TreasuryItemConfig.get_config()
                    clan_config = config_obj.config.get(clan, {})
                    cat_items = clan_config.get(item_category, [])
                    if 0 <= int(item_idx) < len(cat_items):
                        item_ref = cat_items[int(item_idx)]
                        unit_price = int(item_ref.get('price', 0))
                        for req in item_ref.get('requests', []):
                            if req.get('profile_id') == profile.id:
                                req_quantity = int(req.get('quantity', 1))
                                break
                except Exception:
                    pass

            total_price = unit_price * req_quantity

            # Deduct from DKP balance (only for DKP currency)
            if currency == 'DKP':
                if profile.current_dkp < total_price:
                    return JsonResponse({'error': f'Assign Failed! Member DKP is insufficient (Balance: {profile.current_dkp} DKP, Needed: {total_price} DKP) due to recent deductions.'}, status=400)
                
                profile.current_dkp -= total_price
                profile.save()

                # Create DKP log entry
                log_reason = f"Treasury: {item_name}" if req_quantity == 1 else f"Treasury: {item_name} (x{req_quantity})"
                DKPLog.objects.create(
                    profile=profile,
                    amount=-total_price,
                    reason=log_reason,
                    note=note,
                    created_by=request.user
                )

            # Create treasury transaction log
            txn_item_name = f"{item_name} (x{req_quantity})" if req_quantity > 1 else item_name
            txn = TreasuryTransaction.objects.create(
                profile=profile,
                item_name=txn_item_name,
                item_category=item_category,
                amount_deducted=total_price,
                currency=currency,
                clan=clan,
                note=note,
                created_by=request.user
            )

            # Decrement Stock/Max in config and remove request
            if item_ref is not None and config_obj is not None:
                current_max = int(item_ref.get('max_per_person', 0))
                if current_max > 0:
                    new_max = max(0, current_max - req_quantity)
                    item_ref['max_per_person'] = new_max
                
                # Remove assigned user from requests
                requests_list = item_ref.get('requests', [])
                item_ref['requests'] = [r for r in requests_list if r.get('profile_id') != profile.id]
                config_obj.save()

            # Auto-cleanup logs older than 3 days
            from django.utils import timezone
            three_days_ago = timezone.now() - timezone.timedelta(days=3)
            TreasuryTransaction.objects.filter(created_at__lt=three_days_ago).delete()

            return JsonResponse({
                'success': True,
                'message': f'{txn_item_name} assigned to {profile.character.name}',
                'new_dkp': profile.current_dkp,
                'character_name': profile.character.name,
                'admin_name': request.user.username,
                'date': txn.created_at.strftime("%d %b %Y %H:%M"),
                'currency': currency,
                'price': total_price,
                'item_name': txn_item_name,
                'txn_id': txn.id,
                'quantity': req_quantity
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST required'}, status=405)


@login_required(login_url='/login/')
def treasury_delete_logs(request):
    """Delete selected treasury transaction logs manually"""
    if not is_treasury_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            txn_ids_raw = data.get('txn_ids', [])
            txn_ids = []
            for t_id in txn_ids_raw:
                try:
                    txn_ids.append(int(t_id))
                except ValueError:
                    pass
            
            if txn_ids:
                deleted_count, _ = TreasuryTransaction.objects.filter(id__in=txn_ids).delete()
                return JsonResponse({'success': True, 'message': f'{deleted_count} logs deleted!'})
            else:
                return JsonResponse({'success': False, 'error': 'No valid IDs selected'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


# ============================================
# AUCTION SYSTEM
# ============================================

def is_auction_admin(user):
    """Check if user can manage auctions"""
    from items.views import is_admin
    if is_admin(user):
        return True
    try:
        role = user.admin_role
        return role.is_auction_admin
    except Exception:
        return False


@login_required(login_url='/login/')
def auction_page(request):
    """Auction management page"""
    if not is_auction_admin(request.user):
        return HttpResponseForbidden("You do not have access to manage Auctions.")
    
    auctions = Auction.objects.all().select_related('current_winner', 'created_by')
    
    # Auto-check for expired auctions and close them
    for auction in auctions:
        if auction.is_expired and auction.status == 'ACTIVE':
            _close_auction(auction)
    
    # Refresh after potential closures
    auctions = Auction.objects.all().select_related('current_winner', 'created_by')
    
    return render(request, 'dkp/auction.html', {
        'auctions': auctions,
        'is_auction_admin': True,
    })


@login_required(login_url='/login/')
def auction_create(request):
    """Create a new auction item"""
    if not is_auction_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            starting_bid = int(request.POST.get('starting_bid', 100))
            min_increment = int(request.POST.get('min_increment', 10))
            duration_minutes = int(request.POST.get('duration_minutes', 60))
            clan = request.POST.get('clan', 'All')
            image = request.FILES.get('image')
            
            if not title:
                return JsonResponse({'error': 'Item name is required'}, status=400)
            
            if image and image.size > 2 * 1024 * 1024:
                return JsonResponse({'error': 'Image file size must be under 2MB'}, status=400)
            
            auction = Auction.objects.create(
                title=title,
                description=description,
                starting_bid=starting_bid,
                min_increment=min_increment,
                duration_minutes=duration_minutes,
                clan=clan,
                image=image,
                created_by=request.user,
                status='DRAFT',
            )
            
            return JsonResponse({'success': True, 'message': f'Auction "{title}" created!', 'auction_id': auction.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required(login_url='/login/')
def auction_start(request):
    """Start an auction - changes status to ACTIVE and triggers Discord announcement"""
    if not is_auction_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            auction_id = data.get('auction_id')
            
            auction = Auction.objects.get(id=auction_id)
            if auction.status != 'DRAFT':
                return JsonResponse({'error': 'Only DRAFT auctions can be started'}, status=400)
            
            now = timezone.now()
            auction.status = 'ACTIVE'
            auction.started_at = now
            auction.ends_at = now + timezone.timedelta(minutes=auction.duration_minutes)
            auction.current_bid = auction.starting_bid
            auction.save()
            
            # Create Discord announcement
            image_url = ''
            if auction.image:
                image_url = request.build_absolute_uri(auction.image.url)
            
            end_time_wib = auction.ends_at + timezone.timedelta(hours=7)  # Convert to WIB
            end_time_str = end_time_wib.strftime('%d %b %Y %H:%M WIB')
            
            clan_text = 'ALL CLANS' if auction.clan == 'All' else f'Clan {auction.clan} Only'
            
            announce_msg = (
                f"[AUCTION_START]\n"
                f"ID:{auction.id}\n"
                f"TITLE:{auction.title}\n"
                f"DESC:{auction.description}\n"
                f"START_BID:{auction.starting_bid}\n"
                f"INCREMENT:{auction.min_increment}\n"
                f"DURATION:{auction.duration_minutes}m\n"
                f"ENDS:{end_time_str}\n"
                f"CLAN:{clan_text}\n"
                f"IMAGE:{image_url}"
            )
            
            DiscordAnnouncement.objects.create(message=announce_msg)
            
            return JsonResponse({'success': True, 'message': f'Auction "{auction.title}" is now LIVE!'})
        except Auction.DoesNotExist:
            return JsonResponse({'error': 'Auction not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required(login_url='/login/')
def auction_cancel(request):
    """Cancel an auction and refund all bids"""
    if not is_auction_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            auction_id = data.get('auction_id')
            
            auction = Auction.objects.get(id=auction_id)
            if auction.status not in ('DRAFT', 'ACTIVE'):
                return JsonResponse({'error': 'Cannot cancel a closed auction'}, status=400)
            
            # Refund current highest bidder if active
            if auction.status == 'ACTIVE' and auction.current_winner:
                winner = auction.current_winner
                # No actual DKP deduction during bidding - just release the hold
                # Mark all bids as refunded
                auction.bids.update(is_refunded=True)
            
            auction.status = 'CANCELLED'
            auction.save()
            
            # Announce cancellation
            DiscordAnnouncement.objects.create(
                message=f"[AUCTION_CANCEL]\nID:{auction.id}\nTITLE:{auction.title}"
            )
            
            return JsonResponse({'success': True, 'message': f'Auction "{auction.title}" cancelled.'})
        except Auction.DoesNotExist:
            return JsonResponse({'error': 'Auction not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required(login_url='/login/')
def auction_delete(request):
    """Delete a DRAFT or CANCELLED auction"""
    if not is_auction_admin(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            auction_id = data.get('auction_id')
            
            auction = Auction.objects.get(id=auction_id)
            if auction.status == 'ACTIVE':
                return JsonResponse({'error': 'Cannot delete an active auction. Cancel it first.'}, status=400)
            
            title = auction.title
            auction.delete()
            return JsonResponse({'success': True, 'message': f'Auction "{title}" deleted.'})
        except Auction.DoesNotExist:
            return JsonResponse({'error': 'Auction not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


def _close_auction(auction):
    """Internal helper to close an expired auction and process winner"""
    if auction.status != 'ACTIVE':
        return
    
    auction.status = 'CLOSED'
    
    if auction.current_winner:
        winner = auction.current_winner
        bid_amount = auction.current_bid
        
        # Deduct DKP from winner
        winner.current_dkp -= bid_amount
        if winner.current_dkp < 0:
            winner.current_dkp = 0
        winner.save()
        
        # Mark winning bid
        winning_bid = auction.bids.filter(profile=winner).order_by('-amount').first()
        if winning_bid:
            winning_bid.is_winner = True
            winning_bid.save()
        
        # Create DKP log
        DKPLog.objects.create(
            profile=winner,
            amount=-bid_amount,
            reason=f"Auction Won: {auction.title}",
            created_by=auction.created_by
        )
        
        # Announce winner
        DiscordAnnouncement.objects.create(
            message=(
                f"[AUCTION_END]\n"
                f"ID:{auction.id}\n"
                f"TITLE:{auction.title}\n"
                f"WINNER:{winner.character.name}\n"
                f"AMOUNT:{bid_amount}\n"
                f"DISCORD_ID:{winner.character.discord_id or ''}"
            )
        )
    else:
        # No bids - announce no winner
        DiscordAnnouncement.objects.create(
            message=f"[AUCTION_NOBID]\nID:{auction.id}\nTITLE:{auction.title}"
        )
    
    auction.save()


# ============================================
# AUCTION API ENDPOINTS (for Discord Bot)
# ============================================

@csrf_exempt
def api_auction_bid(request):
    """API for Discord bot to place bids"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    if not verify_api_key(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        data = json.loads(request.body)
        auction_id = data.get('auction_id')
        discord_id = data.get('discord_id')
        bid_amount = int(data.get('bid_amount', 0))
        
        # Find character by Discord ID
        try:
            character = Character.objects.get(discord_id=str(discord_id))
        except Character.DoesNotExist:
            return JsonResponse({'error': 'Discord not linked to any character. Please link on the website first.'}, status=404)
        
        profile, _ = DKPProfile.objects.get_or_create(character=character)
        
        # Get auction
        try:
            auction = Auction.objects.get(id=auction_id, status='ACTIVE')
        except Auction.DoesNotExist:
            return JsonResponse({'error': 'Auction not found or not active.'}, status=404)
        
        # Check if expired
        if auction.is_expired:
            _close_auction(auction)
            return JsonResponse({'error': 'This auction has already ended!'}, status=400)
        
        # Check clan eligibility
        if auction.clan != 'All':
            char_clan = character.clan or 'Valkyrie'
            if char_clan != auction.clan:
                return JsonResponse({'error': f'This auction is for {auction.clan} members only.'}, status=403)
        
        # Validate bid amount
        if bid_amount < auction.starting_bid:
            return JsonResponse({'error': f'Bid must be at least {auction.starting_bid} DKP (starting bid).'}, status=400)
        
        if auction.current_winner:
            min_bid = auction.current_bid + auction.min_increment
            if bid_amount < min_bid:
                return JsonResponse({'error': f'Bid must be at least {min_bid} DKP (current: {auction.current_bid} + increment: {auction.min_increment}).'}, status=400)
        
        # Check if bidding against self
        if auction.current_winner and auction.current_winner.id == profile.id:
            return JsonResponse({'error': 'You are already the highest bidder!'}, status=400)
        
        # Calculate available DKP (considering ALL active auction holds)
        held_dkp = 0
        active_bids = AuctionBid.objects.filter(
            profile=profile,
            auction__status='ACTIVE',
            is_refunded=False
        ).select_related('auction')
        
        for ab in active_bids:
            # Only count if this profile is the current leader of that auction
            if ab.auction.current_winner_id == profile.id:
                held_dkp += ab.amount
        
        available_dkp = profile.current_dkp - held_dkp
        
        if available_dkp < bid_amount:
            return JsonResponse({
                'error': f'Insufficient DKP. You have {profile.current_dkp} DKP total, {held_dkp} DKP held in other auctions, {available_dkp} DKP available.'
            }, status=400)
        
        # Place bid (previous leader is automatically released)
        AuctionBid.objects.create(
            auction=auction,
            profile=profile,
            amount=bid_amount,
        )
        
        # Update auction
        old_winner = auction.current_winner
        old_winner_name = old_winner.character.name if old_winner else None
        old_winner_discord = old_winner.character.discord_id if old_winner else None
        
        auction.current_bid = bid_amount
        auction.current_winner = profile
        auction.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{character.name} is now the highest bidder with {bid_amount} DKP!',
            'character_name': character.name,
            'bid_amount': bid_amount,
            'previous_leader': old_winner_name,
            'previous_leader_discord': old_winner_discord,
            'auction_title': auction.title,
            'time_remaining': auction.time_remaining,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def api_auction_active(request):
    """API for Discord bot to list active auctions"""
    if not verify_api_key(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    auctions = Auction.objects.filter(status='ACTIVE').select_related('current_winner')
    data = []
    for a in auctions:
        # Check if expired
        if a.is_expired:
            _close_auction(a)
            continue
        
        data.append({
            'id': a.id,
            'title': a.title,
            'description': a.description,
            'current_bid': a.current_bid,
            'min_increment': a.min_increment,
            'current_leader': a.current_winner.character.name if a.current_winner else 'No bids yet',
            'time_remaining': a.time_remaining,
            'clan': a.clan,
            'total_bids': a.bids.count(),
        })
    
    return JsonResponse({'success': True, 'auctions': data})


@csrf_exempt
def api_auction_check_expired(request):
    """API for bot to check and close expired auctions"""
    if not verify_api_key(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    closed = []
    active_auctions = Auction.objects.filter(status='ACTIVE')
    for auction in active_auctions:
        if auction.is_expired:
            _close_auction(auction)
            closed.append({
                'id': auction.id,
                'title': auction.title,
                'winner': auction.current_winner.character.name if auction.current_winner else None,
                'amount': auction.current_bid if auction.current_winner else 0,
            })
    
    return JsonResponse({'success': True, 'closed_auctions': closed})
