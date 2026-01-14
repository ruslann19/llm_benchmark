from bs4 import BeautifulSoup
import html


def extract_text_from_html_block(html_string, post_message):
    # Парсим HTML
    soup = BeautifulSoup(html_string, "html.parser")

    # Находим нужный блок по id
    id = f"post_message_{post_message}"
    block = soup.find("div", id=id)
    if not block:
        raise ValueError(f"Блок с id='{id}' не найден")

    # Заменяем <br> на '\n', чтобы сохранить разрывы строк
    for br in block.find_all("br"):
        br.replace_with("")

    # Получаем текст — удаляем лишние пробелы/отступы, но сохраняем '\n'
    text = block.get_text(separator="", strip=False)

    # Декодируем HTML-сущности (например, &nbsp; → пробел, &lt; → <)
    text = html.unescape(text)

    # Убираем лишние пустые строки (опционально)
    lines = [line.rstrip() for line in text.splitlines()]

    # Удаляем дублирующиеся пустые строки, оставляя по 1
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if line == "":
            if not prev_empty:
                cleaned_lines.append(line)
            prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False

    return "\n".join(cleaned_lines)
