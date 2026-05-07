import os
import re

base_dir = r"d:\Django Project\Alto Project\items\templates\items"

css_files = ["my_activity.html", "activity_leaderboard.html"]

new_badge = """.event-type-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        padding: 0;
        background: transparent !important;
    }"""

for filename in css_files:
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex replace .event-type-badge
    content = re.sub(r'\.event-type-badge\s*\{[^}]*\}', new_badge, content)
    
    # Replace background colors
    content = re.sub(r'\.event-invasion,\s*\.event-inv_dragon_beast,\s*\.event-inv_carnifex,\s*\.event-inv_orfen\s*\{\s*background:\s*#e74c3c;\s*color:\s*#fff;\s*\}', '.event-invasion, .event-inv_dragon_beast, .event-inv_carnifex, .event-inv_orfen { color: #ff7675; }', content)
    content = re.sub(r'\.event-boss_rush\s*\{\s*background:\s*#9b59b6;\s*color:\s*#fff;\s*\}', '.event-boss_rush { color: #a29bfe; }', content)
    content = re.sub(r'\.event-catacombs\s*\{\s*background:\s*#3498db;\s*color:\s*#fff;\s*\}', '.event-catacombs { color: #74b9ff; }', content)
    content = re.sub(r'\.event-dimensional\s*\{\s*background:\s*#1abc9c;\s*color:\s*#fff;\s*\}', '.event-dimensional { color: #55efc4; }', content)
    content = re.sub(r'\.event-isle_awakening\s*\{\s*background:\s*#f39c12;\s*color:\s*#fff;\s*\}', '.event-isle_awakening { color: #fdcb6e; }', content)
    content = re.sub(r'\.event-war_day\s*\{\s*background:\s*#e74c3c;\s*color:\s*#fff;\s*\}', '.event-war_day { color: #ff7675; }', content)
    content = re.sub(r'\.event-custom\s*\{\s*background:\s*#e67e22;\s*color:\s*#fff;\s*\}', '.event-custom { color: #dfe6e9; }', content)

    # Some old ones had color #fff inside the class body without newline or with different formatting
    content = re.sub(r'\.event-boss_rush \{ background: #9b59b6; \}', '.event-boss_rush { color: #a29bfe; }', content)
    content = re.sub(r'\.event-catacombs \{ background: #3498db; \}', '.event-catacombs { color: #74b9ff; }', content)
    content = re.sub(r'\.event-dimensional \{ background: #1abc9c; \}', '.event-dimensional { color: #55efc4; }', content)
    content = re.sub(r'\.event-isle_awakening \{ background: #f39c12; \}', '.event-isle_awakening { color: #fdcb6e; }', content)
    content = re.sub(r'\.event-war_day \{ background: #e74c3c; \}', '.event-war_day { color: #ff7675; }', content)
    content = re.sub(r'\.event-custom \{ background: #e67e22; \}', '.event-custom { color: #dfe6e9; }', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filename}")

