from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid
from uuid import uuid4

from server.instances import ServerInstances
from server.database import Database
from utils.constants import DATABASE_INSTANCE_NAME
import models.routes as routes

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

    routes: Mapped["routes.Route"] = relationship(back_populates="company")

    points: Mapped["routes.Point"] = relationship(back_populates="company")

    def __repr__(self) -> str:
        return (
            "<Company "
            + f"id='{self.id}' "
            + f"uuid='{self.uuid}' "
            + f"company_name='{self.company_name}' "
            + f"fantasy_name='{self.fantasy_name}' "
            + f"document_cnpj='{self.document_cnpj}' "
            + f"email='{self.email}' "
            + "/>"
        )
