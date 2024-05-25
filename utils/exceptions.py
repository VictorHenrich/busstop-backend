from typing import Type
from sqlalchemy.orm.decl_api import DeclarativeBase


class ModelNotFound(BaseException):
    def __init__(self, model_class: Type[DeclarativeBase], uuid: str) -> None:
        super().__init__(f"{model_class.__name__} with uuid: '{uuid}' was not found!")
