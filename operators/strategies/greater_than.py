from json import loads

from operators.interfaces.strategy import Strategy
from models.task import Task


class GreaterThanStrategy(Strategy):

    def run_task(self, task: Task, payload: dict, external_user_id: str) -> bool:
        transaction: dict = loads(payload)
        evaluation_value: int = transaction.get(task.evaluation_property, None)

        if not evaluation_value:
            return False

        return int(transaction[task.evaluation_property]) > int(task.comparison_value)
