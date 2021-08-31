from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.renderers import JSONRenderer
from json import loads

from ..models.user import User, UserSerializer
from ..auth.jwt_authentication import JwtAuthentication

class UserView(ModelViewSet):
    """
    A view set that provides the standard actions for User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JwtAuthentication]

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            result = User.objects.create(**request.data)
            json = JSONRenderer().render(UserSerializer(result).data)

            return Response(loads(json), content_type='application/json')

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
