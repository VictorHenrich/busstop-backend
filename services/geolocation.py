from typing import Any, Mapping, Sequence, Optional
from httpx import AsyncClient, Response
import logging

from models import Point
from utils.constants import (
    GOOGLE_API_URL,
    GOOGLE_API_KEY,
    TYPE_ADDRESS_NUMBER,
    TYPE_ADDRESS_CITY,
    TYPE_ADDRESS_NEIGHBORHOOD,
    TYPE_ADDRESS_STATE,
    TYPE_ADDRESS_STREET,
    TYPE_ADDRESS_ZIP_CODE,
)
from utils.types import TransportModelType


class GeoLocationService:
    def __get_address_data(
        self, address_type: str, address_components: Sequence[Mapping[str, Any]]
    ) -> str:
        for address in address_components:
            if address_type in address["types"]:
                return address["short_name"]

        return ""

    def __handle_location(self, location: Mapping[str, Any]) -> Point:
        point: Point = Point()

        geometry: Mapping[str, Any] = location["geometry"]

        address_components: Sequence[Mapping[str, Any]] = location["address_components"]

        point.address_zip_code = self.__get_address_data(
            TYPE_ADDRESS_ZIP_CODE, address_components
        )

        point.address_state = self.__get_address_data(
            TYPE_ADDRESS_STATE, address_components
        )

        point.address_city = self.__get_address_data(
            TYPE_ADDRESS_CITY, address_components
        )

        point.address_neighborhood = self.__get_address_data(
            TYPE_ADDRESS_NEIGHBORHOOD, address_components
        )

        point.address_street = self.__get_address_data(
            TYPE_ADDRESS_STREET, address_components
        )

        point.address_number = self.__get_address_data(
            TYPE_ADDRESS_NUMBER, address_components
        )

        point.latitude = str(geometry["latitude"])

        point.longitude = str(geometry["longitude"])

        return point

    async def find_address(
        self, address_description: str, region: str = "BR"
    ) -> Sequence[Point]:
        url: str = f"{GOOGLE_API_URL}/api/geocode/json"

        params: Mapping[str, Any] = {
            "key": GOOGLE_API_KEY,
            "address": address_description,
            "region": region,
        }

        async with AsyncClient() as client:
            response: Response = await client.get(url, params=params)

            response.raise_for_status()

            data: Mapping[str, Any] = response.json()

            locations: Optional[Sequence[Mapping[str, Any]]] = data.get("results")

            logging.info(f"Address Data Response: {data}")

            if not locations:
                return []

            return [self.__handle_location(location) for location in locations]

    async def calculate_distance(
        self,
        origin: Point,
        destiny: Point,
        transport_mode: TransportModelType = TransportModelType.DRIVING,
    ) -> None:
        url: str = f"{GOOGLE_API_URL}/distancematrix/json"

        params: Mapping[str, Any] = {
            "key": GOOGLE_API_KEY,
            "origins": f"{origin.latitude}-{origin.longitude}",
            "destinations": f"{destiny.latitude}-{destiny.longitude}",
            "mode": transport_mode.value,
        }

        async with AsyncClient() as client:
            response: Response = await client.get(url, params=params)

            response.raise_for_status()

            data: Mapping[str, Any] = response.json()

            logging.info(f"Distance Matrix Data Response: {data}")
