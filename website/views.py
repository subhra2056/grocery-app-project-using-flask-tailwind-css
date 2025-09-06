from flask import Blueprint, render_template, flash, redirect, request, jsonify
from .models import product, cart
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

#for payments
API_PUBLISHABLE_KEY = 'ISPubKey_test_8654ea7d-b636-460e-85d6-884d9572f76f'

API_TOKEN = 'ISSecretKey_test_9c99cac1-cea9-4e76-8ce3-b5246a30ab7d'

@views.app_context_processor
def inject_cart():
    if current_user.is_authenticated:
        user_cart = cart.query.filter_by(customer_table_link=current_user.id).all()
    else:
        user_cart = []
    return dict(cart=user_cart)


@views.route('/')
def home():

    items = product.query.filter_by(top_picks = 'Yes').all()
    return render_template('home.html', items = items)

@views.route('/allcategories')
def allcategories():
    return render_template('allcategories.html')


@views.route('/allcategories/<string:category_name>')
def category_page(category_name):

    products = product.query.filter_by(product_category = category_name).all()

    return render_template('displayProductCategorywise.html', products = products, category = category_name)


@views.route('/Add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):

    items_to_add_to_cart = product.query.get(item_id)

    item_exists = cart.query.filter_by(product_table_link = item_id, customer_table_link = current_user.id).first()

    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            flash(f'Added to cart')
            return redirect(request.referrer)
        except Exception:
            flash(f'Failed to add to cart')
            return redirect(request.referrer)
    
    new_cart_item = cart()
    new_cart_item.quantity = 1
    new_cart_item.product_table_link = items_to_add_to_cart.id
    new_cart_item.customer_table_link = current_user.id


    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} added to cart!')

    except Exception:
        flash(f'{new_cart_item.product.product_name} has not been added to cart!')

    return redirect(request.referrer)

@views.route('/Cart')
@login_required
def show_cart():
    Cart = cart.query.filter_by(customer_table_link = current_user.id).all()
    total_cost = 0
    for item in Cart:
        total_cost += item.product.product_price * item.quantity

    return render_template('cart.html', Cart=Cart, total_cost = total_cost, total = total_cost + 500 )


@views.route('/update-cart', methods=['POST'])
@login_required
def update_cart():
    cart_id = request.form.get('cart_id')
    action = request.form.get('action')

    cart_item = cart.query.get(cart_id)

    if not cart_item or cart_item.customer_table_link != current_user.id:
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404

    # Update quantity
    if action == 'plus':
        cart_item.quantity += 1
    elif action == 'minus':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            db.session.delete(cart_item)
    db.session.commit()

    # Recalculate totals
    Cart = cart.query.filter_by(customer_table_link=current_user.id).all()
    total_cost = sum(i.product.product_price * i.quantity for i in Cart)
    delivery_fee = 500
    total = total_cost + delivery_fee

    return jsonify({
        'status': 'success',
        'new_quantity': cart_item.quantity if action == 'plus' or cart_item.quantity > 0 else 0,
        'subtotal': cart_item.product.product_price * cart_item.quantity if cart_item.quantity > 0 else 0,
        'total_cost': total_cost,
        'total': total
    })
