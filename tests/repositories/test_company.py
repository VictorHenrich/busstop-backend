from typing import Sequence, Optional
from unittest.mock import Mock
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


class CompanyRepositoryOnlineTestCase(BaseRepositoryTestCase):
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()

        self.__company: Company = await create_company()

    async def test_find_many(self) -> None:
        limit: int = 10

        page: int = 0

        async with database.create_async_session() as session:
            repository: IFindManyRepository[ICompanyFindManyRepository, Company] = (
                CompanyRepository(session)
            )

            repository_params: ICompanyFindManyRepository = Mock(limit=limit, page=page)

            companies: Sequence[Company] = await repository.find_many(repository_params)

            self.assertTrue(len(companies) > 0)

            self.assertTrue(len(companies) <= limit)

    async def test_find(self):
        async with database.create_async_session() as session:
            repository: IFindRepository[ICompanyFindRepository, Company] = (
                CompanyRepository(session)
            )

            repository_params: ICompanyFindRepository = Mock(uuid=self.__company.uuid)

            company: Optional[Company] = await repository.find(repository_params)

            self.assertIsNotNone(company)

    async def test_delete(self) -> None:
        async with database.create_async_session() as session:
            repository: IDeleteRepository[
                ICompanyDeleteRepository, Optional[Company]
            ] = CompanyRepository(session)

            repository_params: ICompanyDeleteRepository = Mock(
                uuid=self.__company.uuid, instance=None
            )

            company: Optional[Company] = await repository.delete(repository_params)

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
                uuid=self.__company.uuid,
                instance=None,
            )

            company: Optional[Company] = await repository.update(repository_params)

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

            await session.commit()

            self.assertIsNotNone(company)
