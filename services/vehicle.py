from typing import Optional
from pydantic import BaseModel

from models import Vehicle, database
from repositories.vehicle import VehicleRepository, IVehicleFindRepository
from utils.patterns import IFindRepository
from utils.exceptions import ModelNotFound


class VehicleFindProps(BaseModel):
    uuid: str


class VehicleService:
    async def find_vehicle(self, vehicle_uuid: str) -> Vehicle:
        async with database.create_async_session() as session:
            vehicle_repository: IFindRepository[IVehicleFindRepository, Vehicle] = (
                VehicleRepository(session)
            )

            vehicle_props: IVehicleFindRepository = VehicleFindProps(uuid=vehicle_uuid)

            vehicle: Optional[Vehicle] = await vehicle_repository.find(vehicle_props)

            if vehicle is None:
                raise ModelNotFound(Vehicle, vehicle_uuid)

            return vehicle
