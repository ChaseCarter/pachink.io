from abc import ABC, abstractmethod

class SessionRepository(ABC):

    @abstractmethod
    def store_session(self) -> None:
        pass

    @abstractmethod
    def retrieve_session(self, id: str): 
        pass

    @abstractmethod
    def store_completion(self, completion: str) -> None:
        pass
