
import os

items = [
    {
        'id': 'sigil', 'title': '🛡️ PvP Sigil', 'field': 'pvp_sigil', 'color': '#607D8B', 'bg_grad': 'linear-gradient(145deg, #1a2a3a, #0d151d)',
        'choices': {
            "Dream Sigil": "Icon_AR_Sigil_G4_001.png", "Blue": "вопрос_PiWb3ob.png", "Susceptor's Heart": "Icon_AR_Sigil_G3_001.png", "Paradia's Sigil": "Icon_AR_Sigil_G3_002.png", "Cruma's Shell": "Icon_AR_Sigil_G3_003.png", "Sigil of Flames": "Icon_AR_Sigil_G3_004.png", "Jaeger's Sigil": "Icon_AR_Sigil_G3_005.png", "Selihoden's Horn": "Icon_AR_Sigil_G3_006.png", "Tear of Darkness": "Icon_AR_Sigil_G2_001.png", "Draconic Sigil": "Icon_AR_Sigil_G2_002.png", "Arcana Sigil": "Icon_AR_Sigil_G2_003.png"
        }
    },
    {
        'id': 'helmet', 'title': '🪖 PvP Helmet', 'field': 'pvp_helmet', 'color': '#795548', 'bg_grad': 'linear-gradient(145deg, #3a2a1a, #1d150d)',
        'choices': {
            "Blue Wolf Helmet": "Icon_AR_Helmet_G3_006.png", "Majestic Circlet": "Icon_AR_Helmet_G3_001.png", "Helm of Nightmares": "Icon_AR_Helmet_G3_002.png", "Dark Crystal Helmet": "Icon_AR_Helmet_G3_003.png", "Medusa's Helm": "Icon_AR_Helmet_G3_004.png", "Paulina's Helmet": "Icon_AR_Helmet_G3_005.png", "Nevit's Helmet": "Icon_AR_Helmet_G3_007.png", "Tersi's Circlet": "Icon_AR_Helmet_G3_009.png", "Ancient Elven Helm": "Icon_AR_Helmet_G2_002.png", "Imperial Crusader Helmet": "Icon_AR_Helmet_G3_009.png", "Major Arcana Circlet": "Icon_AR_Helmet_G3_009.png", "Draconic Helmet": "Icon_AR_Helmet_G3_009.png"
        }
    },
    {
        'id': 'top_armor', 'title': '👕 PvP Armor (Top/Full)', 'field': 'pvp_top_armor', 'color': '#9E9E9E', 'bg_grad': 'linear-gradient(145deg, #2a2a2a, #151515)',
        'choices': {
            "Blue Wolf Breastplate": "Icon_AR_Torso_G3_006.png", "Majestic Robe": "Icon_AR_Torso_G3_001.png", "Armor of Nightmares": "Icon_AR_Torso_G3_002.png", "Dark Crystal Breastplate": "Icon_AR_Torso_G3_003.png", "Tersi's Robe": "Icon_AR_Torso_G3_008.png", "Paulina's Breastplate": "Icon_AR_Torso_G3_005.png", "Nevit's Armor": "Icon_AR_Torso_G3_007.png", "Savan's Robe": "Icon_AR_Torso_G3_004.png", "Absolute Tunic": "Icon_AR_Torso_G2_003.png", "Apella Plate Armor": "Icon_AR_Torso_G2_004.png", "Forgotten Hero's Breastplate": "Icon_AR_Torso_G3_009.png", "Ancient Elven Armor": "Icon_AR_Torso_G2_002.png", "Demon's Armor": "Icon_AR_Torso_G2_001.png", "Draconic Leather Armor": "Icon_AR_Torso_G3_011.png", "Major Arcana Robe": "Icon_AR_Torso_G3_012.png", "Imperial Crusader Breastplate": "Icon_AR_Torso_G3_010.png"
        }
    },
    {
        'id': 'gloves', 'title': '🧤 PvP Gloves', 'field': 'pvp_gloves', 'color': '#FF5722', 'bg_grad': 'linear-gradient(145deg, #3a1a0a, #1d0d05)',
        'choices': {
            "Blue Wolf Gloves": "Icon_AR_Gloves_G3_006.png", "Majestic Gloves": "Icon_AR_Gloves_G3_001.png", "Gauntlets of Nightmare": "Icon_AR_Gloves_G3_002.png", "Dark Crystal Gloves": "Icon_AR_Gloves_G3_003.png", "Tersi's Gloves": "Icon_AR_Gloves_G3_008.png", "Paulina's Gauntlets": "Icon_AR_Gloves_G3_005.png", "Nevit's Gloves": "Icon_AR_Gloves_G3_007.png", "Jarngreipr": "Icon_AR_Gloves_G3_004.png", "Vision Guardian": "Icon_AR_Gloves_G3_009.png", "Gloves of Blessing": "Icon_AR_Gloves_G2_003.png", "Forgotten Hero Gloves": "Icon_AR_Gloves_G3_010.png", "Demon's Gauntlets": "Icon_AR_Gloves_G2_001.png", "Ancient Elven Gauntlet": "Icon_AR_Gloves_G2_002.png", "Draconic Leather Gloves": "Icon_AR_Gloves_G3_011.png", "Pa'agrio's Flames": "Icon_AR_Gloves_G3_012.png"
        }
    },
    {
        'id': 'boots', 'title': '👢 PvP Boots', 'field': 'pvp_boots', 'color': '#8BC34A', 'bg_grad': 'linear-gradient(145deg, #1a3a0a, #0d1d05)',
        'choices': {
            "Blue Wolf Boots": "Icon_AR_Boots_G3_006.png", "Majestic Boots": "Icon_AR_Boots_G3_001.png", "Boots of Nightmares": "Icon_AR_Boots_G3_002.png", "Dark Crystal Boots": "Icon_AR_Boots_G3_003.png", "Tersi's Boots": "Icon_AR_Boots_G3_008.png", "Paulina's Boots": "Icon_AR_Boots_G3_005.png", "Nevit's Boots": "Icon_AR_Boots_G3_007.png", "Demon's Boots": "Icon_AR_Boots_G2_001.png", "Kaliel's Boots": "Icon_AR_Boots_G2_004.png", "Forgotten Hero's Boots": "Icon_AR_Boots_G3_009.png", "Ancient Elven Boots": "Icon_AR_Boots_G2_002.png", "Draconic": "Icon_AR_Boots_G3_010.png", "Sayha's Wind": "Icon_AR_Boots_G3_011.png"
        }
    },
    {
        'id': 'gaiters', 'title': '👖 PvP Gaiters (Pants)', 'field': 'pvp_gaiters', 'color': '#3F51B5', 'bg_grad': 'linear-gradient(145deg, #0a1a3a, #050d1d)',
        'choices': {
            "Blue Wolf Gaiters": "Icon_AR_Pants_G3_006.png", "Basila Skin": "Icon_AR_Pants_G3_008.png", "Blood Gaiters": "Icon_AR_Pants_G3_001.png", "Gaiters of Light": "Icon_AR_Pants_G3_002.png", "Gaiters of Ice": "Icon_AR_Pants_G3_003.png", "Shilen's Breath": "Icon_AR_Pants_G3_004.png", "Crystal Gaiters": "Icon_AR_Pants_G3_005.png", "Forgotten Hero's Gaiters": "Icon_AR_Pants_G3_007.png", "Imperial Crusader Gaiters": "Icon_AR_Pants_G3_009.png"
        }
    },
    {
        'id': 'cloak', 'title': '🧥 PvP Cloak', 'field': 'pvp_cloak', 'color': '#FFEB3B', 'bg_grad': 'linear-gradient(145deg, #3a3a0a, #1d1d05)',
        'choices': {
            "Silver Cloak": "Icon_AR_Cape_G3_001.png", "Cranigg's Cloak": "Icon_AR_Cape_G3_002.png", "Dragon's Scale": "Icon_AR_Cape_G3_003.png", "Zaken's Cloak": "Icon_AR_Cape_G3_004.png", "Cloak of Freya": "Icon_AR_Cape_G3_005.png", "Queen Ant's Wing": "Icon_AR_Cape_G3_006.png", "Cloak of Silence": "Icon_AR_Cape_G3_007.png", "Eigis Cloak": "Icon_AR_Cape_G3_008.png", "Cloak of Authority": "Icon_AR_Cape_G3_007.png", "Selihoden's Wing": "Icon_AR_Cape_G3_008.png", "Nevit's Cloak of Light": "Icon_AR_Cape_G2_001.png", "Nailop's Cloak": "Icon_AR_Cape_G2_002.png"
        }
    }
]

