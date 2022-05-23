from django.db import models
from django.db.models.signals import post_save, post_delete
from rest_framework.serializers import ModelSerializer
import uuid

from .bucket import Bucket


class Customer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    external_user_id = models.CharField(max_length=100, unique=True)
    birthdate = models.DateField()
    active_points = models.IntegerField(default=0)
    expired_points = models.IntegerField(default=0)
    subtracted_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)

    class Meta:
        db_table = 'customer'
        ordering = ['-created_at']

    @classmethod
    def post_save(cls, sender, instance, **kwargs) -> None:
        """
        Executes after save the customer
        """
        bucket_id: str = instance.bucket.id
        bucket: Bucket = Bucket.objects.get(id=bucket_id)
        customers: int = bucket.customers + 1 if bucket.customers else 1

        Bucket.objects.filter(id=bucket_id).update(customers=customers)

    @classmethod
    def post_delete(cls, sender, instance, **kwargs):
        """
        Executes after delete the customer
        """
        bucket_id: str = instance.bucket.id
        bucket: Bucket = Bucket.objects.get(id=bucket_id)

        Bucket.objects.filter(id=bucket_id).update(customers=bucket.customers - 1)


post_save.connect(Customer.post_save, sender=Customer)
post_delete.connect(Customer.post_delete, sender=Customer)


class CustomerKeys(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )
    key = models.CharField(max_length=100)
    value = models.TextField()
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='keys')

    class Meta:
        db_table = 'customer_keys'
        ordering = ['-created_at']


class CustomerKeysSerializer(ModelSerializer):

    class Meta:
        model = CustomerKeys
        fields = [
            'id',
            'key',
            'value',
            'type',
            'customer',
            'created_at',
            'updated_at',
        ]


class CustomerSerializer(ModelSerializer):
    keys = CustomerKeysSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id',
            'first_name',
            'last_name',
            'external_user_id',
            'birthdate',
            'created_at',
            'updated_at',
            'keys',
            'bucket',
            'active_points',
            'expired_points',
            'subtracted_points',
        ]
