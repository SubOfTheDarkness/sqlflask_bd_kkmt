import functools
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__)
def init_mails():
    global mail
    mail = Mail(current_app)
    global serializer
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# ========== ВХОД ==========
def generate_confirmation_token(email):
    return serializer.dumps(email, salt='email-confirm-salt')

TOKEN_EXPIRATION = 600  # 10 мин

def confirm_token(token, expiration=TOKEN_EXPIRATION):
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except:
        return False
    return email

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.auth'))

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user or g.user['flag_admin']==0:
            return redirect(url_for('auth.need_admin'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/sending_a_mail', methods=['POST'])
def send_email():
    data = request.get_json()
    user_email = data.get('user_email')
    error = None
    
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    msg = Message('Подтверждение аккаунта Suba Market', recipients=[user_email], html=html)
    
    try:
        mail.send(msg)
    except Exception as e:
        error = str(e)
    
    if error:
        db = get_db()
        db.execute('DELETE FROM user WHERE email=?', (user_email,))
        db.commit()
        return jsonify({'status': 'error', 'message': error})
    
    return jsonify({'status': 'success'})

@bp.route('/sent_email')
def sent_email():
    email = request.args.get('email', '')
    return render_template('auth/sent_email.html', email=email)

@bp.route('/sending')
def sending():
    user_email = request.args.get("user_email", "")
    return render_template('auth/sending.html', user_email=user_email)

@bp.route('/email_error')
def email_error():
    error = request.args.get("error", "Неизвестная ошибка")
    return render_template('auth/email_error.html', error=error)

@bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return render_template('auth/confirm_error.html'), 400
    
    db = get_db()
    try:
        db.execute("UPDATE user SET flag_confirmed=1 WHERE email=?", (email,))
        db.commit()
        return render_template('auth/confirmed.html', email=email)
    except:
        return render_template('auth/confirm_error.html'), 500

@bp.route('/register')
def register():
    return redirect(url_for('auth.auth',method='register'))

@bp.route('/login')
def login():
    return redirect(url_for('auth.auth',method='login'))

@bp.route('/forgot', methods=('GET', 'POST'))
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
        if user:
            token = generate_confirmation_token(email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            html = render_template('auth/reset_email.html', reset_url=reset_url)
            msg = Message('Сброс пароля Suba Market', recipients=[email], html=html)
            mail.send(msg)
        flash('Если аккаунт существует, ссылка отправлена на почту', 'info')
        return redirect(url_for('auth.auth'))
    return render_template('auth/forgot.html')


@bp.route('/reset/<token>', methods=('GET', 'POST'))
def reset_password(token):
    email = confirm_token(token)
    if not email:
        flash('Ссылка недействительна или истекла', 'error')
        return redirect(url_for('auth.auth'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm_password']
        if password != confirm:
            flash('Пароли не совпадают', 'error')
        elif len(password) < 6:
            flash('Пароль должен быть не менее 6 символов', 'error')
        else:
            db = get_db()
            db.execute('UPDATE user SET password=? WHERE email=?', 
                      (generate_password_hash(password), email))
            db.commit()
            flash('Пароль успешно изменён', 'success')
            return redirect(url_for('auth.auth'))
    
    return render_template('auth/reset_password.html', token=token)

@bp.route('/need_admin')
def need_admin():
    return render_template('auth/need_admin.html')

@bp.route('/auth', methods=('GET', 'POST'))
def auth():
    method = request.args.get("tab", "Flask")
    input_data=None
    if request.method == 'POST':
        if(method=='register'):
            email = request.form['email']
            password = request.form['password']
            db = get_db()
            error = None

            if not email:
                error = 'E-mail is required.'
            elif not password:
                error = 'Password is required.'
            elif len(password) < 6:
                error = 'Пароль должен быть не менее 6 символов.'
            if error is None:
                try:
                    db.execute("BEGIN")
                    from time import time
                    db.execute(
                        "INSERT INTO user (email, password, created_at) VALUES (?, ?, ?)",
                        (email, generate_password_hash(password), time()),
                    )
                    token = generate_confirmation_token(email)
                    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
                    html = render_template('auth/activate.html', confirm_url=confirm_url)
                    msg = Message('Подтверждение аккаунт', recipients=[email], html=html)
                except db.IntegrityError:
                    error = f"User with e-mail {email} is already registered."
                except Exception as e:
                    db.rollback()
                    error = e
                else:
                    if error is None:
                        db.commit()
                        error = None
                        return redirect(url_for('auth.sending', user_email=email))
            input_data = request.form.to_dict()
            flash(error,'error')

        elif(method=='login'):
            email = request.form['email']
            password = request.form['password']
            db = get_db()
            error = None
            user = db.execute(
                'SELECT * FROM user WHERE email = ?', (email,)
            ).fetchone()
            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
            elif user['flag_confirmed']==0:
                error = 'Пользователь не подтвердил почту'
            if error is None:
                session.clear()
                session['user_id'] = user['id']
                session['email'] = user['email']
                session['flag_admin'] = user['flag_admin']
                return redirect(url_for('catalogue.catalogue'))
            input_data = request.form.to_dict()
            flash(error,'error')
    return render_template('auth/auth.html', input_data=input_data)

@bp.route('/resend_confirmation', methods=['POST'])
def resend_confirmation():
    email = request.form['email']
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE email=? AND flag_confirmed=0', (email,)).fetchone()
    if user:
        token = generate_confirmation_token(email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/activate.html', confirm_url=confirm_url)
        msg = Message('Подтверждение аккаунта Suba Market', recipients=[email], html=html)
        mail.send(msg)
        return redirect(url_for('auth.sending', user_email=email))
    flash('Аккаунт не найден или уже подтверждён', 'error')
    return redirect(url_for('auth.auth'))

@bp.route('/profile')
@login_required
def profile():
    db = get_db()
    user_orders = db.execute(
        'SELECT o.id, o.name, o.phone_number, o.email, o.address_delivery,'
        ' o.pay_method, o.comment'
        ' FROM orders o'
        ' WHERE o.user_id = ?'
        ' ORDER BY o.id DESC',
        (g.user['id'],)
    ).fetchall()

    orders_with_items = []
    total_spent = 0
    for order in user_orders:
        items = db.execute(
            'SELECT product, quantity, price FROM order_products WHERE order_id=?',
            (order['id'],)
        ).fetchall()
        total = sum(item['price'] * item['quantity'] for item in items)
        total_spent += total
        orders_with_items.append({
            'order': order,
            'products': items,
            'total': total
        })

    last_order = orders_with_items[0] if orders_with_items else None

    return render_template('auth/profile.html',
                         orders=orders_with_items,
                         last_order=last_order,
                         total_spent=total_spent)


@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    if not check_password_hash(g.user['password'], old_password):
        flash('Неверный текущий пароль', 'error')
    elif new_password != confirm_password:
        flash('Новые пароли не совпадают', 'error')
    elif len(new_password) < 6:
        flash('Пароль должен быть не менее 6 символов', 'error')
    else:
        db = get_db()
        db.execute(
            'UPDATE user SET password=? WHERE id=?',
            (generate_password_hash(new_password), g.user['id'])
        )
        db.commit()
        flash('Пароль успешно изменён', 'success')
    
    return redirect(url_for('auth.profile'))

@bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = g.user['id']
    db = get_db()
    db.execute('DELETE FROM cart WHERE user_id=?', (user_id,))
    db.execute('DELETE FROM order_products WHERE order_id IN (SELECT id FROM orders WHERE user_id=?)', (user_id,))
    db.execute('DELETE FROM orders WHERE user_id=?', (user_id,))
    db.execute('DELETE FROM user WHERE id=?', (user_id,))
    db.commit()
    session.clear()
    flash('Аккаунт удалён', 'info')
    return redirect(url_for('catalogue.catalogue'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('catalogue.catalogue'))

