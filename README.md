# Samsung TV Channel Editor (SCM Editor)

Bu proje, Samsung Smart TV'lerin USB belleğe dışa aktardığı `.scm` uzantılı kanal listesi dosyalarını **sürükle-bırak** mantığıyla tarayıcınız üzerinden görsel olarak düzenlemenizi sağlayan tamamen açık kaynaklı ve bağımsız bir araçtır.

![Ekran Görüntüsü](static/img/samsung_logo.png)

## Özellikler

- **🪄 Sihirli Değnek:** Önceden hazırlanan veya sizin kaydettiğiniz şablonları saniyeler içinde uygular.
- **🛠️ Şablon Oluşturucu (Ekranı İkiye Bölme):** İstemediğiniz kanalları silmekle uğraşmak yerine, sol taraftan beğendiklerinizi sağdaki "Sepet"e atarak yepyeni bir liste oluşturun.
- **💾 Kendi Şablonlarınızı Kaydetme:** Hazırladığınız mükemmel listeyi tarayıcınıza kaydedip aylar sonra bile tek tıkla geri getirin.
- **🗑️ Toplu İşlemler:** Şifreli kanalları ve radyoları tek tıkla silin. Checkbox'ları kullanarak dilediğiniz kanalları çoklu seçip saniyeler içinde uçurun.
- **🔒 Güvenli Orijinal Çıktı:** Uygulama SCM formatını tersine mühendislikle işler ve TV'nin checksum (doğrulama) algoritmasını birebir taklit eder. İndirilen dosya her zaman TV'nizin kabul edeceği formatta ve orijinal isimde olur.

## Kurulum ve Kullanım

### Gereksinimler
- Python 3.x

### 🚀 Geliştirme (Lokalde Çalıştırma)

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/tarihcituranx/TVChanneleditor.git
   cd TVChanneleditor
   ```
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Flask sunucusunu başlatın:
   ```bash
   python3 app.py
   ```
4. Tarayıcınızda `http://127.0.0.1:5000` adresine gidin.

## 🤖 Yapay Zekalar İçin (AI Guide)
Projeyi geliştirmek, hata ayıklamak veya yeni özellikler eklemek üzere bir yapay zeka (Claude, Gemini, ChatGPT vb.) kullanıyorsanız, projeyi AI'a yüklediğinizde öncelikle [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) dosyasını okumasını isteyin. Bu dosya, AI'ların projenin çekirdek SCM mimarisini ve kurallarını anında kavraması için özel olarak hazırlanmıştır.

## 🙏 Referanslar ve Teşekkürler

Bu proje geliştirilirken açık kaynak topluluğunun ve çeşitli platformların sunduğu değerli verilerden faydalanılmıştır:
* **[İltekin / scm-editor](https://github.com/iltekin/scm-editor):** Projenin temelindeki ilk ilham kaynağı ve SCM manipülasyonunun çekirdek mantığı için @iltekin'e sonsuz teşekkürler.
* **SamyGO & ChanSort Topluluğu:** Samsung .SCM dosya yapısının (TransponderDataBase, map-SateD vb.) ve checksum algoritmasının tersine mühendislikle çözülmesindeki büyük katkıları için teşekkürler.
* **[FrekansListesi.com.tr](https://frekanslistesi.com.tr/):** Projemizdeki otomatik frekans doğrulama (Kör/Geçersiz frekansları tespit etme) özelliği için güncel Türksat 4A frekans veritabanı referans alınmıştır. Doğru ve tarafsız yayıncılıkları için teşekkür ederiz.

## 📄 Lisans

Bu proje açık kaynaklıdır ve MIT Lisansı ile sunulmaktadır. Ticari amaçlarla satılamaz. "Samsung" ve logoları Samsung Electronics Co., Ltd. şirketine aittir.

## Yasal Uyarı
"Samsung" ve Samsung logosu, Samsung Electronics Co., Ltd.'nin tescilli ticari markalarıdır. Bu uygulama tamamen bağımsız, kâr amacı gütmeyen, açık kaynaklı bir topluluk aracıdır ve Samsung ile herhangi bir resmi bağı veya sponsorluğu bulunmamaktadır.
