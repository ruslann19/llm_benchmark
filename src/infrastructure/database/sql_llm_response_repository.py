from interfaces import LLMResponseRepository
from domain import LLMResponse
import sqlite3
from infrastructure.database.mappers import tuple_to_llm_response


class SqlLLMResponseRepository(LLMResponseRepository):
    def __init__(
        self,
        db_name: str,
    ) -> None:
        self._db_name = db_name

    def add(self, entity: LLMResponse) -> LLMResponse:
        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO llm_responses (task_id, llm_id, response, created_at)
                VALUES (?, ?, ?, ?);
                """,
                (entity.task_id, entity.llm_id, entity.response, entity.created_at),
            )
            conn.commit()
            new_id = cursor.lastrowid
            return LLMResponse(
                id=new_id,
                task_id=entity.task_id,
                llm_id=entity.llm_id,
                response=entity.response,
                created_at=entity.created_at,
            )

    def get_by_id(self, entity_id: int) -> LLMResponse:
        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            output_tuple = cursor.execute(
                """
                SELECT *
                FROM llm_responses
                WHERE id = ?;
                """,
                (entity_id,),
            ).fetchone()

            if output_tuple is None:
                return None

            llm_response = tuple_to_llm_response(output_tuple)
            return llm_response

    def get_all(self) -> list[LLMResponse]:
        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            output_tuples = cursor.execute(
                """
                SELECT *
                FROM llm_responses
                """,
            ).fetchall()
            llm_responses = list(map(tuple_to_llm_response, output_tuples))
            return llm_responses

    def update(self, entity: LLMResponse) -> LLMResponse:
        if entity.id is None:
            raise ValueError("Для изменения сущности нужен id")

        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE llm_responses
                SET
                    task_id = ?,
                    llm_id = ?,
                    response = ?,
                    created_at = ?
                WHERE id = ?;
                """,
                (
                    entity.task_id,
                    entity.llm_id,
                    entity.response,
                    entity.created_at,
                    entity.id,
                ),
            )

        return entity

    def delete(self, entity_id: int) -> LLMResponse:
        if self.get_by_id(entity_id) is None:
            return False

        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE
                FROM llm_responses
                WHERE id = ?
                """,
                (entity_id,),
            )

        return True

    def filter_by_llm_id(self, llm_id: int) -> list[LLMResponse]:
        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            output_tuples = cursor.execute(
                """
                SELECT *
                FROM llm_responses
                WHERE llm_id = ?
                """,
                (llm_id,),
            ).fetchall()
            llm_responses = list(map(tuple_to_llm_response, output_tuples))
            return llm_responses

    def filter_by_task_id(self, task_id: int) -> list[LLMResponse]:
        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            output_tuples = cursor.execute(
                """
                SELECT *
                FROM llm_responses
                WHERE task_id = ?
                """,
                (task_id,),
            ).fetchall()
            llm_responses = list(map(tuple_to_llm_response, output_tuples))
            return llm_responses
