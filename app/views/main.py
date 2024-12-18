from flask import Blueprint, render_template, request, session
from app.models import Product
from random import sample

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    featured_products = sample(Product.query.filter_by(is_approved=True, is_sold=False).all(), min(4, Product.query.count()))
    return render_template('index.html', featured_products=featured_products)

@bp.route('/store')
def store():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(is_approved=True, is_sold=False).paginate(page=page, per_page=12)
    return render_template('store.html', products=products)

@bp.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

