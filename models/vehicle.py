from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import common
from utils.types import VehicleType

if TYPE_CHECKING:
    from models.company import Company


class Vehicle(common.BaseModel):
    __tablename__ = "vehicle"

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))

    type: Mapped[str] = mapped_column(default=VehicleType.BUS, nullable=False)

    plate: Mapped[str] = mapped_column(nullable=False, unique=True)

    company: Mapped["Company"] = relationship(back_populates="vehicles")
