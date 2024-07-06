from typing import Any, Mapping, TypeAlias, TypeVar
from enum import Enum


DPT = TypeVar("DPT", bound=str)
DVT = TypeVar("DVT", bound=Any)


class TransportModelType(Enum):
    DRIVING = "driving"
    WALKING = "walking"
    BICYCLING = "bicycling"
    TRANSIT = "transit"


DictType: TypeAlias = Mapping[DPT, DVT]
