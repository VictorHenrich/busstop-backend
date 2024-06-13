from typing import Optional, Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock, patch

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


class PointRepositoryTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_point: Mock = Mock(
            address_state="SC",
            address_city="Capivari de Baixo Alterado",
            address_neighborhood="Centro",
            address_street="victorhenrich993@gmail.com",
            address_number="400",
            latitude="-28.4759466",
            longitude="-49.0059852",
            uuid="4932d9e1-c715-4b97-890a-ab2f678d3d11",
            instance=None,
        )

        self.__mock_company: Mock = Mock(
            id=1,
            uuid="4932d9e1-c715-4b97-890a-ab2f678d3123",
            company_name="TESTE",
            fantasy_name="TESTE",
            document_cnpj="000000000",
        )

        self.__mock_async_session: AsyncMock = AsyncMock()

        self.__mock_session: Mock = Mock()

        self.__mock_point.company = self.__mock_company

    @patch("repositories.point.Point", spec=Point)
    async def test_create(self, MockPointModel: Mock) -> None:
        MockPointModel.return_value = self.__mock_point

        self.__mock_session.add.return_value = None

        point_repository: ICreateRepository[
            PointCreationRepositoryProps, Optional[Point]
        ] = PointRepository(self.__mock_session)

        point: Optional[Point] = await point_repository.create(self.__mock_point)

        self.assertIsNotNone(point)
        self.assertEqual(point, self.__mock_point)

    async def test_update(self) -> None:
        self.__mock_async_session.scalar.return_value = self.__mock_point

        point_repository: IUpdateRepository[
            PointUpdateRepositoryProps, Optional[Point]
        ] = PointRepository(self.__mock_async_session)

        point: Optional[Point] = await point_repository.update(self.__mock_point)

        self.assertIsNotNone(point)
        self.assertEqual(point, self.__mock_point)

    async def test_delete(self) -> None:
        self.__mock_async_session.execute.return_value = None
        self.__mock_async_session.scalar.return_value = self.__mock_point

        filter_props: Mock = Mock(uuid="")

        point_repository: IDeleteRepository[
            PointExclusionRepositoryProps, Optional[Point]
        ] = PointRepository(self.__mock_async_session)

        point: Optional[Point] = await point_repository.delete(filter_props)

        self.assertIsNotNone(point)
        self.assertEqual(point, self.__mock_point)

    async def test_get(self) -> None:
        self.__mock_async_session.scalar.return_value = self.__mock_point

        filter_props: Mock = Mock(uuid="")

        point_repository: IFindRepository[
            PointCaptureRepositoryProps, Point
        ] = PointRepository(self.__mock_async_session)

        point: Optional[Point] = await point_repository.find(filter_props)

        self.assertIsNotNone(point)
        self.assertEqual(point, self.__mock_point)

    async def test_list(self) -> None:
        mock_points: Sequence[Point] = [self.__mock_point]

        mock_scalars_result: Mock = Mock()

        mock_scalars_result.all.return_value = mock_points

        self.__mock_async_session.scalars.return_value = mock_scalars_result

        filter_props: Mock = Mock(company=self.__mock_company, uuids=[])

        point_repository: IFindManyRepository[
            PointListingRepositoryProps, Point
        ] = PointRepository(self.__mock_async_session)

        point: Sequence[Point] = await point_repository.find_many(filter_props)

        self.assertNotEqual(point, [])

        self.assertSequenceEqual(point, mock_points)
