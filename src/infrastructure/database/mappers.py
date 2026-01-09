from domain import Task, LLMInfo, LLMResponse


def tuple_to_task(data: tuple) -> Task:
    return Task(
        id=data[0],
        question=data[1],
        answer=data[2],
        source_url=data[3],
        published_at=data[4],
        state=data[5],
    )


def tuple_to_llm_info(data: tuple) -> LLMInfo:
    return LLMInfo(
        id=data[0],
        name=data[1],
        provider=data[2],
        api_url=data[3],
    )


def tuple_to_llm_response(data: tuple) -> LLMResponse:
    return LLMResponse(
        id=data[0],
        task_id=data[1],
        llm_id=data[2],
        response=data[3],
        created_at=data[4],
    )
