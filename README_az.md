**Son Yenilənmə:** 21 Avqust 2026

# 📺 TV Kanal Redaktoru

> **Çoxmarkalı TV kanal siyahısı redaktoru** — Samsung, LG, Sony, Hisense və daha çoxu üçün tək bir platforma.

[![Canlı Demo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![Lisenziya: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENCE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

---

## 🎯 Bu nə edir?

TV-nizin USB sürücüsünə ötürdüyü kanal siyahısı faylını brauzerinizdə **çəkmə-buraxma** (drag-and-drop) ilə vizual redaktə edib sonra TV-yə yenidən yükləyə bilərsiniz. **Məlumat yalnız emal zamanı müvəqqəti (RAM/Temp) saxlanılır; daimi olaraq yadda saxlanılmır.**

---

## 📺 Dəstəklənən TV Markaları

| Marka | Format | Status |
|-------|--------|-------|
| **Samsung** (E/F/H seriyaları) | `.scm` | ✅ Tam dəstək |
| **Samsung** (J/K/M/Q/R/T – Tizen) | `.zip` (SQLite) | ✅ Tam dəstək |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Tam Dəstək |
| **Sony BRAVIA** | `sdb.xml` | ✅ Tam Dəstək |
| **Hisense** (2017+) | `servicelist.db` | ✅ Tam Dəstək |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Beta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Tezliklə |

## 🛰️ Dəstəklənən Peyklər

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · və digər bütün DVB-S peykləri

---

## ✨ Xüsusiyyətlər

- **🪄 Sehrli Çubuq** — Ümumi / Xəbərlər / İdman şablonlarını tək kliklə tətbiq edin
- **🛠️ Şablon Yaradıcısı** — Öz ideal siyahınızı yaradın və yadda saxlayın
- **📱 Kod vasitəsilə Cihaza Köçürmə** — Televizorun yanındakı mobil telefonunuzdan 8 simvoldan ibarət kodla kanal siyahısını kompüterinizə asanlıqla köçürün
- **🔍 Avtomatik Tezlik Təsdiqi** — Köhnə və ya səhv tezlikləri avtomatik aşkar edir (Türksat)
- **⭐ Sevimlilər & Kilid** — Sevimlilər 1–5 və uşaq kilidini idarə edin
- **🗑️ Kütləvi Əməliyyatlar** — Şifrələnmiş kanalları, radio stansiyalarını və ya seçilmiş elementləri kütləvi şəkildə silin
- **🌙 Qaranlıq/Açıq Tema & 👁️ Rəng Korluğu Rejimi** — Hər kəs üçün əlçatan interfeys
- **🌐 11 Dilli Seçimlər** — Türk / İngilis dili dəstəyi
- **📊 Tam Məxfilik (Cookie-siz Analitika)** — Kukilardan və şəxsi məlumatlardan istifadə etməyən daxili statistika
- **📱 Tam Uyğunluq** — Masaüstü, planşet və mobil cihazlarla uyğun

---

## 🚀 Canlı Demo

Quraşdırma olmadan brauzerinizdə birbaşa istifadə edin:

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
│   ├── js/app.js # Frontend (çəkmə-buraxma, kanal renderləşdirmə, şablonlar)
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

Əgər AI köməkçisi ilə işləyirsinizsə, zəhmət olmasa [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) faylını oxuyun.

---

## 🔌 Tərtibatçı API-dən və AI Agentlərindən İstifadə

Bu layihə yalnız vebsayt deyil; o, həmçinin AI agentləri və tərtibatçıların kod vasitəsilə birbaşa istifadə edə biləcəyi tam funksional **REST API** kimi hazırlanıb.

> 🧑‍💻 **İnkişaf etdiricilər üçün:** İnteraktiv Swagger UI sənədlərini [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs) ünvanında görə bilərsiniz.
> 
> 🤖 **AI agentləri üçün (ChatGPT, Claude və s.):** Sistemin maşın oxunan Plain-Text OpenAPI sxemini bu link vasitəsilə AI-yə təqdim edə bilərsiniz: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### Versiya və Yerləşdirmə Təsdiqi (Versiya yoxlaması)
Render serverinin ən son GitHub komitini yerləşdirib-yerləşdirmədiyini və ya hələ də keşlənib-keşlənmədiyini bir neçə saniyə ərzində yoxlamaq üçün:
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
