from typing import Optional
from pydantic import BaseModel

from models import Company


class CompanyData(BaseModel):
    company_name: str

    fantasy_name: str

    document_cnpj: str

    email: str


class PointData(BaseModel):
    address_zip_code: str

    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str

    place_id: Optional[str] = None

    company: Company


class AgentData(BaseModel):
    name: str

    email: str

    password: str

    company: Company
