import logging

from typing import Tuple

from bson.objectid import ObjectId
from mongoengine.queryset import queryset

from common.singleton import SingletonMeta
from custom_types.pageable import Pageable
from models.bucket import Bucket

logger = logging.getLogger(__name__)


class BucketRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> Bucket | None:
        try:
            return Bucket.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting bucket by id')
            logger.error(e)

            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (Bucket
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_buckets: int = Bucket.objects.count()

        return Pageable(
            total_buckets,
            query,
            offset,
            limit
        )

    @staticmethod
    def get_all_by_filter(filter: dict, offset: int, limit: int) -> Pageable:
        query: queryset = (Bucket
            .objects(__raw__=filter)
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_buckets: int = Bucket.objects.count()

        return Pageable(
            total_buckets,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[Bucket | str, bool]:
        try:
            bucket: Bucket = Bucket(**body)
            saved: Bucket = bucket.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving bucket')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def delete_by_id(pk: str) -> None:
        Bucket.objects(id=ObjectId(pk)).delete()
