from typing import Type
from sqlalchemy.orm.decl_api import DeclarativeBase

from models import Agent


class ModelNotFound(BaseException):
    def __init__(self, model_class: Type[DeclarativeBase], uuid: str) -> None:
        super().__init__(f"{model_class.__name__} with uuid: '{uuid}' was not found!")


class UserNotFound(BaseException):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with email '{email}' was not found")


class InvalidUserPassword(BaseException):
    def __init__(self, agent: Agent) -> None:
        super().__init__(f"Invalid password passed to user {agent.uuid}")
