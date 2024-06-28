from typing import Optional, Sequence, TypeVar, Union, Generic
from pydantic import BaseModel

T = TypeVar("T", bound=Union[BaseModel, Sequence[BaseModel], None])


class JSONSuccessResponse(BaseModel, Generic[T]):
    content: Optional[T]


class JSONErrorResponse(BaseModel):
    detail: str


class JSONUnauthorizedResponse(BaseModel):
    detail: str = "Unauthorized"
