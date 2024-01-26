from pydantic import Field
from pydantic_settings import BaseSettings

"""
Базовые классы настроек, по необходимости можно расширять.
DEBUG можно использовать для разнообразной логики, например:
в db/database.py при создании движка - выводить/не выводить запросы в консоль.
"""


class AppSettings(BaseSettings):
    debug: bool = Field(False, alias='DEBUG')


class PostgresSettings(BaseSettings):
    host: str = Field('localhost', alias='POSTGRES_HOST')
    port: int = Field(5432, alias='POSTGRES_PORT')
    user: str = Field('user', alias='POSTGRES_USER')
    password: str = Field('password', alias='POSTGRES_PASSWORD')
    db_name: str = Field('database', alias='POSTGRES_DB')
    schema: str = Field('plans', alias='POSTGRES_SCHEMA')

    @property
    def database_url(self) -> str:
        return 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.db_name
        )


class Settings:
    app: AppSettings = AppSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
