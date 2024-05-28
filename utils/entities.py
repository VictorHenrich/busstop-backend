from pydantic import BaseModel


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
