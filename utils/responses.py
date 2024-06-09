from typing import Optional, Sequence, TypeVar, Union, Generic
from pydantic import BaseModel
from abc import ABC


T = TypeVar("T", bound=Union[BaseModel, Sequence[BaseModel], None])


class JSONResponse(BaseModel, ABC, Generic[T]):
    content: Optional[T]
