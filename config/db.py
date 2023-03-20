import mongoengine

from common.singleton import SingletonMeta
from config.app import MongoDB


class MongoClient(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.__db = MongoDB.DEFAULT_DB.value

    def connect(self) -> None:
        print('Successful connected to MongoDB')
        mongoengine.connect(host=self.__db)
