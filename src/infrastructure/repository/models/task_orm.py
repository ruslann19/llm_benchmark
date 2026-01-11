from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.repository.models import Base
from datetime import datetime
from domain import Task


class TaskOrm(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str]
    answer: Mapped[str]
    source_url: Mapped[str]
    published_at: Mapped[datetime]
    state: Mapped[str]

    state_changes: Mapped[list["TaskStateChangeOrm"]] = relationship(  # noqa: F821
        back_populates="task",
        cascade="all, delete-orphan",
    )

    llm_responses: Mapped[list["LLMResponseOrm"]] = relationship(  # noqa: F821
        back_populates="task",
        cascade="all, delete-orphan",
    )


def task_to_orm(task: Task) -> TaskOrm:
    return TaskOrm(
        id=task.id,
        question=task.question,
        answer=task.answer,
        source_url=task.source_url,
        published_at=task.published_at,
        state=task.state,
    )


def task_from_orm(task_orm: TaskOrm) -> Task:
    return Task(
        id=task_orm.id,
        question=task_orm.question,
        answer=task_orm.answer,
        source_url=task_orm.source_url,
        published_at=task_orm.published_at,
        state=task_orm.state,
    )
