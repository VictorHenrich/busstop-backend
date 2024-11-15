from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

from server.instances import ServerInstances
from server.database import ServerDatabase
from utils.config import DATABASE_CURRENT_NAME

database: ServerDatabase = ServerInstances.databases.select(DATABASE_CURRENT_NAME)


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

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            + f"id='{self.id}' "
            + f"uuid='{self.uuid}' "
            + f"name='{self.name}' "
            + f"email='{self.email}' "
            + "/>"
        )
