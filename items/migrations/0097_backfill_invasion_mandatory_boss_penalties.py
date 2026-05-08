from django.db import migrations


DEFAULT_MANDATORY_BOSS_PENALTIES = {
    'dragon_beast': 5,
    'carnifex': 5,
    'orfen': 5,
}


def backfill_invasion_mandatory_boss_penalties(apps, schema_editor):
    ActivityEvent = apps.get_model('items', 'ActivityEvent')
    events = ActivityEvent.objects.filter(
        is_mandatory=True,
        event_type__in=['INVASION', 'INV_DRAGON_BEAST', 'INV_CARNIFEX', 'INV_ORFEN'],
    )
    for event in events:
        if not event.mandatory_boss_penalties:
            event.mandatory_boss_penalties = DEFAULT_MANDATORY_BOSS_PENALTIES.copy()
            event.save(update_fields=['mandatory_boss_penalties'])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0096_activityevent_scan_info'),
    ]

    operations = [
        migrations.RunPython(backfill_invasion_mandatory_boss_penalties, noop_reverse),
    ]
