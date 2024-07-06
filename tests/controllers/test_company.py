from unittest import TestCase
from fastapi.testclient import TestClient
from httpx import Response
import logging

from server.instances import ServerInstances
from utils.constants import COMPANY_ENPOINT_NAME
from utils.entities import CompanyBodyEntity
from utils.types import DictType


class CompanyControllerTestCase(TestCase):
    def setUp(self) -> None:
        token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3V1aWQiOiI4N2JhZGE0OS04NDFkLTQ0MDUtYjVkZi1iYmY0NmRjNTQxMjAiLCJleHAiOjE3MjAyNzY0MDksImlzX3JlZnJlc2giOnRydWUsImNvbXBhbnlfdXVpZCI6IjQzNDBkYzQ4LTVmMDQtNDIzMS05YjgyLWMzZjUzMjNjMDc3YSJ9.gxO1fRlohGpohTf4G7Wei3voum61g1lwcmkLnUbjnk4"

        self.__client: TestClient = TestClient(
            ServerInstances.api, headers={"Authorization": f"Bearer {token}"}
        )

    def test_find_company(self) -> None:
        company_uuid: str = "398da0b6-7019-4b7c-b0da-ff7734be63c7"

        url: str = f"{COMPANY_ENPOINT_NAME}/{company_uuid}"

        response: Response = self.__client.get(url)

        data: DictType = response.json()

        logging.info(f"Response Data: {data}")

        self.assertEqual(response.status_code, 200)

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(data["uuid"], company_uuid)

    def test_find_companies(self) -> None:
        url: str = f"{COMPANY_ENPOINT_NAME}"

        response: Response = self.__client.get(url)

        data: DictType = response.json()

        logging.info(f"Response Data: {data}")

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(type(data), list)

        self.assertTrue(len(data) > 0)

    def test_create_company(self) -> None:
        url: str = f"{COMPANY_ENPOINT_NAME}"

        body: CompanyBodyEntity = CompanyBodyEntity(
            company_name="Empresa Teste",
            fantasy_name="Empresa Fantasia teste",
            document_cnpj="00000000",
            email="teste@gmail.com",
        )

        response: Response = self.__client.post(url, json=body.model_dump())

        data: DictType = response.json()

        logging.info(f"Response Data: {data}")

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(data["company_name"], body.company_name)

        self.assertEqual(data["fantasy_name"], body.fantasy_name)

        self.assertEqual(data["document_cnpj"], body.document_cnpj)

        self.assertEqual(data["email"], body.email)

    def test_update_company(self) -> None:
        company_uuid: str = "398da0b6-7019-4b7c-b0da-ff7734be63c7"

        url: str = f"{COMPANY_ENPOINT_NAME}/{company_uuid}"

        body: CompanyBodyEntity = CompanyBodyEntity(
            company_name="Empresa Teste",
            fantasy_name="Empresa Fantasia teste",
            document_cnpj="00000000",
            email="teste@gmail.com",
        )

        response: Response = self.__client.put(url, json=body.model_dump())

        data: DictType = response.json()

        logging.info(f"Response Data: {data}")

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(data["company_name"], body.company_name)

        self.assertEqual(data["fantasy_name"], body.fantasy_name)

        self.assertEqual(data["document_cnpj"], body.document_cnpj)

        self.assertEqual(data["email"], body.email)

        self.assertEqual(data["uuid"], company_uuid)
