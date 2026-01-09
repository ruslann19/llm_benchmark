from dataclasses import dataclass
from datetime import date


@dataclass
class LLMResponse:
    task_id: int
    llm_id: int
    response: str
    created_at: date
    id: int | None = None
