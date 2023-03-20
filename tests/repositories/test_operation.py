from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.operation import OperationRepository
from config.db import MongoClient
from common.promise import Promise
from custom_types.pageable import Pageable
from models.operation import Operation

MongoClient().connect()

class OperationRepositoryTests(IsolatedAsyncioTestCase):

    async def test_crud(self):
        operation = {
            'name': 'Test Action',
            'description': 'This is a test action',
            'operator': '==',
        }
        insertion_result, success = await Promise.resolve(partial(OperationRepository.create, operation))
        self.assertFalse(success)

        single_query_result: Operation | None = await Promise.resolve(partial(
            OperationRepository.get_by_id,
            insertion_result.id
        ))
        self.assertIsNotNone(single_query_result)

        await Promise.resolve(partial(OperationRepository.delete_by_id, insertion_result.id))
        query_result: Pageable = await Promise.resolve(partial(OperationRepository.get_all, 0, 10))
        self.assertIsInstance(query_result, Pageable)


if __name__ == '__main__':
    main()
