import os, sys, django, shutil
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
sys.stdout.reconfigure(encoding='utf-8')

# Step 1: Copy all new armor images to static folder
src_base = r"D:\Django Project\alto files\armor"
dst_base = r"D:\Django Project\Alto Project\items\static\items\images\choices"

# Map folder name to subfolder in static
folders = {
    'helmet': 'armor_helmet',
    'armor': 'armor_armor', 
    'gloves': 'armor_gloves',
    'shoes': 'armor_shoes',
    'bottoms': 'armor_bottoms',
    'cloak': 'armor_cloak',
    'sigil': 'armor_sigil',
    't-shirt': 'armor_tshirt',
}

# Copy files and build a mapping of clean_name -> new_filename
all_new_images = {}
for folder, prefix in folders.items():
    src_dir = os.path.join(src_base, folder)
    for f in os.listdir(src_dir):
        if f.lower().endswith(('.png', '.jpg')):
            # Create clean filename
            clean = f.replace(' ', '_')
            new_name = f"{prefix}_{clean}"
            src = os.path.join(src_dir, f)
            dst = os.path.join(dst_base, new_name)
            shutil.copy2(src, dst)
            
            # Map: item name (without extension) -> new icon filename
            item_name = os.path.splitext(f)[0]
            all_new_images[item_name.lower()] = f"choices/{new_name}"
            print(f"  Copied: {folder}/{f} -> choices/{new_name}")

print(f"\nTotal images copied: {len(all_new_images)}")
print("\n=== Image mapping ===")
for k, v in sorted(all_new_images.items()):
    print(f"  {k} -> {v}")
