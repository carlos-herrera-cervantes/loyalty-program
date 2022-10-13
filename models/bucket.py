from mongoengine import *
from mongoengine.signals import pre_save, post_save, post_delete
from bson.objectid import ObjectId

from datetime import datetime

from models.organization import Organization

def validate_name(name: str) -> ValidationError:
    if not len(name):
        raise ValidationError('Name should not be empty')


class Bucket(Document):
    campaigns: int = IntField(default=0)
    customers: int = IntField(default=0)
    name: str = StringField(required=True, validation=validate_name)
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    organization_id: str = ObjectIdField(required=True)
    meta: dict = {'collection': 'buckets'}

    @classmethod
    def pre_save(cls, sender, document, **kwargs) -> None:
        document.updated_at = datetime.utcnow()

    @classmethod
    def post_save(cls, sender, document, **kwargs) -> None:
        organization_id: str = document.organization_id
        organization: Organization = Organization.objects.get(id=ObjectId(organization_id))
        buckets: int = organization.buckets + 1 if organization.buckets else 1

        Organization.objects.filter(id=ObjectId(organization_id)).update(buckets=buckets)

    @classmethod
    def post_delete(cls, sender, document, **kwargs) -> None:
        organization_id: str = document.organization_id
        organization: Organization = Organization.objects.get(id=ObjectId(organization_id))
        buckets: int = organization.buckets - 1

        Organization.objects.filter(id=ObjectId(organization_id)).update(buckets=buckets)


pre_save.connect(Bucket.pre_save, sender=Bucket)
post_save.connect(Bucket.post_save, sender=Bucket)
post_delete.connect(Bucket.post_delete, sender=Bucket)
