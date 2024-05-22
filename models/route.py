from typing import Set
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid
from uuid import uuid4

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME
from models.point import Point
from models.route_point import RoutePointTable


database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)


class Route(database.Base):
    __tablename__ = "route"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    uuid: Mapped[str] = mapped_column(
        Uuid(as_uuid=False, native_uuid=True), default=uuid4
    )

    description: Mapped[str]

    points: Mapped[Set[Point]] = relationship(secondary=RoutePointTable)
