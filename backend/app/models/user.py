from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.doctor import Doctor


class UserRole(StrEnum):
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"
    DOCTOR = "doctor"
    PATIENT = "patient"


class User(IdMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[UserRole] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="invited", nullable=False)

    doctor_profile: Mapped[Doctor | None] = relationship(back_populates="user")
