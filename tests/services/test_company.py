from typing import Sequence, Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, Mock, AsyncMock

from models import Company
from server.database import Database
from repositories.company import CompanyRepository
from services.company import CompanyService


class CompanyServiceTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_async_session: AsyncMock = AsyncMock()

        self.__mock_async_session.__aenter__.side_effect = (
            lambda: self.__mock_async_session
        )

        self.__mock_async_session.commit.return_value = None

        self.__company_service: CompanyService = CompanyService()

        self.__mock_company: Mock = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia TESTE",
            document_cnpj="00000000",
            email="teste@gmail.com",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df68a",
        )

    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=Database)
    async def test_create(
        self, mock_database: Mock, mock_company_repository_class: Mock
    ) -> None:
        mock_database.create_async_session.side_effect = (
            lambda: self.__mock_async_session
        )

        mock_instance_repository: AsyncMock = AsyncMock()

        mock_instance_repository.create.return_value = self.__mock_company

        mock_company_repository_class.return_value = mock_instance_repository

        company: Optional[Company] = await self.__company_service.create_company(
            company_name=self.__mock_company.company_name,
            fantasy_name=self.__mock_company.fantasy_name,
            document_cnpj=self.__mock_company.document_cnpj,
            email=self.__mock_company.email,
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        self.__mock_async_session.commit.assert_awaited_once()

        mock_instance_repository.create.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertEqual(company, self.__mock_company)

    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=Database)
    async def test_update(
        self, mock_database: Mock, mock_company_repository_class: Mock
    ) -> None:
        mock_database.create_async_session.side_effect = (
            lambda: self.__mock_async_session
        )

        mock_instance_repository: AsyncMock = AsyncMock()

        mock_instance_repository.update.return_value = self.__mock_company

        mock_company_repository_class.return_value = mock_instance_repository

        company: Optional[Company] = await self.__company_service.update_company(
            company_uuid=self.__mock_company.uuid,
            company_name=self.__mock_company.company_name,
            fantasy_name=self.__mock_company.fantasy_name,
            document_cnpj=self.__mock_company.document_cnpj,
            email=self.__mock_company.email,
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        self.__mock_async_session.commit.assert_awaited_once()

        mock_instance_repository.update.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertEqual(company, self.__mock_company)

    @patch("services.company.copy")
    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=Database)
    async def test_delete(
        self, mock_database: Mock, mock_company_repository_class: Mock, mock_copy: Mock
    ) -> None:
        mock_database.create_async_session.side_effect = (
            lambda: self.__mock_async_session
        )

        mock_instance_repository: AsyncMock = AsyncMock()

        mock_instance_repository.delete.return_value = self.__mock_company

        mock_company_repository_class.return_value = mock_instance_repository

        mock_copy.return_value = self.__mock_company

        company: Optional[Company] = await self.__company_service.delete_company(
            company_uuid=self.__mock_company.uuid,
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        self.__mock_async_session.commit.assert_awaited_once()

        mock_instance_repository.delete.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertEqual(company, self.__mock_company)

    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=Database)
    async def test_find(
        self,
        mock_database: Mock,
        mock_company_repository_class: Mock,
    ) -> None:
        mock_database.create_async_session.side_effect = (
            lambda: self.__mock_async_session
        )

        mock_instance_repository: AsyncMock = AsyncMock()

        mock_instance_repository.find.return_value = self.__mock_company

        mock_company_repository_class.return_value = mock_instance_repository

        company: Company = await self.__company_service.find_company(
            company_uuid=self.__mock_company.uuid,
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        mock_instance_repository.find.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertEqual(company, self.__mock_company)

    @patch("services.company.CompanyRepository", spec=CompanyRepository)
    @patch("services.company.database", spec=Database)
    async def test_find_many(
        self,
        mock_database: Mock,
        mock_company_repository_class: Mock,
    ) -> None:
        mock_companies: Sequence[Company] = [self.__mock_company]

        mock_database.create_async_session.side_effect = (
            lambda: self.__mock_async_session
        )

        mock_instance_repository: AsyncMock = AsyncMock()

        mock_instance_repository.find_many.return_value = mock_companies

        mock_company_repository_class.return_value = mock_instance_repository

        companies: Sequence[Company] = await self.__company_service.find_companies(
            company_name="", limit=10, page=0
        )

        self.__mock_async_session.__aenter__.assert_called_once()

        mock_instance_repository.find_many.assert_awaited_once()

        mock_database.create_async_session.assert_called_once()

        self.assertSequenceEqual(companies, mock_companies)
