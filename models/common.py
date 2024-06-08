from sqlalchemy import ForeignKey, Column, Table, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME

database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)


RoutePointRelationship: Table = Table(
    "route_point",
    database.Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("route_id", ForeignKey("route.id"), nullable=False),
    Column("point_id", ForeignKey("point.id"), nullable=False),
)


class BaseModel(database.Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    uuid: Mapped[str] = mapped_column(
        Uuid(as_uuid=False, native_uuid=True), default=uuid4
    )
