import { useForm } from "react-hook-form";

type RegisterForm = {
  organization: string;
  email: string;
};

export function RegisterPage() {
  const { register } = useForm<RegisterForm>();

  return (
    <main className="flex min-h-screen items-center justify-center bg-muted px-6 text-ink">
      <section className="w-full max-w-md rounded-md border border-border bg-surface p-8 shadow-soft">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Setup</p>
        <h1 className="mt-3 text-2xl font-semibold">Register a ClinicFlow workspace</h1>
        <p className="mt-2 text-sm text-slate-600">
          Workspace registration is intentionally inactive until auth and tenant rules are approved.
        </p>
        <form className="mt-6 space-y-4">
          <label className="block text-sm font-medium text-slate-700">
            Organization
            <input
              {...register("organization")}
              className="mt-2 w-full rounded-md border border-border bg-white px-3 py-2 text-sm outline-none focus:border-accent"
              placeholder="Northside Ambulatory"
            />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            Admin email
            <input
              {...register("email")}
              className="mt-2 w-full rounded-md border border-border bg-white px-3 py-2 text-sm outline-none focus:border-accent"
              placeholder="admin@clinic.org"
              type="email"
            />
          </label>
          <button
            className="w-full rounded-md bg-accent px-4 py-2 text-sm font-medium text-white"
            type="button"
          >
            Prepare workspace
          </button>
        </form>
      </section>
    </main>
  );
}
