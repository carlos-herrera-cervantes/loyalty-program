from abc import ABC, abstractmethod

class Strategy(ABC):

    @abstractmethod
    def get_translation(self, key: str) -> str:
        pass
