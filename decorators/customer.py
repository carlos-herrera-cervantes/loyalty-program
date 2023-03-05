from typing import Callable
from functools import wraps

from sanic.request import Request


def flush_readonly_fields(fn: Callable) -> Callable:
    @wraps(fn)
    def inner_fn(req: Request, *args: dict, **kwargs: dict) -> Callable:
        req.json.pop('bucket_id', None)
        return fn(req, *args, **kwargs)
    return inner_fn
