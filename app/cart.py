from flask import Blueprint, render_template
from app.db import get_db

bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    """Страница корзины."""
    db = get_db()
    cart_items = db.execute(
        'SELECT p.id, p.title, p.price, c.quantity, p.category, p.image'
        ' FROM cart c'
        ' JOIN product p ON p.id = c.product_id'
    ).fetchall()

    total = sum(item['price'] * item['quantity'] for item in cart_items)
    cart_count = len(cart_items)

    return render_template('cart/cart.html', cart_items=cart_items, total=total, cart_count=cart_count)


@bp.route('/checkout')
def checkout():
    """Страница оформления заказа."""
    db = get_db()
    cart_summary = db.execute(
        'SELECT p.title, c.quantity, p.price*(1-p.discount/100.0) AS subtotal'
        ' FROM cart c'
        ' JOIN product p ON p.id = c.product_id'
    ).fetchall()

    total = sum(item['subtotal'] * item['quantity'] for item in cart_summary)
    cart_count = len(cart_summary)

    return render_template('cart/checkout.html', cart_summary=cart_summary, total=total, cart_count=cart_count)