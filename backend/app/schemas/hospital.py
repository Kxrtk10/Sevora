from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, field_validator


class HospitalBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    address: str = Field(min_length=1, max_length=500)
    city: str = Field(min_length=1, max_length=120)
    state: str = Field(min_length=1, max_length=120)
    country: str = Field(min_length=1, max_length=120)
    postal_code: str = Field(min_length=1, max_length=30)
    phone: str = Field(min_length=7, max_length=40)
    email: EmailStr
    website: HttpUrl | None = None
    timezone: str = Field(default="Asia/Kolkata", min_length=1, max_length=80)
    is_active: bool = True

    @field_validator("name", "address", "city", "state", "country", "postal_code", "phone")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank.")
        return cleaned


class HospitalCreate(HospitalBase):
    pass


class HospitalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    address: str | None = Field(default=None, min_length=1, max_length=500)
    city: str | None = Field(default=None, min_length=1, max_length=120)
    state: str | None = Field(default=None, min_length=1, max_length=120)
    country: str | None = Field(default=None, min_length=1, max_length=120)
    postal_code: str | None = Field(default=None, min_length=1, max_length=30)
    phone: str | None = Field(default=None, min_length=7, max_length=40)
    email: EmailStr | None = None
    website: HttpUrl | None = None
    timezone: str | None = Field(default=None, min_length=1, max_length=80)
    is_active: bool | None = None

    @field_validator("name", "address", "city", "state", "country", "postal_code", "phone")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank.")
        return cleaned


class HospitalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    phone: str
    email: EmailStr
    website: str | None = None
    timezone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
