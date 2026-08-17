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

### Çalıştırma
Projeyi bilgisayarınıza indirdikten sonra terminalden şu komutları çalıştırmanız yeterlidir:
```bash
pip install -r requirements.txt
python3 app.py
```

Ardından tarayıcınızda `http://localhost:5000` adresine giderek SCM dosyanızı sürükleyip bırakabilirsiniz. Arka planda güvenilir, modern ve hızlı **Flask** web sunucusu çalışmaktadır.

## Yasal Uyarı
"Samsung" ve Samsung logosu, Samsung Electronics Co., Ltd.'nin tescilli ticari markalarıdır. Bu uygulama tamamen bağımsız, kâr amacı gütmeyen, açık kaynaklı bir topluluk aracıdır ve Samsung ile herhangi bir resmi bağı veya sponsorluğu bulunmamaktadır.
