import logging

from operators.interfaces.strategy import Strategy
from models.task import Task
from models.customer import Customer

logger = logging.getLogger(__name__)

class SubtractPointsStrategy(Strategy):

    def run_task(self, task: Task, payload: str, external_user_id: str) -> bool:
        try:
            customer: Customer = Customer.objects.get(external_user_id=external_user_id)

            accumulator: int = customer.active_points - int(task.assign_value)
            accumulated_subtraction: int = int(task.assign_value) + customer.subtracted_points

            (Customer
                .objects
                .filter(external_user_id=external_user_id)
                .update(active_points=accumulator, subtracted_points=accumulated_subtraction))

            return True
        except Exception as e:
            logger.error('Error running task for SubtractPointsStrategy')
            logger.error(e)
            return False
