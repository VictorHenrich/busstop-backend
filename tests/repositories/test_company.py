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

        self.__company_data.company_name = "Empresa teste alterado"
        self.__company_data.fantasy_name = "Nome fantasia alterado"
        self.__company_data.document_cnpj = "02988790000"
        self.__company_data.email = "victorhenrich993@gmail.com"
        self.__company_data.uuid = "6df97b7d-2beb-4d60-ae75-b742ac3df68a"

    def test_create(self) -> None:
        async def main() -> None:
            session: AsyncSession = self.__database.create_async_session()

            company_repository: CreateRepository[
                CompanyCreationRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.create(self.__company_data)

            await session.commit()

        asyncio.run(main())

    def test_update(self) -> None:
        async def main() -> None:
            session: AsyncSession = self.__database.create_async_session()

            company_repository: UpdateRepository[
                CompanyUpdateRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.update(self.__company_data)

            await session.commit()

        asyncio.run(main())

    def test_delete(self) -> None:
        async def main() -> None:
            session: AsyncSession = self.__database.create_async_session()

            company_repository: DeleteRepository[
                CompanyExclusionRepositoryProps, None
            ] = CompanyRepository(session)

            await company_repository.delete(self.__company_data)

            await session.commit()

        asyncio.run(main())

    def test_get_many(self) -> None:
        async def main() -> Sequence[Company]:
            filters: Mock = Mock()

            session: AsyncSession = self.__database.create_async_session()

            company_repository: DeleteRepository[
                CompanyExclusionRepositoryProps, None
            ] = CompanyRepository(session)

            companies: Sequence[Company] = await company_repository.get_many(filters)

            await session.close()

            return companies

        companies: Sequence[Company] = asyncio.run(main())

        logging.info(f"Companies: {companies}")
