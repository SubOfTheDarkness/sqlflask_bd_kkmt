from flask import Blueprint, render_template

cart_bp = Blueprint('cart', __name__)
# ========== КОРЗИНА ==========
@cart_bp.route('/cart')
def cart():
    """Страница корзины."""
    cart_items = [
        {
            'id': 1,
            'name': 'Беспроводные наушники Pro',
            'price': 2499,
            'quantity': 2,
            'category': 'Электроника',
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100'
        },
        {
            'id': 2,
            'name': 'Футболка хлопок Premium',
            'price': 899,
            'quantity': 1,
            'category': 'Одежда',
            'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=100'
        },
        {
            'id': 3,
            'name': 'Python для профессионалов',
            'price': 1200,
            'quantity': 1,
            'category': 'Книги',
            'image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=100'
        }
    ]
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    cart_count = len(cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total, cart_count=cart_count)


# ========== ОФОРМЛЕНИЕ ЗАКАЗА ==========
@cart_bp.route('/checkout')
def checkout():
    """Страница оформления заказа."""
    cart_summary = [
        {'name': 'Наушники Pro', 'quantity': 2, 'subtotal': 4998},
        {'name': 'Футболка', 'quantity': 1, 'subtotal': 899},
        {'name': 'Книга Python', 'quantity': 1, 'subtotal': 1200}
    ]
    
    total = 7097
    cart_count = 3
    
    return render_template('checkout.html', cart_summary=cart_summary, total=total, cart_count=cart_count)
