from dataclasses import dataclass


@dataclass
class LLMInfo:
    name: str
    provider: str
    api_url: str
    id: int | None = None
