from src.domain.models import Task, LLMInfo, LLMResponse
from src.domain.interfaces import LLMAPI


class EvaluateLLMsUseCase:
    def __init__(
        self,
        tasks: list[Task],
        llm_apis: list[LLMInfo],
    ) -> None:
        self._tasks: list[Task] = tasks
        self._llm_apis: list[LLMAPI] = llm_apis

    def run(self) -> list[LLMResponse]:
        for llm_api in self._llm_apis:
            responses: list[LLMResponse] = []

            for task in self._tasks:
                question = self._create_question_with_prompt(task.question)
                task_response = llm_api.ask(question)
                llm_response = LLMResponse(
                    task_id=task.id,
                    llm_id=llm_api.llm_id,
                    task_response=task_response,
                )
                responses.append(llm_response)

        return responses

    def _create_question_with_prompt(self, question: str) -> str:
        prompt = """
            Hello, how are you?
            Are you here?
        """
        return prompt + question
