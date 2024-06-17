from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import common

if TYPE_CHECKING:
    from models.route import Route
    from models.point import Point


class RoutePoint(common.BaseModel):
    __tablename__: str = "route_point"

    route_id: Mapped[int] = mapped_column(ForeignKey("route.id"))

    point_id: Mapped[int] = mapped_column(ForeignKey("point.id"))

    route: Mapped["Route"] = relationship()

    point: Mapped["Point"] = relationship()

    index: Mapped[int] = mapped_column(nullable=False)
