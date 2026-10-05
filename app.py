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
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')

os.makedirs(DATA_DIR, exist_ok=True)

# Default products (used only on first run when no file exists)
DEFAULT_PRODUCTS = [
    {
        'id': 1,
        'name': 'WALKEND SNEAKERS FOR MEN',
        'brand': 'TRENDIFY',
        'price': 1213.00,
        'old_price': 1500.00,
        'image': '/static/images/shoe2.png',
        'gallery_images': [
            '/static/images/shoe2.png',
            '/static/images/shoe1.png',
        ],
        'description': 'Premium lightweight sneakers designed for everyday comfort and style. Features breathable mesh upper, cushioned sole, and modern street-ready look. Perfect for casual wear, walking, and light sports.',
        'ratings': 4.7,
        'category': 'Shoes',
        'variants': [],
        'discount_percent': 19,
        'in_stock': True,
    },
    {
        'id': 2,
        'name': 'FASHIONABLE 4PCS MEN QUARTZ WATCH SET',
        'brand': 'TRENDIFY',
        'price': 280.00,
        'old_price': 350.00,
        'image': '/static/images/watch1.png',
        'gallery_images': [
            '/static/images/watch1.png',
            '/static/images/watch3.png',
            '/static/images/watch4.png',
        ],
        'description': 'Complete premium men\'s accessories set including a stylish quartz chronograph watch, chain bracelet, and ring. Black stainless steel finish with date display. Perfect gift set for any occasion.',
        'ratings': 4.5,
        'category': 'Watches',
        'variants': [],
        'discount_percent': 20,
        'in_stock': True,
    },
    {
        'id': 3,
        'name': 'CASUAL SPORT SHOES',
        'brand': 'TRENDIFY',
        'price': 1500.00,
        'old_price': 1800.00,
        'image': '/static/images/shoe1.png',
        'gallery_images': [
            '/static/images/shoe1.png',
            '/static/images/shoe2.png',
        ],
        'description': 'High-quality casual sport shoes with stylish white, navy and grey color combination. Soft cushioning, durable sole, and fashion-forward design. Ideal for daily wear and light activities.',
        'ratings': 4.8,
        'category': 'Shoes',
        'variants': [],
        'discount_percent': 17,
        'in_stock': True,
    },
    {
        'id': 4,
        'name': 'SANDAL BEAUTY CREAM',
        'brand': 'SANDAL',
        'price': 360.00,
        'old_price': 450.00,
        'image': '/static/images/sandal.png',
        'gallery_images': [
            '/static/images/sandal.png',
        ],
        'description': 'Natural Sandal Beauty Cream for fair, soft and glowing skin. Enriched with sandalwood extract. Helps reduce dullness and keeps skin moisturized. Suitable for all skin types.',
        'ratings': 4.3,
        'category': 'Beauty',
        'variants': [],
        'discount_percent': 20,
        'in_stock': True,
    },
    {
        'id': 5,
        'name': 'TRANSPARENT SKELETON WATCH',
        'brand': 'TRENDIFY',
        'price': 1899.00,
        'old_price': 2499.00,
        'image': '/static/images/watch.png',
        'gallery_images': [
            '/static/images/watch.png',
            '/static/images/watch3.png',
        ],
        'description': 'Luxury transparent case skeleton automatic-style watch with black silicone strap. Unique see-through design showcasing intricate mechanical details. Statement piece for modern men.',
        'ratings': 4.9,
        'category': 'Watches',
        'variants': [],
        'discount_percent': 24,
        'in_stock': True,
    },
    {
        'id': 6,
        'name': 'CLASSIC GOLD TANK WATCH',
        'brand': 'TRENDIFY',
        'price': 2200.00,
        'old_price': 2999.00,
        'image': '/static/images/watch4.png',
        'gallery_images': [
            '/static/images/watch4.png',
        ],
        'description': 'Elegant rectangular gold-tone tank watch with black Roman numeral dial and genuine leather strap. Timeless classic design perfect for formal occasions and daily sophistication.',
        'ratings': 4.6,
        'category': 'Watches',
        'variants': [],
        'discount_percent': 27,
        'in_stock': True,
    },
]

def load_products():
    """Load products from JSON file. Create file with defaults if missing."""
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except (json.JSONDecodeError, IOError):
            pass
    # First run or corrupt file → save defaults
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', host='0.0.0.0', port=port)
