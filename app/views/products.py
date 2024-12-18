from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..models import Product, Cart, CartItem, db
from ..forms import NewProductForm
import os

bp = Blueprint('products', __name__)

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NewProductForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image=filename,
            seller_id=current_user.id,
            is_approved=False,
            is_sold=False
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Your product has been submitted for approval!', 'success')
        return redirect(url_for('products.dashboard'))

    items_for_sale = Product.query.filter_by(seller_id=current_user.id, is_sold=False).all()
    sold_items = Product.query.filter_by(seller_id=current_user.id, is_sold=True).all()
    items_to_approve = Product.query.filter_by(is_approved=False).all() if current_user.is_admin else []
    return render_template('dashboard.html', form=form, items_for_sale=items_for_sale, sold_items=sold_items, items_to_approve=items_to_approve)

@bp.route('/api/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('productId')
    
    if not product_id:
        return jsonify({"message": "Product ID is required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    cart = current_user.cart
    if not cart:
        cart = Cart(user=current_user)
        db.session.add(cart)

    cart_item = CartItem.query.filter_by(cart=cart, product=product).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart=cart, product=product)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Item added to cart successfully", "cart_count": len(cart.items)}), 200

@bp.route('/api/cart-count')
@login_required
def cart_count():
    cart = current_user.cart
    count = sum(item.quantity for item in cart.items) if cart else 0
    return jsonify({"count": count})

@bp.route('/search')
def search():
    query = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(
        Product.name.ilike(f'%{query}%') | 
        Product.description.ilike(f'%{query}%')
    ).filter_by(is_approved=True, is_sold=False).paginate(page=page, per_page=12)
    return render_template('search_results.html', products=products, query=query)

