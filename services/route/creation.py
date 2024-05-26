from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from models import Route, Company, Point, database
from repositories.route import RouteRepository, RouteCreationRepositoryProps
from repositories.company import CompanyRepository, CompanyCaptureRepositoryProps
from repositories.point import PointRepository, PointListingRepositoryProps
from utils.patterns import (
    IService,
    ICreateRepository,
    IFindRepository,
    IFindManyRepository,
    AbstractBaseEntity,
)
from utils.exceptions import ModelNotFound


class RouteCreationProps(AbstractBaseEntity):
    company: Company

    description: str

    points: Sequence[Point]


class PointListingProps(AbstractBaseEntity):
    company: Company

    uuids: Sequence[str]


class CompanyCaptureProps(AbstractBaseEntity):
    uuid: str


class RouteCreationService(IService[Optional[Route]]):
    def __init__(
        self, company_uuid: str, description: str, point_uuids: Sequence[str]
    ) -> None:
        self.__company_uuid: str = company_uuid

        self.__description: str = description

        self.__point_uuids: Sequence[str] = point_uuids

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

    async def __find_points(
        self, session: AsyncSession, company: Company
    ) -> Sequence[Point]:
        point_repository: IFindManyRepository[
            PointListingRepositoryProps, Point
        ] = PointRepository(session)

        point_props: PointListingRepositoryProps = PointListingProps(
            company=company, uuids=self.__point_uuids
        )

        return await point_repository.find_many(point_props)

    async def __create_route(
        self, session: AsyncSession, company: Company, points: Sequence[Point]
    ) -> Optional[Route]:
        route_repository: ICreateRepository[
            RouteCreationRepositoryProps, Optional[Route]
        ] = RouteRepository(session)

        route_props: RouteCreationRepositoryProps = RouteCreationProps(
            company=company, points=points, description=self.__description
        )

        return await route_repository.create(route_props)

    async def execute(self) -> Optional[Route]:
        async with database.create_async_session() as session:
            company: Company = await self.__find_company(session)

            points: Sequence[Point] = await self.__find_points(session, company)

            route: Optional[Route] = await self.__create_route(session, company, points)

            await session.commit()
            await session.refresh(route)

            return route
