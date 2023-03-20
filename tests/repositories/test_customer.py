from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.customer import CustomerRepository
from config.db import MongoClient
from common.promise import Promise
from custom_types.pageable import Pageable
from models.customer import Customer

MongoClient().connect()

class CustomerRepositoryTests(IsolatedAsyncioTestCase):

    async def test_get_by_id_should_return_none(self):
        single_query_result: Customer | None = await Promise.resolve(partial(
            CustomerRepository.get_by_id,
            '641625640176c64f955fee4a'
        ))
        self.assertIsNone(single_query_result)

    async def test_get_one_should_return_none(self):
        single_query_result: Customer | None = await Promise.resolve(partial(
            CustomerRepository.get_one,
            {}
        ))
        self.assertIsNone(single_query_result)

    async def test_get_all_should_return_pageable(self):
        query_result: Pageable = await Promise.resolve(partial(CustomerRepository.get_all, 0, 10))
        self.assertIsInstance(query_result, Pageable)

    async def test_get_all_by_filter_should_return_pageable(self):
        query_result: Pageable = await Promise.resolve(partial(
            CustomerRepository.get_all_by_filter,
            {}, 0, 10
        ))
        self.assertIsInstance(query_result, Pageable)


if __name__ == '__main__':
    main()
