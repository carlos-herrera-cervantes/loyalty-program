import logging
from typing import Tuple

from bson.objectid import ObjectId
from mongoengine.queryset import queryset

from common.singleton import SingletonMeta
from custom_types.pageable import Pageable
from models.transaction import Transaction

logger = logging.getLogger(__name__)


class TransactionRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> Transaction | None:
        try:
            return Transaction.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting transaction by id')
            logger.error(e)
            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (Transaction
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_transactions: int = Transaction.objects.count()

        return Pageable(
            total_transactions,
            query,
            offset,
            limit
        )

    @staticmethod
    def get_all_by_filter(filter: dict, offset: int, limit: int) -> Pageable:
        query: queryset = (Transaction
            .objects(__raw__=filter)
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_transactions: int = Transaction.objects.count()

        return Pageable(
            total_transactions,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[Transaction | str, bool]:
        try:
            transaction: Transaction = Transaction(**body)
            saved: Transaction = transaction.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving transaction')
            logger.error(e)
            return (str(e), True)
