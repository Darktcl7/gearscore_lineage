import os, django
from django.test import Client
from django.contrib.auth import get_user_model
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
User = get_user_model()
user = User.objects.first()
c = Client(SERVER_NAME='127.0.0.1')
c.force_login(user)
r = c.get('/portal/character/edit/7/')
content = r.content.decode('utf-8')
import bs4
soup = bs4.BeautifulSoup(content, 'html.parser')
unlocked = soup.find('input', {'name': 'unlocked_skills'})
print('unlocked input:', unlocked)
