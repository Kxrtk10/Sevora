import {
  Bell,
  CalendarClock,
  FileText,
  Loader2,
  Mail,
  Phone,
  UserRound,
} from "lucide-react";
import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";

type AppointmentStatus =
  | "pending"
  | "confirmed"
  | "checked_in"
  | "completed"
  | "cancelled"
  | "no_show";

type Appointment = {
  id: string;
  patient_name: string;
  patient_email: string;
  patient_phone: string;
  reason_for_visit: string;
  doctor_id: string;
  department_id: string;
  appointment_date: string;
  appointment_start_time: string;
  appointment_end_time: string;
  status: AppointmentStatus;
  notes?: string | null;
  created_at: string;
  updated_at: string;
};

type Doctor = {
  id: string;
  department_id: string;
  full_name: string;
  specialization: string;
  qualification?: string;
};

type Department = {
  id: string;
  name: string;
};

type EnrichedAppointment = Appointment & {
  doctor?: Doctor;
  department?: Department;
};

type Profile = {
  name: string;
  email: string;
  phone: string;
};

const apiBaseUrl = "http://127.0.0.1:8000";

const statusLabels: Record<AppointmentStatus, string> = {
  pending: "Pending",
  confirmed: "Confirmed",
  checked_in: "Checked In",
  completed: "Completed",
  cancelled: "Cancelled",
  no_show: "No Show",
};

const statusStyles: Record<AppointmentStatus, string> = {
  pending: "bg-blueSoft text-blue",
  confirmed: "bg-greenSoft text-emerald-700",
  checked_in: "bg-amber-50 text-amber-700",
  completed: "bg-slate-100 text-slate-700",
  cancelled: "bg-red-50 text-red-700",
  no_show: "bg-slate-200 text-slate-700",
};

const notifications = [
  {
    title: "Appointment confirmed",
    description: "Your clinic visit is confirmed. Please arrive 10 minutes early.",
    tone: "green",
  },
  {
    title: "Reminder for tomorrow",
    description: "Bring any previous reports or prescriptions relevant to your visit.",
    tone: "blue",
  },
  {
    title: "Appointment cancelled",
    description: "Cancelled appointments remain visible in your medical timeline.",
    tone: "red",
  },
];

