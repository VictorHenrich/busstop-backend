from typing import Optional, List
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock
import logging

from utils.entities import CompanyEntity
from utils.responses import BaseJSONResponse
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

    async def test_capture(self) -> None:
        company_uuid: str = ""

        if self.company:
            company_uuid = self.company.uuid

        response: BaseJSONResponse[Optional[CompanyEntity]] = await get_company(
            company_uuid=company_uuid
        )

        logging.info(f"Response: {response.data}")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.content)

        self.company = response.data.content

    async def test_list(self) -> None:
        response: BaseJSONResponse[List[CompanyEntity]] = await list_companies(
            page=0, limit=10, company_name=None
        )

        logging.info(f"Response: {response.data}")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.content)
        self.assertEqual(type(response.data.content), list)
        self.assertNotEqual(response.data.content, [])

        if response.data.content:
            self.company = response.data.content[0]

    async def test_create(self) -> None:
        company_data: Mock = Mock()

        company_data.company_name = "Transportes Capivari LTDA"
        company_data.fantasy_name = "TCL"
        company_data.document_cnpj = "000000"
        company_data.email = "teste@gmail.com"

        response: BaseJSONResponse = await create_company(company_data)

        logging.info(f"Response: {response.data}")

        self.assertEqual(response.status_code, 200)
