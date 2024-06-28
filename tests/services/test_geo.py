from typing import Sequence
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch


from services.geolocation import GeoLocationService
from models import Point


class GeolocationServiceTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__mock_geocoder_instance: AsyncMock = AsyncMock()

        self.__mock_geocoder_instance.__aenter__.return_value = (
            self.__mock_geocoder_instance
        )

    @patch("services.geolocation.GoogleV3")
    async def test_find_address(self, mock_google_v3_class: Mock) -> None:
        amount_register: int = 10

        result: Sequence[Point] = [
            Point(
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

        self.__mock_geocoder_instance.geocode.return_value = [
            Mock(
                latitude="-28.4412408",
                longitude="-48.9505159",
                raw={
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
                    ]
                },
            )
            for _ in range(amount_register)
        ]

        mock_google_v3_class.return_value = self.__mock_geocoder_instance

        geolocation_service: GeoLocationService = GeoLocationService()

        locations: Sequence[Point] = await geolocation_service.find_address("Teste")

        location1: Point = result[0]

        location2: Point = locations[0]

        mock_google_v3_class.assert_called_once()

        self.__mock_geocoder_instance.__aenter__.assert_called_once()

        self.__mock_geocoder_instance.geocode.assert_awaited_once()

        self.assertEqual(len(locations), len(result))
        self.assertEqual(location1.latitude, location2.latitude)
        self.assertEqual(location1.longitude, location2.longitude)
        self.assertEqual(location1.address_state, location2.address_state)
        self.assertEqual(location1.address_zip_code, location2.address_zip_code)
        self.assertEqual(location1.address_city, location2.address_city)
        self.assertEqual(location1.address_neighborhood, location2.address_neighborhood)
        self.assertEqual(location1.address_street, location2.address_street)
        self.assertEqual(location1.address_number, location2.address_number)

    @patch("services.geolocation.GoogleV3")
    async def test_find_address_with_empty_result(
        self, mock_google_v3_class: Mock
    ) -> None:
        result: Sequence[Point] = []

        self.__mock_geocoder_instance.geocode.return_value = None

        mock_google_v3_class.return_value = self.__mock_geocoder_instance

        geolocation_service: GeoLocationService = GeoLocationService()

        locations: Sequence[Point] = await geolocation_service.find_address("Teste")

        mock_google_v3_class.assert_called_once()

        self.__mock_geocoder_instance.__aenter__.assert_called_once()

        self.__mock_geocoder_instance.geocode.assert_awaited_once()

        self.assertSequenceEqual(result, locations)

    @patch("services.geolocation.GoogleV3")
    async def test_find_address_with_error(self, mock_google_v3_class: Mock) -> None:
        self.__mock_geocoder_instance.geocode.return_value = [
            Mock(
                latitude="-28.4412408",
                longitude="-48.9505159",
                raw={
                    "address_informations": [
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
                    ]
                },
            )
        ]

        mock_google_v3_class.return_value = self.__mock_geocoder_instance

        geolocation_service: GeoLocationService = GeoLocationService()

        with self.assertRaises(KeyError):
            await geolocation_service.find_address("Teste")

        mock_google_v3_class.assert_called_once()

        self.__mock_geocoder_instance.__aenter__.assert_called_once()

        self.__mock_geocoder_instance.geocode.assert_awaited_once()
