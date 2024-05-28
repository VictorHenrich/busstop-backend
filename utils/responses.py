from typing import Optional, Sequence, TypeVar, Union, Generic
from pydantic import BaseModel
from enum import Enum
from abc import ABC


T = TypeVar("T", bound=Union[BaseModel, Sequence[BaseModel], None])


class JSONBaseResponseTypes(Enum):
    SUCCESS = "success"
    ERROR = "error"
    UNAUTHORIZED = "unauthorized"


class JSONBaseResponse(BaseModel, ABC, Generic[T]):
    info: JSONBaseResponseTypes
    content: Optional[T]


class SuccessJSONResponse(JSONBaseResponse[T]):
    info: JSONBaseResponseTypes = JSONBaseResponseTypes.SUCCESS
    content: Optional[T] = None


class ErrorJSONResponse(JSONBaseResponse[T]):
    info: JSONBaseResponseTypes = JSONBaseResponseTypes.ERROR
    content: Optional[T] = None


class UnauthorizedJSONResponse(JSONBaseResponse[T]):
    info: JSONBaseResponseTypes = JSONBaseResponseTypes.UNAUTHORIZED
    content: Optional[T] = None
