import { motion } from "framer-motion";
import {
  Building2,
  CalendarClock,
  CheckCircle2,
  ClipboardList,
  Loader2,
  MessageCircle,
  Search,
  Send,
  ShieldCheck,
  Stethoscope,
  UserRound,
  XCircle,
} from "lucide-react";
import { FormEvent, useRef, useState } from "react";

type Department = {
  id: string;
  name: string;
  description?: string | null;
};

type Doctor = {
  id: string;
  department_id: string;
  full_name: string;
  specialization: string;
  qualification: string;
  years_of_experience: number;
  consultation_duration_minutes: number;
  consultation_fee: string;
};

type Slot = {
  doctor_id: string;
  appointment_date: string;
  start_time: string;
  end_time: string;
  label: string;
};

type ConciergeAppointment = {
  id: string;
  patient_name: string;
  doctor_id: string;
  department_id: string;
  appointment_date: string;
  appointment_start_time: string;
  appointment_end_time: string;
  status: string;
};

type ConciergeResponse = {
  intent: string;
  message: string;
  departments: Department[];
  doctors: Doctor[];
  slots: Slot[];
  appointment?: ConciergeAppointment | null;
  safety_notice?: string | null;
  requires_input: string[];
};

type Message = {
  id: number;
  role: "patient" | "concierge";
  text: string;
  response?: ConciergeResponse;
};

const quickActions = [
  { label: "Book Appointment", action: "book_appointment", icon: CalendarClock },
  { label: "Find a Doctor", action: "find_doctor", icon: Stethoscope },
  { label: "Browse Departments", action: "browse_departments", icon: ClipboardList },
  { label: "Reschedule Appointment", action: "reschedule_appointment", icon: CalendarClock },
  { label: "Cancel Appointment", action: "cancel_appointment", icon: XCircle },
  { label: "Hospital Information", action: "hospital_information", icon: Building2 },
];

const apiBaseUrl = "http://127.0.0.1:8000";

