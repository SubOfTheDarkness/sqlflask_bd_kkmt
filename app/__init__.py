import flask
import os


def create_app():
    app = flask.Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production-123!@#'
    app.config['DEBUG'] = True
    
    # Путь к базе данных (подготовка для SQLAlchemy)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from app.catalogue import catalogue_bp
    app.register_blueprint(catalogue_bp)

    from app.cart import cart_bp
    app.register_blueprint(cart_bp)
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    @app.errorhandler(404)
    def not_found(error):
        return '<h1>Ошибка 404</h1><p><a href="/">Вернуться на глваную страницу</a></p>', 404
    
    @app.errorhandler(500)
    def server_error(error):
        return '<h1>Ошибка 500(ошибка сервера)</h1><p><a href="/">Вернуться на глваную страницу</a></p>', 404
    
    return app