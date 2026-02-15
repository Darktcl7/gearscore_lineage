import re
import os

html_content = """
<label for="id_uron_char_mag" class="form-label">Magic Damage</label>
<label for="id_acc_char_mag" class="form-label">Magic Accuracy</label>
<label for="id_crit_char_mag" class="form-label">Magic Critical Hit</label>
<label for="id_uron_char_mele" class="form-label">Melee Damage</label>
<label for="id_acc_char_mele" class="form-label">Melee Accuracy</label>
<label for="id_crit_char_mele" class="form-label">Melee Critical Hit</label>
<label for="id_uron_char_range" class="form-label">Ranged Damage</label>
<label for="id_acc_char_range" class="form-label">Ranged Accuracy</label>
<label for="id_crit_char_range" class="form-label">Ranged Critical Hit</label>
<label for="id_uror_char" class="form-label">Weapon Damage</label>
<label for="id_dopur_char" class="form-label">Extra Damage</label>
<label for="id_dopurcrit_char" class="form-label">Extra Damage (on Critical Hit)</label>
<label for="id_shdvur_char" class="form-label">Double Chance</label>
<label for="id_shtrur_char" class="form-label">Triple Chance</label>
<label for="id_blockor_char" class="form-label">Weapon Block</label>
<label for="id_scoratk_char" class="form-label">Attack Speed</label>
<label for="id_scor_char" class="form-label">Movement Speed</label>
<label for="id_scormag_char" class="form-label">Cast Speed</label>
<label for="id_snih_char" class="form-label">Damage Reduction</label>
<label for="id_snihurvmili" class="form-label">Melee Damage Reduction</label>
<label for="id_snihurvdal" class="form-label">Ranged Damage Reduction</label>
<label for="id_snihurmag" class="form-label">Magic Damage Reduction</label>
<label for="id_def_char" class="form-label">Defence</label>
<label for="id_uklvblis" class="form-label">Melee Evasion</label>
<label for="id_uklvdal" class="form-label">Ranged Evasion</label>
<label for="id_uklvmag" class="form-label">Magic Evasion</label>
<label for="id_sopr_char" class="form-label">Skill Resistance</label>
<label for="id_maxhp" class="form-label">Max HP</label>
<label for="id_maxmp" class="form-label">Max MP</label>
<label for="id_vosthp" class="form-label">HP Recovery (Tick)</label>
<label for="id_vostmp" class="form-label">MP Recovery (Tick)</label>
<label for="id_umenmp" class="form-label">MP Consumption Reduction</label>
<label for="id_umenper" class="form-label">Coldown Reduction</label>
<label for="id_maksgruz" class="form-label">Weigt Limit</label>
<label for="id_uveluror" class="form-label">Weapon Damage Boost</label>
<label for="id_sopruror" class="form-label">Weapon Defence</label>
<label for="id_uvelurumen" class="form-label">Skill Damage Boost</label>
<label for="id_soprurumen" class="form-label">Skill Defence</label>
<label for="id_snihkrit" class="form-label">Critical Hit Reduction</label>
<label for="id_soprkritmili" class="form-label">Mele Critical Hit Resistance</label>
<label for="id_soprktitreng" class="form-label">Ranged Critical Hit Resistance</label>
<label for="id_soprkritmag" class="form-label">Magic Critical Hit Resistance</label>
<label for="id_soprdvoinur" class="form-label">Double Resistance</label>
<label for="id_soprtroinur" class="form-label">Triple Resistance</label>
<label for="id_probivblock" class="form-label">Block Penetration</label>
<label for="id_ignrsnishur" class="form-label">Ignore Damage Reduction</label>
<label for="id_shansogl" class="form-label">Stun Accuracy</label>
<label for="id_soprogl" class="form-label">Stun Resistance</label>
<label for="id_snishurogl" class="form-label">Stun Reduction</label>
<label for="id_zashvogl" class="form-label">Stun Defence</label>
<label for="id_doptochogl" class="form-label">Extra Accuracy (to Stunned)</label>
<label for="id_ignordopsnishogl" class="form-label">Ignore Extra Reduction (to Stunned)</label>
<label for="id_shansuder" class="form-label">Hold Accuracy</label>
<label for="id_soprudersh" class="form-label">Hold Resistance</label>
<label for="id_snishurvsostuder" class="form-label">Hold Reduction</label>
<label for="id_zashvsostuder" class="form-label">Hold Defence</label>
<label for="id_doptchpouder" class="form-label">Extra Accuracy (to Held)</label>
<label for="id_ignordopshishpouder" class="form-label">Ignore Extra Reduction (to Held)</label>
<label for="id_shansagro" class="form-label">Vex Accuracy</label>
<label for="id_sopragro" class="form-label">Aggression Resistance</label>
<label for="id_shansbezmolv" class="form-label">Silence Accuracy</label>
<label for="id_soprbezmolv" class="form-label">Silence Resistance</label>
<label for="id_shansanomal" class="form-label">CC Accuracy</label>
<label for="id_sopranomal" class="form-label">CC Resistance</label>
<label for="id_umendlitanomal" class="form-label">CC Duration Reduction</label>
<label for="id_uveldlitanomalsost" class="form-label">Increases CC Duration</label>
<label for="id_moshzelvost" class="form-label">Potion Recovery Rate</label>
<label for="id_effectzelvost" class="form-label">Potion Recovery Amount</label>
<label for="id_effectlech" class="form-label">Heal Boost</label>
<label for="id_effectpollech" class="form-label">Received Heal Increase</label>
<label for="id_absolutvosthp" class="form-label">Fixed HP Recovery</label>
<label for="id_absolutvostmp" class="form-label">Fixed MP Recovery</label>
<label for="id_ignorshtrafvosthp" class="form-label">Ignore HP Recovery Penalty</label>
<label for="id_ignorshtrafvostmp" class="form-label">Ignore MP Recovery Penalty</label>
<label for="id_tochobichattak" class="form-label">Basic Attack Accuracy</label>
<label for="id_uronobichattak" class="form-label">Basic Attack Damage</label>
<label for="id_snishuronaotobichattak" class="form-label">Basic Attack Damage Reduction</label>
<label for="id_uveluronaotobichattak" class="form-label">Basic Attack Damage Boost</label>
<label for="id_sopruronuotobichattak" class="form-label">Basic Attack Damage Resistance</label>
<label for="id_tochnumen" class="form-label">Skill Accuracy</label>
<label for="id_zashotumen" class="form-label">Skill Evasion</label>
<label for="id_shansdvurotumen" class="form-label">Skill Double Chance</label>
<label for="id_soprdvoinurotumen" class="form-label">Skill Double Resistance</label>
<label for="id_shanstroinurotumen" class="form-label">Skill Triple Chance</label>
<label for="id_soprtroinurotumen" class="form-label">Skill Triple Resistance</label>
<label for="id_dopurvpvp_mele" class="form-label">Extra PvP Melee Damage</label>
<label for="id_tochnvpvp_mele" class="form-label">PvP Melee Accuracy</label>
<label for="id_dopurvpvp_range" class="form-label">Extra PvP Range Damage</label>
<label for="id_tochnvpvp_range" class="form-label">PvP Range Accuracy</label>
<label for="id_dopurvpvp_mag" class="form-label">Extra PvP Magic Damage</label>
<label for="id_tochnvpvp_mag" class="form-label">PvP Magic Accuracy</label>
<label for="id_kritatkpvp" class="form-label">PvP Critical Hit</label>
<label for="id_uklvmilipvp" class="form-label">PvP Melee Evasion</label>
<label for="id_uklvrengepvp" class="form-label">PvP Ranged Evasion</label>
<label for="id_uklmagpvp" class="form-label">PvP Magic Evasion</label>
<label for="id_snishurvmilipvp" class="form-label">PvP Melee Damage Reduction</label>
<label for="id_snishurvrengepvp" class="form-label">PvP Ranged Damage Reduction</label>
<label for="id_snishurvmagpvp" class="form-label">PvP Magic Damage Reduction</label>
<label for="id_soprurvblishpvp" class="form-label">PvP Melee Damage Resistance</label>
<label for="id_soprurvdalnpvp" class="form-label">PvP Ranged Damage Resistance</label>
<label for="id_soprmagurvpvp" class="form-label">PvP Magic Damage Resistance</label>
<label for="id_soprurotumenvpvp" class="form-label">PvP Skill Defence</label>
<label for="id_soprurotoruvpvp" class="form-label">PvP Weapon Defence</label>
<label for="id_shansdvoinurpvp" class="form-label">PvP Double Chance</label>
<label for="id_soprdvoinurvpvp" class="form-label">PvP Double Resistance</label>
<label for="id_shanstroinurvpvp" class="form-label">PvP Triple Chance</label>
<label for="id_soprtroinurvpvp" class="form-label">PvP Triple Resistance</label>
<label for="id_soprkritatkvpvp" class="form-label">PvP Critical Hit Resistance</label>
<label for="id_dopurvpve" class="form-label">Extra PvE Damage</label>
<label for="id_tochnvpve" class="form-label">PvE Accuracy</label>
<label for="id_zashvpve" class="form-label">PvE Defence</label>
<label for="id_snishurvpve" class="form-label">PvE Damage Reduction</label>
<label for="id_soproglvpve" class="form-label">PvE Stun Resistance</label>
<label for="id_uronvodoi" class="form-label">Water Type Damage</label>
<label for="id_uronognem" class="form-label">Fire Type Damage</label>
<label for="id_uronvetrom" class="form-label">Wind Type Damage</label>
<label for="id_uronzemlei" class="form-label">Eart Type Damage</label>
<label for="id_uronsvyat" class="form-label">Light Type Damage</label>
<label for="id_urontmoi" class="form-label">Dark Type Damage</label>
<label for="id_uveluronavodoi" class="form-label">Water Type Damage Boost</label>
<label for="id_uveluronaognem" class="form-label">Fire Type Damage Boost</label>
<label for="id_uvelurovavetrom" class="form-label">Wind Type Damage Boost</label>
<label for="id_uveluronazemlei" class="form-label">Eart Type Damage Boost</label>
<label for="id_uveluronasvyat" class="form-label">Light Type Damage Boost</label>
<label for="id_uveluronatmoi" class="form-label">Dark Type Damage Boost</label>
<label for="id_soprotvode" class="form-label">Water Type Resistance</label>
<label for="id_soprotogny" class="form-label">Fire Type Resistance</label>
<label for="id_soprotvetry" class="form-label">Wind Type Resistance</label>
<label for="id_soprotzemle" class="form-label">Eart Type Resistance</label>
<label for="id_soprotsvyat" class="form-label">Light Type Resistance</label>
<label for="id_soprottme" class="form-label">Dark Type Resistance</label>
<label for="id_tochnostszardushi" class="form-label">Soulshot Accuracy</label>
<label for="id_urotorushszardushi" class="form-label">Soulshot Weapon Damage</label>
<label for="id_uveluronaszardushi" class="form-label">Soulshot Weapon Damage Boost</label>
<label for="id_dopurszaryaddushi" class="form-label">Extra Soulshot Damage</label>
<label for="id_tochszaryaddushiviskach" class="form-label">Greated Soulshot Accuracy</label>
<label for="id_uronotorushszarviskach" class="form-label">Greated Soulshot Weapon Damage</label>
<label for="id_uveluronotorushsvishkach" class="form-label">Greated Soulshot weapon Damage Boost</label>  
<label for="id_dopurszardushiviskach" class="form-label">Extra Greated Soulshot Damage</label>
<label for="id_urotstreli" class="form-label">Arrow Damage</label>
<label for="id_dalnstreli" class="form-label">Extra Range</label>
<label for="id_uvelnapoeng" class="form-label">Blessing Recharge Increase</label>
<label for="id_uvelpoluchengzaporysh" class="form-label">Oracle Quest Blessing Reward Increase</label>    
<label for="id_umenshrasheng" class="form-label">Blessing Conservation</label>
<label for="id_bonuskopyt" class="form-label">Bonus EXP</label>
"""

pattern = r'<label for="id_(\w+)" class="form-label">([^<]+)</label>'

class_lines = [
    "",
    "class CharacteristicsStats(models.Model):",
    "    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='characteristics_stats')",
    ""
]

matches = re.findall(pattern, html_content)
for name, label in matches:
    class_lines.append(f'    {name} = models.IntegerField("{label}", default=0)')

class_lines.append("")
class_lines.append("    def __str__(self):")
class_lines.append("        return f\"Characteristics for {self.character.name}\"")
class_lines.append("")

# Read existing models.py
model_path = 'items/models.py'
with open(model_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove corrupted lines (lines containing spaced out characters like "c l a s s")
clean_lines = []
for line in lines:
    # Check for corruption pattern (space between every char)
    if "c l a s s   C h a r a c t e r i s t i c s" in line:
        break
    clean_lines.append(line)

# Also check if it ends with GearScoreLog and we appended before, good to just ensure clean state
# The last valid class is GearScoreLog. Let's find safe end.
# Actually I'll just append. The previous corruption check handles the mess I made.

# Write back
with open(model_path, 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)
    f.write('\n'.join(class_lines))

print(f"Successfully updated {model_path} with {len(matches)} fields.")
