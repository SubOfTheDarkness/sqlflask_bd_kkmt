import flask
from flask import url_for
app = flask.Flask(__name__)
@app.route("/")
def main():
    return flask.redirect(url_for('index'))
@app.route("/index")
def index():
    return "<h1>Привет, мир!</h1>"
@app.route("/admin")
def admin_panel():
    return "<p>Это админ панель будет короче<p>"

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('admin_panel'))
