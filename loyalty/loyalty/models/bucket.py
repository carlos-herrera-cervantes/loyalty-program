from django.db import models
from django.db.models.signals import post_save, post_delete
from rest_framework.serializers import ModelSerializer
import uuid

from .organization import Organization


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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table = 'bucket'
        ordering = ['-created_at']

    @classmethod
    def post_save(cls, sender, instance, **kwargs) -> None:
        """
        Executes after save a bucket
        """
        organization_id: str = instance.organization.id
        organization: Organization = Organization.objects.get(id=organization_id)
        buckets: int = organization.buckets + 1 if organization.buckets else 1

        Organization.objects.filter(id=organization_id).update(buckets=buckets)

    @classmethod
    def post_delete(cls, sender, instance, **kwargs):
        """
        Executes after deletes a bucket
        """
        organization_id: str = instance.organization.id
        organization: Organization = Organization.objects.get(id=organization_id)

        Organization.objects.filter(id=organization_id).update(buckets=organization.buckets - 1)


post_save.connect(Bucket.post_save, sender=Bucket)
post_delete.connect(Bucket.post_delete, sender=Bucket)


class BucketSerializer(ModelSerializer):

    class Meta:
        model = Bucket
        fields = [
            'id',
            'name',
            'campaigns',
            'customers',
            'organization',
            'created_at',
            'updated_at',
        ]
