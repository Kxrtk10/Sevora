from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    patient_name: str = Field(min_length=1, max_length=200)
    patient_email: EmailStr
    patient_phone: str = Field(min_length=7, max_length=40)
    reason_for_visit: str = Field(min_length=1, max_length=500)
    doctor_id: UUID
    department_id: UUID
    appointment_date: date
    appointment_start_time: time
    appointment_end_time: time
    notes: str | None = Field(default=None, max_length=5000)

    @field_validator("patient_name", "patient_phone", "reason_for_visit")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank.")
        return cleaned


class AppointmentCreate(AppointmentBase):
    status: AppointmentStatus = AppointmentStatus.PENDING


class AppointmentUpdate(BaseModel):
    patient_name: str | None = Field(default=None, min_length=1, max_length=200)
    patient_email: EmailStr | None = None
    patient_phone: str | None = Field(default=None, min_length=7, max_length=40)
    reason_for_visit: str | None = Field(default=None, min_length=1, max_length=500)
    doctor_id: UUID | None = None
    department_id: UUID | None = None
    appointment_date: date | None = None
    appointment_start_time: time | None = None
    appointment_end_time: time | None = None
    notes: str | None = Field(default=None, max_length=5000)

    @field_validator("patient_name", "patient_phone", "reason_for_visit")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank.")
        return cleaned


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AppointmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    patient_name: str
    patient_email: EmailStr
    patient_phone: str
    reason_for_visit: str
    doctor_id: UUID
    department_id: UUID
    appointment_date: date
    appointment_start_time: time
    appointment_end_time: time
    status: AppointmentStatus
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
