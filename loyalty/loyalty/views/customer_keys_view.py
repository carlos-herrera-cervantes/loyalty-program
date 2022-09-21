from rest_framework.viewsets import ModelViewSet

from ..models.customer import CustomerKeys, CustomerKeysSerializer
from ..auth.jwt_authentication import JwtAuthentication


class CustomerKeysView(ModelViewSet):
    """
    A view set that provides the standard actions for CustomerKeys model
    """
    queryset = CustomerKeys.objects.all()
    serializer_class = CustomerKeysSerializer
    authentication_classes = [JwtAuthentication]