from typing import Sequence, Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, Mock, AsyncMock

from models import Company
from server.database import ServerDatabase
from repositories.company import CompanyRepository
from services.company import (
    CompanyService,
    CompanyCaptureProps,
    CompanyUpdateProps,
    CompanyExclusionProps,
)


class CompanyServiceTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_company_repository_instance: AsyncMock = AsyncMock()

        self.__mock_async_session: AsyncMock = AsyncMock()

        self.__company_service: CompanyService = CompanyService()

        self.__mock_company: Mock = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia TESTE",
            document_cnpj="00000000",
            email="teste@gmail.com",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df68a",
        )

        self.__mock_async_session.__aenter__.side_effect = (
            lambda: self.__mock_async_session
        )

        self.__mock_async_session.commit.return_value = None

        self.__mock_async_session.refresh.return_value = None

        self.__mock_company_repository_instance.create.return_value = (
            self.__mock_company
        )
        self.__mock_company_repository_instance.update.return_value = (
            self.__mock_company
        )
        self.__mock_company_repository_instance.delete.return_value = (
            self.__mock_company
        )
        self.__mock_company_repository_instance.find.return_value = self.__mock_company
        self.__mock_company_repository_instance.find_many.return_value = [
            self.__mock_company
        ]

    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=ServerDatabase)
    async def test_create(
        self, mock_database: Mock, mock_company_repository_class: Mock
    ) -> None:
        mock_database.create_async_session.return_value = self.__mock_async_session

        mock_company_repository_class.return_value = (
            self.__mock_company_repository_instance
        )

        company: Optional[Company] = await self.__company_service.create_company(
            company_name=self.__mock_company.company_name,
            fantasy_name=self.__mock_company.fantasy_name,
            document_cnpj=self.__mock_company.document_cnpj,
            email=self.__mock_company.email,
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        self.__mock_company_repository_instance.create.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertEqual(company, self.__mock_company)

    @patch("services.company.CompanyCaptureProps", spec=CompanyCaptureProps)
    @patch("services.company.CompanyUpdateProps", spec=CompanyUpdateProps)
    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=ServerDatabase)
    async def test_update(
        self,
        mock_database: Mock,
        mock_company_repository_class: Mock,
        mock_company_capture_props_class: Mock,
        mock_company_update_props_class: Mock,
    ) -> None:
        mock_database.create_async_session.return_value = self.__mock_async_session

        mock_company_capture_props_class.return_value = Mock()

        mock_company_update_props_class.return_value = Mock()

        mock_company_repository_class.return_value = (
            self.__mock_company_repository_instance
        )

        company: Optional[Company] = await self.__company_service.update_company(
            company_uuid=self.__mock_company.uuid,
            company_name=self.__mock_company.company_name,
            fantasy_name=self.__mock_company.fantasy_name,
            document_cnpj=self.__mock_company.document_cnpj,
            email=self.__mock_company.email,
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        self.__mock_async_session.commit.assert_awaited_once()

        self.__mock_async_session.refresh.assert_awaited_once_with(company)

        self.__mock_company_repository_instance.update.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertEqual(company, self.__mock_company)

    # @patch("services.company.CompanyRepository", spec=CompanyRepository)
    # @patch("services.company.database", spec=ServerDatabase)
    # async def test_update_error(
    #     self, mock_database: Mock, mock_company_repository_class: Mock
    # ) -> None:
    #     self.__mock_company_repository_instance.update.return_value = None

    #     mock_database.create_async_session.return_value = self.__mock_async_session

    #     mock_company_repository_class.return_value = self.__mock_company_repository_instance

    #     company: Optional[Company] = await self.__company_service.update_company(
    #         company_uuid=self.__mock_company.uuid,
    #         company_name=self.__mock_company.company_name,
    #         fantasy_name=self.__mock_company.fantasy_name,
    #         document_cnpj=self.__mock_company.document_cnpj,
    #         email=self.__mock_company.email,
    #     )

    #     self.__mock_async_session.__aenter__.assert_called_once()

    #     self.__mock_async_session.commit.assert_awaited_once()

    #     self.__mock_company_repository_instance.update.assert_awaited_once()

    #     mock_database.create_async_session.assert_called_once()

    #     self.assertEqual(company, self.__mock_company)

    @patch("services.company.CompanyExclusionProps", spec=CompanyExclusionProps)
    @patch("services.company.CompanyCaptureProps", spec=CompanyCaptureProps)
    @patch("services.company.copy")
    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=ServerDatabase)
    async def test_delete(
        self,
        mock_database: Mock,
        mock_company_repository_class: Mock,
        mock_copy: Mock,
        mock_company_capture_props_class: Mock,
        mock_company_exclusion_props_class: Mock,
    ) -> None:
        mock_database.create_async_session.return_value = self.__mock_async_session

        mock_company_repository_class.return_value = (
            self.__mock_company_repository_instance
        )

        mock_copy.return_value = self.__mock_company

        mock_company_capture_props_class.return_value = Mock()

        mock_company_exclusion_props_class.return_value = Mock()

        company: Optional[Company] = await self.__company_service.delete_company(
            company_uuid=self.__mock_company.uuid,
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        self.__mock_async_session.commit.assert_awaited_once()

        self.__mock_company_repository_instance.delete.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        mock_copy.assert_called_once_with(company)

        self.assertEqual(company, self.__mock_company)

    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=ServerDatabase)
    async def test_find(
        self,
        mock_database: Mock,
        mock_company_repository_class: Mock,
    ) -> None:
        mock_database.create_async_session.return_value = self.__mock_async_session

        mock_company_repository_class.return_value = (
            self.__mock_company_repository_instance
        )

        company: Company = await self.__company_service.find_company(
            company_uuid=self.__mock_company.uuid,
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        self.__mock_company_repository_instance.find.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertEqual(company, self.__mock_company)

    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=ServerDatabase)
    async def test_find_many(
        self,
        mock_database: Mock,
        mock_company_repository_class: Mock,
    ) -> None:
        mock_companies: Sequence[Company] = [self.__mock_company]

        mock_database.create_async_session.return_value = self.__mock_async_session

        mock_company_repository_class.return_value = (
            self.__mock_company_repository_instance
        )

        companies: Sequence[Company] = await self.__company_service.find_companies(
            company_name="", limit=10, page=0
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        self.__mock_company_repository_instance.find_many.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertSequenceEqual(companies, mock_companies)
