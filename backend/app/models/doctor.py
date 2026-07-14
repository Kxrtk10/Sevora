from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.department import Department
    from app.models.user import User


class Doctor(IdMixin, TimestampMixin, Base):
    __tablename__ = "doctors"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    department_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("departments.id"))
    license_number: Mapped[str | None] = mapped_column(String(100))
    specialty: Mapped[str | None] = mapped_column(String(120))

    user: Mapped[User] = relationship(back_populates="doctor_profile")
    department: Mapped[Department | None] = relationship(back_populates="doctors")
    appointments: Mapped[list[Appointment]] = relationship(back_populates="doctor")
