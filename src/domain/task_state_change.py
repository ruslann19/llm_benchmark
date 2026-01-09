from datetime import date
from dataclasses import dataclass

# from domain.validations import validate_task_state


@dataclass
class TaskStateChange:
    task_id: int
    previous_state: str
    new_state: str
    changed_at: date
    id: int | None = None


# class TaskStateChange:
#     def __init__(
#         self,
#         task_id: int,
#         previous_state: str,
#         new_state: str,
#         changed_at: date,
#         id: int | None = None,
#     ) -> None:
#         self._id: int = id
#         self._task_id: int = task_id
#         self._previous_state: str = validate_task_state(previous_state)
#         self._new_state: str = validate_task_state(new_state)
#         self._changed_at: date = changed_at

#     def __repr__(self) -> str:
#         attrs = ", ".join(
#             [
#                 f"id={self._id!r}",
#                 f"task_id={self._task_id!r}",
#                 f"previous_state={self._previous_state!r}",
#                 f"new_state={self._new_state!r}",
#                 f"changed_at={self._changed_at!r}",
#             ]
#         )
#         return f"{self.__class__.__name__}({attrs})"

#     @property
#     def id(self) -> int:
#         return self._id

#     @property
#     def task_id(self) -> int:
#         return self._task_id

#     @property
#     def previous_state(self) -> str:
#         return self._previous_state

#     @property
#     def new_state(self) -> str:
#         return self._new_state

#     @property
#     def changed_at(self) -> date:
#         return self._changed_at
