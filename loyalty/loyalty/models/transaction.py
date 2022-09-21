from django.db import models
from django.db.models.signals import post_save
from rest_framework.serializers import ModelSerializer, ValidationError
import uuid

from .campaign import Campaign
from .task import Task, TaskType
from .event_code import EventCode
from .transactions_status import TransactionStatus
from ..operators.strategies.strategy_manager import initialize_manager


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    external_user_id = models.CharField(max_length=100)
    event_code = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default=TransactionStatus.PENDING.value)
    payload = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    class Meta:
        db_table = 'transaction'
        ordering = ['-created_at']

    @classmethod
    def post_save(cls, sender, instance, **kwargs) -> None:
        """
        Executes after save the transaction
        """
        new = kwargs.get('created')
        
        if not new:
            return

        event_code: str = instance.event_code
        event_codes: list = EventCode.objects.filter(name=event_code).values('id')
        
        conditions: list = Task.objects.all().filter(
            event_code=event_codes[0]['id'],
            type=TaskType.CONDITION.value,
        )
        actions: list = Task.objects.all().filter(
            event_code=event_codes[0]['id'],
            type=TaskType.ACTION.value,
        )

        for condition in conditions:
            result: bool = initialize_manager(condition.operator).do_action(
                condition,
                instance.payload,
                instance.external_user_id,
            )

            if not result:
                instance.status = TransactionStatus.PROCESSED.value
                instance.save()

                return

        for action in actions:
            initialize_manager(action.operator).do_action(
                action,
                instance.payload,
                instance.external_user_id,
            )

        instance.status = TransactionStatus.PROCESSED.value
        instance.save()


post_save.connect(Transaction.post_save, sender=Transaction)


class TransactionSerializer(ModelSerializer):

    @staticmethod
    def validate_campaign(self, campaign: Campaign):
        campaign: Campaign = Campaign.objects.get(id=campaign.id)
        
        if not campaign.active:
            raise ValidationError('Expired campaigns cannot be assigned')

        return campaign

    class Meta:
        model = Transaction
        fields = [
            'id',
            'external_user_id',
            'event_code',
            'campaign',
            'created_at',
            'updated_at',
            'status',
            'payload',
        ]
