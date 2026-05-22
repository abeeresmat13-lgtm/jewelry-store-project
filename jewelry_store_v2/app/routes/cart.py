from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# تم التعديل هنا لقراءة الموديلز من الفولدر الجديد
from app.models import db, Product, Order, User
from werkzeug.utils import secure_filename
cart = Blueprint('cart', __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def get_cart():
    return session.get('cart', {})


def save_cart(cart_data):
    session['cart'] = cart_data
    session.modified = True


# ── ROUTE 7: CART (view + add + remove) ───────────────────────
@cart.route('/cart', methods=['GET', 'POST'])
@login_required
def view_cart():
    cart_data = get_cart()

    if request.method == 'POST':
        action     = request.form.get('action')
        product_id = request.form.get('product_id', type=int)

        if action == 'add' and product_id:
            qty = request.form.get('quantity', 1, type=int)
            product = Product.query.get(product_id)
            if product and product.stock_quantity >= qty:
                pid = str(product_id)
                cart_data[pid] = cart_data.get(pid, 0) + qty
                save_cart(cart_data)
                flash(f'"{product.name}" added to cart.', 'success')
            else:
                flash('Not enough stock.', 'error')
            return redirect(request.referrer or url_for('cart.view_cart'))

        elif action == 'remove' and product_id:
            pid = str(product_id)
            if pid in cart_data:
                del cart_data[pid]
                save_cart(cart_data)
                flash('Item removed.', 'info')
            return redirect(url_for('cart.view_cart'))

    items = []
    total = 0
    for pid, qty in list(cart_data.items()):
        product = Product.query.get(int(pid))
        if product:
            subtotal = float(product.price) * qty
            total   += subtotal
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        else:
            if pid in cart_data:
                del cart_data[pid]
            save_cart(cart_data)

    return render_template('cart.html', items=items, total=total)


# ── ROUTE 8: CHECKOUT ─────────────────────────────────────────
@cart.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_data = get_cart()

    if not cart_data:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('cart.view_cart'))

    user = User.query.get(session['user_id'])

    items = []
    total = 0

    for pid, qty in cart_data.items():
        product = Product.query.get(int(pid))
        if product:
            qty = int(qty)
            subtotal = float(product.price) * qty
            total += subtotal
            items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })

    error = None

    if request.method == 'POST':
        address = request.form.get('shipping_address', '').strip()

        if not address:
            error = 'Shipping address is required.'
        elif not items:
            error = 'Cart is empty.'
        else:
            try:
                for item in items:
                    product = item['product']

                    order = Order(
                        user_id=user.id,
                        product_id=product.id,
                        quantity=item['quantity'],
                        total_amount=item['subtotal'],
                        shipping_address=address,
                        status='pending'
                    )

                    db.session.add(order)

                    # update stock safely
                    if product.stock_quantity:
                        product.stock_quantity -= item['quantity']

                db.session.commit()

                session['cart'] = {}
                session.modified = True

                flash('Order placed successfully!', 'success')
                return redirect(url_for('cart.my_orders'))

            except Exception as e:
                db.session.rollback()
                print("CHECKOUT ERROR:", e)
                flash("Checkout failed. Check server logs.", "error")

    return render_template(
        'checkout.html',
        items=items,
        total=total,
        user=user,
        error=error
    )

# ── ROUTE 9: MY ORDERS ────────────────────────────────────────
@cart.route('/my-orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(
        user_id=session['user_id']
    ).order_by(Order.created_at.desc()).all()

    return render_template('my_orders.html', orders=orders)