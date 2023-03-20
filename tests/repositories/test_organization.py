from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.organization import OrganizationRepository
from config.db import MongoClient
from common.promise import Promise
from custom_types.pageable import Pageable
from models.organization import Organization

MongoClient().connect()

class OrganizationRepositoryTests(IsolatedAsyncioTestCase):

    async def test_crud(self):
        organization = {'name': 'Test Action'}
        insertion_result, success = await Promise.resolve(partial(OrganizationRepository.create, organization))
        self.assertFalse(success)

        single_query_result: Organization | None = await Promise.resolve(partial(
            OrganizationRepository.get_by_id,
            insertion_result.id
        ))
        self.assertIsNotNone(single_query_result)

        await Promise.resolve(partial(OrganizationRepository.delete_by_id, insertion_result.id))
        query_result: Pageable = await Promise.resolve(partial(OrganizationRepository.get_all, 0, 10))
        self.assertIsInstance(query_result, Pageable)


if __name__ == '__main__':
    main()
