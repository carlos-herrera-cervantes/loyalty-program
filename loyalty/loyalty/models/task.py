from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
import uuid

from .event_code import EventCode

class Task(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    operator = models.CharField(max_length=10)
    evaluationValue = models.CharField(max_length=100, null=True)
    evaluationValueType = models.CharField(max_length=20, null=True)
    comparisonValue = models.CharField(max_length=100, null=True)
    comparisonValueType = models.CharField(max_length=20, null=True)
    assignValue = models.CharField(max_length=100, null=True)
    assignValueType = models.CharField(max_length=20, null=True)
    customerProperty = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    event_code = models.ForeignKey(EventCode, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id',
            'operator',
            'evaluationValue',
            'evaluationValueType',
            'comparisonValue',
            'comparisonValueType',
            'assignValue',
            'assignValueType',
            'customerProperty',
            'type',
            'event_code',
            'created_at',
            'updated_at',
        ]