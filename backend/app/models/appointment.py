from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.doctor import Doctor


class Appointment(IdMixin, TimestampMixin, Base):
    __tablename__ = "appointments"

    patient_name: Mapped[str] = mapped_column(String(200), nullable=False)
    patient_email: Mapped[str | None] = mapped_column(String(320))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    doctor_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("doctors.id"))
    department_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("departments.id"))

    doctor: Mapped[Doctor | None] = relationship(back_populates="appointments")
    department: Mapped[Department | None] = relationship(back_populates="appointments")
