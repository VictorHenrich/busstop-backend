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
    @classmethod
    def setUpClass(cls) -> None:
        cls.company: Optional[CompanyEntity] = None

    def __get_company_uuid(self) -> str:
        if self.company:
            return self.company.uuid

        return ""

    async def test_delete(self) -> None:
        company_uuid: str = self.__get_company_uuid()

        response: JSONDataEntity[None] = await delete_company(company_uuid=company_uuid)

        logging.info(f"Response: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)

    async def test_get(self) -> None:
        company_uuid: str = self.__get_company_uuid()

        response: JSONDataEntity[Optional[CompanyEntity]] = await get_company(
            company_uuid=company_uuid
        )

        logging.info(f"Response: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)
        self.assertIsNotNone(response.content)

        self.company = response.content

    async def test_update(self) -> None:
        company_body: Mock = Mock()

        company_body.company_name = "Transportes ALTERADO"
        company_body.fantasy_name = "TCL ALTERADO"
        company_body.document_cnpj = "000000"
        company_body.email = "teste@gmail.com"

        company_uuid: str = self.__get_company_uuid()

        response: JSONDataEntity[None] = await update_company(
            company_uuid, company_body
        )

        logging.info(f"Response: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)

    async def test_list(self) -> None:
        response: JSONDataEntity[List[CompanyEntity]] = await list_companies(
            page=0, limit=10, company_name=None
        )

        logging.info(f"Response: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)
        self.assertIsNotNone(response.content)
        self.assertEqual(type(response.content), list)
        self.assertNotEqual(response.content, [])

        if response.content:
            self.company = response.content[0]

    async def test_create(self) -> None:
        company_body: Mock = Mock()

        company_body.company_name = "Transportes Capivari LTDA"
        company_body.fantasy_name = "TCL"
        company_body.document_cnpj = "000000"
        company_body.email = "teste@gmail.com"
        response: JSONDataEntity = await create_company(company_body)

        logging.info(f"Response: {response}")

        self.assertEqual(response.info, JSONDataTypes.SUCCESS)

    async def test_company_automation(self) -> None:
        await self.test_create()
        await self.test_list()
        await self.test_update()
        await self.test_get()
        await self.test_delete()
