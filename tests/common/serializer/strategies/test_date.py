from unittest import TestCase, main

from common.serializer.strategies.date import Date

class DateTests(TestCase):

    def test_parse_value_should_return_string(self) -> None:
        result: str = Date().parse_value(key='date', document={
            'date': {
                '$date': 1667925679,
            },
        })
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    main()
