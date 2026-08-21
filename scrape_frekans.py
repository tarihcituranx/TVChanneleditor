import json
from html.parser import HTMLParser

class FrekansParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.in_tr = False
        self.in_td_name = False
        self.in_td_freq = False
        
        self.td_count = 0
        self.current_channel = ""
        self.current_freq = ""
        
        self.channels = {}

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            # Tablo id'si resultBody olan tbody'i arıyoruz (ya da genel olarak tbody)
            for attr in attrs:
                if attr[0] == "id" and attr[1] == "resultBody":
                    self.in_tbody = True
            # Eğer id yoksa da tbody içindeyiz
            if not self.in_tbody and tag == 'tbody':
                 self.in_tbody = True
                 
        if self.in_tbody and tag == "tr":
            self.in_tr = True
            self.td_count = 0
            self.current_channel = ""
            self.current_freq = ""
            
        if self.in_tr and tag == "td":
            self.td_count += 1
            if self.td_count == 2: # 2. sütun Kanal Adı
                self.in_td_name = True
            elif self.td_count == 3: # 3. sütun Frekans
                self.in_td_freq = True

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_tbody = False
        if tag == "tr" and self.in_tr:
            self.in_tr = False
            if self.current_channel and self.current_freq:
                name = self.current_channel.strip()
                # 11.794 gibi gelen frekansı 11794 yapalım
                freq = self.current_freq.strip().replace(".", "")
                if name and freq.isdigit():
                    self.channels[name.upper()] = int(freq)
                    
        if tag == "td":
            self.in_td_name = False
            self.in_td_freq = False

    def handle_data(self, data):
        if self.in_td_name:
            self.current_channel += data
        if self.in_td_freq:
            self.current_freq += data

# Dosyayı okuyalım
with open("/home/turan/.gemini/antigravity-cli/brain/c4f87790-993d-47bf-93dd-6efcac7f3f19/.system_generated/steps/789/content.md", "r", encoding="utf-8") as f:
    html_content = f.read()

parser = FrekansParser()
parser.feed(html_content)

print(f"Toplam {len(parser.channels)} kanal frekansı bulundu.")
with open("/home/turan/samsung-channel-editor-web/static/data/frekanslar.json", "w", encoding="utf-8") as f:
    json.dump(parser.channels, f, ensure_ascii=False, indent=4)
print("Frekanslar başarıyla static/data/frekanslar.json dosyasına kaydedildi.")
