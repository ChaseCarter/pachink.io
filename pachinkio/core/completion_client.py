from abc import ABC, abstractmethod

class CompletionClient(ABC):

    @abstractmethod
    def get_completions(prompt: str, n: int, temp: float) -> list[str]:
        pass