from typing import Callable
from functools import wraps, partial

from sanic.request import Request
from sanic.response import json

from models.organization import Organization
from repositories.organization import OrganizationRepository
from common.promise import Promise


def validate_organization_id(fn: Callable) -> Callable:
    @wraps(fn)
    async def inner_fn(req: Request, *args: dict, **kwargs: dict) -> Callable:
        organization_id: str = req.match_info.get('organization_id')
        organization: Organization = await Promise.resolve(
            partial(OrganizationRepository.get_by_id, organization_id)
        )

        if not organization:
            return json({
                'message': 'Organization not found'
            }, status=404)

        req.json['organization_id'] = organization_id
        return await fn(req, *args, **kwargs)
    return inner_fn
