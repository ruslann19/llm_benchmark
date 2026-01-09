from src.utils.output import print_with_padding
from domain import Task
from infrastructure.database import (
    InMemoryTaskRepository,
    SqlTaskRepository,
    SqlDatabase,
)
from datetime import date


def run_tasks():
    # repository = InMemoryTaskRepository()
    db_name = "llm_benchmark.db"
    # database = SqlDatabase(db_name)
    # database.drop_tables()
    # database.create_tables()
    repository = SqlTaskRepository(db_name)
    tasks = [
        Task(
            question="Какое сегодня число?",
            answer="08.01.2026",
            source_url="datetime.com",
            published_at=date.today(),
            state="on_validation",
        ),
        Task(
            question="Какая столица России?",
            answer="Москва",
            source_url="questions.com",
            published_at=date.today(),
            state="on_validation",
        ),
        Task(
            question="Существует ли Дед Мороз?",
            answer="Да",
            source_url="happy-new-year.com",
            published_at=date.today(),
            state="on_validation",
        ),
    ]

    for task in tasks:
        repository.add(task)

    # for task in repository.get_all():
    #     task_id = task.id
    #     repository.delete(task_id)

    tasks = repository.get_all()
    if len(tasks) != 0:
        selected_task = tasks[0]
        task_id = selected_task.id
    else:
        task_id = 0

    state_changes = []
    for task in tasks:
        current_task_id = task.id
        state_changes.append(repository.get_state_changes(current_task_id))

    print(f"Tasks: {len(tasks)}")
    print(f"State changes: {len(state_changes)}")

    print_with_padding("После вставки всех данных", end="\n")
    print(f"{repository.get_by_id(task_id)=}")
    print(f"{repository.get_state_changes(task_id)=}\n")

    selected_task.state = "queue"
    repository.update(selected_task)
    selected_task.state = "benchmark"
    repository.update(selected_task)
    selected_task.state = "archive"
    repository.update(selected_task)

    print_with_padding("После изменения состояния", end="\n")
    print(f"{repository.get_by_id(task_id)=}")
    print(f"{repository.get_state_changes(task_id)=}\n")

    repository.delete(task_id)

    print_with_padding("После удаления задачи", end="\n")
    print(f"{repository.get_by_id(task_id)=}")
    print(f"{repository.get_state_changes(task_id)=}\n")
