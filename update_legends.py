"""
Script to:
1. Copy new legendary class, agathion, mount images to static/items/images/choices/
2. Update LegendaryClass, LegendaryAgathion, LegendaryMount database entries
"""
import os, sys, shutil, glob

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
sys.path.insert(0, r'D:\Django Project\Alto Project')

import django
django.setup()

from items.models import LegendaryClass, LegendaryAgathion, LegendaryMount

DEST = r'D:\Django Project\Alto Project\static\items\images\choices'

# ============================================
# 1. LEGENDARY CLASSES - Delete old, add new
# ============================================
SRC_CLASS = r'D:\Django Project\alto files\File Foto InGame\New folder\Class\Legend'

LegendaryClass.objects.all().delete()
print("Deleted all old LegendaryClass entries")

for f in sorted(glob.glob(os.path.join(SRC_CLASS, '*.*'))):
    basename = os.path.basename(f)
    name = os.path.splitext(basename)[0]
    ext = os.path.splitext(basename)[1]
    dest_name = f"class_legend_{name.replace(' ', '_')}{ext}"
    shutil.copy2(f, os.path.join(DEST, dest_name))
    LegendaryClass.objects.create(name=name, icon_file=dest_name)
    print(f"  Class: {name} -> {dest_name}")

print(f"Created {LegendaryClass.objects.count()} legendary classes")

# ============================================
# 2. LEGENDARY AGATHIONS - Delete old, add new
# ============================================
SRC_AGATHION = r'D:\Django Project\alto files\File Foto InGame\New folder\Agathion\Legend'

LegendaryAgathion.objects.all().delete()
print("\nDeleted all old LegendaryAgathion entries")

for f in sorted(glob.glob(os.path.join(SRC_AGATHION, '*.*'))):
    basename = os.path.basename(f)
    name = os.path.splitext(basename)[0]
    ext = os.path.splitext(basename)[1]
    dest_name = f"agathion_legend_{name.replace(' ', '_')}{ext}"
    shutil.copy2(f, os.path.join(DEST, dest_name))
    LegendaryAgathion.objects.create(name=name, icon_file=dest_name)
    print(f"  Agathion: {name} -> {dest_name}")

print(f"Created {LegendaryAgathion.objects.count()} legendary agathions")

# ============================================
# 3. LEGENDARY MOUNTS - Delete old, add new
# ============================================
SRC_MOUNT = r'D:\Django Project\alto files\File Foto InGame\New folder\Mount\Legend'

LegendaryMount.objects.all().delete()
print("\nDeleted all old LegendaryMount entries")

for f in sorted(glob.glob(os.path.join(SRC_MOUNT, '*.*'))):
    basename = os.path.basename(f)
    name = os.path.splitext(basename)[0]
    ext = os.path.splitext(basename)[1]
    dest_name = f"mount_legend_{name.replace(' ', '_')}{ext}"
    shutil.copy2(f, os.path.join(DEST, dest_name))
    LegendaryMount.objects.create(name=name, icon_file=dest_name)
    print(f"  Mount: {name} -> {dest_name}")

print(f"Created {LegendaryMount.objects.count()} legendary mounts")

print("\n=== DONE ===")
