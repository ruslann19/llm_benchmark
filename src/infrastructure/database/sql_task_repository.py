from domain import Task, TaskStateChange
from interfaces import TaskRepository
import sqlite3
from datetime import date

from infrastructure.database.mappers import tuple_to_task


class SqlTaskRepository(TaskRepository):
    def __init__(
        self,
        db_name: str,
    ) -> None:
        self._db_name: str = db_name

    def get_by_id(self, task_id: int) -> Task:
        tasks = self._execute(
            """
            SELECT *
            FROM tasks
            WHERE tasks.id == ?
            """,
            (task_id,),
        )
        if len(tasks) != 0:
            return tuple_to_task(tasks[0])

        return None

    def get_all(self) -> list[Task]:
        result = self._execute("SELECT * FROM tasks")
        tasks = list(map(tuple_to_task, result))
        return tasks

    def add(self, task: Task) -> Task:
        with sqlite3.connect(self._db_name) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (question, answer, source_url, published_at, state)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    task.question,
                    task.answer,
                    task.source_url,
                    task.published_at,
                    task.state,
                ),
            )
            connection.commit()
            task_id = cursor.lastrowid
            return Task(
                id=task_id,
                question=task.question,
                answer=task.answer,
                source_url=task.source_url,
                published_at=task.published_at,
                state=task.state,
            )

    def delete(self, task_id: int) -> bool:
        if self.get_by_id(task_id) is None:
            return False

        self._execute(
            """
            DELETE FROM tasks
            WHERE tasks.id == ?
            """,
            (task_id,),
        )
        return True

    def update(self, task: Task) -> Task:
        if task.id is None:
            raise ValueError("Для изменения записи нужен id")

        persisted_tuple = self.get_by_id(task.id)
        persisted_task = tuple_to_task(persisted_tuple)
        if persisted_task is None:
            raise ValueError("Нельзя изменить задание,которое не лежит в базе данных")

        self._execute(
            """
            UPDATE tasks
            SET
                question = ?,
                answer = ?,
                source_url = ?,
                published_at = ?,
                state = ?
            WHERE id = ?
            """,
            (
                task.question,
                task.answer,
                task.source_url,
                task.published_at,
                task.state,
                task.id,
            ),
        )

        if persisted_task.state != task.state:
            change_state = TaskStateChange(
                task_id=task.id,
                previous_state=persisted_task.state,
                new_state=task.state,
                changed_at=date.today(),
            )

            self._execute(
                """
                INSERT INTO task_state_changes (
                    task_id,
                    previous_state,
                    new_state,
                    changed_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    change_state.task_id,
                    change_state.previous_state,
                    change_state.new_state,
                    change_state.changed_at,
                ),
            )

        return task

    def get_state_changes(self, task_id: int) -> list[TaskStateChange]:
        return self._execute(
            """
            SELECT * FROM task_state_changes
            WHERE task_state_changes.task_id == ?
            """,
            (task_id,),
        )

    def _execute(self, query: str, params: tuple = ()) -> any:
        with sqlite3.connect(self._db_name) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            cursor = connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
