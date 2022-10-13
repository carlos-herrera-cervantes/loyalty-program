from typing import Callable
from functools import wraps, partial

from sanic.request import Request
from sanic.response import json

from models.event_code import EventCode
from repositories.event_code import EventCodeRepository
from common.promise import Promise

promise = Promise()


def validate_event_code_id(fn: Callable) -> Callable:
    @wraps(fn)
    async def inner_fn(req: Request, *args: dict, **kwargs: dict) -> Callable:
        event_code_id: str = req.match_info.get('event_code_id')
        event_code: EventCode = await promise.resolve(
            partial(EventCodeRepository.get_by_id, event_code_id)
        )

        if not event_code:
            return json({
                'message': 'Event code not found'
            }, status=404)

        req.json['event_code_id'] = event_code_id
        return await fn(req, *args, **kwargs)
    return inner_fn
