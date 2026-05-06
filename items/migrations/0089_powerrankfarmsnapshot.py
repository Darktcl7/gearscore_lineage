from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0088_playeractivity_dkp_penalty_amount_applied_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowerRankFarmSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tab', models.CharField(choices=[('overall', 'Overall'), ('valkyrie', 'Valkyrie'), ('valhalla', 'Valhalla')], max_length=20, unique=True)),
                ('snapshot_data', models.JSONField(blank=True, default=list)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
            options={
                'verbose_name': 'Power Rank Farm Snapshot',
                'verbose_name_plural': 'Power Rank Farm Snapshots',
            },
        ),
    ]
