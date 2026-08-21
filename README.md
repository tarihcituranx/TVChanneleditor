[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Son Güncelleme:** 2026-08-21

# 📺 TV Channel Editor

> **Multi-brand TV kanal listesi düzenleyici** — Tarayıcı üzerinden Samsung, LG, Sony, Hisense TV kanal listelerinizi düzenleyin.

[![Canlı Demo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![API Docs](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ Ne İşe Yarar?

TV'nizin USB belleğe aktardığı kanal listesi dosyasını tarayıcınızda **sürükle-bırak** yöntemiyle görsel olarak düzenlemenizi sağlayan, açık kaynaklı bir araçtır. Kurulum gerektirmez, doğrudan tarayıcı veya REST API üzerinden çalışır.

## 👤 Kimler Kullanabilir?

- Samsung TV kanal listesini bilgisayardan düzenlemek isteyenler
- LG GlobalClone XML `.tll` dosyalarını düzenlemek isteyenler
- Sony `sdb.xml` ve Hisense `servicelist.db` listeleriyle çalışanlar
- Kanal listesini programatik olarak değiştirmek isteyen geliştiriciler
- AI agent ile kanal listesi otomasyonu yapmak isteyenler

## 📺 Desteklenen Formatlar (Uyumluluk Matrisi)

| Format | Okuma | Düzenleme | Yeniden oluşturma | Not |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | E/F/H Serisi (Binary) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | J/K/M/Q/R/T Serisi (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | BRAVIA Serisi |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | 2017 ve 2021 Modelleri |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | Sadece GlobalClone XML (Binary desteklenmez) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | Planlandı / Geliştirme aşamasında |

> **⚠️ Önemli LG Uyumluluk Notu:** LG'nin eski nesil **Binary .tll** dosyaları desteklenmemektedir. Sadece yeni nesil XML tabanlı (GlobalClone) `.tll` dosyaları işlenebilir. Eski dosyalar için masaüstü *ChanSort* uygulamasını kullanmanız gerekir.


## ⚠️ Önemli Kısıtlamalar

Kullanmadan önce lütfen aşağıdaki teknik sınırları göz önünde bulundurun:
- **LG Binary TLL:** Eski nesil ikili `.tll` dosyaları desteklenmez.
- **Panasonic SVL:** Destek geliştirme aşamasındadır (Planlandı).
- **Frekans Doğrulama:** Yalnızca Türksat uydu verileri için aktiftir.
- **Dosya Boyutu Sınırı:** Yüklenen dosyalar maksimum **2 MB** olabilir.
- **Geçici Oturum:** Dosyalar kalıcı olarak saklanmaz, oturum bitiminde otomatik silinir.

## 🚀 Hızlı Başlangıç

1. **TV'den USB'ye Aktarın:** TV menüsünden (Yayın > Uzman Ayarları) kanal listesini FAT32 formatlı USB'ye aktarın.
2. **Yükleyin:** USB'deki dosyayı siteye sürükleyip bırakın.
3. **Düzenleyin:** Sürükle-bırak ile sıralayın, gereksizleri silin veya 💡 Akıllı Şablonları kullanın.
4. **İndirin:** Düzenlenmiş dosyayı bilgisayarınıza geri indirin.
5. **TV'ye Yükleyin:** USB'yi tekrar TV'ye takıp yeni listeyi içe aktarın.

## 🛰️ Uydu ve Frekans Desteği

**DVB-S/S2** kanal listeleri format açısından sorunsuz şekilde işlenebilir. **Otomatik frekans doğrulama (Eski/yanlış frekansları tespit etme) özelliği şu anda sadece Türksat 4A/5B verileri için aktiftir.** Diğer uydular (Hotbird, Astra vb.) sıralama ve düzenleme için tamamen desteklenmektedir.

---

## 🔌 Geliştirici API (REST) Nasıl Çalışır?

AI Ajanları ve geliştiriciler için 3 adımlı basit bir akış mevcuttur. Daha fazla detay için [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) veya [OpenAPI Şeması](https://tvchanneleditor.onrender.com/api/openapi.txt) bağlantılarına bakabilirsiniz.

**Adım 1: Yükleme (Upload)**
```http
POST /upload
Content-Type: multipart/form-data
```
*(Yanıt olarak bir `session_id` ve kanalların JSON listesi döner)*

**Adım 2: İnşa Etme (Build)**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... düzenlenmiş liste ... ]
}
```
*(Yanıt olarak dosyanın indirilebileceği `/download/...` linki döner)*

**Adım 3: İndirme (Download)**
```http
GET /download/{session_id}/{filename}
```
*(Düzenlenmiş ikili/arşiv dosyası indirilir)*

## 🔐 Gizlilik ve Güvenlik

- **2 MB** dosya boyutu sınırı vardır.
- **Dosyalar sunucuda kalıcı saklanmaz.** Yüklenen dosyalar düzenleme oturumu boyunca geçici sunucu depolamasında işlenir, kalıcı olarak arşivlenmez ve oturum süresi dolduğunda (yaklaşık 1 saat) otomatik olarak tamamen silinir.
- Herhangi bir hesap, üyelik veya veritabanı loglaması yoktur.
- API üzerinde XML ayrıştırma işlemleri (Billion Laughs saldırılarına karşı) `defusedxml` ile korunmaktadır.

## 🧪 Test Sistemi (CI)

Proje, **Round-Trip (Gidiş-Dönüş)** test mimarisine sahiptir.
- Gerçek dünya test dosyaları (fixtures) kullanılarak, bozulan veya değiştirilen motor kodlarının orijinal TV veritabanı yapılarını bozmadığı test edilir.
- Her `push` ve `PR` işleminde GitHub Actions üzerinde `tests/test_roundtrip.py` otomatik çalışır.

## 🌍 Dil Desteği

Arayüz ve kullanım kılavuzları **11 dilde** mevcuttur: Türkçe, İngilizce, Almanca, Rusça, İspanyolca, İtalyanca, Fransızca, Arapça, Farsça, Azerbaycanca ve Portekizce.

## 🏗️ Proje Yapısı

```
├── app.py              # Flask sunucu, API rotaları ve i18n
├── scm_core.py         # Samsung SCM motoru
├── tizen_core.py       # Samsung Tizen SQLite motoru
├── lg_core.py          # LG XML motoru
├── sony_core.py        # Sony XML motoru
├── hisense_core.py     # Hisense SQLite motoru
├── templates/          # Jinja2 HTML arayüzleri (11 Dil)
├── static/             # CSS, JS, OpenAPI YAML şemaları
└── tests/
    ├── test_roundtrip.py  # Tüm motorlar için gidiş-dönüş testleri
    └── fixtures/          # Testler için gerçek TV veritabanı örnekleri
```

## 🙏 Teşekkürler

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — İlk ilham kaynağı
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Çoklu marka formatları için tersine mühendislik referansı
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — Türksat frekans veritabanı

## 📄 Lisans

MIT Lisansı ile açık kaynak olarak sunulmuştur.
> "Samsung", "LG", "Sony", "Hisense", "Panasonic" ve logoları ilgili şirketlerin tescilli ticari markalarıdır. Bu bağımsız, açık kaynaklı bir topluluk aracıdır.