def generate_html(item):
    id = item['id']
    title = item['title']
    field = item['field']
    color = item['color']
    bg_grad = item['bg_grad']
    
    return f'''
                        <!-- {title} Selection Section -->
                        <div class="form-group" id="{id}-section"
                            style="background: {bg_grad}; border: 1px solid rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.3);">
                            <label class="form-label"><strong>{title}</strong></label>
                            <p style="color: #aaa; font-size: 0.9rem; margin-bottom: 15px;">Select your {title.replace('PvP ', '')}</p>

                            <div style="display: none;">
                                {{{{ attributes_form.{field} }}}}
                                {{{{ attributes_form.{field}_enchant }}}}
                            </div>

                            <div class="{id}-grid" id="{id}-grid"
                                style="display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px;">
                            </div>

                            <div id="{id}-enchant-section" style="display: none; margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2);">
                                <label class="form-label" style="color: {color}; margin-bottom: 10px;">
                                    <strong>✨ Enchant Level</strong>
                                    <span id="selected-{id}-name" style="color: #ccc; font-weight: normal; margin-left: 8px;"></span>
                                </label>
                                <div id="{id}-enchant-grid" style="display: flex; flex-wrap: wrap; gap: 8px;"></div>
                            </div>
                        </div>
'''

def generate_js(item):
    id = item['id']
    camel_id = "".join([x.capitalize() for x in id.split('_')])
    choices = item['choices']
    
    choices_js = ",\n            ".join([f'"{k}": "{v}"' for k, v in choices.items()])
    
    return f'''
    // === PVP {id.upper().replace('_', ' ')} ===
    function get{camel_id}Image(itemName) {{
        const images = {{
            {choices_js}
        }};
        return images[itemName] || null;
    }}

    buildEquipGrid({{
        selectEl: document.getElementById('id_{item['field']}'),
        enchantInput: document.getElementById('id_{item['field']}_enchant'),
        gridEl: document.getElementById('{id}-grid'),
        enchantSection: document.getElementById('{id}-enchant-section'),
        enchantGridEl: document.getElementById('{id}-enchant-grid'),
        nameSpan: document.getElementById('selected-{id}-name'),
        getImageFn: get{camel_id}Image,
        cardClass: '{id}-card',
        enchantClass: '{id}-enchant',
        radioName: '{id}_visual'
    }});
'''

all_html = ""
all_js = ""

for item in items:
    all_html += generate_html(item)
    all_js += generate_js(item)

path = r"D:\Django Project\Alto Project\items\templates\items\character_form.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert HTML after Ring Right Section
ring_right_end = '<!-- Skills Section -->'
if ring_right_end in content:
    content = content.replace(ring_right_end, all_html + "\n\n" + ring_right_end)
    print("Inserted HTML sections")
else:
    print("ERROR: Could not find insertion point for HTML")

# Insert JS before closing script
js_end = '</script>'
if js_end in content:
    parts = content.rsplit(js_end, 1)
    content = parts[0] + all_js + js_end + parts[1]
    print("Inserted JS code")
else:
    print("ERROR: Could not find insertion point for JS")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Template updated.")
