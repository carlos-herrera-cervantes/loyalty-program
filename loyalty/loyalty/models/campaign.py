from django.db import models
from django.db.models.signals import post_save, post_delete
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
import uuid

from .bucket import Bucket

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
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    active = models.BooleanField()

    class Meta:
        db_table = 'campaign'
        ordering = ['-created_at']

    @classmethod
    def post_save(cls, sender, instance, **kwargs) -> None:
        """
        Executes after save the campaign
        """
        bucket_id: str = instance.bucket.id
        bucket: Bucket = Bucket.objects.get(id=bucket_id)
        campaigns: int = bucket.campaigns + 1 if bucket.campaigns else 1

        Bucket.objects.filter(id=bucket_id).update(campaigns=campaigns)

    @classmethod
    def post_delete(cls, sender, instance, **kwargs):
        """
        Executes after delete the campaign
        """
        bucket_id: str = instance.bucket.id
        bucket: Bucket = Bucket.objects.get(id=bucket_id)

        Bucket.objects.filter(id=bucket_id).update(campaigns=bucket.campaigns - 1)

post_save.connect(Campaign.post_save, sender=Campaign)
post_delete.connect(Campaign.post_delete, sender=Campaign)

class CampaignSerializer(ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

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
            'bucket',
            'active',
        ]
