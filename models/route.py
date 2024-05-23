from typing import Set
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, ForeignKey
from uuid import uuid4

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME
from models.point import Point
from models.route_point import RoutePointTable
from models.company import Company


database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)


class Route(database.Base):
    __tablename__: str = "route"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    uuid: Mapped[str] = mapped_column(
        Uuid(as_uuid=False, native_uuid=True), default=uuid4
    )

    company_id: Mapped[int] = mapped_column(ForeignKey(f"{Company.__tablename__}.id"))

    description: Mapped[str]

    points: Mapped[Set[Point]] = relationship(
        secondary=RoutePointTable, back_populates="parents"
    )

    company: Mapped[Company] = relationship(back_populates="children")
