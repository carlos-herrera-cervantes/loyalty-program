from interfaces.strategy_interface import Strategy
from models.task import Task
from models.customer import CustomerKeys

class GreaterThanEqualStrategy(Strategy):

    def run_task(self, task: Task, keys: CustomerKeys) -> bool:
        evaluationValue: str = task.evaluationValue
        comparisonValue: str = task.comparisonValue

        return evaluationValue >= comparisonValue