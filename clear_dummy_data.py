import os
import sys

# Script to clear dummy Activity and DKP data

def clear_data():
    from dkp.models import DKPEvent, DKPAttendance, DKPLog, DKPProfile
    from items.models import ActivityEvent, PlayerActivity, MonthlyReport

    print("Deleting ActivityEvent, PlayerActivity, and MonthlyReport records...")
    ActivityEvent.objects.all().delete()
    PlayerActivity.objects.all().delete()
    MonthlyReport.objects.all().delete()

    print("Deleting DKPEvent, DKPAttendance, and DKPLog records...")
    DKPEvent.objects.all().delete()
    DKPAttendance.objects.all().delete()
    DKPLog.objects.all().delete()

    print("Resetting DKP Profiles to 0...")
    profiles = DKPProfile.objects.all()
    profiles.update(current_dkp=0, total_earned=0, last_decay_percent=0)

    print("All dummy DKP and Activity data cleared successfully!")

if __name__ == "__main__":
    clear_data()
