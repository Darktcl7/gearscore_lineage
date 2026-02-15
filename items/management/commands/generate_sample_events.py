# D:\Django Project\Alto Project\items\management\commands\generate_sample_events.py
"""
Management command to generate sample events for testing.
Usage: python manage.py generate_sample_events [--count N]
"""

from django.core.management.base import BaseCommand
from items.models import ActivityEvent, PlayerActivity, Character
from items.services import calculate_monthly_reports
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Generate sample activity events for testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of events to generate (default: 10)',
        )
        parser.add_argument(
            '--with-attendance',
            action='store_true',
            help='Also generate random attendance for each event',
        )
    
    def handle(self, *args, **options):
        count = options['count']
        with_attendance = options['with_attendance']
        
        self.stdout.write(f'Generating {count} sample events...')
        
        event_types = ['INVASION', 'BOSS_RUSH', 'CATACOMBS']
        events_created = 0
        
        for i in range(count):
            event_type = random.choice(event_types)
            days_ago = random.randint(0, 30)
            event_date = timezone.now() - timedelta(days=days_ago)
            
            # Generate boss kills for invasion
            bosses_killed = {}
            if event_type == 'INVASION':
                bosses_killed = {
                    'dragon_beast': random.random() > 0.3,
                    'carnifex': random.random() > 0.4,
                    'orfen': random.random() > 0.6,
                }
            
            event = ActivityEvent.objects.create(
                event_type=event_type,
                name=f"{event_type.replace('_', ' ').title()} #{i+1}",
                date=event_date,
                is_completed=True,
                is_win=random.random() > 0.4,
                bosses_killed=bosses_killed,
            )
            events_created += 1
            
            if with_attendance:
                characters = Character.objects.all()
                attendance_count = 0
                
                for char in characters:
                    # Random attendance (70% chance)
                    if random.random() > 0.3:
                        PlayerActivity.objects.create(
                            player=char,
                            event=event,
                            status='ATTENDED',
                        )
                        attendance_count += 1
                    else:
                        PlayerActivity.objects.create(
                            player=char,
                            event=event,
                            status='ABSENT',
                            points_earned=0,
                        )
                
                self.stdout.write(f"  Created {event.name} with {attendance_count} attendees")
        
        self.stdout.write(self.style.SUCCESS(f"✅ Created {events_created} events"))
        
        if with_attendance:
            self.stdout.write("Recalculating monthly reports...")
            result = calculate_monthly_reports()
            if result.get('status') == 'success':
                self.stdout.write(self.style.SUCCESS(
                    f"✅ Updated {result['reports_updated']} player reports"
                ))
