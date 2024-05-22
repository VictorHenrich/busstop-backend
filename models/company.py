from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid
from uuid import uuid4

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME


database: Database = ServerInstances.databases.select(DATABASE_INSTANCE_NAME)


class Company(database.Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)

    uuid: Mapped[str] = mapped_column(
        Uuid(as_uuid=False, native_uuid=True), default=uuid4
    )

    company_name: Mapped[str] = mapped_column(nullable=False)

    fantasy_name: Mapped[str] = mapped_column(nullable=False)

    document_cnpj: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[str]
