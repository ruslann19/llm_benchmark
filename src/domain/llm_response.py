from dataclasses import dataclass


@dataclass
class LLMResponse:
    task_id: int
    llm_id: int
    response: str
    is_correct: bool | None = None
    id: int | None = None
