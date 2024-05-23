from typing import Sequence
from unittest import TestCase
from unittest.mock import Mock
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import logging

from server.instances import ServerInstances
from server.database import Database
from models import Company
from repositories.company import (
    CompanyRepository,
    CompanyCreationRepositoryProps,
    CompanyUpdateRepositoryProps,
    CompanyExclusionRepositoryProps,
)
from utils.patterns import CreateRepository, UpdateRepository, DeleteRepository
from utils.constants import DATABASE_INSTANCE_NAME


class CompanyRepositoryCase(TestCase):
    def setUp(self) -> None:
        self.__database: Database = ServerInstances.databases.select(
            DATABASE_INSTANCE_NAME
        )

        self.__company_data: Mock = Mock()

        self.__company_data.company_name = "Empresa teste"
        self.__company_data.fantasy_name = "Nome fantasia"
        self.__company_data.document_cnpj = "02988790000"
        self.__company_data.email = "victorhenrich993@gmail.com"
        self.__company_data.uuid = ""

    def test_create(self) -> None:
        session: AsyncSession = self.__database.create_async_session()

        company_repository: CreateRepository[
            CompanyCreationRepositoryProps, None
        ] = CompanyRepository(session)

        asyncio.run(company_repository.create(self.__company_data))

    def test_update(self) -> None:
        session: AsyncSession = self.__database.create_async_session()

        company_repository: UpdateRepository[
            CompanyUpdateRepositoryProps, None
        ] = CompanyRepository(session)

        asyncio.run(company_repository.update(self.__company_data))

    def test_delete(self) -> None:
        session: AsyncSession = self.__database.create_async_session()

        company_repository: DeleteRepository[
            CompanyExclusionRepositoryProps, None
        ] = CompanyRepository(session)

        asyncio.run(company_repository.delete(self.__company_data))

    def test_get_many(self) -> None:
        filters: Mock = Mock()

        session: AsyncSession = self.__database.create_async_session()

        company_repository: DeleteRepository[
            CompanyExclusionRepositoryProps, None
        ] = CompanyRepository(session)

        companies: Sequence[Company] = asyncio.run(company_repository.get_many(filters))

        logging.info(f"Companies: {companies}")
