import openai
from typing import Generator

from pachinkio.core.completion_client import CompletionClient
from pachinkio.core.embedding_client import EmbeddingClient

class OpenAIClient(CompletionClient, EmbeddingClient):
    """Implementation of CompletionClient and EmbeddingClient which calls OpenAI API.
    """

    organization: str
    api_key: str
    engine: str

    def __init__(self, organization: str, api_key: str, engine: str = 'text-babbage-001') -> None:
        self.organization = organization
        self.api_key = api_key
        self.engine = engine

        openai.organization = organization
        openai.api_key = api_key
        print(f"Initializing OpenAIClient with engine [{self.engine}]")

    def get_completions(self, prompt: str, n: int = 1, temp: float = 0.5, stop: str = None) -> Generator[str, None, None]:
        res = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            temperature=temp,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop,
            n=n
        )
        return (choice['text'].strip() for choice in res['choices'])
    
    def get_embeddings(self, texts: list[str]) -> Generator[list[float], None, None]:
        res = openai.Embedding.create(input=texts, model='text-embedding-ada-002')
        return ((item['embedding'], item['index']) for item in res["data"])
