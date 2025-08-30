from flask import Blueprint, render_template, flash, send_from_directory
from flask_login import login_required, current_user
from .forms import shop_item_form
from werkzeug.utils import secure_filename
from .models import product
from . import db

admin = Blueprint('admin', __name__)


@admin.route('/Add-Products', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1:
        form = shop_item_form()
        if form.validate_on_submit():
            product_name = form.product_name.data
            product_price = form.product_price.data
            product_in_stock = form.product_in_stock.data
            product_picture = form.product_picture.data
            best_sellers = form.best_sellers.data

            file_name = secure_filename(product_picture.filename) 

            file_path = f'./media/{file_name}'

            product_picture.save(file_path)

            new_product = product()
            new_product.product_name = product_name
            new_product.product_price = product_price
            new_product.product_in_stock = product_in_stock
            new_product.product_picture = file_path
            new_product.best_sellers = best_sellers

            try:
                db.session.add(new_product)
                db.session.commit()
                flash(f'{product_name} added to store successfully!')
                print('Item has been added')
                return render_template('Add-Products.html', form = form)
            except Exception as e:
                print(e)
                flash('Item not added')

        return render_template('Add-Products.html', form=form)

    return render_template('404.html')


@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/Shop-Items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = product.query.order_by(product.date_added).all()
        return render_template('shopitems.html', items=items)

    return render_template('404.html')
