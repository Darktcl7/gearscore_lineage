import os
from PIL import Image, ImageDraw

files = [
    r"C:\Users\chlui\.gemini\antigravity\brain\fc1f61f7-4ac4-4b60-b698-147999cf191b\media__1778216171974.png",
    r"C:\Users\chlui\.gemini\antigravity\brain\fc1f61f7-4ac4-4b60-b698-147999cf191b\media__1778216172182.png",
    r"C:\Users\chlui\.gemini\antigravity\brain\fc1f61f7-4ac4-4b60-b698-147999cf191b\media__1778216172280.png",
    r"C:\Users\chlui\.gemini\antigravity\brain\fc1f61f7-4ac4-4b60-b698-147999cf191b\media__1778216172362.png",
    r"C:\Users\chlui\.gemini\antigravity\brain\fc1f61f7-4ac4-4b60-b698-147999cf191b\media__1778216172531.png"
]

names = ['raid', 'territory', 'world', 'rift', 'arena']
dest_dir = r"d:\Django Project\Alto Project\static\images\events"
os.makedirs(dest_dir, exist_ok=True)
dest_dir2 = r"d:\Django Project\Alto Project\items\static\images\events"
os.makedirs(dest_dir2, exist_ok=True)

def make_circle(img_path, save_path, save_path2):
    try:
        img = Image.open(img_path).convert("RGBA")
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        img = img.crop((left, top, right, bottom))
        
        img = img.resize((256, 256), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', (256, 256), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 256, 256), fill=255)
        
        output = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        output.paste(img, (0, 0), mask)
        
        output.save(save_path, "PNG")
        output.save(save_path2, "PNG")
        print(f"Saved {save_path}")
    except Exception as e:
        print(f"Failed {img_path}: {e}")

for f, n in zip(files, names):
    make_circle(f, os.path.join(dest_dir, n + '.png'), os.path.join(dest_dir2, n + '.png'))
