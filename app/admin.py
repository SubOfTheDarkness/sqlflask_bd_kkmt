from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from app.db import get_db

bp = Blueprint('admin', __name__)


@bp.route('/admin')
def admin():
    import os
    db = get_db()
    products = db.execute('SELECT * FROM product ORDER BY id DESC').fetchall()
    users = db.execute('SELECT * FROM user ORDER BY id DESC').fetchall()
    carts = db.execute(
        'SELECT c.id, u.email, p.title, c.quantity, c.user_id, c.product_id '
        'FROM cart c '
        'LEFT JOIN user u ON u.id = c.user_id '
        'LEFT JOIN product p ON p.id = c.product_id '
        'ORDER BY c.id DESC'
    ).fetchall()
    images = []
    img_dir = os.path.join(current_app.root_path, 'static', 'images')
    if os.path.exists(img_dir):
        images = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png', '.jpeg', '.gif', '.webp'))]
    
    return render_template('admin/admin.html', products=products, users=users, carts=carts, images=images)


# ========== ТОВАРЫ ==========

@bp.route('/admin/product/add', methods=['POST'])
def add_product():
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    discount = request.form.get('discount', 0) or 0
    category = request.form['category']
    image = request.form.get('image', '')
    image_url = request.form.get('image_url', '')
    
    # Если указан URL — используем его
    if image_url:
        image = image_url
    
    db = get_db()
    db.execute(
        'INSERT INTO product(title, description, price, discount, category, image) VALUES(?,?,?,?,?,?)',
        (title, description, price, discount, category, image)
    )
    db.commit()
    return redirect(url_for('admin.admin'))


@bp.route('/admin/product/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    discount = request.form.get('discount', 0) or 0
    category = request.form['category']
    image = request.form.get('image', '')
    db = get_db()
    db.execute(
        'UPDATE product SET title=?, description=?, price=?, discount=?, category=?, image=? WHERE id=?',
        (title, description, price, discount, category, image, product_id)
    )
    db.commit()
    return redirect(url_for('admin.admin'))


@bp.route('/admin/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    db = get_db()
    # Удаляем товар из всех корзин
    db.execute('DELETE FROM cart WHERE product_id = ?', (product_id,))
    # Удаляем сам товар
    db.execute('DELETE FROM product WHERE id = ?', (product_id,))
    db.commit()
    return redirect(url_for('admin.admin'))


# ========== ПОЛЬЗОВАТЕЛИ ==========

@bp.route('/admin/user/add', methods=['POST'])
def add_user():
    from werkzeug.security import generate_password_hash
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    try:
        db.execute(
            'INSERT INTO user(email, password, flag_confirmed) VALUES(?,?,1)',
            (email, generate_password_hash(password),)
        )
        db.commit()
    except db.IntegrityError:
        flash("Пользователь уже существует")
    return redirect(url_for('admin.admin'))


@bp.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    db = get_db()
    # Удаляем корзину пользователя
    db.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
    # Удаляем пользователя
    db.execute('DELETE FROM user WHERE id = ?', (user_id,))
    db.commit()
    return redirect(url_for('admin.admin'))


@bp.route('/admin/user/toggle_confirmation/<int:user_id>', methods=['POST'])
def toggle_confirmation(user_id):
    db = get_db()
    user = db.execute('SELECT flag_confirmed FROM user WHERE id = ?', (user_id,)).fetchone()
    if user:
        new_val = 0 if user['flag_confirmed'] else 1
        db.execute('UPDATE user SET flag_confirmed = ? WHERE id = ?', (new_val, user_id))
        db.commit()
    return redirect(url_for('admin.admin'))


# ========== КОРЗИНЫ ==========

@bp.route('/admin/cart/delete/<int:cart_id>', methods=['POST'])
def delete_cart_item(cart_id):
    db = get_db()
    db.execute('DELETE FROM cart WHERE id = ?', (cart_id,))
    db.commit()
    return redirect(url_for('admin.admin'))


@bp.route('/admin/cart/update/<int:cart_id>', methods=['POST'])
def update_cart_item(cart_id):
    quantity = request.form.get('quantity', 1)
    db = get_db()
    db.execute('UPDATE cart SET quantity = ? WHERE id = ?', (quantity, cart_id))
    db.commit()
    return redirect(url_for('admin.admin'))