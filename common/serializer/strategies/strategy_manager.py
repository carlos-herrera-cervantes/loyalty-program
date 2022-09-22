from mongoengine import Document

from common.serializer.interfaces.strategy import Strategy
from common.serializer.strategies.id import Id
from common.serializer.strategies.date import Date


class StrategyManager:

    def __init__(self, type: str) -> None:
        self.__strategies: dict = {
            'id': Id(),
            'date': Date(),
        }
        self.__type = type

    def parse_value(self, key: str, document: Document) -> str | int | bool | list:
        strategy: Strategy = self.__strategies.get(self.__type, None)

        if not strategy:
            return document[key]

        return strategy.parse_value(key, document)


def initialize_manager(type: str) -> StrategyManager:
    return StrategyManager(type)
