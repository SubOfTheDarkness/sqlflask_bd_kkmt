import flask
import os
import threading
import time
from app.db import get_db

# Таймауты в секундах
USER_EXPIRATION = 600      # 1 час для удаления неподтверждённых
CHECK_INTERVAL = 60       # Проверка раз в 30 минут

def delete_unconfirmed_users(app):
    while True:
        time.sleep(CHECK_INTERVAL)
        with app.app_context():
            db = get_db()
            db.execute(
                "DELETE FROM user WHERE flag_confirmed = 0 AND created_at < ?",
                (time.time() - USER_EXPIRATION,)
            )
            db.commit()

def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'subamarket.sqlite')
    )
    app.config.from_pyfile('config.py')
    os.makedirs(app.instance_path, exist_ok=True)
    
    from . import db
    db.init_app(app)
    from . import cart
    app.register_blueprint(cart.bp)
    from . import admin
    app.register_blueprint(admin.bp)
    from . import auth
    with app.app_context():
        auth.init_mails()
    app.register_blueprint(auth.bp)

    from . import catalogue
    app.register_blueprint(catalogue.bp)
    
    @app.errorhandler(404)
    def not_found(error):
        return '<h1>Ошибка 404</h1><p><a href="/">Вернуться на главную страницу</a></p>', 404
    
    @app.errorhandler(500)
    def server_error(error):
        return '<h1>Ошибка 500(ошибка сервера)</h1><p><a href="/">Вернуться на главную страницу</a></p>', 500
    
    # Запуск фонового потока удаления неподтверждённых пользователей
    threading.Thread(target=delete_unconfirmed_users, args=(app,), daemon=True).start()
    
    return app