from dotenv import dotenv_values


class Settings:
    def __init__(self):
        config = dotenv_values(".env")
        self._openrouter_api_key = config["OPENROUTER_API_KEY"]
        self._deepseek_api_key = config["DEEPSEEK_API_KEY"]
        self._gigachat_api_key = config["GIGACHAT_API_KEY"]

        self._db_name = config["DB_NAME"]
        self._db_host = config["DB_HOST"]
        self._db_port = config["DB_PORT"]
        self._db_user = config["DB_USER"]
        self._db_password = config["DB_PASSWORD"]

    @property
    def DB_URL(self) -> str:
        return f"postgresql://{self._db_user}:{self._db_password}@{self._db_host}:{self._db_port}/{self._db_name}"

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
