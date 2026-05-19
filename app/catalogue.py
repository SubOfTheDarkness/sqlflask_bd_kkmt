from flask import Blueprint, redirect, render_template, url_for
from app.db import get_db
bp = Blueprint('catalogue', __name__)


# ========== ГЛАВНАЯ — КАТАЛОГ ==========
@bp.route('/')
def index_redirect():
    return redirect(url_for('catalogue.catalogue'))
@bp.route('/catalogue')
def catalogue():
    """Главная страница с каталогом товаров."""
    db=get_db()
    products = db.execute(
        'SELECT p.id, title, price, discount, category, image'
        ' FROM product p'
    ).fetchall()
    #     {
    #         'id': 1,
    #         'name': 'Беспроводные наушники Pro',
    #         'price': 2499,
    #         'old_price': 3120,
    #         'discount': 20,
    #         'category': 'Электроника',
    #         'rating': 4.5,
    #         'reviews': 128,
    #         'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
    #     },
    #     {
    #         'id': 2,
    #         'name': 'Футболка хлопок Premium',
    #         'price': 899,
    #         'old_price': None,
    #         'discount': None,
    #         'category': 'Одежда',
    #         'rating': 5,
    #         'reviews': 89,
    #         'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'
    #     },
    #     {
    #         'id': 3,
    #         'name': 'Python для профессионалов',
    #         'price': 1200,
    #         'old_price': None,
    #         'discount': None,
    #         'category': 'Книги',
    #         'rating': 4,
    #         'reviews': 256,
    #         'image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400'
    #     },
    #     {
    #         'id': 4,
    #         'name': 'Рюкзак городской Urban',
    #         'price': 3100,
    #         'old_price': 3650,
    #         'discount': 15,
    #         'category': 'Аксессуары',
    #         'rating': 4,
    #         'reviews': 73,
    #         'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'
    #     },
    
    return render_template('catalogue/catalog.html', products=products)


# ========== КАРТОЧКА ТОВАРА ==========
@bp.route('/product')
@bp.route('/product/<int:product_id>')
def product(product_id=1):
    """Страница отдельного товара."""
    db=get_db()
    product_data = db.execute(
        'SELECT p.id, title, description, price, discount, category, image'
        ' FROM product p WHERE p,id = ?', (product_id,)
    ).fetchone()
    # {
    #     'id': product_id,
    #     'name': 'Беспроводные наушники Pro',
    #     'price': 2499,
    #     'old_price': 3120,
    #     'category': 'Электроника',
    #     'rating': 4.5,
    #     'reviews': 128,
    #     'stock': 15,
    #     'description': 'Премиальные беспроводные наушники с активным шумоподавлением. До 30 часов автономной работы.',
    #     'features': ['Bluetooth 5.3', '30 часов работы', 'Шумоподавление ANC', 'Защита IPX5'],
    #     'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600',
    #     'gallery': [ 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100',
    #     'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=100',
    #     'https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?w=100'],
    #     'discount': 20,
    # }
    return render_template('catalogue/product.html', product=product_data)




