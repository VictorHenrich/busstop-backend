from typing import Optional, Union, Sequence, TypeVar, Generic
from abc import ABC
from pydantic import BaseModel
from enum import Enum


M = TypeVar("M", bound=Union[BaseModel, Sequence[BaseModel], None])


class JSONDataTypes(Enum):
    SUCCESS = "success"
    ERROR = "error"
    UNAUTHORIZED = "unauthorized"


class JSONDataEntity(BaseModel, ABC, Generic[M]):
    info: JSONDataTypes
    content: Optional[M]


class UUIDEntity(BaseModel):
    uuid: str


class IndexEntity(BaseModel):
    version: str = "1.0"
    name: str = "APPLICATION"
    description: str = "APLICATION RUNNING"


class CompanyBodyEntity(BaseModel):
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyEntity(CompanyBodyEntity, UUIDEntity):
    pass
