from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Product, db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/approve_product/<int:product_id>', methods=['POST'])
@login_required
def approve_product(product_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.index'))
    
    product = Product.query.get_or_404(product_id)
    product.is_approved = True
    db.session.commit()
    flash('Product approved successfully!', 'success')
    return redirect(url_for('products.dashboard'))

@bp.route('/reject_product/<int:product_id>', methods=['POST'])
@login_required
def reject_product(product_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.index'))
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product rejected and removed.', 'success')
    return redirect(url_for('products.dashboard'))

