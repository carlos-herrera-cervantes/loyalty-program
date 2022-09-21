from .es_strategy import EsStrategy
from .en_strategy import EnStrategy
from ..interfaces.strategy_interface import Strategy


class StrategyManager:
    
    def __init__(self, lang: str):
        self.strategies: dict = {
            'en': EnStrategy(),
            'es': EsStrategy(),
        }

        self.lang = lang

    def translate(self, key: str) -> str:
        strategy: Strategy = self.strategies.get(self.lang)

        if not strategy:
            return key

        return strategy.get_translation(key)


def initialize_manager(lang: str) -> StrategyManager:
    return StrategyManager(lang)
