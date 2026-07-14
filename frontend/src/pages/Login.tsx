import { useForm } from "react-hook-form";

type LoginForm = {
  email: string;
};

export function LoginPage() {
  const { register } = useForm<LoginForm>();

  return (
    <main className="flex min-h-screen items-center justify-center bg-muted px-6 text-ink">
      <section className="w-full max-w-md rounded-md border border-border bg-surface p-8 shadow-soft">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Access</p>
        <h1 className="mt-3 text-2xl font-semibold">Sign in to ClinicFlow</h1>
        <p className="mt-2 text-sm text-slate-600">
          Authentication architecture is prepared. Login behavior will be implemented later.
        </p>
        <form className="mt-6 space-y-4">
          <label className="block text-sm font-medium text-slate-700">
            Work email
            <input
              {...register("email")}
              className="mt-2 w-full rounded-md border border-border bg-white px-3 py-2 text-sm outline-none focus:border-accent"
              placeholder="name@clinic.org"
              type="email"
            />
          </label>
          <button
            className="w-full rounded-md bg-accent px-4 py-2 text-sm font-medium text-white"
            type="button"
          >
            Continue
          </button>
        </form>
      </section>
    </main>
  );
}
