import http.server
import socketserver
import json
import os
import urllib.parse
import cgi
import scm_core

PORT = 5000
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
            # simple static file serving
            try:
                filepath = self.path[1:]
                with open(filepath, 'rb') as f:
                    self.send_response(200)
                    if filepath.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    elif filepath.endswith('.js'):
                        self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception:
                self.send_error(404, "File not found")
        elif self.path.startswith('/download'):
            from urllib.parse import urlparse, parse_qs
            parsed_path = urlparse(self.path)
            query = parse_qs(parsed_path.query)
            download_name = query.get('name', ['channel_list.scm'])[0]
            
            filepath = os.path.join(UPLOAD_DIR, 'yeni_kanal_listesi.scm')
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{download_name}"')
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/upload':
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                fields = cgi.parse_multipart(self.rfile, pdict)
                file_data = fields.get('file')[0]
                
                filepath = os.path.join(UPLOAD_DIR, 'uploaded.scm')
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                
                channels = scm_core.get_channels(filepath)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'channels': channels}).encode('utf-8'))
            else:
                self.send_error(400, "Bad Request")
                
        elif self.path == '/build':
            length = int(self.headers['content-length'])
            body = self.rfile.read(length)
            data = json.loads(body)
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
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if success:
                safe_name = urllib.parse.quote(original_name)
                self.wfile.write(json.dumps({'success': True, 'download_url': f'/download?name={safe_name}'}).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({'error': 'Failed to build SCM file'}).encode('utf-8'))

with socketserver.TCPServer(("", PORT), SCMHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
