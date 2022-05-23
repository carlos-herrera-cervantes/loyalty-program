from rest_framework.viewsets import ModelViewSet

from ..models.user import User, UserSerializer
from ..auth.jwt_authentication import JwtAuthentication


class UserView(ModelViewSet):
    """
    A view set that provides the standard actions for User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JwtAuthentication]
