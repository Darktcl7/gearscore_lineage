from django.db import migrations


DEFAULT_PENALTIES_BY_EVENT_TYPE = {
    'INV_DRAGON_BEAST': {'dragon_beast': 5},
    'INV_CARNIFEX': {'carnifex': 5},
    'INV_ORFEN': {'orfen': 5},
}


def split_invasion_mandatory_boss_penalties(apps, schema_editor):
    ActivityEvent = apps.get_model('items', 'ActivityEvent')
    events = ActivityEvent.objects.filter(
        is_mandatory=True,
        event_type__in=list(DEFAULT_PENALTIES_BY_EVENT_TYPE.keys()),
    )
    for event in events:
        expected = DEFAULT_PENALTIES_BY_EVENT_TYPE[event.event_type]
        existing = event.mandatory_boss_penalties or {}
        boss_key = next(iter(expected))
        penalty = existing.get(boss_key, expected[boss_key])
        event.mandatory_boss_penalties = {boss_key: penalty}
        event.save(update_fields=['mandatory_boss_penalties'])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0097_backfill_invasion_mandatory_boss_penalties'),
    ]

    operations = [
        migrations.RunPython(split_invasion_mandatory_boss_penalties, noop_reverse),
    ]
