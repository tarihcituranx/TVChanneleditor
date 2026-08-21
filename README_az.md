[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Son yenilənmə:** 21 avqust 2026

# 📺 TV Kanal Redaktoru

> **Çoxmarkalı TV kanal siyahısı redaktoru** — Samsung, LG, Sony, Hisense və daha çoxu üçün tək bir platforma.

[![Canlı Demo](https://img.shields.io/badge/🌐_Live_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Lisenziya: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENCE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)
[![API sənədləri](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)

---

## 🎯 Bu nə edir?

Brauzerinizdə **çəkmə-buraxma** (drag-and-drop) funksiyası ilə televizorunuzun USB diskə köçürdüyü kanal siyahısı faylını vizual şəkildə redaktə edib sonra onu yenidən televizora yükləyə bilərsiniz. **Məlumat yalnız proses zamanı müvəqqəti (RAM/Temp) saxlanılır; daimi yadda saxlanılmır.**

---

## 📺 Dəstəklənən TV Markaları

| Marka | Format | Status |
|-------|--------|-------|
| **Samsung** (E/F/H seriyaları) | `.scm` | ✅ Tam dəstək |
| **Samsung** (J/K/M/Q/R/T – Tizen) | `.zip` (SQLite) | ✅ Tam dəstək |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Tam Dəstək |
| **Sony BRAVIA** | `sdb.xml` | ✅ Tam Dəstək |
| **Hisense** (2017+) | `servicelist.db` | ✅ Tam dəstək |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Beta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Tezliklə |

## 🛰️ Dəstəklənən Peyklər

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · və digər bütün DVB-S peykları

---

## ✨ Xüsusiyyətlər

- **💡 Ağıllı Şablonlar** — Ümumi / Xəbərlər / İdman şablonlarını tək kliklə tətbiq edin
- **🛠️ Şablon Yaradıcısı** — Öz ideal siyahınızı yaradın və yadda saxlayın
- **📱 Kod vasitəsilə Cihaza Köçürmə** — Televizorun yanındakı mobil telefonunuzdan kanallar siyahısını kompüterinizə 8 simvoldan ibarət kodla asanlıqla köçürün
- **🔍 Avtomatik tezlik yoxlaması** — Köhnə və ya düzgün olmayan tezlikləri (Türksat) avtomatik aşkar edir
- **⭐ Sevimlilər & Kilid** — Sevimlilər 1–5 və uşaq kilidi parametrlərini idarə edin
- **🗑️ Kütləvi Əməliyyatlar** — Şifrələnmiş kanalları, radio stansiyalarını və ya seçilmiş elementləri kütləvi şəkildə silin
- **🌙 Qaranlıq/Açıq Tema & 👁️ Rəng Kökü Modu** — Hər kəs üçün əlçatan interfeys
- **🌐 11 Dili Dəstəkləyir**
- **📊 Tam Məxfilik (Cookie-siz Analitika)** — Kukilərdən və şəxsi məlumatlardan istifadə etməyən daxili statistika
- **📱 Tamamilə adaptiv** — Masaüstü, planşet və mobil cihazlarla uyğun gəlir

---

## 🚀 Canlı nümayiş

Heç bir quraşdırma olmadan brauzerinizdə birbaşa istifadə edin:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Yerli Quraşdırma

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Brauzerinizdə `http://127.0.0.1:5000` ünvanına keçin.

---

## 🏗️ Layihənin Strukturı

```
├── app.py # Flask əsas tətbiqi və təhlükəsizlik başlıqları
├── scm_core.py # Samsung SCM (ikili) mühərriki
├── tizen_core.py # Samsung Tizen SQLite mühərriki
├── lg_core.py # LG GlobalClone XML mühərriki
├── sony_core.py # Sony sdb.xml mühərriki
├── hisense_core.py     # Hisense SQLite mühərriki
├── templates/ # Jinja2 HTML şablonları (11 dil)
├── static/
│   ├── css/style.css   # Tünd/Açıq tema + bütün stillər
│   ├── js/app.js # Frontend (çəkmə-buraxma, kanal renderləmə, şablonlar)
│   └── data/ # frequencies.json, templates.json
```

---

## 🔐 Təhlükəsizlik

- Bütün təhlükəsizlik başlıqları aktivləşdirilib (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- Fayl ölçüsü limiti: 2MB
- Yüklənmiş fayllar emaldan sonra silinir
- Serverdə heç bir kanal məlumatı qeydə alınmır
- Təhlükəsizlik üzrə əlaqə: `tarihcituranx@proton.me`

---

## 🤖 AI Bələdçisi

Əgər AI köməkçisi ilə inkişaf edirsinizsə, zəhmət olmasa [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) faylını oxuyun.

---

## 🔌 Tərtibatçı API-dən və AI Agentlərindən İstifadə

Bu layihə yalnız vebsayt deyil; o, həmçinin AI agentləri və tərtibatçıların kod vasitəsilə birbaşa istifadə edə biləcəyi tam funksional **REST API** kimi hazırlanıb.

> 🧑‍💻 **İnkişaf etdiricilər üçün:** İnteraktiv Swagger UI sənədlərini [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs) ünvanında görə bilərsiniz.
> 
> 🤖 **AI agentləri üçün (ChatGPT, Claude və s.):** Sistemin maşın oxunaqlı Plain-Text OpenAPI sxemini bu link vasitəsilə AI-yə təqdim edə bilərsiniz: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### Versiya və Yerləşdirmə Təsdiqi (Versiya yoxlaması)
Render serverinin ən son GitHub komitini yerləşdirib-yerləşdirmədiyini və ya hələ də keşlənib-keşlənmədiyini dərhal yoxlamaq üçün:
```bash
curl -sS https://tvchanneleditor.onrender.com/api/version
```
```json
{
  "status": "online",
  "version": "1.0.0",
  "commit": "abc1234...",
  "deployed_at": "2026-08-21T19:00:51.123Z"
}
```

---

## 🙏 Təşəkkürlər

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — İlkin ilham mənbəyi
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — SCM və çoxmarkalı formatlar üçün tərs mühəndislik istinadı
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Türksat tezlik təsdiqləmə verilənlər bazası

---

## 📄 Lisenziya

MIT lisenziyası altında açıq mənbə kimi yayımlanıb.

> "Samsung", "LG", "Sony", "Hisense", "Panasonic" və onların loqotipləri müvafiq şirkətlərin qeydiyyatdan keçmiş ticarət nişanlarıdır. Bu, müstəqil, açıq mənbə icması üçün bir alətdir.
