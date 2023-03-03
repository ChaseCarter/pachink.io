from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_cors import CORS, cross_origin
from injector import Injector

import pachinkio.api.api as api
from pachinkio.core.director import Director

def create_app(injector: Injector):
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    print("Initializing Flask application")

    director = injector.get(Director)
    api_blueprint = api.construct_blueprint(director)

    app.register_blueprint(api_blueprint, url_prefix='')

    return app

if __name__ == '__main__':
    from pachinkio.openai.oa_module import OpenAiApiModule
    from pachinkio.prompts.prompts_module import PromptsModule

    injector = Injector([OpenAiApiModule, PromptsModule('./pachinkio/prompts/prompts_v1.ini')])
    app = create_app(injector)

    app.run(debug = True)