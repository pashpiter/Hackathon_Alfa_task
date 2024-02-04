"""empty message

Revision ID: d07d97a7e584
Revises: c20ee987ab46a
Create Date: 2024-01-29 17:12:59.561223

"""
from typing import Sequence, Union

from alembic import op

from core.config import settings

# revision identifiers, used by Alembic.
revision: str = 'd07d97a7e584'
down_revision: Union[str, None] = 'c20ee987ab46a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
db_schema: str = settings.postgres.db_schema


def upgrade() -> None:
    op.execute(f'ALTER TABLE {db_schema}.user ADD COLUMN photo varchar')


def downgrade() -> None:
    op.execute(f'ALTER TABLE {db_schema}.user DROP COLUMN photo RESTRICT')
