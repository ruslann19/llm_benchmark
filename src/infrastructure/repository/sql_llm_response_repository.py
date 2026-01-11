from interfaces import LLMResponseRepository
from domain import LLMResponse
from sqlalchemy.orm import sessionmaker, Session
from infrastructure.repository.models import (
    LLMResponseOrm,
    llm_response_to_orm,
    llm_response_from_orm,
)
from sqlalchemy import select


class SqlLLMResponseRepository(LLMResponseRepository):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self._session_factory = session_factory
        self._to_orm = llm_response_to_orm
        self._from_orm = llm_response_from_orm

    def add(self, entity: LLMResponse) -> LLMResponse:
        entity_orm = self._to_orm(entity)
        with self._session_factory() as session:
            session.add(entity_orm)
            session.flush()
            entity = self._from_orm(entity_orm)
            session.commit()

        return entity

    def add_all(self, entities: list[LLMResponse]) -> list[LLMResponse]:
        entities_orm = list(map(self._to_orm, entities))
        with self._session_factory() as session:
            session.add_all(entities_orm)
            session.flush()
            entities = list(map(self._from_orm, entities_orm))
            session.commit()

        return entities

    def get_by_id(self, entity_id: int) -> LLMResponse | None:
        with self._session_factory() as session:
            entity_orm = session.get(LLMResponseOrm, entity_id)

        if not entity_orm:
            return None

        return self._from_orm(entity_orm)

    def get_all(self):
        stmt = select(LLMResponseOrm)
        with self._session_factory() as session:
            entities_orm = list(session.execute(stmt).scalars())

        return list(map(self._from_orm, entities_orm))

    def update(self, entity: LLMResponse) -> LLMResponse:
        if entity.id is None:
            raise ValueError("Для изменения сущности нужен id")

        with self._session_factory() as session:
            entity_orm = session.get(LLMResponseOrm, entity.id)

            entity_orm.task_id = entity.task_id
            entity_orm.llm_id = entity.llm_id
            entity_orm.response = entity.response
            entity_orm.created_at = entity.created_at

            session.commit()
            session.refresh(entity_orm)
            entity = self._from_orm(entity_orm)
            return entity

    def delete(self, entity_id: LLMResponse) -> bool:
        with self._session_factory() as session:
            entity_orm = session.get(LLMResponseOrm, entity_id)
            if not entity_orm:
                return False

            session.delete(entity_orm)
            session.commit()
            return True

    def filter_by_llm_id(self, llm_id: int) -> list[LLMResponse]:
        with self._session_factory() as session:
            stmt = select(LLMResponseOrm).where(LLMResponseOrm.llm_id == llm_id)
            responses_orm = session.execute(stmt).scalars().all()
            responses = list(map(self._from_orm, responses_orm))
            return responses

    def filter_by_task_id(self, task_id: int) -> list[LLMResponse]:
        with self._session_factory() as session:
            stmt = select(LLMResponseOrm).where(LLMResponseOrm.task_id == task_id)
            responses_orm = session.execute(stmt).scalars().all()
            responses = list(map(self._from_orm, responses_orm))
            return responses
