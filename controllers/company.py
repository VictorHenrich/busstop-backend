from typing import Sequence, Optional, List

from server.instances import ServerInstances
from services.company.creation import CompanyCreationService
from services.company.update import CompanyUpdateService
from services.company.exclusion import CompanyExclusionService
from services.company.capture import CompanyCaptureService
from services.company.listing import CompanyListingService
from models import Company
from utils.responses import SuccessJSONResponse, JSONBaseResponse
from utils.patterns import IService
from utils.entities import CompanyEntity, CompanyBodyEntity
from utils.constants import COMPANY_ENPOINT_NAME


@ServerInstances.api.get(f"{COMPANY_ENPOINT_NAME}")
async def list_companies(
    page: int = 0, limit: int = 10, company_name: Optional[str] = None
) -> JSONBaseResponse[List[CompanyEntity]]:
    company_listing_service: IService[Sequence[Company]] = CompanyListingService(
        company_name=company_name, limit=limit, page=page
    )

    companies: Sequence[Company] = await company_listing_service.execute()

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

    return SuccessJSONResponse(content=companies_handled)


@ServerInstances.api.get(f"{COMPANY_ENPOINT_NAME}/{{company_uuid}}")
async def get_company(company_uuid: str) -> JSONBaseResponse[Optional[CompanyEntity]]:
    company_capture_service: IService[Optional[Company]] = CompanyCaptureService(
        company_uuid
    )

    company: Optional[Company] = await company_capture_service.execute()

    company_handled: Optional[CompanyEntity] = None

    if company:
        company_handled = CompanyEntity(
            uuid=company.uuid,
            company_name=company.company_name,
            fantasy_name=company.fantasy_name,
            document_cnpj=company.document_cnpj,
            email=company.email,
        )

    return SuccessJSONResponse(content=company_handled)


@ServerInstances.api.post(f"{COMPANY_ENPOINT_NAME}")
async def create_company(company_body: CompanyBodyEntity) -> JSONBaseResponse[None]:
    company_creation_service: IService[None] = CompanyCreationService(
        company_name=company_body.company_name,
        fantasy_name=company_body.fantasy_name,
        document_cnpj=company_body.document_cnpj,
        email=company_body.email,
    )

    await company_creation_service.execute()

    return SuccessJSONResponse()


@ServerInstances.api.put(f"{COMPANY_ENPOINT_NAME}/{{company_uuid}}")
async def update_company(
    company_uuid: str, company_body: CompanyBodyEntity
) -> JSONBaseResponse[None]:
    company_update_service: IService[None] = CompanyUpdateService(
        uuid=company_uuid,
        company_name=company_body.company_name,
        fantasy_name=company_body.fantasy_name,
        document_cnpj=company_body.document_cnpj,
        email=company_body.email,
    )

    await company_update_service.execute()

    return SuccessJSONResponse()


@ServerInstances.api.delete(f"/{COMPANY_ENPOINT_NAME}/{{company_uuid}}")
async def delete_company(company_uuid: str) -> JSONBaseResponse[None]:
    company_exclusion_service: IService[None] = CompanyExclusionService(company_uuid)

    await company_exclusion_service.execute()

    return SuccessJSONResponse()
