# FoodMate

FoodMate, Django Rest Framework ve Python kullanılarak geliştirilen bir yemek tarifleri web uygulamasıdır. Uygulama, kullanıcıların tarifler oluşturmasına, alışveriş sepeti oluşturarak tarif malzemelerini eklemesine ve manuel olarak alışveriş listesine ürünler eklemesine olanak tanır.

## Özellikler

•⁠  ⁠*Kullanıcı Kayıt ve Giriş:*
  - Kullanıcılar sisteme kayıt olabilir ve giriş yapabilir.
  
•⁠  ⁠*Tarifler:*
  - Kullanıcılar mevcut tarifleri görüntüleyebilir.
  - Kendi tariflerini ekleyebilir ve paylaşabilirler.
  
•⁠  ⁠*Alışveriş Sepeti:*
  - Tariflerdeki malzemeler otomatik olarak alışveriş sepetine eklenebilir.
  - Kullanıcılar alışveriş listesine manuel olarak ürün ekleyebilir.

## Kurulum

1.⁠ ⁠*Depoyu klonlayın:*

   ```bash
   git clone https://github.com/kullaniciadiniz/foodmate.git
   cd foodmate

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
