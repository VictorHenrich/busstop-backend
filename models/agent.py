from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import common

if TYPE_CHECKING:
    from models.company import Company


class Agent(common.UserBaseModel):
    __tablename__ = "agent"

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    company: Mapped["Company"] = relationship(back_populates="agents")
