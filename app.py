from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'trendify_professional_secret_2026_change_in_production')

# ============================================================
# PRODUCT STORAGE (JSON file - permanent save)
# ============================================================
# Prefer /data when Railway Volume is mounted (survives restarts)
if os.path.isdir('/data'):
    DATA_DIR = '/data'
else:
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')

os.makedirs(DATA_DIR, exist_ok=True)

# Default products (used only on first run when no file exists)
DEFAULT_PRODUCTS = json.loads(r'''
[
  {
    "id": 1,
    "name": "CASUAL SPORT SHOES - FASHION PRINT",
    "brand": "TRENDIFY",
    "price": 1499.0,
    "old_price": 1899.0,
    "image": "/static/images/shoe1.png",
    "gallery_images": [
      "/static/images/shoe1.png",
      "/static/images/shoe3.png"
    ],
    "description": "Stylish white navy beige casual sneakers with artistic print. Soft cushioning, durable sole. Perfect for daily wear.",
    "ratings": 4.8,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 21,
    "in_stock": true
  },
  {
    "id": 2,
    "name": "FLK SPOT BLACK SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1199.0,
    "old_price": 1599.0,
    "image": "/static/images/shoe2.png",
    "gallery_images": [
      "/static/images/shoe2.png"
    ],
    "description": "Lightweight black mesh sports sneakers with reflective stripes. Breathable and comfortable for running and casual use.",
    "ratings": 4.6,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 25,
    "in_stock": true
  },
  {
    "id": 3,
    "name": "WAVE PRINT CASUAL SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1599.0,
    "old_price": 1999.0,
    "image": "/static/images/shoe3.png",
    "gallery_images": [
      "/static/images/shoe3.png",
      "/static/images/shoe1.png"
    ],
    "description": "Premium casual sneakers with Japanese wave art print. Navy white beige design, thick sole for comfort.",
    "ratings": 4.7,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 20,
    "in_stock": true
  },
  {
    "id": 4,
    "name": "BLACK SPORT RUNNERS",
    "brand": "TRENDIFY",
    "price": 1299.0,
    "old_price": 1699.0,
    "image": "/static/images/shoe4.png",
    "gallery_images": [
      "/static/images/shoe4.png"
    ],
    "description": "Breathable mesh black runners with anti-slip sole. Lightweight design for daily walking and light workouts.",
    "ratings": 4.5,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 24,
    "in_stock": true
  },
  {
    "id": 5,
    "name": "BROWN WHITE CLASSIC SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1699.0,
    "old_price": 2199.0,
    "image": "/static/images/shoe5.png",
    "gallery_images": [
      "/static/images/shoe5.png"
    ],
    "description": "Trendy brown and white low-top sneakers. Clean design, comfortable fit for casual and semi-formal looks.",
    "ratings": 4.8,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 23,
    "in_stock": true
  },
  {
    "id": 6,
    "name": "NAVY BLUE SPORT SHOES",
    "brand": "TRENDIFY",
    "price": 1399.0,
    "old_price": 1799.0,
    "image": "/static/images/shoe6.png",
    "gallery_images": [
      "/static/images/shoe6.png"
    ],
    "description": "Navy blue mesh sports shoes with white wave design and orange inner. Durable and stylish for everyday use.",
    "ratings": 4.6,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 22,
    "in_stock": true
  },
  {
    "id": 7,
    "name": "PURE WHITE CLASSIC SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1249.0,
    "old_price": 1599.0,
    "image": "/static/images/shoe7.png",
    "gallery_images": [
      "/static/images/shoe7.png"
    ],
    "description": "Clean all-white classic sneakers. Minimal design that goes with every outfit. Soft sole and easy to clean.",
    "ratings": 4.7,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 22,
    "in_stock": true
  },
  {
    "id": 8,
    "name": "BLACK SLIP-ON SPORTS SHOES",
    "brand": "TRENDIFY",
    "price": 999.0,
    "old_price": 1399.0,
    "image": "/static/images/shoe8.png",
    "gallery_images": [
      "/static/images/shoe8.png"
    ],
    "description": "Comfortable black mesh slip-on shoes. No laces needed. Ideal for quick wear and casual outings.",
    "ratings": 4.4,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 9,
    "name": "BLACK WHITE LOW-TOP SNEAKERS",
    "brand": "TRENDIFY",
    "price": 1549.0,
    "old_price": 1999.0,
    "image": "/static/images/shoe9.png",
    "gallery_images": [
      "/static/images/shoe9.png"
    ],
    "description": "Modern black and white low-top sneakers. Street style look with cushioned sole.",
    "ratings": 4.7,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 23,
    "in_stock": true
  },
  {
    "id": 10,
    "name": "BROWN SPORT RUNNERS",
    "brand": "TRENDIFY",
    "price": 1349.0,
    "old_price": 1749.0,
    "image": "/static/images/shoe10.png",
    "gallery_images": [
      "/static/images/shoe10.png"
    ],
    "description": "Brown mesh sports runners with white sole. Breathable, anti-slip, durable build for daily use.",
    "ratings": 4.5,
    "category": "Shoes",
    "variants": [],
    "discount_percent": 23,
    "in_stock": true
  },
  {
    "id": 11,
    "name": "TRANSPARENT SKELETON WATCH",
    "brand": "TRENDIFY",
    "price": 1899.0,
    "old_price": 2499.0,
    "image": "/static/images/watch.png",
    "gallery_images": [
      "/static/images/watch.png"
    ],
    "description": "Luxury transparent case skeleton watch with black silicone strap. Unique see-through mechanical design.",
    "ratings": 4.9,
    "category": "Watches",
    "variants": [],
    "discount_percent": 24,
    "in_stock": true
  },
  {
    "id": 12,
    "name": "BLACK CHRONOGRAPH WATCH SET",
    "brand": "TRENDIFY",
    "price": 899.0,
    "old_price": 1299.0,
    "image": "/static/images/watch1.png",
    "gallery_images": [
      "/static/images/watch1.png",
      "/static/images/watch6.png"
    ],
    "description": "Premium black chronograph watch with chain bracelet and ring set. Stainless steel finish with date display.",
    "ratings": 4.6,
    "category": "Watches",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 13,
    "name": "BLACK SILICONE CHRONOGRAPH",
    "brand": "TRENDIFY",
    "price": 749.0,
    "old_price": 999.0,
    "image": "/static/images/watch3.png",
    "gallery_images": [
      "/static/images/watch3.png"
    ],
    "description": "Matte black silicone strap chronograph watch. Lightweight, water-resistant style for everyday wear.",
    "ratings": 4.5,
    "category": "Watches",
    "variants": [],
    "discount_percent": 25,
    "in_stock": true
  },
  {
    "id": 14,
    "name": "CLASSIC GOLD TANK WATCH",
    "brand": "TRENDIFY",
    "price": 2199.0,
    "old_price": 2999.0,
    "image": "/static/images/watch4.png",
    "gallery_images": [
      "/static/images/watch4.png"
    ],
    "description": "Elegant gold-tone rectangular tank watch with Roman numerals and black leather strap. Timeless formal look.",
    "ratings": 4.8,
    "category": "Watches",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 15,
    "name": "SMART JUBILE BLACK WATCH",
    "brand": "TRENDIFY",
    "price": 599.0,
    "old_price": 899.0,
    "image": "/static/images/watch5.png",
    "gallery_images": [
      "/static/images/watch5.png"
    ],
    "description": "Sleek black analog watch with crystal markers and brown strap. Simple elegant design for men and women.",
    "ratings": 4.3,
    "category": "Watches",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 16,
    "name": "POSH BLACK WATCH GIFT SET",
    "brand": "TRENDIFY",
    "price": 999.0,
    "old_price": 1499.0,
    "image": "/static/images/watch6.png",
    "gallery_images": [
      "/static/images/watch6.png"
    ],
    "description": "Complete black watch gift set with bracelet and ring. Chronograph dial, premium boxed packaging style.",
    "ratings": 4.7,
    "category": "Watches",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 17,
    "name": "ARABIC DIAL LUXURY WATCH",
    "brand": "TRENDIFY",
    "price": 1799.0,
    "old_price": 2499.0,
    "image": "/static/images/watch7.png",
    "gallery_images": [
      "/static/images/watch7.png"
    ],
    "description": "Modern luxury watch with Arabic numerals. Available style in gold, silver and white marble finishes.",
    "ratings": 4.8,
    "category": "Watches",
    "variants": [],
    "discount_percent": 28,
    "in_stock": true
  },
  {
    "id": 18,
    "name": "PARIS TRACKSUIT SET",
    "brand": "TRENDIFY",
    "price": 1499.0,
    "old_price": 2199.0,
    "image": "/static/images/shirt.png",
    "gallery_images": [
      "/static/images/shirt.png"
    ],
    "description": "Black Paris printed t-shirt and trouser tracksuit set. Comfortable fabric for casual wear and workouts.",
    "ratings": 4.6,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 32,
    "in_stock": true
  },
  {
    "id": 19,
    "name": "CLASSIC LOGO T-SHIRT 3PCS",
    "brand": "TRENDIFY",
    "price": 1299.0,
    "old_price": 1899.0,
    "image": "/static/images/shirt1.png",
    "gallery_images": [
      "/static/images/shirt1.png"
    ],
    "description": "Pack of stylish logo t-shirts in black, white and blue. Soft cotton feel, regular fit.",
    "ratings": 4.5,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 32,
    "in_stock": true
  },
  {
    "id": 20,
    "name": "TEAL LONG SLEEVE T-SHIRT",
    "brand": "TRENDIFY",
    "price": 899.0,
    "old_price": 1299.0,
    "image": "/static/images/shirt3.png",
    "gallery_images": [
      "/static/images/shirt3.png"
    ],
    "description": "Premium teal long sleeve round neck t-shirt. Soft fabric, perfect for casual and layering.",
    "ratings": 4.4,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 21,
    "name": "MONEY HEIST TRACKSUIT SET",
    "brand": "TRENDIFY",
    "price": 1699.0,
    "old_price": 2499.0,
    "image": "/static/images/shirt4.png",
    "gallery_images": [
      "/static/images/shirt4.png"
    ],
    "description": "Money Heist themed black tracksuit set - t-shirt, shorts and joggers. Unique print, comfortable fit.",
    "ratings": 4.7,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 32,
    "in_stock": true
  },
  {
    "id": 22,
    "name": "GREY GEOMETRIC PRINT T-SHIRT",
    "brand": "TRENDIFY",
    "price": 699.0,
    "old_price": 999.0,
    "image": "/static/images/shirt5.png",
    "gallery_images": [
      "/static/images/shirt5.png"
    ],
    "description": "Modern grey t-shirt with geometric black and white print. Casual street style look.",
    "ratings": 4.3,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 23,
    "name": "WHITE FORMAL DRESS SHIRT",
    "brand": "TRENDIFY",
    "price": 1199.0,
    "old_price": 1699.0,
    "image": "/static/images/shirt6.png",
    "gallery_images": [
      "/static/images/shirt6.png"
    ],
    "description": "Classic white formal dress shirt. Crisp collar, office and event ready. Regular fit.",
    "ratings": 4.6,
    "category": "Clothing",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 24,
    "name": "SANDAL BEAUTY CREAM",
    "brand": "SANDAL",
    "price": 360.0,
    "old_price": 450.0,
    "image": "/static/images/sandal.png",
    "gallery_images": [
      "/static/images/sandal.png"
    ],
    "description": "Natural Sandal Beauty Cream for fair soft glowing skin. Enriched with sandalwood extract. All skin types.",
    "ratings": 4.3,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 20,
    "in_stock": true
  },
  {
    "id": 25,
    "name": "FLOKA SILK TOUCH CREAM",
    "brand": "FLOKA",
    "price": 499.0,
    "old_price": 699.0,
    "image": "/static/images/cream.png",
    "gallery_images": [
      "/static/images/cream.png"
    ],
    "description": "Floka Silk Touch body cream with coconut essence. Deep moisturizing formula for soft smooth skin.",
    "ratings": 4.5,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 29,
    "in_stock": true
  },
  {
    "id": 26,
    "name": "KAIYA FLORAL HAND CREAM SET",
    "brand": "KAIYA BEAUTY",
    "price": 599.0,
    "old_price": 899.0,
    "image": "/static/images/cream1.png",
    "gallery_images": [
      "/static/images/cream1.png"
    ],
    "description": "Set of floral scent hand creams - rose, lavender, cherry and more. 30g tubes, nourishing formula.",
    "ratings": 4.6,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 27,
    "name": "HAND & FOOT CARE CREAM",
    "brand": "CHEEK AND CHIN",
    "price": 450.0,
    "old_price": 650.0,
    "image": "/static/images/cream2.png",
    "gallery_images": [
      "/static/images/cream2.png"
    ],
    "description": "Hand and foot care cream for all skin types. Softens rough skin, moisturizes and protects.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 28,
    "name": "NICONI MEN DE-TAN PACK",
    "brand": "NICONI",
    "price": 550.0,
    "old_price": 799.0,
    "image": "/static/images/cream3.png",
    "gallery_images": [
      "/static/images/cream3.png"
    ],
    "description": "Niconi Men Enzyme De-Tan Pack for face and body. Removes tan, brightens skin. 50g jar.",
    "ratings": 4.5,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 29,
    "name": "JOCKEY SHAVING FOAM",
    "brand": "JOCKEY",
    "price": 399.0,
    "old_price": 549.0,
    "image": "/static/images/cream4.png",
    "gallery_images": [
      "/static/images/cream4.png"
    ],
    "description": "Jockey shaving foam for smooth comfortable shave. Rich lather, protects skin from razor burn.",
    "ratings": 4.4,
    "category": "Beauty",
    "variants": [],
    "discount_percent": 27,
    "in_stock": true
  },
  {
    "id": 30,
    "name": "IKT HAIR WAX STICK",
    "brand": "IKT",
    "price": 449.0,
    "old_price": 649.0,
    "image": "/static/images/hair.png",
    "gallery_images": [
      "/static/images/hair.png"
    ],
    "description": "IKT wax stick for flyaways and edge control. 75g, adds texture and hold for neat hairstyles.",
    "ratings": 4.6,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 31,
    "in_stock": true
  },
  {
    "id": 31,
    "name": "SILICONE SHAMPOO BRUSH",
    "brand": "TRENDIFY",
    "price": 299.0,
    "old_price": 449.0,
    "image": "/static/images/hair1.png",
    "gallery_images": [
      "/static/images/hair1.png"
    ],
    "description": "Soft silicone scalp massage shampoo brush. Deep cleans scalp, improves blood circulation.",
    "ratings": 4.5,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 33,
    "in_stock": true
  },
  {
    "id": 32,
    "name": "HAIR OIL APPLICATOR BOTTLE",
    "brand": "TRENDIFY",
    "price": 349.0,
    "old_price": 499.0,
    "image": "/static/images/hair2.png",
    "gallery_images": [
      "/static/images/hair2.png"
    ],
    "description": "Hair oil applicator bottle with comb tip and scalp massager. Easy oiling without mess.",
    "ratings": 4.4,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 33,
    "name": "ROOT TOUCH-UP HAIR STICK",
    "brand": "TRENDIFY",
    "price": 499.0,
    "old_price": 799.0,
    "image": "/static/images/hair3.png",
    "gallery_images": [
      "/static/images/hair3.png"
    ],
    "description": "Instant root touch-up stick for grey coverage. Easy to apply, natural looking temporary color.",
    "ratings": 4.3,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 38,
    "in_stock": true
  },
  {
    "id": 34,
    "name": "DR ALIES BEARD GROWTH OIL",
    "brand": "DR ALIES",
    "price": 699.0,
    "old_price": 999.0,
    "image": "/static/images/oil.png",
    "gallery_images": [
      "/static/images/oil.png"
    ],
    "description": "Dr Alies Professional Beard Growth Oil 30ml. Natural formula, sulfate free, for all skin types.",
    "ratings": 4.7,
    "category": "Hair Care",
    "variants": [],
    "discount_percent": 30,
    "in_stock": true
  },
  {
    "id": 35,
    "name": "SAMSUNG GALAXY A-SERIES PHONE",
    "brand": "SAMSUNG",
    "price": 24999.0,
    "old_price": 29999.0,
    "image": "/static/images/samsung.png",
    "gallery_images": [
      "/static/images/samsung.png"
    ],
    "description": "Samsung Galaxy A-series smartphone. Dual camera, large display, reliable performance for daily use.",
    "ratings": 4.5,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 17,
    "in_stock": true
  },
  {
    "id": 36,
    "name": "SAMSUNG GALAXY S22 ULTRA",
    "brand": "SAMSUNG",
    "price": 189999.0,
    "old_price": 229999.0,
    "image": "/static/images/samsung1.png",
    "gallery_images": [
      "/static/images/samsung1.png"
    ],
    "description": "Samsung Galaxy S22 Ultra flagship. S Pen support, pro camera system, premium design in multiple colors.",
    "ratings": 4.9,
    "category": "Electronics",
    "variants": [],
    "discount_percent": 17,
    "in_stock": true
  }
]
''')


