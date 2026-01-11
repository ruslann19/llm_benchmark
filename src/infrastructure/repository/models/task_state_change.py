from infrastructure.repository.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from domain import TaskStateChange


class TaskStateChangeOrm(Base):
    __tablename__ = "task_state_changes"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    previous_state: Mapped[str]
    new_state: Mapped[str]
    changed_at: Mapped[datetime]

    task: Mapped["TaskOrm"] = relationship(back_populates="state_changes")  # noqa: F821


def state_change_to_orm(state_change: TaskStateChange) -> TaskStateChangeOrm:
    return TaskStateChangeOrm(
        id=state_change.id,
        task_id=state_change.task_id,
        previous_state=state_change.previous_state,
        new_state=state_change.new_state,
        changed_at=state_change.changed_at,
    )


def state_change_from_orm(state_change_orm: TaskStateChangeOrm) -> TaskStateChange:
    return TaskStateChange(
        id=state_change_orm.id,
        task_id=state_change_orm.task_id,
        previous_state=state_change_orm.previous_state,
        new_state=state_change_orm.new_state,
        changed_at=state_change_orm.changed_at,
    )
