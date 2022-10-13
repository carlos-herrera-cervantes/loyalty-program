from mongoengine import *
from mongoengine.signals import pre_save

from datetime import datetime

def validate_name(name: str) -> ValidationError:
    if not len(name):
        raise ValidationError('Name should not be empty')


def validate_description(description: str) -> ValidationError:
    if not len(description):
        raise ValidationError('Description should not be empty')


def validate_operator(operator: str) -> ValidationError:
    if not len(operator):
        raise ValidationError('Operator should not be empty')


class Action(Document):
    name: str = StringField(required=True, validation=validate_name)
    description: str = StringField(required=True, validation=validate_description)
    operator: str = StringField(required=True, validation=validate_operator)
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    meta: dict = {'collection': 'actions'}

    @classmethod
    def pre_save(cls, sender, document, **kwargs) -> None:
        document.updated_at = datetime.utcnow()


pre_save.connect(Action.pre_save, sender=Action)
