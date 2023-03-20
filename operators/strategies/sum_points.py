import logging

from operators.interfaces.strategy import Strategy
from models.task import Task
from models.customer import Customer

logger = logging.getLogger(__name__)

class SumPointsStrategy(Strategy):

    def run_task(self, task: Task, payload: str, external_user_id: str) -> bool:
        try:
            customer: Customer = (Customer
                .objects
                .get(external_user_id=external_user_id))

            accumulator: int = int(task.assign_value) + customer.active_points
            (Customer
                .objects
                .filter(external_user_id=external_user_id)
                .update(active_points=accumulator))

            return True
        except Exception as e:
            logger.error('Error running task for SumPointsStrategy')
            logger.error(e)
            return False
