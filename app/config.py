from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Базовые классы настроек, по необходимости можно расширять.
DEBUG можно использовать для разнообразной логики, например:
в db/database.py при создании движка - выводить/не выводить запросы в консоль.
"""


class DevelopmentSettings(BaseSettings):
    database_URL: str = "sqlite:///development.sqlite"
    DEBUG: bool = True


class ProductionSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DEBUG: bool = False

    @property
    def database_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../.env")


settings = DevelopmentSettings()
