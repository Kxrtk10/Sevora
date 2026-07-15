from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_appointment_service
from app.models.appointment import AppointmentStatus
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentStatusUpdate,
    AppointmentUpdate,
)
from app.services.appointments import (
    AppointmentNotFoundError,
    AppointmentService,
    DepartmentNotFoundError,
    DoctorNotFoundError,
    DoubleBookingError,
    InactiveDoctorError,
    InvalidAppointmentScheduleError,
    InvalidStatusTransitionError,
)

router = APIRouter()


@router.post(
    "",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(
    payload: AppointmentCreate,
    appointment_service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> AppointmentRead:
    try:
        appointment = await appointment_service.create_appointment(payload)
    except (DoctorNotFoundError, DepartmentNotFoundError) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor or department was not found.",
        ) from exc
    except InactiveDoctorError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointments cannot be booked with inactive doctors.",
        ) from exc
    except InvalidAppointmentScheduleError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Appointment time must be in the future, within doctor working hours, "
                "and last between 15 and 240 minutes."
            ),
        ) from exc
    except DoubleBookingError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The doctor already has an appointment during this time slot.",
        ) from exc

    return AppointmentRead.model_validate(appointment)


@router.get("", response_model=list[AppointmentRead])
async def list_appointments(
    appointment_service: Annotated[AppointmentService, Depends(get_appointment_service)],
    doctor_id: UUID | None = None,
    department_id: UUID | None = None,
    appointment_date: date | None = None,
    status_filter: Annotated[AppointmentStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[AppointmentRead]:
    appointments = await appointment_service.list_appointments(
        doctor_id=doctor_id,
        department_id=department_id,
        appointment_date=appointment_date,
        status=status_filter,
        limit=limit,
        offset=offset,
    )
    return [AppointmentRead.model_validate(appointment) for appointment in appointments]


@router.get("/{appointment_id}", response_model=AppointmentRead)
async def get_appointment(
    appointment_id: UUID,
    appointment_service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> AppointmentRead:
    try:
        appointment = await appointment_service.get_appointment(appointment_id)
    except AppointmentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment was not found.",
        ) from exc
    return AppointmentRead.model_validate(appointment)


@router.put("/{appointment_id}", response_model=AppointmentRead)
async def update_appointment(
    appointment_id: UUID,
    payload: AppointmentUpdate,
    appointment_service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> AppointmentRead:
    try:
        appointment = await appointment_service.update_appointment(appointment_id, payload)
    except AppointmentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment was not found.",
        ) from exc
    except (DoctorNotFoundError, DepartmentNotFoundError) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor or department was not found.",
        ) from exc
    except InactiveDoctorError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointments cannot be booked with inactive doctors.",
        ) from exc
    except InvalidAppointmentScheduleError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Appointment time must be in the future, within doctor working hours, "
                "and last between 15 and 240 minutes."
            ),
        ) from exc
    except DoubleBookingError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The doctor already has an appointment during this time slot.",
        ) from exc
    except InvalidStatusTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cancelled or completed appointments cannot be updated.",
        ) from exc

    return AppointmentRead.model_validate(appointment)


@router.delete("/{appointment_id}", response_model=AppointmentRead)
async def cancel_appointment(
    appointment_id: UUID,
    appointment_service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> AppointmentRead:
    try:
        appointment = await appointment_service.cancel_appointment(appointment_id)
    except AppointmentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment was not found.",
        ) from exc
    except InvalidStatusTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Appointment status cannot transition to cancelled.",
        ) from exc

    return AppointmentRead.model_validate(appointment)


@router.patch("/{appointment_id}/status", response_model=AppointmentRead)
async def update_appointment_status(
    appointment_id: UUID,
    payload: AppointmentStatusUpdate,
    appointment_service: Annotated[AppointmentService, Depends(get_appointment_service)],
) -> AppointmentRead:
    try:
        appointment = await appointment_service.update_appointment_status(
            appointment_id,
            payload.status,
        )
    except AppointmentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment was not found.",
        ) from exc
    except InvalidStatusTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Appointment status transition is not allowed.",
        ) from exc

    return AppointmentRead.model_validate(appointment)
