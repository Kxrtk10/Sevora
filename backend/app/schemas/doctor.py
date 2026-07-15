from datetime import datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DoctorBase(BaseModel):
    hospital_id: UUID
    department_id: UUID
    full_name: str = Field(min_length=1, max_length=200)
    specialization: str = Field(min_length=1, max_length=160)
    qualification: str = Field(min_length=1, max_length=200)
    years_of_experience: int = Field(ge=0, le=80)
    biography: str | None = Field(default=None, max_length=5000)
    consultation_duration_minutes: int = Field(ge=5, le=240)
    consultation_fee: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    is_active: bool = True

    @field_validator("full_name", "specialization", "qualification")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank.")
        return cleaned


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    hospital_id: UUID | None = None
    department_id: UUID | None = None
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    specialization: str | None = Field(default=None, min_length=1, max_length=160)
    qualification: str | None = Field(default=None, min_length=1, max_length=200)
    years_of_experience: int | None = Field(default=None, ge=0, le=80)
    biography: str | None = Field(default=None, max_length=5000)
    consultation_duration_minutes: int | None = Field(default=None, ge=5, le=240)
    consultation_fee: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    is_active: bool | None = None

    @field_validator("full_name", "specialization", "qualification")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank.")
        return cleaned


class DoctorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    hospital_id: UUID
    department_id: UUID
    full_name: str
    specialization: str
    qualification: str
    years_of_experience: int
    biography: str | None = None
    consultation_duration_minutes: int
    consultation_fee: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime


class DoctorScheduleBase(BaseModel):
    doctor_id: UUID
    weekday: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    slot_duration: int = Field(ge=5, le=240)
    maximum_patients: int = Field(ge=1, le=500)
    is_available: bool = True


class DoctorScheduleCreate(DoctorScheduleBase):
    pass


class DoctorScheduleUpdate(BaseModel):
    doctor_id: UUID | None = None
    weekday: int | None = Field(default=None, ge=0, le=6)
    start_time: time | None = None
    end_time: time | None = None
    slot_duration: int | None = Field(default=None, ge=5, le=240)
    maximum_patients: int | None = Field(default=None, ge=1, le=500)
    is_available: bool | None = None


class DoctorScheduleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    doctor_id: UUID
    weekday: int
    start_time: time
    end_time: time
    slot_duration: int
    maximum_patients: int
    is_available: bool
    created_at: datetime
    updated_at: datetime
