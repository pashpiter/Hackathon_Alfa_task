from http import HTTPStatus

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


class AlreadyExists(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.CONFLICT, message)
