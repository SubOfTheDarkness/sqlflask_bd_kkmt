from flask import Blueprint, render_template
from app.db import get_db
bp = Blueprint('cart', __name__)
# ========== КОРЗИНА ==========
@bp.route('/cart')
def cart():
    """Страница корзины."""
    db=get_db()
    cart_items = db.execute(
        'SELECT p.title, c.quantity, p.price, p.discount, p.category, p.image FROM cart c'
        'LEFT JOIN product p ON p.id = c.product_id'
    ).fetchall()
    #     {
    #         'id': 1,
    #         'name': 'Беспроводные наушники Pro',
    #         'price': 2499,
    #         'quantity': 2,
    #         'category': 'Электроника',
    #         'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100'
    #     },
    #     {
    #         'id': 2,
    #         'name': 'Футболка хлопок Premium',
    #         'price': 899,
    #         'quantity': 1,
    #         'category': 'Одежда',
    #         'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=100'
    #     },
    #     {
    #         'id': 3,
    #         'name': 'Python для профессионалов',
    #         'price': 1200,
    #         'quantity': 1,
    #         'category': 'Книги',
    #         'image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=100'
    #     }
    # ]
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    cart_count = len(cart_items)
    
    return render_template('cart/cart.html', cart_items=cart_items, total=total, cart_count=cart_count)


# ========== ОФОРМЛЕНИЕ ЗАКАЗА ==========
@bp.route('/checkout')
def checkout():
    db=get_db()
    """Страница оформления заказа."""
    cart_summary = db.execute(
        'SELECT p.title, c.quantity, p.price*(1-p.discount/100) AS subtotal FROM cart c'
        'LEFT JOIN product p ON p.id = c.product_id'
    ).fetchall()
    # cart_summary = [
    #     {'name': 'Наушники Pro', 'quantity': 2, 'subtotal': 4998},
    #     {'name': 'Футболка', 'quantity': 1, 'subtotal': 899},
    #     {'name': 'Книга Python', 'quantity': 1, 'subtotal': 1200}
    # ]
    
    total = sum(item['subtotal'] * item['quantity'] for item in cart_summary)
    cart_count = len(cart_summary)
    
    return render_template('cart/checkout.html', cart_summary=cart_summary, total=total, cart_count=cart_count)
