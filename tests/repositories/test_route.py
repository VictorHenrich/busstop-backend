from typing import Optional, Sequence
from unittest.mock import Mock

from models import Company, Point, Route, database
from repositories.route import (
    RouteRepository,
    IRouteCreateRepository,
    IRouteUpdateRepository,
    IRouteDeleteRepository,
    IRouteFindRepository,
    IRouteFindManyRepository,
)
from utils.patterns import (
    ICreateRepository,
    IFindManyRepository,
    IFindRepository,
    IUpdateRepository,
    IDeleteRepository,
)
from .common import BaseRepositoryTestCase
from .mocks import create_company, create_point, create_route


class RouteRepositoryTestCase(BaseRepositoryTestCase):
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()

        self.__company: Company = await create_company()

        self.__point: Point = await create_point(self.__company)

        self.__route: Route = await create_route(self.__company)

    async def test_create(self) -> None:
        async with database.create_async_session() as session:
            route_repository: ICreateRepository[
                IRouteCreateRepository, Optional[Route]
            ] = RouteRepository(session)

            route_repository_props: IRouteCreateRepository = Mock(
                company=self.__company,
                description=self.__route.description,
                opening_time=self.__route.opening_time,
                closing_time=self.__route.closing_time,
                ticket_price=self.__route.ticket_price,
                points=[self.__point],
            )

            route: Optional[Route] = await route_repository.create(
                route_repository_props
            )

            self.assertIsNotNone(route)

    async def test_update(self) -> None:
        async with database.create_async_session() as session:
            route_repository: IUpdateRepository[
                IRouteUpdateRepository, Optional[Route]
            ] = RouteRepository(session)

            route_repository_props: IRouteUpdateRepository = Mock(
                company=self.__company,
                description=self.__route.description,
                opening_time=self.__route.opening_time,
                closing_time=self.__route.closing_time,
                ticket_price=self.__route.ticket_price,
                points=[self.__point],
                instance=None,
                uuid=self.__route.uuid,
            )

            route: Optional[Route] = await route_repository.update(
                route_repository_props
            )

            self.assertIsNotNone(route)

    async def test_delete(self) -> None:
        async with database.create_async_session() as session:
            route_repository: IDeleteRepository[
                IRouteDeleteRepository, Optional[Route]
            ] = RouteRepository(session)

            route_repository_props: IRouteDeleteRepository = Mock(
                instance=None, uuid=self.__route.uuid
            )

            route: Optional[Route] = await route_repository.delete(
                route_repository_props
            )

            self.assertIsNotNone(route)

    async def test_find(self) -> None:
        async with database.create_async_session() as session:
            route_repository: IFindRepository[IRouteFindRepository, Optional[Route]] = (
                RouteRepository(session)
            )

            route_repository_props: IRouteFindRepository = Mock(uuid=self.__route.uuid)

            route: Optional[Route] = await route_repository.find(route_repository_props)

            self.assertIsNotNone(route)

    async def test_find_many(self) -> None:
        async with database.create_async_session() as session:
            route_repository: IFindManyRepository[
                IRouteFindManyRepository, Optional[Route]
            ] = RouteRepository(session)

            route_repository_props: IRouteFindManyRepository = Mock(
                company=self.__company
            )

            routes: Sequence[Route] = await route_repository.find_many(
                route_repository_props
            )

            self.assertTrue(len(routes) > 0)
