from functools import wraps
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from json import dumps

import logging

from ..localization.locales.strategies.strategy_manager import initialize_manager
from ..models.customer import Customer
from ..models.event_code import EventCode

logger = logging.getLogger(__name__)

def validate_customer(fn):
    """
    Validates if customer exists on database
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            Customer.objects.get(external_user_id=args[1].data['external_user_id'])
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error('Error when finding a customer')
            logger.error(e)

            lang: str = args[1].headers.get('Accept-Language', 'en')

            return Response({
                'status': False,
                'code': 'CustomerNotFound',
                'message': initialize_manager(lang).translate('CustomerNotFound'),
            }, status=HTTP_404_NOT_FOUND)
    return inner

def validate_event_code(fn):
    """
    Validates if event code exists on database
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            EventCode.objects.get(name=args[1].data['event_code'])
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error('Error when finding a event code')
            logger.error(e)

            lang: str = args[1].headers.get('Accept-Language', 'en')

            return Response({
                'status': False,
                'code': 'EventCodeNotFound',
                'message': initialize_manager(lang).translate('EventCodeNotFound'),
            }, status=HTTP_404_NOT_FOUND)
    return inner

def transform_payload(fn):
    """
    Transforms the payload object to string
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            payload: dict = args[1].data['payload']
            args[1].data['payload'] = dumps(payload)

            return fn(*args, **kwargs)
        except Exception as e:
            logger.error('Error when transforming a payload')
            logger.error(e)

            lang: str = args[1].headers.get('Accept-Language', 'en')

            return Response({
                'status': False,
                'code': 'SerializeError',
                'message': initialize_manager(lang).translate('SerializeError'),
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
    return inner