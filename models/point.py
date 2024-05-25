from typing import Set, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, ForeignKey, String
from uuid import uuid4

from . import common

if TYPE_CHECKING:
    from models.company import Company
    from models.route import Route


class Point(common.database.Base):
    __tablename__: str = "point"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    uuid: Mapped[str] = mapped_column(
        Uuid(as_uuid=False, native_uuid=True), default=uuid4
    )

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    address_state: Mapped[str] = mapped_column(String(2), nullable=False)

    address_city: Mapped[str] = mapped_column(nullable=False)

    address_neighborhood: Mapped[str] = mapped_column(nullable=False)

    address_street: Mapped[str] = mapped_column(nullable=False)

    address_number: Mapped[str] = mapped_column(nullable=False)

    latitude: Mapped[str] = mapped_column(nullable=False)

    longitude: Mapped[str] = mapped_column(nullable=False)

    company: Mapped["Company"] = relationship(back_populates="points")

    routes: Mapped[Set["Route"]] = relationship(
        secondary=common.RoutePointRelationship, back_populates="points"
    )

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
