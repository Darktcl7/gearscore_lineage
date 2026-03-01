import re

with open('items/models.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import sys

new_lines = []
skip = False
for i, line in enumerate(lines):
    # Skip soulshot_level and valor_level
    if "soulshot_level =" in line or "valor_level =" in line:
        continue
    # Skip gear score stats block
    if "# NEW STAT FIELDS FOR GEAR SCORE CALCULATION" in line:
        skip = True
        # Insert G fields here
        g_fields = """    # KELOMPOK G - BASE STATS
    g1 = models.IntegerField("Melee Damage Reduction", default=0)
    g2 = models.IntegerField("Ranged Damage Reduction", default=0)
    g3 = models.IntegerField("Magic Damage Reduction", default=0)
    g4 = models.IntegerField("Melee Evasion", default=0)
    g5 = models.IntegerField("Ranged Evasion", default=0)
    g6 = models.IntegerField("Magic Evasion", default=0)
    g7 = models.IntegerField("Skill Resistance", default=0)
    g8 = models.IntegerField("Movement Speed (%)", default=0)
    g9 = models.IntegerField("Max HP", default=0)
    g10 = models.IntegerField("Max MP", default=0)
    g11 = models.IntegerField("Weapon Block (%)", default=0)
    g12 = models.IntegerField("Defense", default=0)
    g13 = models.IntegerField("Cooldown Reduction (%)", default=0)
    g14 = models.IntegerField("Melee Damage", default=0)
    g15 = models.IntegerField("Melee Accuracy", default=0)
    g16 = models.IntegerField("Melee Critical Hit (%)", default=0)
    g17 = models.IntegerField("Ranged Damage", default=0)
    g18 = models.IntegerField("Ranged Accuracy", default=0)
    g19 = models.IntegerField("Ranged Critical Hit (%)", default=0)
    g20 = models.IntegerField("Magic Damage", default=0)
    g21 = models.IntegerField("Magic Accuracy", default=0)
    g22 = models.IntegerField("Magic Critical Hit (%)", default=0)
    g23 = models.IntegerField("Weapon Damage Boost (%)", default=0)
    g24 = models.IntegerField("Weapon Defense (%)", default=0)
    g25 = models.IntegerField("Skill Damage Boost (%)", default=0)
    g26 = models.IntegerField("Skill Defense (%)", default=0)
    g27 = models.IntegerField("Attack Speed (%)", default=0)
    g28 = models.IntegerField("Cast Speed (%)", default=0)
    g29 = models.IntegerField("Weapon Damage", default=0)
    g30 = models.IntegerField("Extra Damage", default=0)
    g31 = models.IntegerField("HP Recovery (Tick)", default=0)
    g32 = models.IntegerField("MP Recovery (Tick)", default=0)
    g33 = models.IntegerField("MP Consumption Reduction (%)", default=0)
    g34 = models.IntegerField("Weight Limit", default=0)
    g35 = models.IntegerField("SOULSHOT Level", default=0)
    g36 = models.IntegerField("VALOR Level", default=0)
    g37 = models.IntegerField("GUARDIAN Level", default=0)
    g38 = models.IntegerField("CONQUER Level", default=0)

"""
        new_lines.append(g_fields)
        continue
    
    # End skip
    if skip and "weapon =" in line:
        skip = False

    if not skip:
        new_lines.append(line)

with open('items/models.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

# now replace calculate_gear_score_breakdown
with open('items/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'def calculate_gear_score_breakdown\(self\):(.*?)return total_score', re.DOTALL)
new_func = """def calculate_gear_score_breakdown(self):
        characteristics_score = 0.0
        try:
            char_stats = self.characteristics_stats
            characteristics_score = float(char_stats.calculate_total_score())
        except CharacteristicsStats.DoesNotExist:
            pass

        # 2. SUB-CLASS SCORE
        subclass_score = 0.0
        try:
            subclass = self.subclass_stats
            subclass_score = float(subclass.calculate_subclass_score())
        except SubclassStats.DoesNotExist:
            pass

        # 3. MAIN CLASS SCORE (Gear Score Stats - KELOMPOK G)
        mainclass_score = 0.0
        dmg = acc = def_stat = reduc = resist = skill_dmg_boost = wpn_dmg_boost = soulshot = valor = guardian = conquer = 0
        try:
            attrs = self.attributes
            g_score = (
                0.5 * (attrs.g1 + attrs.g2 + attrs.g3 + attrs.g4 + attrs.g5 + attrs.g6 + attrs.g7) +
                0.005 * (attrs.g8 + attrs.g11 + attrs.g12 + attrs.g13 + attrs.g27 + attrs.g28 + attrs.g33) +
                0.0005 * (attrs.g9 + attrs.g10) +
                0.0001 * (attrs.g34) +
                0.05 * (attrs.g14 + attrs.g15 + attrs.g17 + attrs.g18 + attrs.g20 + attrs.g21 + attrs.g29 + attrs.g30 + attrs.g31 + attrs.g32) +
                0.005 * (attrs.g16 + attrs.g19 + attrs.g22 + attrs.g23 + attrs.g24 + attrs.g25 + attrs.g26) +
                0.15 * attrs.g35 + 0.2 * attrs.g36 + 0.2 * attrs.g37 + 0.25 * attrs.g38
            )
            mainclass_score = float(g_score)
            
            # backward compatibility for view returning attributes (though no longer accurate for original intent)
            dmg = attrs.g14
            acc = attrs.g15
            def_stat = attrs.g12
            soulshot = attrs.g35
            valor = attrs.g36
        except CharacterAttributes.DoesNotExist:
            pass

        # TOTAL SCORE
        total_score = characteristics_score + subclass_score + mainclass_score

        return {
            'total_score': total_score,
            'gear_stats_score': mainclass_score,
            'characteristics': characteristics_score,
            'subclass': subclass_score,
            'mainclass': mainclass_score,
            'dmg': dmg,
            'acc': acc,
            'def_stat': def_stat,
            'reduc': reduc,
            'resist': resist,
            'skill_dmg_boost': skill_dmg_boost,
            'wpn_dmg_boost': wpn_dmg_boost,
            'soulshot': soulshot,
            'valor': valor,
            'guardian': guardian,
            'conquer': conquer,
            'legend_class_point': 0,
            'legend_agathion_point': 0,
            'total_legend_codex': 0,
            'total_epic_mount': 0,
        }

    def calculate_gear_score(self):
        breakdown = self.calculate_gear_score_breakdown()
        return breakdown['total_score']"""

if "def calculate_gear_score_breakdown(self):" in content:
    content = content[:content.find("    def calculate_gear_score_breakdown(self):")] + "    " + new_func + "\n"
    with open('items/models.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("models.py updated successfully")
