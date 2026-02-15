import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from items.forms import CharacteristicsStatsForm

# Create an instance of the form
form = CharacteristicsStatsForm()

# Count visible fields
visible_fields = list(form.fields.keys())
print(f"Total fields in CharacteristicsStatsForm: {len(visible_fields)}")
print()
print("Form visible fields:")
for i, field in enumerate(visible_fields, 1):
    print(f"  {i}. {field}")
