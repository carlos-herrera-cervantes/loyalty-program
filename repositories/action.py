import logging

from typing import Tuple

from bson.objectid import ObjectId
from mongoengine.queryset import queryset

from common.singleton import SingletonMeta
from custom_types.pageable import Pageable
from models.action import Action

logger = logging.getLogger(__name__)


class ActionRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> Action | None:
        try:
            return Action.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting action by id')
            logger.error(e)

            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (Action
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_actions: int = Action.objects.count()

        return Pageable(
            total_actions,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[Action | str, bool]:
        try:
            action: Action = Action(**body)
            saved: Action = action.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving action')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def delete_by_id(pk: str) -> None:
        Action.objects(id=ObjectId(pk)).delete()
