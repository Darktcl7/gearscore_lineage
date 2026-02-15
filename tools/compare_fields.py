import re

# Read reference HTML
with open(r"D:\Django Project\Alto Project\alto files\Character characteristics.html", 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read models.py
with open(r"D:\Django Project\Alto Project\items\models.py", 'r', encoding='utf-8') as f:
    models_content = f.read()

# Extract fields from HTML (name attributes)
html_fields = re.findall(r'name="([^"]+)"', html_content)
html_fields = [f for f in html_fields if f != 'csrfmiddlewaretoken']
html_fields = list(dict.fromkeys(html_fields))  # Remove duplicates, keep order

# Extract fields from CharacteristicsStats model
# Find the class definition
model_match = re.search(r'class CharacteristicsStats\(models\.Model\):(.*?)(?=class |\Z)', models_content, re.DOTALL)
if model_match:
    model_content = model_match.group(1)
    model_fields = re.findall(r'(\w+)\s*=\s*models\.IntegerField', model_content)
else:
    model_fields = []

print("=" * 60)
print("PERBANDINGAN FIELD: REFERENSI HTML vs MODEL")
print("=" * 60)
print(f"\nTotal fields di Referensi HTML: {len(html_fields)}")
print(f"Total fields di Model: {len(model_fields)}")

# Check missing in model
missing_in_model = [f for f in html_fields if f not in model_fields]
missing_in_html = [f for f in model_fields if f not in html_fields]

print(f"\n--- MISSING IN MODEL (ada di HTML tapi tidak di Model): {len(missing_in_model)} ---")
for f in missing_in_model:
    print(f"  - {f}")

print(f"\n--- EXTRA IN MODEL (ada di Model tapi tidak di HTML): {len(missing_in_html)} ---")
for f in missing_in_html:
    print(f"  - {f}")

if len(missing_in_model) == 0 and len(missing_in_html) == 0:
    print("\n✅ SEMUA FIELD SUDAH SAMA!")
else:
    print(f"\n⚠️  Ada perbedaan yang perlu diperbaiki")

print("\n" + "=" * 60)
print("DAFTAR FIELD REFERENSI HTML (urutan asli):")
print("=" * 60)
for i, f in enumerate(html_fields, 1):
    status = "✅" if f in model_fields else "❌"
    print(f"{i:3}. {status} {f}")
