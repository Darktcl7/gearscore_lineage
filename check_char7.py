import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.models import CharacterAttributes

a = CharacterAttributes.objects.filter(character_id=7).first()
if a:
    fields = ['pvp_helmet','pvp_gloves','pvp_boots','pvp_gaiters','pvp_top_armor','pvp_cloak','pvp_sigil']
    for f in fields:
        val = getattr(a, f, '')
        enc = getattr(a, f+'_enchant', 0)
        print(f"{f}: [{val}] +{enc}")
else:
    print("No attrs for char 7")
