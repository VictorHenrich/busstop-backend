from typing import Sequence, Optional, List

from server.instances import ServerInstances
from services.company import CompanyService
from models import Company
from utils.responses import JSONResponse
from utils.entities import CompanyEntity, CompanyBodyEntity
from utils.constants import COMPANY_ENPOINT_NAME
from utils.functions import handle_company_body


@ServerInstances.api.get(COMPANY_ENPOINT_NAME)
async def list_companies(
    page: int = 0, limit: int = 10, company_name: Optional[str] = None
) -> JSONResponse[List[CompanyEntity]]:
    company_service: CompanyService = CompanyService()

    companies: Sequence[Company] = await company_service.find_companies(
        company_name=company_name, limit=limit, page=page
    )

    companies_handled: List[CompanyEntity] = [
        CompanyEntity(
            uuid=company.uuid,
            company_name=company.company_name,
            fantasy_name=company.fantasy_name,
            document_cnpj=company.document_cnpj,
            email=company.email,
        )
        for company in companies
    ]

    return JSONResponse(content=companies_handled)


@ServerInstances.api.get(f"{COMPANY_ENPOINT_NAME}/{{company_uuid}}")
async def get_company(company_uuid: str) -> JSONResponse[Optional[CompanyEntity]]:
    company_service: CompanyService = CompanyService()

    company: Optional[Company] = await company_service.find_company(
        company_uuid=company_uuid
    )

    company_handled: Optional[CompanyEntity] = handle_company_body(company)

    return JSONResponse(content=company_handled)


@ServerInstances.api.post(COMPANY_ENPOINT_NAME)
async def create_company(
    company_body: CompanyBodyEntity,
) -> JSONResponse[Optional[CompanyEntity]]:
    company_service: CompanyService = CompanyService()

    company: Optional[Company] = await company_service.create_company(
        company_name=company_body.company_name,
        fantasy_name=company_body.fantasy_name,
        document_cnpj=company_body.document_cnpj,
        email=company_body.email,
    )

    company_handled: Optional[CompanyEntity] = handle_company_body(company)

    return JSONResponse(content=company_handled)


@ServerInstances.api.put(f"{COMPANY_ENPOINT_NAME}/{{company_uuid}}")
async def update_company(
    company_uuid: str, company_body: CompanyBodyEntity
) -> JSONResponse[Optional[CompanyEntity]]:
    company_service: CompanyService = CompanyService()

    company: Optional[Company] = await company_service.update_company(
        company_uuid=company_uuid,
        company_name=company_body.company_name,
        fantasy_name=company_body.fantasy_name,
        document_cnpj=company_body.document_cnpj,
        email=company_body.email,
    )

    company_handled: Optional[CompanyEntity] = handle_company_body(company)

    return JSONResponse(content=company_handled)


@ServerInstances.api.delete(f"{COMPANY_ENPOINT_NAME}/{{company_uuid}}")
async def delete_company(
    company_uuid: str,
) -> JSONResponse[Optional[CompanyEntity]]:
    company_service: CompanyService = CompanyService()

    company: Optional[Company] = await company_service.delete_company(company_uuid)

    company_handled: Optional[CompanyEntity] = handle_company_body(company)

    return JSONResponse(content=company_handled)
