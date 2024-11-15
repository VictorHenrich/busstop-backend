from unittest import TestCase
from fastapi.testclient import TestClient
from httpx import Response
import logging

from server.instances import ServerInstances
from utils.config import USER_ENDPOINT_NAME
from utils.entities import UserBodyEntity
from utils.types import DictType


class UserControllerTestCase(TestCase):
    def setUp(self) -> None:
        token: str = ""

        self.__client: TestClient = TestClient(
            ServerInstances.user_api, headers={"Authorization": f"Bearer {token}"}
        )

    def test_create_user(self) -> None:
        url: str = f"{USER_ENDPOINT_NAME}"

        body: UserBodyEntity = UserBodyEntity(
            name="Usuário teste", email="usertest@gmail.com", password="1234"
        )

        response: Response = self.__client.post(url, json=body.model_dump())

        data: DictType = response.json()

        logging.info(f"Response Data: {data}")

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(body.name, data["name"])

        self.assertEqual(body.email, data["email"])

    def test_update_user(self) -> None:
        user_uuid: str = ""

        url: str = f"{USER_ENDPOINT_NAME}/{user_uuid}"

        body: UserBodyEntity = UserBodyEntity(
            name="Usuário teste", email="usertest@gmail.com", password="1234"
        )

        response: Response = self.__client.put(url, json=body.model_dump())

        data: DictType = response.json()

        logging.info(f"Response Data: {data}")

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(body.name, data["name"])

        self.assertEqual(body.email, data["email"])

        self.assertEqual(user_uuid, data["uuid"])

    def test_delete_user(self) -> None:
        user_uuid: str = ""

        url: str = f"{USER_ENDPOINT_NAME}/{user_uuid}"

        response: Response = self.__client.delete(url)

        data: DictType = response.json()

        logging.info(f"Response Data: {data}")

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(user_uuid, data["uuid"])

    def test_find_user(self) -> None:
        user_uuid: str = ""

        url: str = f"{USER_ENDPOINT_NAME}/{user_uuid}"

        response: Response = self.__client.get(url)

        data: DictType = response.json()

        logging.info(f"Response Data: {data}")

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(user_uuid, data["uuid"])
