from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from server.instances import ServerInstances
from server.database import Database
from models import Company, Point
from repositories.point import PointRepository, PointListingRepositoryProps
from repositories.company import CompanyRepository, CompanyCaptureRepositoryProps
from utils.patterns import (
    IFindRepository,
    IService,
    IFindManyRepository,
    AbstractBaseEntity,
)
from utils.constants import DATABASE_INSTANCE_NAME


class CompanyCaptureProps(AbstractBaseEntity):
    uuid: str


class PointListingProps(AbstractBaseEntity):
    company: Company

    uuids: Sequence[str]


class PointListingService(IService[Sequence[Point]]):
    def __init__(self, company_uuid: str, uuids: Sequence[str] = []) -> None:
        self.__company_uuid: str = company_uuid

        self.__uuids: Sequence[str] = uuids

    async def __find_company(self, session: AsyncSession) -> Company:
        company_repository: IFindRepository[
            CompanyCaptureRepositoryProps, Company
        ] = CompanyRepository(session)

        capture_props: CompanyCaptureRepositoryProps = CompanyCaptureProps(
            uuid=self.__company_uuid
        )

        company: Optional[Company] = await company_repository.find(capture_props)

        if not company:
            raise Exception("Company not found!")

        return company

    async def __find_points(
        self, session: AsyncSession, company: Company
    ) -> Sequence[Point]:
        data: PointListingProps = PointListingProps(company=company, uuids=self.__uuids)

        company_repository: IFindManyRepository[
            PointListingRepositoryProps, Point
        ] = PointRepository(session)

        return await company_repository.find_many(data)

    async def execute(self) -> Sequence[Point]:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company: Company = await self.__find_company(session)

            return await self.__find_points(session, company)
