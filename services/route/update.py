from typing import Optional, Sequence
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


from server.database import Database
from server.instances import ServerInstances
from models import Route, Company, Point
from repositories.route import (
    RouteRepository,
    RouteUpdateRepositoryProps,
    RouteCaptureRepositoryProps,
)
from repositories.point import PointRepository, PointListingRepositoryProps
from utils.patterns import (
    IService,
    IUpdateRepository,
    IFindRepository,
    IFindManyRepository,
)
from utils.exceptions import ModelNotFound
from utils.constants import DATABASE_INSTANCE_NAME


class RouteUpdateProps(BaseModel):
    uuid: str

    description: str

    points: Sequence[Point]

    route_instance: Optional[Route] = None


class PointListingProps(BaseModel):
    company: Company
    uuids: Sequence[str] = []


class RouteCaptureProps(BaseModel):
    uuid: str


class RouteUpdateService(IService[Optional[Route]]):
    def __init__(
        self,
        route_uuid: str,
        description: str,
        point_uuids: Sequence[str],
    ) -> None:
        self.__route_uuid: str = route_uuid

        self.__description: str = description

        self.__point_uuids: Sequence[str] = point_uuids

    async def __find_route(self, session: AsyncSession) -> Route:
        route_repository: IFindRepository[
            RouteCaptureRepositoryProps, Route
        ] = RouteRepository(session)

        route_props: RouteCaptureRepositoryProps = RouteCaptureProps(
            uuid=self.__route_uuid
        )

        route: Optional[Route] = await route_repository.find(route_props)

        if not route:
            raise ModelNotFound(Route, self.__route_uuid)

        return route

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

    async def __update_route(
        self, session: AsyncSession, points: Sequence[Point]
    ) -> Optional[Route]:
        route_repository: IUpdateRepository[
            RouteUpdateRepositoryProps, Optional[Route]
        ] = RouteRepository(session)

        route_props: RouteUpdateRepositoryProps = RouteUpdateProps(
            uuid=self.__route_uuid, points=points, description=self.__description
        )

        return await route_repository.update(route_props)

    async def execute(self) -> Optional[Route]:
        database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

        async with database.create_async_session() as session:
            route: Route = await self.__find_route(session)

            points: Sequence[Point] = await self.__find_points(session, route.company)

            return await self.__update_route(session, points)
