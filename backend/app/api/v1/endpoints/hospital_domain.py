from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_hospital_domain_service
from app.schemas.department import DepartmentCreate, DepartmentRead, DepartmentUpdate
from app.schemas.doctor import (
    DoctorCreate,
    DoctorRead,
    DoctorScheduleCreate,
    DoctorScheduleRead,
    DoctorScheduleUpdate,
    DoctorUpdate,
)
from app.schemas.hospital import HospitalCreate, HospitalRead, HospitalUpdate
from app.services.hospital_domain import (
    DeleteBlockedError,
    DuplicateDepartmentError,
    HospitalDomainService,
    InactiveDoctorScheduleError,
    InvalidRelationshipError,
    InvalidScheduleError,
    NotFoundError,
    OverlappingScheduleError,
)

router = APIRouter()


@router.post("/hospitals", response_model=HospitalRead, status_code=status.HTTP_201_CREATED)
async def create_hospital(
    payload: HospitalCreate,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> HospitalRead:
    hospital = await service.create_hospital(payload)
    return HospitalRead.model_validate(hospital)


@router.get("/hospitals", response_model=list[HospitalRead])
async def list_hospitals(
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[HospitalRead]:
    hospitals = await service.list_hospitals(limit=limit, offset=offset)
    return [HospitalRead.model_validate(hospital) for hospital in hospitals]


@router.get("/hospitals/{hospital_id}", response_model=HospitalRead)
async def get_hospital(
    hospital_id: UUID,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> HospitalRead:
    try:
        hospital = await service.get_hospital(hospital_id)
    except NotFoundError as exc:
        raise _not_found("Hospital was not found.") from exc
    return HospitalRead.model_validate(hospital)


@router.put("/hospitals/{hospital_id}", response_model=HospitalRead)
async def update_hospital(
    hospital_id: UUID,
    payload: HospitalUpdate,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> HospitalRead:
    try:
        hospital = await service.update_hospital(hospital_id, payload)
    except NotFoundError as exc:
        raise _not_found("Hospital was not found.") from exc
    return HospitalRead.model_validate(hospital)


@router.delete("/hospitals/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hospital(
    hospital_id: UUID,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> None:
    try:
        await service.delete_hospital(hospital_id)
    except NotFoundError as exc:
        raise _not_found("Hospital was not found.") from exc
    except DeleteBlockedError as exc:
        raise _conflict("Hospitals with departments or doctors cannot be deleted.") from exc


@router.post("/departments", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(
    payload: DepartmentCreate,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DepartmentRead:
    try:
        department = await service.create_department(payload)
    except NotFoundError as exc:
        raise _not_found("Hospital was not found.") from exc
    except DuplicateDepartmentError as exc:
        raise _conflict("A department with this name already exists in this hospital.") from exc
    return DepartmentRead.model_validate(department)


@router.get("/departments", response_model=list[DepartmentRead])
async def list_departments(
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
    hospital_id: UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[DepartmentRead]:
    departments = await service.list_departments(
        hospital_id=hospital_id,
        limit=limit,
        offset=offset,
    )
    return [DepartmentRead.model_validate(department) for department in departments]


@router.get("/departments/{department_id}", response_model=DepartmentRead)
async def get_department(
    department_id: UUID,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DepartmentRead:
    try:
        department = await service.get_department(department_id)
    except NotFoundError as exc:
        raise _not_found("Department was not found.") from exc
    return DepartmentRead.model_validate(department)


@router.put("/departments/{department_id}", response_model=DepartmentRead)
async def update_department(
    department_id: UUID,
    payload: DepartmentUpdate,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DepartmentRead:
    try:
        department = await service.update_department(department_id, payload)
    except NotFoundError as exc:
        raise _not_found("Hospital or department was not found.") from exc
    except DuplicateDepartmentError as exc:
        raise _conflict("A department with this name already exists in this hospital.") from exc
    return DepartmentRead.model_validate(department)


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: UUID,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> None:
    try:
        await service.delete_department(department_id)
    except NotFoundError as exc:
        raise _not_found("Department was not found.") from exc
    except DeleteBlockedError as exc:
        raise _conflict("Departments with doctors cannot be deleted.") from exc


@router.post("/doctors", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    payload: DoctorCreate,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DoctorRead:
    try:
        doctor = await service.create_doctor(payload)
    except NotFoundError as exc:
        raise _not_found("Hospital or department was not found.") from exc
    except InvalidRelationshipError as exc:
        raise _bad_request("Department does not belong to the selected hospital.") from exc
    return DoctorRead.model_validate(doctor)


@router.get("/doctors", response_model=list[DoctorRead])
async def list_doctors(
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
    hospital_id: UUID | None = None,
    department_id: UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[DoctorRead]:
    doctors = await service.list_doctors(
        hospital_id=hospital_id,
        department_id=department_id,
        limit=limit,
        offset=offset,
    )
    return [DoctorRead.model_validate(doctor) for doctor in doctors]


@router.get("/doctors/{doctor_id}", response_model=DoctorRead)
async def get_doctor(
    doctor_id: UUID,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DoctorRead:
    try:
        doctor = await service.get_doctor(doctor_id)
    except NotFoundError as exc:
        raise _not_found("Doctor was not found.") from exc
    return DoctorRead.model_validate(doctor)


@router.put("/doctors/{doctor_id}", response_model=DoctorRead)
async def update_doctor(
    doctor_id: UUID,
    payload: DoctorUpdate,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DoctorRead:
    try:
        doctor = await service.update_doctor(doctor_id, payload)
    except NotFoundError as exc:
        raise _not_found("Hospital, department, or doctor was not found.") from exc
    except InvalidRelationshipError as exc:
        raise _bad_request("Department does not belong to the selected hospital.") from exc
    return DoctorRead.model_validate(doctor)


@router.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    doctor_id: UUID,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> None:
    try:
        await service.delete_doctor(doctor_id)
    except NotFoundError as exc:
        raise _not_found("Doctor was not found.") from exc


@router.post(
    "/doctor-schedules",
    response_model=DoctorScheduleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_doctor_schedule(
    payload: DoctorScheduleCreate,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DoctorScheduleRead:
    try:
        schedule = await service.create_schedule(payload)
    except NotFoundError as exc:
        raise _not_found("Doctor was not found.") from exc
    except InactiveDoctorScheduleError as exc:
        raise _bad_request("Schedules cannot be created for inactive doctors.") from exc
    except InvalidScheduleError as exc:
        raise _bad_request("Schedule hours or slot duration are invalid.") from exc
    except OverlappingScheduleError as exc:
        raise _conflict("Doctor schedule overlaps an existing schedule.") from exc
    return DoctorScheduleRead.model_validate(schedule)


@router.get("/doctor-schedules", response_model=list[DoctorScheduleRead])
async def list_doctor_schedules(
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
    doctor_id: UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[DoctorScheduleRead]:
    schedules = await service.list_schedules(doctor_id=doctor_id, limit=limit, offset=offset)
    return [DoctorScheduleRead.model_validate(schedule) for schedule in schedules]


@router.get("/doctor-schedules/{schedule_id}", response_model=DoctorScheduleRead)
async def get_doctor_schedule(
    schedule_id: UUID,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DoctorScheduleRead:
    try:
        schedule = await service.get_schedule(schedule_id)
    except NotFoundError as exc:
        raise _not_found("Doctor schedule was not found.") from exc
    return DoctorScheduleRead.model_validate(schedule)


@router.put("/doctor-schedules/{schedule_id}", response_model=DoctorScheduleRead)
async def update_doctor_schedule(
    schedule_id: UUID,
    payload: DoctorScheduleUpdate,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> DoctorScheduleRead:
    try:
        schedule = await service.update_schedule(schedule_id, payload)
    except NotFoundError as exc:
        raise _not_found("Doctor or schedule was not found.") from exc
    except InactiveDoctorScheduleError as exc:
        raise _bad_request("Schedules cannot be updated for inactive doctors.") from exc
    except InvalidScheduleError as exc:
        raise _bad_request("Schedule hours or slot duration are invalid.") from exc
    except OverlappingScheduleError as exc:
        raise _conflict("Doctor schedule overlaps an existing schedule.") from exc
    return DoctorScheduleRead.model_validate(schedule)


@router.delete("/doctor-schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_schedule(
    schedule_id: UUID,
    service: Annotated[HospitalDomainService, Depends(get_hospital_domain_service)],
) -> None:
    try:
        await service.delete_schedule(schedule_id)
    except NotFoundError as exc:
        raise _not_found("Doctor schedule was not found.") from exc


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def _bad_request(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def _conflict(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
