# D:\Django Project\Alto Project\items\management\commands\recalculate_activity.py
"""
Management command to recalculate monthly activity reports.
Usage: python manage.py recalculate_activity [--month YYYY-MM]
"""

from django.core.management.base import BaseCommand
from items.services import calculate_monthly_reports
from django.utils import timezone


class Command(BaseCommand):
    help = 'Recalculate monthly activity reports for all players'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--month',
            type=str,
            help='Target month in YYYY-MM format (default: current month)',
        )
    
    def handle(self, *args, **options):
        month_str = options.get('month')
        
        if month_str:
            try:
                year, month = map(int, month_str.split('-'))
            except ValueError:
                self.stderr.write(self.style.ERROR('Invalid month format. Use YYYY-MM.'))
                return
        else:
            today = timezone.now()
            year = today.year
            month = today.month
        
        self.stdout.write(f'Calculating reports for {year}-{month:02d}...')
        
        result = calculate_monthly_reports(year, month)
        
        if result.get('status') == 'success':
            self.stdout.write(self.style.SUCCESS(
                f"✅ Successfully updated {result['reports_updated']} reports for {result['month']}"
            ))
            self.stdout.write(f"   Total events: {result['total_events']}")
        elif result.get('status') == 'no_events':
            self.stdout.write(self.style.WARNING(f"⚠️ {result['message']}"))
        else:
            self.stdout.write(self.style.ERROR(f"❌ Error: {result}"))
