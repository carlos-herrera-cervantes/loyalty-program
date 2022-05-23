import json
import logging
import os

from ..interfaces.strategy_interface import Strategy

logger = logging.getLogger(__name__)


class EnStrategy(Strategy):
    def get_translation(self, key: str) -> str:
        path: str = os.path.relpath(__file__)
        final: str = os.path.dirname(path)

        final: str = final.replace('strategies', 'source')
        os.chdir(final)

        try:
            with open('en.json') as file:
                data: list = json.load(file)
                filtered_values: list = list(filter(lambda x: x['key'] == key, data))

                return filtered_values.pop()['value']
        except Exception as e:
            logger.error('Error when loading the EN file for locales: ')
            logger.error(e)
            return key
