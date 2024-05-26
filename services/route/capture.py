from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from models import Route, database
from repositories.route import RouteRepository, RouteCaptureRepositoryProps
from utils.patterns import IService, IFindRepository, AbstractBaseEntity


class RouteCaptureProps(AbstractBaseEntity):
    uuid: str


class RouteCaptureService(IService[Optional[Route]]):
    def __init__(self, route_uuid: str) -> None:
        self.__route_uuid: str = route_uuid

    async def __find_route(self, session: AsyncSession) -> Optional[Route]:
        route_repository: IFindRepository[
            RouteCaptureRepositoryProps, Optional[Route]
        ] = RouteRepository(session)

        route_props: RouteCaptureRepositoryProps = RouteCaptureProps(
            uuid=self.__route_uuid
        )

        return await route_repository.find(route_props)

    async def execute(self) -> Optional[Route]:
        async with database.create_async_session() as session:
            return await self.__find_route(session)
