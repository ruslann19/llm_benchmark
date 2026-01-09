from dotenv import dotenv_values


class Settings:
    def __init__(self):
        config = dotenv_values(".env")
        self._db_name = config["DB_NAME"]

    @property
    def DB_URL(self):
        return f"sqlite:///{self._db_name}.db"


settings = Settings()
