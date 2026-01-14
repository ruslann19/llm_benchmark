from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def ask(self, question: str) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def llm_id(self) -> int:
        raise NotImplementedError
