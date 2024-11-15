from typing import Sequence, Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock
import logging

from models import Company, database
from repositories.company import (
    CompanyRepository,
    ICompanyCreateRepository,
    ICompanyUpdateRepository,
    ICompanyDeleteRepository,
    ICompanyFindRepository,
    ICompanyFindManyRepository,
)
from utils.patterns import (
    ICreateRepository,
    IFindRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindManyRepository,
)
from .mocks import create_company
from .common import BaseRepositoryTestCase


class CompanyRepositoryOfflineTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_company: Mock = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia TESTE",
            document_cnpj="00000000",
            email="teste@gmail.com",
            uuid="6df97b7d-2beb-4d60-ae75-b742ac3df68a",
        )

        self.__mock_session: AsyncMock = AsyncMock()

    async def test_create(self) -> None:
        self.__mock_session.scalar.return_value = self.__mock_company

        company_repository: ICreateRepository[
            ICompanyCreateRepository, Optional[Company]
        ] = CompanyRepository(self.__mock_session)

        company: Optional[Company] = await company_repository.create(
            self.__mock_company
        )

        self.__mock_session.scalar.assert_awaited_once()

        self.assertIsNotNone(company)

        self.assertEqual(company, self.__mock_company)

    async def test_update(self) -> None:
        self.__mock_session.scalar.return_value = self.__mock_company

        company_repository: IUpdateRepository[
            ICompanyUpdateRepository, Optional[Company]
        ] = CompanyRepository(self.__mock_session)

        company: Optional[Company] = await company_repository.update(
            self.__mock_company
        )

        self.__mock_session.scalar.assert_awaited_once()

        self.assertIsNotNone(company)

        self.assertEqual(company, self.__mock_company)

    async def test_delete(self) -> None:
        self.__mock_session.scalar.return_value = self.__mock_company

        filter_props: Mock = Mock(uuid="")

        company_repository: IDeleteRepository[
            ICompanyDeleteRepository, Optional[Company]
        ] = CompanyRepository(self.__mock_session)

        company: Optional[Company] = await company_repository.delete(filter_props)

        self.__mock_session.scalar.assert_awaited_once()

        self.assertIsNotNone(company)

        self.assertEqual(company, self.__mock_company)

    async def test_get(self) -> None:
        self.__mock_session.scalar.return_value = self.__mock_company

        filter_props: Mock = Mock(uuid="")

        company_repository: IFindRepository[ICompanyFindRepository, Company] = (
            CompanyRepository(self.__mock_session)
        )

        company: Optional[Company] = await company_repository.find(filter_props)

        self.__mock_session.scalar.assert_awaited_once()

        self.assertIsNotNone(company)

        self.assertEqual(company, self.__mock_company)

    async def test_list(self) -> None:
        mock_companies: Sequence[Company] = [self.__mock_company]

        filter_props: Mock = Mock(company_name="TESTE", limit=50, page=0)

        mock_result_session: Mock = Mock()

        mock_result_session.all.return_value = mock_companies

        self.__mock_session.scalars.return_value = mock_result_session

        company_repository: IFindManyRepository[ICompanyFindManyRepository, Company] = (
            CompanyRepository(self.__mock_session)
        )

        companies: Sequence[Company] = await company_repository.find_many(filter_props)

        mock_result_session.all.assert_called_once()

        self.__mock_session.scalars.assert_awaited_once()

        self.assertNotEqual(companies, [])

        self.assertSequenceEqual(companies, mock_companies)


class CompanyRepositoryOnlineTestCase(BaseRepositoryTestCase):
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()

        self.company: Company = await create_company()

    async def test_find_many(self) -> None:
        limit: int = 10

        page: int = 0

        async with database.create_async_session() as session:
            repository: IFindManyRepository[ICompanyFindManyRepository, Company] = (
                CompanyRepository(session)
            )

            repository_params: ICompanyFindManyRepository = Mock(limit=limit, page=page)

            companies: Sequence[Company] = await repository.find_many(repository_params)

            logging.info(f"Companies: {companies}\n")

            self.assertTrue(len(companies) > 0)

            self.assertTrue(len(companies) <= limit)

    async def test_find(self):
        async with database.create_async_session() as session:
            repository: IFindRepository[ICompanyFindRepository, Company] = (
                CompanyRepository(session)
            )

            repository_params: ICompanyFindRepository = Mock(uuid=self.company.uuid)

            company: Optional[Company] = await repository.find(repository_params)

            logging.info(f"Company Finded: {company}")

            self.assertIsNotNone(company)

    async def test_delete(self) -> None:
        async with database.create_async_session() as session:
            repository: IDeleteRepository[
                ICompanyDeleteRepository, Optional[Company]
            ] = CompanyRepository(session)

            repository_params: ICompanyDeleteRepository = Mock(
                uuid=self.company.uuid, instance=None
            )

            company: Optional[Company] = await repository.delete(repository_params)

            logging.info(f"Company Deleted: {company}")

            await session.commit()

            self.assertIsNotNone(company)

    async def test_update(self) -> None:
        async with database.create_async_session() as session:
            repository: IUpdateRepository[
                ICompanyUpdateRepository, Optional[Company]
            ] = CompanyRepository(session)

            repository_params: ICompanyUpdateRepository = Mock(
                company_name="Empresa Teste Alterada",
                fantasy_name="Nome Fantasia Alterada",
                document_cnpj="00000000",
                email="alterado@gmail.com",
                uuid=self.company.uuid,
                instance=None,
            )

            company: Optional[Company] = await repository.update(repository_params)

            logging.info(f"Company Updated: {company}")

            await session.commit()

            self.assertIsNotNone(company)

    async def test_create(self) -> None:
        async with database.create_async_session() as session:
            repository: ICreateRepository[
                ICompanyCreateRepository, Optional[Company]
            ] = CompanyRepository(session)

            repository_params: ICompanyCreateRepository = Mock(
                company_name="Empresa Teste",
                fantasy_name="Nome Fantasia Teste",
                document_cnpj="00000000",
                email="teste@gmail.com",
                instance=None,
            )

            company: Optional[Company] = await repository.create(repository_params)

            logging.info(f"Company Created: {company}")

            await session.commit()

            self.assertIsNotNone(company)
