from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure import settings
from infrastructure.repository import (
    SqlTaskRepository,
    SqlLLMInfoRepository,
    SqlLLMResponseRepository,
    SqlDatabase,
)
from domain import Task, LLMInfo, LLMResponse


# Подключение к БД
engine = create_engine(
    url=settings.DB_URL,
    echo=True,
)
database = SqlDatabase(engine)
session_factory = sessionmaker(engine)


database.drop_tables()
database.create_tables()


llm_repo = SqlLLMInfoRepository(session_factory)
task_repo = SqlTaskRepository(session_factory)
response_repo = SqlLLMResponseRepository(session_factory)


tasks = [
    Task(
        question="Какой сегодня день?",
        answer="Отличный",
        source_url="weather.com",
    ),
    Task(
        question="Какая столица в России?",
        answer="Москва",
        source_url="geographics.com",
    ),
]
task_repo.add_all(tasks)

llm_infos = [
    LLMInfo(
        name="Qwen",
        provider="Yandex",
        api_url="open-ai.com/chat-gpt",
    ),
    LLMInfo(
        name="DeepSeek",
        provider="DeepSeek",
        api_url="open-router/chat-gpt",
    ),
]
llm_repo.add_all(llm_infos)

llm_responses = [
    LLMResponse(
        task_id=1,
        llm_id=1,
        response="Суперский",
    ),
    LLMResponse(
        task_id=1,
        llm_id=1,
        response="Отличный",
    ),
    LLMResponse(
        task_id=1,
        llm_id=2,
        response="Крутой",
    ),
    LLMResponse(
        task_id=2,
        llm_id=1,
        response="Париж",
    ),
    LLMResponse(
        task_id=2,
        llm_id=2,
        response="Лондон",
    ),
]
response_repo.add_all(llm_responses)


output = response_repo.filter_by_task_id(task_id=2)
print(f"{output=}")
