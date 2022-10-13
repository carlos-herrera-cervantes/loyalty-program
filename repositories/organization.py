import logging

from bson.objectid import ObjectId
from mongoengine.queryset import queryset
from typing import Tuple

from models.organization import Organization
from custom_types.pageable import Pageable
from common.singleton import SingletonMeta

logger = logging.getLogger(__name__)


class OrganizationRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> Organization | None:
        try:
            return Organization.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting organization by id')
            logger.error(e)

            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (Organization
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_organizations: int = Organization.objects.count()

        return Pageable(
            total_organizations,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[Organization | str, bool]:
        try:
            organization: Organization = Organization(**body)
            saved: Organization = organization.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving organization')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def delete_by_id(pk: str) -> None:
        Organization.objects(id=ObjectId(pk)).delete()