def load_products():
    """Load products from JSON file. Create file with defaults if missing."""
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Use file only if it has a full catalog (not old 6-item file)
                if isinstance(data, list) and len(data) >= 30:
                    return data
        except (json.JSONDecodeError, IOError):
            pass
    # First run, corrupt, or incomplete file → save full defaults
    save_products(DEFAULT_PRODUCTS)
    return [dict(p) for p in DEFAULT_PRODUCTS]


def save_products(products_list):
    """Save products to JSON file so they survive server restart."""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products_list, f, ensure_ascii=False, indent=2)


def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_orders(orders_list):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders_list, f, ensure_ascii=False, indent=2)


# Load into memory at startup
PRODUCTS = load_products()
ORDERS = load_orders()


ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'trendify2026'


def get_product_by_id(product_id):
    for product in PRODUCTS:
        if product['id'] == product_id:
            return product
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Please login as admin first.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================
# STORE ROUTES
# ============================================================

@app.route('/')
def home():
    category = request.args.get('category', '').strip()
    q = request.args.get('q', '').strip().lower()

    filtered = PRODUCTS[:]

    if category and category.lower() != 'all':
        filtered = [p for p in filtered if p.get('category', '').lower() == category.lower()]

    if q:
        filtered = [
            p for p in filtered
            if q in p.get('name', '').lower()
            or q in p.get('description', '').lower()
            or q in p.get('brand', '').lower()
            or q in p.get('category', '').lower()
        ]

    # Unique categories for nav
    categories = sorted(set(p.get('category', 'General') for p in PRODUCTS if p.get('category')))

    return render_template(
        'index.html',
        products=filtered,
        categories=categories,
        active_category=category or 'All',
        search_query=request.args.get('q', '')
    )


