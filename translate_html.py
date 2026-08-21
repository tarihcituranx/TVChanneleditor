import requests
import glob
import os
import time

# SET YOUR API KEY HERE OR PASS AS ENVIRONMENT VARIABLE
DEEPL_KEY = os.environ.get('DEEPL_KEY', 'YOUR_DEEPL_API_KEY_HERE')
URL = "https://api-free.deepl.com/v2/translate"

# Full list of supported target languages
langs = ['DE', 'RU', 'ES', 'IT', 'FR', 'AR', 'FA', 'AZ', 'PT']

def translate_html(text, target_lang):
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": [text],
        "target_lang": target_lang,
        "source_lang": "EN",
        "tag_handling": "html"
    }
    response = requests.post(URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        print(f"Error: {response.status_code} {response.text}")
        return text

en_files = glob.glob('templates/*_en.html')

for lang in langs:
    print(f"\n--- Translating to {lang} ---")
    lang_lower = lang.lower()
    for file in en_files:
        # Swagger and base_en.html are handled manually
        if 'swagger' in file or 'base_en.html' in file:
            continue
            
        print(f"Translating {file} to {lang}...")
        with open(file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        translated = translate_html(html_content, lang)
        
        # RTL support for Arabic and Farsi
        if lang in ['AR', 'FA']:
            translated = translated.replace('lang="en"', f'lang="{lang_lower}" dir="rtl"')
        else:
            translated = translated.replace('lang="en"', f'lang="{lang_lower}"')
            
        # Fix DeepL escaping Jinja quotes
        translated = translated.replace('&quot;', '"')
        translated = translated.replace('base_en.html', f'base_{lang_lower}.html')
        
        out_file = file.replace('_en.html', f'_{lang_lower}.html')
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(translated)
            
        # Sleep to avoid rate limiting
        time.sleep(1)

print("Translation complete!")
