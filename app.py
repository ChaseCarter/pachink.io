from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/telephone', methods = ['POST'])
def telephone() -> Response:
    content = request.json
    iterations = content['iterations'] if 'iterations' in content else None
    temperature = content['temperature'] if 'temperature' in content else None
    kwargs = dict(statement = content['statement'], iterations = iterations, temperature = temperature)

    results = director.run_telephone_game(**{k: v for k, v in kwargs.items() if v is not None})
    print(type(jsonify({'steps': results, 'endStatement': results[-1]})))
    return jsonify({'steps': results, 'endStatement': results[-1]})

if __name__ == '__main__':
    from injector import Injector
    from pachinkio.openai.oa_module import OpenAiApiModule
    from pachinkio.core.director import Director

    print("Initializing Flask application")
    
    injector = Injector([OpenAiApiModule])
    director = injector.get(Director)

    app.run(debug = True)