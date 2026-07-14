from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class AppointmentRead(BaseModel):
    id: UUID
    patient_name: str
    patient_email: EmailStr | None = None
    scheduled_at: datetime
    status: str
    doctor_id: UUID | None = None
    department_id: UUID | None = None
