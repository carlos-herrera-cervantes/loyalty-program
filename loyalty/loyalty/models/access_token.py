from django.db import models
import uuid

class AccessToken(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4
    )
    token = models.CharField(max_length=300)
    user = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loyalty_access_token'
        ordering = ['-created_at']
