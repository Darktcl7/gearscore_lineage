
path = r"D:\Django Project\Alto Project\items\templates\items\character_form.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_crlf = "{% if not field.name|is_gearscore_field and not field.name|is_skill_field and not\r\n                        field.name|is_weapon_field %}"
old_lf = "{% if not field.name|is_gearscore_field and not field.name|is_skill_field and not\n                        field.name|is_weapon_field %}"
new = "{% if not field.name|is_gearscore_field and not field.name|is_skill_field and not field.name|is_weapon_field %}"

if old_crlf in content:
    content = content.replace(old_crlf, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed split if tag (CRLF)")
elif old_lf in content:
    content = content.replace(old_lf, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed split if tag (LF)")
else:
    print("Already fixed")
