from unittest import TestCase, main

from operators.strategies.greater_than_equal import GreaterThanEqualStrategy
from models.task import Task


class GreaterThanEqualStrategyTests(TestCase):

    def test_run_task_should_return_false(self):
        result: bool = GreaterThanEqualStrategy().run_task(task=Task(), payload='{}', external_user_id='user@example.com')
        self.assertFalse(result)

    def test_run_task_should_return_true(self):
        task = Task()
        task.evaluation_property = 'age'
        task.comparison_value = '30'

        payload = """{"age": 44}"""
        result: bool = GreaterThanEqualStrategy().run_task(task=task, payload=payload, external_user_id='user@example.com')
        self.assertTrue(result)

if __name__ == '__main__':
    main()
