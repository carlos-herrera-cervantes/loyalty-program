import logging

from functools import wraps, partial
from typing import Callable
from json import dumps

from sanic.response import json
from sanic.request import Request

from models.customer import Customer
from models.event_code import EventCode
from repositories.customer import CustomerRepository
from repositories.event_code import EventCodeRepository
from common.promise import Promise

logger = logging.getLogger(__name__)
promise = Promise()


def validate_customer(fn: Callable) -> Callable:
    @wraps(fn)
    async def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json | Callable:
        body: dict = req.json
        external_user_id: str = body.get('external_user_id', None)

        customer: Customer | None = await promise.resolve(
            partial(CustomerRepository.get_one, {'external_user_id': external_user_id})
        )

        if customer:
            return await fn(req, *args, **kwargs)

        return json({'message': 'customer not found'}, status=404)
    return inner_fn


def validate_event_code(fn: Callable) -> Callable:
    @wraps(fn)
    async def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json | Callable:
        body: dict = req.json
        event_code_name: str = body.get('event_code', None)

        event_code: EventCode | None = await promise.resolve(
            partial(EventCodeRepository.get_one, {'name': event_code_name})
        )

        if event_code:
            return await fn(req, *args, **kwargs)

        return json({'message': 'event code not found'}, status=404)
    return inner_fn


def transform_payload(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> json | Callable:
        body: dict = req.json
        payload: dict = body.get('payload', {})

        try:
            req.json['payload'] = dumps(payload)
            return fn(req, *args, **kwargs)
        except Exception as e:
            logger.error('Error transforming the payload')
            logger.error(e)

            return json({
                'message': 'an error has ocurred processing the payload'
            }, status=400)
    return inner_fn
