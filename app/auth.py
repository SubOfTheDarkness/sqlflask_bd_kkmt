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

def confirm_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except:
        return False
    return email

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
    return render_template('auth/sent_email.html')

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
    error = None
    if not email:
        return 'Ссылка подтверждения недействительна или истекла.', 400

    db = get_db()
    try:
        db.execute("BEGIN")
        db.execute(
            "UPDATE user SET flag_confirmed=1 WHERE email=?", (email,)
        )
    except:
        db.rollback()
        error = "Ошибка в БД"
    else:
        db.commit()
        return render_template('auth/confirmed.html', email=email)
    flash(error, 'error')
    return redirect(url_for('auth.auth'))

@bp.route('/register')
def register():
    return redirect(url_for('auth.auth',method='register'))

@bp.route('/login')
def login():
    return redirect(url_for('auth.auth',method='login'))

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
            #elif not '@' in email and not '.' in email:
            #    error = 'This is not e-mail.'
            if error is None:
                try:
                    db.execute("BEGIN")
                    db.execute(
                        "INSERT INTO user (email, password) VALUES (?, ?)",
                        (email, generate_password_hash(password),),
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

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user or g.user['flag_admin']==0:
            return redirect(url_for('auth.need_admin'))
        return view(**kwargs)
    return wrapped_view