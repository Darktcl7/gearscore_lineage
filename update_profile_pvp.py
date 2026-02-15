
# Script to update profile displays for PVP items with enchant level
import re

path = r"D:\Django Project\Alto Project\items\templates\items\character_profile.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

items = [
    {'field': 'pvp_sigil', 'color': '#607D8B'},
    {'field': 'pvp_helmet', 'color': '#795548'},
    {'field': 'pvp_top_armor', 'color': '#9E9E9E'},
    {'field': 'pvp_gloves', 'color': '#FF5722'},
    {'field': 'pvp_boots', 'color': '#8BC34A'},
    {'field': 'pvp_gaiters', 'color': '#3F51B5'},
    {'field': 'pvp_cloak', 'color': '#FFEB3B'},
]

for item in items:
    field = item['field']
    color = item['color']
    
    # Regex to find the <p class="item-grade"> line
    # Matches: <p class="item-grade">{{ attrs.FIELD|default:"-" }}</p>
    pattern = re.compile(f'(<p class="item-grade">{{{{ attrs\.{field}\|default:"-" }}}}</p>)')
    
    replacement = f'''<p class="item-grade">
                            {{{{ attrs.{field}|default:"-" }}}}
                            {{% if attrs.{field}_enchant and attrs.{field}_enchant > 0 %}}
                            <span style="color: {color}; font-weight: 700;"> +{{{{ attrs.{field}_enchant }}}}</span>
                            {{% endif %}}
                        </p>'''
    
    if pattern.search(content):
        content = pattern.sub(replacement, content)
        print(f"Updated display for {field}")
    else:
        print(f"WARNING: Could not find display for {field}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Profile updated.")
