import os
from PIL import Image

# Tier icon images from the user's attachments  
# The images are in the conversation artifacts directory
artifact_dir = r"C:\Users\chlui\.gemini\antigravity\brain\fc1f61f7-4ac4-4b60-b698-147999cf191b"

# List all png files to find the tier images
for f in sorted(os.listdir(artifact_dir)):
    if f.endswith('.png'):
        fpath = os.path.join(artifact_dir, f)
        try:
            img = Image.open(fpath)
            print(f"{f}: {img.size} ({os.path.getsize(fpath)} bytes)")
        except:
            print(f"{f}: not an image")
