from .completion_client import CompletionClient
import openai

class OpenAICompletions(CompletionClient):

    organization: str
    api_key: str
    engine: str

    def __init__(self, organization: str, api_key: str, engine: str = 'text-babbage-001'):
        self.organization = organization
        self.api_key = api_key
        self.engine = engine

        openai.organization = organization
        openai.api_key = api_key

    def get_completions(self, prompt: str, n: int = 1, temp: float = 0.5) -> list[str]:
        res = openai.Completion.create(
            engine='text-babbage-001',
            prompt=prompt,
            temperature=temp,
            max_tokens=124,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            n=n
        )
        return (choice['text'].strip() for choice in res['choices'])