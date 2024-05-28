from typing import Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock
import logging

from models import Company, database
from repositories.company import (
    CompanyRepository,
    CompanyCreationRepositoryProps,
    CompanyUpdateRepositoryProps,
    CompanyExclusionRepositoryProps,
)
from utils.patterns import ICreateRepository, IUpdateRepository, IDeleteRepository


class CompanyRepositoryTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__company_data: Mock = Mock()

        self.__company_data.company_name = "Empresa teste alterado"
        self.__company_data.fantasy_name = "Nome fantasia alterado"
        self.__company_data.document_cnpj = "02988790000"
        self.__company_data.email = "victorhenrich993@gmail.com"
        self.__company_data.uuid = "6df97b7d-2beb-4d60-ae75-b742ac3df68a"

    async def test_create(self) -> None:
        async with database.create_async_session() as session:
            company_repository: ICreateRepository[
                CompanyCreationRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.create(self.__company_data)

            await session.commit()

    async def test_update(self) -> None:
        async with database.create_async_session() as session:
            company_repository: IUpdateRepository[
                CompanyUpdateRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.update(self.__company_data)

            await session.commit()

    async def test_delete(self) -> None:
        async with database.create_async_session() as session:
            company_repository: IDeleteRepository[
                CompanyExclusionRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.delete(self.__company_data)

            await session.commit()

    async def test_find_many(self) -> None:
        async with database.create_async_session() as session:
            filters: Mock = Mock()

            company_repository: IDeleteRepository[
                CompanyExclusionRepositoryProps, None
            ] = CompanyRepository(session)

            companies: Sequence[Company] = await company_repository.find_many(filters)

            logging.info(f"Companies: {companies}")
