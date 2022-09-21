from ..interfaces.strategy_interface import Strategy
from ...models.task import Task
from ...models.customer import CustomerKeys, Customer


class SetStrategy(Strategy):

    def run_task(self, task: Task, payload: dict, external_user_id: str) -> bool:
        customers: Customer = Customer.objects.filter(external_user_id=external_user_id).values('id')

        CustomerKeys.objects.create({
            'key': task.customer_property,
            'value': task.assign_value,
            'type': task.assign_value_type,
            'customer': customers[0]['id'],
        })

        return True
