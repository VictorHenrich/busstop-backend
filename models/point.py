from typing import Set
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid, String
from uuid import uuid4

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME
from models.route import Route
from models.route_point import RoutePointTable


database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)


class Point(database.Base):
    __tablename__: str = "point"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    uuid: Mapped[str] = mapped_column(
        Uuid(as_uuid=False, native_uuid=True), default=uuid4
    )

    address_state: Mapped[str] = mapped_column(String(2), nullable=False)

    address_city: Mapped[str] = mapped_column(nullable=False)

    address_neighborhood: Mapped[str] = mapped_column(nullable=False)

    address_street: Mapped[str] = mapped_column(nullable=False)

    address_number: Mapped[str] = mapped_column(nullable=False)

    latitude: Mapped[str] = mapped_column(nullable=False)

    longitude: Mapped[str] = mapped_column(nullable=False)

    routers: Mapped[Set[Route]] = mapped_column(
        secondary=RoutePointTable, back_populates="children"
    )