export function AIConciergePage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState<Slot | null>(null);
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null);
  const [selectedDepartment, setSelectedDepartment] = useState<Department | null>(null);
  const [bookingForm, setBookingForm] = useState({
    patient_name: "",
    patient_email: "",
    patient_phone: "",
  });
  const [appointmentId, setAppointmentId] = useState("");
  const nextMessageId = useRef(1);

  async function sendMessage(message: string, action?: string, extraPayload = {}) {
    if (!message.trim() || isLoading) return;

    const patientMessage: Message = {
      id: nextMessageId.current,
      role: "patient",
      text: message,
    };
    nextMessageId.current += 1;
    setMessages((current) => [...current, patientMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/ai-concierge/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, action, ...extraPayload }),
      });
      if (!response.ok) {
        throw new Error("Concierge request failed.");
      }
      const body = (await response.json()) as ConciergeResponse;
      setMessages((current) => [
        ...current,
        {
          id: nextMessageId.current,
          role: "concierge",
          text: body.message,
          response: body,
        },
      ]);
      nextMessageId.current += 1;
    } catch {
      setMessages((current) => [
        ...current,
        {
          id: nextMessageId.current,
          role: "concierge",
          text: "I couldn't reach ClinicFlow services right now. Please try again in a moment.",
        },
      ]);
      nextMessageId.current += 1;
    } finally {
      setIsLoading(false);
    }
  }

  function submitMessage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendMessage(input);
  }

  function selectSlot(slot: Slot, doctors: Doctor[], departments: Department[]) {
    const doctor = doctors.find((item) => item.id === slot.doctor_id) ?? null;
    const department = departments.find((item) => item.id === doctor?.department_id) ?? null;
    setSelectedSlot(slot);
    setSelectedDoctor(doctor);
    setSelectedDepartment(department);
  }

  function submitBooking(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedSlot || !selectedDoctor || !selectedDepartment) return;
    void sendMessage("Book this appointment", "book_appointment", {
      doctor_id: selectedDoctor.id,
      department_id: selectedDepartment.id,
      patient_name: bookingForm.patient_name,
      patient_email: bookingForm.patient_email,
      patient_phone: bookingForm.patient_phone,
      reason_for_visit: input || `Appointment with ${selectedDoctor.specialization}`,
      appointment_date: selectedSlot.appointment_date,
      appointment_start_time: selectedSlot.start_time,
      appointment_end_time: selectedSlot.end_time,
    });
    setSelectedSlot(null);
  }

  function submitCancellation(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendMessage("I need to cancel my appointment", "cancel_appointment", {
      appointment_id: appointmentId,
    });
    setAppointmentId("");
  }

  return (
    <section className="mx-auto max-w-7xl">
      <div className="grid gap-6 lg:grid-cols-[0.72fr_1.28fr]">
        <aside className="rounded-[2rem] border border-border bg-white p-6 shadow-soft">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blueSoft text-blue">
            <MessageCircle className="h-6 w-6" />
          </div>
          <h1 className="mt-6 text-3xl font-semibold tracking-[-0.04em] text-ink">
            Welcome to ClinicFlow AI Concierge
          </h1>
          <p className="mt-4 text-sm leading-7 text-slate-600">
            I&apos;m here to help you book appointments, find the right department, answer
            hospital questions and simplify your healthcare journey.
          </p>
          <div className="mt-6 rounded-2xl border border-border bg-muted p-4">
            <div className="flex items-start gap-3">
              <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0 text-emerald-700" />
              <p className="text-sm leading-6 text-slate-600">
                I can coordinate care access, but I can&apos;t diagnose conditions, interpret
                reports or recommend medication.
              </p>
            </div>
          </div>
          <div className="mt-6 grid gap-3">
            {quickActions.map((item) => (
              <button
                key={item.action}
                type="button"
                onClick={() => void sendMessage(item.label, item.action)}
                className="flex items-center gap-3 rounded-2xl border border-border bg-white px-4 py-3 text-left text-sm font-semibold text-ink transition hover:border-blue/30 hover:bg-blueSoft/40"
              >
                <item.icon className="h-4 w-4 text-blue" />
                {item.label}
              </button>
            ))}
          </div>
        </aside>

        <div className="overflow-hidden rounded-[2rem] border border-border bg-white shadow-product">
          <div className="border-b border-border px-6 py-5">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">
              Front Desk
            </p>
            <h2 className="mt-1 text-xl font-semibold text-ink">Patient Concierge</h2>
          </div>

          <div className="min-h-[560px] space-y-5 bg-muted/70 p-5">
            {messages.length === 0 ? (
              <EmptyState />
            ) : (
              messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={message.role === "patient" ? "ml-auto max-w-2xl" : "max-w-4xl"}
                >
                  <div
                    className={`rounded-3xl border p-5 ${
                      message.role === "patient"
                        ? "border-blue/20 bg-blue text-white"
                        : "border-border bg-white text-ink"
                    }`}
                  >
                    <p className="text-sm leading-6">{message.text}</p>
                    {message.response ? (
                      <ResponseCards
                        response={message.response}
                        onSelectSlot={(slot) =>
                          selectSlot(
                            slot,
                            message.response?.doctors ?? [],
                            message.response?.departments ?? [],
                          )
                        }
                      />
                    ) : null}
                  </div>
                </motion.div>
              ))
            )}

            {isLoading ? (
              <div className="flex max-w-sm items-center gap-3 rounded-3xl border border-border bg-white p-4 text-sm text-slate-600">
                <Loader2 className="h-4 w-4 animate-spin text-blue" />
                ClinicFlow Concierge is checking availability
              </div>
            ) : null}
          </div>

          {selectedSlot ? (
            <form onSubmit={submitBooking} className="border-t border-border bg-white p-5">
              <p className="text-sm font-semibold text-ink">
                Confirm {selectedSlot.label} with {selectedDoctor?.full_name}
              </p>
              <div className="mt-4 grid gap-3 md:grid-cols-3">
                <input
                  required
                  placeholder="Patient name"
                  value={bookingForm.patient_name}
                  onChange={(event) =>
                    setBookingForm({ ...bookingForm, patient_name: event.target.value })
                  }
                  className="rounded-2xl border border-border px-4 py-3 text-sm outline-none focus:border-blue"
                />
                <input
                  required
                  type="email"
                  placeholder="Email"
                  value={bookingForm.patient_email}
                  onChange={(event) =>
                    setBookingForm({ ...bookingForm, patient_email: event.target.value })
                  }
                  className="rounded-2xl border border-border px-4 py-3 text-sm outline-none focus:border-blue"
                />
                <input
                  required
                  placeholder="Phone"
                  value={bookingForm.patient_phone}
                  onChange={(event) =>
                    setBookingForm({ ...bookingForm, patient_phone: event.target.value })
                  }
                  className="rounded-2xl border border-border px-4 py-3 text-sm outline-none focus:border-blue"
                />
              </div>
              <button className="mt-4 rounded-full bg-blue px-5 py-3 text-sm font-semibold text-white">
                Confirm Appointment
              </button>
            </form>
          ) : null}

          <div className="border-t border-border bg-white p-5">
            <form onSubmit={submitMessage} className="flex gap-3">
              <input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Tell me what you need help with"
                className="min-h-12 flex-1 rounded-full border border-border px-5 text-sm outline-none transition focus:border-blue focus:ring-4 focus:ring-blue/10"
              />
              <button
                type="submit"
                className="flex h-12 w-12 items-center justify-center rounded-full bg-blue text-white"
                aria-label="Send message"
              >
                <Send className="h-4 w-4" />
              </button>
            </form>
            <form onSubmit={submitCancellation} className="mt-3 flex gap-3">
              <input
                value={appointmentId}
                onChange={(event) => setAppointmentId(event.target.value)}
                placeholder="Appointment ID for cancellation or reschedule"
                className="min-h-11 flex-1 rounded-full border border-border px-5 text-xs outline-none transition focus:border-blue"
              />
              <button className="rounded-full border border-border px-4 text-xs font-semibold text-slate-700">
                Cancel
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}

