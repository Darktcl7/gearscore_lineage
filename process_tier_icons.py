import os
from PIL import Image
import numpy as np

src_dir = r"D:\Django Project\alto files\tier"
dest1 = r"d:\Django Project\Alto Project\static\images\tiers"
dest2 = r"d:\Django Project\Alto Project\items\static\images\tiers"
os.makedirs(dest1, exist_ok=True)
os.makedirs(dest2, exist_ok=True)

tier_map = {
    'tier_core.png': os.path.join(src_dir, 'core member.png'),
    'tier_elite.png': os.path.join(src_dir, 'elite member.png'),
    'tier_active.png': os.path.join(src_dir, 'active member.png'),
    'tier_unactive.png': os.path.join(src_dir, 'inactive member.png'),
}

for name, src in tier_map.items():
    img = Image.open(src).convert("RGBA")
    data = np.array(img)
    
    # Remove black/near-black background
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    threshold = 30
    dark_mask = (r < threshold) & (g < threshold) & (b < threshold)
    data[dark_mask, 3] = 0
    
    # Smooth edges
    edge_threshold = 50
    edge_mask = (r < edge_threshold) & (g < edge_threshold) & (b < edge_threshold) & ~dark_mask
    brightness = (r.astype(float) + g.astype(float) + b.astype(float)) / 3.0
    edge_alpha = np.clip((brightness - threshold) / (edge_threshold - threshold) * 255, 0, 255).astype(np.uint8)
    data[edge_mask, 3] = edge_alpha[edge_mask]
    
    result = Image.fromarray(data)
    result = result.resize((128, 128), Image.Resampling.LANCZOS)
    
    result.save(os.path.join(dest1, name), "PNG", optimize=True)
    result.save(os.path.join(dest2, name), "PNG", optimize=True)
    fsize = os.path.getsize(os.path.join(dest1, name))
    print(f"Saved {name}: 128x128, {fsize} bytes")

print("Done!")
