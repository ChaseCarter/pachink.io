from abc import ABC, abstractmethod
from typing import Generator

class CompletionClient(ABC):

    @abstractmethod
    def get_completions(prompt: str, n: int, temp: float) -> Generator[str, None, None]:
        pass