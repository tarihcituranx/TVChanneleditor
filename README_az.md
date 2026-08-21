[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Son yenilənmə:** 21 avqust 2026

# 📺 TV Kanal Redaktoru

> **Çoxmarkalı TV kanal siyahısı redaktoru** — Samsung, LG, Sony və Hisense TV kanal siyahılarınızı brauzeriniz vasitəsilə redaktə edin.

[![Canlı Demo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![API sənədləri](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Lisenziya: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENCE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ Nə edir?

Bu, brauzerinizdə **çəkmə-buraxma** üsulu ilə televizorunuzun USB yaddaşına köçürdüyü kanal siyahısı faylını vizual şəkildə redaktə etməyə imkan verən açıq mənbə alətidir. Quraşdırma tələb etmir və birbaşa brauzeriniz və ya REST API vasitəsilə işləyir.

## 👤 Kim İstifadə Edə bilər?

- Kompüterdən Samsung TV kanal siyahısını redaktə etmək istəyənlər
- LG GlobalClone XML `.tll` fayllarını redaktə etmək istəyənlər
- Sony `sdb.xml` və Hisense `servicelist.db` siyahıları ilə işləyənlər
- Kanal siyahısını proqram təminatı ilə dəyişdirmək istəyən inkişaf etdiricilər
- AI agentlərindən istifadə edərək kanal siyahısının idarə edilməsini avtomatlaşdırmaq istəyənlər

## 📺 Dəstəklənən Formatlar (Uyğunluq Matrisi)

| Format | Oxu | Redaktə | Yenidən yaradın | Qeyd |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | E/F/H Seriyası (Binary) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | J/K/M/Q/R/T Seriyaları (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | BRAVIA Seriyası |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | 2017 və 2021 modelləri |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | Yalnız GlobalClone XML (Binary dəstəklənmir) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | Planlaşdırılır / Hazırlanır |

> **⚠️ Vacib LG Uyğunluq Qeyd:** LG-nin köhnə nəsil **Binary .tll** faylları dəstəklənmir. Yalnız yeni nəsil XML-əsaslı (GlobalClone) `.tll` faylları emal edilə bilər. Köhnə fayllar üçün masaüstü *ChanSort* tətbiqindən istifadə etməlisiniz.


## ⚠️ Vacib Məhdudiyyətlər

İstifadə etməzdən əvvəl aşağıdakı texniki məhdudiyyətləri nəzərə alın:
- **LG Binary TLL:** Köhnə nəsil binary `.tll` faylları dəstəklənmir.
- **Panasonic SVL:** Dəstək hazırlanır (planlaşdırılır).
- **Yayım tezliyinin yoxlanışı:** Yalnız Türksat peyk məlumatları üçün aktivdir.
- **Fayl Ölçüsü Məhdudiyyəti:** Yüklənən fayllar maksimum **2 MB** ola bilər.
- **Müvəqqəti Sessiya:** Fayllar daimi saxlanılmır; sessiyanın sonunda avtomatik olaraq silinirlər.

## 🚀 Sürətli Başlanğıc

1. **TV-dən USB-yə köçürmə:** TV menyusundan (Yayım > Gelişmiş Parametrlər), kanal siyahısını FAT32 formatlı USB diskinə köçürün.
2. **Yükləmə:** Faylı USB sürücüsündən vebsayta sürükləyib buraxın.
3. **Düzəliş:** Sürükləmə və buraxma ilə sıranı dəyişdirin, lazımsız elementləri silin və ya 💡 Ağıllı Şablonlardan istifadə edin.
4. **Yüklə:** Düzəldilmiş faylı yenidən kompüterinizə yükləyin.
5. **TV-yə quraşdırın:** USB sürücüsünü TV-yə yenidən daxil edin və yeni siyahını idxal edin.

## 🛰️ Peyk və Tezlik Dəstəyi

**DVB-S/S2** kanal siyahıları dəstəklənən qurğular (markalar) tərəfindən təqdim oluna bilər. **Avtomatik tezlik yoxlama funksiyası (köhnə/səhv tezlikləri aşkar etmək) hazırda yalnız Türksat 4A/5B məlumatları üçün aktivdir.** Digər peyklər (Hotbird, Astra və s.) çeşidləmə və redaktə üçün tam dəstəklənir.

---

## 🔌 Tərtibatçı API (REST) necə işləyir?

AI agentləri və tərtibatçılar üçün sadə 3 addımlı iş axını mövcuddur. Əlavə məlumat üçün [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) və ya [OpenAPI Schema](https://tvchanneleditor.onrender.com/api/openapi.txt) keçidlərinə baxın.

**Addım 1: Yükləmə**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... sıralanmış siyahı ... ]
}
```
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... redaktə olunmuş siyahı ... ]
}
```
*(Faylın yüklənməsi üçün `/download/...` linki qaytarılır)*

**3-cü addım: Yükləmə**
```http
GET /download/{session_id}/{filename}
```
*(Düzəldilmiş binary/arxiv fayl yüklənir)*

## 🔐 Məxfilik və Təhlükəsizlik

- Fayl ölçüsü üçün **2 MB** həddi var.
- **Fayllar serverdə daimi saxlanılmır.** Yüklənmiş fayllar redaktə sessiyası müddətində müvəqqəti server yaddaşında emal olunur; onlar daimi arxivləşdirilmir və sessiya bitdikdən sonra (təxminən 1 saat) avtomatik olaraq tamamilə silinirlər.
- Hesab, üzvlük və ya verilənlər bazası qeydiyyatı yoxdur.
- API-də XML parsite əməliyyatları (Billion Laughs hücumlarından qorunmaq üçün) `defusedxml` tərəfindən qorunur.

## 🧪 Test Sistemi (CI)

Layihə **Geri Dönüşlü (Round-Trip)** test memarlığından istifadə edir.
- Real test fayllarından (fixtures) istifadə edərək, korlanmış və ya dəyişdirilmiş mühərrik kodunun ilkin TV verilənlər bazası strukturlarını pozmadığını təsdiqləyirik.
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
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Türksat tezlik bazası

## 📄 Lisenziya

MIT lisenziyası altında açıq mənbə kimi yayımlanıb.
> "Samsung", "LG", "Sony", "Hisense", "Panasonic" və onların loqotipləri müvafiq şirkətlərin qeydiyyatdan keçmiş ticarət nişanlarıdır. Bu, müstəqil, açıq mənbə icma alətidir.
