from abc import ABC, abstractmethod

class EmbeddingClient(ABC):

    @abstractmethod
    def get_embeddings(texts: list[str]):
        pass
