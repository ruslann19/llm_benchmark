from interfaces import LLMClient
from infrastructure import settings
from openai import OpenAI
from .question_params import question_header


class DeepSeekClient(LLMClient):
    def __init__(self, llm_id: int) -> None:
        self._llm_id = llm_id

    def ask(self, question: str) -> str:
        client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        )

        content = question_header + question

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": content},
            ],
            stream=False,
        )

        return response.choices[0].message.content

    @property
    def llm_id(self) -> int:
        return self._llm_id
