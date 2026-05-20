import flask
import os

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

    from . import db
    db.init_app(app)

    from . import cart
    app.register_blueprint(cart.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import catalogue
    app.register_blueprint(catalogue.bp)
    @app.errorhandler(404)
    def not_found(error):
        return '<h1>Ошибка 404</h1><p><a href="/">Вернуться на глваную страницу</a></p>', 404
    
    @app.errorhandler(500)
    def server_error(error):
        return '<h1>Ошибка 500(ошибка сервера)</h1><p><a href="/">Вернуться на глваную страницу</a></p>', 500
    return app