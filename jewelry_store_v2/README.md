# 💎 Lumière Jewels — Flask Jewelry Store (v2)

## Tech Stack
- **Backend:** Python 3.11, Flask 3.0
- **Database:** MySQL 8.0
- **Auth:** Session-based (plain forms, no extensions)
- **Docker:** Docker Compose

---

## 🗄️ Database Schema — 4 Tables

```
users       → id, username, email, password_hash, full_name, phone, address, role, is_active
categories  → id, name, description
products    → id, name, description, price, stock_quantity, category_id→categories, material, is_featured, is_active
orders      → id, user_id→users, product_id→products, quantity, total_amount, status, shipping_address
```

---

## 🔗 Routes — 10 Endpoints

| # | Method | Route | File | Description |
|---|--------|-------|------|-------------|
| 1 | GET/POST | `/register` | routes/auth.py | Customer registration |
| 2 | GET/POST | `/login` | routes/auth.py | User login |
| 3 | GET | `/logout` | routes/auth.py | Logout |
| 4 | GET | `/` | routes/shop.py | Home page |
| 5 | GET | `/shop` | routes/shop.py | Product listing & filters |
| 6 | GET | `/product/<id>` | routes/shop.py | Product detail |
| 7 | GET/POST | `/cart` | routes/cart.py | View cart / Add / Remove |
| 8 | GET/POST | `/checkout` | routes/cart.py | Checkout & place order |
| 9 | GET | `/my-orders` | routes/cart.py | Order history |
| 10 | GET | `/admin/` | routes/admin.py | Admin dashboard (products + orders) |

---

## 📁 File Structure

```
jewelry_store/
├── app.py               ← Flask app + blueprint registration + seed
├── models.py            ← 4 SQLAlchemy models
├── routes/
│   ├── auth.py          ← Routes 1, 2, 3
│   ├── shop.py          ← Routes 4, 5, 6
│   ├── cart.py          ← Routes 7, 8, 9
│   └── admin.py         ← Route 10
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── shop.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── my_orders.html
│   └── admin/dashboard.html
├── static/css/style.css
├── static/js/main.js
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🚀 Run with Docker

```bash
docker-compose up --build
```

Open: **http://localhost:5000**

## 👤 Default Admin

| Email | Password |
|-------|----------|
| admin@lumiere.com | admin123 |
