from configparser import ConfigParser
from injector import Module

from .oa_client import OpenAIClient 
from pachinkio.core.completion_client import CompletionClient
from pachinkio.core.embedding_client import EmbeddingClient


class OpenAiApiModule(Module):
    def configure(self, binder):
        config = ConfigParser()
        config.read('.env')
        openAiConfig = config['open-ai']
        org_id = openAiConfig['organization-id']
        api_key = openAiConfig['api-key']
        engine = openAiConfig['engine']

        client = OpenAIClient(organization=org_id, api_key=api_key, engine=engine)
        binder.bind(CompletionClient, to=client)
        binder.bind(EmbeddingClient, to=client)