from typing import Set, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import common


if TYPE_CHECKING:
    from models.company import Company
    from models.point import Point


class Route(common.BaseModel):
    __tablename__: str = "route"

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    description: Mapped[str]

    company: Mapped["Company"] = relationship(back_populates="routes")

    points: Mapped[Set["Point"]] = relationship(
        secondary=common.RoutePointRelationship, back_populates="routes"
    )

    def __repr__(self) -> str:
        return (
            "<Route "
            + f"id='{self.id}' "
            + f"uuid='{self.uuid}' "
            + f"company_id='{self.company_id}' "
            + f"description='{self.description}' "
            + "/>"
        )
