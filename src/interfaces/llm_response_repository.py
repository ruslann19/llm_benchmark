from interfaces import Repository
from domain import LLMResponse
from abc import abstractmethod


class LLMResponseRepository(Repository[LLMResponse]):
    @abstractmethod
    def filter_by_llm_id(self, llm_id: int) -> list[LLMResponse]:
        raise NotImplementedError

    @abstractmethod
    def filter_by_task_id(self, task_id: int) -> list[LLMResponse]:
        raise NotImplementedError
