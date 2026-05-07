from django.db import migrations, models


def backfill_existing_attendance(apps, schema_editor):
    PlayerActivity = apps.get_model('items', 'PlayerActivity')
    PlayerActivity.objects.filter(status='ATTENDED').update(checkin_verified=True)


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0094_warpointconfig_auto_delete_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='playeractivity',
            name='checkin_verified',
            field=models.BooleanField(default=False, verbose_name='Check-in Verified'),
        ),
        migrations.AddField(
            model_name='playeractivity',
            name='party_scan_verified',
            field=models.BooleanField(default=False, verbose_name='Party Scan Verified'),
        ),
        migrations.RunPython(backfill_existing_attendance, migrations.RunPython.noop),
    ]
