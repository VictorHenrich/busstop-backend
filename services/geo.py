from typing import Any, Mapping, Sequence
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import GoogleV3
from geopy import Location

from models import Point
from utils.constants import (
    GOOGLE_API_KEY,
    TYPE_ADDRESS_NUMBER,
    TYPE_ADDRESS_CITY,
    TYPE_ADDRESS_NEIGHBORHOOD,
    TYPE_ADDRESS_STATE,
    TYPE_ADDRESS_STREET,
    TYPE_ADDRESS_ZIP_CODE,
)


class GeoService:
    def __init__(self) -> None:
        self.__geocoder: GoogleV3 = GoogleV3(
            api_key=GOOGLE_API_KEY, user_agent="busstop", adapter_factory=AioHTTPAdapter
        )

    def __get_address_data(
        self, address_type: str, location_raw: Mapping[str, Any]
    ) -> str:
        address_components: Sequence[Mapping[str, Any]] = location_raw["location_raw"]

        for address in address_components:
            if address_type in address["types"]:
                return address["short_name"]

        return ""

    def __handle_location(self, location: Location) -> Point:
        point: Point = Point()

        point.address_zip_code = self.__get_address_data(
            TYPE_ADDRESS_ZIP_CODE, location.raw
        )

        point.address_state = self.__get_address_data(TYPE_ADDRESS_STATE, location.raw)

        point.address_city = self.__get_address_data(TYPE_ADDRESS_CITY, location.raw)

        point.address_neighborhood = self.__get_address_data(
            TYPE_ADDRESS_NEIGHBORHOOD, location.raw
        )

        point.address_street = self.__get_address_data(
            TYPE_ADDRESS_STREET, location.raw
        )

        point.address_number = self.__get_address_data(
            TYPE_ADDRESS_NUMBER, location.raw
        )

        point.latitude = location.latitude

        point.longitude = location.longitude

        return point

    async def find_address(
        self, address_description: str, region: str = "BR"
    ) -> Sequence[Point]:
        async with self.__geocoder as geocoder:
            locations = await geocoder.geocode(
                query=address_description, region=region, exactly_one=False
            )

            return [self.__handle_location(location) for location in locations]
