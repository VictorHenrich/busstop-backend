from typing import Sequence, Optional
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
from utils.types import TransportModelType, DictType


class GeoLocationService:
    def __get_location_data(
        self, address_type: str, address_components: Sequence[DictType]
    ) -> str:
        for address in address_components:
            if address_type in address["types"]:
                return address["short_name"]

        return ""

    def __handle_location(self, location: DictType) -> Point:
        point: Point = Point()

        geometry: DictType = location["geometry"]["location"]

        address_components: Sequence[DictType] = location["address_components"]

        point.address_zip_code = self.__get_location_data(
            TYPE_ADDRESS_ZIP_CODE, address_components
        )

        point.address_state = self.__get_location_data(
            TYPE_ADDRESS_STATE, address_components
        )

        point.address_city = self.__get_location_data(
            TYPE_ADDRESS_CITY, address_components
        )

        point.address_neighborhood = self.__get_location_data(
            TYPE_ADDRESS_NEIGHBORHOOD, address_components
        )

        point.address_street = self.__get_location_data(
            TYPE_ADDRESS_STREET, address_components
        )

        point.address_number = self.__get_location_data(
            TYPE_ADDRESS_NUMBER, address_components
        )

        point.latitude = str(geometry["lat"])

        point.longitude = str(geometry["lng"])

        return point

    def __get_distance_data(self, element: DictType) -> DictType:
        distance_data: DictType = element["distance"]

        duration_data: DictType = element["duration"]

        duration_in_traffic_data: DictType = element["duration_in_traffic"]

        return {
            "distance": {
                "description": distance_data["text"],
                "value": distance_data["value"],
            },
            "duration": {
                "description": duration_data["text"],
                "value": duration_data["value"],
            },
            "duration_in_traffic": {
                "description": duration_in_traffic_data["text"],
                "value": duration_in_traffic_data["value"],
            },
        }

    def __handle_distance(self, elements: Sequence[DictType]) -> Sequence[DictType]:
        return [self.__get_distance_data(element) for element in elements]

    async def find_address(
        self, address_description: str, region: str = "BR"
    ) -> Sequence[Point]:
        url: str = f"{GOOGLE_API_URL}/geocode/json"

        params: DictType = {
            "key": GOOGLE_API_KEY,
            "address": address_description,
            "region": region,
        }

        async with AsyncClient() as client:
            response: Response = await client.get(url, params=params)

            response.raise_for_status()

            data: DictType = response.json()

            logging.info(f"Address Data Response: {data}")

            locations: Optional[Sequence[DictType]] = data.get("results")

            if not locations:
                return []

            return [self.__handle_location(location) for location in locations]

    async def calculate_distance(
        self,
        origin: Point,
        destiny: Point,
        transport_mode: TransportModelType = TransportModelType.DRIVING,
    ) -> Sequence[Sequence[DictType]]:
        url: str = f"{GOOGLE_API_URL}/distancematrix/json"

        params: DictType = {
            "key": GOOGLE_API_KEY,
            "origins": f"{origin.latitude}-{origin.longitude}",
            "destinations": f"{destiny.latitude}-{destiny.longitude}",
            "mode": transport_mode.value,
        }

        async with AsyncClient() as client:
            response: Response = await client.get(url, params=params)

            response.raise_for_status()

            data: DictType = response.json()

            logging.info(f"Distance Matrix Data Response: {data}")

            distances: Sequence[DictType] = data["rows"]

            return [
                self.__handle_distance(distance["elements"]) for distance in distances
            ]
