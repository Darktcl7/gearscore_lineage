
import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import ActivityEvent, PlayerActivity, MonthlyReport
from items.services import calculate_monthly_reports

def fix_scores():
    print("🔄 Starting score recalculation...")
    
    # 1. Update semua PlayerActivity yang poinnya 0
    activities = PlayerActivity.objects.all()
    count = 0
    for activity in activities:
        # Force re-calculate points (akan pakai logic baru: min 5 pts)
        activity.points_earned = activity.event.calculate_max_points()
        activity.save()
        count += 1
        print(f"   - Fixed {activity.player.name} in {activity.event.name}: {activity.points_earned} pts")

    print(f"✅ Updated {count} activity records.")

    # 2. Recalculate Monthly Reports
    print("📊 Updating Leaderboard...")
    today = datetime.now()
    result = calculate_monthly_reports(today.year, today.month)
    
    print(f"✅ Leaderboard updated! {result['reports_updated']} players recalculated.")

if __name__ == '__main__':
    from datetime import datetime
    fix_scores()
