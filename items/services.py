# D:\Django Project\Alto Project\items\services.py
"""
Activity Calculation Services
Handles all the business logic for activity tracking, scoring, and prize distribution.
"""

from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime
from .models import ActivityEvent, PlayerActivity, MonthlyReport, Character, PrizePoolConfig

# Default Fallback Configuration
DEFAULT_CONFIG = {
    'total': 10000,
    'tier_allocation': {
        'ELITE': 0.20,
        'CORE': 0.70,
        'ACTIVE': 0.10,
        'CASUAL': 0.00,
    },
    'consistency_bonus': { # Keep this hardcoded for now or move to DB later
        90: 150,
        70: 100,
        50: 50,
    }
}

def get_active_config():
    """Retrieve the active prize pool configuration or default."""
    config = PrizePoolConfig.objects.last()
    if config:
        return {
            'total': config.total_pool,
            'tier_allocation': {
                'ELITE': config.elite_percentage,
                'CORE': config.core_percentage,
                'ACTIVE': config.active_percentage,
                'CASUAL': config.casual_percentage,
            },
            'consistency_bonus': DEFAULT_CONFIG['consistency_bonus']
        }
    return DEFAULT_CONFIG


def calculate_monthly_reports(year=None, month=None):
    """
    Calculate and update monthly reports for all players.
    Should be called after recording attendance or at end of month.
    
    Args:
        year: Target year (default: current year)
        month: Target month (default: current month)
    
    Returns:
        dict: Summary of calculations
    """
    if year is None or month is None:
        today = timezone.now()
        year = today.year
        month = today.month
    
    # Create month date (first day of month)
    month_date = datetime(year, month, 1).date()
    
    # Get all events for this month
    events = ActivityEvent.objects.filter(
        date__year=year,
        date__month=month
        # Include ALL events (completed or active) so score updates immediately
        # is_completed=True 
    )
    
    total_events = events.count()
    
    if total_events == 0:
        return {'status': 'no_events', 'message': 'No completed events found for this month'}
    
    # Get all characters
    characters = Character.objects.all()
    
    reports_updated = 0
    config = get_active_config()
    
    for character in characters:
        # Get all activities for this character this month
        activities = PlayerActivity.objects.filter(
            player=character,
            event__in=events,
            status='ATTENDED'
        )
        
        # Calculate stats
        attended_events = activities.count()
        attendance_rate = (attended_events / total_events) if total_events > 0 else 0
        activity_score = activities.aggregate(total=Sum('points_earned'))['total'] or 0
        
        # Calculate consistency bonus
        consistency_bonus = 0
        for threshold, bonus in sorted(config['consistency_bonus'].items(), reverse=True):
            if attendance_rate * 100 >= threshold:
                consistency_bonus = bonus
                break
        
        # Total score
        total_score = activity_score + consistency_bonus
        
        # Update or create monthly report
        report, created = MonthlyReport.objects.update_or_create(
            month=month_date,
            player=character,
            defaults={
                'total_events': total_events,
                'attended_events': attended_events,
                'attendance_rate': attendance_rate,
                'activity_score': activity_score,
                'consistency_bonus': consistency_bonus,
                'total_score': total_score,
            }
        )
        reports_updated += 1
    
    # After updating all reports, calculate prize distribution
    calculate_prize_distribution(year, month)
    
    return {
        'status': 'success',
        'month': month_date.strftime('%B %Y'),
        'total_events': total_events,
        'reports_updated': reports_updated,
    }


def calculate_prize_distribution(year, month):
    """
    Calculate prize distribution for all qualified players.
    Uses proportional distribution within each tier.
    
    Args:
        year: Target year
        month: Target month
    """
    month_date = datetime(year, month, 1).date()
    
    # LOAD DYNAMIC CONFIG
    config = get_active_config()
    total_pool = config['total']
    allocations = config['tier_allocation']
    
    # Get all reports for this month
    reports = MonthlyReport.objects.filter(month=month_date)
    
    # Calculate tier totals
    tier_data = {}
    for tier_code, allocation in allocations.items():
        tier_reports = reports.filter(tier=tier_code)
        tier_total_score = tier_reports.aggregate(total=Sum('total_score'))['total'] or 0
        tier_pool = total_pool * allocation
        
        tier_data[tier_code] = {
            'pool': tier_pool,
            'total_score': tier_total_score,
            'reports': tier_reports,
        }
    
    # Distribute prizes proportionally
    for tier_code, data in tier_data.items():
        if data['total_score'] > 0:
            for report in data['reports']:
                # Calculate proportional share
                share = report.total_score / data['total_score']
                prize = int(data['pool'] * share)
                
                report.prize_amount = prize
                report.save(update_fields=['prize_amount'])
        else:
            # No one in this tier, set prize to 0
            for report in data['reports']:
                report.prize_amount = 0
                report.save(update_fields=['prize_amount'])


def get_leaderboard_summary(year=None, month=None):
    """
    Get summary data for leaderboard display.
    
    Args:
        year: Target year (default: current year)
        month: Target month (default: current month)
    
    Returns:
        dict: Leaderboard summary data
    """
    if year is None or month is None:
        today = timezone.now()
        year = today.year
        month = today.month
    
    month_date = datetime(year, month, 1).date()
    
    reports = MonthlyReport.objects.filter(month=month_date).select_related('player')
    
    # Tier counts
    tier_counts = {
        'ELITE': reports.filter(tier='ELITE').count(),
        'CORE': reports.filter(tier='CORE').count(),
        'ACTIVE': reports.filter(tier='ACTIVE').count(),
        'CASUAL': reports.filter(tier='CASUAL').count(),
    }
    
    # Total stats
    total_qualified = reports.filter(is_qualified=True).count()
    total_prizes = reports.aggregate(total=Sum('prize_amount'))['total'] or 0
    
    # Top performers
    top_3 = reports.order_by('-total_score')[:3]
    
    return {
        'month': month_date,
        'tier_counts': tier_counts,
        'total_qualified': total_qualified,
        'total_prizes': total_prizes,
        'top_performers': top_3,
        'all_reports': reports.order_by('-total_score'),
    }


def recalculate_event_points(event):
    """
    Recalculate points for all participants of a specific event.
    Call this after updating event results (boss kills, win status).
    
    Args:
        event: ActivityEvent instance
    """
    # Iterate through all attended participants to update their individual points
    # We must call .save() on each instance so the model's save() method 
    # runs the point calculation logic (including Invasion per-player checks)
    activities = PlayerActivity.objects.filter(
        event=event,
        status='ATTENDED'
    )
    
    for activity in activities:
        activity.save()  # This triggers the self.points_earned calculation
    
    # Also recalculate monthly reports
    calculate_monthly_reports(event.date.year, event.date.month)
