from abc import ABC, abstractmethod
from domain import Task


class TaskGenerator(ABC):
    @abstractmethod
    def generate_from_text(self, text: str) -> list[Task]:
        raise NotImplementedError
