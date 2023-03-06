from injector import Injector
import pytest

from pachinkio import create_app
from pachinkio.openai.oa_module import OpenAiApiModule
from pachinkio.prompts.prompts_module import PromptsModule

@pytest.fixture()
def app():
    
    injector = Injector([OpenAiApiModule('test.env'), PromptsModule('./pachinkio/prompts/prompts_v1.ini')])
    app = create_app(injector)
    app.config.update({"TESTING": True})

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()