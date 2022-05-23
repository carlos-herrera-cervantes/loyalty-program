from django.db import models
from rest_framework.serializers import ModelSerializer
from enum import Enum
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
    evaluation_value = models.CharField(max_length=100, null=True)
    evaluation_value_type = models.CharField(max_length=20, null=True)
    comparison_value = models.CharField(max_length=100, null=True)
    comparison_value_type = models.CharField(max_length=20, null=True)
    assign_value = models.CharField(max_length=100, null=True)
    assign_value_type = models.CharField(max_length=20, null=True)
    customer_property = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    event_code = models.ForeignKey(EventCode, on_delete=models.CASCADE)

    class Meta:
        db_table = 'task'
        ordering = ['-created_at']


class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id',
            'operator',
            'evaluation_value',
            'evaluation_value_type',
            'comparison_value',
            'comparison_value_type',
            'assign_value',
            'assign_value_type',
            'customer_property',
            'type',
            'event_code',
            'created_at',
            'updated_at',
        ]


class TaskType(Enum):
    ACTION = 'action'
    CONDITION = 'condition'
