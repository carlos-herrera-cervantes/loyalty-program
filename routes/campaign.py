from json import loads
from functools import partial

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request
from bson.objectid import ObjectId

from common.serializer.document import default
from common.promise import Promise
from decorators.pageable import validate_page_attributes
from decorators.campaign import validate_bucket_id
from decorators.common import validate_body
from custom_types.pageable import Pageable
from models.campaign import Campaign
from repositories.campaign import CampaignRepository

campaign_router = Blueprint(
    'campaign_router',
    url_prefix='/organizations/<organization_id>/buckets/<bucket_id>/campaigns'
)


@campaign_router.route('/<pk>', methods=['GET'])
async def get_by_id(req: Request, organization_id: str, bucket_id: str, pk: str) -> json:
    campaign: Campaign = await Promise.resolve(
        partial(CampaignRepository.get_by_id, pk)
    )

    if not campaign:
        return json({'message': 'campaign not found'}, status=404)

    return json({
        'data': loads(campaign.to_json(), object_hook=default)
    })


@campaign_router.route('', methods=['GET'])
@validate_page_attributes
async def get_all(req: Request, organization_id: str, bucket_id: str) -> json:
    offset: int = req.args['offset']
    limit: int = req.args['limit']

    fn: partial = partial(
        CampaignRepository.get_all_by_filter,
        {'bucket_id': ObjectId(bucket_id)},
        offset,
        limit
    )
    pageable: Pageable = await Promise.resolve(fn)

    return json(loads(pageable.pages))


@campaign_router.route('', methods=['POST'])
@validate_body
@validate_bucket_id
async def create(req: Request, organization_id: str, bucket_id: str) -> json:
    body: dict = req.json
    (saved, err) = await Promise.resolve(
        partial(CampaignRepository.create, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })


@campaign_router.route('/<pk>', methods=['DELETE'])
async def delete_by_id(req: Request, organization_id: str, bucket_id: str, pk: str) -> json:
    await Promise.resolve(partial(
        CampaignRepository.delete_by_id, pk)
    )
    return json(None, status=204)
