from unittest import TestCase
from fastapi.testclient import TestClient
from httpx import Response
import logging

from server.instances import ServerInstances
from utils.constants import AUTH_ENDPOINT_NAME
from utils.entities import AuthBodyEntity
from utils.types import DictType


class AuthControllerTestCase(TestCase):
    def setUp(self) -> None:
        self.__agent_client: TestClient = TestClient(ServerInstances.agent_api)

        self.__user_client: TestClient = TestClient(ServerInstances.user_api)

    def test_authenticate_agent(self) -> None:
        url: str = f"{AUTH_ENDPOINT_NAME}/agent"

        body: AuthBodyEntity = AuthBodyEntity(email="master@gmail.com", password="1234")

        response: Response = self.__agent_client.post(url, json=body.model_dump())

        data: DictType = response.json()

        logging.info(f"ResponseData: {data}")

        self.assertEqual(response.status_code, 200)

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertIsNotNone(data["token"])

        self.assertIsNotNone(data["refresh_token"])

    def test_authenticate_agent_with_email_not_found(self) -> None:
        url: str = f"{AUTH_ENDPOINT_NAME}/agent"

        wrong_email: str = "teste@gmail.com"

        body: AuthBodyEntity = AuthBodyEntity(email=wrong_email, password="")

        response: Response = self.__agent_client.post(url, json=body.model_dump())

        data: DictType = response.json()

        logging.info(f"ResponseData: {data}")

        self.assertEqual(response.status_code, 500)

        self.assertEqual(
            data["detail"], f"User with email '{wrong_email}' was not found"
        )

    def test_authenticate_agent_with_password_invalid(self) -> None:
        url: str = f"{AUTH_ENDPOINT_NAME}/agent"

        body: AuthBodyEntity = AuthBodyEntity(email="master@gmail.com", password="")

        response: Response = self.__agent_client.post(url, json=body.model_dump())

        data: DictType = response.json()

        logging.info(f"ResponseData: {data}")

        self.assertEqual(response.status_code, 500)

        self.assertEqual(type(data["detail"]), str)

        self.assertTrue(data["detail"].startswith("Invalid password passed to user"))

    def test_authenticate_user(self) -> None:
        url: str = f"{AUTH_ENDPOINT_NAME}/user"

        body: AuthBodyEntity = AuthBodyEntity(email="master@gmail.com", password="1234")

        response: Response = self.__user_client.post(url, json=body.model_dump())

        data: DictType = response.json()

        logging.info(f"ResponseData: {data}")

        self.assertEqual(response.status_code, 200)

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertIsNotNone(data["token"])

        self.assertIsNotNone(data["refresh_token"])
