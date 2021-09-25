from interfaces.strategy_interface import Strategy
from models.task import Task
from models.customer import CustomerKeys

class AddStrategy(Strategy):

    def run_task(self, task: Task, keys: CustomerKeys) -> bool:
        assignValue: str = task.assignValue
        parsedAssignValue: int = int(assignValue)
        parsedPropertyValue: int = int(keys.value)

        CustomerKeys.objects.filter(id=keys.id).update(
            key=str(parsedAssignValue + parsedPropertyValue)
        )

        return True