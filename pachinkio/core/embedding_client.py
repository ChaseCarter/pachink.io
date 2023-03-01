from abc import ABC, abstractmethod
from typing import Generator

class EmbeddingClient(ABC):

    @abstractmethod
    def get_embeddings(texts: list[str]) -> Generator[list[float], None, None]:
        pass
