export function LoadingPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-muted px-6 text-ink">
      <div className="rounded-md border border-border bg-surface p-6 shadow-soft">
        <p className="text-sm font-medium">Loading ClinicFlow...</p>
        <p className="mt-1 text-sm text-slate-500">Preparing the workspace.</p>
      </div>
    </div>
  );
}
