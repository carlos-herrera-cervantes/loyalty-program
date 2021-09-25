from abc import ABC, abstractmethod

from models.task import Task
from models.customer import CustomerKeys

class Strategy(ABC):

    @abstractmethod
    def run_task(self, task: Task, keys: CustomerKeys) -> bool:
        pass