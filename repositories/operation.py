import logging

from typing import Tuple

from bson.objectid import ObjectId
from mongoengine.queryset import queryset

from common.singleton import SingletonMeta
from custom_types.pageable import Pageable
from models.operation import Operation

logger = logging.getLogger(__name__)


class OperationRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> Operation | None:
        try:
            return Operation.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting operation by id')
            logger.error(e)

            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (Operation
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_operations: int = Operation.objects.count()

        return Pageable(
            total_operations,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[Operation | str, bool]:
        try:
            action: Operation = Operation(**body)
            saved: Operation = action.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving operation')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def delete_by_id(pk: str) -> None:
        Operation.objects(id=ObjectId(pk)).delete()
