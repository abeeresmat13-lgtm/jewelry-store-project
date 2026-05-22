import os
import time
from flask import Flask
from .models import db, User, Category, Product
from werkzeug.utils import secure_filename

def create_app():
    app = Flask(__name__)
    
    # 1. الإعدادات (Configurations)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lumiere-secret-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:root@127.0.0.1:3306/jewelry_store'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['UPLOAD_FOLDER'] = 'static/uploads/products'
    # 2. تهيئة الداتابيز
    db.init_app(app)

    # 3. تسجيل الـ Blueprints (لاحظي النقطة . قبل routes عشان الـ relative import)
    from .routes.auth import auth
    from .routes.shop import shop
    from .routes.cart import cart
    from .routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(shop)
    app.register_blueprint(cart)
    app.register_blueprint(admin)

    # 4. تجهيز الداتابيز وعمل الـ Seeding عند بناء التطبيق
    with app.app_context():
        init_db()

    return app


def seed():
    if not User.query.filter_by(role='admin').first():
        admin_user = User(
            username='admin',
            email='admin@lumiere.com',
            full_name='Lumière Admin',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()

    if not Category.query.first():
        cats = [
            Category(name='Rings', description='Elegant rings'),
            Category(name='Necklaces', description='Stunning necklaces'),
            Category(name='Bracelets', description='Beautiful bracelets'),
            Category(name='Earrings', description='Exquisite earrings'),
        ]
        db.session.add_all(cats)
        db.session.flush()

        products = [
            Product(
                name='Diamond Solitaire Ring',
                price=2999.99,
                stock_quantity=10,
                category_id=cats[0].id,
                material='18K White Gold, Diamond',
                is_featured=True,
                image='diamond_solitaire_ring.jpg'
            ),
            Product(
                name='Rose Gold Twisted Band',
                price=699.99,
                stock_quantity=25,
                category_id=cats[0].id,
                material='14K Rose Gold',
                image='rose_gold_twisted_band.jpg'
            ),
            Product(
                name='Sapphire Halo Ring',
                price=3499.99,
                stock_quantity=6,
                category_id=cats[0].id,
                material='18K Gold, Sapphire',
                is_featured=True,
                image='sapphire_halo_ring.jpg'
            ),
            Product(
                name='Pearl Strand Necklace',
                price=549.99,
                stock_quantity=15,
                category_id=cats[1].id,
                material='Sterling Silver, Pearl',
                is_featured=True,
                image='pearl_strand_necklace.jpg'
            ),
            Product(
                name='Gold Herringbone Chain',
                price=1299.99,
                stock_quantity=8,
                category_id=cats[1].id,
                material='18K Yellow Gold',
                image='gold_herringbone_chain.jpg'
            ),
            Product(
                name='Emerald Pendant',
                price=2199.99,
                stock_quantity=4,
                category_id=cats[1].id,
                material='18K Gold, Emerald',
                is_featured=True,
                image='emerald_pendant.jpg'
            ),
            Product(
                name='Diamond Tennis Bracelet',
                price=4599.99,
                stock_quantity=5,
                category_id=cats[2].id,
                material='14K White Gold, Diamonds',
                is_featured=True,
                image='diamond_tennis_bracelet.jpg'
            ),
            Product(
                name='Gold Bangle Set',
                price=899.99,
                stock_quantity=20,
                category_id=cats[2].id,
                material='18K Yellow Gold',
                image='gold_bangle_set.jpg'
            ),
            Product(
                name='Diamond Stud Earrings',
                price=799.99,
                stock_quantity=30,
                category_id=cats[3].id,
                material='14K White Gold, Diamonds',
                is_featured=True,
                image='diamond_stud_earrings.jpg'
            ),
            Product(
                name='Pearl Drop Earrings',
                price=349.99,
                stock_quantity=18,
                category_id=cats[3].id,
                material='Sterling Silver, Pearl',
                image='pearl_drop_earrings.jpg'
            ),
        ]

        db.session.add_all(products)
        db.session.commit()

def init_db():
    retries = 10
    for i in range(retries):
        try:
            db.create_all()
            seed()
            print('✓ Database ready.')
            return
        except Exception as e:
            print(f'DB not ready yet ({i+1}/{retries}): {e}')
            time.sleep(3)
    print('✗ Could not connect to database.')