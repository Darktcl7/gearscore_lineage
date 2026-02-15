import os
import sys
import django

# Setup path to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import connection

print("Starting data fix for character attributes...")

with connection.cursor() as cursor:
    # 1. Update soulshot_level - extract first number
    cursor.execute("""
        UPDATE items_characterattributes 
        SET soulshot_level = CASE 
            WHEN soulshot_level ~ '^[0-9]+' THEN SPLIT_PART(soulshot_level, '-', 1)
            ELSE '0'
        END
    """)
    
    # 2. Update valor_level - extract first number
    cursor.execute("""
        UPDATE items_characterattributes 
        SET valor_level = CASE 
            WHEN valor_level ~ '^[0-9]+' THEN SPLIT_PART(valor_level, '-', 1)
            ELSE '0'
        END
    """)
    
    # 3. Update epic_classes_count - extract first number
    cursor.execute("""
        UPDATE items_characterattributes 
        SET epic_classes_count = CASE 
            WHEN epic_classes_count ~ '^[0-9]+' THEN SPLIT_PART(epic_classes_count, '-', 1)
            ELSE '0'
        END
    """)
    
    # 4. Update epic_agathions_count - extract LAST number (e.g. 10-20 -> 20)
    cursor.execute("""
        UPDATE items_characterattributes 
        SET epic_agathions_count = CASE 
            WHEN epic_agathions_count LIKE '%-%' THEN SPLIT_PART(epic_agathions_count, '-', 2)
            WHEN epic_agathions_count ~ '^[0-9]+' THEN epic_agathions_count
            ELSE '0'
        END
    """)

print("Data fix completed. You can now run 'python manage.py migrate items'.")
