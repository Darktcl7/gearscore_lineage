from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import DKPEvent, DKPAttendance, DKPProfile, DKPLog
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
    
    profiles = DKPProfile.objects.order_by('-current_dkp')[:20]
    data = []
    rank = 1
    for p in profiles:
        data.append({
            'rank': rank,
            'character': p.character.name,
            'dkp': p.current_dkp
        })
        rank += 1
        

    return JsonResponse({
        'success': True,
        'leaderboard': data
    })

def dkp_leaderboard_web(request):
    profiles = DKPProfile.objects.select_related('character').order_by('-current_dkp')
    is_admin = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
    return render(request, 'dkp/leaderboard.html', {'profiles': profiles, 'is_admin': is_admin})

@login_required(login_url='/login/')
def dkp_decay(request):
    """Apply DKP decay to a single player - max 5%"""
    if not (request.user.is_staff or request.user.is_superuser):
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
    if not (request.user.is_staff or request.user.is_superuser):
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
    if not (request.user.is_staff or request.user.is_superuser):
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
    if not (request.user.is_staff or request.user.is_superuser):
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
    if not (request.user.is_staff or request.user.is_superuser):
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
    if not (request.user.is_staff or request.user.is_superuser):
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
    if not (request.user.is_staff or request.user.is_superuser):
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
    
    profiles = []
    if user_chars.exists():
        for char in user_chars:
            p, _ = DKPProfile.objects.get_or_create(character=char)
            # Fetch logs too?
            p.recent_logs = p.logs.order_by('-created_at')[:10]
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
            p.recent_logs = p.logs.order_by('-created_at')[:10]
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
        p.recent_logs = p.logs.order_by('-created_at')[:5]
    
    return render(request, 'dkp/all_wallets.html', {'profiles': profiles})

from items.models import ActivityEvent

@login_required(login_url='/login/')
def dkp_manage(request):
    if not request.user.is_staff:
        return redirect('index')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            name = request.POST.get('name')
            code = request.POST.get('code')
            value = request.POST.get('value')
            if name and value:
                # 1. Close ALL running events first to prevent duplicates
                # This ensures only 1 event is active at a time
                DKPEvent.objects.filter(is_active=True).update(is_active=False, is_closed=True)
                
                # 2. Create the new event
                final_name = f"{name} ({code})" if code else name
                
                DKPEvent.objects.create(
                    name=final_name,
                    points_to_award=value,
                    is_active=True
                )
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

        return redirect('web-dkp-manage')
            
    events = DKPEvent.objects.order_by('-date')
    return render(request, 'dkp/manage.html', {'events': events})

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
