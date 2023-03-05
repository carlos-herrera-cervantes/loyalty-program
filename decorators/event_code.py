from typing import Callable
from functools import wraps, partial

from sanic.request import Request
from sanic.response import json

from models.campaign import Campaign
from repositories.campaign import CampaignRepository
from common.promise import Promise


def validate_campaign_id(fn: Callable) -> Callable:
    @wraps(fn)
    async def inner_fn(req: Request, *args: dict, **kwargs: dict) -> Callable:
        campaign_id: str = req.match_info.get('campaign_id')
        campaign: Campaign = await Promise.resolve(
            partial(CampaignRepository.get_by_id, campaign_id)
        )

        if not campaign:
            return json({
                'message': 'Campaign not found'
            }, status=404)

        req.json['campaign_id'] = campaign_id
        return await fn(req, *args, **kwargs)
    return inner_fn
