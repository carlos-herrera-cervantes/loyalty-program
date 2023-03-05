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
from custom_types.pageable import Pageable
from models.event_code import EventCode
from repositories.event_code import EventCodeRepository

event_code_router = Blueprint(
    'event_code_router',
    url_prefix='/organizations/<organization_id>/buckets/<bucket_id>/campaigns/<campaign_id>/event-codes'
)


@event_code_router.route('/<pk>', methods=['GET'])
async def get_by_id(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str,
    pk: str
) -> json:
    event_code: EventCode = await Promise.resolve(
        partial(EventCodeRepository.get_by_id, pk)
    )

    if not event_code:
        return json({'message': 'event code not found'}, status=404)

    return json({
        'data': loads(event_code.to_json(), object_hook=default)
    })


@event_code_router.route('', methods=['GET'])
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
        EventCodeRepository.get_all_by_filter,
        {'campaign_id': ObjectId(campaign_id)},
        offset,
        limit
    )
    pageable: Pageable = await Promise.resolve(fn)

    return json(loads(pageable.pages))


@event_code_router.route('', methods=['POST'])
@validate_body
@validate_campaign_id
async def create(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str
) -> json:
    body: dict = req.json
    (saved, err) = await Promise.resolve(
        partial(EventCodeRepository.create, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })


@event_code_router.route('/<pk>', methods=['DELETE'])
async def delete_by_id(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str,
    pk: str
) -> json:
    await Promise.resolve(partial(
        EventCodeRepository.delete_by_id, pk)
    )
    return json(None, status=204)
