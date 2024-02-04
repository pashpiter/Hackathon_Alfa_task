from pydantic import Field
from pydantic_settings import BaseSettings


class FastapiSettings(BaseSettings):
    host: str = Field('127.0.0.1', alias='SERVER_HOST')
    port: str = Field('8000', alias='SERVER_PORT')

    @property
    def url(self):
        return f'http://{self.host}:{self.port}'


class PostgresSettings(BaseSettings):
    db_name: str = Field('database', alias='POSTGRES_DB')
    host: str = Field('127.0.0.1', alias='POSTGRES_HOST')
    port: int = Field(5432, alias='POSTGRES_PORT')
    user: str = Field('user', alias='POSTGRES_USER')
    password: str = Field('password', alias='POSTGRES_PASSWORD')
    search_path: str = Field('test', alias='POSTGRES_SEARCH_PATH')


class TestSettings(BaseSettings):
    fastapi: FastapiSettings = FastapiSettings()
    postgres: PostgresSettings = PostgresSettings()


test_settings = TestSettings()
