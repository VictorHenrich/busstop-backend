from typing import Any, Mapping, TypeAlias, TypeVar
from enum import Enum


DPT = TypeVar("DPT", bound=str)
DVT = TypeVar("DVT", bound=Any)


class TransportModelType(Enum):
    DRIVING = "driving"
    WALKING = "walking"
    BICYCLING = "bicycling"
    TRANSIT = "transit"


class VehicleType(Enum):
    BUS = "bus"
    CAR = "car"


class DatabaseDialectType(Enum):
    POSTGRESQL = "postgresql"

    MYSQL = "mysql"


DictType: TypeAlias = Mapping[DPT, DVT]
