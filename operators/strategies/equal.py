from json import loads

from operators.interfaces.strategy import Strategy
from models.task import Task


class EqualStrategy(Strategy):

    def run_task(self, task: Task, payload: dict, external_user_id: str) -> bool:
        transaction: dict = loads(payload)
        evaluation_value: str | int = transaction.get(task.evaluation_property, None)

        if not evaluation_value:
            return False

        if task.comparison_value_type == 'int':
            return int(transaction[task.evaluation_property]) == int(task.comparison_value)

        return transaction[task.evaluation_property] == task.comparison_value
