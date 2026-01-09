from utils.output import print_with_padding
from domain import LLMInfo
from infrastructure.database import SqlDatabase, SqlLLMInfoRepository
from random import choice


def run_llm_info():
    db_name = "llm_benchmark.db"

    database = SqlDatabase(db_name)
    database.drop_tables()
    database.create_tables()

    llm_repo = SqlLLMInfoRepository(db_name)

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

    print_with_padding("Добавление данных")

    for llm_info in llm_infos:
        llm_repo.add(llm_info)

    random_id = choice(range(1, len(llm_infos) + 1))
    random_entity = llm_repo.get_by_id(random_id)
    print(f"{random_entity=}")
    entities = llm_repo.get_all()
    print(f"LLMs: {len(entities)}")

    # ------------------------------------------

    print_with_padding("Обновление данных")

    random_entity.name = "Большой языковой говорун"
    random_entity.provider = "Я тут главный"
    random_entity.api_url = "Где надо, там и находится"
    random_entity = llm_repo.update(random_entity)
    print(f"{random_entity=}")
    random_entity = llm_repo.get_by_id(random_id)
    print(f"{random_entity=}")
    entities = llm_repo.get_all()
    print(f"LLMs: {len(entities)}")

    # ------------------------------------------

    print_with_padding("Удаление данных")

    for task in llm_repo.get_all():
        task_id = task.id
        llm_repo.delete(task_id)

    random_entity = llm_repo.get_by_id(random_id)
    print(f"{random_entity=}")
    entities = llm_repo.get_all()
    print(f"LLMs: {len(entities)}")
