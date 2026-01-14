from interfaces import TextLoader
from infrastructure.task_maker.html_processing import extract_text_from_html_block
import requests
from urllib.parse import urlparse, parse_qs


class YourOwnGameLoader(TextLoader):
    def __init__(self):
        super().__init__()

    def get_raw_text(self, url: str) -> str:
        # Разбираем URL
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # вызовет исключение при 4xx/5xx
            html_content = response.text
        except requests.exceptions.RequestException as error:
            print("Ошибка загрузки:", error)

        text = extract_text_from_html_block(
            html_content, post_message=query_params["p"][0]
        )

        return text

        # with open("./data/aux/game.txt", "w", encoding="utf-8") as f:
        #     f.write(text)
        # print(text)