export function PatientDashboardPage() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [selectedAppointmentId, setSelectedAppointmentId] = useState<string | null>(null);
  const [rescheduleAppointmentId, setRescheduleAppointmentId] = useState<string | null>(null);
  const [rescheduleForm, setRescheduleForm] = useState({
    appointment_date: "",
    appointment_start_time: "",
    appointment_end_time: "",
  });
  const [profile, setProfile] = useState<Profile>({
    name: "",
    email: "",
    phone: "",
  });
  const [savedProfile, setSavedProfile] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadPortal = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [appointmentResponse, doctorResponse, departmentResponse] = await Promise.all([
        fetch(`${apiBaseUrl}/api/v1/appointments?limit=200`),
        fetch(`${apiBaseUrl}/api/v1/doctors?limit=200`),
        fetch(`${apiBaseUrl}/api/v1/departments?limit=200`),
      ]);
      if (!appointmentResponse.ok || !doctorResponse.ok || !departmentResponse.ok) {
        throw new Error("Unable to load patient portal.");
      }
      const appointmentData = (await appointmentResponse.json()) as Appointment[];
      setAppointments(appointmentData);
      setDoctors((await doctorResponse.json()) as Doctor[]);
      setDepartments((await departmentResponse.json()) as Department[]);

      const firstAppointment = appointmentData[0];
      if (firstAppointment) {
        setProfile((current) => ({
          name: current.name || firstAppointment.patient_name,
          email: current.email || firstAppointment.patient_email,
          phone: current.phone || firstAppointment.patient_phone,
        }));
      }
    } catch {
      setError("Patient portal data is unavailable. Confirm the backend is running and try again.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const loader = window.setTimeout(() => {
      void loadPortal();
    }, 0);
    return () => window.clearTimeout(loader);
  }, [loadPortal]);

  const doctorById = useMemo(
    () => new Map(doctors.map((doctor) => [doctor.id, doctor])),
    [doctors],
  );
  const departmentById = useMemo(
    () => new Map(departments.map((department) => [department.id, department])),
    [departments],
  );

  const enrichedAppointments = useMemo<EnrichedAppointment[]>(
    () =>
      appointments
        .map((appointment) => ({
          ...appointment,
          doctor: doctorById.get(appointment.doctor_id),
          department: departmentById.get(appointment.department_id),
        }))
        .sort((a, b) => {
          const left = `${a.appointment_date}T${a.appointment_start_time}`;
          const right = `${b.appointment_date}T${b.appointment_start_time}`;
          return left.localeCompare(right);
        }),
    [appointments, departmentById, doctorById],
  );

  const upcomingAppointment =
    enrichedAppointments.find((appointment) =>
      ["pending", "confirmed", "checked_in"].includes(appointment.status),
    ) ?? null;

  const selectedAppointment =
    enrichedAppointments.find((appointment) => appointment.id === selectedAppointmentId) ?? null;

  const previousAppointments = enrichedAppointments.filter((appointment) =>
    ["completed", "cancelled", "no_show"].includes(appointment.status),
  );

  async function cancelAppointment(appointment: Appointment) {
    setUpdatingId(appointment.id);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/appointments/${appointment.id}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error("Unable to cancel appointment.");
      }
      const updated = (await response.json()) as Appointment;
      setAppointments((current) =>
        current.map((item) => (item.id === appointment.id ? updated : item)),
      );
    } catch {
      setError("This appointment could not be cancelled. Please contact reception.");
    } finally {
      setUpdatingId(null);
    }
  }

  async function submitReschedule(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!rescheduleAppointmentId) return;
    setUpdatingId(rescheduleAppointmentId);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/appointments/${rescheduleAppointmentId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(rescheduleForm),
      });
      if (!response.ok) {
        throw new Error("Unable to reschedule appointment.");
      }
      const updated = (await response.json()) as Appointment;
      setAppointments((current) =>
        current.map((item) => (item.id === updated.id ? updated : item)),
      );
      setRescheduleAppointmentId(null);
      setRescheduleForm({
        appointment_date: "",
        appointment_start_time: "",
        appointment_end_time: "",
      });
    } catch {
      setError("That time is unavailable. Please choose a slot within the doctor's schedule.");
    } finally {
      setUpdatingId(null);
    }
  }

  function startReschedule(appointment: Appointment) {
    setRescheduleAppointmentId(appointment.id);
    setRescheduleForm({
      appointment_date: appointment.appointment_date,
      appointment_start_time: appointment.appointment_start_time,
      appointment_end_time: appointment.appointment_end_time,
    });
  }

  function saveProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSavedProfile(true);
    window.setTimeout(() => setSavedProfile(false), 2400);
  }

  return (
    <section className="mx-auto max-w-[1400px] space-y-6">
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Patient Portal
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-[-0.04em] text-ink">
            Your care, organized.
          </h1>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            View appointments, manage changes and keep your contact details ready without calling
            the clinic.
          </p>
        </div>
        <button
          type="button"
          onClick={() => void loadPortal()}
          className="min-h-11 rounded-2xl bg-blue px-5 text-sm font-semibold text-white"
        >
          Refresh Portal
        </button>
      </div>

      {error ? (
        <div className="rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      ) : null}

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <UpcomingAppointmentCard appointment={upcomingAppointment} isLoading={isLoading} />
        <ProfileCard
          profile={profile}
          isSaved={savedProfile}
          onChange={setProfile}
          onSubmit={saveProfile}
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-6">
          <AppointmentsPanel
            appointments={enrichedAppointments}
            updatingId={updatingId}
            onSelect={(appointment) => setSelectedAppointmentId(appointment.id)}
            onCancel={(appointment) => void cancelAppointment(appointment)}
            onReschedule={startReschedule}
          />
          <MedicalTimeline appointments={previousAppointments} />
        </div>

        <div className="space-y-6">
          <AppointmentDetails appointment={selectedAppointment} />
          <ReschedulePanel
            appointment={enrichedAppointments.find((item) => item.id === rescheduleAppointmentId) ?? null}
            form={rescheduleForm}
            onChange={setRescheduleForm}
            onCancel={() => setRescheduleAppointmentId(null)}
            onSubmit={submitReschedule}
            isUpdating={Boolean(updatingId && updatingId === rescheduleAppointmentId)}
          />
          <NotificationCenter />
        </div>
      </div>
    </section>
  );
}

function UpcomingAppointmentCard({
  appointment,
  isLoading,
}: {
  appointment: EnrichedAppointment | null;
  isLoading: boolean;
}) {
  return (
    <div className="rounded-[1.75rem] border border-border bg-white p-6 shadow-soft">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">
            Dashboard
          </p>
          <h2 className="mt-2 text-xl font-semibold text-ink">Upcoming Appointment</h2>
        </div>
        <CalendarClock className="h-5 w-5 text-blue" />
      </div>

      {isLoading ? (
        <div className="mt-8 flex items-center gap-3 text-sm text-slate-500">
          <Loader2 className="h-4 w-4 animate-spin text-blue" />
          Loading your visit
        </div>
      ) : appointment ? (
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <Metric label="Next Visit Date" value={appointment.appointment_date} />
          <Metric label="Appointment Status" value={statusLabels[appointment.status]} />
          <Metric label="Assigned Doctor" value={appointment.doctor?.full_name ?? "Unassigned"} />
          <Metric label="Department" value={appointment.department?.name ?? "Unknown"} />
        </div>
      ) : (
        <div className="mt-8 rounded-2xl bg-muted p-5 text-sm text-slate-600">
          No upcoming appointment is currently scheduled.
        </div>
      )}
    </div>
  );
}

function ProfileCard({
  profile,
  isSaved,
  onChange,
  onSubmit,
}: {
  profile: Profile;
  isSaved: boolean;
  onChange: (profile: Profile) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <form onSubmit={onSubmit} className="rounded-[1.75rem] border border-border bg-white p-6 shadow-soft">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">Profile</p>
          <h2 className="mt-2 text-xl font-semibold text-ink">Contact Details</h2>
        </div>
        <UserRound className="h-5 w-5 text-blue" />
      </div>
      <div className="mt-5 grid gap-3">
        <ProfileInput
          icon={UserRound}
          label="Name"
          value={profile.name}
          onChange={(value) => onChange({ ...profile, name: value })}
        />
        <ProfileInput
          icon={Mail}
          label="Email"
          type="email"
          value={profile.email}
          onChange={(value) => onChange({ ...profile, email: value })}
        />
        <ProfileInput
          icon={Phone}
          label="Phone"
          value={profile.phone}
          onChange={(value) => onChange({ ...profile, phone: value })}
        />
      </div>
      <div className="mt-5 flex items-center justify-between gap-4">
        <p className="text-xs text-slate-500">
          Profile changes are saved for this portal session.
        </p>
        <button className="rounded-full bg-blue px-5 py-2.5 text-sm font-semibold text-white">
          Save
        </button>
      </div>
      {isSaved ? (
        <div className="mt-4 rounded-2xl bg-greenSoft px-4 py-3 text-sm font-medium text-emerald-700">
          Profile updated.
        </div>
      ) : null}
    </form>
  );
}

function AppointmentsPanel({
  appointments,
  updatingId,
  onSelect,
  onCancel,
  onReschedule,
}: {
  appointments: EnrichedAppointment[];
  updatingId: string | null;
  onSelect: (appointment: EnrichedAppointment) => void;
  onCancel: (appointment: EnrichedAppointment) => void;
  onReschedule: (appointment: EnrichedAppointment) => void;
}) {
  return (
    <div className="overflow-hidden rounded-[1.75rem] border border-border bg-white shadow-soft">
      <div className="border-b border-border px-5 py-4">
        <h2 className="text-base font-semibold text-ink">Appointments</h2>
        <p className="mt-1 text-xs text-slate-500">View, reschedule or cancel clinic visits.</p>
      </div>
      {appointments.length ? (
        <div className="divide-y divide-border">
          {appointments.map((appointment) => (
            <div key={appointment.id} className="grid gap-4 px-5 py-4 lg:grid-cols-[1fr_auto]">
              <button type="button" onClick={() => onSelect(appointment)} className="text-left">
                <div className="flex flex-wrap items-center gap-3">
                  <p className="text-sm font-semibold text-ink">{appointment.reason_for_visit}</p>
                  <StatusBadge status={appointment.status} />
                </div>
                <p className="mt-2 text-sm text-slate-600">
                  {appointment.appointment_date} at {formatTime(appointment.appointment_start_time)}
                  {" · "}
                  {appointment.doctor?.full_name ?? "Unassigned"}
                </p>
                <p className="mt-1 text-xs text-slate-500">{appointment.department?.name}</p>
              </button>
              <div className="flex flex-wrap items-center gap-2">
                <ActionButton disabled={updatingId === appointment.id} onClick={() => onSelect(appointment)}>
                  Details
                </ActionButton>
                <ActionButton
                  disabled={updatingId === appointment.id || isTerminal(appointment.status)}
                  onClick={() => onReschedule(appointment)}
                >
                  Reschedule
                </ActionButton>
                <ActionButton
                  disabled={updatingId === appointment.id || isTerminal(appointment.status)}
                  onClick={() => onCancel(appointment)}
                >
                  Cancel
                </ActionButton>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid min-h-52 place-items-center px-6 text-center">
          <div>
            <CalendarClock className="mx-auto h-8 w-8 text-slate-300" />
            <p className="mt-3 text-sm font-semibold text-ink">No appointments yet</p>
            <p className="mt-1 text-sm text-slate-500">Booked visits will appear here.</p>
          </div>
        </div>
      )}
    </div>
  );
}

function MedicalTimeline({ appointments }: { appointments: EnrichedAppointment[] }) {
  return (
    <div className="rounded-[1.75rem] border border-border bg-white p-5 shadow-soft">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-ink">Medical Timeline</h2>
          <p className="mt-1 text-xs text-slate-500">Previous visits in chronological order.</p>
        </div>
        <FileText className="h-5 w-5 text-blue" />
      </div>
      <div className="mt-5 space-y-3">
        {appointments.length ? (
          appointments.map((appointment) => (
            <div key={appointment.id} className="flex gap-3 rounded-2xl border border-border bg-muted p-4">
              <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-blue" />
              <div>
                <p className="text-sm font-semibold text-ink">{appointment.appointment_date}</p>
                <p className="mt-1 text-sm text-slate-600">
                  {appointment.doctor?.full_name ?? "Unassigned"} · {appointment.department?.name}
                </p>
                <p className="mt-1 text-xs text-slate-500">{statusLabels[appointment.status]}</p>
              </div>
            </div>
          ))
        ) : (
          <p className="rounded-2xl bg-muted p-4 text-sm text-slate-500">
            Completed or cancelled visits will appear here.
          </p>
        )}
      </div>
    </div>
  );
}

function AppointmentDetails({ appointment }: { appointment: EnrichedAppointment | null }) {
  return (
    <div className="rounded-[1.75rem] border border-border bg-white p-5 shadow-soft">
      <h2 className="text-base font-semibold text-ink">Appointment Details</h2>
      {appointment ? (
        <div className="mt-5 space-y-4">
          <Detail label="Patient" value={appointment.patient_name} />
          <Detail label="Reason" value={appointment.reason_for_visit} />
          <Detail label="Doctor" value={appointment.doctor?.full_name ?? "Unassigned"} />
          <Detail label="Department" value={appointment.department?.name ?? "Unknown"} />
          <Detail
            label="Visit Time"
            value={`${appointment.appointment_date}, ${formatTime(appointment.appointment_start_time)}`}
          />
          <Detail label="Notes" value={appointment.notes ?? "No notes recorded"} />
          <Detail label="Appointment ID" value={appointment.id} />
        </div>
      ) : (
        <p className="mt-4 text-sm leading-6 text-slate-500">
          Select an appointment to review visit details.
        </p>
      )}
    </div>
  );
}

function ReschedulePanel({
  appointment,
  form,
  onChange,
  onCancel,
  onSubmit,
  isUpdating,
}: {
  appointment: EnrichedAppointment | null;
  form: {
    appointment_date: string;
    appointment_start_time: string;
    appointment_end_time: string;
  };
  onChange: (form: {
    appointment_date: string;
    appointment_start_time: string;
    appointment_end_time: string;
  }) => void;
  onCancel: () => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  isUpdating: boolean;
}) {
  if (!appointment) return null;

  return (
    <form onSubmit={onSubmit} className="rounded-[1.75rem] border border-border bg-white p-5 shadow-soft">
      <h2 className="text-base font-semibold text-ink">Reschedule Appointment</h2>
      <p className="mt-2 text-sm text-slate-500">{appointment.reason_for_visit}</p>
      <div className="mt-5 grid gap-3">
        <input
          required
          type="date"
          value={form.appointment_date}
          onChange={(event) => onChange({ ...form, appointment_date: event.target.value })}
          className="min-h-11 rounded-2xl border border-border px-4 text-sm outline-none focus:border-blue"
        />
        <input
          required
          type="time"
          value={form.appointment_start_time.slice(0, 5)}
          onChange={(event) => onChange({ ...form, appointment_start_time: `${event.target.value}:00` })}
          className="min-h-11 rounded-2xl border border-border px-4 text-sm outline-none focus:border-blue"
        />
        <input
          required
          type="time"
          value={form.appointment_end_time.slice(0, 5)}
          onChange={(event) => onChange({ ...form, appointment_end_time: `${event.target.value}:00` })}
          className="min-h-11 rounded-2xl border border-border px-4 text-sm outline-none focus:border-blue"
        />
      </div>
      <div className="mt-5 flex flex-wrap gap-2">
        <button
          disabled={isUpdating}
          className="rounded-full bg-blue px-5 py-2.5 text-sm font-semibold text-white disabled:opacity-50"
        >
          Save New Time
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="rounded-full border border-border px-5 py-2.5 text-sm font-semibold text-slate-700"
        >
          Close
        </button>
      </div>
    </form>
  );
}

function NotificationCenter() {
  return (
    <div className="rounded-[1.75rem] border border-border bg-white p-5 shadow-soft">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-ink">Notifications</h2>
          <p className="mt-1 text-xs text-slate-500">Delivery will be connected later.</p>
        </div>
        <Bell className="h-5 w-5 text-blue" />
      </div>
      <div className="mt-5 space-y-3">
        {notifications.map((notification) => (
          <div key={notification.title} className="rounded-2xl border border-border bg-muted p-4">
            <div className="flex items-start gap-3">
              <span
                className={`mt-1 h-2.5 w-2.5 shrink-0 rounded-full ${
                  notification.tone === "green"
                    ? "bg-emerald-500"
                    : notification.tone === "red"
                      ? "bg-red-500"
                      : "bg-blue"
                }`}
              />
              <div>
                <p className="text-sm font-semibold text-ink">{notification.title}</p>
                <p className="mt-1 text-sm leading-6 text-slate-600">{notification.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-border bg-muted p-4">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-2 text-sm font-semibold text-ink">{value}</p>
    </div>
  );
}

function ProfileInput({
  icon: Icon,
  label,
  value,
  onChange,
  type = "text",
}: {
  icon: typeof UserRound;
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
}) {
  return (
    <label className="block">
      <span className="text-xs font-medium text-slate-500">{label}</span>
      <span className="mt-2 flex min-h-11 items-center gap-3 rounded-2xl border border-border px-4 focus-within:border-blue">
        <Icon className="h-4 w-4 text-slate-400" />
        <input
          required
          type={type}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          className="w-full bg-transparent text-sm outline-none"
        />
      </span>
    </label>
  );
}

function StatusBadge({ status }: { status: AppointmentStatus }) {
  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${statusStyles[status]}`}>
      {statusLabels[status]}
    </span>
  );
}

function ActionButton({
  children,
  onClick,
  disabled = false,
}: {
  children: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="rounded-full border border-border bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 transition hover:border-blue/30 hover:bg-blueSoft disabled:cursor-not-allowed disabled:opacity-50"
    >
      {children}
    </button>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-medium text-slate-400">{label}</p>
      <p className="mt-1 break-words text-sm leading-6 text-ink">{value}</p>
    </div>
  );
}

function formatTime(value: string) {
  return value.slice(0, 5);
}

function isTerminal(status: AppointmentStatus) {
  return ["completed", "cancelled", "no_show"].includes(status);
}
