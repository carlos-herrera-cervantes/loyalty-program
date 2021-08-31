from abc import ABC, abstractmethod

class Strategy(ABC):
    def get_translation(self, key: str) -> str:
        pass
