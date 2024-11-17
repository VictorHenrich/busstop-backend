from typing import Optional, Sequence
from unittest.mock import Mock

from models import Point, Company, database
from repositories.point import (
    PointRepository,
    IPointCreateRepository,
    IPointUpdateRepository,
    IPointDeleteRepository,
    IPointFindRepository,
    IPointFindManyRepository,
)
from utils.patterns import (
    ICreateRepository,
    IFindManyRepository,
    IFindRepository,
    IUpdateRepository,
    IDeleteRepository,
)
from .mocks import create_company, create_point
from .common import BaseRepositoryTestCase


class PointRepositoryTestCase(BaseRepositoryTestCase):
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()

        self.__company: Company = await create_company()

        self.__point: Point = await create_point(self.__company)

    async def test_create(self) -> None:
        async with database.create_async_session() as session:
            point_repository: ICreateRepository[
                IPointCreateRepository, Optional[Point]
            ] = PointRepository(session)

            repository_props: IPointCreateRepository = Mock(
                company=self.__company,
                address_zip_code="00000",
                address_state="SC",
                address_city="Cidade teste",
                address_neighborhood="Bairro teste",
                address_street="Rua teste",
                address_number="00",
                latitude="0",
                longitude="0",
                place_id="1234",
            )

            point: Optional[Point] = await point_repository.create(repository_props)

            self.assertIsNotNone(point)

    async def test_update(self) -> None:
        async with database.create_async_session() as session:
            point_repository: IUpdateRepository[
                IPointUpdateRepository, Optional[Point]
            ] = PointRepository(session)

            repository_props: IPointUpdateRepository = Mock(
                company=self.__company,
                uuid=self.__point.uuid,
                address_zip_code="00000",
                address_state="SC",
                address_city="Cidade teste",
                address_neighborhood="Bairro teste",
                address_street="Rua teste",
                address_number="00",
                latitude="0",
                longitude="0",
                place_id="1234",
                instance=None,
            )

            point: Optional[Point] = await point_repository.update(repository_props)

            self.assertIsNotNone(point)

    async def test_delete(self) -> None:
        async with database.create_async_session() as session:
            point_repository: IDeleteRepository[
                IPointDeleteRepository, Optional[Point]
            ] = PointRepository(session)

            repository_props: IPointDeleteRepository = Mock(uuid=self.__point.uuid)

            point: Optional[Point] = await point_repository.delete(repository_props)

            self.assertIsNotNone(point)

    async def test_find(self) -> None:
        async with database.create_async_session() as session:
            point_repository: IFindRepository[IPointFindRepository, Optional[Point]] = (
                PointRepository(session)
            )

            repository_props: IPointFindRepository = Mock(uuid=self.__point.uuid)

            point: Optional[Point] = await point_repository.find(repository_props)

            self.assertIsNotNone(point)

    async def test_find_many(self) -> None:
        async with database.create_async_session() as session:
            point_repository: IFindManyRepository[
                IPointFindManyRepository, Optional[Point]
            ] = PointRepository(session)

            repository_props: IPointFindManyRepository = Mock(
                company=self.__company, uuids=[]
            )

            points: Sequence[Point] = await point_repository.find_many(repository_props)

            self.assertIsNotNone(points)

            self.assertTrue(len(points) > 0)
