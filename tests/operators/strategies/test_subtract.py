from unittest import TestCase, main

from operators.strategies.subtract import SubtractStrategy
from models.task import Task
from config.db import MongoClient

MongoClient().connect()

class SubtractStrategyTests(TestCase):

    def test_run_task_should_return_false(self):
        result: bool = SubtractStrategy().run_task(task=Task(), payload='{}', external_user_id='user@example.com')
        self.assertFalse(result)

if __name__ == '__main__':
    main()
