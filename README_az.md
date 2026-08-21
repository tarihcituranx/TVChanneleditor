[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Son Yenilənmə:** 21 Avqust 2026

# 📺 TV Kanal Redaktoru

> **Çoxmarkalı TV kanal siyahısı redaktoru** — Samsung, LG, Sony və Hisense TV kanal siyahılarınızı brauzeriniz vasitəsilə redaktə edin.

[![Canlı Demo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![API sənədləri](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Lisenziya: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENCE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ Nə edir?

Bu, brauzerinizdə **çəkmə-buraxma** üsulu ilə televizorunuzun USB yaddaş cihazına ötürdüyü kanal siyahısı faylını vizual şəkildə redaktə etməyə imkan verən açıq mənbəli alətdir. Quraşdırma tələb etmir və brauzeriniz və ya REST API vasitəsilə birbaşa işləyir.

## 👤 Kim İstifadə Edə bilər?

- Kompüterdən Samsung TV kanal siyahısını redaktə etmək istəyənlər
- LG GlobalClone XML `.tll` fayllarını redaktə etmək istəyənlər
- Sony `sdb.xml` və Hisense `servicelist.db` siyahıları ilə işləyənlər
- Kanal siyahısını proqram təminatı ilə dəyişdirmək istəyən inkişaf etdiricilər
- AI agentindən istifadə edərək kanal siyahısını avtomatlaşdırmaq istəyənlər

## 📺 Dəstəklənən Formatlar (Uyğunluq Matrisi)

| Format | Oxu | Dəyişmə | Yenidən yaradın | Qeyd |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | E/F/H Seriyası (Binary) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | J/K/M/Q/R/T Seriyaları (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | BRAVIA Seriyası |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | 2017 və 2021 modelləri |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | Yalnız GlobalClone XML (Binary dəstəklənmir) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | Planlaşdırılır / İnkişaf mərhələsindədir |

> **⚠️ Vacib LG Uyğunluq Qeyd:** LG-nin köhnə nəsil **Binary .tll** faylları dəstəklənmir. Yalnız daha yeni XML-əsaslı (GlobalClone) `.tll` faylları emal edilə bilər. Köhnə fayllar üçün masaüstü *ChanSort* tətbiqindən istifadə etməlisiniz.


## ⚠️ Vacib Məhdudiyyətlər

İstifadə etməzdən əvvəl aşağıdakı texniki məhdudiyyətləri nəzərə alın:
- **LG Binary TLL:** Köhnə nəsil binary `.tll` faylları dəstəklənmir.
- **Panasonic SVL:** Dəstək hazırlıq mərhələsindədir (planlaşdırılır).
- **Yayım tezliyi yoxlaması:** Yalnız Türksat peyk məlumatları üçün aktivdir.
- **Fayl Ölçüsü Məhdudiyyəti:** Yüklənən fayllar maksimum **2 MB** ola bilər.
- **Müvəqqəti Sessiya:** Fayllar daimi saxlanmır; sessiyanın sonunda avtomatik silinirlər.

## 🚀 Sürətli Başlanğıc

1. **TV-dən USB-yə köçürmə:** TV menyusundan (Yayım > Ekspert parametrləri) kanal siyahısını FAT32 formatlı USB diskinə köçürün.
2. **Yükləmə:** USB diskindən faylı vebsayta sürükləyib buraxın.
3. **Düzəliş:** Faylları sürükləməklə sıralayın, lazımsız qeydləri silin və ya 💡 Ağıllı Şablonlardan (Smart Templates) istifadə edin.
4. **Yükləmə:** Düzəliş edilmiş faylı yenidən kompüterinizə yükləyin.
5. **TV-yə quraşdırın:** USB sürücüsünü yenidən TV-yə qoşun və yeni siyahını idxal edin.

## 🛰️ Peyk və tezlik dəstəyi

**DVB-S/S2** kanal siyahıları problemsiz emal edilə bilər. **Avtomatik tezlik yoxlama xüsusiyyəti (köhnə/səhv tezlikləri aşkar etmə) hazırda yalnız Türksat 4A/5B məlumatları üçün aktivdir.** Digər peyklər (Hotbird, Astra və s.) çeşidləmə və redaktə üçün tam dəstəklənir.

---

## 🔌 Tərtibatçı API (REST) necə işləyir?

AI agentləri və tərtibatçılar üçün sadə üç addımlı iş axını mövcuddur. Ətraflı məlumat üçün [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) və ya [OpenAPI Schema](https://tvchanneleditor.onrender.com/api/openapi.txt) keçidlərinə baxın.

**Addım 1: Yükləmə**
```http
POST /upload
Content-Type: multipart/form-data
```
*(Cavabda `session_id` və kanalların JSON siyahısı qaytarılır)*

**2-ci addım: Qurmaq**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... emal olunmuş siyahı ... ]
}
```
*(Faylın yüklənməsi üçün `/download/...` linki qaytarılır)*

**3-cü addım: Yükləmə**
```http
GET /download/{session_id}/{filename}
```
*(Düzəliş edilmiş binary/arxiv fayl yüklənir)*

## 🔐 Məxfilik və Təhlükəsizlik

- Fayl ölçüsü üçün **2 MB** limit mövcuddur.
- **Fayllar serverdə daimi saxlanılmır.** Yüklənmiş fayllar redaktə sessiyası müddətində müvəqqəti server yaddaşında emal olunur; onlar daimi arxivləşdirilmir və sessiya bitdikdə (təxminən 1 saat) avtomatik olaraq tamamilə silinirlər.
- Hesab, üzvlük və ya verilənlər bazası qeydiyyatı yoxdur.
- API-də XML parsitemə əməliyyatları (Billion Laughs hücumlarından qorunmaq üçün) `defusedxml` tərəfindən qorunur.

## 🧪 Test Sistemi (CI)

Layihə **Gediş-dönüşlü (Round-Trip)** test memarlığından istifadə edir.
- Real test fayllarından (fixtures) istifadə edərək, dəyişdirilmiş və ya korlanmış mühərrik kodunun ilkin TV verilənlər bazası strukturlarını korlamadığını təsdiqləyirik.
- Hər `push` və `PR` ilə `tests/test_roundtrip.py` GitHub Actions-da avtomatik işə düşür.

## 🌍 Dil Dəstəyi

İnterfeys və istifadəçi bələdçiləri **11 dildə** mövcuddur: Türk, İngilis, Alman, Rus, İspan, İtalyan, Fransız, ərəb, fars, azərbaycan və portuqal.

## 🏗️ Layihənin Strukturı

```
├── app.py # Flask serveri, API marşrutları və i18n
├── scm_core.py # Samsung SCM mühərriki
├── tizen_core.py # Samsung Tizen SQLite mühərriki
├── lg_core.py # LG XML mühərriki
├── sony_core.py # Sony XML mühərriki
├── hisense_core.py     # Hisense SQLite mühərriki
├── templates/ # Jinja2 HTML interfeysləri (11 dil)
├── static/ # CSS, JS, OpenAPI YAML sxemləri
└── tests/
    ├── test_roundtrip.py  # Bütün mühərriklər üçün round-trip testləri
    └── fixtures/ # Testlər üçün real TV verilənlər bazası nümunələri
```

## 🙏 Təşəkkürlər

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — İlkin ilham mənbəyi
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Çoxmarkalı formatlar üçün tərs mühəndislik istinadı
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Türksat tezliklər bazası

## 📄 Lisenziya

MIT lisenziyası altında açıq mənbə kimi yayımlanıb.
> "Samsung", "LG", "Sony", "Hisense", "Panasonic" və onların loqotipləri müvafiq şirkətlərin qeydiyyatdan keçmiş ticarət nişanlarıdır. Bu, müstəqil, açıq mənbə icma alətidir.
