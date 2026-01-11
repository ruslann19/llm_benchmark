from dataclasses import dataclass


@dataclass
class LLMResponse:
    task_id: int
    llm_id: int
    response: str
    id: int | None = None
