type PageScaffoldProps = {
  eyebrow: string;
  title: string;
  description: string;
};

export function PageScaffold({ eyebrow, title, description }: PageScaffoldProps) {
  return (
    <section className="mx-auto max-w-6xl">
      <div className="rounded-md border border-border bg-surface p-6 shadow-soft">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">{eyebrow}</p>
        <h2 className="mt-3 text-2xl font-semibold text-ink">{title}</h2>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">{description}</p>
      </div>
    </section>
  );
}
