from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.permissions import AllowAny
from bcrypt import checkpw
from django.conf import settings
import datetime
import jwt

from ..models.user import User
from ..models.access_token import AccessToken
from ..localization.locales.strategies.strategy_manager import initialize_manager

class LoginView(APIView):
    """
    A view that provides the access token mechanism to authenticate a user
    """
    def post(self, request: Request) -> Response:
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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4),
            },
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        AccessToken.objects.create(**{'user': email, 'token': token})
        response: any = {'status': True, 'accessToken': token}

        return Response(response, content_type='application/json')
