from datetime import datetime

from mongoengine import *

def validate_name(name: str) -> ValidationError:
    if not len(name):
        raise ValidationError('Name should not be empty')


class Organization(Document):
    name:str = StringField(required=True, validation=validate_name)
    buckets: int = IntField(default=0)
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    meta: dict = {'collection': 'organizations'}
