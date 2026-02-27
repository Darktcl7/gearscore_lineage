import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()
c = Client()
try:
    user = User.objects.first()
    c.force_login(user)
    response = c.get('/portal/character/edit/7/')
    html = response.content.decode('utf-8')
    print("COUNT target:", html.count("name=\"unlocked_skills\""))
    for line in html.split('\n'):
        if 'unlocked_skills' in line:
            print(line.strip())
except Exception as e:
    print('error', e)
