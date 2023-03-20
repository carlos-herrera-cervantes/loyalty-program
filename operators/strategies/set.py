import logging

from operators.interfaces.strategy import Strategy
from models.task import Task
from models.customer import CustomerKeys, Customer

logger = logging.getLogger(__name__)

class SetStrategy(Strategy):

    def run_task(self, task: Task, payload: str, external_user_id: str) -> bool:
        try:
            customer: Customer = (Customer
                .objects
                .get(external_user_id=external_user_id))

            CustomerKeys.objects.create({
                'key': task.customer_property,
                'value': task.assign_value,
                'type': task.assign_value_type,
                'customer': customer.id,
            })

            return True
        except Exception as e:
            logger.error('Error running task for SetStrategy')
            logger.error(e)
            return False
