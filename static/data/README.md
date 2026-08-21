# 🌍 TV Channel Editor - Veritabanı ve Şablonlar

Bu klasör, TV Kanal Editörü'nün otomatik frekans doğrulama ve "Akıllı Şablonlar" şablon sistemlerinin verilerini içerir. Gelecekte sisteme yabancı uydular ve kablo yayıncıları eklenebileceği için veriler **Ülke > Uydu/Platform** hiyerarşisiyle tasarlanmıştır.

## 📂 Klasör Yapısı

```text
/static/data/
 └── /TURKIYE/
      └── /TURKSAT/
           ├── frekanslar.json   # Türksat güncel frekans veritabanı
           └── templates.json    # Türksat hazır kanal dizilim şablonları
```

## 🛠️ Dosyalar Nasıl Güncellenir?

### 1. `frekanslar.json`
Bu dosya, kullanıcılar listelerine yeni bir kanal eklediğinde veya mevcut kanalların doğruluğunu kontrol ettiğinde (otomatik frekans doğrulama) arka planda kullanılır.

Basit bir "Anahtar-Değer" (Key-Value) haritasıdır:
```json
{
    "TRT 1 HD": "11958",
    "ATV HD": "12053",
    "NOW HD": "12368"
}
```
* **Güncelleme:** Sadece kanal adını büyük/küçük harf duyarlı olarak yazıp karşısına güncel frekansı (MHz) eklemeniz yeterlidir. Tarayıcı dosyayı anında okur.

### 2. `templates.json`
"Akıllı Şablonlar" özelliğinde ekrana gelen **Hazır Şablonların** listesidir. Kanalların sıralamasını belirler.

```json
{
    "general": [
        "TRT 1 HD", 
        "KANAL D HD", 
        "SHOW HD"
    ],
    "news": [
        "TRT HABER HD", 
        "NTV", 
        "HABERTURK HD"
    ]
}
```
* **Güncelleme:** Şablona yeni bir kanal eklemek için kanalın yayın adını listeye virgülle ekleyin. Sistem listede yazan isimle uyuşan kanalları kullanıcının dosyasından bulup otomatik olarak başa dizer.

## 🚀 Yeni Bir Ülke/Uydu Ekleneceğinde Ne Yapılmalı?
Örneğin, Almanya'daki **Astra 19.2E** uydusunu desteklemek isterseniz:
1. `static/data/GERMANY/ASTRA/` klasörünü oluşturun.
2. İçine Almanya'ya özel `frekanslar.json` ve `templates.json` dosyalarını yukarıdaki formatta yerleştirin.
3. Ön uçta (Frontend) kullanıcının uydu seçebileceği küçük bir liste ekleyip `app.js` içerisindeki `fetch('/static/data/TURKIYE/TURKSAT/...')` yollarını seçime göre dinamikleştirin.
