from abc import ABC, abstractmethod

from models.task import Task


class Strategy(ABC):

    @abstractmethod
    def run_task(self, task: Task, payload: dict, external_user_id: str) -> bool:
        pass
