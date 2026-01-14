from interfaces import TaskGenerator
from domain import Task
from openai import OpenAI
from infrastructure import settings
import json
from tqdm.auto import tqdm


class LLMTaskGenerator(TaskGenerator):
    def __init__(self):
        with open("./prompt_headers/parse_game.md") as f:
            self._prompt_header = f.read()

    def generate_from_text(self, text: str) -> list[Task]:
        client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        )

        content = self._prompt_header + text

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": content},
            ],
            stream=True,
        )

        count = 0
        pbar = tqdm(desc="Обработка объектов")

        tasks = []
        buffer = ""
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                buffer += delta
                # Обрабатываем всё, что можно распарсить до последней незавершённой строки
                lines = buffer.split("\n")
                # Последняя часть может быть неполной — оставляем в буфере
                buffer = lines[-1]

                for line in lines[:-1]:
                    line = line.strip()
                    if line:
                        try:
                            obj = json.loads(line)
                            # Немедленно обрабатываем объект
                            task = Task(
                                question=obj["question"],
                                answer=obj["answer"],
                            )
                            tasks.append(task)

                            pbar.update(1)  # +1 к счётчику
                            count += 1
                        except json.JSONDecodeError:
                            # Не валидный JSON — возможно, модель ещё не закончила строку
                            # Но в корректном JSONL такого не должно быть
                            pass

                # full_response += delta
                # print(delta, end="", flush=True)  # Постепенный вывод

        if buffer.strip():
            try:
                obj = json.loads(buffer.strip())
                task = Task(
                    question=obj["question"],
                    answer=obj["answer"],
                )
                tasks.append(task)

                pbar.update(1)  # +1 к счётчику
                count += 1
            except json.JSONDecodeError:
                print("Остаток буфера не является валидным JSON:", buffer)

        pbar.close()

        print(f"Всего: {count} объектов")

        return tasks
