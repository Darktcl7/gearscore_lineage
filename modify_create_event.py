import re
import os

print("Starting modify_create_event.py...")

# 1. Modify items/templates/items/create_event.html
html_path = 'items/templates/items/create_event.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Remove DKP Penalty checkbox
dkp_checkbox_pattern = r'<label id="dkp-penalty-checkbox-label"[\s\S]*?</label>'
html_content = re.sub(dkp_checkbox_pattern, '', html_content)

# Remove invasion mandatory bosses block
invasion_bosses_pattern = r'<div id="invasion-mandatory-bosses"[\s\S]*?</div>\s*</div>\s*</div>'
html_content = re.sub(invasion_bosses_pattern, '</div>', html_content)

# The above regex might be too greedy, let's use exact string replacement or safer regex
html_content = re.sub(r'<div id="invasion-mandatory-bosses".*?</div>\s*</div>', '', html_content, flags=re.DOTALL)

# In JS, remove invasion logic
js_replacements = [
    ("if (evType === 'INVASION')", "if (false)"),
    ("var isDkp = document.getElementById('is_dkp_penalty').checked;", "var isDkp = false;"),
    ("var dkpCheckboxLabel = document.getElementById('dkp-penalty-checkbox-label');", ""),
    ("dkpCheckboxLabel.style.display = 'flex';", ""),
    ("dkpCheckboxLabel.style.display = 'none';", ""),
    ("document.getElementById('is_dkp_penalty').checked = false;", ""),
    ("document.getElementById('is_dkp_penalty').addEventListener", "// document.getElementById('is_dkp_penalty').addEventListener"),
]

for old, new in js_replacements:
    html_content = html_content.replace(old, new)

# Wait, let's just do a clean replace for the JS part to avoid issues.
# Actually, the user asked to replace "INVASION" with specific types.
# When the type is `INV_DRAGON_BEAST`, etc. we just want it to behave like a normal event (points, normal mandatory penalty).
# So `evType !== 'INVASION'` will naturally be true for `INV_DRAGON_BEAST` and it will show points.

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated create_event.html")

# 2. Modify items/views.py for create_event
views_path = 'items/views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

# We need to remove the logic for `if event_type == 'INVASION':` around line 1445.
# Let's find it.
invasion_logic_start = "if event_type == 'INVASION':"
invasion_logic_end = "event.save()"

# It's better to just use replace.
old_logic = """
        # For INVASION, set default boss_point_config and mandatory penalties
        if event_type == 'INVASION':
            event_kwargs['boss_point_config'] = {
                'dragon_beast': 50,
                'carnifex': 25,
                'orfen': 100,
            }
            
            if request.POST.get('is_mandatory') == 'on':
                mandatory_penalties = {}
                dkp_mandatory_penalties = {}
                
                if request.POST.get('mandatory_dragon_beast') == 'on':
                    try:
                        mandatory_penalties['dragon_beast'] = int(request.POST.get('penalty_dragon_beast', 5))
                    except (ValueError, TypeError):
                        pass
                    
                    if is_dkp_penalty:
                        try:
                            dkp_mandatory_penalties['dragon_beast'] = int(request.POST.get('dkp_penalty_dragon_beast', 5))
                        except (ValueError, TypeError):
                            pass
                            
                if request.POST.get('mandatory_carnifex') == 'on':
                    try:
                        mandatory_penalties['carnifex'] = int(request.POST.get('penalty_carnifex', 5))
                    except (ValueError, TypeError):
                        pass
                        
                    if is_dkp_penalty:
                        try:
                            dkp_mandatory_penalties['carnifex'] = int(request.POST.get('dkp_penalty_carnifex', 5))
                        except (ValueError, TypeError):
                            pass
                            
                if request.POST.get('mandatory_orfen') == 'on':
                    try:
                        mandatory_penalties['orfen'] = int(request.POST.get('penalty_orfen', 5))
                    except (ValueError, TypeError):
                        pass
                        
                    if is_dkp_penalty:
                        try:
                            dkp_mandatory_penalties['orfen'] = int(request.POST.get('dkp_penalty_orfen', 5))
                        except (ValueError, TypeError):
                            pass
                            
                event_kwargs['mandatory_boss_penalties'] = mandatory_penalties
                event_kwargs['dkp_mandatory_boss_penalties'] = dkp_mandatory_penalties
"""
new_logic = """
        # No more generic INVASION logic needed since they are specific events now
"""

views_content = views_content.replace(old_logic, new_logic)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)

print("Updated views.py")
