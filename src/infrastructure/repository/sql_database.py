from infrastructure.repository.models import Base
from sqlalchemy import Engine


class SqlDatabase:
    def __init__(
        self,
        engine: Engine,
    ) -> None:
        self._engine = engine

    def create_tables(self) -> None:
        Base.metadata.create_all(self._engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(self._engine)
