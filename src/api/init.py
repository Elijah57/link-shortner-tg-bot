from flask import Flask
from .routes import api

def create_app():
    app = Flask(__name__)

    # Register the API Blueprint with a URL prefix
    app.register_blueprint(api, url_prefix='/api')

    return app
