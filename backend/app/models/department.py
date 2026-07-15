from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.doctor import Doctor
    from app.models.hospital import Hospital


class Department(IdMixin, TimestampMixin, Base):
    __tablename__ = "departments"
    __table_args__ = (UniqueConstraint("hospital_id", "name", name="uq_department_hospital_name"),)

    hospital_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("hospitals.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    hospital: Mapped[Hospital] = relationship(back_populates="departments")
    doctors: Mapped[list[Doctor]] = relationship(back_populates="department")
    appointments: Mapped[list[Appointment]] = relationship(back_populates="department")
