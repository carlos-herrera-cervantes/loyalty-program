from typing import Tuple
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
import logging

from ..models.user import User

logger = logging.getLogger(__name__)

class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Tuple(User, None):
        authorization_header: str = request.headers.get('authorization')

        if not authorization_header:
            raise AuthenticationFailed

        try:
            payload: dict = jwt.decode(
                authorization_header.split(' ').pop(),
                settings.SECRET_KEY,
                algorithms=['HS256'],
            )

            email: str = payload.get('email')
            user: User = User.objects.get(email=email)

            return user, None
        except Exception as e:
            logger.error('Error when decoding JWT - Login Middleware: ', e)
            raise AuthenticationFailed
