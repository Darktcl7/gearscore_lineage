import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.forms import CharacterAttributesForm
form = CharacterAttributesForm({'unlocked_skills': '["skill1", "skill2"]'})
form.is_valid()
print(form.errors)
