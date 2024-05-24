from typing import Optional, Sequence
from unittest import TestCase
from unittest.mock import Mock
import asyncio
import logging

from server.instances import ServerInstances
from server.database import Database
from models import Point
from repositories.point import (
    PointRepository,
    PointCreationRepositoryProps,
    PointUpdateRepositoryProps,
    PointExclusionRepositoryProps,
    PointCaptureRepositoryProps,
    PointListingRepositoryProps,
)
from utils.patterns import (
    ICreateRepository,
    IFindManyRepository,
    IFindRepository,
    IUpdateRepository,
    IDeleteRepository,
)
from utils.constants import DATABASE_INSTANCE_NAME


class PointRepositoryCase(TestCase):
    def setUp(self) -> None:
        self.__database: Database = ServerInstances.databases.select(
            DATABASE_INSTANCE_NAME
        )

        self.__point_data: Mock = Mock()

        self.__point_data.company = Mock(
            id=1, uuid="48a78ba8-d113-4801-8c50-0d0ab1f3197e"
        )

        self.__point_data.address_state = "SC"
        self.__point_data.address_city = "Capivari de Baixo Alterado"
        self.__point_data.address_neighborhood = "Centro"
        self.__point_data.address_street = "victorhenrich993@gmail.com ALTERADO"
        self.__point_data.address_number = "400 ALTERADO"
        self.__point_data.latitude = "-28.4759466"
        self.__point_data.longitude = "-49.0059852"
        self.__point_data.uuid = "4932d9e1-c715-4b97-890a-ab2f678d3d11"
        self.__point_data.point_instance = None

    def test_create(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                point_repository: ICreateRepository[
                    PointCreationRepositoryProps, Optional[Point]
                ] = PointRepository(session)

                point: Optional[Point] = await point_repository.create(
                    self.__point_data
                )

                await session.commit()

                await session.refresh(point)

                logging.info(f"Point Created: {point}")

        asyncio.run(main())

    def test_update(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                point_repository: IUpdateRepository[
                    PointUpdateRepositoryProps, Optional[Point]
                ] = PointRepository(session)

                point: Optional[Point] = await point_repository.update(
                    self.__point_data
                )

                await session.commit()

                await session.refresh(point)

                logging.info(f"Point Updated: {point}")

        asyncio.run(main())

    def test_delete(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                point_repository: IDeleteRepository[
                    PointExclusionRepositoryProps, Optional[Point]
                ] = PointRepository(session)

                point: Optional[Point] = await point_repository.delete(
                    self.__point_data
                )

                logging.info(f"Point Deleted: {point}")

                await session.commit()

        asyncio.run(main())

    def test_find(self) -> None:
        async def main() -> None:
            async with self.__database.create_async_session() as session:
                point_repository: IFindRepository[
                    PointCaptureRepositoryProps, Point
                ] = PointRepository(session)

                point: Optional[Point] = await point_repository.find(self.__point_data)

                logging.info(f"Point: {point}")

                self.assertIsNot(point, None)

        asyncio.run(main())

    def test_find_many(self) -> None:
        async def main() -> None:
            filters: Mock = Mock()

            filters.company_uuid = "48a78ba8-d113-4801-8c50-0d0ab1f3197e"

            async with self.__database.create_async_session() as session:
                point_repository: IFindManyRepository[
                    PointListingRepositoryProps, Point
                ] = PointRepository(session)

                points: Sequence[Point] = await point_repository.find_many(filters)

                logging.info(f"Points: {points}")

                self.assertIsNot(points, None)

        asyncio.run(main())
