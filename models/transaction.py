from datetime import datetime

from mongoengine import *
from mongoengine.signals import post_save
from bson.objectid import ObjectId

from enums.transaction_status import TransactionStatus
from enums.task_type import TaskType
from models.event_code import EventCode
from models.task import Task
from operators.strategies.strategy_manager import initialize_manager


class Transaction(Document):
    external_user_id: str = StringField(required=True)
    event_code: str = StringField(required=True)
    status: str = StringField(default=TransactionStatus.PENDING.value)
    payload: str = StringField(default='{}')
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    campaign_id: str = ObjectIdField(required=True)
    meta: dict = {'collection': 'transactions'}

    @classmethod
    def post_save(cls, sender, document, **kwargs) -> None:
        new: bool = kwargs.get('created')

        if not new:
            return

        event_code_name: str = document.event_code
        event_code: EventCode = EventCode.objects.get(name=event_code_name)
        event_code_id: str = event_code.id

        conditions: list[Task] = (Task
            .objects
            .filter(event_code_id=ObjectId(event_code_id), type=TaskType.CONDITION.value))
        actions: list[Task] = (Task
            .objects
            .filter(event_code_id=ObjectId(event_code_id), type=TaskType.ACTION.value))

        for condition in conditions:
            result: bool = initialize_manager(condition.operator).do_action(
                condition,
                document.payload,
                document.external_user_id,
            )

            if not result:
                document.status = TransactionStatus.PROCESSED.value
                document.save()

                return

        for action in actions:
            initialize_manager(action.operator).do_action(
                action,
                document.payload,
                document.external_user_id,
            )

        document.status = TransactionStatus.PROCESSED.value
        document.save()


post_save.connect(Transaction.post_save, sender=Transaction)
