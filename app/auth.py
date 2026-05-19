from flask import Blueprint, render_template

bp = Blueprint('auth', __name__)
# ========== ВХОД ==========
@bp.route('/login')
def login():
    """Страница входа и регистрации."""
    return render_template('login.html', cart_count=3)