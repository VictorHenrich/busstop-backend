from typing import Sequence, Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

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


class CompanyRepositoryOnlineTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__company_uuid: str = ""

    async def __create_company(self, session: AsyncSession) -> Optional[Company]:
        repository: ICreateRepository[ICompanyCreateRepository, Optional[Company]] = (
            CompanyRepository(session)
        )

        repository_params: ICompanyCreateRepository = Mock(
            company_name="Empresa Teste",
            fantasy_name="Nome Fantasia Teste",
            document_cnpj="00000000",
            email="teste@gmail.com",
        )

        return await repository.create(repository_params)

    async def __update_company(
        self, session: AsyncSession, company_uuid: str
    ) -> Optional[Company]:
        repository: IUpdateRepository[ICompanyUpdateRepository, Optional[Company]] = (
            CompanyRepository(session)
        )

        repository_params: ICompanyUpdateRepository = Mock(
            company_name="Empresa Teste Alterada",
            fantasy_name="Nome Fantasia Alterada",
            document_cnpj="00000000",
            email="alterado@gmail.com",
            uuid=company_uuid,
        )

        return await repository.update(repository_params)

    async def __delete_company(
        self, session: AsyncSession, company_uuid: str
    ) -> Optional[Company]:
        repository: IDeleteRepository[ICompanyDeleteRepository, Optional[Company]] = (
            CompanyRepository(session)
        )

        repository_params: ICompanyDeleteRepository = Mock(uuid=company_uuid)

        return await repository.delete(repository_params)

    async def __find_company(
        self, session: AsyncSession, company_uuid: str
    ) -> Optional[Company]:
        repository: IFindRepository[ICompanyFindRepository, Company] = (
            CompanyRepository(session)
        )

        repository_params: ICompanyFindRepository = Mock(uuid=company_uuid)

        return await repository.find(repository_params)

    async def __find_many_company(
        self, session: AsyncSession, limit: int, page: int
    ) -> Sequence[Company]:
        repository: IFindManyRepository[ICompanyFindManyRepository, Company] = (
            CompanyRepository(session)
        )

        repository_params: ICompanyFindManyRepository = Mock(limit=limit, page=page)

        return await repository.find_many(repository_params)

    async def test_find_many(self) -> None:
        limit: int = 10

        async with database.create_async_session() as session:
            companies: Sequence[Company] = await self.__find_many_company(
                session, limit=limit, page=0
            )

            self.assertTrue(len(companies) > 0)

            self.assertTrue(len(companies) <= limit)

    async def test_find(self):
        async with database.create_async_session() as session:
            company: Optional[Company] = await self.__find_company(
                session, self.__company_uuid
            )

            self.assertIsNotNone(company)

    async def test_delete(self) -> None:
        async with database.create_async_session() as session:
            company: Optional[Company] = await self.__delete_company(
                session, self.__company_uuid
            )

            await session.commit()

            self.assertIsNotNone(company)

    async def test_update(self) -> None:
        async with database.create_async_session() as session:
            company: Optional[Company] = await self.__update_company(
                session, self.__company_uuid
            )

            await session.commit()

            self.assertIsNotNone(company)

    async def test_create(self) -> None:
        async with database.create_async_session() as session:
            company: Optional[Company] = await self.__create_company(session)

            await session.commit()

            self.assertIsNotNone(company)

    async def test_crud(self) -> None:
        async with database.create_async_session() as session:
            company: Company = await self.__create_company(session)

            assert company is not None

            company = await self.__update_company(session, company.uuid)

            assert company is not None

            company, companies = await asyncio.gather(
                self.__find_company(session, company.uuid),
                self.__find_many_company(session, limit=10, page=0),
            )

            assert company is not None

            assert len(companies) > 0

            company = await self.__delete_company(session, company.uuid)

            assert company is not None

            session.rollback()
