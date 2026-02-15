import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from items.models import CharacteristicsStats

# Count all fields in the model
all_fields = [f.name for f in CharacteristicsStats._meta.fields if f.name not in ['id', 'character']]
print(f"Total fields in CharacteristicsStats model: {len(all_fields)}")
print()
print("All field names:")
for i, field in enumerate(all_fields, 1):
    print(f"  {i}. {field}")
