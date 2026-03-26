import shutil, os

# Copy icon image
src = r"D:\Django Project\alto files\File Foto InGame\icon\soul_progression_accuracy-removebg-preview.png"
dst = r"D:\Django Project\Alto Project\items\static\items\images\choices\soul_progression_accuracy-removebg-preview.png"
shutil.copy2(src, dst)
print(f"Copied icon: {os.path.getsize(dst)} bytes")
