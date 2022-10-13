from mongoengine import Document

from common.serializer.interfaces.strategy import Strategy


class Id(Strategy):

    def parse_value(self, key: str, document: Document) -> str:
        id: str = document[key]['$oid']
        return id
