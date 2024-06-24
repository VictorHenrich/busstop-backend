from typing import List
from pydantic import BaseModel
from datetime import datetime, time

from utils.constants import SWAGGER_API_VERSION


class UUIDEntity(BaseModel):
    uuid: str


class IndexEntity(BaseModel):
    version: str = SWAGGER_API_VERSION
    name: str = "APPLICATION"
    description: str = "APLICATION RUNNING"


class CompanyBodyEntity(BaseModel):
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class CompanyEntity(CompanyBodyEntity, UUIDEntity):
    pass


class PointBodyEntity(BaseModel):
    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str


class PointEntity(PointBodyEntity, UUIDEntity):
    pass


class RouteBodyEntity(BaseModel):
    description: str

    opening_time: time

    closing_time: time

    ticket_price: float

    point_uuids: List[str]


class RouteEntity(UUIDEntity):
    description: str
    points: List[PointEntity]


class AgentBodyEntity(BaseModel):
    name: str
    email: str
    password: str


class AgentEntity(AgentBodyEntity, UUIDEntity):
    pass


class AuthRefreshBodyEntity(BaseModel):
    refresh_token: str


class AuthRefreshResultEntity(BaseModel):
    token: str


class AuthResultEntity(BaseModel):
    refresh_token: str
    token: str


class AuthBodyEntity(BaseModel):
    email: str

    password: str


class TokenDataEntity(BaseModel):
    agent_uuid: str
    company_uuid: str
    exp: datetime
    is_refresh: bool
