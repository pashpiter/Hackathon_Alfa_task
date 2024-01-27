# flake8: noqa: VNE003
from typing import Optional

from sqlmodel import Field

PK_TYPE = int
USER_PK_TYPE = int


class PrimaryKey:
    """Класс для добавления id(pk) к схемам"""
    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
