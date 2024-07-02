from typing import Type
from sqlalchemy.orm.decl_api import DeclarativeBase
from fastapi.exceptions import HTTPException

from models import UserBaseModel


class ModelNotFound(BaseException):
    def __init__(self, model_class: Type[DeclarativeBase], uuid: str) -> None:
        super().__init__(f"{model_class.__name__} with uuid: '{uuid}' was not found!")


class UserNotFound(BaseException):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with email '{email}' was not found")


class InvalidUserPassword(BaseException):
    def __init__(self, user: UserBaseModel) -> None:
        super().__init__(f"Invalid password passed to user {user.uuid}")


class InvalidToken(BaseException):
    def __init__(self, token: str) -> None:
        super().__init__(f"Passed token is invalid: '{token}'")


class HTTPFailure(HTTPException):
    def __init__(self, error_message: str) -> None:
        super().__init__(500, error_message)
