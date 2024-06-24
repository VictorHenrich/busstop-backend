from typing import Optional, Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch

from services.route import RouteService
from services.point import PointService
from services.company import CompanyService
from repositories.route import RouteRepository
from models import Company, Route


class RouteServiceTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_company_service_instance: AsyncMock = AsyncMock()

        self.__mock_point_service_instance: AsyncMock = AsyncMock()

        self.__mock_route_repository_instance: AsyncMock = AsyncMock()

        self.__mock_async_session: AsyncMock = AsyncMock()

        self.__mock_route: Mock = Mock(
            description="",
            uuid="4932d9e1-c715-4b97-890a-ab2f678d3d11",
            instance=None,
            ticket_price=0,
            spec=Route,
        )

        self.__mock_company: Mock = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia TESTE",
            document_cnpj="00000000",
            email="teste@gmail.com",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df68a",
            spec=Company,
        )

        self.__mock_async_session.__aenter__.side_effect = (
            lambda: self.__mock_async_session
        )

        self.__mock_async_session.commit.return_value = None

        self.__mock_point_service_instance.find_points.return_value = []

        self.__mock_company_service_instance.find_company.return_value = (
            self.__mock_company
        )

        self.__mock_route_repository_instance.create.return_value = self.__mock_route
        self.__mock_route_repository_instance.update.return_value = self.__mock_route
        self.__mock_route_repository_instance.delete.return_value = self.__mock_route
        self.__mock_route_repository_instance.find.return_value = self.__mock_route
        self.__mock_route_repository_instance.find_many.return_value = [
            self.__mock_route
        ]

    @patch("services.route.PointService", spec=PointService)
    @patch("services.route.CompanyService", spec=CompanyService)
    @patch("services.route.database")
    @patch("services.route.RouteRepository", spec=RouteRepository)
    async def test_create(
        self,
        mock_route_repository_class: Mock,
        mock_database_instance: Mock,
        mock_company_service_class: Mock,
        mock_point_service_class: Mock,
    ) -> None:
        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_route_repository_class.return_value = self.__mock_route_repository_instance

        mock_company_service_class.return_value = self.__mock_company_service_instance

        mock_point_service_class.return_value = self.__mock_point_service_instance

        route_service: RouteService = RouteService()

        route: Optional[Route] = await route_service.create_route(
            description=self.__mock_route.description,
            point_uuids=[],
            company_uuid=self.__mock_company.uuid,
            ticket_price=self.__mock_route.ticket_price,
            closing_time=self.__mock_route.closing_time,
            opening_time=self.__mock_route.opening_time,
        )

        self.__mock_route_repository_instance.create.assert_awaited_once()

        self.__mock_company_service_instance.find_company.assert_awaited_once()

        self.__mock_point_service_instance.find_points.assert_awaited_once()

        mock_database_instance.create_async_session.assert_called_once()

        self.__mock_async_session.commit.assert_awaited_once()

        self.assertEqual(route, self.__mock_route)

    @patch("services.route.PointService", spec=PointService)
    @patch("services.route.database")
    @patch("services.route.RouteRepository", spec=RouteRepository)
    async def test_update(
        self,
        mock_route_repository_class: Mock,
        mock_database_instance: Mock,
        mock_point_service_class: Mock,
    ) -> None:
        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_route_repository_class.return_value = self.__mock_route_repository_instance

        mock_point_service_class.return_value = self.__mock_point_service_instance

        route_service: RouteService = RouteService()

        route: Optional[Route] = await route_service.update_route(
            description=self.__mock_route.description,
            point_uuids=[],
            route_uuid=self.__mock_route.uuid,
            ticket_price=self.__mock_route.ticket_price,
            closing_time=self.__mock_route.closing_time,
            opening_time=self.__mock_route.opening_time,
        )

        self.__mock_route_repository_instance.update.assert_awaited_once()

        self.__mock_route_repository_instance.find.assert_awaited_once()

        self.__mock_point_service_instance.find_points.assert_awaited_once()

        mock_database_instance.create_async_session.assert_called_once()

        self.__mock_async_session.commit.assert_awaited_once()

        self.assertEqual(route, self.__mock_route)

    @patch("services.route.copy")
    @patch("services.route.database")
    @patch("services.route.RouteRepository", spec=RouteRepository)
    async def test_delete(
        self,
        mock_route_repository_class: Mock,
        mock_database_instance: Mock,
        mock_copy_function: Mock,
    ) -> None:
        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_route_repository_class.return_value = self.__mock_route_repository_instance

        mock_copy_function.return_value = self.__mock_route

        route_service: RouteService = RouteService()

        route: Optional[Route] = await route_service.delete_route(
            route_uuid=self.__mock_route.uuid,
        )

        self.__mock_route_repository_instance.delete.assert_awaited_once()

        mock_database_instance.create_async_session.assert_called_once()

        mock_copy_function.assert_called_once()

        self.__mock_async_session.commit.assert_awaited_once()

        self.assertEqual(route, self.__mock_route)

    @patch("services.route.database")
    @patch("services.route.RouteRepository", spec=RouteRepository)
    async def test_find(
        self,
        mock_route_repository_class: Mock,
        mock_database_instance: Mock,
    ) -> None:
        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_route_repository_class.return_value = self.__mock_route_repository_instance

        route_service: RouteService = RouteService()

        route: Optional[Route] = await route_service.find_route(
            route_uuid=self.__mock_route.uuid,
        )

        self.__mock_route_repository_instance.find.assert_awaited_once()

        mock_database_instance.create_async_session.assert_called_once()

        self.assertEqual(route, self.__mock_route)

    @patch("services.route.CompanyService", spec=CompanyService)
    @patch("services.route.database")
    @patch("services.route.RouteRepository", spec=RouteRepository)
    async def test_find_many(
        self,
        mock_route_repository_class: Mock,
        mock_database_instance: Mock,
        mock_company_service_class: Mock,
    ) -> None:
        mock_database_instance.create_async_session.return_value = (
            self.__mock_async_session
        )

        mock_route_repository_class.return_value = self.__mock_route_repository_instance

        mock_company_service_class.return_value = self.__mock_company_service_instance

        route_service: RouteService = RouteService()

        routes: Sequence[Route] = await route_service.find_routes(
            company_uuid=self.__mock_company.uuid
        )

        self.__mock_company_service_instance.find_company.assert_awaited_once()

        self.__mock_route_repository_instance.find_many.assert_awaited_once()

        mock_database_instance.create_async_session.assert_called_once()

        self.assertSequenceEqual(routes, [self.__mock_route])
