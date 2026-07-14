import { Moon, Sun } from "lucide-react";
import { Link } from "react-router-dom";

import { useTheme } from "../../app/providers/theme-context";

export function TopNavigation() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-border bg-surface/95 px-6 backdrop-blur lg:px-8">
      <div>
        <p className="text-xs font-medium uppercase tracking-[0.16em] text-slate-500">ClinicFlow</p>
        <h1 className="text-base font-semibold text-ink">Enterprise healthcare operations</h1>
      </div>

      <div className="flex items-center gap-3">
        <Link
          to="/appointments"
          className="hidden rounded-md border border-border px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-muted md:inline-flex"
        >
          Command Center
        </Link>
        <button
          type="button"
          onClick={toggleTheme}
          className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-border text-slate-600 transition hover:bg-muted"
          aria-label="Toggle theme"
        >
          {theme === "light" ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
        </button>
      </div>
    </header>
  );
}
