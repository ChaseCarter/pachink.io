from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/telephone', methods = ['POST'])
def telephone() -> Response:
    content = request.json
    iterations = int(content['iterations']) if 'iterations' in content else None
    temperature = float(content['temperature']) if 'temperature' in content else None
    kwargs = dict(statement = content['statement'], iterations = iterations, temperature = temperature)

    results = director.run_telephone_game(**{k: v for k, v in kwargs.items() if v is not None})
    return jsonify({'steps': results, 'endStatement': results[-1]})

@app.route('/compare-statements', methods = ['POST'])
def compare_statements() -> Response:
    content = request.json
    statement_1 = content['statement1']
    statement_2 = content['statement2']
    similarity = director.compare_statements(statement_1, statement_2)
    return jsonify({'similarity': similarity})

@app.route('/interpolate-concepts', methods = ['POST'])
def interpolate_concepts() -> Response:
    content = request.json
    iterations = int(content['iterations']) if 'iterations' in content else None
    fanout = int(content['fanout']) if 'fanout' in content else None
    kwargs = dict(start_statement = content['startStatement'], target_statement = content['targetStatement'], iterations = iterations, fanout = fanout)
    results = director.interpolate_concepts(**{k: v for k, v in kwargs.items() if v is not None})
    return jsonify({'steps': results[0], 'terminationReason': results[1]})

if __name__ == '__main__':
    from injector import Injector

    from pachinkio.core.director import Director
    from pachinkio.openai.oa_module import OpenAiApiModule
    from pachinkio.prompts.prompts_v1_module import PromptsV1Module
    

    print("Initializing Flask application")
    
    injector = Injector([OpenAiApiModule, PromptsV1Module])
    director = injector.get(Director)

    app.run(debug = True)