from __future__ import annotations

import uuid
from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.doctor import Doctor


class DoctorSchedule(IdMixin, TimestampMixin, Base):
    __tablename__ = "doctor_schedules"
    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "weekday",
            "start_time",
            "end_time",
            name="uq_doctor_schedule_window",
        ),
    )

    doctor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    weekday: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time(), nullable=False)
    end_time: Mapped[time] = mapped_column(Time(), nullable=False)
    slot_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_patients: Mapped[int] = mapped_column(Integer, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    doctor: Mapped[Doctor] = relationship(back_populates="schedules")
