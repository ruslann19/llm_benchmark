from dotenv import dotenv_values


class Settings:
    def __init__(self):
        config = dotenv_values(".env")
        self._db_name = config["DB_NAME"]
        self._openrouter_api_key = config["OPENROUTER_API_KEY"]
        self._deepseek_api_key = config["DEEPSEEK_API_KEY"]
        self._gigachat_api_key = config["GIGACHAT_API_KEY"]

    @property
    def DB_URL(self) -> str:
        return f"sqlite:///{self._db_name}.db"

    @property
    def OPENROUTER_API_KEY(self) -> int:
        return self._openrouter_api_key

    @property
    def DEEPSEEK_API_KEY(self) -> int:
        return self._deepseek_api_key

    @property
    def GIGACHAT_API_KEY(self) -> int:
        return self._gigachat_api_key


settings = Settings()
