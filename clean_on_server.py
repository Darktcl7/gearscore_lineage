import os
path = '/home/valkyrie.id/public_html/myproject/settings.py'
with open(path, 'r') as f:
    lines = f.readlines()

tags = ['DEBUG =', 'ALLOWED_HOSTS =', 'SECURE_PROXY_SSL_HEADER =', 'USE_X_FORWARDED_HOST =', 'USE_X_FORWARDED_PORT =', 'CSRF_TRUSTED_ORIGINS =', 'CORS_ALLOW_ALL_ORIGINS =', 'STATIC_ROOT =', 'import os']
new_lines = [l for l in lines if not any(l.strip().startswith(t) for t in tags)]

prod = [
    'import os\n',
    'DEBUG = False\n',
    "ALLOWED_HOSTS = ['valkyrie.id', 'www.valkyrie.id', '148.230.97.130', '127.0.0.1', 'localhost']\n",
    "SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')\n",
    'USE_X_FORWARDED_HOST = False\n',
    'USE_X_FORWARDED_PORT = False\n',
    "CSRF_TRUSTED_ORIGINS = ['https://valkyrie.id', 'https://www.valkyrie.id']\n",
    'CORS_ALLOW_ALL_ORIGINS = True\n',
    'STATIC_ROOT = BASE_DIR / "staticfiles"\n'
]

with open(path, 'w') as f:
    f.writelines(new_lines)
    f.write('\n# --- FINAL CLEAN SETTINGS ---\n')
    f.writelines(prod)

print("Settings cleaned.")
