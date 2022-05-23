from rest_framework.viewsets import ModelViewSet

from ..models.customer import Customer, CustomerSerializer
from ..auth.jwt_authentication import JwtAuthentication


class CustomerView(ModelViewSet):
    """
    A view set that provides the standard actions for Customer model
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [JwtAuthentication]
