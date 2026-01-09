def get_data_from_page(page_url: str, domain_url: str):
    match domain_url:
        case "Своя игра":
            page_data: str = None
            ...  # извлекаем данные из своей игры

        case "Какие-то новости":
            page_data: str = None
            ...  # извлекаем данные из новостей

        case _:
            raise ValueError(f"Invalid domain_url: {domain_url}")

    return page_data
