from abc import abstractmethod
from domain import Task
from interfaces.repository import Repository
from datetime import date


class TaskRepository(Repository[Task]):
    @abstractmethod
    def filter_by_state(self, state: str) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def update_benchmark(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_benchmark_version(self, benchmarked_at: date) -> list[Task]:
        raise NotImplementedError
