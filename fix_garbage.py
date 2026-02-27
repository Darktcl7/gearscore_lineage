import sys
path = '/home/valkyrie.id/public_html/myproject/settings.py'

with open(path, 'r') as f:
    lines = f.readlines()

clean_lines = lines[:152]

final_block = """
# ==========================================
# KONFIGURASI PRODUKSI & CLOUDFLARE
# ==========================================
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

with open(path, 'w') as f:
    f.writelines(clean_lines)
    f.write(final_block)

print("Settings cleaned successfully.")
