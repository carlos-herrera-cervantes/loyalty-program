from django.db import models
from rest_framework.serializers import ModelSerializer
import uuid

class Bucket(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )
    campaigns = models.IntegerField(null=True)
    customers = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class BucketSerializer(ModelSerializer):

    class Meta:
        model = Bucket
        fields = [
            'id',
            'name',
            'campaigns',
            'customers',
            'created_at',
            'updated_at',
        ]