from typing import Awaitable, Optional, Protocol, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update, update, Delete, delete, Select, select, func
from sqlalchemy.orm import joinedload

from models import Company, Vehicle
from utils.patterns import (
    BaseRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
    IAuthRepository,
)
from utils.types import DictType, VehicleType


class IVehicleCreateRepository(Protocol):
    company: Company

    type: VehicleType

    plate: str


class IVehicleUpdateRepository(Protocol):
    uuid: str

    type: VehicleType

    plate: str

    instance: Optional[Vehicle]


class IVehicleDeleteRepository(Protocol):
    uuid: str

    instance: Optional[Vehicle]


class IVehicleFindRepository(Protocol):
    uuid: str


class IVehicleFindManyRepository(Protocol):
    company: Company


class VehicleRepository(
    BaseRepository[AsyncSession], IFindRepository[IVehicleFindRepository, Vehicle]
):
    async def find(self, props: IVehicleFindRepository) -> Optional[Vehicle]:
        query: Select = select(Vehicle).where(Vehicle.uuid == props.uuid)

        return await self.session.scalar(query)
