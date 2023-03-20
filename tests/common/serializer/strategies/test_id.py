from unittest import TestCase, main

from common.serializer.strategies.id import Id

class IdTests(TestCase):

    def test_parse_value_should_return_string(self) -> None:
        result: str = Id().parse_value(key='customer_id', document={
            'customer_id': {
                '$oid': '636a80212342d3513ad1733e',
            },
        })
        expected_result = '636a80212342d3513ad1733e'
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    main()
