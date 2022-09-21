from ..interfaces.strategy_interface import Strategy
from ...models.task import Task
from json import loads


class EqualStrategy(Strategy):

    def run_task(self, task: Task, payload: dict, external_user_id: str) -> bool:
        transaction: dict = loads(payload)

        if task.comparison_value_type == 'int':
            return int(transaction['evaluation_value']) == int(task.comparison_value)

        return transaction['evaluation_value'] == task.comparison_value
