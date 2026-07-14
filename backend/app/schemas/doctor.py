from uuid import UUID

from pydantic import BaseModel


class DoctorRead(BaseModel):
    id: UUID
    user_id: UUID
    department_id: UUID | None = None
    specialty: str | None = None
