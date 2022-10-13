import logging

from typing import Tuple

from bson.objectid import ObjectId
from mongoengine.queryset import queryset

from common.singleton import SingletonMeta
from custom_types.pageable import Pageable
from models.event_code import EventCode

logger = logging.getLogger(__name__)


class EventCodeRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> EventCode | None:
        try:
            return EventCode.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting event code by id')
            logger.error(e)

            return None

    @staticmethod
    def get_one(filter: dict) -> EventCode | None:
        try:
            return EventCode.objects.get(__raw__=filter)
        except Exception as e:
            logger.error('Error getting event code by filter')
            logger.error(e)

            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (EventCode
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_event_code: int = EventCode.objects.count()

        return Pageable(
            total_event_code,
            query,
            offset,
            limit
        )

    @staticmethod
    def get_all_by_filter(filter: dict, offset: int, limit: int) -> Pageable:
        query: queryset = (EventCode
            .objects(__raw__=filter)
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_event_code: int = EventCode.objects.count()

        return Pageable(
            total_event_code,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[EventCode | str, bool]:
        try:
            event_code: EventCode = EventCode(**body)
            saved: EventCode = event_code.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving event code')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def delete_by_id(pk: str) -> None:
        EventCode.objects(id=ObjectId(pk)).delete()
