import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-muted px-6 text-ink">
      <div className="max-w-lg rounded-md border border-border bg-surface p-8 shadow-soft">
        <p className="text-sm font-semibold text-slate-500">404</p>
        <h1 className="mt-3 text-2xl font-semibold">Page not found</h1>
        <p className="mt-3 text-sm text-slate-600">
          This ClinicFlow route has not been defined in the product shell.
        </p>
        <Link
          to="/"
          className="mt-6 inline-flex rounded-md bg-accent px-4 py-2 text-sm font-medium text-white"
        >
          Return home
        </Link>
      </div>
    </div>
  );
}
