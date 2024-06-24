from typing import Set, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import time

from . import common


if TYPE_CHECKING:
    from models.company import Company
    from models.route_point import RoutePoint


class Route(common.BaseModel):
    __tablename__: str = "route"

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    description: Mapped[str]

    company: Mapped["Company"] = relationship(back_populates="routes")

    points: Mapped[Set["RoutePoint"]] = relationship(back_populates="route")

    opening_time: Mapped[time] = mapped_column(nullable=False)

    closing_time: Mapped[time] = mapped_column(nullable=False)

    ticket_price: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            "<Route "
            + f"id='{self.id}' "
            + f"uuid='{self.uuid}' "
            + f"company_id='{self.company_id}' "
            + f"description='{self.description}' "
            + "/>"
        )
