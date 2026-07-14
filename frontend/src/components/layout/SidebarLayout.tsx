import {
  Bot,
  CalendarDays,
  Settings,
  ShieldCheck,
  Stethoscope,
  UserRound,
  UsersRound,
} from "lucide-react";
import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";

const navigation = [
  { label: "Patient", to: "/patient", icon: UserRound },
  { label: "Reception", to: "/reception", icon: UsersRound },
  { label: "Admin", to: "/admin", icon: ShieldCheck },
  { label: "Doctor", to: "/doctor", icon: Stethoscope },
  { label: "AI Concierge", to: "/ai-concierge", icon: Bot },
  { label: "Appointments", to: "/appointments", icon: CalendarDays },
  { label: "Settings", to: "/settings", icon: Settings },
];

export function SidebarLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-muted text-ink">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-border bg-surface px-4 py-5 lg:block">
        <NavLink to="/" className="mb-8 flex items-center gap-3 px-2">
          <span className="flex h-10 w-10 items-center justify-center rounded-md bg-accent text-sm font-semibold text-white">
            CF
          </span>
          <span>
            <span className="block text-sm font-semibold">ClinicFlow</span>
            <span className="block text-xs text-slate-500">Operations foundation</span>
          </span>
        </NavLink>

        <nav className="space-y-1">
          {navigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition",
                  isActive
                    ? "bg-accent text-white"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-950",
                ].join(" ")
              }
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="absolute bottom-5 left-4 right-4 rounded-md border border-border bg-muted p-3 text-xs text-slate-500">
          MVP foundation only. No clinical automation or appointment business logic is active.
        </div>
      </aside>

      <div className="lg:pl-72">{children}</div>
    </div>
  );
}
