from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from pachinkio.core.director import Director

def construct_blueprint(director: Director) -> Blueprint:

    api_blueprint = Blueprint('api_blueprint', __name__)

    @api_blueprint.route('/telephone', methods = ['POST'])
    def telephone() -> Response:
        req = request.json
        iterations = int(req['iterations']) if 'iterations' in req else None
        temperature = float(req['temperature']) if 'temperature' in req else None
        kwargs = dict(statement = req['statement'], iterations = iterations, temperature = temperature)

        results = director.run_telephone_game(**{k: v for k, v in kwargs.items() if v is not None})
        return jsonify({'steps': results, 'endStatement': results[-1]})

    @api_blueprint.route('/compare-statements', methods = ['POST'])
    def compare_statements() -> Response:
        req = request.json
        similarity = director.compare_statements(req['statement1'], req['statement2'])
        return jsonify({'similarity': similarity})

    @api_blueprint.route('/interpolate-concepts', methods = ['POST'])
    def interpolate_concepts() -> Response:
        req = request.json
        iterations = int(req['iterations']) if 'iterations' in req else None
        fanout = int(req['fanout']) if 'fanout' in req else None
        kwargs = dict(start_statement = req['startStatement'], target_statement = req['targetStatement'], iterations = iterations, fanout = fanout)
        results = director.interpolate_concepts(**{k: v for k, v in kwargs.items() if v is not None})
        return jsonify({'steps': results[0], 'terminationReason': results[1]})
    
    return api_blueprint