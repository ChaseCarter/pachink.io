from flask import Flask
from flask_cors import CORS
from injector import Injector

from .core.director import Director
from .api import api

def create_app(injector: Injector) -> Flask:
    
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    print("Constructing Flask application")
    director = injector.get(Director)
    api_blueprint = api.construct_blueprint(director)
    app.register_blueprint(api_blueprint, url_prefix='')

    return app