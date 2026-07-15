import {
  AlertTriangle,
  CalendarClock,
  CheckCircle2,
  Clock3,
  Filter,
  Loader2,
  Search,
  Stethoscope,
  UserCheck,
  XCircle,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

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
  is_active: boolean;
};

type Department = {
  id: string;
  name: string;
};

type EnrichedAppointment = Appointment & {
  doctor?: Doctor;
  department?: Department;
};

const apiBaseUrl = "http://127.0.0.1:8000";
const today = new Date().toISOString().slice(0, 10);

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

export function ReceptionDashboardPage() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [selectedDate, setSelectedDate] = useState(today);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<"all" | AppointmentStatus>("all");
  const [doctorFilter, setDoctorFilter] = useState("all");
  const [departmentFilter, setDepartmentFilter] = useState("all");
  const [selectedAppointmentId, setSelectedAppointmentId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingId, setUpdatingId] = useState<string | null>(null);

  const loadDashboard = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [appointmentResponse, doctorResponse, departmentResponse] = await Promise.all([
        fetch(`${apiBaseUrl}/api/v1/appointments?appointment_date=${selectedDate}&limit=200`),
        fetch(`${apiBaseUrl}/api/v1/doctors?limit=200`),
        fetch(`${apiBaseUrl}/api/v1/departments?limit=200`),
      ]);
      if (!appointmentResponse.ok || !doctorResponse.ok || !departmentResponse.ok) {
        throw new Error("Unable to load reception data.");
      }
      setAppointments((await appointmentResponse.json()) as Appointment[]);
      setDoctors((await doctorResponse.json()) as Doctor[]);
      setDepartments((await departmentResponse.json()) as Department[]);
    } catch {
      setError("Reception data is unavailable. Confirm the backend is running and try again.");
    } finally {
      setIsLoading(false);
    }
  }, [selectedDate]);

  useEffect(() => {
    const loader = window.setTimeout(() => {
      void loadDashboard();
    }, 0);
    return () => window.clearTimeout(loader);
  }, [loadDashboard]);

  async function updateStatus(appointment: Appointment, status: AppointmentStatus) {
    setUpdatingId(appointment.id);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/appointments/${appointment.id}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });
      if (!response.ok) {
        throw new Error("Status update failed.");
      }
      const updated = (await response.json()) as Appointment;
      setAppointments((current) =>
        current.map((item) => (item.id === appointment.id ? updated : item)),
      );
    } catch {
      setError("That status change is not available for this appointment.");
    } finally {
      setUpdatingId(null);
    }
  }

  async function cancelAppointment(appointment: Appointment) {
    setUpdatingId(appointment.id);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/appointments/${appointment.id}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error("Cancellation failed.");
      }
      const updated = (await response.json()) as Appointment;
      setAppointments((current) =>
        current.map((item) => (item.id === appointment.id ? updated : item)),
      );
    } catch {
      setError("This appointment could not be cancelled.");
    } finally {
      setUpdatingId(null);
    }
  }

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
        .sort((a, b) => a.appointment_start_time.localeCompare(b.appointment_start_time)),
    [appointments, departmentById, doctorById],
  );

  const filteredAppointments = enrichedAppointments.filter((appointment) => {
    const query = search.trim().toLowerCase();
    const matchesSearch =
      !query ||
      appointment.patient_name.toLowerCase().includes(query) ||
      appointment.id.toLowerCase().includes(query) ||
      appointment.doctor?.full_name.toLowerCase().includes(query);
    const matchesStatus = statusFilter === "all" || appointment.status === statusFilter;
    const matchesDoctor = doctorFilter === "all" || appointment.doctor_id === doctorFilter;
    const matchesDepartment =
      departmentFilter === "all" || appointment.department_id === departmentFilter;
    return matchesSearch && matchesStatus && matchesDoctor && matchesDepartment;
  });

  const selectedAppointment =
    enrichedAppointments.find((appointment) => appointment.id === selectedAppointmentId) ?? null;

  const summary = {
    total: enrichedAppointments.length,
    waiting: enrichedAppointments.filter((item) => item.status === "checked_in").length,
    confirmed: enrichedAppointments.filter((item) => item.status === "confirmed").length,
    completed: enrichedAppointments.filter((item) => item.status === "completed").length,
    cancelled: enrichedAppointments.filter((item) => item.status === "cancelled").length,
    averageWait: calculateAverageWait(enrichedAppointments),
  };

  return (
    <section className="mx-auto max-w-[1500px] space-y-6">
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
            Reception
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-[-0.04em] text-ink">
            Daily Patient Flow
          </h1>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            Manage arrivals, confirmations, cancellations and handoffs from one calm operational
            workspace.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <input
            type="date"
            value={selectedDate}
            onChange={(event) => setSelectedDate(event.target.value)}
            className="min-h-11 rounded-2xl border border-border bg-white px-4 text-sm text-ink outline-none focus:border-blue"
          />
          <button
            type="button"
            onClick={() => void loadDashboard()}
            className="min-h-11 rounded-2xl bg-blue px-5 text-sm font-semibold text-white"
          >
            Refresh
          </button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-6">
        <KpiCard label="Today's Appointments" value={summary.total} icon={CalendarClock} />
        <KpiCard label="Waiting Patients" value={summary.waiting} icon={Clock3} tone="amber" />
        <KpiCard label="Confirmed" value={summary.confirmed} icon={UserCheck} tone="green" />
        <KpiCard label="Completed" value={summary.completed} icon={CheckCircle2} />
        <KpiCard label="Cancelled" value={summary.cancelled} icon={XCircle} tone="red" />
        <KpiCard label="Average Waiting Time" value={`${summary.averageWait}m`} icon={Clock3} />
      </div>

      {error ? (
        <div className="rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      ) : null}

      <div className="grid gap-6 xl:grid-cols-[1fr_360px]">
        <div className="space-y-6">
          <div className="rounded-[1.75rem] border border-border bg-white p-5 shadow-soft">
            <div className="grid gap-3 lg:grid-cols-[1.4fr_repeat(3,1fr)]">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <input
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  placeholder="Search patient, doctor or appointment ID"
                  className="min-h-11 w-full rounded-2xl border border-border bg-muted pl-11 pr-4 text-sm outline-none focus:border-blue"
                />
              </div>
              <SelectFilter value={departmentFilter} onChange={setDepartmentFilter}>
                <option value="all">All Departments</option>
                {departments.map((department) => (
                  <option key={department.id} value={department.id}>
                    {department.name}
                  </option>
                ))}
              </SelectFilter>
              <SelectFilter value={doctorFilter} onChange={setDoctorFilter}>
                <option value="all">All Doctors</option>
                {doctors.map((doctor) => (
                  <option key={doctor.id} value={doctor.id}>
                    {doctor.full_name}
                  </option>
                ))}
              </SelectFilter>
              <SelectFilter value={statusFilter} onChange={(value) => setStatusFilter(value as typeof statusFilter)}>
                <option value="all">All Statuses</option>
                {Object.entries(statusLabels).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </SelectFilter>
            </div>
          </div>

          <div className="overflow-hidden rounded-[1.75rem] border border-border bg-white shadow-soft">
            <div className="flex items-center justify-between border-b border-border px-5 py-4">
              <div>
                <h2 className="text-base font-semibold text-ink">Today&apos;s Queue</h2>
                <p className="mt-1 text-xs text-slate-500">
                  Chronological patient flow for {selectedDate}
                </p>
              </div>
              <Filter className="h-4 w-4 text-slate-400" />
            </div>

            {isLoading ? (
              <div className="flex min-h-80 items-center justify-center gap-3 text-sm text-slate-500">
                <Loader2 className="h-4 w-4 animate-spin text-blue" />
                Loading reception queue
              </div>
            ) : filteredAppointments.length === 0 ? (
              <div className="grid min-h-80 place-items-center px-6 text-center">
                <div>
                  <CalendarClock className="mx-auto h-8 w-8 text-slate-300" />
                  <p className="mt-3 text-sm font-semibold text-ink">No appointments found</p>
                  <p className="mt-1 text-sm text-slate-500">
                    Adjust the date, filters or search query.
                  </p>
                </div>
              </div>
            ) : (
              <div className="divide-y divide-border">
                {filteredAppointments.map((appointment) => (
                  <AppointmentRow
                    key={appointment.id}
                    appointment={appointment}
                    isUpdating={updatingId === appointment.id}
                    isSelected={selectedAppointmentId === appointment.id}
                    onSelect={() => setSelectedAppointmentId(appointment.id)}
                    onStatus={(status) => void updateStatus(appointment, status)}
                    onCancel={() => void cancelAppointment(appointment)}
                  />
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <DoctorStatusPanel doctors={doctors} appointments={enrichedAppointments} />
          <AppointmentDrawer
            appointment={selectedAppointment}
            onClose={() => setSelectedAppointmentId(null)}
            onStatus={(appointment, status) => void updateStatus(appointment, status)}
            onCancel={(appointment) => void cancelAppointment(appointment)}
          />
        </div>
      </div>
    </section>
  );
}

function KpiCard({
  label,
  value,
  icon: Icon,
  tone = "blue",
}: {
  label: string;
  value: string | number;
  icon: typeof CalendarClock;
  tone?: "blue" | "green" | "amber" | "red";
}) {
  const toneClass = {
    blue: "bg-blueSoft text-blue",
    green: "bg-greenSoft text-emerald-700",
    amber: "bg-amber-50 text-amber-700",
    red: "bg-red-50 text-red-700",
  }[tone];

  return (
    <div className="rounded-[1.5rem] border border-border bg-white p-5 shadow-soft">
      <div className={`flex h-10 w-10 items-center justify-center rounded-2xl ${toneClass}`}>
        <Icon className="h-5 w-5" />
      </div>
      <p className="mt-5 text-2xl font-semibold tracking-[-0.03em] text-ink">{value}</p>
      <p className="mt-1 text-xs font-medium text-slate-500">{label}</p>
    </div>
  );
}

function SelectFilter({
  value,
  onChange,
  children,
}: {
  value: string;
  onChange: (value: string) => void;
  children: React.ReactNode;
}) {
  return (
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className="min-h-11 rounded-2xl border border-border bg-muted px-4 text-sm text-ink outline-none focus:border-blue"
    >
      {children}
    </select>
  );
}

function AppointmentRow({
  appointment,
  isUpdating,
  isSelected,
  onSelect,
  onStatus,
  onCancel,
}: {
  appointment: EnrichedAppointment;
  isUpdating: boolean;
  isSelected: boolean;
  onSelect: () => void;
  onStatus: (status: AppointmentStatus) => void;
  onCancel: () => void;
}) {
  return (
    <div
      className={`grid gap-4 px-5 py-4 transition hover:bg-muted/60 xl:grid-cols-[0.9fr_0.8fr_0.9fr_0.8fr_0.7fr_1.4fr] xl:items-center ${
        isSelected ? "bg-blueSoft/40" : ""
      }`}
    >
      <button type="button" onClick={onSelect} className="text-left">
        <p className="text-sm font-semibold text-ink">{appointment.patient_name}</p>
        <p className="mt-1 max-w-48 truncate text-xs text-slate-500">{appointment.id}</p>
      </button>
      <div>
        <p className="text-sm font-semibold text-ink">{formatTime(appointment.appointment_start_time)}</p>
        <p className="mt-1 text-xs text-slate-500">
          {formatTime(appointment.appointment_end_time)}
        </p>
      </div>
      <p className="text-sm text-slate-700">{appointment.doctor?.full_name ?? "Unassigned"}</p>
      <p className="text-sm text-slate-700">{appointment.department?.name ?? "Unknown"}</p>
      <StatusBadge status={appointment.status} />
      <div className="flex flex-wrap gap-2">
        <ActionButton disabled={isUpdating} onClick={() => onStatus("checked_in")}>
          Check In
        </ActionButton>
        <ActionButton disabled={isUpdating} onClick={() => onStatus("confirmed")}>
          Confirm
        </ActionButton>
        <ActionButton disabled={isUpdating} onClick={() => onStatus("pending")}>
          Reschedule
        </ActionButton>
        <ActionButton disabled={isUpdating} onClick={onCancel}>
          Cancel
        </ActionButton>
        <ActionButton disabled={isUpdating} onClick={() => onStatus("completed")}>
          Complete
        </ActionButton>
      </div>
    </div>
  );
}

function DoctorStatusPanel({
  doctors,
  appointments,
}: {
  doctors: Doctor[];
  appointments: EnrichedAppointment[];
}) {
  return (
    <div className="rounded-[1.75rem] border border-border bg-white p-5 shadow-soft">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-ink">Doctor Status</h2>
          <p className="mt-1 text-xs text-slate-500">Availability and waiting load</p>
        </div>
        <Stethoscope className="h-4 w-4 text-blue" />
      </div>
      <div className="mt-5 space-y-3">
        {doctors.map((doctor) => {
          const doctorAppointments = appointments.filter((item) => item.doctor_id === doctor.id);
          const waiting = doctorAppointments.filter((item) => item.status === "checked_in");
          const nextAppointment = doctorAppointments.find((item) =>
            ["pending", "confirmed", "checked_in"].includes(item.status),
          );
          const overloaded = waiting.length >= 3;
          return (
            <div key={doctor.id} className="rounded-2xl border border-border bg-muted p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-ink">{doctor.full_name}</p>
                  <p className="mt-1 text-xs text-slate-500">{doctor.specialization}</p>
                </div>
                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${
                    doctor.is_active ? "bg-greenSoft text-emerald-700" : "bg-slate-200 text-slate-600"
                  }`}
                >
                  {doctor.is_active ? "Available" : "Inactive"}
                </span>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-3 text-xs">
                <div className="rounded-xl bg-white p-3">
                  <p className="text-slate-500">Next</p>
                  <p className="mt-1 font-semibold text-ink">
                    {nextAppointment ? formatTime(nextAppointment.appointment_start_time) : "Clear"}
                  </p>
                </div>
                <div className="rounded-xl bg-white p-3">
                  <p className="text-slate-500">Waiting</p>
                  <p className="mt-1 font-semibold text-ink">{waiting.length}</p>
                </div>
              </div>
              {overloaded ? (
                <div className="mt-3 flex items-center gap-2 rounded-xl bg-amber-50 px-3 py-2 text-xs font-medium text-amber-700">
                  <AlertTriangle className="h-4 w-4" />
                  Schedule is overloaded
                </div>
              ) : null}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function AppointmentDrawer({
  appointment,
  onClose,
  onStatus,
  onCancel,
}: {
  appointment: EnrichedAppointment | null;
  onClose: () => void;
  onStatus: (appointment: Appointment, status: AppointmentStatus) => void;
  onCancel: (appointment: Appointment) => void;
}) {
  if (!appointment) {
    return (
      <div className="rounded-[1.75rem] border border-dashed border-border bg-white p-6 text-center shadow-soft">
        <p className="text-sm font-semibold text-ink">Appointment Details</p>
        <p className="mt-2 text-sm leading-6 text-slate-500">
          Select an appointment to view patient details, visit reason, history and available actions.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-[1.75rem] border border-border bg-white p-5 shadow-soft">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">
            Appointment Details
          </p>
          <h2 className="mt-2 text-xl font-semibold tracking-[-0.03em] text-ink">
            {appointment.patient_name}
          </h2>
        </div>
        <button type="button" onClick={onClose} className="text-sm font-semibold text-slate-500">
          Close
        </button>
      </div>

      <div className="mt-5 space-y-4">
        <Detail label="Patient Email" value={appointment.patient_email} />
        <Detail label="Patient Phone" value={appointment.patient_phone} />
        <Detail label="Reason for Visit" value={appointment.reason_for_visit} />
        <Detail label="Doctor" value={appointment.doctor?.full_name ?? "Unassigned"} />
        <Detail label="Department" value={appointment.department?.name ?? "Unknown"} />
        <Detail label="Notes" value={appointment.notes ?? "No notes recorded"} />
      </div>

      <div className="mt-5 rounded-2xl bg-muted p-4">
        <p className="text-sm font-semibold text-ink">Appointment History</p>
        <div className="mt-3 space-y-2 text-xs text-slate-600">
          <p>Created {formatDateTime(appointment.created_at)}</p>
          <p>Last updated {formatDateTime(appointment.updated_at)}</p>
          <p>Status is currently {statusLabels[appointment.status]}.</p>
        </div>
      </div>

      <div className="mt-5 flex flex-wrap gap-2">
        <ActionButton onClick={() => onStatus(appointment, "checked_in")}>Check In</ActionButton>
        <ActionButton onClick={() => onStatus(appointment, "confirmed")}>Confirm</ActionButton>
        <ActionButton onClick={() => onStatus(appointment, "completed")}>Complete</ActionButton>
        <ActionButton onClick={() => onCancel(appointment)}>Cancel</ActionButton>
      </div>
    </div>
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
      <p className="mt-1 text-sm leading-6 text-ink">{value}</p>
    </div>
  );
}

function calculateAverageWait(appointments: EnrichedAppointment[]) {
  const waiting = appointments.filter((item) => item.status === "checked_in");
  if (!waiting.length) return 0;
  const total = waiting.reduce((sum, appointment) => {
    const start = new Date(`${appointment.appointment_date}T${appointment.appointment_start_time}`);
    const minutes = Math.max(0, Math.round((Date.now() - start.getTime()) / 60000));
    return sum + minutes;
  }, 0);
  return Math.round(total / waiting.length);
}

function formatTime(value: string) {
  return value.slice(0, 5);
}

function formatDateTime(value: string) {
  return new Date(value).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
