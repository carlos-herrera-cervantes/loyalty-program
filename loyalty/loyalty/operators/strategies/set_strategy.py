from interfaces.strategy_interface import Strategy
from models.task import Task
from models.customer import CustomerKeys

class SetStrategy(Strategy):

    def run_task(self, task: Task, keys: CustomerKeys) -> bool:
        customerProperty: str = task.customerProperty
        assignValue: str = task.assignValue
        assignValueType: str = task.assignValueType

        CustomerKeys.objects.create({
            'key': customerProperty,
            'value': assignValue,
            'type': assignValueType,
        })

        return True