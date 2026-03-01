import os

appdata = os.environ.get('APPDATA')
if not appdata:
    appdata = r"C:\Users\chlui\AppData\Roaming"

history_path = os.path.join(appdata, 'Code', 'User', 'History')
files = []
for root, _, fnames in os.walk(history_path):
    for f in fnames:
        files.append(os.path.join(root, f))

found = []
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            if 'class CharacteristicsStats(models.Model):' in content and 'MONTHLY RECAPS FOR DKP SYSTEM' in content:
                found.append((f, os.path.getmtime(f)))
    except:
        pass

found.sort(key=lambda x: x[1], reverse=True)
for f, mtime in found[:5]:
    print(f"Matches: {f} Time: {mtime}")
