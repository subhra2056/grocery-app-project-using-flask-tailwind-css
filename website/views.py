from flask import Blueprint, render_template
from .models import product

views = Blueprint('views', __name__)


@views.route('/')
def home():

    items = product.query.filter_by(top_picks = 'Yes').all()
    return render_template('home.html', items = items)