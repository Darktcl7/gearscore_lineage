import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

from items.models import LegendaryAgathion, LegendaryClass, LegendaryMount, MythicClass

# 1. Mythic Classes
mythics = [
    ("No mythic class", "х3.png"),
    ("Elcadia", "Icon_Classcard_Elcadia.png"),
    ("Elhwynha", "Icon_Classcard_Elhwynha.png"),
    ("Raoul", "Icon_Classcard_Raoul.png"),
]
for name, icon in mythics:
    obj, created = MythicClass.objects.get_or_create(name=name, defaults={'icon_file': icon})
    print(f"Mythic: {name} -> {'CREATED' if created else 'EXISTS'}")

# 2. Make sure "No legendary class" exists
obj, created = LegendaryClass.objects.get_or_create(name="No legendary class", defaults={'icon_file': "х3.png"})

# 3. Make sure "No legendary mount" exists
obj, created = LegendaryMount.objects.get_or_create(name="No legendary mount", defaults={'icon_file': "х3.png"})

# 4. Make sure "No legendary agathions" exists
obj, created = LegendaryAgathion.objects.get_or_create(name="No legendary agathions", defaults={'icon_file': "х3.png"})

print("Done population.")
