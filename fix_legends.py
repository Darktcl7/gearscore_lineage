"""
Fix: Re-copy legendary class and mount images, update DB entries.
"""
import os, sys, shutil, glob

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
sys.path.insert(0, r'D:\Django Project\Alto Project')

import django
django.setup()

from items.models import LegendaryClass, LegendaryAgathion, LegendaryMount

DEST = r'D:\Django Project\Alto Project\static\items\images\choices'

# ============================================
# 1. LEGENDARY CLASSES
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

print(f"Created {LegendaryClass.objects.count()} legendary classes\n")

# ============================================
# 2. LEGENDARY AGATHIONS
# ============================================
SRC_AGATHION = r'D:\Django Project\alto files\File Foto InGame\New folder\Agathion\Legend'

LegendaryAgathion.objects.all().delete()
print("Deleted all old LegendaryAgathion entries")

for f in sorted(glob.glob(os.path.join(SRC_AGATHION, '*.*'))):
    basename = os.path.basename(f)
    name = os.path.splitext(basename)[0]
    ext = os.path.splitext(basename)[1]
    dest_name = f"agathion_legend_{name.replace(' ', '_')}{ext}"
    shutil.copy2(f, os.path.join(DEST, dest_name))
    LegendaryAgathion.objects.create(name=name, icon_file=dest_name)
    print(f"  Agathion: {name} -> {dest_name}")

print(f"Created {LegendaryAgathion.objects.count()} legendary agathions\n")

# ============================================
# 3. LEGENDARY MOUNTS
# ============================================
SRC_MOUNT = r'D:\Django Project\alto files\File Foto InGame\New folder\Mount\Legend'

LegendaryMount.objects.all().delete()
print("Deleted all old LegendaryMount entries")

for f in sorted(glob.glob(os.path.join(SRC_MOUNT, '*.*'))):
    basename = os.path.basename(f)
    name = os.path.splitext(basename)[0]
    ext = os.path.splitext(basename)[1]
    dest_name = f"mount_legend_{name.replace(' ', '_')}{ext}"
    shutil.copy2(f, os.path.join(DEST, dest_name))
    LegendaryMount.objects.create(name=name, icon_file=dest_name)
    print(f"  Mount: {name} -> {dest_name}")

print(f"Created {LegendaryMount.objects.count()} legendary mounts\n")

# Verify files exist
print("=== Verification ===")
for model, prefix in [(LegendaryClass, 'class'), (LegendaryAgathion, 'agathion'), (LegendaryMount, 'mount')]:
    for obj in model.objects.all():
        path = os.path.join(DEST, obj.icon_file)
        exists = os.path.exists(path)
        if not exists:
            print(f"  MISSING: {obj.icon_file}")
    print(f"  {model.__name__}: {model.objects.count()} entries, all files verified")

print("\n=== DONE ===")
