from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.repository.models import Base
from datetime import datetime, date
from domain import Task


class TaskOrm(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)

    question: Mapped[str]
    answer: Mapped[str]
    state: Mapped[str]
    source_url: Mapped[str | None]
    published_date: Mapped[date | None]

    benchmark_version: Mapped[int | None]
    created_at: Mapped[datetime]

    llm_responses: Mapped[list["LLMResponseOrm"]] = relationship(  # noqa: F821
        back_populates="task",
        cascade="all, delete-orphan",
    )


def task_to_orm(task: Task) -> TaskOrm:
    return TaskOrm(
        id=task.id,
        question=task.question,
        state=task.state,
        answer=task.answer,
        source_url=task.source_url,
        published_date=task.published_date,
        benchmark_version=task.benchmark_version,
        created_at=task.created_at,
    )


def task_from_orm(task_orm: TaskOrm) -> Task:
    return Task(
        id=task_orm.id,
        question=task_orm.question,
        answer=task_orm.answer,
        state=task_orm.state,
        source_url=task_orm.source_url,
        published_date=task_orm.published_date,
        benchmark_version=task_orm.benchmark_version,
        created_at=task_orm.created_at,
    )
