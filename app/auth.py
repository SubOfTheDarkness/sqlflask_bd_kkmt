from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)
# ========== ВХОД ==========
@auth_bp.route('/login')
def login():
    """Страница входа и регистрации."""
    return render_template('login.html', cart_count=3)