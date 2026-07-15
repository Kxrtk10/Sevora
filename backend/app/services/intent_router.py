from enum import StrEnum


class ConciergeIntent(StrEnum):
    BOOK_APPOINTMENT = "book_appointment"
    FIND_DOCTOR = "find_doctor"
    BROWSE_DEPARTMENTS = "browse_departments"
    HOSPITAL_INFORMATION = "hospital_information"
    CANCEL_APPOINTMENT = "cancel_appointment"
    RESCHEDULE_APPOINTMENT = "reschedule_appointment"
    MEDICAL_ADVICE = "medical_advice"
    UNKNOWN = "unknown"


class RuleBasedIntentRouter:
    def route(self, message: str, action: str | None = None) -> ConciergeIntent:
        if action:
            try:
                return ConciergeIntent(action)
            except ValueError:
                return ConciergeIntent.UNKNOWN

        normalized = message.lower()
        if any(word in normalized for word in ["diagnose", "medicine", "medication", "report"]):
            return ConciergeIntent.MEDICAL_ADVICE
        if any(word in normalized for word in ["cancel", "call off"]):
            return ConciergeIntent.CANCEL_APPOINTMENT
        if any(word in normalized for word in ["reschedule", "change my appointment", "move"]):
            return ConciergeIntent.RESCHEDULE_APPOINTMENT
        if any(word in normalized for word in ["department", "departments", "browse"]):
            return ConciergeIntent.BROWSE_DEPARTMENTS
        if any(word in normalized for word in ["doctor", "specialist", "physician", "skin"]):
            return ConciergeIntent.FIND_DOCTOR
        if any(
            word in normalized for word in ["book", "appointment", "pain", "knee", "fever", "child"]
        ):
            return ConciergeIntent.BOOK_APPOINTMENT
        if any(
            word in normalized for word in ["hospital", "address", "phone", "hours", "information"]
        ):
            return ConciergeIntent.HOSPITAL_INFORMATION
        return ConciergeIntent.UNKNOWN


def infer_department_name(message: str) -> str | None:
    normalized = message.lower()
    if any(word in normalized for word in ["knee", "bone", "joint", "orthopedic", "orthopaedic"]):
        return "Orthopedics"
    if any(word in normalized for word in ["skin", "rash", "dermatology", "dermatologist"]):
        return "Dermatology"
    if any(word in normalized for word in ["child", "kid", "pediatric", "paediatric"]):
        return "Pediatrics"
    if any(word in normalized for word in ["fever", "general", "checkup", "cough"]):
        return "General Medicine"
    return None
