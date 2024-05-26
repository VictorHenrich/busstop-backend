from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from models import Route, Company, database
from repositories.route import RouteRepository, RouteListingRepositoryProps
from repositories.company import CompanyRepository, CompanyCaptureRepositoryProps
from utils.patterns import (
    IService,
    IFindManyRepository,
    IFindRepository,
    AbstractBaseEntity,
)
from utils.exceptions import ModelNotFound


class RouteListingProps(AbstractBaseEntity):
    company: Company


class CompanyCaptureProps(AbstractBaseEntity):
    uuid: str


class RouteListingService(IService[Sequence[Route]]):
    def __init__(self, company_uuid: str) -> None:
        self.__company_uuid: str = company_uuid

    async def __find_company(self, session: AsyncSession) -> Company:
        company_repository: IFindRepository[
            CompanyCaptureRepositoryProps, Company
        ] = CompanyRepository(session)

        company_props: CompanyCaptureRepositoryProps = CompanyCaptureProps(
            uuid=self.__company_uuid
        )

        company: Optional[Company] = await company_repository.find(company_props)

        if not company:
            raise ModelNotFound(Company, self.__company_uuid)

        return company

    async def __find_routes(
        self, session: AsyncSession, company: Company
    ) -> Sequence[Route]:
        route_repository: IFindManyRepository[
            RouteListingRepositoryProps, Optional[Route]
        ] = RouteRepository(session)

        route_props: RouteListingRepositoryProps = RouteListingProps(company=company)

        return await route_repository.find_many(route_props)

    async def execute(self) -> Sequence[Route]:
        async with database.create_async_session() as session:
            company: Company = await self.__find_company(session)

            return await self.__find_routes(session, company)
