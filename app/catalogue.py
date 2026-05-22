from flask import Blueprint, redirect, render_template, url_for, request, jsonify, g, flash
from app.auth import login_required
from app.db import get_db

bp = Blueprint('catalogue', __name__)


@bp.route('/')
def index_redirect():
    return redirect(url_for('catalogue.catalogue'))

@bp.route('/to_cart', methods=['POST'])
def to_cart():
    if g.user is not None:
        data = request.get_json()
        val = data.get('value')
        product_ids = data.get('product_id')
        try:
            db = get_db()
            db.execute(
                'INSERT INTO cart(product_id,user_id,quantity)'
                ' VALUES(?,?,?)', (product_ids,g.user['id'],val))
            db.commit()
            return jsonify({'status': 'success'})

        except Exception as e:
            return jsonify({'status': 'error','message': str(e)})
    else:
        return jsonify({'status': 'error','message': 'Для добавления товара в корзину необходимо войти в аккаунт'})

@bp.route('/catalogue')
def catalogue():
    db = get_db()
    products = db.execute(
        'SELECT id, title, price, discount, category, image'
        ' FROM product'
    ).fetchall()
    if g.user is not None:
        carts = db.execute(
            'SELECT product_id FROM cart WHERE user_id = ?', (g.user['id'],)
        ).fetchall()
    else:
        carts=[{"product_id": None}]
    return render_template('catalogue/catalog.html', products=products, carts=carts)


@bp.route('/product')
@bp.route('/product/<int:product_id>')
def product(product_id=1):
    db = get_db()
    product = db.execute(
        'SELECT id, title, description, price, discount, category, image'
        ' FROM product WHERE id = ?', (product_id,)
    ).fetchone()
    if product is None:
        return 'Товар не найден', 404
    if g.user is not None:
        carts = db.execute(
            'SELECT product_id FROM cart WHERE user_id = ?', (g.user['id'],)
        ).fetchall()
    else:
        carts=[{"product_id": None}]

    return render_template('catalogue/product.html', product=product, carts=carts)