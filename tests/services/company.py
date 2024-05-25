from typing import Sequence
from unittest import TestCase
import asyncio
import logging

from utils.patterns import IService
from models import Company
from services.company.creation import CompanyCreationService
from services.company.update import CompanyUpdateService
from services.company.exclusion import CompanyExclusionService
from services.company.listing import CompanyListingService


class CompanyServiceCase(TestCase):
    def test_creation(self) -> None:
        async def main():
            company_service: IService[None] = CompanyCreationService(
                company_name="TCL",
                fantasy_name="Transportes Capivari LTDA",
                document_cnpj="000000000",
                email="transportescapivari@gmail.com",
            )

            await company_service.execute()

        asyncio.run(main())

    def test_update(self) -> None:
        async def main():
            company_service: IService[None] = CompanyUpdateService(
                company_name="TCL ALTERADO",
                fantasy_name="Transportes Capivari LTDA ALTERADO",
                document_cnpj="000000000",
                email="transportescapivari@gmail.com",
                uuid="e95d2a92-a5a2-4cb8-aa0f-bbea29be9afa",
            )

            await company_service.execute()

        asyncio.run(main())

    def test_exclusion(self) -> None:
        async def main():
            company_service: IService[None] = CompanyExclusionService(
                uuid="e95d2a92-a5a2-4cb8-aa0f-bbea29be9afa"
            )

            await company_service.execute()

        asyncio.run(main())

    def test_listing(self) -> None:
        async def main():
            company_service: IService[Sequence[Company]] = CompanyListingService(
                company_name=None
            )

            companies: Sequence[Company] = await company_service.execute()

            self.assertTrue(companies)

            logging.info(f"Companies: {companies}")

        asyncio.run(main())
