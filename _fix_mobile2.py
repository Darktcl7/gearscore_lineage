path = r'd:\Django Project\Alto Project\items\static\items\css\mobile.css'
with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

# Add box-sizing rules
new_rules = '''
    /* Prevent horizontal overflow */
    *, *:before, *:after {
        box-sizing: border-box !important;
    }

    /* Additional safety for forms and panels */
    .panel-card, .glass-card, .form-group, input, select, textarea {
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    body, html {
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }
'''

if '/* Prevent horizontal overflow */' not in css:
    css = css.replace('/* ---- TABLET (max-width: 900px) ---- */\n@media (max-width: 900px) {\n', 
                     '/* ---- TABLET (max-width: 900px) ---- */\n@media (max-width: 900px) {\n' + new_rules)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("SUCCESS")
else:
    print("ALREADY APPLIED")
