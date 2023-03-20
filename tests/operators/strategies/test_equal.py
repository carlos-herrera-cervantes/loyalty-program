from unittest import TestCase, main

from operators.strategies.equal import EqualStrategy
from models.task import Task


class EqualStrategyTests(TestCase):

    def test_run_task_should_return_false_by_evaluation_property(self):
        result: bool = EqualStrategy().run_task(task=Task(), payload='{}', external_user_id='user@example.com')
        self.assertFalse(result)

    def test_run_task_should_return_true_by_int(self):
        task = Task()
        task.evaluation_property = 'age'
        task.comparison_value_type = 'int'
        task.comparison_value = '28'

        payload = """{"age": 28}"""

        result: bool = EqualStrategy().run_task(task=task, payload=payload, external_user_id='user@example.com')
        self.assertTrue(result)

    def test_run_task_should_return_true_by_string(self):
        task = Task()
        task.evaluation_property = 'last_name'
        task.comparison_value_type = 'string'
        task.comparison_value = 'Ortíz'

        payload = """{"last_name": "Ortíz"}"""

        result: bool = EqualStrategy().run_task(task=task, payload=payload, external_user_id='user@example.com')
        self.assertTrue(result)

if __name__ == '__main__':
    main()
