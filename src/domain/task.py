from datetime import datetime, date
from dataclasses import dataclass


ON_VALIDATION_STATE = "on validation"
QUEUE_STATE = "queue"
BENCHMARK_STATE = "benchmark"
ARCHIVE_STATE = "archive"


@dataclass
class Task:
    question: str
    answer: str
    state: str = QUEUE_STATE
    id: int | None = None
    source_url: str | None = None
    published_date: date | None = None

    benchmark_version: int | None = None
    created_at: datetime = datetime.now()


# from domain.validations import validate_task_state


# class Task:
#     def __init__(
#         self,
#         question: str,
#         answer: str,
#         source_url: str,
#         published_at: date,
#         state: str,
#         id: int | None = None,
#     ) -> None:
#         self._id: int = id
#         self._question: str = question
#         self._answer: str = answer
#         self._source_url: str = source_url
#         self._published_at: date = published_at
#         self._state: str = validate_task_state(state)

#     def __repr__(self) -> str:
#         attrs = ", ".join(
#             [
#                 f"id={self._id!r}",
#                 f"question={self._question!r}",
#                 f"answer={self._answer!r}",
#                 f"source_url={self._source_url!r}",
#                 f"published_at={self._published_at!r}",
#                 f"state={self._state!r}",
#             ]
#         )
#         return f"{self.__class__.__name__}({attrs})"

#     @property
#     def id(self) -> int:
#         return self._id

#     @property
#     def question(self) -> str:
#         return self._question

#     @property
#     def answer(self) -> str:
#         return self._answer

#     @property
#     def source_url(self) -> str:
#         return self._source_url

#     @property
#     def published_at(self) -> date:
#         return self._published_at

#     @property
#     def state(self) -> str:
#         return self._state

#     def change_state(self, new_state: str) -> None:
#         self._state = validate_task_state(new_state)

#     def add_id(self, id: int) -> None:
#         if self._id is not None:
#             raise ValueError("id cannot be changed")

#         self._id = id
