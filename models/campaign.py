from datetime import datetime

from mongoengine import *
from mongoengine.signals import pre_save, post_save, post_delete
from bson.objectid import ObjectId

from models.bucket import Bucket


class Campaign(Document):
    name: str = StringField(required=True)
    description: str = StringField(required=True)
    start_date: datetime = DateTimeField(required=True)
    end_date: datetime = DateTimeField(required=True)
    created_at: datetime = DateTimeField(default=datetime.utcnow)
    updated_at: datetime = DateTimeField(default=datetime.utcnow)
    active: bool = BooleanField(default=True)
    bucket_id: str = ObjectIdField(required=True)
    meta: dict = {'collection': 'campaigns'}

    def clean(self) -> None:
        now: datetime = datetime.utcnow()

        if not self.name or not len(self.name):
            raise ValidationError('Name should not be empty')

        if not self.description or not len(self.description):
            raise ValidationError('Description should not be empty')

        if not self.start_date or datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S') < now:
            raise ValidationError('Start date is not valid')

        if (
            not self.end_date or
            datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S') < now or
            datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S') < datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
        ):
            raise ValidationError('End date is not valid')

    @classmethod
    def pre_save(cls, sender, document, **kwargs) -> None:
        document.updated_at = datetime.utcnow()

    @classmethod
    def post_save(cls, sender, document, **kwargs) -> None:
        bucket_id: str = document.bucket_id
        bucket: Bucket = Bucket.objects.get(id=ObjectId(bucket_id))
        campaigns: int = bucket.campaigns + 1 if bucket.campaigns else 1

        Bucket.objects.filter(id=ObjectId(bucket_id)).update(campaigns=campaigns)

    @classmethod
    def post_delete(cls, sender, document, **kwargs) -> None:
        bucket_id: str = document.bucket_id
        bucket: Bucket = Bucket.objects.get(id=ObjectId(bucket_id))
        campaigns: int = bucket.campaigns - 1

        Bucket.objects.filter(id=ObjectId(bucket_id)).update(campaigns=campaigns)


pre_save.connect(Campaign.pre_save, sender=Campaign)
post_save.connect(Campaign.post_save, sender=Campaign)
post_delete.connect(Campaign.post_delete, sender=Campaign)
