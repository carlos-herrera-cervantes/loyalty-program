from json import loads
from functools import partial

from sanic import Blueprint
from sanic.response import json
from sanic.request import Request

from common.serializer.document import default
from common.promise import Promise
from decorators.pageable import validate_page_attributes
from decorators.common import validate_body
from custom_types.pageable import Pageable
from models.action import Action
from repositories.action import ActionRepository

action_router = Blueprint(
    'action_router',
    url_prefix='/actions'
)
promise = Promise()


@action_router.route('/<pk>', methods=['GET'])
async def get_by_id(req: Request, pk: str) -> json:
    action: Action = await promise.resolve(
        partial(ActionRepository.get_by_id, pk)
    )

    if not action:
        return json({'message': 'action not found'}, status=404)

    return json({
        'data': loads(action.to_json(), object_hook=default)
    })


@action_router.route('', methods=['GET'])
@validate_page_attributes
async def get_all(req: Request) -> json:
    offset: int = req.args['offset']
    limit: int = req.args['limit']

    pageable: Pageable = await promise.resolve(
        partial(ActionRepository.get_all, offset, limit)
    )

    return json(loads(pageable.pages))


@action_router.route('', methods=['POST'])
@validate_body
async def create(req: Request) -> json:
    body: dict = req.json
    (saved, err) = await promise.resolve(
        partial(ActionRepository.create, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })


@action_router.route('/<pk>', methods=['DELETE'])
async def delete_by_id(req: Request, pk: str) -> json:
    await promise.resolve(partial(
        ActionRepository.delete_by_id, pk)
    )
    return json(None, status=204)
