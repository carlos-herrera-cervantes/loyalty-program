import logging

from typing import Tuple

from bson.objectid import ObjectId
from mongoengine.queryset import queryset

from common.singleton import SingletonMeta
from custom_types.pageable import Pageable
from models.customer import Customer

logger = logging.getLogger(__name__)


class CustomerRepository(metaclass=SingletonMeta):

    @staticmethod
    def get_by_id(pk: str) -> Customer | None:
        try:
            return Customer.objects.get(id=ObjectId(pk))
        except Exception as e:
            logger.error('Error getting customer by id')
            logger.error(e)

            return None

    @staticmethod
    def get_one(filter: dict) -> Customer | None:
        try:
            return Customer.objects.get(__raw__=filter)
        except Exception as e:
            logger.error('Error getting customer by filter')
            logger.error(e)

            return None

    @staticmethod
    def get_all(offset: int, limit: int) -> Pageable:
        query: queryset = (Customer
            .objects
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_customers: int = Customer.objects.count()

        return Pageable(
            total_customers,
            query,
            offset,
            limit
        )

    @staticmethod
    def get_all_by_filter(filter: dict, offset: int, limit: int) -> Pageable:
        query: queryset = (Customer
            .objects(__raw__=filter)
            .order_by('-created_at')
            .skip(offset * limit)
            .limit(limit)
            .all())
        total_customers: int = Customer.objects.count()

        return Pageable(
            total_customers,
            query,
            offset,
            limit
        )

    @staticmethod
    def create(body: dict) -> Tuple[Customer | str, bool]:
        try:
            customer: Customer = Customer(**body)
            saved: Customer = customer.save()
            return (saved, False)
        except Exception as e:
            logger.error('Error saving customer')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def update_by_id(pk: str, body: dict) -> Tuple[Customer | str, bool]:
        try:
            Customer.objects(id=ObjectId(pk)).update_one(**body)
            updated: Customer = Customer.objects.get(id=ObjectId(pk))
            updated.save()
            return (updated, False)
        except Exception as e:
            logger.error('Error updating customer')
            logger.error(e)
            return (str(e), True)

    @staticmethod
    def delete_by_id(pk: str) -> None:
        Customer.objects(id=ObjectId(pk)).delete()
