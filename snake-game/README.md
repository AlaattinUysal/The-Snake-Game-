# 🐍 The Snake Game

> Modern Python tabanlı yılan oyunu. Özel güçler, dinamik zorluk seviyesi ve modern arayüz ile klasik oyunu yeniden yorumluyor. 🎮✨

Modern ve eğlenceli bir yılan oyunu uygulaması. Klasik yılan oyununun ötesine geçen özellikler ve modern bir arayüz ile yeniden tasarlandı.

![Game Preview](preview.png)

## ✨ Özellikler

- 🎮 Sezgisel kontroller (WASD ve Ok tuşları desteği)
- 🎯 Farklı türde yiyecekler ve özel güçler
- 🏆 Yüksek skor sistemi
- 🎨 Modern ve şık arayüz
- 🎵 Ses efektleri
- 🎯 Dinamik zorluk seviyesi
- 🍎 Altın elma ile duvar geçişi özelliği
- 🎮 Duraklatma ve menü sistemi
- 📊 Detaylı skor tablosu

## 🎮 Kontroller

- **Hareket:**
  - W veya ↑ (Yukarı)
  - S veya ↓ (Aşağı)
  - A veya ← (Sol)
  - D veya → (Sağ)
- **Diğer Kontroller:**
  - ESC: Menüye dön
  - P: Oyunu duraklat/devam ettir
  - SPACE: Oyun bittiğinde yeniden başlat

## 🚀 Kurulum

1. Python 3.x sürümünün yüklü olduğundan emin olun
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Oyunu başlatın:
   ```bash
   python src/main.py
   ```

## 📁 Proje Yapısı

```
snake-game/
├── src/
│   ├── main.py           # Ana oyun döngüsü ve mantığı
│   ├── snake.py          # Yılan sınıfı ve hareket mantığı
│   ├── food.py           # Yiyecek sistemi ve özel güçler
│   ├── scoreboard.py     # Skor sistemi ve yüksek skorlar
│   ├── obstacles.py      # Engel sistemi
│   ├── boundary.py       # Oyun sınırları
│   └── menu.py          # Menü sistemi
├── sounds/
│   └── eat_apple.mp3    # Yemek yeme sesi
├── requirements.txt      # Proje bağımlılıkları
└── README.md            # Bu dosya
```

## 🎯 Oyun Özellikleri Detayları

### Yiyecek Sistemi
- 🍎 Normal Elma: 1 puan
- 🍇 Özel Yiyecekler: Farklı puanlar ve etkiler
- 🍎 Altın Elma: Duvar geçişi özelliği kazandırır

### Zorluk Sistemi
- Her 10 puanda bir oyun alanı küçülür
- Engeller dinamik olarak eklenir
- Duvar geçişi özelliği sınırlı süreyle aktif

### Skor Sistemi
- Anlık skor takibi
- Yüksek skor kaydı
- Detaylı skor tablosu

## 🛠️ Geliştirme

### Gereksinimler
- Python 3.x
- Pygame kütüphanesi

### Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Açıklama'`)
4. Dalınıza push yapın (`git push origin yeni-ozellik`)
5. Bir Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## 👏 Teşekkürler

- Pygame topluluğu
- Tüm katkıda bulunanlar
- Oyunu test eden ve geri bildirim sağlayan herkese

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 