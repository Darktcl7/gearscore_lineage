import os
path = '/home/valkyrie.id/public_html/myproject/settings.py'
with open(path, 'r') as f:
    c = f.read()
c = c.replace('USE_X_FORWARDED_HOST = True', 'USE_X_FORWARDED_HOST = False')
c = c.replace('USE_X_FORWARDED_PORT = True', 'USE_X_FORWARDED_PORT = False')
with open(path, 'w') as f:
    f.write(c)
print("Done modifying.")
