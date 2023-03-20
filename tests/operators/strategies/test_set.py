from unittest import TestCase, main

from operators.strategies.set import SetStrategy
from models.task import Task
from config.db import MongoClient

MongoClient().connect()

class SetStrategyTests(TestCase):

    def test_run_task_should_return_false(self):
        result: bool = SetStrategy().run_task(task=Task(), payload='{}', external_user_id='user@example.com')
        self.assertFalse(result)

if __name__ == '__main__':
    main()
