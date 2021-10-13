from ..interfaces.strategy_interface import Strategy
from ...models.task import Task
from json import loads

class GreaterThanEqualStrategy(Strategy):

    def run_task(self, task: Task, payload: dict, external_user_id: str) -> bool:
        transaction: dict = loads(payload)
        return int(transaction['evaluation_value']) >= int(task.comparison_value)