from abc import ABC, abstractmethod

from mongoengine import Document


class Strategy(ABC):

    @abstractmethod
    def parse_value(key: str, document: Document) -> str:
        pass
