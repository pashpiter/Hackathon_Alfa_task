"""empty message

Revision ID: d07d97a7e584
Revises: c20ee987ab46a
Create Date: 2024-01-29 17:12:59.561223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd07d97a7e584'
down_revision: Union[str, None] = 'c20ee987ab46a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE plans.user ADD COLUMN photo varchar')


def downgrade() -> None:
    op.execute('ALTER TABLE plans.user DROP COLUMN photo RESTRICT')
