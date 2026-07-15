import { motion } from "framer-motion";
import type { ComponentType, InputHTMLAttributes, ReactNode } from "react";
import { Link, NavLink } from "react-router-dom";

type IconComponent = ComponentType<{ className?: string }>;

const navItems = [
  { label: "Home", to: "/" },
  { label: "Product", to: "/product" },
  { label: "Features", to: "/features" },
  { label: "About", to: "/about" },
  { label: "Contact", to: "/contact" },
];

export function Wordmark() {
  return (
    <Link to="/" className="group inline-flex items-center gap-3" aria-label="ClinicFlow home">
      <span className="flex h-9 w-9 items-center justify-center rounded-xl border border-blue/10 bg-white text-sm font-semibold text-blue shadow-soft">
        Cf
      </span>
      <span className="text-[1.05rem] font-semibold tracking-[-0.02em] text-ink">ClinicFlow</span>
    </Link>
  );
}

export function MarketingNav() {
  return (
    <header className="fixed left-0 right-0 top-0 z-50 border-b border-border/70 bg-white/88 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 sm:px-6 lg:px-8">
        <Wordmark />
        <nav className="hidden items-center gap-7 text-sm font-medium text-slate-600 lg:flex">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `transition hover:text-ink ${isActive ? "text-ink" : "text-slate-600"}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <Link
            to="/login"
            className="hidden rounded-full px-4 py-2 text-sm font-medium text-slate-600 transition hover:text-ink sm:inline-flex"
          >
            Sign in
          </Link>
          <Link
            to="/contact"
            className="rounded-full bg-blue px-4 py-2 text-sm font-semibold text-white shadow-product transition hover:bg-blue/90"
          >
            Book Demo
          </Link>
        </div>
      </div>
    </header>
  );
}

export function MarketingPageShell({ children }: { children: ReactNode }) {
  return (
    <main className="min-h-screen bg-muted text-ink">
      <MarketingNav />
      {children}
      <MarketingFooter />
    </main>
  );
}

export function ButtonLink({
  children,
  href,
  variant = "primary",
}: {
  children: ReactNode;
  href: string;
  variant?: "primary" | "secondary";
}) {
  const className =
    variant === "primary"
      ? "bg-blue text-white shadow-product hover:bg-blue/90"
      : "border border-border bg-white text-ink hover:border-blue/30 hover:bg-blueSoft/50";

  return (
    <a
      href={href}
      className={`inline-flex min-h-11 items-center justify-center rounded-full px-5 text-sm font-semibold transition ${className}`}
    >
      {children}
    </a>
  );
}

export function Badge({ children }: { children: ReactNode }) {
  return (
    <span className="inline-flex rounded-full border border-blue/15 bg-blueSoft px-3 py-1 text-xs font-semibold text-blue">
      {children}
    </span>
  );
}

export function SectionHeader({
  eyebrow,
  title,
  description,
  align = "center",
}: {
  eyebrow: string;
  title: string;
  description: string;
  align?: "center" | "left";
}) {
  const alignment = align === "center" ? "mx-auto text-center" : "";

  return (
    <div className={`${alignment} max-w-3xl`}>
      <Badge>{eyebrow}</Badge>
      <h2 className="mt-5 text-3xl font-semibold tracking-[-0.035em] text-ink sm:text-4xl lg:text-5xl">
        {title}
      </h2>
      <p className="mt-5 text-base leading-8 text-slate-600">{description}</p>
    </div>
  );
}

export function FeatureCard({
  icon: Icon,
  title,
  description,
  tone = "blue",
}: {
  icon: IconComponent;
  title: string;
  description: string;
  tone?: "blue" | "teal" | "green";
}) {
  const toneClass = {
    blue: "bg-blueSoft text-blue",
    teal: "bg-tealSoft text-teal-700",
    green: "bg-greenSoft text-emerald-700",
  }[tone];

  return (
    <motion.article
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="rounded-3xl border border-border bg-white p-6 shadow-soft"
    >
      <span className={`flex h-11 w-11 items-center justify-center rounded-2xl ${toneClass}`}>
        <Icon className="h-5 w-5" />
      </span>
      <h3 className="mt-5 text-lg font-semibold tracking-[-0.015em] text-ink">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-slate-600">{description}</p>
    </motion.article>
  );
}

export function ProductPreviewCard({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.45, ease: "easeOut" }}
      className="overflow-hidden rounded-[2rem] border border-border bg-white shadow-product"
    >
      <div className="border-b border-border px-5 py-4">
        <h3 className="text-base font-semibold text-ink">{title}</h3>
        <p className="mt-1 text-sm text-slate-500">{description}</p>
      </div>
      <div className="bg-muted p-4">{children}</div>
    </motion.article>
  );
}

export function PrincipleCard({
  icon: Icon,
  children,
}: {
  icon: IconComponent;
  children: ReactNode;
}) {
  return (
    <div className="flex items-start gap-4 rounded-3xl border border-border bg-white p-6 shadow-soft">
      <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-greenSoft text-emerald-700">
        <Icon className="h-5 w-5" />
      </span>
      <p className="text-sm font-medium leading-6 text-ink">{children}</p>
    </div>
  );
}

export function MarketingInput(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className="min-h-11 w-full rounded-2xl border border-border bg-white px-4 text-sm text-ink outline-none transition placeholder:text-slate-400 focus:border-blue focus:ring-4 focus:ring-blue/10"
    />
  );
}

export function MarketingFooter() {
  return (
    <footer className="border-t border-border bg-white">
      <div className="mx-auto grid max-w-7xl gap-8 px-5 py-10 sm:px-6 md:grid-cols-[1fr_auto] md:items-end lg:px-8">
        <div>
          <Wordmark />
          <p className="mt-3 max-w-md text-sm leading-6 text-slate-500">
            Helping Healthcare Flow Better. Built by Sevora with long-term healthcare partnerships
            in mind.
          </p>
        </div>
        <p className="text-sm italic text-slate-500">Your Constant in an Evolving World.</p>
      </div>
    </footer>
  );
}
