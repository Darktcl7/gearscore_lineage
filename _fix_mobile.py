import re

path = r'd:\Django Project\Alto Project\items\static\items\css\mobile.css'
with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Change 768px to 900px for consistency with base.html
css = css.replace('@media (max-width: 768px)', '@media (max-width: 900px)')

# 2. Main Padding to 0
old_main = '''    main {
        padding: 5px !important;
        overflow: visible !important;
    }'''
new_main = '''    main {
        padding: 0 !important;
        overflow: visible !important;
        width: 100% !important;
        max-width: 100% !important;
    }'''
css = css.replace(old_main, new_main)

# 3. Common containers to 0 margin, 0 radius
css = re.sub(
    r'(/\* Common containers.*\n.*?{)\s*margin-left:.*?;\s*margin-right:.*?;\s*margin-top:(.*?);\s*border-radius:.*?;',
    r'\1\n        margin-left: 0 !important;\n        margin-right: 0 !important;\n        margin-top: \2;\n        border-radius: 0 !important;',
    css
)

# 4. DKP pages
css = re.sub(
    r'(\.lb-container,\s*\.profile-container\s*{)\s*margin-left:.*?;\s*margin-right:.*?;\s*margin-top:(.*?);\s*border-radius:.*?;',
    r'\1\n        margin-left: 0 !important;\n        margin-right: 0 !important;\n        margin-top: \2;\n        border-radius: 0 !important;',
    css
)

css = re.sub(
    r'(\.dkp-manage-container\s*{)\s*margin-left:.*?;\s*margin-right:.*?;\s*margin-top:(.*?);\s*border-radius:.*?;',
    r'\1\n        margin-left: 0 !important;\n        margin-right: 0 !important;\n        margin-top: \2;\n        border-radius: 0 !important;',
    css
)

css = re.sub(
    r'(\.manage-container\s*{)\s*margin-left:.*?;\s*margin-right:.*?;\s*margin-top:(.*?);\s*border-radius:.*?;',
    r'\1\n        margin-left: 0 !important;\n        margin-right: 0 !important;\n        margin-top: \2;\n        border-radius: 0 !important;',
    css
)

css = re.sub(
    r'(\.discord-container\s*{)\s*margin-left:.*?;\s*margin-right:.*?;\s*margin-top:(.*?);',
    r'\1\n        margin-left: 0 !important;\n        margin-right: 0 !important;\n        margin-top: \2;\n        border-radius: 0 !important;',
    css
)

# 5. Max-width 480px section -> just make sure left/right are 0
css = re.sub(
    r'(margin-left:\s*)3px(.*?\n\s*margin-right:\s*)3px(.*?\n\s*margin-top:.*?;\n\s*border-radius:\s*)8px',
    r'\g<1>0\g<2>0\g<3>0',
    css
)


with open(path, 'w', encoding='utf-8') as f:
    f.write(css)
print('SUCCESS')
