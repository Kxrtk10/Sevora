from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.department import Department
    from app.models.doctor_schedule import DoctorSchedule
    from app.models.hospital import Hospital
    from app.models.user import User


class Doctor(IdMixin, TimestampMixin, Base):
    __tablename__ = "doctors"

    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), unique=True)
    hospital_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("hospitals.id"), nullable=False)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    specialization: Mapped[str] = mapped_column(String(160), nullable=False)
    qualification: Mapped[str] = mapped_column(String(200), nullable=False)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    biography: Mapped[str | None] = mapped_column(Text())
    consultation_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    consultation_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped[User | None] = relationship(back_populates="doctor_profile")
    hospital: Mapped[Hospital] = relationship(back_populates="doctors")
    department: Mapped[Department] = relationship(back_populates="doctors")
    schedules: Mapped[list[DoctorSchedule]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan",
    )
    appointments: Mapped[list[Appointment]] = relationship(back_populates="doctor")
