from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from server.instances import ServerInstances
from server.database import Database
from models import Company, Point
from repositories.point import PointRepository, PointCreationRepositoryProps
from repositories.company import CompanyRepository, CompanyCaptureRepositoryProps
from utils.patterns import (
    IFindRepository,
    IService,
    ICreateRepository,
    AbstractBaseEntity,
)
from utils.constants import DATABASE_INSTANCE_NAME


class CompanyCaptureProps(AbstractBaseEntity):
    uuid: str


class PointCreationProps(AbstractBaseEntity):
    address_state: str

    address_city: str

    address_neighborhood: str

    address_street: str

    address_number: str

    latitude: str

    longitude: str

    company: Company


class PointCreationService(IService[Optional[Point]]):
    def __init__(
        self,
        company_uuid: str,
        address_state: str,
        address_city: str,
        address_neighborhood: str,
        address_street: str,
        address_number: str,
        latitude: str,
        longitude: str,
    ) -> None:
        self.__company_uuid: str = company_uuid

        self.__address_state: str = address_state

        self.__address_city: str = address_city

        self.__address_neighborhood: str = address_neighborhood

        self.__address_street: str = address_street

        self.__address_number: str = address_number

        self.__latitude: str = latitude

        self.__longitude: str = longitude

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

    async def __create_point(
        self, session: AsyncSession, company: Company
    ) -> Optional[Point]:
        data: PointCreationProps = PointCreationProps(
            address_state=self.__address_state,
            address_city=self.__address_city,
            address_neighborhood=self.__address_neighborhood,
            address_street=self.__address_street,
            address_number=self.__address_number,
            latitude=self.__latitude,
            longitude=self.__longitude,
            company=company,
        )

        company_repository: ICreateRepository[
            PointCreationRepositoryProps, Optional[Point]
        ] = PointRepository(session)

        point: Optional[Point] = await company_repository.create(data)

        await session.commit()

        await session.refresh(point)

        return point

    async def execute(self) -> Optional[Point]:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            company: Company = await self.__find_company(session)

            return await self.__create_point(session, company)
