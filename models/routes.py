from typing import Set
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, ForeignKey, Column, Table, String
from uuid import uuid4

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME


database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

RoutePointRelationship: Table = Table(
    "route_point",
    database.Base.metadata,
    Column("route_id", ForeignKey("route.id"), primary_key=True, nullable=False),
    Column("point_id", ForeignKey("point.id"), primary_key=True, nullable=False),
)


class Route(database.Base):
    __tablename__: str = "route"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    uuid: Mapped[str] = mapped_column(
        Uuid(as_uuid=False, native_uuid=True), default=uuid4
    )

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    description: Mapped[str]

    points: Mapped[Set["Point"]] = relationship(
        secondary=RoutePointRelationship, back_populates="routes"
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


class Point(database.Base):
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

    routes: Mapped[Set[Route]] = relationship(
        secondary=RoutePointRelationship, back_populates="points"
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
