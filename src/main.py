from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure import settings
from infrastructure.repository import (
    SqlTaskRepository,
    SqlLLMInfoRepository,
    SqlLLMResponseRepository,
    SqlDatabase,
)
from domain import (
    Task,
    LLMInfo,
    LLMResponse,
    ON_VALIDATION_STATE,
    QUEUE_STATE,
    BENCHMARK_STATE,
    ARCHIVE_STATE,
)


# Подключение к БД
engine = create_engine(
    url=settings.DB_URL,
    # echo=True,
    echo=False,
)
database = SqlDatabase(engine)
session_factory = sessionmaker(engine)


database.drop_tables()
database.create_tables()


task_repo = SqlTaskRepository(session_factory)

tasks = [
    Task(
        question="Сынок, ты покушал?",
        answer="Да",
        state=QUEUE_STATE,
    ),
    Task(
        question="Кто здесь?",
        answer="Никого",
        state=QUEUE_STATE,
    ),
    Task(
        question="Какой сегодня день?",
        answer="Отличный",
        state=QUEUE_STATE,
    ),
    Task(
        question="2 + 2 = ?",
        answer="4",
        state=QUEUE_STATE,
    ),
    Task(
        question="Кто убил Марка?",
        answer="Не знаю",
        state=QUEUE_STATE,
    ),
    Task(
        question="Что лучше: бакалавриат или факультет?",
        answer="Я думаю, что факультет",
        state=QUEUE_STATE,
    ),
    Task(
        question="Дорогой, где ты был?",
        answer="Бегал",
        state=QUEUE_STATE,
    ),
    Task(
        question="В чём секрет успеха?",
        answer="Дисциплина",
        state=QUEUE_STATE,
    ),
]

task_repo.add_all(tasks)
for i in range(4):
    task_repo.update_benchmark()

    benchmark_tasks = task_repo.filter_by_state(state="benchmark")
    print(benchmark_tasks, "\n")
