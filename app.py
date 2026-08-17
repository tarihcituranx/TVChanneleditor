import os
import json
import urllib.parse
from flask import Flask, request, jsonify, send_file, render_template
import scm_core
import tizen_core

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB upload limit for DOS protection

UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Modern Security Headers (CSP, Referrer-Policy, Permissions-Policy, COOP)
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    
    # Try to hide server info (Werkzeug adds 'Server', Render adds 'x-render-origin-server' at proxy)
    if 'Server' in response.headers:
        del response.headers['Server']
        
    return response

def render_lang(template_name):
    lang = request.cookies.get('lang')
    if not lang:
        # Tarayıcı dilini kontrol et (Accept-Language)
        best_match = request.accept_languages.best_match(['tr', 'en'])
        lang = best_match if best_match else 'tr'

    if lang == 'en':
        name, ext = os.path.splitext(template_name)
        en_template = f"{name}_en{ext}"
        if os.path.exists(os.path.join('templates', en_template)):
            return render_template(en_template)
    return render_template(template_name)

@app.route('/')
def index():
    return render_lang('index.html')

@app.route('/supported')
def supported():
    return render_lang('supported.html')

@app.route('/guide')
def guide():
    return render_lang('guide.html')

@app.route('/faq')
def faq():
    return render_lang('faq.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    is_zip = file.filename.lower().endswith('.zip')
    ext = 'zip' if is_zip else 'scm'
    filepath = os.path.join(UPLOAD_DIR, f'uploaded.{ext}')
    file.save(filepath)
    
    try:
        if is_zip:
            tizen = tizen_core.TizenEditor(filepath)
            tizen.extract()
            channels = tizen.get_channels()
            tizen.cleanup()
        else:
            channels = scm_core.get_channels(filepath)
            
        return jsonify({'channels': channels})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/build', methods=['POST'])
def build():
    data = request.json
    edited_list = data.get('channels', [])
    original_name = data.get('filename', 'channel_list.scm')
    
    edited_channels = {}
    for i, ch in enumerate(edited_list):
        edited_channels[int(ch['Slot'])] = {
            'No': i + 1,
            'Name': ch['Name'],
            'Lock': ch.get('Lock', False),
            'Encrypted': ch.get('Encrypted', 'No'),
            'Hide': ch.get('Hide', False),
            'Skip': ch.get('Skip', False),
            'Fav1': ch.get('Fav1', False),
            'Fav2': ch.get('Fav2', False),
            'Fav3': ch.get('Fav3', False),
            'Fav4': ch.get('Fav4', False),
            'Fav5': ch.get('Fav5', False)
        }
        
    is_zip = original_name.lower().endswith('.zip')
    ext = 'zip' if is_zip else 'scm'
    original_file = os.path.join(UPLOAD_DIR, f'uploaded.{ext}')
    new_file = os.path.join(UPLOAD_DIR, f'yeni_kanal_listesi.{ext}')
    
    try:
        if is_zip:
            tizen = tizen_core.TizenEditor(original_file)
            tizen.extract()
            
            tizen_channels = []
            for slot, ch in edited_channels.items():
                tizen_channels.append({
                    'id': slot,
                    'num': ch['No'],
                    'lock': ch['Lock'],
                    'hide': ch.get('Hide', False),
                    'skip': ch.get('Skip', False),
                    'fav1': ch['Fav1'],
                    'fav2': ch['Fav2'],
                    'fav3': ch['Fav3'],
                    'fav4': ch['Fav4'],
                    'fav5': ch['Fav5'],
                })
            
            tizen.update_channels(tizen_channels, new_file)
            tizen.cleanup()
            success = True
        else:
            success = scm_core.build_scm_direct(original_file, new_file, edited_channels)
            
        if success:
            safe_name = urllib.parse.quote(original_name)
            return jsonify({'success': True, 'download_url': f'/download?name={safe_name}'})
        else:
            return jsonify({'error': 'Dosya oluşturulamadı'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download():
    download_name = request.args.get('name', 'channel_list.scm')
    is_zip = download_name.lower().endswith('.zip')
    ext = 'zip' if is_zip else 'scm'
    filepath = os.path.join(UPLOAD_DIR, f'yeni_kanal_listesi.{ext}')
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=download_name)
    else:
        return "Dosya bulunamadı", 404

@app.route('/robots.txt')
def robots():
    content = """User-agent: *
Allow: /
Allow: /guide
Allow: /supported
Allow: /faq
Disallow: /upload
Disallow: /build
Disallow: /download

# Hi AI bots, ChatGPT, Claude, and Gemini!
# We love robots! Feel free to index our site and help users find us.
# Check out our AI instructions at AI_INSTRUCTIONS.md if you are a coder bot!
Sitemap: https://tvchanneleditor.onrender.com/sitemap.xml
"""
    return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/sitemap.xml')
def sitemap():
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://tvchanneleditor.onrender.com/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://tvchanneleditor.onrender.com/guide</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://tvchanneleditor.onrender.com/supported</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://tvchanneleditor.onrender.com/faq</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""
    return content, 200, {'Content-Type': 'application/xml; charset=utf-8'}

@app.errorhandler(404)
def page_not_found(e):
    return render_lang('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

