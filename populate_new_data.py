import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

from items.models import LegendaryAgathion, LegendaryClass, LegendaryMount

# Add new agathions
new_agathions = [
    ("Abyssal Death Knight", "Icon_Agathion_AbyssalDeathKnight.png"),
    ("Akamanah", "Icon_Agathion_Akamanah.png"),
]
for name, icon in new_agathions:
    obj, created = LegendaryAgathion.objects.get_or_create(name=name, defaults={'icon_file': icon})
    print(f"Agathion: {name} -> {'CREATED' if created else 'EXISTS'}")

# Add new classes
new_classes = [
    ("Amadeo Cadmus", "Icon_Classcard_AmadeoCadmus.png"),
    ("Bartz", "Icon_Classcard_Bartz.png"),
    ("Etis Von Etina", "Icon_Classcard_EtisVonEtina.jpg"),
    ("Frintezza", "Icon_Classcard_Frintezza.jpg"),
    ("Kranvel", "Icon_Classcard_Kranvel.jpg"),
]
for name, icon in new_classes:
    obj, created = LegendaryClass.objects.get_or_create(name=name, defaults={'icon_file': icon})
    print(f"Class: {name} -> {'CREATED' if created else 'EXISTS'}")

# Add mounts
mounts = [
    ("Cerberus", "Icon_Mount_Cerberus.png"),
    ("Freyja", "Icon_Mount_Freyja.png"),
    ("Lucis", "Icon_Mount_Lucis.png"),
]
for name, icon in mounts:
    obj, created = LegendaryMount.objects.get_or_create(name=name, defaults={'icon_file': icon})
    print(f"Mount: {name} -> {'CREATED' if created else 'EXISTS'}")

print("\nDone! All data populated.")
