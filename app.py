from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/telephone', methods = ['POST'])
def telephone() -> Response:
    req = request.json
    iterations = int(req['iterations']) if 'iterations' in req else None
    temperature = float(req['temperature']) if 'temperature' in req else None
    kwargs = dict(statement = req['statement'], iterations = iterations, temperature = temperature)

    results = director.run_telephone_game(**{k: v for k, v in kwargs.items() if v is not None})
    return jsonify({'steps': results, 'endStatement': results[-1]})

@app.route('/compare-statements', methods = ['POST'])
def compare_statements() -> Response:
    req = request.json
    similarity = director.compare_statements(req['statement1'], req['statement2'])
    return jsonify({'similarity': similarity})

@app.route('/interpolate-concepts', methods = ['POST'])
def interpolate_concepts() -> Response:
    req = request.json
    iterations = int(req['iterations']) if 'iterations' in req else None
    fanout = int(req['fanout']) if 'fanout' in req else None
    kwargs = dict(start_statement = req['startStatement'], target_statement = req['targetStatement'], iterations = iterations, fanout = fanout)
    results = director.interpolate_concepts(**{k: v for k, v in kwargs.items() if v is not None})
    return jsonify({'steps': results[0], 'terminationReason': results[1]})

if __name__ == '__main__':
    from injector import Injector

    from pachinkio.core.director import Director
    from pachinkio.openai.oa_module import OpenAiApiModule
    from pachinkio.prompts.prompts_module import PromptsModule
    
    print("Initializing Flask application")
    
    injector = Injector([OpenAiApiModule, PromptsModule('./pachinkio/prompts/prompts_v1.ini')])
    director = injector.get(Director)

    app.run(debug = True)