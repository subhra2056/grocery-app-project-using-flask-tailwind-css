from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(150))
    account_creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    cart_items = db.relationship('cart', backref=db.backref('customer', lazy = True))
    orders = db.relationship('order', backref=db.backref('customer', lazy = True))

    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)
    
    def __str__(self):
        return '<customer %r>' % customer.id
    

class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    In_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000), nullable=False)
    Best_Sellers = db.Column(db.Boolean, default=False)
    Date_added = db.Column(db.DateTime, default=datetime.utcnow)

    carts = db.relationship('cart', backref=db.backref('product', lazy = True))
    orders = db.relationship('order', backref=db.backref('product', lazy = True))


    def __str__(self):
        return '<product %r>' % self.product_name
    

class cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable = False)

    customer_table_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_table_link = db.Column(db.Integer,db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return '<cart %r>' %self.id


class order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)

    customer_table_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_table_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


    def __str__(self):
        return '<order %r>' %self.id

# class category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)
#     description = db.Column(db.String(500))

#     products = db.relationship('product', backref='category', lazy=True)

# class wishlist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     wishlist_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
#     wishlist_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     added_at = db.Column(db.DateTime, default=datetime.utcnow)

#     __table_args__ = (
#     db.UniqueConstraint('customer_id', 'product_id', name='unique_wishlist_item'),
# )
