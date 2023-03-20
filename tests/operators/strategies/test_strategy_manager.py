from unittest import TestCase, main

from operators.strategies.strategy_manager import initialize_manager
from models.task import Task

class StrategyManagerTests(TestCase):

    def test_do_action_should_return_false_when_no_strategy(self):
        result: bool = initialize_manager(operator='bad').do_action(task=Task(), payload='{}', external_user_id='')
        self.assertFalse(result)

    def test_do_action_should_return_false_by_strategy(self):
        result: bool = initialize_manager(operator='==').do_action(task=Task(), payload='{}', external_user_id='')
        self.assertFalse(result)

if __name__ == '__main__':
    main()
