# TRENDIFY - Professional E-commerce Store

A clean, modern Flask-based online store for fashion, watches, shoes and lifestyle products.

## Features

- Product catalog with gallery images, ratings, discounts
- Shopping cart with quantity controls
- Full checkout flow (Cash on Delivery)
- Order confirmation page
- Admin panel (login / add / edit / delete products)
- Newsletter subscription
- Contact form
- Privacy, Terms & Return Policy pages
- Responsive Bootstrap 5 design

## How to Run

```bash
cd trendify
pip install flask
python app.py
```

Open: http://127.0.0.1:5000

## Admin Login

- **URL:** http://127.0.0.1:5000/admin/login
- **Username:** `admin`
- **Password:** `trendify2026`

## Project Structure

```
trendify/
├── app.py                 # Main application
├── templates/             # HTML templates
├── static/
│   ├── css/style.css      # Custom styles
│   └── images/            # Product images
└── README.md
```

## Permanent Storage

Products and orders are saved in the `data/` folder:
- `data/products.json` — all products (survive restart)
- `data/orders.json` — all orders

When you add/edit/delete a product, it is written to the file immediately.
Server restart will **keep** your products.

## What Was Improved (Professional Upgrades)

1. **Complete Backend**
   - Working admin authentication
   - Add / Edit / Delete products (protected)
   - Proper checkout with order creation
   - Quantity support when adding to cart
   - Full remove from cart option

2. **Rich Product Data**
   - Descriptions, gallery images, ratings, discount %
   - 6 products (shoes, watches, beauty cream)

3. **Consistency**
   - Same phone & email across all pages
   - Newsletter form connected
   - Social icons fixed
   - Professional CSS added

4. **Better UX**
   - Flash messages
   - Empty cart handling
   - Order success with real data
   - Admin mode indicator on homepage

## Next Level Improvements (Optional)

- Use SQLite / PostgreSQL instead of in-memory list
- Image upload instead of path input
- Search & category filters
- User accounts / order history
- WhatsApp order notifications
- Deploy on Railway / Render / VPS

---
Made with ❤️ for Trendify


## Deploy Live (Render - Free)

1. Create account at https://render.com
2. New → Web Service
3. Connect GitHub repo OR upload this folder
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Create Web Service → wait 2-3 minutes
6. Your live URL will be: `https://your-app-name.onrender.com`

Admin: `/admin/login` → admin / trendify2026

**Note:** Free Render plan sleeps after 15 min inactivity. First load may take 30-50 sec.
Products are in `data/products.json`. On free tier, files may reset on redeploy — keep a backup of products.json.
