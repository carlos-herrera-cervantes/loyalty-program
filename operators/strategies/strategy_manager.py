from operators.strategies.equal import EqualStrategy
from operators.strategies.add import AddStrategy
from operators.strategies.greater_than_equal import GreaterThanEqualStrategy
from operators.strategies.greater_than import GreaterThanStrategy
from operators.strategies.less_than_equal import LessThanEqualStrategy
from operators.strategies.less_than import LessThanStrategy
from operators.strategies.set import SetStrategy
from operators.strategies.subtract import SubtractStrategy
from operators.strategies.sum_points import SumPointsStrategy
from operators.strategies.subtract_points import SubtractPointsStrategy
from operators.interfaces.strategy import Strategy
from models.task import Task


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
