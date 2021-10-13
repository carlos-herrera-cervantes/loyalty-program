from ..interfaces.strategy_interface import Strategy
from ...models.task import Task
from ...models.customer import CustomerKeys, Customer

class SubtractStrategy(Strategy):

    def run_task(self, task: Task, payload: dict, external_user_id: str) -> bool:
        customers: Customer = Customer.objects.filter(external_user_id=external_user_id).values('id')
        key: CustomerKeys = CustomerKeys.objects.get(
            customer=customers[0]['id'],
            key=task.customer_property,
        )
        
        parsed_property_value: int = int(key.value)
        parsed_assign_value: int = int(task.assign_value)

        CustomerKeys.objects.filter(id=key.id).update(
            value=str(parsed_property_value - parsed_assign_value)
        )

        return True