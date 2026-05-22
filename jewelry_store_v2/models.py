from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name     = db.Column(db.String(150), nullable=False)
    phone         = db.Column(db.String(20))
    address       = db.Column(db.Text)
    role          = db.Column(db.Enum('admin', 'customer'), default='customer')
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    orders        = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'


class Category(db.Model):
    __tablename__ = 'categories'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    products    = db.relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    __tablename__ = 'products'
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(200), nullable=False)
    description    = db.Column(db.Text)
    price          = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    category_id    = db.Column(db.Integer, db.ForeignKey('categories.id'))
    material       = db.Column(db.String(100))
    is_featured    = db.Column(db.Boolean, default=False)
    is_active      = db.Column(db.Boolean, default=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    __tablename__ = 'orders'
    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id       = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity         = db.Column(db.Integer, nullable=False, default=1)
    total_amount     = db.Column(db.Numeric(10, 2), nullable=False)
    status           = db.Column(db.Enum('pending','confirmed','shipped','delivered','cancelled'), default='pending')
    shipping_address = db.Column(db.Text, nullable=False)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    product          = db.relationship('Product')