# Yapılacaklar Listesi (TODO)

## Tersine Mühendislik & İleri Seviye (V2.0)
- [ ] **Sony Base64 AES Şifre Çözümü:** 
  - Yeni nesil Sony Bravia TV'lerin `sdb.xml` dosyalarındaki `<BinaryData>` AES şifreli bloklarını çözmek.
  - ChanSort'un açık kaynak kodlarından (GitHub) Sony AES anahtarını (Key) ve block-cipher yapısını inceleyip Python'a uyarlamak.
  - Sadece okunabilir değil, **yazılabilir (re-encrypt)** hale getirmek.

## Diğer Bekleyen İşler
- [ ] Kullanıcı deneyimi (UX) testlerinin yapılması ve mobil tasarımlarda olası ince ayarlar.

- [x] **API Geliştirmeleri (V1.5):** Sitedeki zeki fonksiyonların (Radyoları sil, Büyük harf yap, Şablon uygula vb.) bağımsız stateless API uç noktaları (Tools & Actions) olarak dış kullanıma açılması. (Tamamlandı)
