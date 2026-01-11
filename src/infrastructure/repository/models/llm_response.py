from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.repository.models import Base
from sqlalchemy import ForeignKey
from datetime import datetime
from domain import LLMResponse


class LLMResponseOrm(Base):
    __tablename__ = "llm_responses"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    llm_id: Mapped[int] = mapped_column(ForeignKey("llm_infos.id", ondelete="CASCADE"))
    response: Mapped[str]
    created_at: Mapped[datetime]

    task: Mapped["TaskOrm"] = relationship(back_populates="llm_responses")  # noqa: F821

    llm_info: Mapped["LLMInfoOrm"] = relationship(back_populates="llm_responses")  # noqa: F821


def llm_response_to_orm(llm_response: LLMResponse) -> LLMResponseOrm:
    return LLMResponseOrm(
        id=llm_response.id,
        task_id=llm_response.task_id,
        llm_id=llm_response.llm_id,
        response=llm_response.response,
        created_at=llm_response.created_at,
    )


def llm_response_from_orm(llm_response_orm: LLMResponseOrm) -> LLMResponse:
    return LLMResponse(
        id=llm_response_orm.id,
        task_id=llm_response_orm.task_id,
        llm_id=llm_response_orm.llm_id,
        response=llm_response_orm.response,
        created_at=llm_response_orm.created_at,
    )
