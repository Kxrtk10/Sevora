from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.doctor import Doctor


class Hospital(IdMixin, TimestampMixin, Base):
    __tablename__ = "hospitals"

    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[str] = mapped_column(String(120), nullable=False)
    country: Mapped[str] = mapped_column(String(120), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    website: Mapped[str | None] = mapped_column(String(500))
    timezone: Mapped[str] = mapped_column(String(80), default="Asia/Kolkata", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    departments: Mapped[list[Department]] = relationship(back_populates="hospital")
    doctors: Mapped[list[Doctor]] = relationship(back_populates="hospital")
