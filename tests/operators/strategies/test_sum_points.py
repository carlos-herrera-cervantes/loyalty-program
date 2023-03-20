from unittest import TestCase, main

from operators.strategies.sum_points import SumPointsStrategy
from models.task import Task
from config.db import MongoClient

MongoClient().connect()

class SumPointsStrategyTests(TestCase):

    def test_run_task_should_return_false(self):
        result: bool = SumPointsStrategy().run_task(task=Task(), payload='{}', external_user_id='user@example.com')
        self.assertFalse(result)

if __name__ == '__main__':
    main()
