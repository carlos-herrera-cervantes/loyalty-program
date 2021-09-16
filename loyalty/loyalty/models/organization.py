from django.db import models
from rest_framework.serializers import ModelSerializer
import uuid

class Organization(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    name = models.CharField(max_length=100)
    buckets = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class OrganizationSerializer(ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'buckets',
            'created_at',
            'updated_at',
        ]