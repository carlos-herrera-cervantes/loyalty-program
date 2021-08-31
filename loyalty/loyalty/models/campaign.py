from django.db import models
from rest_framework.serializers import ModelSerializer
import uuid

class Campaign(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class CampaignSerializer(ModelSerializer):

    class Meta:
        model = Campaign
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
            'created_at',
            'updated_at',
        ]