@app.route('/search')
def search():
    """Redirect search form to home with query param."""
    q = request.args.get('q', '').strip()
    return redirect(url_for('home', q=q) if q else url_for('home'))


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('home'))
    return render_template('product.html', product=product)


# ============================================================
# CART ROUTES
# ============================================================

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('home'))

    qty = request.args.get('qty', 1, type=int)
    if qty < 1:
        qty = 1

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    str_id = str(product_id)

    if str_id in cart:
        cart[str_id] += qty
    else:
        cart[str_id] = qty

    session.modified = True
    flash(f'{product["name"]} added to cart!', 'success')
    return redirect(url_for('cart'))


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        str_id = str(product_id)
        if str_id in cart:
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
            session.modified = True
            flash('Item updated in cart.', 'info')
    return redirect(url_for('cart'))


@app.route('/delete_from_cart/<int:product_id>')
def delete_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        str_id = str(product_id)
        if str_id in cart:
            del cart[str_id]
            session.modified = True
            flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_session = session.get('cart', {})
    cart_items = []
    total = 0.0

    for str_id, quantity in cart_session.items():
        product = get_product_by_id(int(str_id))
        if product:
            subtotal = product['price'] * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=cart_items, total=total)


# ============================================================
# CHECKOUT & ORDER
# ============================================================

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_session = session.get('cart', {})
    if not cart_session:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))

    cart_items = []
    total = 0.0
    for str_id, quantity in cart_session.items():
        product = get_product_by_id(int(str_id))
        if product:
            subtotal = product['price'] * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    if request.method == 'POST':
        order = {
            'id': len(ORDERS) + 1,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'email': request.form.get('email'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'name': f"{request.form.get('first_name', '')} {request.form.get('last_name', '')}".strip(),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'postal_code': request.form.get('postal_code'),
            'phone': request.form.get('phone'),
            'country': request.form.get('country', 'Pakistan'),
            'payment_method': request.form.get('payment_method', 'Cash on Delivery (COD)'),
            'items': cart_items,
            'subtotal': total,
            'shipping': 199.00,
            'total': total + 199.00,
            'status': 'Processing'
        }
        ORDERS.append(order)
        save_orders(ORDERS)
        session.pop('cart', None)
        session.modified = True

        return render_template(
            'order_success.html',
            name=order['name'],
            payment_method=order['payment_method'],
            total=order['total']
        )

    return render_template('checkout.html', cart_items=cart_items, total=total)


@app.route('/order-success')
def order_success():
    return redirect(url_for('home'))


# ============================================================
# NEWSLETTER
# ============================================================

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email', '').strip()
    if email and '@' in email:
        flash('Thank you! You have successfully subscribed to our newsletter.', 'newsletter')
    else:
        flash('Please enter a valid email address.', 'danger')
    return redirect(request.referrer or url_for('home'))


# ============================================================
# STATIC PAGES
# ============================================================

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you! Your message has been sent. We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/return-policy')
def return_policy():
    return render_template('return_policy.html')


# ============================================================
# ADMIN ROUTES
# ============================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('is_admin'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            flash('Welcome Admin! You are now logged in.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', type=float)
        old_price = request.form.get('old_price', type=float) or None
        image = request.form.get('image', '').strip()
        description = request.form.get('description', '').strip()

        if not name or price is None:
            flash('Name and price are required.', 'danger')
            return redirect(url_for('add_product'))

        new_id = max([p['id'] for p in PRODUCTS], default=0) + 1
        discount = 0
        if old_price and old_price > price:
            discount = int(((old_price - price) / old_price) * 100)

        # Smart image path: accept filename or full path
        if image.startswith('http') or image.startswith('/static/'):
            img_path = image
        elif image.startswith('static/'):
            img_path = '/' + image
        else:
            img_path = f'/static/images/{image}'

        PRODUCTS.append({
            'id': new_id,
            'name': name,
            'brand': 'TRENDIFY',
            'price': price,
            'old_price': old_price,
            'image': img_path,
            'gallery_images': [img_path],
            'description': description or 'Premium quality product from Trendify.',
            'ratings': 4.5,
            'category': request.form.get('category', 'General'),
            'variants': [],
            'discount_percent': discount,
            'in_stock': True,
        })
        save_products(PRODUCTS)
        flash(f'Product "{name}" added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_product.html')


@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        product['name'] = request.form.get('name', product['name']).strip()
        product['price'] = request.form.get('price', type=float) or product['price']
        old_price = request.form.get('old_price', type=float)
        product['old_price'] = old_price if old_price else None
        product['image'] = request.form.get('image', product['image']).strip()
        product['description'] = request.form.get('description', product['description']).strip()

        if product['old_price'] and product['old_price'] > product['price']:
            product['discount_percent'] = int(
                ((product['old_price'] - product['price']) / product['old_price']) * 100
            )
        else:
            product['discount_percent'] = 0

        save_products(PRODUCTS)
        flash(f'Product "{product["name"]}" updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_product.html', product=product)


@app.route('/admin/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    global PRODUCTS
    product = get_product_by_id(product_id)
    if product:
        PRODUCTS = [p for p in PRODUCTS if p['id'] != product_id]
        save_products(PRODUCTS)
        flash(f'Product "{product["name"]}" deleted.', 'info')
    else:
        flash('Product not found!', 'danger')
    return redirect(url_for('home'))



@app.route('/admin/export_products')
@login_required
def export_products():
    """Download products.json backup — save this file on your computer."""
    from flask import Response
    payload = json.dumps(PRODUCTS, ensure_ascii=False, indent=2)
    return Response(
        payload,
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment; filename=products_backup.json'}
    )


@app.route('/admin/import_products', methods=['GET', 'POST'])
@login_required
def import_products():
    """Upload a products_backup.json to restore all products."""
    global PRODUCTS
    if request.method == 'POST':
        f = request.files.get('file')
        if not f or not f.filename:
            flash('Please choose a JSON file.', 'danger')
            return redirect(url_for('import_products'))
        try:
            data = json.load(f.stream)
            if not isinstance(data, list) or len(data) == 0:
                flash('Invalid file: expected a non-empty product list.', 'danger')
                return redirect(url_for('import_products'))
            PRODUCTS = data
            save_products(PRODUCTS)
            flash(f'Restored {len(PRODUCTS)} products successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Import failed: {e}', 'danger')
            return redirect(url_for('import_products'))
    return render_template('import_products.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', host='0.0.0.0', port=port)
