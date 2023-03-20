import logging

from bson.objectid import ObjectId
from mongoengine.queryset import queryset
from typing import Tuple

from models.task import Task
from custom_types.pageable import Pageable
from common.singleton import SingletonMeta

logger = logging.getLogger(__name__)


class TaskRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> Task | None:
        try:
            return Task.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting task by id')
            logger.error(e)
            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (Task
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_tasks: int = Task.objects.count()

        return Pageable(
            total_tasks,
            query,
            offset,
            limit
        )

    @staticmethod
    def get_all_by_filter(filter: dict, offset: int, limit: int) -> Pageable:
        query: queryset = (Task
            .objects(__raw__=filter)
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_tasks: int = Task.objects.count()

        return Pageable(
            total_tasks,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[Task | str, bool]:
        try:
            task: Task = Task(**body)
            saved: Task = task.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving task')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def delete_by_id(pk: str) -> None:
        Task.objects(id=ObjectId(pk)).delete()
