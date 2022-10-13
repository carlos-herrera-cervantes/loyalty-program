from asyncio import AbstractEventLoop, get_event_loop, Future, gather
from typing import Callable
from functools import partial

from common.singleton import SingletonMeta


class Promise(metaclass=SingletonMeta):

    @staticmethod
    async def resolve(fn: partial) -> any:
        loop: AbstractEventLoop = get_event_loop()
        future: Future = loop.run_in_executor(None, fn)
        return await future

    @staticmethod
    async def resolve_all(fns: list[partial]) -> list[any]:
        loop: AbstractEventLoop = get_event_loop()
        tasks: list[Callable] = []

        for fn in fns:
            task: Future = loop.run_in_executor(None, fn)
            tasks.append(task)

        return await gather(*tasks)
