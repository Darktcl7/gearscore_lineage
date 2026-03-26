import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
django.setup()

from items.models import InheritorBook

new_books = [
    'Increase Agility',
    'Increase Wisdom',
    'Increase Constitution',
    'Salvation',
    'Stun Resist I',
    'Hold Resist',
    'Increase Stun I',
    'Increase Skill Power I',
    'Increase Retribution',
    'High Accuracy',
    'High Potion II',
    'Royal Weapon Mastery',
    'Weapon Block III',
    'Piercing Reduction II',
    'Eternal Life',
    'Invincible Champion',
    'Punishment',
    'Increase Attack Speed',
]

for name in new_books:
    obj, created = InheritorBook.objects.get_or_create(name=name)
    status = "CREATED" if created else "EXISTS"
    print(f"  {status}: {name}")

print(f"\nTotal InheritorBook entries: {InheritorBook.objects.count()}")
