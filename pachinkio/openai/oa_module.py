import configparser
from .oa_client import OpenAIClient 
from injector import Module
from pachinkio.core.completion_client import CompletionClient
from pachinkio.core.embedding_client import EmbeddingClient

class OpenAiApiModule(Module):
    def configure(self, binder):
        config = configparser.ConfigParser()
        config.read('.env')
        org_id = config['open-ai']['organization-id']
        api_key = config['open-ai']['api-key']
        engine = config['open-ai']['engine']

        client = OpenAIClient(organization=org_id, api_key=api_key, engine=engine)
        binder.bind(CompletionClient, to=client)
        binder.bind(EmbeddingClient, to=client)