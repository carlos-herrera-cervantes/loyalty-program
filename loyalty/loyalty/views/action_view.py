from rest_framework.viewsets import ModelViewSet

from ..models.action import Action, ActionSerializer
from ..auth.jwt_authentication import JwtAuthentication


class ActionView(ModelViewSet):
    """
    A view set that provides the standard actions for Operation model
    """
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    authentication_classes = [JwtAuthentication]
