from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class AIConciergeRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    action: str | None = Field(default=None, max_length=80)
    appointment_id: UUID | None = None
    department_id: UUID | None = None
    doctor_id: UUID | None = None
    patient_name: str | None = Field(default=None, max_length=200)
    patient_email: EmailStr | None = None
    patient_phone: str | None = Field(default=None, max_length=40)
    reason_for_visit: str | None = Field(default=None, max_length=500)
    appointment_date: date | None = None
    appointment_start_time: time | None = None
    appointment_end_time: time | None = None


class ConciergeDepartment(BaseModel):
    id: UUID
    name: str
    description: str | None = None


class ConciergeDoctor(BaseModel):
    id: UUID
    department_id: UUID
    full_name: str
    specialization: str
    qualification: str
    years_of_experience: int
    consultation_duration_minutes: int
    consultation_fee: str


class ConciergeSlot(BaseModel):
    doctor_id: UUID
    appointment_date: date
    start_time: time
    end_time: time
    label: str


class ConciergeAppointment(BaseModel):
    id: UUID
    patient_name: str
    doctor_id: UUID
    department_id: UUID
    appointment_date: date
    appointment_start_time: time
    appointment_end_time: time
    status: str


class ConciergeAction(BaseModel):
    label: str
    action: str
    payload: dict[str, str] = Field(default_factory=dict)


class AIConciergeResponse(BaseModel):
    intent: str
    message: str
    departments: list[ConciergeDepartment] = Field(default_factory=list)
    doctors: list[ConciergeDoctor] = Field(default_factory=list)
    slots: list[ConciergeSlot] = Field(default_factory=list)
    appointment: ConciergeAppointment | None = None
    actions: list[ConciergeAction] = Field(default_factory=list)
    safety_notice: str | None = None
    requires_input: list[str] = Field(default_factory=list)
