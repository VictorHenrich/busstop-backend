from typing import Any, Mapping, TypeAlias, TypeVar, Union
from enum import Enum


DPT = TypeVar("DPT", bound=str)
DVT = TypeVar("DVT")


class TransportModelType(Enum):
    DRIVING = "driving"
    WALKING = "walking"
    BICYCLING = "bicycling"
    TRANSIT = "transit"


DictType: TypeAlias = Mapping[Union[DPT, str], Union[DVT, Any]]
