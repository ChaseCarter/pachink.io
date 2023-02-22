from flask import Flask, jsonify, request

app = Flask(__name__)

if __name__ == '__main__':
    from pachinkio.core.director import Director
    from pachinkio.core.oa_client import OpenAIClient
    import configparser

    config = configparser.ConfigParser()
    config.read('.env')
    org_id = config['open-ai']['organization-id']
    api_key = config['open-ai']['api-key']
    engine = config['open-ai']['engine']

    print(f"Initializing Director with engine: {engine}")

    client = OpenAIClient(organization=org_id, api_key=api_key, engine=engine)
    director = Director(client, client)

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
    return jsonify({'steps': results, 'end-statement': results[-1]})

if __name__ == '__main__':
    app.run(debug = True)
