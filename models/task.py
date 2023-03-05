from datetime import datetime

from mongoengine import *

from enums.task_type import TaskType

def validate_task_type(type: str) -> ValidationError:
    if type == TaskType.ACTION.value or type == TaskType.CONDITION.value:
        return

    raise ValidationError('Task type not valid. Only: action or condition')


class Task(Document):
    operator: str = StringField(required=True)
    evaluation_property: str = StringField()
    evaluation_value_type: str = StringField()
    comparison_value: str = StringField()
    comparison_value_type: str = StringField()
    assign_value: str = StringField()
    assign_value_type: str = StringField()
    customer_property: str = StringField()
    type: str = StringField(required=True, validation=validate_task_type)
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    event_code_id: str = ObjectIdField(required=True)
    meta: dict = {'collection': 'tasks'}
