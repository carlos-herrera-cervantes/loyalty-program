from unittest import TestCase, main
from unittest.mock import Mock
from json import loads

from custom_types.pageable import Pageable

class PageableTests(TestCase):

    def test_pages_return_string(self) -> None:
        docs = Mock()
        docs.to_json.return_value = """[
            {
                "created_at": {
                    "$date": 1667925679
                },
                "_id": {
                    "$oid": "640ce5e0933b2b3cf6efd51d"
                },
                "password": "secret"
            }
        ]"""
        pages: str = Pageable(total_docs=1, docs=docs, offset=0, limit=10).pages
        result: dict = loads(pages)

        self.assertEqual(result['total_docs'], 1)
        self.assertEqual(result['page'], 0)
        self.assertEqual(result['page_size'], 10)
        self.assertEqual(result['has_next'], False)
        self.assertEqual(result['has_previous'], False)
        self.assertIsInstance(result['data'][0]['created_at'], str)
        self.assertEqual(result['data'][0]['_id'], '640ce5e0933b2b3cf6efd51d')
        self.assertNotIn('password', result['data'][0])


if __name__ == '__main__':
    main()
