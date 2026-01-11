from interfaces import LLMInfoRepository
from domain import LLMInfo
from sqlalchemy.orm import sessionmaker, Session
from infrastructure.repository.models import (
    LLMInfoOrm,
    llm_info_to_orm,
    llm_info_from_orm,
)
from sqlalchemy import select


class SqlLLMInfoRepository(LLMInfoRepository):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self._session_factory = session_factory
        self._to_orm = llm_info_to_orm
        self._from_orm = llm_info_from_orm

    def add(self, entity: LLMInfo) -> LLMInfo:
        entity_orm = self._to_orm(entity)
        with self._session_factory() as session:
            session.add(entity_orm)
            session.flush()
            entity = self._from_orm(entity_orm)
            session.commit()

        return entity

    def add_all(self, entities: list[LLMInfo]) -> list[LLMInfo]:
        entities_orm = list(map(self._to_orm, entities))
        with self._session_factory() as session:
            session.add_all(entities_orm)
            session.flush()
            entities = list(map(self._from_orm, entities_orm))
            session.commit()

        return entities

    def get_by_id(self, entity_id: int) -> LLMInfo | None:
        with self._session_factory() as session:
            entity_orm = session.get(LLMInfoOrm, entity_id)

        if not entity_orm:
            return None

        return self._from_orm(entity_orm)

    def get_all(self):
        stmt = select(LLMInfoOrm)
        with self._session_factory() as session:
            entities_orm = list(session.execute(stmt).scalars())

        return list(map(self._from_orm, entities_orm))

    def update(self, entity: LLMInfo) -> LLMInfo:
        if entity.id is None:
            raise ValueError("Для изменения сущности нужен id")

        with self._session_factory() as session:
            llm_info_orm = session.get(LLMInfoOrm, entity.id)

            llm_info_orm.name = entity.name
            llm_info_orm.provider = entity.provider
            llm_info_orm.api_url = entity.api_url

            session.commit()
            session.refresh(llm_info_orm)
            llm_info = self._from_orm(llm_info_orm)
            return llm_info

    def delete(self, entity_id: LLMInfo) -> bool:
        with self._session_factory() as session:
            entity_orm = session.get(LLMInfoOrm, entity_id)
            if not entity_orm:
                return False

            session.delete(entity_orm)
            session.commit()
            return True
