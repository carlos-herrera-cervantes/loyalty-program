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
from decorators.event_code import validate_campaign_id
from decorators.transaction import (
    validate_customer,
    validate_event_code,
    transform_payload
)
from custom_types.pageable import Pageable
from models.transaction import Transaction
from repositories.transaction import TransactionRepository

transaction_router = Blueprint(
    'transaction_router',
    url_prefix=(
        '/organizations/<organization_id>/buckets' +
        '/<bucket_id>/campaigns/<campaign_id>' +
        '/transactions'
    )
)
promise = Promise()


@transaction_router.route('/<pk>', methods=['GET'])
async def get_by_id(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str,
    pk: str
) -> json:
    transaction: Transaction = await promise.resolve(
        partial(TransactionRepository.get_by_id, pk)
    )

    if not transaction:
        return json({'message': 'transaction not found'}, status=404)

    return json({
        'data': loads(transaction.to_json(), object_hook=default)
    })


@transaction_router.route('', methods=['GET'])
@validate_page_attributes
async def get_all(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str
) -> json:
    offset: int = req.args['offset']
    limit: int = req.args['limit']

    fn: partial = partial(
        TransactionRepository.get_all_by_filter,
        {'campaign_id': ObjectId(campaign_id)},
        offset,
        limit
    )
    pageable: Pageable = await promise.resolve(fn)

    return json(loads(pageable.pages))


@transaction_router.route('', methods=['POST'])
@validate_body
@validate_campaign_id
@validate_customer
@validate_event_code
@transform_payload
async def create(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str
) -> json:
    body: dict = req.json
    (saved, err) = await promise.resolve(
        partial(TransactionRepository.create, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })
