from typing import Mapping, Any
from unittest import TestCase
from fastapi.testclient import TestClient
from httpx import Response
import logging

from server.instances import ServerInstances
from utils.constants import COMPANY_ENPOINT_NAME


class CompanyControllerTestCase(TestCase):
    def setUp(self) -> None:
        self.__client: TestClient = TestClient(ServerInstances.api)

    def test_create(self) -> None:
        token: str = ""

        url: str = f"{COMPANY_ENPOINT_NAME}"

        response: Response = self.__client.get(
            url, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)

        data: Mapping[str, Any] = response.json()

        logging.info(f"Response Create: {data}")
