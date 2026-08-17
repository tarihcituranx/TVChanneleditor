import http.server
import socketserver
import json
import os
import urllib.parse
import cgi
import scm_core

PORT = int(os.environ.get('PORT', 5000))
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SCMHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('templates/index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path.startswith('/static/'):
@app.route('/')
def index():
    return render_template('index.html')

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
            'Name': ch['Name']
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
