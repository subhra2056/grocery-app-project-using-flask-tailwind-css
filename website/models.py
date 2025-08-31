from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(50), nullable=False)  # fixed
    password_hash = db.Column(db.String(150), nullable=False)
    account_creation_date = db.Column(db.DateTime(), default=datetime.utcnow)

    cart_items = db.relationship('cart', backref=db.backref('customer', lazy=True))
    orders = db.relationship('order', backref=db.backref('customer', lazy=True))

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f'<customer {self.id}>'


class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100),unique=True, nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000),unique=True, nullable=False)
    top_picks = db.Column(db.String(10), default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    carts = db.relationship('cart', backref=db.backref('product', lazy=True))
    orders = db.relationship('order', backref=db.backref('product', lazy=True))

    def __str__(self):
        return f'<product {self.product_name}>'


class cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    customer_table_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_table_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return f'<cart {self.id}>'


class order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)

    customer_table_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_table_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return f'<order {self.id}>'


