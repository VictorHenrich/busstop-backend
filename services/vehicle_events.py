from typing import Sequence, Union
from fastapi import WebSocket
import asyncio

from server.instances import ServerInstances
from models import Vehicle
from services.vehicle import VehicleService
from utils.types import DictType
from utils.config import VEHICLE_ENDPOINT_NAME


class VehicleEventsService:
    def __init__(self) -> None:
        self.__vehicle_service: VehicleService = VehicleService()

    async def process_vehicle_position(
        self,
        vehicle_uuid: str,
        latitude: Union[str, float],
        longitude: Union[str, float],
    ) -> None:
        vehicle: Vehicle = await self.__vehicle_service.find_vehicle(vehicle_uuid)

        data: DictType = {
            "vehicle_uuid": vehicle.uuid,
            "latitude": latitude,
            "longitude": longitude,
        }

        url: str = f"{VEHICLE_ENDPOINT_NAME}/{vehicle_uuid}/location"

        connections: Sequence[WebSocket] = (
            ServerInstances.general_api.find_websocket_connections_by_url(url)
        )

        await asyncio.gather(
            *[connection.send_json(data) for connection in connections]
        )
