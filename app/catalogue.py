from flask import Blueprint, redirect, render_template, url_for, request
from app.db import get_db

bp = Blueprint('catalogue', __name__)


@bp.route('/')
def index_redirect():
    return redirect(url_for('catalogue.catalogue'))


@bp.route('/catalogue',  methods=('GET', 'POST'))
def catalogue():
    if request.method == "POST":
        msg=request.form.get("product_id")
        print(msg)
        db = get_db()
        db.execute(
            'INSERT INTO cart(product_id,user_id,quantity)'
            ' VALUES(?,0,1)', (msg,))
        db.commit()
    db = get_db()
    products = db.execute(
        'SELECT id, title, price, discount, category, image'
        ' FROM product'
    ).fetchall()
    carts = db.execute(
        'SELECT product_id FROM cart WHERE user_id = ?', (0,)
    ).fetchall()
    return render_template('catalogue/catalog.html', products=products, carts=carts)


@bp.route('/product')
@bp.route('/product/<int:product_id>', methods=('GET', 'POST'))
def product(product_id=1):
    if request.method == "POST":
        msg=request.form.get("product_id")
        print(msg)
        db = get_db()
        db.execute(
            'INSERT INTO cart(product_id,user_id,quantity)'
            ' VALUES(?,0,?)', (product_id,msg,))
        db.commit()
    db = get_db()
    product = db.execute(
        'SELECT id, title, description, price, discount, category, image'
        ' FROM product WHERE id = ?', (product_id,)
    ).fetchone()
    carts = db.execute(
        'SELECT product_id FROM cart WHERE user_id = ?', (0,)
    ).fetchall()
    if product is None:
        return 'Товар не найден', 404

    return render_template('catalogue/product.html', product=product, carts=carts)