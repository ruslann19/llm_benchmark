from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure import settings
from infrastructure.repository import (
    SqlTaskRepository,
    SqlDatabase,
)
from infrastructure.task_maker import LLMTaskGenerator, YourOwnGameLoader
from use_cases import TaskCollector
import argparse


# Подключение к БД
engine = create_engine(
    url=settings.DB_URL,
    # echo=True,
    echo=False,
)
database = SqlDatabase(engine)
session_factory = sessionmaker(engine)


# database.drop_tables()
# database.create_tables()


task_repository = SqlTaskRepository(session_factory)


def main():
    parser = argparse.ArgumentParser(description="CLI для управления задачами.")

    # Опция --task с выбором из допустимых значений
    parser.add_argument(
        "--task",
        required=True,
        choices=["collect_tasks", "update_benchmark"],
        help="Выберите задачу для выполнения",
    )

    # Опция --url (не обязательная по умолчанию)
    parser.add_argument(
        "--url", help="URL для сбора задач (требуется только для collect_tasks)"
    )

    args = parser.parse_args()

    # Валидация: если задача — collect_tasks, то url обязателен
    if args.task == "collect_tasks":
        if not args.url:
            parser.error("--url обязателен при --task=collect_tasks")

    # Выполнение логики
    if args.task == "collect_tasks":
        print(f"Сбор задач с URL: {args.url}")
        task_collector = TaskCollector(
            text_loader=YourOwnGameLoader(),
            task_generator=LLMTaskGenerator(),
            task_repository=task_repository,
        )
        task_collector.collect_tasks(url=args.url)

    elif args.task == "update_benchmark":
        print("Обновление бенчмарка")
        updated_success = True
        try:
            task_repository.update_benchmark()
        except ValueError as error:
            updated_success = False
            print(f"Возникла ошибка: {error}")

        if updated_success:
            print("Запуск тестирования")
            # run_testing()


if __name__ == "__main__":
    main()
