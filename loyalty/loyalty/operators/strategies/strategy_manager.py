from .equal_strategy import EqualStrategy
from .add_strategy import AddStrategy
from .greater_than_equal_strategy import GreaterThanEqualStrategy
from .greater_than_strategy import GreaterThanStrategy
from .less_than_equal_strategy import LessThanEqualStrategy
from .less_than_strategy import LessThanStrategy
from .set_strategy import SetStrategy
from .subtract_strategy import SubtractStrategy
from .sum_points_strategy import SumPointsStrategy
from .subtract_points_strategy import SubtractPointsStrategy
from ..interfaces.strategy_interface import Strategy
from ...models.task import Task

class StrategyManager:

    def __init__(self, operator: str) -> None:
        self.strategies: dict = {
            '==': EqualStrategy(),
            '+': AddStrategy(),
            '>=': GreaterThanEqualStrategy(),
            '>': GreaterThanStrategy(),
            '<=': LessThanEqualStrategy(),
            '<': LessThanStrategy(),
            '=': SetStrategy(),
            '-': SubtractStrategy(),
            'add': SumPointsStrategy(),
            'subtract': SubtractPointsStrategy(),
        }

        self.operator = operator

    def do_action(self, task: Task, payload: dict, external_user_id: str) -> bool:
        strategy: Strategy = self.strategies.get(self.operator)

        if not strategy:
            return False

        return strategy.run_task(task, payload, external_user_id)

def initialize_manager(operator: str):
    return StrategyManager(operator)