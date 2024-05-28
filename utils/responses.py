from typing import Mapping, Optional, Sequence, TypeVar, Generic, Union
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from abc import ABC

from utils.entities import JSONDataEntity, JSONDataTypes


T = TypeVar("T", bound=Union[BaseModel, Sequence[BaseModel], None])


class BaseJSONResponse(JSONResponse, ABC, Generic[T]):
    def __init__(
        self,
        content: T,
        info: JSONDataTypes,
        status_code: int,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self.__data: JSONDataEntity = JSONDataEntity(info=info, content=content)

        super().__init__(self.__data, status_code, headers, None, None)

    @property
    def data(self) -> JSONDataEntity[T]:
        return self.__data


class SuccessJSONResponse(BaseJSONResponse[T]):
    def __init__(
        self, content: T = None, headers: Optional[Mapping[str, str]] = None
    ) -> None:
        super().__init__(content, JSONDataTypes.SUCCESS, 200, headers)


class ErrorJSONResponse(BaseJSONResponse[T]):
    def __init__(
        self, content: T = None, headers: Optional[Mapping[str, str]] = None
    ) -> None:
        super().__init__(content, JSONDataTypes.ERROR, 500, headers)


class UnauthorizedJSONResponse(BaseJSONResponse[T]):
    def __init__(
        self, content: T = None, headers: Optional[Mapping[str, str]] = None
    ) -> None:
        super().__init__(content, JSONDataTypes.UNAUTHORIZED, 400, headers)
