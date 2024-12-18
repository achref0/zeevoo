from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..models import User, db, Cart, Order, Product
from ..forms import AccountSettingsForm, UpdatePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
import os

bp = Blueprint('account', __name__)

@bp.route('/account/settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    form = AccountSettingsForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            form.profile_picture.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_picture = filename
        db.session.commit()
        flash('Account settings updated successfully!', 'success')
        return redirect(url_for('account.account_settings'))
    return render_template('account_settings.html', form=form)

@bp.route('/account/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.current_password.data):
            current_user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('account.account_settings'))
        else:
            flash('Current password is incorrect', 'error')
    return render_template('update_password.html', form=form)

@bp.route('/checkout', methods=['POST', 'GET'])
@login_required
def checkout():
    if request.method == 'POST':
        cart = current_user.cart
        if not cart or not cart.items:
            flash('Your cart is empty', 'error')
            return redirect(url_for('main.cart'))

        for item in cart.items:
            order = Order(
                user_id=current_user.id,
                product_id=item.product_id,
                quantity=item.quantity,
                total_price=item.product.price * item.quantity
            )
            db.session.add(order)
            product = item.product
            product.is_sold = True

        db.session.query(CartItem).filter_by(cart_id=cart.id).delete()
        db.session.commit()

        flash('Checkout completed successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('checkout.html')

