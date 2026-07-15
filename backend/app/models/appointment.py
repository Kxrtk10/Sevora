from __future__ import annotations

import uuid
from datetime import date, time
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.doctor import Doctor


class AppointmentStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class Appointment(IdMixin, TimestampMixin, Base):
    __tablename__ = "appointments"

    patient_name: Mapped[str] = mapped_column(String(200), nullable=False)
    patient_email: Mapped[str] = mapped_column(String(320), nullable=False)
    patient_phone: Mapped[str] = mapped_column(String(40), nullable=False)
    reason_for_visit: Mapped[str] = mapped_column(String(500), nullable=False)
    doctor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"), nullable=False)
    appointment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    appointment_start_time: Mapped[time] = mapped_column(Time(), nullable=False)
    appointment_end_time: Mapped[time] = mapped_column(Time(), nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        String(50),
        default=AppointmentStatus.PENDING,
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text())

    doctor: Mapped[Doctor] = relationship(back_populates="appointments")
    department: Mapped[Department] = relationship(back_populates="appointments")
