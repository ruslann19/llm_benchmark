import sqlite3


class SqlDatabase:
    def __init__(
        self,
        db_name: str,
    ) -> None:
        self._db_name = db_name

    def create_tables(self) -> None:
        self._execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                source_url TEXT NOT NULL,
                published_at DATE NOT NULL,
                state TEXT NOT NULL
            )
            """
        )
        self._execute(
            """
            CREATE TABLE IF NOT EXISTS task_state_changes (
                id INTEGER PRIMARY KEY,
                task_id INTEGER NOT NULL,
                previous_state TEXT NOT NULL,
                new_state TEXT NOT NULL,
                changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
            )
            """
        )
        self._execute(
            """
            CREATE TABLE llm_infos (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                provider TEXT NOT NULL,
                api_url TEXT NOT NULL
            );
            """
        )
        self._execute(
            """
            CREATE TABLE llm_responses (
                id INTEGER PRIMARY KEY,
                task_id INTEGER NOT NULL,
                llm_id INTEGER NOT NULL,
                response TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
                FOREIGN KEY (llm_id) REFERENCES llm_infos(id) ON DELETE CASCADE
            );
            """
        )

    def drop_tables(self) -> None:
        self._execute("DROP TABLE IF EXISTS llm_responses")
        self._execute("DROP TABLE IF EXISTS task_state_changes")
        self._execute("DROP TABLE IF EXISTS tasks")
        self._execute("DROP TABLE IF EXISTS llm_infos")

    def _execute(self, query: str, params: tuple = ()) -> any:
        with sqlite3.connect(self._db_name) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            cursor = connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
