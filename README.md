# 📺 TV Channel Editor

> **Multi-brand TV kanal listesi düzenleyici** — Samsung, LG, Sony, Hisense ve daha fazlası için tek platform.

[![Canlı Demo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

---

## 🎯 Ne Yapıyor?

TV'nizin USB'ye aktardığı kanal listesi dosyasını tarayıcıda **sürükle-bırak** ile görsel olarak düzenleyip tekrar TV'ye yükleyebilirsiniz. **Hiçbir veri sunucumuzda saklanmaz.**

---

## 📺 Desteklenen TV Markaları

| Marka | Format | Durum |
|-------|--------|-------|
| **Samsung** (E/F/H Serisi) | `.scm` | ✅ Tam Destek |
| **Samsung** (J/K/M/Q/R/T - Tizen) | `.zip` (SQLite) | ✅ Tam Destek |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Tam Destek |
| **Sony BRAVIA** | `sdb.xml` | ✅ Tam Destek |
| **Hisense** (2017+) | `servicelist.db` | ✅ Tam Destek |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Beta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Yakında |

## 🛰️ Desteklenen Uydular

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · ve diğer tüm DVB-S uyduları

---

## ✨ Özellikler

- **🪄 Sihirli Değnek** — Genel / Haber / Spor şablonlarını tek tıkla uygula
- **🛠️ Şablon Oluşturucu** — Kendi ideal listenizi oluşturup kaydedin
- **🔍 Otomatik Frekans Doğrulama** — Eski/yanlış frekansları otomatik tespit eder (Türksat)
- **⭐ Favori & Kilit** — Favori 1-5 ve çocuk kilidi düzenleme
- **🗑️ Toplu İşlemler** — Şifreli kanalları, radyoları veya seçilileri toplu sil
- **🌙 Karanlık/Aydınlık Tema** — Sistem teması veya manuel seçim
- **🌐 İki Dil** — Türkçe / English
- **📱 Tam Responsive** — Masaüstü, tablet ve mobil uyumlu

---

## 🚀 Canlı Kullanım

Hiçbir kurulum yapmadan doğrudan tarayıcıda kullanın:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Yerel Kurulum

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Tarayıcıda `http://127.0.0.1:5000` adresine gidin.

---

## 🏗️ Proje Yapısı

```
├── app.py              # Flask ana uygulama & güvenlik header'ları
├── scm_core.py         # Samsung SCM (binary) motoru
├── tizen_core.py       # Samsung Tizen SQLite motoru
├── lg_core.py          # LG GlobalClone XML motoru
├── sony_core.py        # Sony sdb.xml motoru
├── hisense_core.py     # Hisense SQLite motoru
├── templates/          # Jinja2 HTML şablonları (TR + EN)
├── static/
│   ├── css/style.css   # Dark/Light tema + tüm stiller
│   ├── js/app.js       # Frontend (drag-drop, kanal render, template)
│   └── data/           # frekanslar.json, templates.json
```

---

## 🔐 Güvenlik

- Tüm güvenlik header'ları aktif (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- Dosya boyutu limiti: 2MB
- Yüklenen dosyalar işlendikten sonra silinir
- Hiçbir kanal verisi sunucuda loglanmaz
- Security contact: `tarihcituranx@proton.me`

---

## 🤖 Yapay Zeka Rehberi

AI asistanı ile geliştirme yapıyorsanız [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) dosyasını okutun.

---

## 🔌 Geliştirici API & AI Ajanı Kullanımı (Developer API)

Bu proje yalnızca bir web sitesi değil, aynı zamanda yapay zeka ajanlarının (AI Agents) ve geliştiricilerin doğrudan kodla kullanabileceği bir **REST API** olarak tasarlanmıştır. Projeyi kendi sunucunuza kurduktan sonra veya `tvchanneleditor.onrender.com` üzerinden aşağıdaki API uç noktalarını kullanarak dosyaları otomatize edebilirsiniz:

### 1. Kanal Listesini Oku (Upload)
```bash
curl -X POST -F "file=@channel_list.scm" https://tvchanneleditor.onrender.com/upload
```
**Yanıt (JSON):**
Kanal listesi bozulmadan okunur ve JSON olarak döner.
```json
{
  "brand": "samsung",
  "session_id": "uuid-v4-session-id",
  "channels": [
    { "No": 1, "Name": "TRT 1", "Freq": "11958", "Pol": "V" }
  ]
}
```

### 2. Değiştirilmiş Listeyi İndir (Download)
Düzenlediğiniz veya AI ajanının sıraladığı yeni JSON listesini aynı `session_id` ile sunucuya yollayın ve orijinal dosya uzantısında yeni kanal listenizi ikili (binary) olarak geri alın.
```bash
curl -X POST https://tvchanneleditor.onrender.com/download \
     -H "Content-Type: application/json" \
     -d '{"session_id": "uuid-v4-session-id", "channels": [{"No": 1, "Name": "TRT 1", "Freq": "11958", "Pol": "V"}]}' \
     --output new_channel_list.scm
```

### 3. Rate Limit & API Key (Bypass)
Sistem varsayılan olarak IP başına **50 istek/saat** kotasıyla çalışır (DDoS koruması). Yapay zeka servislerinin (örneğin OpenAI sunucularının) aynı IP üzerinden yüzlerce istek atıp banlanmasını engellemek için, API isteklerinize bir şifre ekleyebilirsiniz:
```bash
curl -H "X-API-Key: YOUR_SECRET_KEY" -F "file=@list.scm" ...
```
Bunun çalışması için sunucunun (veya bilgisayarınızın) çevre değişkenlerine (Environment Variables) yetkili şifreleri eklemeniz gerekir:
```bash
export VALID_API_KEYS="secret-key-1,secret-key-2"
```

> **Not:** Ücretsiz sunucudaki (Render) genel web erişimi saatlik **50 istek** ile sınırlandırılmıştır. Yoğun AI/Bot kullanımı için kendi API şifrenizi tanımlayabilir veya projeyi kendi sunucunuzda çalıştırabilirsiniz.

---

## 🙏 Teşekkürler

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — İlk ilham kaynağı
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — SCM + çoklu marka formatları için tersine mühendislik referansı
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — Türksat frekans doğrulama veritabanı

---

## 📄 Lisans

MIT Lisansı — Ticari amaçla satılamaz.

> "Samsung", "LG", "Sony", "Hisense", "Panasonic" ve logoları ilgili şirketlerin tescilli ticari markalarıdır. Bu bağımsız, açık kaynaklı bir topluluk aracıdır.
