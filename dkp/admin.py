from django.contrib import admin
from .models import DKPEvent, DKPProfile, DKPAttendance, DKPLog

class AttendanceInline(admin.TabularInline):
    model = DKPAttendance
    extra = 0
    # raw_id_fields = ('character',) # Character is not huge yet, dropdown ok

@admin.register(DKPEvent)
class DKPEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'is_active', 'is_finalized', 'points_to_award', 'participant_count')
    inlines = [AttendanceInline]
    actions = ['finalize_event']

    def participant_count(self, obj):
        return obj.attendances.count()

    @admin.action(description='Distribute Points to Verified Attendees')
    def finalize_event(self, request, queryset):
        count = 0
        for event in queryset:
            if event.is_finalized: continue
            
            verified = event.attendances.filter(is_verified=True)
            if not verified.exists():
                self.message_user(request, f"No verified attendees for {event.name}", level='warning')
                continue

            for att in verified:
                # Add points
                profile, _ = DKPProfile.objects.get_or_create(character=att.character)
                profile.current_dkp += event.points_to_award
                profile.total_earned += event.points_to_award
                profile.save()
                
                # Log
                DKPLog.objects.create(
                    profile=profile,
                    amount=event.points_to_award,
                    reason=f"Event: {event.name}",
                    created_by=request.user
                )
            
            event.is_finalized = True
            event.is_active = False # Close
            event.is_closed = True
            event.save()
            count += 1
            
        self.message_user(request, f"Finalized points for {count} events.")

@admin.register(DKPProfile)
class DKPProfileAdmin(admin.ModelAdmin):
    list_display = ('character', 'current_dkp', 'total_earned')
    search_fields = ('character__name',)
    
@admin.register(DKPLog)
class DKPLogAdmin(admin.ModelAdmin):
    list_display = ('profile', 'amount', 'reason', 'created_at', 'created_by')
    list_filter = ('created_at',)
    search_fields = ('profile__character__name',)
