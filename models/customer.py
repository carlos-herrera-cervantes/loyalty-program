from mongoengine import *
from mongoengine.signals import pre_save, post_save, post_delete
from bson.objectid import ObjectId

from datetime import datetime, date

from models.bucket import Bucket


class Customer(Document):
    first_name: str = StringField(required=True)
    last_name: str = StringField(required=True)
    external_user_id: str = StringField(required=True, unique=True)
    birthdate: date = DateField(required=True)
    active_points: int = IntField(default=0)
    expired_points: int = IntField(default=0)
    subtracted_points: int = IntField(default=0)
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    bucket_id: str = ObjectIdField(required=True)
    meta: dict = {'collection': 'customers'}

    @classmethod
    def pre_save(cls, sender, document, **kwargs) -> None:
        document.updated_at = datetime.utcnow()

    @classmethod
    def post_save(cls, sender, document, **kwargs) -> None:
        new: bool = kwargs.get('created')

        if not new:
            return

        bucket_id: str = document.bucket_id
        bucket: Bucket = Bucket.objects.get(id=ObjectId(bucket_id))
        customers: int = bucket.customers + 1 if bucket.customers else 1

        Bucket.objects.filter(id=ObjectId(bucket_id)).update(customers=customers)

    @classmethod
    def post_delete(cls, sender, document, **kwargs) -> None:
        bucket_id: str = document.bucket_id
        bucket: Bucket = Bucket.objects.get(id=ObjectId(bucket_id))
        customers: int = bucket.customers - 1

        Bucket.objects.filter(id=ObjectId(bucket_id)).update(customers=customers)


class CustomerKeys(Document):
    key: str = StringField(required=True)
    value: str = StringField(required=True)
    type: str = StringField(required=True)
    created_at: datetime = DateTimeField(default=datetime.utcnow())
    updated_at: datetime = DateTimeField(default=datetime.utcnow())
    customer_id: str = ObjectIdField(required=True)
    meta: dict = {'collection': 'customer_keys'}


pre_save.connect(Customer.pre_save, sender=Customer)
post_save.connect(Customer.post_save, sender=Customer)
post_delete.connect(Customer.post_delete, sender=Customer)
