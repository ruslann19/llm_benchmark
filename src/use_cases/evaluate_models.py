# import os
# import sys

# absolute_path = os.path.abspath("./src/")
# if absolute_path not in sys.path:
#     sys.path.append(absolute_path)

from domain import Task, LLMResponse
from interfaces import LLMClient


class Evaluator:
    def __init__(
        self,
        tasks: list[Task],
        llm_clients: list[LLMClient],
    ) -> None:
        self._tasks = tasks
        self._llm_clients = llm_clients

    def run(self) -> list[LLMResponse]:
        for llm_client in self._llm_clients:
            responses: list[LLMResponse] = []

            for task in self._tasks:
                question = create_question_with_header(task.question)
                task_response = llm_client.ask(question)
                llm_response = LLMResponse(
                    task_id=task.id,
                    llm_id=llm_client.llm_id,
                    task_response=task_response,
                )
                responses.append(llm_response)

        return responses


def create_question_with_header(question: str) -> str:
    filename = "./prompt_headers/question.md"
    with open(filename) as f:
        question_header = f.read()

    content = question_header + question
    return content
