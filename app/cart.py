from flask import Blueprint, render_template, request, jsonify, g
from app.db import get_db

from app.auth import login_required

bp = Blueprint('cart', __name__)

@bp.route('/update_count', methods=['POST'])
def update_count():
    data = request.get_json()
    val = data.get('value')
    item_ids = data.get('item_id')
    try:
        db = get_db()
        db.execute(
            'UPDATE cart'
            ' SET quantity=?'
            ' WHERE id=?', (val,item_ids))
        db.commit()
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error','message': str(e)})

@bp.route('/delete_product', methods=['POST'])
def delete_product():
    data = request.get_json()
    item_ids = data.get('item_id')
    try:
        db = get_db()
        db.execute(
            'DELETE FROM cart'
            ' WHERE id=?', (int(item_ids),))
        db.commit()
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error','message': str(e)})


@bp.route('/cart')
@login_required
def cart():
    """Страница корзины."""
    db = get_db()
    cart_items = db.execute(
        'SELECT c.id AS item_id,c.product_id, p.title, p.price*(1-p.discount/100.0) AS price, c.quantity, p.category, p.image'
        ' FROM cart c'
        ' JOIN product p ON p.id = c.product_id'
        ' WHERE c.user_id=?', (g.user['id'],)
    ).fetchall()
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    cart_count = len(cart_items)

    return render_template('cart/cart.html', cart_items=cart_items, total=total, cart_count=cart_count)


@bp.route('/checkout')
@login_required
def checkout():
    """Страница оформления заказа."""
    db = get_db()
    cart_summary = db.execute(
        'SELECT p.id,p.title, c.quantity, p.price*(1-p.discount/100.0) AS subtotal'
        ' FROM cart c'
        ' JOIN product p ON p.id = c.product_id'
        ' WHERE c.user_id=?', (g.user['id'],)
    ).fetchall()
    total = sum(item['subtotal'] * item['quantity'] for item in cart_summary)
    cart_count = len(cart_summary)

    return render_template('cart/checkout.html', cart_summary=cart_summary, total=total, cart_count=cart_count)