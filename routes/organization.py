from json import loads
from functools import partial

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request

from common.serializer.document import default
from common.promise import Promise
from models.organization import Organization
from custom_types.pageable import Pageable
from decorators.pageable import validate_page_attributes
from decorators.common import validate_body
from repositories.organization import OrganizationRepository

organization_router = Blueprint(
    'organization_router',
    url_prefix='/organizations'
)


@organization_router.route('/<pk>', methods=['GET'])
async def get_by_id(req: Request, pk: str) -> json:
    organization: Organization = await Promise.resolve(
        partial(OrganizationRepository.get_by_id, pk)
    )

    if not organization:
        return json({'message': 'organization not found'}, status=404)

    return json({
        'data': loads(organization.to_json(), object_hook=default)
    })


@organization_router.route('', methods=['GET'])
@validate_page_attributes
async def get_all(req: Request) -> json:
    offset: int = req.args['offset']
    limit: int = req.args['limit']

    pageable: Pageable = await Promise.resolve(
        partial(OrganizationRepository.get_all, offset, limit)
    )

    return json(loads(pageable.pages))


@organization_router.route('', methods=['POST'])
@validate_body
async def create(req: Request) -> json:
    body: dict = req.json
    (saved, err) = await Promise.resolve(
        partial(OrganizationRepository.create, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })


@organization_router.route('/<pk>', methods=['DELETE'])
async def delete_by_id(req: Request, pk: str) -> json:
    await Promise.resolve(partial(
        OrganizationRepository.delete_by_id, pk)
    )
    return json(None, status=204)
