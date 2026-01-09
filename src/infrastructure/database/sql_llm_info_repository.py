from interfaces import LLMInfoRepository
from domain import LLMInfo
import sqlite3
from infrastructure.database.mappers import tuple_to_llm_info


class SqlLLMInfoRepository(LLMInfoRepository):
    def __init__(
        self,
        db_name: str,
    ) -> None:
        self._db_name = db_name

    def add(self, entity: LLMInfo) -> LLMInfo:
        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO llm_infos (name, provider, api_url)
                VALUES (?, ?, ?);
                """,
                (entity.name, entity.provider, entity.api_url),
            )
            conn.commit()
            new_id = cursor.lastrowid
            return LLMInfo(
                id=new_id,
                name=entity.name,
                provider=entity.provider,
                api_url=entity.api_url,
            )

    def get_by_id(self, entity_id: int) -> LLMInfo:
        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            llm_info_tuple = cursor.execute(
                """
                SELECT *
                FROM llm_infos
                WHERE id = ?
                """,
                (entity_id,),
            ).fetchone()

            if llm_info_tuple is None:
                return None

            llm_info = tuple_to_llm_info(llm_info_tuple)
            return llm_info

    def get_all(self):
        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            llm_info_tuples = cursor.execute(
                """
                SELECT *
                FROM llm_infos
                """,
            ).fetchall()

            llm_infos = list(map(tuple_to_llm_info, llm_info_tuples))
            return llm_infos

    def update(self, entity: LLMInfo) -> LLMInfo:
        if entity.id is None:
            raise ValueError("Для изменения сущности нужен id")

        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE llm_infos
                SET
                    name = ?,
                    provider = ?,
                    api_url = ?
                WHERE id = ?
                """,
                (
                    entity.name,
                    entity.provider,
                    entity.api_url,
                    entity.id,
                ),
            )

        return entity

    def delete(self, entity_id: LLMInfo) -> bool:
        if self.get_by_id(entity_id) is None:
            return False

        with sqlite3.connect(self._db_name) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE
                FROM llm_infos
                WHERE id = ?
                """,
                (entity_id,),
            )

        return True
