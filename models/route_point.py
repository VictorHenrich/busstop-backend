from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME


database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)

RoutePointTable: Table = Table(
    "route_point",
    database.Base.metadata,
    Column("route_id", ForeignKey("route.id"), primary_key=True, nullable=False),
    Column("point_id", ForeignKey("point.id"), primary_key=True, nullable=False),
)
