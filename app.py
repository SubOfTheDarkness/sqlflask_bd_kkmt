from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/admin")
def admin_panel():
    return "<p>Это админ панель будет короче<p>"
