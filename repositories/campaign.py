import logging

from typing import Tuple

from bson.objectid import ObjectId
from mongoengine.queryset import queryset

from common.singleton import SingletonMeta
from custom_types.pageable import Pageable
from models.campaign import Campaign

logger = logging.getLogger(__name__)


class CampaignRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> Campaign | None:
        try:
            return Campaign.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting campaign by id')
            logger.error(e)

            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (Campaign
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_campaigns: int = Campaign.objects.count()

        return Pageable(
            total_campaigns,
            query,
            offset,
            limit
        )

    @staticmethod
    def get_all_by_filter(filter: dict, offset: int, limit: int) -> Pageable:
        query: queryset = (Campaign
            .objects(__raw__=filter)
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_campaigns: int = Campaign.objects.count()

        return Pageable(
            total_campaigns,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[Campaign | str, bool]:
        try:
            campaign: Campaign = Campaign(**body)
            saved: Campaign = campaign.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving campaign')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def delete_by_id(pk: str) -> None:
        Campaign.objects(id=ObjectId(pk)).delete()
