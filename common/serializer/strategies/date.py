from datetime import datetime

from mongoengine import Document

from common.serializer.interfaces.strategy import Strategy


class Date(Strategy):

    def parse_value(self, key: str, document: Document) -> str:
        date: str = datetime.fromtimestamp(document[key]['$date'] / 1000).isoformat()
        return date
