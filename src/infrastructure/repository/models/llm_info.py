from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.repository.models import Base
from domain import LLMInfo


class LLMInfoOrm(Base):
    __tablename__ = "llm_infos"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    provider: Mapped[str]
    api_url: Mapped[str]

    llm_responses: Mapped[list["LLMResponseOrm"]] = relationship(  # noqa: F821
        back_populates="llm_info",
        cascade="all, delete-orphan",
    )


def llm_info_to_orm(llm_info: LLMInfo) -> LLMInfoOrm:
    return LLMInfoOrm(
        id=llm_info.id,
        name=llm_info.name,
        provider=llm_info.provider,
        api_url=llm_info.api_url,
    )


def llm_info_from_orm(llm_info_orm: LLMInfoOrm) -> LLMInfo:
    return LLMInfo(
        id=llm_info_orm.id,
        name=llm_info_orm.name,
        provider=llm_info_orm.provider,
        api_url=llm_info_orm.api_url,
    )
