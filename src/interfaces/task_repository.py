from abc import abstractmethod
from domain import Task, TaskStateChange
from interfaces.repository import Repository


class TaskRepository(Repository[Task]):
    @abstractmethod
    def get_state_changes(self, task_id: int) -> list[TaskStateChange]:
        pass
