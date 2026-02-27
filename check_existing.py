import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

from items.models import LegendaryAgathion, LegendaryClass

print('=== Existing Agathions ===')
for a in LegendaryAgathion.objects.all():
    print(f'  {a.name} -> {a.icon_file}')

print()
print('=== Existing Classes ===')
for c in LegendaryClass.objects.all():
    print(f'  {c.name} -> {c.icon_file}')

# Check if Mount model exists
try:
    from items.models import LegendaryMount
    print('\n=== LegendaryMount model EXISTS ===')
    for m in LegendaryMount.objects.all():
        print(f'  {m.name} -> {m.icon_file}')
except ImportError:
    print('\n=== LegendaryMount model DOES NOT EXIST ===')
