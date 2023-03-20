from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.action import ActionRepository
from config.db import MongoClient
from common.promise import Promise
from custom_types.pageable import Pageable
from models.action import Action

MongoClient().connect()

class ActionRepositoryTests(IsolatedAsyncioTestCase):

    async def test_crud(self):
        action = {
            'name': 'Test Action',
            'description': 'This is a test action',
            'operator': '==',
        }
        insertion_result, success = await Promise.resolve(partial(ActionRepository.create, action))
        self.assertFalse(success)

        single_query_result: Action | None = await Promise.resolve(partial(ActionRepository.get_by_id, insertion_result.id))
        self.assertIsNotNone(single_query_result)

        await Promise.resolve(partial(ActionRepository.delete_by_id, insertion_result.id))
        query_result: Pageable = await Promise.resolve(partial(ActionRepository.get_all, 0, 10))
        self.assertIsInstance(query_result, Pageable)


if __name__ == '__main__':
    main()
