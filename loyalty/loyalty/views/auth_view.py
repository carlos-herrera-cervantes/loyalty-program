from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from bcrypt import checkpw
from django.conf import settings
import datetime
import jwt

from ..models.user import User
from ..models.access_token import AccessToken
from ..localization.locales.strategies.strategy_manager import initialize_manager

class AuthView(GenericViewSet, RetrieveModelMixin):
    """
    A view that provides the access token mechanism to authenticate a user
    """

    def sign_in(self, request: Request) -> Response:
        email: str = request.data['email']
        lang: str = request.headers.get('Accept-Language', 'en')

        entered_password: str = request.data['password']
        user: User = User.objects.get(email=email)

        if not checkpw(entered_password.encode('utf-8'), user.password.encode('utf-8')):
            return Response({
                'status': False,
                'code': 'InvalidCredentials',
                'message': initialize_manager(lang).translate('InvalidCredentials'),
            }, content_type='application/json', status=HTTP_403_FORBIDDEN)

        token: str = jwt.encode(
            {
                'id': str(user.id),
                'email': email,
                'role': user.roles,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=4),
            },
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        AccessToken.objects.create(**{'user': email, 'token': token})
        response: any = {'status': True, 'accessToken': token}

        return Response(response, content_type='application/json')

    def logout(self, request: Request) -> Response:
        access_token: str = request.headers.get('autorization')

        if not access_token:
            lang: str = request.headers.get('Accept-Language', 'en')

            return Response({
                'status': False,
                'code': 'Forbidden',
                'message': initialize_manager(lang).translate('Forbidden'),
            }, status=HTTP_403_FORBIDDEN)

        AccessToken.objects.filter(token=access_token).delete()

        return Response(status=HTTP_204_NO_CONTENT)
