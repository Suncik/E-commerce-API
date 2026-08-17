# E-commerce API

Django REST Framework asosida qurilgan kichik e-commerce backend. Service/selector arxitekturasi, JWT autentifikatsiya va race-condition-safe checkout logikasi bilan.

## Arxitektura

Loyiha uchta qatlamga bo'lingan:

- **`core/`** — umumiy fundament: `BaseModel` (UUID PK, soft-delete), `ApplicationError` (markazlashgan xato formati), `IsAdminOrReadOnly` permission
- **`apps/catalog/`** — `Category`, `Product`. Faqat admin (`is_staff`) yozishi mumkin, o'qish barcha login qilgan foydalanuvchilarga ochiq
- **`apps/cart/`** — `Cart`, `CartItem`. Har foydalanuvchida bitta doimiy savat, mahsulot qo'shilganda avtomatik "increment" qiladi (bir xil mahsulot uchun yangi qator yaratmaydi)
- **`apps/orders/`** — `Order`, `OrderItem`. Checkout paytida narx va mahsulot nomi "snapshot" qilinadi — `Product` keyinchalik o'zgarsa yoki o'chirilsa ham, eski buyurtma tarixi o'zgarmaydi
- **`apps/users/`** — JWT autentifikatsiya (register, login, refresh, token blacklist)

Har bir app ichida: `models.py` → ma'lumot, `selectors.py` → o'qish so'rovlari, `services.py` → yozish/biznes qoidalar, `views.py` → HTTP qatlami (ingichka, faqat selector/service'ga uzatadi).

## Hal qilingan asosiy texnik muammolar

- **Race condition (overselling)** — checkout paytida stock `F()` expression orqali atomik kamaytiriladi (`Product.objects.filter(stock__gte=qty).update(stock=F("stock") - qty)`), shuning uchun ikki mijoz bir vaqtda oxirgi mahsulotni sotib olishga urinsa, faqat bittasi muvaffaqiyatli bo'ladi
- **Snapshot printsipi** — `OrderItem.product_name` va `OrderItem.price_at_purchase` checkout paytida `Product`dan nusxa olinadi, shuning uchun keyingi narx o'zgarishlari eski buyurtmalarga ta'sir qilmaydi
- **Atomik tranzaksiya** — `checkout_cart()` butunlay `@transaction.atomic` ichida, agar istalgan qadamda xato chiqsa (masalan stock yetarli emas), barcha oldingi o'zgarishlar avtomatik bekor qilinadi
- **N+1 query oldini olish** — `select_related`/`prefetch_related` ForeignKey bog'lanishlarni bitta so'rovda yig'ish uchun ishlatilgan

## O'rnatish

```bash
git clone <repo_url>
cd ecommerce_api
python -m venv venv
venv\Scripts\activate          # Windows
# yoki: source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoint'lar

### Auth
| Method | URL | Tavsif |
|---|---|---|
| POST | `/api/v1/auth/register/` | Ro'yxatdan o'tish |
| POST | `/api/v1/auth/login/` | Login (access + refresh token) |
| POST | `/api/v1/auth/refresh/` | Access tokenni yangilash |

### Catalog
| Method | URL | Ruxsat |
|---|---|---|
| GET | `/api/v1/products/` | Login qilgan har qanday foydalanuvchi |
| POST | `/api/v1/products/` | Faqat admin |
| GET | `/api/v1/products/<uuid:pk>/` | Login qilgan har qanday foydalanuvchi |
| PATCH/PUT | `/api/v1/products/<uuid:pk>/` | Faqat admin |
| DELETE | `/api/v1/products/<uuid:pk>/` | Faqat admin |

### Cart
| Method | URL | Tavsif |
|---|---|---|
| GET | `/api/v1/cart/` | O'z savatini ko'rish |
| POST | `/api/v1/cart/add/` | Mahsulot qo'shish (`product_id`, `quantity`) |
| DELETE | `/api/v1/cart/remove/<uuid:product_id>/` | Mahsulotni savatdan olib tashlash |

### Orders
| Method | URL | Tavsif |
|---|---|---|
| GET | `/api/v1/orders/` | O'z buyurtmalari ro'yxati |
| GET | `/api/v1/orders/<uuid:order_id>/` | Bitta buyurtma tafsiloti |
| POST | `/api/v1/orders/checkout/` | Savatni buyurtmaga aylantirish |
| POST | `/api/v1/orders/<uuid:order_id>/cancel/` | Buyurtmani bekor qilish |

Barcha endpoint'lar (register/login'dan tashqari) `Authorization: Bearer <access_token>` header talab qiladi.

## Testlarni ishga tushirish

```bash
pytest -v
```

15 ta test: `catalog` (permission va CRUD), `cart` (increment logikasi, stock tekshiruvi), `orders` (checkout, snapshot, transaction atomicity).

## Kelajakdagi rejalar

- Docker/docker-compose
- Swagger/OpenAPI (drf-spectacular)
- Celery orqali asinxron email/notification
- Return/refund workflow