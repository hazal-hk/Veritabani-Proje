# Akıllı Kütüphane Yönetim Sistemi

Bu proje, Flask (Python) ile geliştirilmiş, bir kütüphane otomasyon sistemidir. JWT tabanlı kimlik doğrulama, otomatik e-posta bildirimleri ve Swagger API dokümantasyonu gibi modern özellikler içermektedir.

## Teknolojiler
- **Backend:** Python, Flask, SQLAlchemy
- **Veritabanı:** MySQL
- **Kimlik Doğrulama:** JSON Web Tokens (JWT)
- **API Test/Dokümantasyon:** Swagger (Flasgger)
- **Diğer:** Flask-Mail, Werkzeug

## Kurulum ve Çalıştırma

1.  **Depoyu klonlayın:**
    ```bash
    git clone [https://github.com/kullanici-adiniz/akilli-kutuphane.git](https://github.com/kullanici-adiniz/akilli-kutuphane.git)
    cd akilli-kutuphane
    ```
2.  **Sanal ortam oluşturun ve aktif edin:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows için: venv\Scripts\activate
    ```
3.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Uygulamayı çalıştırın:**
    ```bash
    flask run
    ```
5.  **API Dokümantasyonu:**
    Uygulama çalışırken [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/) adresini ziyaret edin.
