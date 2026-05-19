from flask import Blueprint, redirect, render_template, url_for
from app.db import get_db

bp = Blueprint('catalogue', __name__)


@bp.route('/')
def index_redirect():
    return redirect(url_for('catalogue.catalogue'))


@bp.route('/catalogue')
def catalogue():
    """Главная страница с каталогом товаров."""
    db = get_db()
    products = db.execute(
        'SELECT id, title, price, discount, category, image'
        ' FROM product'
    ).fetchall()

    return render_template('catalogue/catalog.html', products=products)


@bp.route('/product')
@bp.route('/product/<int:product_id>')
def product(product_id=1):
    """Страница отдельного товара."""
    db = get_db()
    product = db.execute(
        'SELECT id, title, description, price, discount, category, image'
        ' FROM product WHERE id = ?', (product_id,)
    ).fetchone()

    if product is None:
        return 'Товар не найден', 404

    return render_template('catalogue/product.html', product=product)