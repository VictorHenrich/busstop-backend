from typing import Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch
import logging

from services.geolocation import GeoLocationService
from models import Point
from utils.types import DictType, TransportModelType


class GeolocationServiceTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_async_client_instance: AsyncMock = AsyncMock()

        self.__mock_response: Mock = Mock()

        self.__mock_response.status_code = 200

        self.__mock_response.raise_for_status.return_value = None

        self.__mock_response.json.return_value = None

        self.__mock_async_client_instance.get.return_value = self.__mock_response

        self.__mock_async_client_instance.__aenter__.return_value = (
            self.__mock_async_client_instance
        )

    @patch("services.geolocation.AsyncClient")
    async def test_find_address(self, mock_async_client_class: Mock) -> None:
        amount_register: int = 2

        result: Sequence[Point] = [
            Mock(
                address_zip_code="88745-000",
                address_state="SC",
                address_city="Capivari de Baixo",
                address_neighborhood="",
                address_street="",
                address_number="",
                latitude="-28.4412408",
                longitude="-48.9505159",
                uuid=None,
            )
            for _ in range(amount_register)
        ]

        self.__mock_response.json.return_value = {
            "results": [
                {
                    "address_components": [
                        {
                            "long_name": "88745-000",
                            "short_name": "88745-000",
                            "types": ["postal_code"],
                        },
                        {
                            "long_name": "Capivari de Baixo",
                            "short_name": "Capivari de Baixo",
                            "types": ["administrative_area_level_2", "political"],
                        },
                        {
                            "long_name": "State of Santa Catarina",
                            "short_name": "SC",
                            "types": ["administrative_area_level_1", "political"],
                        },
                    ],
                    "geometry": {"location": {"lat": -28.4412408, "lng": -48.9505159}},
                }
                for _ in range(amount_register)
            ]
        }

        self.__mock_response.status_code = 200

        mock_async_client_class.return_value = self.__mock_async_client_instance

        geolocation_service: GeoLocationService = GeoLocationService()

        locations: Sequence[Point] = await geolocation_service.find_address("Teste")

        logging.info(f"Located Locations: {locations}")

        location1: Point = result[0]

        location2: Point = locations[0]

        self.__mock_async_client_instance.__aenter__.assert_called_once()

        self.__mock_async_client_instance.get.assert_awaited_once()

        self.__mock_response.json.assert_called_once()

        self.__mock_response.raise_for_status.assert_called_once()

        self.assertEqual(self.__mock_response.status_code, 200)

        self.assertEqual(len(locations), len(result))

        self.assertEqual(location1.latitude, location2.latitude)

        self.assertEqual(location1.longitude, location2.longitude)

    @patch("services.geolocation.AsyncClient")
    async def test_calculate_distance(self, mock_async_client_class: Mock) -> None:
        total_rows: int = 1

        total_elements: int = 2

        origin: Point = Mock(
            latitude="-28.4412408", longitude="-48.9505159", spec=Point
        )

        destiny: Point = Mock(
            latitude="-28.4412408", longitude="-48.9505159", spec=Point
        )

        self.__mock_response.json.return_value = {
            "rows": [
                {
                    "elements": [
                        {
                            "distance": {"text": "33.3 km", "value": 33253},
                            "duration": {"text": "27 mins", "value": 1620},
                            "duration_in_traffic": {"text": "34 mins", "value": 2019},
                            "status": "OK",
                        }
                        for _ in range(total_elements)
                    ]
                }
                for _ in range(total_rows)
            ]
        }

        self.__mock_response.status_code = 200

        mock_async_client_class.return_value = self.__mock_async_client_instance

        geolocation_service: GeoLocationService = GeoLocationService()

        distances: Sequence[
            Sequence[DictType]
        ] = await geolocation_service.calculate_distance(
            origin, destiny, transport_mode=TransportModelType.WALKING
        )

        logging.info(f"Located Distances: {distances}")

        self.__mock_async_client_instance.get.assert_awaited_once()

        self.__mock_response.json.assert_called_once()

        self.__mock_response.raise_for_status.assert_called_once()

        self.assertTrue(len(distances) == total_rows)

        self.assertTrue(len(distances[0]) == total_elements)
