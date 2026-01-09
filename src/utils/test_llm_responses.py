from utils.output import print_with_padding
from domain import LLMInfo, Task, LLMResponse
from infrastructure.database import (
    SqlDatabase,
    SqlTaskRepository,
    SqlLLMInfoRepository,
    SqlLLMResponseRepository,
)
from datetime import date


import random
import string


def generate_random_string(length):
    # Define the possible characters: lowercase, uppercase letters, and digits
    characters = string.ascii_letters + string.digits
    # Use random.choices to select characters with replacement
    random_string = "".join(random.choices(characters, k=length))
    return random_string


# # Example usage:
# length = 10
# print(f"Random string: {generate_random_string(length)}")


def run():
    db_name = "llm_benchmark.db"

    database = SqlDatabase(db_name)
    database.drop_tables()
    database.create_tables()

    task_repo = SqlTaskRepository(db_name)
    llm_repo = SqlLLMInfoRepository(db_name)
    responses_repo = SqlLLMResponseRepository(db_name)

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

    llm_infos = [
        LLMInfo(
            name="GPT-6",
            provider="OpenAI",
            api_url="open-ai/models/gpt-6",
        ),
        LLMInfo(
            name="DeepSeek-R3",
            provider="DeepSeek",
            api_url="deepseek/models/deepseek-r3",
        ),
        LLMInfo(
            name="Qwen3-Max",
            provider="Alibaba",
            api_url="alibaba/models/qwen3-max",
        ),
        LLMInfo(
            name="Gemini 3",
            provider="Google",
            api_url="google/models/gemini-3",
        ),
    ]

    # -----------------------------------------

    print_with_padding("Добавление данных", end="\n\n")

    for task in tasks:
        task_repo.add(task)

    for llm_info in llm_infos:
        llm_repo.add(llm_info)

    persisted_tasks = task_repo.get_all()
    print(f"Tasks: {len(persisted_tasks)}")

    random_task_id = random.choice(range(1, len(tasks) + 1))
    random_task = task_repo.get_by_id(random_task_id)
    print(f"Random task: {random_task}\n")

    persisted_llms = llm_repo.get_all()
    print(f"LLMs: {len(persisted_llms)}")

    random_llm_id = random.choice(range(1, len(llm_infos) + 1))
    random_llm = llm_repo.get_by_id(random_llm_id)
    print(f"Random LLM: {random_llm}\n")

    RESPONSE_LENGTH = 10
    RESPONSES = 10
    for i in range(RESPONSES):
        current_task_id = random.choice(range(1, len(tasks) + 1))
        current_llm_id = random.choice(range(1, len(llm_infos) + 1))
        response = generate_random_string(RESPONSE_LENGTH)
        llm_response = LLMResponse(
            task_id=current_task_id,
            llm_id=current_llm_id,
            response=response,
            created_at=date.today(),
        )
        responses_repo.add(llm_response)

    persisted_responses = responses_repo.get_all()
    print(f"Responses: {len(persisted_responses)}")
    random_response_id = random.choice(range(1, RESPONSES + 1))
    random_response = responses_repo.get_by_id(random_response_id)
    print(f"Random response: {random_response}\n")
    print(f"Random task responses: {responses_repo.filter_by_task_id(random_task_id)}")
    print(f"Random LLM responses: {responses_repo.filter_by_task_id(random_llm_id)}\n")

    # ------------------------------------------

    print_with_padding("Обновление данных", end="\n\n")

    random_response.response = "Теперь ответ будет такой!"
    random_response = responses_repo.update(random_response)
    print(f"{random_response=}")
    random_response = responses_repo.get_by_id(random_response_id)
    print(f"{random_response=}")
    print(f"Responses: {len(responses_repo.get_all())}\n")

    # # ------------------------------------------

    print_with_padding("Удаление данных", end="\n\n")

    for response in responses_repo.get_all():
        llm_repo.delete(response.id)

    random_response = llm_repo.get_by_id(random_response_id)
    print(f"{random_response=}")
    print(f"Responses: {len(responses_repo.get_all())}")
