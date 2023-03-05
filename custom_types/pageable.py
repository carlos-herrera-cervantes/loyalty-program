from json import dumps, loads

from common.serializer.document import default


class Pageable:

    def __init__(self, total_docs: int, docs: list[any], offset: int, limit: int):
        self.__total_docs: int = total_docs
        self.__docs: list[any] = docs
        self.__page: int = offset
        self.__page_size: int = limit
        self.__has_next: bool = False
        self.__has_previous: bool = False

    @property
    def pages(self) -> dict:
        skip: int = self.__page * self.__page_size
        
        self.__has_next = skip + self.__page_size < self.__total_docs
        self.__has_previous = not(self.__page == 0)

        return dumps({
            'total_docs': self.__total_docs,
            'data': loads(self.__docs.to_json(), object_hook=default),
            'page': self.__page,
            'page_size': self.__page_size,
            'has_next': self.__has_next,
            'has_previous': self.__has_previous,
        })
