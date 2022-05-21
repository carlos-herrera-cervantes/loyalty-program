from typing import Tuple
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
import logging

from ..models.user import User
from ..models.access_token import AccessToken

logger = logging.getLogger(__name__)

class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Tuple[User, None]:
        authorization_header: str = request.headers.get('authorization')

        if not authorization_header:
            raise AuthenticationFailed

        access_token_header: str = authorization_header.split(' ').pop()

        try:
            access_token: AccessToken = AccessToken.objects.get(token=access_token_header)
        except Exception as e:
            logger.error('Error when finding the current access token - Login Middleware: ')
            logger.error(e)
            raise AuthenticationFailed

        if not access_token:
            raise AuthenticationFailed

        try:
            payload: dict = jwt.decode(
                access_token_header,
                settings.SECRET_KEY,
                algorithms=['HS256'],
            )

            email: str = payload.get('email')
            user: User = User.objects.get(email=email)

            return user, None
        except Exception as e:
            logger.error('Error when decoding JWT - Login Middleware: ')
            logger.error(e)
            AccessToken.objects.filter(token=access_token_header).delete()

            raise AuthenticationFailed
