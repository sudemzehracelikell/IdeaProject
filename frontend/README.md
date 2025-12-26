# IdeaHub Frontend

Modern ve kullanıcı dostu bir fikir paylaşım platformu frontend uygulaması.

## 🎨 Özellikler

### Tasarım
- ✨ Modern glassmorphism efektleri
- 🌈 Canlı gradyan renk paleti
- 🎭 Smooth animasyonlar ve geçişler
- 📱 Tam responsive tasarım
- 🌙 Dark mode tema

### Kullanıcı Özellikleri
- 👤 Kullanıcı kayıt ve giriş sistemi
- 🔐 4 farklı rol seviyesi (Admin, Takım Lideri, Katılımcı, Hakem)
- 📊 Kişiselleştirilmiş dashboard
- 👥 Profil yönetimi

### Fikir Yönetimi
- 💡 Fikir oluşturma ve düzenleme
- 📂 Kategori ve etiket sistemi
- 📝 Detaylı açıklama ve kısa özet
- 🎯 Durum takibi (Taslak, Yayında, Kapalı)
- 📸 Medya dosyası desteği (planlı)

### Etkileşim
- ⭐ Oylama sistemi
- 💬 Yorum yapma
- 📈 Güncelleme timeline'ı
- 🔍 Gelişmiş arama ve filtreleme

### Takım İşbirliği
- 👥 Takım oluşturma ve yönetimi
- 🤝 Takım üyesi ekleme
- 📋 Takım bazlı fikir yönetimi

## 🚀 Kurulum

### Gereksinimler
- Modern bir web tarayıcı (Chrome, Firefox, Edge)
- Django backend sunucusu (port 8000'de çalışıyor olmalı)

### Adımlar

1. **Backend'i başlatın:**
```bash
cd IdeaHub-Deneme
python manage.py runserver
```

2. **Frontend'i açın:**
- `frontend/index.html` dosyasını tarayıcınızda açın
- VEYA bir local server kullanın:

```bash
cd frontend
# Python ile
python -m http.server 8080

# Node.js ile
npx serve
```

3. **Tarayıcıda açın:**
```
http://localhost:8080
```

## 📁 Dosya Yapısı

```
frontend/
├── index.html          # Ana sayfa (landing page)
├── auth.html           # Giriş/Kayıt sayfası
├── dashboard.html      # Kullanıcı dashboard'u
├── ideas.html          # Fikirler listesi
├── idea-detail.html    # Fikir detay sayfası
├── idea-form.html      # Fikir oluşturma/düzenleme formu
├── teams.html          # Takımlar sayfası
├── profile.html        # Kullanıcı profili
├── styles.css          # Ana CSS dosyası (design system)
├── app.js              # Core uygulama mantığı
├── api.js              # API servis katmanı
└── components.js       # Yeniden kullanılabilir UI bileşenleri
```

## 🎯 Kullanım

### İlk Kullanım

1. **Kayıt Olun:**
   - "Giriş Yap" butonuna tıklayın
   - "Kayıt Olun" linkine tıklayın
   - Bilgilerinizi girin ve rolünüzü seçin

2. **Fikir Ekleyin:**
   - Dashboard'dan "Yeni Fikir Ekle" butonuna tıklayın
   - Formu doldurun
   - "Fikri Yayınla" butonuna tıklayın

3. **Fikirleri Keşfedin:**
   - "Fikirler" sayfasına gidin
   - Filtreleri kullanarak arama yapın
   - Beğendiğiniz fikirlere oy verin ve yorum yapın

### Rol Bazlı Özellikler

**Admin:**
- Tüm fikirleri düzenleyebilir/silebilir
- Kullanıcı yönetimi
- Kategori yönetimi

**Takım Lideri:**
- Takım oluşturabilir
- Takım üyelerini yönetebilir
- Takım fikirlerini düzenleyebilir

**Katılımcı:**
- Fikir oluşturabilir
- Kendi fikirlerini düzenleyebilir
- Yorum yapabilir ve oy verebilir

**Hakem:**
- Tüm fikirleri görüntüleyebilir
- Oy verebilir
- Değerlendirme yapabilir

## 🎨 Tasarım Sistemi

### Renkler
- **Primary:** #6366f1 (İndigo)
- **Secondary:** #ec4899 (Pink)
- **Accent:** #14b8a6 (Teal)
- **Background:** #0a0e27 (Dark Blue)

### Tipografi
- **Headings:** Outfit
- **Body:** Inter

### Efektler
- Glassmorphism kartlar
- Smooth hover animasyonları
- Gradient butonlar
- Floating animasyonlar

## 🔧 API Entegrasyonu

Uygulama, Django backend ile aşağıdaki endpoint'ler üzerinden iletişim kurar:

- `GET/POST /UserApp/users/` - Kullanıcı işlemleri
- `GET/POST /IdeaApp/ideas/` - Fikir işlemleri
- `GET /IdeaApp/categories/` - Kategoriler
- `GET /IdeaApp/tags/` - Etiketler
- `GET/POST /TeamApp/teams/` - Takım işlemleri
- `GET/POST /InteractionApp/ideas/{id}/comments/` - Yorumlar
- `POST /InteractionApp/ideas/{id}/vote/` - Oylama
- `GET/POST /IdeaApp/ideas/{id}/updates/` - Güncellemeler

## 🐛 Sorun Giderme

### Backend bağlantı hatası
- Django sunucusunun çalıştığından emin olun (`python manage.py runserver`)
- CORS ayarlarının doğru yapılandırıldığını kontrol edin
- Tarayıcı konsolunda hata mesajlarını kontrol edin

### Sayfa yüklenmiyor
- Tarayıcı önbelleğini temizleyin
- JavaScript hatalarını kontrol edin (F12 > Console)
- Tüm dosyaların doğru yüklendiğinden emin olun

### Stil sorunları
- `styles.css` dosyasının doğru yüklendiğini kontrol edin
- Tarayıcınızın modern CSS özelliklerini desteklediğinden emin olun

## 📱 Responsive Breakpoints

- **Mobile:** < 768px
- **Tablet:** 768px - 1024px
- **Desktop:** > 1024px

## 🌟 Gelecek Özellikler

- [ ] Gerçek zamanlı bildirimler
- [ ] Medya dosyası yükleme
- [ ] Gelişmiş arama (full-text search)
- [ ] Fikir favorileme
- [ ] Kullanıcı takip sistemi
- [ ] Aktivite feed'i
- [ ] Export/Import özellikleri

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👨‍💻 Geliştirici

IdeaHub Frontend - Modern Fikir Paylaşım Platformu

---

**Not:** Bu uygulama, backend sunucusunun `http://localhost:8000` adresinde çalışıyor olmasını gerektirir. Backend sunucusunu başlatmadan önce frontend'i kullanmaya çalışırsanız, API istekleri başarısız olacaktır.
