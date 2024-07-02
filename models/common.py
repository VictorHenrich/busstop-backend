from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME

database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)


class BaseModel(database.Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    uuid: Mapped[str] = mapped_column(
        Uuid(as_uuid=False, native_uuid=True), default=uuid4
    )


class UserBaseModel(BaseModel):
    __abstract__ = True

    name: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    password: Mapped[str] = mapped_column(nullable=False)
