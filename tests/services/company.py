from typing import Sequence
from unittest import TestCase
import asyncio
import logging

from utils.patterns import IService
from models import Company
from services.company.creation import (
    CompanyCreationService,
    CompanyCreationServiceProps,
)
from services.company.update import CompanyUpdateService, CompanyUpdateServiceProps
from services.company.exclusion import (
    CompanyExclusionService,
    CompanyExclusionServiceProps,
)
from services.company.listing import CompanyListingService, CompanyListingServiceProps


class CompanyServiceCase(TestCase):
    def test_creation(self) -> None:
        async def main():
            creation_props: CompanyCreationServiceProps = CompanyCreationServiceProps(
                company_name="Empresa teste",
                fantasy_name="Nome Fantasia teste",
                document_cnpj="029999999",
                email="vcitorhenrich993@gmail.com",
            )

            company_creation_service: IService[
                CompanyCreationServiceProps, None
            ] = CompanyCreationService(creation_props)

            await company_creation_service.execute()

        asyncio.run(main())

    def test_update(self) -> None:
        async def main():
            update_props: CompanyUpdateServiceProps = CompanyUpdateServiceProps(
                uuid="ec6812e5-7bdb-4c89-a71b-b9f07fe56ccd",
                company_name="ALTERADO",
                fantasy_name="ALTERADO",
                document_cnpj="000000000",
                email="teste@gmail.com",
            )

            company_creation_service: IService[
                CompanyUpdateServiceProps, None
            ] = CompanyUpdateService(update_props)

            await company_creation_service.execute()

        asyncio.run(main())

    def test_exclusion(self) -> None:
        async def main():
            exclusion_props: CompanyExclusionServiceProps = (
                CompanyExclusionServiceProps(
                    uuid="ec6812e5-7bdb-4c89-a71b-b9f07fe56ccd"
                )
            )

            company_creation_service: IService[
                CompanyExclusionServiceProps, None
            ] = CompanyExclusionService(exclusion_props)

            await company_creation_service.execute()

        asyncio.run(main())

    def test_listing(self) -> None:
        async def main():
            exclusion_props: CompanyListingServiceProps = CompanyListingServiceProps(
                company_name=None
            )

            company_creation_service: IService[
                CompanyListingServiceProps, Sequence[Company]
            ] = CompanyListingService(exclusion_props)

            companies: Sequence[Company] = await company_creation_service.execute()

            self.assertTrue(companies)

            logging.info(f"Companies: {companies}")

        asyncio.run(main())
