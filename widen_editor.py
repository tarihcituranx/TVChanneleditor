import glob

# For index pages, we can just inject a style tag that widens the app-container
# Since the index page has the editor.
files = glob.glob('templates/index*.html')
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<style>.app-container { max-width: 1280px !important; }</style>' not in content:
        content = content.replace('{% block content %}', '{% block content %}\n<style>.app-container { max-width: 1280px !important; }</style>')
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

print("Editor widened!")
