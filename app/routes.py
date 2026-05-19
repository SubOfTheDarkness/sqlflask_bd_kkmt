from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


# ========== ГЛАВНАЯ — КАТАЛОГ ==========
@main_bp.route('/')
@main_bp.route('/catalog')
def catalog():
    """Главная страница с каталогом товаров."""
    # Пока статические данные, позже — из базы
    products = [
        {
            'id': 1,
            'name': 'Беспроводные наушники Pro',
            'price': 2499,
            'old_price': 3120,
            'discount': 20,
            'category': 'Электроника',
            'rating': 4.5,
            'reviews': 128,
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
        },
        {
            'id': 2,
            'name': 'Футболка хлопок Premium',
            'price': 899,
            'old_price': None,
            'discount': None,
            'category': 'Одежда',
            'rating': 5,
            'reviews': 89,
            'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'
        },
        {
            'id': 3,
            'name': 'Python для профессионалов',
            'price': 1200,
            'old_price': None,
            'discount': None,
            'category': 'Книги',
            'rating': 4,
            'reviews': 256,
            'image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400'
        },
        {
            'id': 4,
            'name': 'Рюкзак городской Urban',
            'price': 3100,
            'old_price': 3650,
            'discount': 15,
            'category': 'Аксессуары',
            'rating': 4,
            'reviews': 73,
            'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'
        },
    ]
    
    cart_count = 3  # заглушка
    return render_template('catalog.html', products=products, cart_count=cart_count)


# ========== КАРТОЧКА ТОВАРА ==========
@main_bp.route('/product')
@main_bp.route('/product/<int:product_id>')
def product(product_id=1):
    """Страница отдельного товара."""
    product_data = {
        'id': product_id,
        'name': 'Беспроводные наушники Pro',
        'price': 2499,
        'old_price': 3120,
        'category': 'Электроника',
        'rating': 4.5,
        'reviews': 128,
        'stock': 15,
        'description': 'Премиальные беспроводные наушники с активным шумоподавлением. До 30 часов автономной работы.',
        'features': ['Bluetooth 5.3', '30 часов работы', 'Шумоподавление ANC', 'Защита IPX5'],
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600',
        'gallery': [ 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100',
        'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=100',
        'https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?w=100'],
        'discount': 20,
    }
    
    cart_count = 3
    return render_template('product.html', product=product_data, cart_count=cart_count)


# ========== КОРЗИНА ==========
@main_bp.route('/cart')
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
@main_bp.route('/checkout')
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


# ========== ВХОД ==========
@main_bp.route('/login')
def login():
    """Страница входа и регистрации."""
    return render_template('login.html', cart_count=3)