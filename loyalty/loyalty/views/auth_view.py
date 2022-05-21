from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from bcrypt import checkpw
from django.conf import settings
from json import loads
import datetime
import jwt


from ..models.user import User, UserSerializer
from ..models.customer import Customer, CustomerSerializer
from ..models.access_token import AccessToken
from ..models.bucket import Bucket
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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4),
            },
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        AccessToken.objects.create(**{'user': email, 'token': token})
        response: any = {'status': True, 'accessToken': token}

        return Response(response, content_type='application/json')

    def logout(self, request: Request) -> Response:
        access_token: str = request.headers.get('authorization')

        if not access_token:
            lang: str = request.headers.get('Accept-Language', 'en')

            return Response({
                'status': False,
                'code': 'Forbidden',
                'message': initialize_manager(lang).translate('Forbidden'),
            }, status=HTTP_403_FORBIDDEN)

        AccessToken.objects.filter(token=access_token.split(' ').pop()).delete()

        return Response(status=HTTP_204_NO_CONTENT)

    def sign_up_user(self, request: Request) -> Response:
        serializer: UserSerializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

        created = User.objects.create(**request.data)
        json = JSONRenderer().render(UserSerializer(created).data)

        return Response(loads(json), status=HTTP_201_CREATED)

    def sign_up_customer(self, request: Request) -> Response:
        serializer: CustomerSerializer = CustomerSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

        bucket: Bucket = Bucket.objects.get(id=request.data['bucket'])

        request.data.pop('bucket')
        
        created = Customer.objects.create(**request.data, bucket=bucket)
        json = JSONRenderer().render(CustomerSerializer(created).data)

        return Response(loads(json), status=HTTP_201_CREATED)
