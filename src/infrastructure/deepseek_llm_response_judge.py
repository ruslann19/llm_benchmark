from interfaces import LLMResponseJudge
from infrastructure.llm_clients import DeepSeekClient


class DeepSeekLLMResponseJudge(LLMResponseJudge):
    def __init__(self):
        with open("./prompt_headers/verify_response.md") as f:
            self._prompt_template = f.read()
        self._deepseek_client = DeepSeekClient(llm_id=None)

    def is_correct(self, question: str, answer: str, response: str) -> bool:
        prompt = self._prompt_template.format(
            question=question,
            answer=answer,
            response=response,
        )
        verdict = self._deepseek_client.ask(prompt)
        result = True if verdict == "OK" else False
        return result
