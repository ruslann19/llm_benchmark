from abc import ABC, abstractmethod


class LLMResponseJudge(ABC):
    @abstractmethod
    def is_correct(
        self,
        question: str,
        answer: str,
        response: str,
    ) -> bool:
        raise NotImplementedError
