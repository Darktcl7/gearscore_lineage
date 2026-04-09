import sys

with open('dkp/templates/dkp/auction.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace head and body with extends and blocks
start_body_idx = html.find('<body>') + 6
end_body_idx = html.find('</body>')

body_content = html[start_body_idx:end_body_idx]

# Extract styles
start_style_idx = html.find('<style>')
end_style_idx = html.find('</style>') + 8
styles = html[start_style_idx:end_style_idx]

# Remove the body, html, * rules from styles to avoid overriding base
styles = styles.replace('body {\n            font-family: \'Outfit\', sans-serif;\n            background: #0d0d0d;\n            color: #e0e0e0;\n            min-height: 100vh;\n        }', '')
styles = styles.replace('* { margin: 0; padding: 0; box-sizing: border-box; }', '')

# Replace .main-container and .page-header with activity-container pattern
styles += '''
<style>
.activity-container {
    min-height: 60vh;
    margin-top: 0;
    margin-bottom: 40px;
    display: flex;
    flex-direction: column;
    background: rgba(10,10,10,0.9);
    border-radius: 20px;
    padding: 30px;
    margin-left: max(20px, 10%);
    margin-right: max(20px, 10%);
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
    border: 1px solid #222;
    color: white;
}

.page-header {
    background: transparent;
    border: none;
    border-bottom: 1px solid #333;
    padding: 0 0 20px 0;
    margin-bottom: 20px;
}
.main-container { max-width: 100%; padding: 0; }
</style>
'''

new_html = f'''{{% extends 'items/base.html' %}}
{{% load static %}}
{{% block title %}}DKP Auction House{{% endblock %}}
{{% block extra_body_attributes %}}class="fullscreen-page"{{% endblock %}}

{{% block extra_head %}}
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
''' + styles + '''
{% endblock %}

{% block content %}
<div class="activity-container">
''' + body_content + '''
</div>
{% endblock %}
'''

with open('dkp/templates/dkp/auction.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
