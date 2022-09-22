from mongoengine import *

from datetime import datetime


class Operation(Document):
    name: str = StringField(required=True)
    description: str = StringField(required=True)
    operator: str = StringField(required=True)
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    meta: dict = {'collection': 'operations'}
