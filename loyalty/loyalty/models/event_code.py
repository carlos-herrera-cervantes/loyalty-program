from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
import uuid

from .campaign import Campaign

class EventCode(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    class Meta:
        db_table = 'event_code'
        ordering = ['-created_at']

class EventCodeSerializer(ModelSerializer):

    class Meta:
        model = EventCode
        fields = [
            'id',
            'name',
            'campaign',
            'created_at',
            'updated_at',
        ]