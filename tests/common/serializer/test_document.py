from unittest import TestCase, main

from mongoengine import Document

from common.serializer.document import default

class DocumentTests(TestCase):

    def test_default_should_return_Document(self) -> None:
        result: Document = default(document={
            'created_at': {
                '$date': 1667925679,
            },
            'password': 'secret123',
            '_id': {
                '$oid': '636a80212342d3513ad1733e',
            },
        })
        expected_id = '636a80212342d3513ad1733e'

        self.assertIsInstance(result['created_at'], str)
        self.assertEqual(result['_id'], expected_id)
        self.assertTrue('password' not in result)


if __name__ == '__main__':
    main()
