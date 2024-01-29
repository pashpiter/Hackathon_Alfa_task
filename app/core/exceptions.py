from http import HTTPStatus
from typing import Any, Dict, Optional
from typing_extensions import Annotated, Doc

from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.NOT_FOUND, message)


class ForbiddenException(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class IncorrectDate(HTTPException):
    def __init__(self, message: str):   
        super().__init__(HTTPStatus.FORBIDDEN, message)
