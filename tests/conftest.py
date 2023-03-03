import pytest
from flask import Flask, jsonify, request
from flask.wrappers import Response
from flask_cors import CORS, cross_origin

@pytest.fixture()
def app():
    app = create_app()
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()