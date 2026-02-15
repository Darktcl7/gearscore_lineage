import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from items.models import Character, CharacterAttributes

def check_char(pk):
    print(f"--- Checking Character ID {pk} ---")
    try:
        char = Character.objects.get(pk=pk)
        print(f"Name: {char.name}")
        print(f"Owner: {char.owner} (ID: {char.owner.id})")
        print(f"Level: {char.level}")
        
        # Check Attributes
        try:
            attrs = char.attributes
            print(f"Attributes: Found (ID: {attrs.id})")
        except CharacterAttributes.DoesNotExist:
            print("Attributes: NOT FOUND (This might be the issue!)")
            # Try creating it
            # CharacterAttributes.objects.create(character=char)
            # print("Attributes: Created just now.")
            
    except Character.DoesNotExist:
        print("Character NOT FOUND.")

# Check Admin User
try:
    admin_user = User.objects.get(username='admin')
    print(f"\nUser 'admin': ID={admin_user.id}, Is Staff={admin_user.is_staff}, Is Superuser={admin_user.is_superuser}")
except User.DoesNotExist:
    print("\nUser 'admin' not found.")

check_char(7)
check_char(8)
