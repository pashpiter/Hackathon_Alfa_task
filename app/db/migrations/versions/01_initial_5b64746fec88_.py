"""empty message

Revision ID: 5b64746fec88
Revises: 
Create Date: 2024-01-25 11:32:34.351286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b64746fec88'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS plans;")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS plans;")