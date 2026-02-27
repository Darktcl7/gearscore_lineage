import os

path = '/home/valkyrie.id/public_html/myproject/settings.py'

# 1. Read the file
with open(path, 'r') as f:
    lines = f.readlines()

# 2. Filter out all production tags
tags = [
    'DEBUG =', 
    'ALLOWED_HOSTS =', 
    'SECURE_PROXY_SSL_HEADER =', 
    'USE_X_FORWARDED_HOST =', 
    'USE_X_FORWARDED_PORT =', 
    'CSRF_TRUSTED_ORIGINS =', 
    'CORS_ALLOW_ALL_ORIGINS =', 
    'STATIC_ROOT =', 
    'import os'
]

new_lines = []
for line in lines:
    stripped = line.strip()
    is_tag = False
    for tag in tags:
        if stripped.startswith(tag):
            is_tag = True
            break
    if not is_tag:
        new_lines.append(line)

# 3. Define the final block
final_block = """
import os
DEBUG = False
ALLOWED_HOSTS = ['valkyrie.id', 'www.valkyrie.id', '148.230.97.130', '127.0.0.1', 'localhost']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = False
USE_X_FORWARDED_PORT = False
CSRF_TRUSTED_ORIGINS = ['https://valkyrie.id', 'https://www.valkyrie.id']
CORS_ALLOW_ALL_ORIGINS = True
STATIC_ROOT = BASE_DIR / "staticfiles"
"""

# 4. Write back
with open(path, 'w') as f:
    f.writelines(new_lines)
    f.write("\\n# --- FINAL CLEAN SETTINGS ---\\n")
    f.write(final_block)

print("Settings successfully cleaned.")
