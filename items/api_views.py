# D:\Django Project\Alto Project\items\api_views.py
"""
API Views for Discord Bot Integration (Phase 2)
These endpoints will be called by the Discord Bot to sync data.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
import json
from datetime import datetime

from .models import ActivityEvent, PlayerActivity, Character, MonthlyReport, DiscordAlarm, DiscordAnnouncement
from .services import calculate_monthly_reports, recalculate_event_points

# ... (Existing code) ...

@csrf_exempt
@require_http_methods(["GET"])
def api_get_discord_alarms(request):
    """Get all active alarms for bot sync"""
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    alarms = DiscordAlarm.objects.filter(is_active=True).values('day', 'time', 'message')
    
    alarm_list = []
    for a in alarms:
        alarm_list.append({
            'day': a['day'],
            'time': a['time'].strftime('%H:%M'),
            'msg': a['message']
        })
        
    return JsonResponse({'success': True, 'alarms': alarm_list})


@csrf_exempt
@require_http_methods(["GET"])
def api_check_discord_announcements(request):
    """Bot calls this periodically to check for broadcasts"""
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    announcement = DiscordAnnouncement.objects.filter(is_sent=False).order_by('created_at').first()
    
    if announcement:
        announcement.is_sent = True
        announcement.sent_at = datetime.now()
        announcement.save()
        
        return JsonResponse({
            'success': True,
            'has_new': True,
            'message': announcement.message
        })
    else:
        return JsonResponse({'success': True, 'has_new': False})


# Simple API Key authentication (replace with proper auth in production)
API_KEY = "alto-discord-bot-key-2026"


def verify_api_key(request):
    """Verify API key from request header"""
    key = request.headers.get('X-API-Key', '')
    return key == API_KEY


@csrf_exempt
@require_http_methods(["POST"])
def api_create_event(request):
    """
    Create a new event from Discord Bot.
    
    POST /api/activity/event/create/
    Headers: X-API-Key: your-api-key
    Body: {
        "event_type": "INVASION",
        "name": "Weekly Invasion #10",
        "date": "2026-01-31T20:00:00",
        "discord_message_id": "123456789"  # Optional, for reference
    }
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        data = json.loads(request.body)
        
        event = ActivityEvent.objects.create(
            event_type=data.get('event_type'),
            name=data.get('name', f"{data.get('event_type')} Event"),
            date=datetime.fromisoformat(data.get('date')),
            is_completed=False,
        )
        
        return JsonResponse({
            'success': True,
            'event_id': event.event_id,
            'message': f"Event created: {event.name}"
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_record_checkin(request):
    """
    Record a player check-in from Discord.
    
    POST /api/activity/checkin/
    Headers: X-API-Key: your-api-key
    Body: {
        "event_id": "INVASION_ABC12345",
        "discord_user_id": "123456789012345678",
        "character_name": "SonOfZeus"  # Optional, if discord_id not linked
    }
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        data = json.loads(request.body)
        
        # Find event
        event = ActivityEvent.objects.get(event_id=data.get('event_id'))
        
        # Validate event is still active (not completed)
        if event.is_completed:
            return JsonResponse({
                'error': 'Event sudah selesai',
                'message': 'Event ini sudah berakhir dan tidak menerima check-in lagi.'
            }, status=400)
        
        # Find character ONLY by discord_user_id (must be linked first!)
        discord_id = data.get('discord_user_id')
        
        if not discord_id:
            return JsonResponse({
                'error': 'Discord not linked',
                'message': 'Discord ID tidak ditemukan dalam request.'
            }, status=400)
        
        # Find character by linked Discord ID
        character = Character.objects.filter(discord_id=discord_id).first()
        
        if not character:
            return JsonResponse({
                'error': 'Discord not linked',
                'message': 'Discord kamu belum ter-link dengan karakter. Silakan link di website terlebih dahulu.'
            }, status=404)
        
        # Check if already checked in
        existing_activity = PlayerActivity.objects.filter(
            player=character,
            event=event
        ).first()

        if existing_activity and existing_activity.status == 'ATTENDED':
             return JsonResponse({
                'success': True, # Still success to not trigger error in Discord UI
                'already_checked_in': True,
                'character': character.name,
                'event': event.name,
                'points': existing_activity.points_earned,
                'message': f"Kamu sudah check-in sebelumnya sebagai {character.name}!"
            })
        
        # Record attendance
        activity, created = PlayerActivity.objects.update_or_create(
            player=character,
            event=event,
            defaults={
                'status': 'ATTENDED',
                'discord_user_id': discord_id or '',
            }
        )
        
        # Update monthly report leaderboard immediately
        calculate_monthly_reports(event.date.year, event.date.month)
        
        return JsonResponse({
            'success': True,
            'character': character.name,
            'event': event.name,
            'points': activity.points_earned,
            'message': f"Check-in recorded for {character.name}!"
        })
    
    except ActivityEvent.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_complete_event(request):
    """
    Mark event as complete and record results.
    
    POST /api/activity/event/complete/
    Headers: X-API-Key: your-api-key
    Body: {
        "event_id": "INVASION_ABC12345",
        "is_win": true,  # For Boss Rush / Catacombs
        "bosses_killed": {  # For Invasion
            "dragon_beast": true,
            "carnifex": true,
            "orfen": false
        }
    }
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        data = json.loads(request.body)
        
        event = ActivityEvent.objects.get(event_id=data.get('event_id'))
        
        # Update event results
        event.is_completed = True
        event.is_win = data.get('is_win', False)
        
        if 'bosses_killed' in data:
            event.bosses_killed = data.get('bosses_killed')
        
        event.save()
        
        # Recalculate points for all participants
        recalculate_event_points(event)
        
        # Get participant count
        participant_count = event.participants.filter(status='ATTENDED').count()
        
        return JsonResponse({
            'success': True,
            'event_id': event.event_id,
            'max_points': event.calculate_max_points(),
            'participants': participant_count,
            'message': f"Event completed! {participant_count} players earned points."
        })
    
    except ActivityEvent.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def api_get_leaderboard(request):
    """
    Get current month leaderboard.
    
    GET /api/activity/leaderboard/
    Headers: X-API-Key: your-api-key
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        from django.utils import timezone
        today = timezone.now()
        
        reports = MonthlyReport.objects.filter(
            month__year=today.year,
            month__month=today.month
        ).select_related('player').order_by('-total_score')[:10]
        
        leaderboard = []
        for i, report in enumerate(reports, 1):
            leaderboard.append({
                'rank': i,
                'player': report.player.name,
                'score': report.total_score,
                'tier': report.get_tier_display(),
                'prize': report.prize_amount if report.is_qualified else 0,
            })
        
        return JsonResponse({
            'success': True,
            'month': today.strftime('%B %Y'),
            'leaderboard': leaderboard
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def api_player_stats(request, character_name):
    """
    Get a player's current month stats.
    
    GET /api/activity/player/<character_name>/
    Headers: X-API-Key: your-api-key
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        from django.utils import timezone
        today = timezone.now()
        
        character = Character.objects.filter(name__iexact=character_name).first()
        
        if not character:
            return JsonResponse({'error': 'Character not found'}, status=404)
        
        report = MonthlyReport.objects.filter(
            player=character,
            month__year=today.year,
            month__month=today.month
        ).first()
        
        if report:
            return JsonResponse({
                'success': True,
                'player': character.name,
                'total_score': report.total_score,
                'tier': report.get_tier_display(),
                'attendance': f"{report.attendance_rate * 100:.1f}%",
                'events_joined': report.attended_events,
                'total_events': report.total_events,
                'estimated_prize': report.prize_amount if report.is_qualified else 0,
            })
        else:
            return JsonResponse({
                'success': True,
                'player': character.name,
                'total_score': 0,
                'tier': '🌱 Casual',
                'attendance': '0%',
                'events_joined': 0,
                'total_events': 0,
                'estimated_prize': 0,
            })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def api_player_stats_discord(request, discord_id):
    """
    Get a player's current month stats by Discord ID.
    GET /api/activity/player/discord/<discord_id>/
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        from django.utils import timezone
        today = timezone.now()
        
        character = Character.objects.filter(discord_id=discord_id).first()
        
        if not character:
            return JsonResponse({'error': 'Discord not linked to any Character'}, status=404)
        
        report = MonthlyReport.objects.filter(
            player=character,
            month__year=today.year,
            month__month=today.month
        ).first()
        
        if report:
            return JsonResponse({
                'success': True,
                'player': character.name,
                'total_score': report.total_score,
                'tier': report.get_tier_display(),
                'attendance': f"{report.attendance_rate * 100:.1f}%",
                'events_joined': report.attended_events,
                'total_events': report.total_events,
                'estimated_prize': report.prize_amount if report.is_qualified else 0,
            })
        else:
            return JsonResponse({
                'success': True,
                'player': character.name,
                'total_score': 0,
                'tier': '🌱 Casual',
                'attendance': '0%',
                'events_joined': 0,
                'total_events': 0,
                'estimated_prize': 0,
            })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def api_get_active_events(request):
    """
    Get list of active (incomplete) events.
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        events = ActivityEvent.objects.filter(is_completed=False).order_by('-date')
        
        event_list = []
        for event in events:
            event_list.append({
                'event_id': event.event_id,
                'name': event.name,
                'type': event.event_type,
                'date': event.date.strftime('%Y-%m-%d %H:%M'),
                'participants': event.participants.count()
            })
            
        return JsonResponse({'success': True, 'events': event_list})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_toggle_event_status(request, event_pk):
    """
    Toggle event status (Open/Completed).
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        event = ActivityEvent.objects.get(pk=event_pk)
        event.is_completed = not event.is_completed
        event.save()
        
        status_text = "Completed" if event.is_completed else "Re-opened"
        return JsonResponse({
            'success': True, 
            'message': f'Event {event.name} is now {status_text}',
            'is_completed': event.is_completed
        })
        
    except ActivityEvent.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_toggle_event_result(request, event_pk):
    """
    Toggle event result (Win/Lose) for Boss Rush / Catacombs.
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        event = ActivityEvent.objects.get(pk=event_pk)
        if event.event_type == 'INVASION':
             return JsonResponse({'error': 'Invasion result cannot be toggled simply.'}, status=400)
             
        event.is_win = not event.is_win
        event.save()
        
        # Recalculate points for all participants because result changed points
        recalculate_event_points(event)
        
        # Also need to update monthly reports since points changed
        calculate_monthly_reports(event.date.year, event.date.month)

        result_text = "Win" if event.is_win else "Lose"
        return JsonResponse({
            'success': True, 
            'message': f'Event {event.name} result changed to {result_text}',
            'is_win': event.is_win
        })
        
    except ActivityEvent.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_update_event_result(request, event_pk):
    """
    Update detailed event result (especially for Invasion bosses).
    """
    try:
        if not verify_api_key(request):
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
            
        try:
            event = ActivityEvent.objects.get(pk=event_pk)
        except ActivityEvent.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        
        # Update bosses killed - Ensure it's a dict
        if 'bosses_killed' in data:
            bosses = data['bosses_killed']
            if isinstance(bosses, dict):
                event.bosses_killed = bosses
            else:
                 return JsonResponse({'error': 'bosses_killed must be a dictionary'}, status=400)
            
        event.save()
        
        # Recalculate points
        recalculate_event_points(event)
        
        return JsonResponse({
            'success': True, 
            'message': f'Event {event.name} result updated',
            'bosses_killed': event.bosses_killed
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc() # Print error to server console
        return JsonResponse({'error': f"Internal Error: {str(e)}"}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_delete_event(request):
    """
    Delete an event via API.
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        data = json.loads(request.body)
        event_id = data.get('event_id')
        
        event = ActivityEvent.objects.get(event_id=event_id)
        
        # Delete related activities first
        PlayerActivity.objects.filter(event=event).delete()
        event.delete()
        
        return JsonResponse({'success': True, 'message': f'Event {event_id} deleted'})
        
    except ActivityEvent.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
