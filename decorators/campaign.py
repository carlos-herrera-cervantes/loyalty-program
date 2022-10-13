from typing import Callable
from functools import wraps, partial

from sanic.request import Request
from sanic.response import json

from models.bucket import Bucket
from repositories.bucket import BucketRepository
from common.promise import Promise

promise = Promise()


def validate_bucket_id(fn: Callable) -> Callable:
    @wraps(fn)
    async def inner_fn(req: Request, *args: dict, **kwargs: dict) -> Callable:
        bucket_id: str = req.match_info.get('bucket_id')
        bucket: Bucket = await promise.resolve(
            partial(BucketRepository.get_by_id, bucket_id)
        )

        if not bucket:
            return json({
                'message': 'Bucket not found'
            }, status=404)

        req.json['bucket_id'] = bucket_id
        return await fn(req, *args, **kwargs)
    return inner_fn
