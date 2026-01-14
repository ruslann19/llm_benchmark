from domain import (
    Task,
    QUEUE_STATE,
    BENCHMARK_STATE,
    ARCHIVE_STATE,
)
from interfaces import TaskRepository
from datetime import date
from infrastructure.repository.models import (
    TaskOrm,
    task_to_orm,
    task_from_orm,
)
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, func, update


class SqlTaskRepository(TaskRepository):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self._session_factory = session_factory
        self._to_orm = task_to_orm
        self._from_orm = task_from_orm
        self._BENCHMARK_SIZE = 10

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
            task_orm.published_date = task.published_date
            task_orm.benchmark_version = task.benchmark_version
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

    def filter_by_state(self, state: str) -> list[Task]:
        with self._session_factory() as session:
            stmt = select(TaskOrm).where(TaskOrm.state == state)
            entities_orm = session.execute(stmt).scalars().all()
            entities = list(map(self._from_orm, entities_orm))
            return entities

    def update_benchmark(self) -> list[Task]:
        with self._session_factory() as session:
            stmt = select(func.count(TaskOrm.id)).where(TaskOrm.state == QUEUE_STATE)
            queue_size = session.execute(stmt).scalars().one()

            if queue_size < self._BENCHMARK_SIZE:
                raise ValueError(
                    "В очереди недостаточно заданий для обновления бенчмарка"
                )

            stmt = (
                update(TaskOrm)
                .where(TaskOrm.state == BENCHMARK_STATE)
                .values(state=ARCHIVE_STATE)
            )
            session.execute(stmt)

            stmt = select(func.max(TaskOrm.benchmark_version))
            version = session.execute(stmt).scalar()
            if not version:
                version = 0

            stmt_select = (
                select(TaskOrm.id)
                .where(TaskOrm.state == QUEUE_STATE)
                .order_by(TaskOrm.created_at.asc())
                .limit(self._BENCHMARK_SIZE)
            )
            ids_to_update = session.execute(stmt_select).scalars().all()

            if ids_to_update:
                stmt_update = (
                    update(TaskOrm)
                    .where(TaskOrm.id.in_(ids_to_update))
                    .values(state=BENCHMARK_STATE, benchmark_version=version + 1)
                )
                session.execute(stmt_update)

            session.commit()

        benchmark_tasks = self.filter_by_state(state=BENCHMARK_STATE)
        return benchmark_tasks

    def get_benchmark_version(self, benchmark_version: date) -> list[Task]:
        stmt = select(TaskOrm).where(TaskOrm.benchmark_version == benchmark_version)

        with self._session_factory() as session:
            entities_orm = session.execute(stmt).scalars().all()

        entities = list(map(self._from_orm, entities_orm))
        return entities
