from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_cors import CORS, cross_origin

if __name__ == '__main__':
    from injector import Injector

    import pachinkio.api.api as api
    from pachinkio.core.director import Director
    from pachinkio.openai.oa_module import OpenAiApiModule
    from pachinkio.prompts.prompts_module import PromptsModule

    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    print("Initializing Flask application")
    
    injector = Injector([OpenAiApiModule, PromptsModule('./pachinkio/prompts/prompts_v1.ini')])
    director = injector.get(Director)
    api_blueprint = api.construct_blueprint(director)

    app.register_blueprint(api_blueprint, url_prefix='')

    app.run(debug = True)