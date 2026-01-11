from infrastructure.repository.models import Base
from sqlalchemy import Engine, event


class SqlDatabase:
    def __init__(
        self,
        engine: Engine,
    ) -> None:
        self._engine = engine

        # Включаем поддержку внешних ключей в SQLite
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    def create_tables(self) -> None:
        Base.metadata.create_all(self._engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(self._engine)
