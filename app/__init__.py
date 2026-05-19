import flask
import os


# def create_app(test_config=None):
#     app = flask.Flask(__name__, instance_relative_config=True)
    
#     app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production-123!@#'
#     app.config['DEBUG'] = True
#     if test_config is None:
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         app.config.from_mapping(test_config)
#     os.makedirs(app.instance_path, exist_ok=True)
#     # Путь к базе данных (подготовка для SQLAlchemy)
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop.db')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     from . import catalogue_bp
#     app.register_blueprint(catalogue_bp)

#     from . import cart_bp
#     app.register_blueprint(cart_bp)
    
#     from . import auth_bp
#     app.register_blueprint(auth_bp)

    
    
#     return app
def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    os.makedirs(app.instance_path, exist_ok=True)
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # from . import bp
    # db.init_app(app)

    from . import cart
    app.register_blueprint(cart.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import catalogue
    app.register_blueprint(catalogue.bp)
    app.add_url_rule('/', endpoint='/catalogue')
    @app.errorhandler(404)
    def not_found(error):
        return '<h1>Ошибка 404</h1><p><a href="/">Вернуться на глваную страницу</a></p>', 404
    
    @app.errorhandler(500)
    def server_error(error):
        return '<h1>Ошибка 500(ошибка сервера)</h1><p><a href="/">Вернуться на глваную страницу</a></p>', 404
    return app