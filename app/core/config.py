import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

"""
Базовые классы настроек, по необходимости можно расширять.
DEBUG можно использовать для разнообразной логики, например:
в db/database.py при создании движка - выводить/не выводить запросы в консоль.
"""

BASE_DIR: Path = Path(__file__).parent.parent
LOG_DIR: Path = BASE_DIR / 'logs'


class AppSettings(BaseSettings):
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        super().__init__()
    name: str = Field('ИПР для сотрудников Альфа-Банка', alias='APP_NAME')
    debug: bool = Field(False, alias='DEBUG')


class LoggingSettings(BaseSettings):
    log_file: Path = LOG_DIR / 'plans.log'
    log_format: str = '%(asctime)s - [%(levelname)s] - [%(name)s] - %(message)s'  # noqa:E501
    dt_format: str = '%d.%m.%Y %H:%M:%S'
    debug: bool = Field(True, alias='DEBUG')


class PostgresSettings(BaseSettings):
    host: str = Field('localhost', alias='POSTGRES_HOST')
    port: int = Field(5432, alias='POSTGRES_PORT')
    user: str = Field('user', alias='POSTGRES_USER')
    password: str = Field('password', alias='POSTGRES_PASSWORD')
    db_name: str = Field('database', alias='POSTGRES_DB')
    db_schema: str = Field('plans', alias='POSTGRES_SCHEMA')

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
    logging: LoggingSettings = LoggingSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
