from abc import ABC, abstractmethod
from typing import Generator

class CompletionClient(ABC):

    @abstractmethod
    def get_completions(prompt: str, n: int, temp: float, stop: str) -> Generator[str, None, None]:
        """Get 'n' text completions for a given 'prompt' at temperature 'temp', with 'stop' word. Return
        a Generator of completion strings.
        """

        pass