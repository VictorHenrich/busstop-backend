from typing import Optional, Union, List
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock
import logging

from utils.responses import JSONBaseResponse, JSONBaseResponseTypes
from utils.entities import PointEntity
from controllers.point import (
    create_point,
    update_point,
    delete_point,
    get_point,
    list_points,
)


class PointControllerTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.__point: Optional[PointEntity] = None

        self.__company_uuid: str = ""

        self.__point_uuid: str = ""

    def __get_point_uuid(self) -> str:
        if self.__point:
            return self.__point.uuid

        return self.__point_uuid

    async def test_create(self) -> None:
        logging.info("...CREATION RUNNING...")

        point_body: Mock = Mock(
            address_state="SC",
            address_city="Capivari de Baixo",
            address_neighborhood="Centro",
            address_street="Centro",
            address_number="000",
            latitude="-20000",
            longitude="-150000",
        )

        response: JSONBaseResponse[Optional[PointEntity]] = await create_point(
            self.__company_uuid, point_body
        )

        logging.info(f"Response Creation: {response}")

        self.assertEqual(response.info, JSONBaseResponseTypes.SUCCESS)
        self.assertIsNotNone(response.content)

        if response.content:
            self.__point = response.content

    async def test_update(self) -> None:
        logging.info("...UPDATE RUNNING...")

        point_body: Union[Mock, PointEntity] = Mock()

        if self.__point:
            point_body = self.__point

        point_body.address_state = "ALTERADO"
        point_body.address_city = "ALTERADO"
        point_body.address_neighborhood = "ALTERADO"
        point_body.address_street = "ALTERADO"
        point_body.address_number = "ALTERADO"
        point_body.latitude = "0000000"
        point_body.longitude = "000000"

        point_uuid: str = self.__get_point_uuid()

        response: JSONBaseResponse[Optional[PointEntity]] = await update_point(
            point_uuid, point_body
        )

        logging.info(f"Response Update: {response}")

        self.assertEqual(response.info, JSONBaseResponseTypes.SUCCESS)
        self.assertIsNotNone(response.content)

        if response.content:
            self.__point = response.content

    async def test_delete(self) -> None:
        logging.info("...EXCLUSION RUNNING...")

        point_uuid: str = self.__get_point_uuid()

        response: JSONBaseResponse[Optional[PointEntity]] = await delete_point(
            point_uuid
        )

        logging.info(f"Response Exclusion: {response}")

        self.assertEqual(response.info, JSONBaseResponseTypes.SUCCESS)

    async def test_get(self) -> None:
        logging.info("...CAPTURE RUNNING...")

        point_uuid: str = self.__get_point_uuid()

        response: JSONBaseResponse[Optional[PointEntity]] = await get_point(point_uuid)

        logging.info(f"Response Capture: {response}")

        self.assertEqual(response.info, JSONBaseResponseTypes.SUCCESS)
        self.assertIsNotNone(response.content)

    async def test_list(self) -> None:
        logging.info("...LISTING RUNNING...")

        response: JSONBaseResponse[List[PointEntity]] = await list_points(
            self.__company_uuid
        )

        logging.info(f"Response Listing: {response}")

        self.assertEqual(response.info, JSONBaseResponseTypes.SUCCESS)
        self.assertIsNotNone(response.content)
        self.assertNotEqual(response.content, [])

    async def test_point_automation_crud(self) -> None:
        await self.test_create()
        await self.test_update()
        await self.test_get()
        await self.test_list()
        await self.test_delete()
        await self.test_list()
