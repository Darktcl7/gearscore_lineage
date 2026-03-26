import shutil, os

src_dir = r"D:\Django Project\Alto Project\static\items\images\choices"
dst_dir = r"D:\Django Project\Alto Project\items\static\items\images\choices"

files = [
    "class_legend_Regina.jpeg",
    "class_legend_Shiel.jpeg",
    "class_legend_Tania.jpeg",
    "class_legend_Zanak.jpeg",
    "mount_legend_Lucis.jpeg",
    "class_legend_Shunaiman.jpeg",
    "class_legend_Khalia.jpeg",
    "class_legend_Lionel_Hunter.jpeg",
    "class_legend_Krenaht.jpeg",
]

for f in files:
    src = os.path.join(src_dir, f)
    dst = os.path.join(dst_dir, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {f} ({os.path.getsize(dst)} bytes)")
    else:
        print(f"NOT FOUND: {src}")

print("Done!")
