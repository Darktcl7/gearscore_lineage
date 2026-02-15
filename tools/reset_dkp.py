
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from dkp.models import DKPEvent, DKPAttendance, DKPProfile, DKPLog

print("🧹 Starting DKP Cleanup...")

# Delete in order of dependency
count_log = DKPLog.objects.all().delete()[0]
print(f"Deleted {count_log} DKP Logs")

count_att = DKPAttendance.objects.all().delete()[0]
print(f"Deleted {count_att} Attendances")

count_profile = DKPProfile.objects.all().delete()[0]
print(f"Deleted {count_profile} Profiles")

count_event = DKPEvent.objects.all().delete()[0]
print(f"Deleted {count_event} Events")

print("✅ ALL DKP DATA CLEARED!")
