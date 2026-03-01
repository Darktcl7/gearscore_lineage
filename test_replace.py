import re

with open('items/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find CharacteristicsStats and all its contents until the ActivityEvent model
pattern = re.compile(r'class CharacteristicsStats\(models\.Model\):(.*?)def __str__\(self\):\n\s+return f"Characteristics.*?name\}"\s*\n', re.DOTALL)

new_class = """class CharacteristicsStats(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='characteristics_stats')

    # KELOMPOK A - CORE PVP DEFENSE
    a1 = models.IntegerField("PvP Melee Damage Reduction", default=0)
    a2 = models.IntegerField("PvP Ranged Damage Reduction", default=0)
    a3 = models.IntegerField("PvP Magic Damage Reduction", default=0)
    a4 = models.IntegerField("PvP Melee Evasion", default=0)
    a5 = models.IntegerField("PvP Ranged Evasion", default=0)
    a6 = models.IntegerField("PvP Magic Evasion", default=0)
    a7 = models.IntegerField("PvP Skill Defense (%)", default=0)
    a8 = models.IntegerField("PvP Weapon Defense (%)", default=0)
    a9 = models.IntegerField("PvP Melee Damage Resistance (%)", default=0)
    a10 = models.IntegerField("PvP Ranged Damage Resistance (%)", default=0)
    a11 = models.IntegerField("PvP Magic Damage Resistance (%)", default=0)
    a12 = models.IntegerField("PvP Critical Hit Resistance (%)", default=0)

    # KELOMPOK B - CORE PVP OFFENSE
    b1 = models.IntegerField("Extra PvP Melee Damage", default=0)
    b2 = models.IntegerField("Extra PvP Ranged Damage", default=0)
    b3 = models.IntegerField("Extra PvP Magic Damage", default=0)
    b4 = models.IntegerField("PvP Melee Accuracy", default=0)
    b5 = models.IntegerField("PvP Ranged Accuracy", default=0)
    b6 = models.IntegerField("PvP Magic Accuracy", default=0)
    b7 = models.IntegerField("PvP Critical Hit (%)", default=0)
    b8 = models.IntegerField("PvP Double Chance (%)", default=0)
    b9 = models.IntegerField("PvP Triple Chance (%)", default=0)

    # KELOMPOK C - CROWD CONTROL
    c1 = models.IntegerField("Stun Accuracy (%)", default=0)
    c2 = models.IntegerField("Stun Resistance (%)", default=0)
    c3 = models.IntegerField("Hold Accuracy (%)", default=0)
    c4 = models.IntegerField("Hold Resistance (%)", default=0)
    c5 = models.IntegerField("CC Accuracy (%)", default=0)
    c6 = models.IntegerField("CC Resistance (%)", default=0)
    c7 = models.IntegerField("CC Duration Reduction (%)", default=0)
    c8 = models.IntegerField("Increases CC Duration (%)", default=0)
    c9 = models.IntegerField("Extra Accuracy (to Stunned)", default=0)
    c10 = models.IntegerField("Ignore Extra Reduction (to Stunned)", default=0)
    c11 = models.IntegerField("Hold Defense", default=0)
    c12 = models.IntegerField("Stun Reduction", default=0)
    c13 = models.IntegerField("Stun Defense", default=0)
    c14 = models.IntegerField("Vex Accuracy (%)", default=0)
    c15 = models.IntegerField("Aggression Resistance (%)", default=0)
    c16 = models.IntegerField("Silence Accuracy (%)", default=0)
    c17 = models.IntegerField("Silence Resistance (%)", default=0)

    # KELOMPOK D - SURVIVAL
    d1 = models.IntegerField("Heal Boost (%)", default=0)
    d2 = models.IntegerField("Received Heal Increase (%)", default=0)
    d3 = models.IntegerField("Potion Recovery Rate (%)", default=0)
    d4 = models.IntegerField("Potion Recovery Amount", default=0)
    d5 = models.IntegerField("Fixed HP Recovery", default=0)
    d6 = models.IntegerField("Fixed MP Recovery", default=0)
    d7 = models.IntegerField("Ignore HP Recovery Penalty (%)", default=0)
    d8 = models.IntegerField("Ignore MP Recovery Penalty (%)", default=0)

    # KELOMPOK E - SECONDARY DEFENSE
    e1 = models.IntegerField("Critical Hit Reduction", default=0)
    e2 = models.IntegerField("Melee Critical Hit Resistance (%)", default=0)
    e3 = models.IntegerField("Ranged Critical Hit Resistance (%)", default=0)
    e4 = models.IntegerField("Magic Critical Hit Resistance (%)", default=0)
    e5 = models.IntegerField("Double Resistance (%)", default=0)
    e6 = models.IntegerField("Triple Resistance (%)", default=0)
    e7 = models.IntegerField("PvP Double Resistance (%)", default=0)
    e8 = models.IntegerField("PvP Triple Resistance (%)", default=0)
    e9 = models.IntegerField("Skill Double Resistance (%)", default=0)
    e10 = models.IntegerField("Skill Triple Resistance (%)", default=0)

    # KELOMPOK F - SECONDARY OFFENSE
    f1 = models.IntegerField("Block Penetration (%)", default=0)
    f2 = models.IntegerField("Ignore Damage Reduction", default=0)
    f3 = models.IntegerField("Extra Damage (on Critical Hit)", default=0)
    f4 = models.IntegerField("Soulshot Weapon Damage Boost (%)", default=0)
    f5 = models.IntegerField("Extra Soulshot Damage", default=0)
    f6 = models.IntegerField("Greater Soulshot Weapon Damage Boost (%)", default=0)
    f7 = models.IntegerField("Extra Greater Soulshot Damage", default=0)
    f8 = models.IntegerField("Double Chance (%)", default=0)
    f9 = models.IntegerField("Triple Chance (%)", default=0)
    f10 = models.IntegerField("Soulshot Accuracy", default=0)
    f11 = models.IntegerField("Soulshot Weapon Damage", default=0)
    f12 = models.IntegerField("Greater Soulshot Accuracy", default=0)
    f13 = models.IntegerField("Greater Soulshot Weapon Damage", default=0)

    def calculate_total_score(self):
        A = 2 * (self.a1 + self.a2 + self.a3 + self.a4 + self.a5 + self.a6) + 0.02 * (self.a7 + self.a8 + self.a9 + self.a10 + self.a11 + self.a12)
        B = 1.8 * (self.b1 + self.b2 + self.b3 + self.b4 + self.b5 + self.b6) + 0.018 * (self.b7 + self.b8 + self.b9)
        C = 0.015 * (self.c1 + self.c2 + self.c3 + self.c4 + self.c5 + self.c6 + self.c7 + self.c8 + self.c14 + self.c15 + self.c16 + self.c17) + 1.5 * (self.c9 + self.c10 + self.c11 + self.c12 + self.c13)
        D = 0.012 * (self.d1 + self.d2 + self.d3 + self.d7 + self.d8) + 1.2 * (self.d4 + self.d5 + self.d6)
        E = 1.0 * self.e1 + 0.01 * (self.e2 + self.e3 + self.e4 + self.e5 + self.e6 + self.e7 + self.e8 + self.e9 + self.e10)
        F = 0.01 * (self.f1 + self.f4 + self.f6 + self.f8 + self.f9) + 1.0 * (self.f2 + self.f3 + self.f5 + self.f7 + self.f10 + self.f11 + self.f12 + self.f13)
        return A + B + C + D + E + F

    def __str__(self):
        return f\"Characteristics Stats for {self.character.name}\"\n"""
print(len(content))
new_content, count = pattern.subn(new_class, content)
if count > 0:
    with open('items/models.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced CharacteristicsStats successfully.")
else:
    print("Failed to replace CharacteristicsStats.")
