from json import loads
from functools import partial

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request
from bson.objectid import ObjectId

from common.serializer.document import default
from common.promise import Promise
from decorators.pageable import validate_page_attributes
from decorators.bucket import validate_organization_id
from decorators.common import validate_body
from custom_types.pageable import Pageable
from models.bucket import Bucket
from repositories.bucket import BucketRepository

bucket_router = Blueprint(
    'bucket_router',
    url_prefix='/organizations/<organization_id>/buckets'
)


@bucket_router.route('/<pk>', methods=['GET'])
async def get_by_id(req: Request, organization_id: str, pk: str) -> json:
    bucket: Bucket = await Promise.resolve(
        partial(BucketRepository.get_by_id, pk)
    )

    if not bucket:
        return json({'message': 'organization not found'}, status=404)

    return json({
        'data': loads(bucket.to_json(), object_hook=default)
    })


@bucket_router.route('', methods=['GET'])
@validate_page_attributes
async def get_all(req: Request, organization_id: str) -> json:
    offset: int = req.args['offset']
    limit: int = req.args['limit']

    fn: partial = partial(
        BucketRepository.get_all_by_filter,
        {'organization_id': ObjectId(organization_id)},
        offset,
        limit
    )
    pageable: Pageable = await Promise.resolve(fn)

    return json(loads(pageable.pages))


@bucket_router.route('', methods=['POST'])
@validate_body
@validate_organization_id
async def create(req: Request, organization_id: str) -> json:
    body: dict = req.json
    (saved, err) = await Promise.resolve(
        partial(BucketRepository.create, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })


@bucket_router.route('/<pk>', methods=['DELETE'])
async def delete_by_id(req: Request, organization_id: str, pk: str) -> json:
    await Promise.resolve(partial(
        BucketRepository.delete_by_id, pk)
    )
    return json(None, status=204)
