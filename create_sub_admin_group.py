import os, sys, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
sys.path.insert(0, r'D:\Django Project\Alto Project')
django.setup()
from django.contrib.auth.models import Group
g, created = Group.objects.get_or_create(name='Sub Admin')
print(f'Sub Admin group: {"CREATED" if created else "already exists"}')
