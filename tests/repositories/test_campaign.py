from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.campaign import CampaignRepository
from config.db import MongoClient
from common.promise import Promise
from custom_types.pageable import Pageable
from models.campaign import Campaign

MongoClient().connect()

class CampaignRepositoryTests(IsolatedAsyncioTestCase):

    async def test_get_by_id_should_return_none(self):
        single_query_result: Campaign | None = await Promise.resolve(partial(
            CampaignRepository.get_by_id,
            '641625640176c64f955fee4a'
        ))
        self.assertIsNone(single_query_result)

    async def test_get_all_should_return_pageable(self):
        query_result: Pageable = await Promise.resolve(partial(CampaignRepository.get_all, 0, 10))
        self.assertIsInstance(query_result, Pageable)

    async def test_get_all_by_filter_should_return_pageable(self):
        query_result: Pageable = await Promise.resolve(partial(
            CampaignRepository.get_all_by_filter,
            {}, 0, 10
        ))
        self.assertIsInstance(query_result, Pageable)


if __name__ == '__main__':
    main()
