from typing import Optional
from copy import copy
from sqlalchemy.ext.asyncio import AsyncSession

from models import Route, database
from repositories.route import RouteRepository, RouteExclusionRepositoryProps
from utils.patterns import IService, IDeleteRepository, AbstractBaseEntity


class RouteExclusionProps(AbstractBaseEntity):
    uuid: str

    route_instance: Optional[Route] = None


class RouteExclusionService(IService[Optional[Route]]):
    def __init__(self, route_uuid: str) -> None:
        self.__route_uuid: str = route_uuid

    async def __delete_route(self, session: AsyncSession) -> Optional[Route]:
        route_repository: IDeleteRepository[
            RouteExclusionRepositoryProps, Optional[Route]
        ] = RouteRepository(session)

        route_props: RouteExclusionRepositoryProps = RouteExclusionProps(
            uuid=self.__route_uuid
        )

        return await route_repository.delete(route_props)

    async def execute(self) -> Optional[Route]:
        async with database.create_async_session() as session:
            route: Optional[Route] = await self.__delete_route(session)

            route_copy: Optional[Route] = None

            if route:
                route_copy = copy(route)

            await session.commit()

            return route_copy
