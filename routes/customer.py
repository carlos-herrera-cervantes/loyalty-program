from json import loads
from functools import partial

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request
from bson.objectid import ObjectId

from common.serializer.document import default
from common.promise import Promise
from decorators.pageable import validate_page_attributes
from decorators.common import validate_body
from decorators.campaign import validate_bucket_id
from decorators.customer import flush_readonly_fields
from custom_types.pageable import Pageable
from models.customer import Customer
from repositories.customer import CustomerRepository

customer_router = Blueprint(
    'customer_router',
    url_prefix='/organizations/<organization_id>/buckets/<bucket_id>/customers'
)
promise = Promise()


@customer_router.route('/<pk>', methods=['GET'])
async def get_by_id(
    req: Request,
    organization_id: str,
    bucket_id: str,
    pk: str
) -> json:
    customer: Customer = await promise.resolve(
        partial(CustomerRepository.get_by_id, pk)
    )

    if not customer:
        return json({'message': 'customer not found'}, status=404)

    return json({
        'data': loads(customer.to_json(), object_hook=default)
    })


@customer_router.route('', methods=['GET'])
@validate_page_attributes
async def get_all(req: Request, organization_id: str, bucket_id: str) -> json:
    offset: int = req.args['offset']
    limit: int = req.args['limit']

    fn: partial = partial(
        CustomerRepository.get_all_by_filter,
        {'bucket_id': ObjectId(bucket_id)},
        offset,
        limit
    )
    pageable: Pageable = await promise.resolve(fn)

    return json(loads(pageable.pages))


@customer_router.route('', methods=['POST'])
@validate_body
@validate_bucket_id
async def create(req: Request, organization_id: str, bucket_id: str) -> json:
    body: dict = req.json
    (saved, err) = await promise.resolve(
        partial(CustomerRepository.create, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })


@customer_router.route('/<pk>', methods=['PATCH'])
@validate_body
@flush_readonly_fields
async def update_by_id(
    req: Request,
    organization_id: str,
    bucket_id: str,
    pk: str
) -> json:
    body: dict = req.json
    (saved, err) = await promise.resolve(
        partial(CustomerRepository.update_by_id, pk, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })


@customer_router.route('/<pk>', methods=['DELETE'])
async def delete_by_id(
    req: Request,
    organization_id: str,
    bucket_id: str,
    pk: str
) -> json:
    await promise.resolve(partial(
        CustomerRepository.delete_by_id, pk)
    )
    return json(None, status=204)
