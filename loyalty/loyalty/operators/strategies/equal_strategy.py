from interfaces.strategy_interface import Strategy
from models.task import Task
from models.customer import CustomerKeys

class EqualStrategy(Strategy):

    def run_task(self, task: Task, keys: CustomerKeys) -> bool:
        evaluationValue: str = task.evaluationValue
        evaluationValueType: str = task.evaluationValueType
        comparisonValue: str = task.comparisonValue

        if evaluationValueType == 'int':
            return int(evaluationValue) == int(comparisonValue)

        return evaluationValue == comparisonValue