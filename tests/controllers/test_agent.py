from typing import Mapping, Any
from unittest import TestCase
from fastapi.testclient import TestClient
from httpx import Response
import logging

from server.instances import ServerInstances
from utils.constants import AGENT_ENDPOINT_NAME
from utils.entities import AgentBodyEntity


class AgentControllerTestCase(TestCase):
    def setUp(self) -> None:
        token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3V1aWQiOiIyNDg5Y2Q5OC0yMTc4LTQxMzItYmZhNi1jZDdmNmI4ZjE1N2IiLCJleHAiOjE3MjAyMTEyNDIsImlzX3JlZnJlc2giOmZhbHNlLCJjb21wYW55X3V1aWQiOiIyNDg5Y2Q5OC0yMTc4LTQxMzItYmZhNi1jZDdmNmI4ZjE1N2EifQ.itwX8B-N9iUOCD1hxLac3L7E1-3ktaSb9kK8xnq4vm0"

        self.__client: TestClient = TestClient(
            ServerInstances.api, headers={"Authorization": f"Bearer {token}"}
        )

    def test_create_agent(self) -> None:
        url: str = f"{AGENT_ENDPOINT_NAME}"

        body: AgentBodyEntity = AgentBodyEntity(
            name="Usuário teste", email="victorhenrich@gmail.com", password="1234"
        )

        response: Response = self.__client.post(url, json=body.model_dump())

        data: Mapping[str, Any] = response.json()

        logging.info(f"Response Data: {data}")

        self.assertEqual(response.status_code, 200)

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(body.name, data["name"])

        self.assertEqual(body.email, data["email"])

    def test_update_agent(self) -> None:
        agent_uuid: str = "8ac1eee1-500a-4849-9a20-a1042b47eb88"

        url: str = f"{AGENT_ENDPOINT_NAME}/{agent_uuid}"

        body: AgentBodyEntity = AgentBodyEntity(
            name="Usuário teste", email="master123@gmail.com", password="1234"
        )

        response: Response = self.__client.put(url, json=body.model_dump())

        data: Mapping[str, Any] = response.json()

        logging.info(f"Response Data: {data}")

        self.assertEqual(response.status_code, 200)

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(body.name, data["name"])

        self.assertEqual(body.email, data["email"])

        self.assertEqual(agent_uuid, data["uuid"])

    def test_delete_agent(self) -> None:
        agent_uuid: str = "a840eaac-ca35-40f6-b57c-1d590c975941"

        url: str = f"{AGENT_ENDPOINT_NAME}/{agent_uuid}"

        response: Response = self.__client.delete(url)

        data: Mapping[str, Any] = response.json()

        logging.info(f"Response Data: {data}")

        self.assertEqual(response.status_code, 200)

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(agent_uuid, data["uuid"])

    def test_find_agent(self) -> None:
        agent_uuid: str = "a840eaac-ca35-40f6-b57c-1d590c975941"

        url: str = f"{AGENT_ENDPOINT_NAME}/{agent_uuid}"

        response: Response = self.__client.get(url)

        data: Mapping[str, Any] = response.json()

        logging.info(f"Response Data: {data}")

        self.assertEqual(response.status_code, 200)

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(agent_uuid, data["uuid"])

    def test_find_agents(self) -> None:
        url: str = f"{AGENT_ENDPOINT_NAME}"

        response: Response = self.__client.get(url)

        data: Mapping[str, Any] = response.json()

        logging.info(f"Response Data: {data}")

        self.assertEqual(response.status_code, 200)

        data = data["content"]

        self.assertIsNotNone(data)

        self.assertEqual(type(data), list)

        self.assertTrue(len(data) > 0)
