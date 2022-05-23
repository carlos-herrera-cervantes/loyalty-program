from django.db import models
from django.db.models.signals import post_save
from rest_framework.serializers import ModelSerializer
import uuid
import bcrypt

from .roles import Role


class User(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    roles = models.CharField(max_length=100, default=Role.SUPER_ADMIN.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'
        ordering = ['-created_at']

    @classmethod
    def post_save(cls, sender, instance, **kwargs) -> None:
        """
        Executes after save the user
        """
        new: bool = kwargs.get('created')

        if not new:
            return

        password = instance.password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        instance.password = hashed_password.decode('utf-8')
        instance.save()


post_save.connect(User.post_save, sender=User)


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'roles',
            'created_at',
            'updated_at',
        ]
