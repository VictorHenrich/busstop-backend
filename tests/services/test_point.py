from typing import Optional, Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch

from models import Point, Company
from services.point import (
    PointService,
    PointCreationProps,
    PointUpdateProps,
    PointExclusionProps,
    PointCaptureProps,
    PointListingProps,
)
from services.company import CompanyService
from repositories.point import PointRepository


class PointServiceTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_async_session: AsyncMock = AsyncMock()

        self.__mock_async_session.__aenter__.side_effect = (
            lambda: self.__mock_async_session
        )

        self.__mock_async_session.commit.return_value = None

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
            spec=Point,
        )

        self.__mock_company: Mock = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia TESTE",
            document_cnpj="00000000",
            email="teste@gmail.com",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df68a",
            spec=Company,
        )

    def __configure_mock_company_service(
        self, mock_company_service_class: Mock
    ) -> AsyncMock:
        mock_company_service_instance: AsyncMock = AsyncMock()

        mock_company_service_instance.find_company.return_value = self.__mock_company

        mock_company_service_class.return_value = mock_company_service_instance

        return mock_company_service_instance

    def __configure_mock_database(self, mock_database: Mock) -> None:
        mock_database.create_async_session.return_value = self.__mock_async_session

    def __assert_called_in_database(self, mock_database: Mock) -> None:
        mock_database.create_async_session.assert_called_once()

    def __assert_called_in_company_service(
        self, mock_company_service_instance: AsyncMock
    ) -> None:
        mock_company_service_instance.find_company.assert_awaited_once()

    @patch("services.point.database")
    @patch("services.point.PointRepository", spec=PointRepository)
    @patch("services.point.CompanyService", spec=CompanyService)
    @patch("services.point.PointCreationProps", spec=PointCreationProps)
    async def test_create(
        self,
        mock_point_creation_props_class: Mock,
        mock_company_service_class: Mock,
        mock_point_repository_class: Mock,
        mock_database: Mock,
    ) -> None:
        mock_point_repository_instance: AsyncMock = AsyncMock()

        mock_point_repository_instance.create.return_value = self.__mock_point

        mock_point_creation_props_class.return_value = Mock()

        mock_point_repository_class.return_value = mock_point_repository_instance

        self.__configure_mock_database(mock_database)

        mock_company_service_instance: AsyncMock = (
            self.__configure_mock_company_service(mock_company_service_class)
        )

        point_service: PointService = PointService()

        point: Optional[Point] = await point_service.create_point(
            address_state=self.__mock_point.address_state,
            address_city=self.__mock_point.address_city,
            address_neighborhood=self.__mock_point.address_neighborhood,
            address_street=self.__mock_point.address_street,
            address_number=self.__mock_point.address_number,
            address_zip_code=self.__mock_point.address_zip_code,
            latitude=self.__mock_point.latitude,
            longitude=self.__mock_point.longitude,
            company_uuid=self.__mock_company.uuid,
        )

        self.__mock_async_session.commit.assert_awaited_once()

        self.__assert_called_in_database(mock_database)

        self.__assert_called_in_company_service(mock_company_service_instance)

        mock_point_repository_instance.create.assert_awaited_once()

        mock_point_repository_class.assert_called_once()

        self.assertEqual(point, self.__mock_point)

    @patch("services.point.database")
    @patch("services.point.PointRepository", spec=PointRepository)
    @patch("services.point.PointUpdateProps", spec=PointUpdateProps)
    async def test_update(
        self,
        mock_point_update_props_class: Mock,
        mock_point_repository_class: Mock,
        mock_database: Mock,
    ) -> None:
        mock_point_repository_instance: AsyncMock = AsyncMock()

        mock_point_repository_instance.update.return_value = self.__mock_point

        mock_point_update_props_class.return_value = Mock()

        mock_point_repository_class.return_value = mock_point_repository_instance

        self.__configure_mock_database(mock_database)

        point_service: PointService = PointService()

        point: Optional[Point] = await point_service.update_point(
            address_state=self.__mock_point.address_state,
            address_city=self.__mock_point.address_city,
            address_neighborhood=self.__mock_point.address_neighborhood,
            address_street=self.__mock_point.address_street,
            address_number=self.__mock_point.address_number,
            address_zip_code=self.__mock_point.address_zip_code,
            latitude=self.__mock_point.latitude,
            longitude=self.__mock_point.longitude,
            point_uuid=self.__mock_point.uuid,
        )

        self.__mock_async_session.commit.assert_awaited_once()

        self.__assert_called_in_database(mock_database)

        mock_point_repository_instance.update.assert_awaited_once()

        mock_point_repository_class.assert_called_once()

        self.assertEqual(point, self.__mock_point)

    @patch("services.point.database")
    @patch("services.point.PointRepository", spec=PointRepository)
    @patch("services.point.PointExclusionProps", spec=PointExclusionProps)
    @patch("services.point.copy")
    async def test_delete(
        self,
        mock_copy: Mock,
        mock_point_exclusion_props_class: Mock,
        mock_point_repository_class: Mock,
        mock_database: Mock,
    ) -> None:
        mock_point_repository_instance: AsyncMock = AsyncMock()

        mock_point_repository_instance.delete.return_value = self.__mock_point

        mock_point_exclusion_props_class.return_value = Mock()

        mock_point_repository_class.return_value = mock_point_repository_instance

        mock_copy.return_value = self.__mock_point

        self.__configure_mock_database(mock_database)

        point_service: PointService = PointService()

        point: Optional[Point] = await point_service.delete_point(
            point_uuid=self.__mock_point.uuid,
        )

        self.__mock_async_session.commit.assert_awaited_once()

        self.__assert_called_in_database(mock_database)

        mock_point_repository_instance.delete.assert_awaited_once()

        mock_point_repository_class.assert_called_once()

        self.assertEqual(point, self.__mock_point)

    @patch("services.point.database")
    @patch("services.point.PointRepository", spec=PointRepository)
    @patch("services.point.PointCaptureProps", spec=PointCaptureProps)
    async def test_find(
        self,
        mock_point_capture_props_class: Mock,
        mock_point_repository_class: Mock,
        mock_database: Mock,
    ) -> None:
        mock_point_repository_instance: AsyncMock = AsyncMock()

        mock_point_repository_instance.find.return_value = self.__mock_point

        mock_point_capture_props_class.return_value = Mock()

        mock_point_repository_class.return_value = mock_point_repository_instance

        self.__configure_mock_database(mock_database)

        point_service: PointService = PointService()

        point: Optional[Point] = await point_service.find_point(
            point_uuid=self.__mock_point.uuid,
        )

        self.__assert_called_in_database(mock_database)

        mock_point_repository_instance.find.assert_awaited_once()

        mock_point_repository_class.assert_called_once()

        self.assertEqual(point, self.__mock_point)

    @patch("services.point.database")
    @patch("services.point.CompanyService", spec=CompanyService)
    @patch("services.point.PointRepository", spec=PointRepository)
    @patch("services.point.PointListingProps", spec=PointListingProps)
    async def test_find_many(
        self,
        mock_point_listing_props_class: Mock,
        mock_point_repository_class: Mock,
        mock_company_service_class: Mock,
        mock_database: Mock,
    ) -> None:
        mock_points: Sequence[Point] = [self.__mock_point]

        mock_point_repository_instance: AsyncMock = AsyncMock()

        mock_point_repository_instance.find_many.return_value = mock_points

        mock_point_listing_props_class.return_value = Mock()

        mock_point_repository_class.return_value = mock_point_repository_instance

        self.__configure_mock_database(mock_database)

        mock_company_service_instance: Mock = self.__configure_mock_company_service(
            mock_company_service_class
        )

        point_service: PointService = PointService()

        point: Sequence[Point] = await point_service.find_points(
            point_uuids=[self.__mock_point.uuid], company_uuid=self.__mock_company.uuid
        )

        self.__assert_called_in_database(mock_database)

        self.__assert_called_in_company_service(mock_company_service_instance)

        mock_point_repository_instance.find_many.assert_awaited_once()

        mock_point_repository_class.assert_called_once()

        self.assertSequenceEqual(point, mock_points)

    async def test_find_points_closer(self) -> None:
        point_service: PointService = PointService()

        points: Sequence[Point] = await point_service.find_points_closer(Mock(), 0, [])
