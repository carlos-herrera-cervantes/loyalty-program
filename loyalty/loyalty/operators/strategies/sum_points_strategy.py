from ..interfaces.strategy_interface import Strategy
from ...models.task import Task
from ...models.customer import Customer


class SumPointsStrategy(Strategy):

    def run_task(self, task: Task, payload: dict, external_user_id: str) -> bool:
        customers: Customer = Customer.objects.filter(
            external_user_id=external_user_id,
        ).values('active_points')

        accumulator: int = int(task.assign_value) + customers[0]['active_points']
        Customer.objects.filter(external_user_id=external_user_id).update(active_points=accumulator)

        return True
