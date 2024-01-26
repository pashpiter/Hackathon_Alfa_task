from sqlmodel import Field
from typing import Optional


PK_TYPE = int
USER_PK_TYPE = int


class PrimaryKey:
    """Класс для добавления id(pk) к схемам"""
    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)