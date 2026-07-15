from datetime import UTC, date, datetime, timedelta
from uuid import UUID

from app.models.appointment import Appointment
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.schemas.ai_concierge import (
    AIConciergeRequest,
    AIConciergeResponse,
    ConciergeAction,
    ConciergeAppointment,
    ConciergeDepartment,
    ConciergeDoctor,
    ConciergeSlot,
)
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.services.ai_provider import AIProvider
from app.services.appointments import (
    AppointmentNotFoundError,
    AppointmentService,
    DoubleBookingError,
    InvalidAppointmentScheduleError,
    InvalidStatusTransitionError,
)
from app.services.hospital_domain import HospitalDomainService
from app.services.intent_router import ConciergeIntent, RuleBasedIntentRouter, infer_department_name

MEDICAL_SAFETY_MESSAGE = (
    "I'm unable to provide medical advice. I can help connect you with the appropriate "
    "department or arrange an appointment."
)


class AIConciergeService:
    def __init__(
        self,
        *,
        hospital_service: HospitalDomainService,
        appointment_service: AppointmentService,
        intent_router: RuleBasedIntentRouter,
        ai_provider: AIProvider,
    ) -> None:
        self.hospital_service = hospital_service
        self.appointment_service = appointment_service
        self.intent_router = intent_router
        self.ai_provider = ai_provider

    async def handle(self, payload: AIConciergeRequest) -> AIConciergeResponse:
        intent = self.intent_router.route(payload.message, payload.action)
        if intent == ConciergeIntent.MEDICAL_ADVICE:
            return AIConciergeResponse(
                intent=intent,
                message=await self.ai_provider.render_response(intent, MEDICAL_SAFETY_MESSAGE),
                safety_notice=MEDICAL_SAFETY_MESSAGE,
                actions=[ConciergeAction(label="Find a department", action="browse_departments")],
            )
        if intent == ConciergeIntent.BROWSE_DEPARTMENTS:
            return await self._browse_departments(intent)
        if intent in {ConciergeIntent.BOOK_APPOINTMENT, ConciergeIntent.FIND_DOCTOR}:
            return await self._doctor_guidance(intent, payload)
        if intent == ConciergeIntent.HOSPITAL_INFORMATION:
            return await self._hospital_information(intent)
        if intent == ConciergeIntent.CANCEL_APPOINTMENT:
            return await self._cancel_appointment(intent, payload)
        if intent == ConciergeIntent.RESCHEDULE_APPOINTMENT:
            return await self._reschedule_appointment(intent, payload)
        return AIConciergeResponse(
            intent=intent,
            message=(
                "I can help with appointments, doctors, departments, cancellations "
                "or hospital information."
            ),
            actions=[
                ConciergeAction(label="Book Appointment", action="book_appointment"),
                ConciergeAction(label="Browse Departments", action="browse_departments"),
            ],
        )

    async def _browse_departments(self, intent: ConciergeIntent) -> AIConciergeResponse:
        departments = await self.hospital_service.list_departments(limit=100)
        active = [department for department in departments if department.is_active]
        return AIConciergeResponse(
            intent=intent,
            message="Here are the departments I can connect you with.",
            departments=[self._department_card(department) for department in active],
        )

    async def _doctor_guidance(
        self,
        intent: ConciergeIntent,
        payload: AIConciergeRequest,
    ) -> AIConciergeResponse:
        department = await self._resolve_department(payload)
        departments = (
            [department]
            if department
            else [
                item
                for item in await self.hospital_service.list_departments(limit=100)
                if item.is_active
            ]
        )
        doctors = await self._active_doctors(department.id if department else payload.department_id)
        slots = await self._available_slots(doctors)

        if payload.action == ConciergeIntent.BOOK_APPOINTMENT and self._has_booking_payload(
            payload
        ):
            return await self._book_appointment(intent, payload)

        message = "I found doctors who match your request."
        if department is not None:
            message = f"For this request, {department.name} is the best starting point."
        return AIConciergeResponse(
            intent=intent,
            message=message,
            departments=[self._department_card(item) for item in departments[:4]],
            doctors=[self._doctor_card(doctor) for doctor in doctors],
            slots=slots,
            actions=[ConciergeAction(label="Confirm Booking", action="book_appointment")],
            requires_input=["patient_name", "patient_email", "patient_phone"] if doctors else [],
        )

    async def _book_appointment(
        self,
        intent: ConciergeIntent,
        payload: AIConciergeRequest,
    ) -> AIConciergeResponse:
        missing = [
            field
            for field in [
                "doctor_id",
                "department_id",
                "patient_name",
                "patient_email",
                "patient_phone",
                "appointment_date",
                "appointment_start_time",
                "appointment_end_time",
            ]
            if getattr(payload, field) is None
        ]
        if missing:
            return AIConciergeResponse(
                intent=intent,
                message="I can book that once I have the patient details and selected time.",
                requires_input=missing,
            )
        try:
            appointment = await self.appointment_service.create_appointment(
                AppointmentCreate(
                    patient_name=payload.patient_name or "",
                    patient_email=payload.patient_email,
                    patient_phone=payload.patient_phone or "",
                    reason_for_visit=payload.reason_for_visit or payload.message,
                    doctor_id=payload.doctor_id,
                    department_id=payload.department_id,
                    appointment_date=payload.appointment_date,
                    appointment_start_time=payload.appointment_start_time,
                    appointment_end_time=payload.appointment_end_time,
                )
            )
        except (DoubleBookingError, InvalidAppointmentScheduleError):
            return AIConciergeResponse(
                intent=intent,
                message="That appointment time is no longer available. Please choose another slot.",
                slots=await self._available_slots(
                    await self._active_doctors(payload.department_id)
                ),
            )
        return AIConciergeResponse(
            intent=intent,
            message="Your appointment is confirmed in ClinicFlow.",
            appointment=self._appointment_card(appointment),
        )

    async def _cancel_appointment(
        self,
        intent: ConciergeIntent,
        payload: AIConciergeRequest,
    ) -> AIConciergeResponse:
        if payload.appointment_id is None:
            return AIConciergeResponse(
                intent=intent,
                message="Please share the appointment ID so I can cancel the correct booking.",
                requires_input=["appointment_id"],
            )
        try:
            appointment = await self.appointment_service.cancel_appointment(payload.appointment_id)
        except (AppointmentNotFoundError, InvalidStatusTransitionError):
            return AIConciergeResponse(
                intent=intent,
                message=(
                    "I couldn't cancel that appointment. Please check the appointment ID "
                    "or status."
                ),
            )
        return AIConciergeResponse(
            intent=intent,
            message="The appointment has been cancelled.",
            appointment=self._appointment_card(appointment),
        )

    async def _reschedule_appointment(
        self,
        intent: ConciergeIntent,
        payload: AIConciergeRequest,
    ) -> AIConciergeResponse:
        if payload.appointment_id is None:
            return AIConciergeResponse(
                intent=intent,
                message="Please share the appointment ID and preferred new slot.",
                requires_input=["appointment_id"],
            )
        try:
            appointment = await self.appointment_service.update_appointment(
                payload.appointment_id,
                AppointmentUpdate(
                    appointment_date=payload.appointment_date,
                    appointment_start_time=payload.appointment_start_time,
                    appointment_end_time=payload.appointment_end_time,
                ),
            )
        except (AppointmentNotFoundError, DoubleBookingError, InvalidAppointmentScheduleError):
            return AIConciergeResponse(
                intent=intent,
                message="I couldn't reschedule that appointment to the selected time.",
            )
        return AIConciergeResponse(
            intent=intent,
            message="The appointment has been rescheduled.",
            appointment=self._appointment_card(appointment),
        )

    async def _hospital_information(self, intent: ConciergeIntent) -> AIConciergeResponse:
        hospitals = await self.hospital_service.list_hospitals(limit=1)
        if not hospitals:
            return AIConciergeResponse(
                intent=intent, message="Hospital information is not available yet."
            )
        hospital = hospitals[0]
        return AIConciergeResponse(
            intent=intent,
            message=(
                f"{hospital.name} is located at {hospital.address}, {hospital.city}. "
                f"You can reach the front desk at {hospital.phone}."
            ),
        )

    async def _resolve_department(self, payload: AIConciergeRequest) -> Department | None:
        if payload.department_id is not None:
            return await self.hospital_service.get_department(payload.department_id)
        inferred = infer_department_name(payload.message)
        if inferred is None:
            return None
        departments = await self.hospital_service.list_departments(limit=100)
        return next((item for item in departments if item.name.lower() == inferred.lower()), None)

    async def _active_doctors(self, department_id: UUID | None = None) -> list[Doctor]:
        doctors = await self.hospital_service.list_doctors(department_id=department_id, limit=100)
        return [doctor for doctor in doctors if doctor.is_active]

    async def _available_slots(self, doctors: list[Doctor]) -> list[ConciergeSlot]:
        slots: list[ConciergeSlot] = []
        today = datetime.now(UTC).date()
        for doctor in doctors[:4]:
            schedules = await self.hospital_service.list_schedules(doctor_id=doctor.id, limit=20)
            for schedule in schedules:
                if not schedule.is_available:
                    continue
                slot_date = self._next_date_for_weekday(today, schedule.weekday)
                appointments = await self.appointment_service.list_appointments(
                    doctor_id=doctor.id,
                    appointment_date=slot_date,
                )
                if self._slot_is_available(schedule, appointments, slot_date):
                    slots.append(
                        ConciergeSlot(
                            doctor_id=doctor.id,
                            appointment_date=slot_date,
                            start_time=schedule.start_time,
                            end_time=self._slot_end(schedule),
                            label=(
                                f"{slot_date.isoformat()} at "
                                f"{schedule.start_time.strftime('%H:%M')}"
                            ),
                        )
                    )
                if len(slots) >= 6:
                    return slots
        return slots

    def _slot_is_available(
        self,
        schedule: DoctorSchedule,
        appointments: list[Appointment],
        slot_date: date,
    ) -> bool:
        slot_end = self._slot_end(schedule)
        return not any(
            appointment.appointment_date == slot_date
            and appointment.appointment_start_time < slot_end
            and appointment.appointment_end_time > schedule.start_time
            for appointment in appointments
        )

    def _slot_end(self, schedule: DoctorSchedule):
        return (
            datetime.combine(date.min, schedule.start_time)
            + timedelta(minutes=schedule.slot_duration)
        ).time()

    def _next_date_for_weekday(self, today: date, weekday: int) -> date:
        days_ahead = (weekday - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)

    def _has_booking_payload(self, payload: AIConciergeRequest) -> bool:
        return payload.doctor_id is not None and payload.appointment_date is not None

    def _department_card(self, department: Department) -> ConciergeDepartment:
        return ConciergeDepartment(
            id=department.id,
            name=department.name,
            description=department.description,
        )

    def _doctor_card(self, doctor: Doctor) -> ConciergeDoctor:
        return ConciergeDoctor(
            id=doctor.id,
            department_id=doctor.department_id,
            full_name=doctor.full_name,
            specialization=doctor.specialization,
            qualification=doctor.qualification,
            years_of_experience=doctor.years_of_experience,
            consultation_duration_minutes=doctor.consultation_duration_minutes,
            consultation_fee=str(doctor.consultation_fee),
        )

    def _appointment_card(self, appointment: Appointment) -> ConciergeAppointment:
        return ConciergeAppointment(
            id=appointment.id,
            patient_name=appointment.patient_name,
            doctor_id=appointment.doctor_id,
            department_id=appointment.department_id,
            appointment_date=appointment.appointment_date,
            appointment_start_time=appointment.appointment_start_time,
            appointment_end_time=appointment.appointment_end_time,
            status=appointment.status,
        )
