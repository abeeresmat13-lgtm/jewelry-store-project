from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
# تم التعديل هنا لقراءة الموديلز من الفولدر الجديد
from app.models import db, User, Product, Order, Category
from uuid import uuid4

admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in.', 'error')
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('shop.home'))
        return f(*args, **kwargs)
    return decorated


# ── ROUTE 10: ADMIN DASHBOARD ─────────────────────────────────
@admin.route('/')
@admin_required
def dashboard():
    stats = {
        'total_customers': User.query.filter_by(role='customer').count(),
        'total_products' : Product.query.filter_by(is_active=True).count(),
        'total_orders'   : Order.query.count(),
        'pending_orders' : Order.query.filter_by(status='pending').count(),
        'revenue'        : db.session.query(
                               db.func.sum(Order.total_amount)
                           ).filter(Order.status != 'cancelled').scalar() or 0,
    }
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()
    products      = Product.query.order_by(Product.created_at.desc()).all()
    categories    = Category.query.all()

    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_orders=recent_orders,
                           products=products,
                           categories=categories)


# ── ADMIN: ADD PRODUCT ────────────────────────────────────────


UPLOAD_FOLDER = "app/static/uploads/products"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@admin.route('/product/add', methods=['POST'])
@admin_required
def add_product():
    name     = request.form.get('name', '').strip()
    price    = request.form.get('price', '')
    cat_id   = request.form.get('category_id')
    desc     = request.form.get('description', '').strip()
    stock    = request.form.get('stock_quantity', 0)
    material = request.form.get('material', '').strip()
    featured = 'is_featured' in request.form

    file = request.files.get('image')

    if not name or not price:
        flash('Name and price are required.', 'error')
        return redirect(url_for('admin.dashboard'))

    image_filename = None

    # ✅ SAVE IMAGE PROPERLY
    if file and file.filename:
        ext = file.filename.rsplit('.', 1)[-1].lower()
        image_filename = f"{uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, image_filename)
        file.save(file_path)

    product = Product(
        name           = name,
        description    = desc,
        price          = float(price),
        stock_quantity = int(stock),
        category_id    = int(cat_id) if cat_id else None,
        material       = material,
        is_featured    = featured,
        is_active      = True,
        image          = image_filename   
    )

    db.session.add(product)
    db.session.commit()

    flash(f'Product "{name}" added.', 'success')
    return redirect(url_for('admin.dashboard'))

# ── ADMIN: DELETE PRODUCT ─────────────────────────────────────
@admin.route('/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_active = False
    db.session.commit()
    flash(f'Product "{product.name}" deactivated.', 'info')
    return redirect(url_for('admin.dashboard'))


# ── ADMIN: UPDATE ORDER STATUS ────────────────────────────────
@admin.route('/order/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order(order_id):
    order      = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    valid      = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

    if new_status in valid:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.id} → {new_status}.', 'success')

    return redirect(url_for('admin.dashboard'))