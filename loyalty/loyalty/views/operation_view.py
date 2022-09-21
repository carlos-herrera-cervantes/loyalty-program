from rest_framework.viewsets import ModelViewSet

from ..models.operation import Operation, OperationSerializer
from ..auth.jwt_authentication import JwtAuthentication


class OperationView(ModelViewSet):
    """
    A view set that provides the standard actions for Operation model
    """
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    authentication_classes = [JwtAuthentication]
