
if __name__ == '__main__':

    from flask import Flask, jsonify, request
    from flask_cors import CORS, cross_origin
    from injector import Injector
    from pachinkio.openai.oa_module import OpenAiApiModule
    from pachinkio.core.director import Director

    print("Initializing Flask application")
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    injector = Injector([OpenAiApiModule])
    director = injector.get(Director)

    app.run(debug = True)

@app.route('/engine', methods = ['GET'])
def get_engine():
    return jsonify({'engine': engine})

@app.route('/telephone', methods = ['POST'])
def telephone():
    content = request.json
    iterations = content['iterations'] if 'iterations' in content else None
    temperature = content['temperature'] if 'temperature' in content else None
    kwargs = dict(statement = content['statement'], iterations = iterations, temperature = temperature)

    results = director.run_telephone_game(**{k: v for k, v in kwargs.items() if v is not None})
    return jsonify({'steps': results, 'endStatement': results[-1]})
