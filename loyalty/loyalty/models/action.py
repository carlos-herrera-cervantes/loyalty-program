from django.db import models
from rest_framework.serializers import ModelSerializer
import uuid

class Action(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, null=True)
    operator = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class ActionSerializer(ModelSerializer):

    class Meta:
        model = Action
        fields = [
            'id',
            'name',
            'description',
            'operator',
            'created_at',
            'updated_at',
        ]