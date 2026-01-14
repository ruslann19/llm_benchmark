from interfaces import LLMClient
from infrastructure import settings
from openai import OpenAI


class DeepSeekClient(LLMClient):
    def __init__(self, llm_id: int) -> None:
        self._llm_id = llm_id

    def ask(self, question: str) -> str:
        client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        )

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": question},
            ],
            stream=False,
        )

        return response.choices[0].message.content

    @property
    def llm_id(self) -> int:
        return self._llm_id

    def __repr__(self) -> str:
        return f"DeepSeekClient(llm_id={self.llm_id})"
