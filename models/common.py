from sqlalchemy import ForeignKey, Column, Table, Integer

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
