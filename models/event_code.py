import re
from datetime import datetime
from difflib import Match

from mongoengine import *

def validate_name(name: str) -> ValidationError:
    if not len(name):
        raise ValidationError('Name should not be empty')

    match: Match[str] | None = re.search(r'(?=\S*^[^-])([a-z-]+$)', name)

    if not match:
        message: str = (
            'Event code name should be a string in lower case separated by hyphens'
        )
        raise ValidationError(message)


class EventCode(Document):
    name: str = StringField(required=True, validation=validate_name)
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    campaign_id: str = ObjectIdField(required=True)
    meta: dict = {'collection': 'event_codes'}
