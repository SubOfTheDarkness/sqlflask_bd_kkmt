import functools
from __init__ import serializer
from __init__ import mail
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__)
# ========== ВХОД ==========
def generate_confirmation_token(email):
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except:
        return False
    return email
@bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return 'Ссылка подтверждения недействительна или истекла.', 400
    
    db = get_db()
    db.execute(
        "UPDATE user SET flag_confirmed=1 WHERE email=?",(email)
    )
    db.commit()
    return f'Почта {email} успешно подтверждена!'
@bp.route('/register')
def register():
    return redirect(url_for('auth.auth',method='register'))
@bp.route('/login')
def login():
    return redirect(url_for('auth.auth',method='login'))

@bp.route('/auth', methods=('GET', 'POST'))
def auth():
    method = request.args.get("tab", "Flask")
    
    if request.method == 'POST':
        if(method=="register"):
            email = request.form['email']
            password = request.form['password']
            db = get_db()
            error = None

            if not email:
                error = 'E-mail is required.'
            elif not password:
                error = 'Password is required.'
            elif not '@' in email and not '.' in email:
                error = 'This is not e-mail.'
            if error is None:
                try:
                    db.execute(
                        "INSERT INTO user (email, password) VALUES (?, ?)",
                        (email, generate_password_hash(password)),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"User with e-mail {email} is already registered."
                else:
                    error = None
                    return "<p>Ссылка на подтверждение отправлена Вам на почту</p>"

            flash(error)
        else:
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

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('catalogue.catalogue'))

            flash(error)
    return render_template('auth/auth.html')

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

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.auth'))

        return view(**kwargs)

    return wrapped_view
# @bp.route('/login')
# def login():
#     """Страница входа и регистрации."""
#     return render_template('auth/login.html')