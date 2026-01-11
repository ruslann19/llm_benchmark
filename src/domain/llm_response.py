from dataclasses import dataclass
from datetime import datetime


@dataclass
class LLMResponse:
    task_id: int
    llm_id: int
    response: str
    created_at: datetime = datetime.now()
    id: int | None = None
