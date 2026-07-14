import { Link, useRouteError } from "react-router-dom";

export function ErrorPage() {
  const error = useRouteError();
  const message = error instanceof Error ? error.message : "Something went wrong.";

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted px-6 text-ink">
      <div className="max-w-lg rounded-md border border-border bg-surface p-8 shadow-soft">
        <p className="text-sm font-semibold text-red-600">Application error</p>
        <h1 className="mt-3 text-2xl font-semibold">ClinicFlow could not load this view.</h1>
        <p className="mt-3 text-sm text-slate-600">{message}</p>
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
