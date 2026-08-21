**Son Güncelleme:** 2026-08-21

# 📺 TV Channel Editor

> **Multi-brand TV kanal listesi düzenleyici** — Samsung, LG, Sony, Hisense ve daha fazlası için tek platform.

[![Canlı Demo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

---

## 🎯 Ne Yapıyor?

TV'nizin USB'ye aktardığı kanal listesi dosyasını tarayıcıda **sürükle-bırak** ile görsel olarak düzenleyip tekrar TV'ye yükleyebilirsiniz. **Veriler sadece işlem sırasında geçici olarak (RAM/Temp) tutulur, kalıcı olarak saklanmaz.**

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
- **📱 Kod ile Cihaza Aktarım** — 8 karakterlik kod ile kanal listesini TV yanındaki cep telefonundan bilgisayara kolayca aktarın
- **🔍 Otomatik Frekans Doğrulama** — Eski/yanlış frekansları otomatik tespit eder (Türksat)
- **⭐ Favori & Kilit** — Favori 1-5 ve çocuk kilidi düzenleme
- **🗑️ Toplu İşlemler** — Şifreli kanalları, radyoları veya seçilileri toplu sil
- **🌙 Karanlık/Aydınlık Tema & 👁️ Renk Körlüğü Modu** — Herkes için erişilebilir arayüz
- **🌐 11 Dil Seçeneği** — Türkçe / English desteği
- **📊 Tam Gizlilik (Çerezsiz Analitik)** — Çerez veya kişisel veri kullanmayan yerleşik istatistik
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
├── templates/          # Jinja2 HTML şablonları (11 Dil)
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

Bu proje yalnızca bir web sitesi değil, aynı zamanda yapay zeka ajanlarının (AI Agents) ve geliştiricilerin doğrudan kodla kullanabileceği tam teşekküllü bir **REST API** olarak tasarlanmıştır.

> 🧑‍💻 **Geliştiriciler İçin:** Etkileşimli Swagger UI dökümantasyonunu [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs) adresinden inceleyebilirsiniz.
> 
> 🤖 **AI Ajanları İçin (ChatGPT, Claude, vb.):** Sistemin makine tarafından okunabilir Saf Metin (Plain-Text) OpenAPI şemasını yapay zekaya şu link üzerinden verebilirsiniz: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)


Bunun çalışması için sunucunun (veya bilgisayarınızın) çevre değişkenlerine (Environment Variables) yetkili şifreleri eklemeniz gerekir:
```bash
export VALID_API_KEYS="secret-key-1,secret-key-2"
```

### 4. Sürüm ve Deploy Doğrulaması (Version Check)
Render sunucusunun güncel Github Commit'ini yayına alıp almadığını veya önbellekte kalıp kalmadığını saniyesinde test etmek için:
```bash
curl -sS https://tvchanneleditor.onrender.com/api/version
```
```json
{
  "status": "online",
  "version": "1.0.0",
  "commit": "97401a5...",
  "deployed_at": "2026-08-18T19:00:51.123Z"
}
```

---

## 🙏 Teşekkürler

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — İlk ilham kaynağı
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — SCM + çoklu marka formatları için tersine mühendislik referansı
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — Türksat frekans doğrulama veritabanı

---

## 📄 Lisans

MIT Lisansı ile açık kaynak olarak sunulmuştur.

> "Samsung", "LG", "Sony", "Hisense", "Panasonic" ve logoları ilgili şirketlerin tescilli ticari markalarıdır. Bu bağımsız, açık kaynaklı bir topluluk aracıdır.
