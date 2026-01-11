from domain import Task, TaskStateChange
from interfaces import TaskRepository
from datetime import datetime
from infrastructure.repository.models import (
    TaskOrm,
    task_to_orm,
    task_from_orm,
    TaskStateChangeOrm,
    state_change_from_orm,
)
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select


class SqlTaskRepository(TaskRepository):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self._session_factory = session_factory
        self._to_orm = task_to_orm
        self._from_orm = task_from_orm

    def add(self, task: Task) -> Task:
        task_orm = self._to_orm(task)
        with self._session_factory() as session:
            session.add(task_orm)
            # Делаем flush, чтобы в task_orm появился id
            session.flush()
            task = self._to_orm(task_orm)
            session.commit()

        return task

    def add_all(self, entities: list[TaskOrm]) -> list[TaskOrm]:
        entities_orm = list(map(self._to_orm, entities))
        with self._session_factory() as session:
            session.add_all(entities_orm)
            session.flush()
            entities = list(map(self._from_orm, entities_orm))
            session.commit()

        return entities

    def get_by_id(self, task_id: int) -> Task | None:
        with self._session_factory() as session:
            task = session.get(TaskOrm, task_id)

        if not task:
            return None

        return self._from_orm(task)

    def get_all(self) -> list[Task]:
        stmt = select(TaskOrm)
        with self._session_factory() as session:
            tasks_orm = list(session.execute(stmt).scalars())

        return list(map(self._from_orm, tasks_orm))

    def update(self, task: Task) -> Task:
        if task.id is None:
            raise ValueError("Для изменения сущности нужен id")

        with self._session_factory() as session:
            task_orm = session.get(TaskOrm, task.id)

            task_orm.question = task.question
            task_orm.answer = task.answer
            task_orm.source_url = task.source_url
            task_orm.published_at = task.published_at

            if task.state != task_orm.state:
                state_change = TaskStateChangeOrm(
                    task_id=task.id,
                    previous_state=task_orm.state,
                    new_state=task.state,
                    changed_at=datetime.now(),
                )
                session.add(state_change)

            task_orm.state = task.state

            session.commit()
            session.refresh(task_orm)
            task = self._from_orm(task_orm)
            return task

    def delete(self, task_id: int) -> bool:
        with self._session_factory() as session:
            task_orm = session.get(TaskOrm, task_id)
            if not task_orm:
                return False

            session.delete(task_orm)
            session.commit()
            return True

    def get_state_changes(self, task_id: int) -> list[TaskStateChange]:
        with self._session_factory() as session:
            task_orm = session.get(TaskOrm, task_id)

            if not task_orm:
                return []

            state_changes_orm = task_orm.state_changes
            state_changes = list(map(state_change_from_orm, state_changes_orm))
            return state_changes
