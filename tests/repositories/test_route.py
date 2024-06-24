from typing import Optional, Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from datetime import time

from models import Route
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


class RouteRepositoryTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_points: MagicMock = MagicMock()

        self.__mock_route: Mock = Mock(
            uuid="0d0a6d5d-d762-4cc2-8131-1ff5214e3b47",
            description="Rota alterada",
            ticket_price=0,
            opening_time=time(),
            closing_time=time(),
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

        self.__mock_points.add.return_value = None

        self.__mock_points.__iter__.return_value = [
            Mock(
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

        self.__mock_route.points = self.__mock_points

        self.__mock_route.company = self.__mock_company

    @patch("repositories.route.Route", spec=Route)
    async def test_create(self, MockRoute: Mock) -> None:
        MockRoute.return_value = self.__mock_route

        route_repository: ICreateRepository[
            RouteCreationRepositoryProps, Optional[Route]
        ] = RouteRepository(self.__mock_session)

        route: Optional[Route] = await route_repository.create(self.__mock_route)

        self.assertEqual(route, self.__mock_route)

    async def test_update(self) -> None:
        self.__mock_async_session.scalar.return_value = self.__mock_route

        self.__mock_async_session.execute.return_value = None

        route_repository: IUpdateRepository[
            RouteUpdateRepositoryProps, Optional[Route]
        ] = RouteRepository(self.__mock_async_session)

        route: Optional[Route] = await route_repository.update(self.__mock_route)

        self.__mock_async_session.scalar.assert_awaited_once()

        self.__mock_async_session.execute.assert_awaited_once()

        self.assertEqual(route, self.__mock_route)

    async def test_delete(self) -> None:
        self.__mock_async_session.scalar.return_value = self.__mock_route

        self.__mock_async_session.execute.return_value = None

        filter_props: Mock = Mock(uuid="", company=self.__mock_company, instance=None)

        route_repository: IDeleteRepository[
            RouteExclusionRepositoryProps, Optional[Route]
        ] = RouteRepository(self.__mock_async_session)

        route: Optional[Route] = await route_repository.delete(filter_props)

        self.__mock_async_session.scalar.assert_awaited_once()

        self.__mock_async_session.execute.assert_awaited_once()

        self.assertEqual(route, self.__mock_route)

    async def test_find(self) -> None:
        self.__mock_async_session.scalar.return_value = self.__mock_route

        filter_props: Mock = Mock(uuid="")

        route_repository: IFindRepository[
            RouteCaptureRepositoryProps, Route
        ] = RouteRepository(self.__mock_async_session)

        point: Optional[Route] = await route_repository.find(filter_props)

        self.__mock_async_session.scalar.assert_awaited_once()

        self.assertEqual(point, self.__mock_route)

    async def test_find_many(self) -> None:
        mock_routes: Sequence[Route] = [self.__mock_route]

        mock_scalars_result: Mock = Mock()

        mock_scalars_result.all.return_value = mock_routes

        self.__mock_async_session.scalars.return_value = mock_scalars_result

        filter_props: Mock = Mock(company=self.__mock_company)

        route_repository: IFindManyRepository[
            RouteListingRepositoryProps, Route
        ] = RouteRepository(self.__mock_async_session)

        points: Sequence[Route] = await route_repository.find_many(filter_props)

        self.__mock_async_session.scalars.assert_awaited_once()

        mock_scalars_result.all.assert_called_once()

        self.assertSequenceEqual(points, mock_routes)
