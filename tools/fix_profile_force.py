import os
import re

file_path = r"dkp\templates\dkp\my_profile.html"

# Read
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define corrections
corrections = [
    # Fix Name split
    (r"\{\{\s*p\.character\.name\s*\n\s*\}\}", "{{ p.character.name }}"),
    # Fix Level split - Regex to match the split pattern specifically
    (r"Lv\.\s*\{\{\s*\n\s*p\.character\.level\s*\}\}", "Lv. {{ p.character.level }}"),
    # Generic safety catch for other simple splits
    (r"\{\{\s*\n\s*([a-zA-Z0-9_.]+)\s*\}\}", r"{{ \1 }}") 
]

new_content = content
for pattern, replacement in corrections:
    new_content = re.sub(pattern, replacement, new_content)

if new_content != content:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("FIXED: Cleaned up template tags.")
else:
    print("WARNING: No patterns matched. File might differ from expectation.")
    # Debug: print snippet around "Lv."
    idx = new_content.find("Lv.")
    if idx != -1:
        print(f"Snippet around Lv.: {repr(new_content[idx:idx+50])}")
