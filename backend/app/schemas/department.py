from uuid import UUID

from pydantic import BaseModel


class DepartmentRead(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    status: str
