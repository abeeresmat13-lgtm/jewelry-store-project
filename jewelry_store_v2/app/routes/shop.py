from flask import Blueprint, render_template, request, session
# تم التعديل هنا لقراءة الموديلز من الفولدر الجديد
from app.models import Product, Category

shop = Blueprint('shop', __name__)


# ── ROUTE 4: HOME ─────────────────────────────────────────────
@shop.route('/')
def home():
    featured   = Product.query.filter_by(is_featured=True, is_active=True).limit(6).all()
    categories = Category.query.all()
    return render_template('home.html', featured=featured, categories=categories)


# ── ROUTE 5: SHOP ─────────────────────────────────────────────
@shop.route('/shop')
def shop_page():
    category_id = request.args.get('category', type=int)
    search      = request.args.get('search', '').strip()
    sort        = request.args.get('sort', 'name')
    page        = request.args.get('page', 1, type=int)

    query = Product.query.filter_by(is_active=True)

    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.name.asc())

    products   = query.paginate(page=page, per_page=9)
    categories = Category.query.all()

    return render_template('shop.html',
                           products=products,
                           categories=categories,
                           current_category=category_id,
                           search=search,
                           sort=sort)


# ── ROUTE 6: PRODUCT DETAIL ───────────────────────────────────
@shop.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter_by(
        category_id=product.category_id,
        is_active=True
    ).filter(Product.id != product_id).limit(4).all()

    return render_template('product_detail.html',
                           product=product,
                           related=related)