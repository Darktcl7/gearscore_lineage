from django.db import models
from django.utils import timezone
from items.models import Character
from django.contrib.auth.models import User

class DKPProfile(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='dkp_profile')
    current_dkp = models.IntegerField("Current DKP", default=0)
    total_earned = models.IntegerField("Total Earned (Lifetime)", default=0)
    last_decay_percent = models.FloatField("Last Decay %", default=0, blank=True)
    
    def __str__(self):
        return f"{self.character.name} - {self.current_dkp} DKP"

    class Meta:
        verbose_name = "DKP Profile"

class DKPEvent(models.Model):
    name = models.CharField("Nama Event", max_length=200)
    date = models.DateTimeField("Tanggal", default=timezone.now)
    
    is_active = models.BooleanField("Open Check-in", default=True) 
    is_closed = models.BooleanField("Check-in Closed", default=False)
    is_finalized = models.BooleanField("Points Distributed", default=False)
    
    points_to_award = models.IntegerField("Points Reward", default=10)
    
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.date.strftime('%d/%m/%Y')})"

class DKPAttendance(models.Model):
    event = models.ForeignKey(DKPEvent, on_delete=models.CASCADE, related_name='attendances')
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField("Verified", default=False)
    
    class Meta:
        unique_together = ('event', 'character')
        verbose_name = "DKP Attendance"

class DKPLog(models.Model):
    profile = models.ForeignKey(DKPProfile, on_delete=models.CASCADE, related_name='logs')
    amount = models.IntegerField("Jumlah")
    reason = models.CharField("Alasan", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.profile.character.name}: {self.amount} ({self.reason})"
