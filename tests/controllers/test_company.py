from typing import Optional, List
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock
import logging

from utils.entities import CompanyEntity, JSONDataEntity, JSONDataTypes
from controllers.company import (
    create_company,
    update_company,
    delete_company,
    get_company,
    list_companies,
)


class CompanyControllerTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.__company: Optional[CompanyEntity] = None

        self.__company_uuid: str = ""

    def __get_company_uuid(self) -> str:
        if self.__company:
            return self.__company.uuid

        return self.__company_uuid

    async def test_create(self) -> None:
        logging.info("...RUNNING CREATE...")

        company_body: Mock = Mock()

        company_body.company_name = "Transportes Capivari LTDA"
        company_body.fantasy_name = "TCL"
        company_body.document_cnpj = "000000"
        company_body.email = "teste@gmail.com"
        response: JSONDataEntity = await create_company(company_body)

        logging.info(f"Response Create: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)

    async def test_update(self) -> None:
        logging.info("...RUNNING UPDATE...")

        company_body: Mock = Mock()

        company_body.company_name = "Transportes ALTERADO"
        company_body.fantasy_name = "TCL ALTERADO"
        company_body.document_cnpj = "000000"
        company_body.email = "teste@gmail.com"

        company_uuid: str = self.__get_company_uuid()

        response: JSONDataEntity[None] = await update_company(
            company_uuid, company_body
        )

        logging.info(f"Response Update: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)

    async def test_delete(self) -> None:
        logging.info("...RUNNING DELETE...")
        company_uuid: str = self.__get_company_uuid()

        response: JSONDataEntity[None] = await delete_company(company_uuid=company_uuid)

        logging.info(f"Response Delete: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)

    async def test_get(self) -> None:
        logging.info("...RUNNING GET...")

        company_uuid: str = self.__get_company_uuid()

        response: JSONDataEntity[Optional[CompanyEntity]] = await get_company(
            company_uuid=company_uuid
        )

        logging.info(f"Response Get: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)
        self.assertIsNotNone(response.content)

        self.__company = response.content

    async def test_list(self) -> None:
        logging.info("...RUNNING LIST...")

        response: JSONDataEntity[List[CompanyEntity]] = await list_companies(
            page=0, limit=10, company_name=None
        )

        logging.info(f"Response List: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)
        self.assertIsNotNone(response.content)
        self.assertEqual(type(response.content), list)
        self.assertNotEqual(response.content, [])

        if response.content:
            self.__company = response.content[0]

    async def test_company_crud_automation(self) -> None:
        await self.test_create()
        await self.test_list()
        await self.test_update()
        await self.test_get()
        await self.test_delete()
