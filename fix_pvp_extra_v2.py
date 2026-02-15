"""
Batch Update Script Part 2 v2 (Corrected): FORMS & EXTRAS
Updates forms.py and item_extras.py for remaining PVP items.
"""

# === 1. FORMS ===
path = r"D:\Django Project\Alto Project\items\forms.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace RadioSelect with Select for all items
# Note: pvp_armor was wrong, use pvp_top_armor
items = ['pvp_sigil', 'pvp_helmet', 'pvp_gloves', 'pvp_boots', 'pvp_gaiters', 'pvp_top_armor', 'pvp_cloak']
for item in items:
    content = content.replace(f"'{item}': forms.RadioSelect,", f"'{item}': forms.Select,")
    print(f"Updated widget for {item}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("forms.py saved.")


# === 2. ITEM EXTRAS ===
path = r"D:\Django Project\Alto Project\items\templatetags\item_extras.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update is_weapon_field filter
# Including pvp_top_armor instead of pvp_armor
new_filter_items = [
    'weapon', 'weapon_enchant',
    'pvp_belt', 'pvp_belt_enchant',
    'pvp_ring_left', 'pvp_ring_left_enchant',
    'pvp_ring_right', 'pvp_ring_right_enchant',
    'pvp_necklace', 'pvp_necklace_enchant',
    'pvp_sigil', 'pvp_sigil_enchant',
    'pvp_helmet', 'pvp_helmet_enchant',
    'pvp_gloves', 'pvp_gloves_enchant',
    'pvp_boots', 'pvp_boots_enchant',
    'pvp_gaiters', 'pvp_gaiters_enchant',
    'pvp_top_armor', 'pvp_top_armor_enchant',
    'pvp_cloak', 'pvp_cloak_enchant'
]
filter_str = ", ".join([f"'{item}'" for item in new_filter_items])
new_filter_code = f"    return field_name in ({filter_str})"

import re
# Regex replacement for the return line - be careful not to replace wrong lines
# Look for: return field_name in (...)
content = re.sub(r"return field_name in \([^\)]+\)", new_filter_code, content)
print("Updated is_weapon_field filter")

# Mappings were already added by previous script (it just failed on pvp_armor field logic if I had that there)
# Actually, the previous script `fix_pvp_extra.py` only updated filter and added mappings.
# The filter update in previous script used `pvp_armor`.
# So this script will fix the filter to use `pvp_top_armor`.
# The mappings were added successfully in previous run because they are just strings in a dict.

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("item_extras.py saved.")
