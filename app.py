import os
import json
import urllib.parse
from flask import Flask, request, jsonify, send_file, render_template
import scm_core

app = Flask(__name__)

UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    
    filepath = os.path.join(UPLOAD_DIR, 'uploaded.scm')
    file.save(filepath)
    
    try:
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
            'Fav1': ch.get('Fav1', False),
            'Fav2': ch.get('Fav2', False),
            'Fav3': ch.get('Fav3', False),
            'Fav4': ch.get('Fav4', False),
            'Fav5': ch.get('Fav5', False)
        }
        
    original_scm = os.path.join(UPLOAD_DIR, 'uploaded.scm')
    new_scm = os.path.join(UPLOAD_DIR, 'yeni_kanal_listesi.scm')
    
    success = scm_core.build_scm_direct(original_scm, new_scm, edited_channels)
    
    if success:
        safe_name = urllib.parse.quote(original_name)
        return jsonify({'success': True, 'download_url': f'/download?name={safe_name}'})
    else:
        return jsonify({'error': 'SCM dosyası oluşturulamadı'}), 500

@app.route('/download')
def download():
    download_name = request.args.get('name', 'channel_list.scm')
    filepath = os.path.join(UPLOAD_DIR, 'yeni_kanal_listesi.scm')
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=download_name)
    else:
        return "Dosya bulunamadı", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
