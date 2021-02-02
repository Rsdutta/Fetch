from flask import Flask

from Controller import urls_blueprint

app = Flask(__name__)

app.register_blueprint(urls_blueprint)
