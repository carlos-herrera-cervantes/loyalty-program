from typing import Callable
from functools import wraps

from sanic.request import Request


def validate_page_attributes(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> Callable:
        offset: int = int(req.args.get('offset', '0'))
        limit: int = int(req.args.get('limit', '10'))

        req.args['offset'] = offset if offset > -1 else 0
        req.args['limit'] = limit if limit > 0 and limit < 50 else 10
        
        return fn(req, *args, **kwargs)
    return inner_fn
