import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from items.models import Character, CharacterAttributes

# Log in
User = get_user_model()
c = Client(SERVER_NAME='127.0.0.1')
user = User.objects.first()
c.force_login(user)

char = Character.objects.get(id=7)
# Get the edit page to see current form
response = c.get('/portal/character/edit/7/')

# Now POST the data back
post_data = {
    'name': char.name,
    'character_class': char.character_class,
    'unlocked_skills': '["Dignity (Rapier)"]'
}
response = c.post('/portal/character/edit/7/', post_data, follow=True)
print("Response status:", response.status_code)
if response.context is not None:
    if 'character_form' in response.context:
         print("Char Form errors:", response.context['character_form'].errors)
    if 'attributes_form' in response.context:
         print("Attr Form errors:", response.context['attributes_form'].errors)

attrs = CharacterAttributes.objects.get(character__id=7)
print("Skills in DB:", attrs.unlocked_skills)
