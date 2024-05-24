from typing import Optional, Sequence
from unittest import TestCase
from unittest.mock import Mock
import asyncio
import logging

from server.instances import ServerInstances
from server.database import Database
from models import Route, Point
from repositories.route import (
    RouteRepository,
    RouteCreationRepositoryProps,
    RouteUpdateRepositoryProps,
    RouteExclusionRepositoryProps,
    RouteCaptureRepositoryProps,
    RouteListingRepositoryProps,
)
from utils.patterns import (
    ICreateRepository,
    IFindManyRepository,
    IFindRepository,
    IUpdateRepository,
    IDeleteRepository,
)
from utils.constants import DATABASE_INSTANCE_NAME


class RouteRepositoryCase(TestCase):
    def setUp(self) -> None:
        self.__database: Database = ServerInstances.databases.select(
            DATABASE_INSTANCE_NAME
        )

        self.__route_data: Mock = Mock()

        self.__route_data.company = Mock()

        self.__route_data.company.id = 1
        self.__route_data.company.uuid = "29edd5cc-4e7d-4e86-b9bd-b69e64601532"
        self.__route_data.uuid = "0d0a6d5d-d762-4cc2-8131-1ff5214e3b47"
        self.__route_data.description = "Rota alterada"
        self.__route_data.points = [
            Point(
                address_state="SC",
                address_city="Capivari de Baixo Alterado",
                address_neighborhood="Centro",
                address_street="victorhenrich993@gmail.com ALTERADO",
                address_number="400 ALTERADO",
                latitude="-28.4759466",
                longitude="-49.0059852",
                company_id=1,
                uuid="8f45263e-66b7-499c-bcb6-05c21deb6e6a",
                id=3,
            )
        ]
        self.__route_data.route_instance = None

    def test_create(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                route_repository: ICreateRepository[
                    RouteCreationRepositoryProps, Optional[Route]
                ] = RouteRepository(session)

                route: Optional[Route] = await route_repository.create(
                    self.__route_data
                )

                await session.commit()

                await session.refresh(route)

                logging.info(f"Route Created: {route}")

        asyncio.run(main())

    def test_update(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                route_repository: IUpdateRepository[
                    RouteUpdateRepositoryProps, Optional[Route]
                ] = RouteRepository(session)

                route: Optional[Route] = await route_repository.update(
                    self.__route_data
                )

                await session.commit()

                await session.refresh(route)

                logging.info(f"Route Updated: {route}")

        asyncio.run(main())

    def test_delete(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                route_repository: IDeleteRepository[
                    RouteExclusionRepositoryProps, Optional[Route]
                ] = RouteRepository(session)

                route: Optional[Route] = await route_repository.delete(
                    self.__route_data
                )

                logging.info(f"Route Deleted: {route}")

                await session.commit()

        asyncio.run(main())

    def test_find(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                route_repository: IFindRepository[
                    RouteCaptureRepositoryProps, Route
                ] = RouteRepository(session)

                point: Optional[Route] = await route_repository.find(self.__route_data)

                logging.info(f"Route: {point}")

                self.assertIsNot(point, None)

        asyncio.run(main())

    def test_find_many(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                route_repository: IFindManyRepository[
                    RouteListingRepositoryProps, Route
                ] = RouteRepository(session)

                points: Sequence[Route] = await route_repository.find_many(
                    self.__route_data
                )

                logging.info(f"Routes: {points}")

                self.assertIsNot(points, None)

        asyncio.run(main())
