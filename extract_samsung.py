import re
from bs4 import BeautifulSoup

with open("/home/turan/.gemini/antigravity-cli/brain/2bc771a7-b9e2-4e0a-8934-0748981df9e0/.system_generated/steps/2279/content.md", "r", encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

# Find the main content area. In Samsung support, it's usually inside an article or specific classes.
# We'll just look for paragraphs containing the text.
paragraphs = soup.find_all(['p', 'h3', 'li', 'h4', 'span'])

text_content = []
for p in paragraphs:
    text = p.get_text().strip()
    if text and len(text) > 15:
        text_content.append(text)

# We want the instructions. Look for lines like "Menü", "Yayın", "Otomatik Ayarlama"
interesting = []
for t in text_content:
    if any(keyword in t.lower() for keyword in ['türksat', 'tkgs', 'menü', 'yayın', 'uydu']):
        if t not in interesting:
            interesting.append(t)

for i, line in enumerate(interesting[:40]):
    print(line)