function EmptyState() {
  return (
    <div className="grid min-h-[520px] place-items-center">
      <div className="max-w-xl text-center">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-blue shadow-soft">
          <UserRound className="h-6 w-6" />
        </div>
        <h3 className="mt-5 text-2xl font-semibold tracking-[-0.035em] text-ink">
          How can I help with your visit today?
        </h3>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          Try “I have knee pain”, “I want a skin specialist”, or “I need to cancel my appointment”.
        </p>
      </div>
    </div>
  );
}

function ResponseCards({
  response,
  onSelectSlot,
}: {
  response: ConciergeResponse;
  onSelectSlot: (slot: Slot) => void;
}) {
  return (
    <div className="mt-5 space-y-4">
      {response.safety_notice ? (
        <div className="rounded-2xl bg-greenSoft p-4 text-sm text-emerald-800">
          {response.safety_notice}
        </div>
      ) : null}

      {response.departments.length ? (
        <div className="grid gap-3 md:grid-cols-2">
          {response.departments.map((department) => (
            <div key={department.id} className="rounded-2xl border border-border bg-muted p-4">
              <p className="text-sm font-semibold text-ink">{department.name}</p>
              <p className="mt-1 text-xs leading-5 text-slate-600">{department.description}</p>
            </div>
          ))}
        </div>
      ) : null}

      {response.doctors.length ? (
        <div className="grid gap-3 md:grid-cols-2">
          {response.doctors.map((doctor) => (
            <div key={doctor.id} className="rounded-2xl border border-border bg-white p-4">
              <div className="flex items-start gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blueSoft text-blue">
                  <Stethoscope className="h-5 w-5" />
                </span>
                <div>
                  <p className="text-sm font-semibold text-ink">{doctor.full_name}</p>
                  <p className="mt-1 text-xs text-slate-500">{doctor.specialization}</p>
                  <p className="mt-2 text-xs leading-5 text-slate-600">
                    {doctor.qualification} · {doctor.years_of_experience} years · ₹
                    {doctor.consultation_fee}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : null}

      {response.slots.length ? (
        <div className="grid gap-3 md:grid-cols-3">
          {response.slots.map((slot) => (
            <button
              key={`${slot.doctor_id}-${slot.appointment_date}-${slot.start_time}`}
              type="button"
              onClick={() => onSelectSlot(slot)}
              className="rounded-2xl border border-blue/20 bg-blueSoft p-4 text-left text-sm font-semibold text-blue transition hover:bg-blueSoft/70"
            >
              <CalendarClock className="mb-2 h-4 w-4" />
              {slot.label}
            </button>
          ))}
        </div>
      ) : null}

      {response.appointment ? (
        <div className="rounded-2xl border border-emerald-200 bg-greenSoft p-4">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="h-5 w-5 text-emerald-700" />
            <div>
              <p className="text-sm font-semibold text-ink">Appointment {response.appointment.status}</p>
              <p className="mt-1 text-xs text-slate-600">
                {response.appointment.appointment_date} ·{" "}
                {response.appointment.appointment_start_time}
              </p>
              <p className="mt-2 font-mono text-xs text-slate-500">{response.appointment.id}</p>
            </div>
          </div>
        </div>
      ) : null}

      {response.intent === "unknown" ? (
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <Search className="h-4 w-4" />
          Try asking for a doctor, department, appointment booking, cancellation or hospital details.
        </div>
      ) : null}
    </div>
  );
}
