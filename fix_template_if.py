
import os

path = r"D:\Django Project\Alto Project\items\templates\items\character_form.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the split if tag
old_crlf = "{% if not field.name|is_gearscore_field and not field.name|is_skill_field and not\r\n                        field.name|is_weapon_field %}"
old_lf = "{% if not field.name|is_gearscore_field and not field.name|is_skill_field and not\n                        field.name|is_weapon_field %}"
new = "{% if not field.name|is_gearscore_field and not field.name|is_skill_field and not field.name|is_weapon_field %}"

if old_crlf in content:
    content = content.replace(old_crlf, new)
    print("Fixed split if tag (CRLF)")
elif old_lf in content:
    content = content.replace(old_lf, new)
    print("Fixed split if tag (LF)")
else:
    print("If tag already correct or not found.")

# Also verify that necklace visuals are correct
if 'id="necklace-section"' in content:
    print("Verified: Necklace section present.")
else:
    print("WARNING: Necklace section missing.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")
