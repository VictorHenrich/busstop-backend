from typing import Sequence
from unittest import TestCase
import asyncio

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
                company_name="", fantasy_name="", document_cnpj="", email=""
            )

            company_creation_service: IService[
                CompanyCreationServiceProps, None
            ] = CompanyCreationService(creation_props)

            await company_creation_service.execute()

        asyncio.run(main())

    def test_update(self) -> None:
        async def main():
            update_props: CompanyUpdateServiceProps = CompanyUpdateServiceProps(
                uuid="", company_name="", fantasy_name="", document_cnpj="", email=""
            )

            company_creation_service: IService[
                CompanyUpdateServiceProps, None
            ] = CompanyUpdateService(update_props)

            await company_creation_service.execute()

        asyncio.run(main())

    def test_exclusion(self) -> None:
        async def main():
            exclusion_props: CompanyExclusionServiceProps = (
                CompanyExclusionServiceProps(uuid="")
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

            await company_creation_service.execute()

        asyncio.run(main())
