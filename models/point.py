from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from . import common

if TYPE_CHECKING:
    from models.company import Company
    from models.route_point import RoutePoint


class Point(common.BaseModel):
    __tablename__: str = "point"

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    address_zip_code: Mapped[str] = mapped_column(nullable=False)

    address_state: Mapped[str] = mapped_column(String(2), nullable=False)

    address_city: Mapped[str] = mapped_column(nullable=False)

    address_neighborhood: Mapped[str] = mapped_column(nullable=False)

    address_street: Mapped[str] = mapped_column(nullable=False)

    address_number: Mapped[str] = mapped_column(nullable=False)

    latitude: Mapped[str] = mapped_column(nullable=False)

    longitude: Mapped[str] = mapped_column(nullable=False)

    company: Mapped["Company"] = relationship(back_populates="points")

    routes: Mapped[List["RoutePoint"]] = relationship(back_populates="point")

    def __repr__(self) -> str:
        return (
            "<Point "
            + f"id='{self.id}' "
            + f"uuid='{self.uuid}' "
            + f"company_id='{self.company_id}' "
            + f"address_state='{self.address_state}' "
            + f"address_city='{self.address_city}' "
            + f"address_neighborhood='{self.address_neighborhood}' "
            + f"address_street='{self.address_street}' "
            + f"address_number='{self.address_number}' "
            + f"latitude='{self.latitude}' "
            + f"longitude='{self.latitude}' "
            + "/>"
        )
