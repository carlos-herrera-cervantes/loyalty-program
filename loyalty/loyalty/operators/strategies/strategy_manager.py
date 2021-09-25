from equal_strategy import EqualStrategy
from interfaces.strategy_interface import Strategy
from models.task import Task

class StrategyManager:

    def __init__(self, operator: str) -> None:
        self.strategies: dict = {
            '=': EqualStrategy(),
        }

        self.operator = operator

    def do_action(self, task: Task) -> bool:
        strategy: Strategy = self.strategies.get(self.operator)

        if not strategy:
            return False

        return strategy.run_task(task)

def initialize_manager(operator: str):
    return StrategyManager(operator)