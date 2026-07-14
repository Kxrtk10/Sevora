import { Link } from "react-router-dom";

export function LandingPage() {
  return (
    <main className="min-h-screen bg-muted px-6 py-10 text-ink">
      <section className="mx-auto flex min-h-[calc(100vh-5rem)] max-w-6xl flex-col justify-center">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">ClinicFlow</p>
        <h1 className="mt-5 max-w-3xl text-5xl font-semibold tracking-tight">
          Enterprise-grade healthcare operations foundation.
        </h1>
        <p className="mt-5 max-w-2xl text-base leading-7 text-slate-600">
          This implementation shell prepares ClinicFlow for secure, modular product development without
          shipping business logic before the domain is ready.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link to="/login" className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white">
            Sign in
          </Link>
          <Link
            to="/appointments"
            className="rounded-md border border-border bg-surface px-4 py-2 text-sm font-medium text-slate-700"
          >
            View shell
          </Link>
        </div>
      </section>
    </main>
  );
}
