from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel

from app.config import settings
# Импортируем все модели, для которых необходимо создать миграции.
from app.plan.schemas import *


config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

# Через config можно переопределять параметры, заданные а alembic.ini.
config.set_main_option("sqlalchemy.url", settings.database_URL)

# Важно наследовать все модели от SQLModel, для аккумулирования метадаты.
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """
    Запуск миграций к БД в offline-режиме.
    Не требует создания Engine, только URL БД.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
