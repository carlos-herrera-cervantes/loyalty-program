from unittest import TestCase, main

from operators.strategies.less_than import LessThanStrategy
from models.task import Task


class LessThanStrategyTests(TestCase):

    def test_run_task_should_return_false(self):
        result: bool = LessThanStrategy().run_task(task=Task(), payload='{}', external_user_id='user@example.com')
        self.assertFalse(result)

    def test_run_task_should_return_true(self):
        task = Task()
        task.evaluation_property = 'age'
        task.comparison_value = '30'

        payload = """{"age": 20}"""
        result: bool = LessThanStrategy().run_task(task=task, payload=payload, external_user_id='user@example.com')
        self.assertTrue(result)

if __name__ == '__main__':
    main()
