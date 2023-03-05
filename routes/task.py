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
from decorators.task import validate_event_code_id
from custom_types.pageable import Pageable
from models.task import Task
from repositories.task import TaskRepository

task_router = Blueprint(
    'task_router',
    url_prefix=(
        '/organizations/<organization_id>/buckets' +
        '/<bucket_id>/campaigns/<campaign_id>' +
        '/event-codes/<event_code_id>/tasks'
    )
)


@task_router.route('/<pk>', methods=['GET'])
async def get_by_id(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str,
    event_code_id: str,
    pk: str
) -> json:
    task: Task = await Promise.resolve(
        partial(TaskRepository.get_by_id, pk)
    )

    if not task:
        return json({'message': 'task not found'}, status=404)

    return json({
        'data': loads(task.to_json(), object_hook=default)
    })


@task_router.route('', methods=['GET'])
@validate_page_attributes
async def get_all(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str,
    event_code_id: str,
) -> json:
    offset: int = req.args['offset']
    limit: int = req.args['limit']

    fn: partial = partial(
        TaskRepository.get_all_by_filter,
        {'event_code_id': ObjectId(event_code_id)},
        offset,
        limit
    )
    pageable: Pageable = await Promise.resolve(fn)

    return json(loads(pageable.pages))


@task_router.route('', methods=['POST'])
@validate_body
@validate_event_code_id
async def create(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str,
    event_code_id: str,
) -> json:
    body: dict = req.json
    (saved, err) = await Promise.resolve(
        partial(TaskRepository.create, body)
    )

    if err:
        return json({'message': saved}, status=400)

    return json({
        'data': loads(saved.to_json(), object_hook=default),
    })


@task_router.route('/<pk>', methods=['DELETE'])
async def delete_by_id(
    req: Request,
    organization_id: str,
    bucket_id: str,
    campaign_id: str,
    event_code_id: str,
    pk: str
) -> json:
    await Promise.resolve(partial(
        TaskRepository.delete_by_id, pk)
    )
    return json(None, status=204)
