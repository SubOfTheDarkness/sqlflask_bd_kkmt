from flask import Flask
import os


def create_app():
    """
    Фабрика приложения Flask.
    Позволяет гибко настраивать приложение (тесты, разные конфигурации).
    """
    app = Flask(__name__)
    
    # ========== КОНФИГУРАЦИЯ ==========
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production-123!@#'
    app.config['DEBUG'] = True
    
    # Путь к базе данных (подготовка для SQLAlchemy)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # ========== РЕГИСТРАЦИЯ МАРШРУТОВ ==========
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # ========== ОБРАБОТЧИКИ ОШИБОК ==========
    @app.errorhandler(404)
    def not_found(error):
        return '<h1 style="text-align:center; margin-top:4rem;">🔍 Страница не найдена</h1><p style="text-align:center;"><a href="/">Вернуться в каталог</a></p>', 404
    
    @app.errorhandler(500)
    def server_error(error):
        return '<h1 style="text-align:center; margin-top:4rem;">💥 Ошибка сервера</h1><p style="text-align:center;"><a href="/">Вернуться в каталог</a></p>', 500
    
    return app