from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure import settings
from infrastructure.repository import (
    SqlTaskRepository,
    SqlLLMInfoRepository,
    SqlLLMResponseRepository,
)
from infrastructure.task_maker import LLMTaskGenerator, YourOwnGameLoader
from use_cases import TaskCollector, Evaluator
import argparse
from infrastructure.llm_clients import DeepSeekClient
from infrastructure.deepseek_llm_response_judge import DeepSeekLLMResponseJudge


# Подключение к БД
engine = create_engine(
    url=settings.DB_URL,
    # echo=True,
    echo=False,
)

session_factory = sessionmaker(engine)


task_repository = SqlTaskRepository(session_factory)
llm_repository = SqlLLMInfoRepository(session_factory)
response_repository = SqlLLMResponseRepository(session_factory)


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

            llm_names = [
                "DeepSeek",
                "GigaChat",
                "Alice AI",
            ]
            llms = {}
            for name in llm_names:
                llms[name] = llm_repository.get_by_name(name)

            llm_clients = [
                DeepSeekClient(llm_id=llms["DeepSeek"].id),
            ]

            evaluator = Evaluator(
                tasks=task_repository.filter_by_state("benchmark"),
                llm_clients=llm_clients,
                judge=DeepSeekLLMResponseJudge(),
            )
            llm_responses = evaluator.run()
            response_repository.add_all(llm_responses)


if __name__ == "__main__":
    main()

    # import pandas as pd
    # from domain import Task
    # from infrastructure.repository import SqlDatabase

    # database = SqlDatabase(engine)
    # database.drop_tables()
    # database.create_tables()

    # tasks = task_repository.get_all()
    # df = pd.DataFrame(tasks)
    # df.to_csv("tasks.csv")

    # df = pd.read_csv("tasks.csv")

    # tasks = []
    # for task_df in df.values:
    #     task = Task(
    #         question=task_df[1],
    #         answer=task_df[2],
    #         source_url=task_df[5],
    #     )
    #     tasks.append(task)

    # task_repository.add_all(tasks)
