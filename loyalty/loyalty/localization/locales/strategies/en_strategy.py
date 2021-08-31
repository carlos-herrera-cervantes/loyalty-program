import json
import logging
import os

from ..interfaces.strategy_interface import Strategy

logger = logging.getLogger(__name__)

class EnStrategy(Strategy):
    def get_translation(self, key: str) -> str:
        path: str = os.path.relpath(__file__)
        dir: str = os.path.dirname(path)

        dir = dir.replace('strategies', 'source')
        os.chdir(dir)

        try:
            with open('en.json') as file:
                data: list = json.load(file)
                filtered_values: list = filter(lambda x: x['key'] == key, data)

                return list(filtered_values).pop()['value']
        except Exception as e:
            logger.error('Error when loading the EN file for locales: ', e)
            return key
