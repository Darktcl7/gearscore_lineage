
import re

path = r"D:\Django Project\Alto Project\items\models.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def add_enchant_field(content, field_name, verbose_name):
    # Regex look for: pvp_field = models.CharField(...)
    # Replace with: pvp_field = ... \n    pvp_field_enchant = models.IntegerField(...)
    
    # Using more flexible whitespace regex
    pattern = re.compile(f"({field_name} = models\.CharField\(.*?blank=True\))", re.DOTALL)
    
    enchant_field = f'''\\1
    {field_name}_enchant = models.IntegerField("{verbose_name} Enchant Level", default=0, validators=[MinValueValidator(0), MaxValueValidator(11)], help_text="Enchant level +0 to +11")'''
    
    if pattern.search(content):
        return pattern.sub(enchant_field, content, count=1)
    else:
        print(f"WARNING: Could not find field {field_name}")
        return content

content = add_enchant_field(content, "pvp_top_armor", "PvP Armor")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("models.py saved.")
