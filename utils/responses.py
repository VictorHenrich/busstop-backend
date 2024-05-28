from typing import Optional, Sequence, TypeVar, Union
from pydantic import BaseModel

from utils.entities import JSONDataEntity, JSONDataTypes


T = TypeVar("T", bound=Union[BaseModel, Sequence[BaseModel], None])


class SuccessJSONResponse(JSONDataEntity[T]):
    info: JSONDataTypes = JSONDataTypes.SUCCESS
    content: Optional[T] = None


class ErrorJSONResponse(JSONDataEntity[T]):
    info: JSONDataTypes = JSONDataTypes.ERROR
    content: Optional[T] = None


class UnauthorizedJSONResponse(JSONDataEntity[T]):
    info: JSONDataTypes = JSONDataTypes.UNAUTHORIZED
    content: Optional[T] = None
