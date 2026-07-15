import {
  BarChart3,
  CalendarClock,
  CheckCircle2,
  LockKeyhole,
  MessageSquareText,
  Route,
  ShieldCheck,
  Sparkles,
  UsersRound,
} from "lucide-react";

import {
  Badge,
  ButtonLink,
  FeatureCard,
  MarketingInput,
  MarketingPageShell,
  PrincipleCard,
  ProductPreviewCard,
  SectionHeader,
} from "../components/marketing/MarketingComponents";
import {
  AdminMockup,
  ConciergeMockup,
  DoctorSchedulingMockup,
  PatientPortalMockup,
  ReceptionMockup,
} from "./Landing";

export function ProductPage() {
  return (
    <MarketingPageShell>
      <PageHero
        eyebrow="Product"
        title="A calmer operating layer for the clinic day."
        description="ClinicFlow brings appointment coordination, patient communication, queue visibility and operational intelligence into one premium workflow experience."
      />
      <section className="pb-20">
        <div className="mx-auto grid max-w-7xl gap-6 px-5 sm:px-6 lg:grid-cols-2 lg:px-8">
          <ProductPreviewCard
            title="Patient Portal"
            description="Clear intake, confirmation and arrival preparation."
          >
            <PatientPortalMockup />
          </ProductPreviewCard>
          <ProductPreviewCard
            title="Reception Dashboard"
            description="Front-desk clarity without operational noise."
          >
            <ReceptionMockup />
          </ProductPreviewCard>
          <ProductPreviewCard
            title="Admin Dashboard"
            description="A leadership view of patient flow and bottlenecks."
          >
            <AdminMockup />
          </ProductPreviewCard>
          <ProductPreviewCard
            title="Doctor Scheduling"
            description="Preparation and availability in one readable surface."
          >
            <DoctorSchedulingMockup />
          </ProductPreviewCard>
        </div>
      </section>
    </MarketingPageShell>
  );
}

export function FeaturesPage() {
  const features = [
    {
      icon: Sparkles,
      title: "AI Concierge",
      description: "Guides requests into the right operational path while preserving human oversight.",
    },
    {
      icon: CalendarClock,
      title: "Smart Scheduling",
      description: "Helps teams see appointment readiness, changes and staff coordination clearly.",
    },
    {
      icon: Route,
      title: "Queue Insights",
      description: "Makes waiting states and front-desk pressure visible before they compound.",
    },
    {
      icon: MessageSquareText,
      title: "Patient Communication",
      description: "Turns confirmations, intake and follow-up into measurable workflows.",
    },
    {
      icon: BarChart3,
      title: "Operational Intelligence",
      description: "Surfaces the metrics that explain flow, delay, workload and readiness.",
    },
    {
      icon: LockKeyhole,
      title: "Secure Foundation",
      description: "Built around access control, privacy and healthcare-grade accountability.",
    },
  ];

  return (
    <MarketingPageShell>
      <PageHero
        eyebrow="Features"
        title="Focused tools for the work around care."
        description="ClinicFlow avoids generic feature sprawl. Each surface exists to reduce ambiguity, improve coordination and make operations easier to manage."
      />
      <section className="pb-20">
        <div className="mx-auto grid max-w-7xl gap-4 px-5 sm:px-6 md:grid-cols-2 lg:grid-cols-3 lg:px-8">
          {features.map((feature, index) => (
            <FeatureCard
              key={feature.title}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              tone={index % 3 === 0 ? "blue" : index % 3 === 1 ? "teal" : "green"}
            />
          ))}
        </div>
      </section>
    </MarketingPageShell>
  );
}

export function AIConciergeMarketingPage() {
  return (
    <MarketingPageShell>
      <PageHero
        eyebrow="AI Concierge"
        title="Intelligent routing without replacing clinical judgement."
        description="The ClinicFlow AI Concierge is designed for operational clarity: collect intent, guide next steps and escalate to people when judgement matters."
      />
      <section className="pb-20">
        <div className="mx-auto grid max-w-7xl gap-10 px-5 sm:px-6 lg:grid-cols-[1fr_0.9fr] lg:px-8">
          <ProductPreviewCard
            title="AI Concierge"
            description="Transparent, human-first request handling."
          >
            <ConciergeMockup />
          </ProductPreviewCard>
          <div className="grid content-start gap-4">
            <PrincipleCard icon={ShieldCheck}>
              AI assists healthcare professionals. It never replaces clinical judgement.
            </PrincipleCard>
            <PrincipleCard icon={UsersRound}>
              Human escalation is always available when context, risk or judgement requires it.
            </PrincipleCard>
            <PrincipleCard icon={LockKeyhole}>
              Privacy and security are fundamental design constraints, not implementation details.
            </PrincipleCard>
          </div>
        </div>
      </section>
    </MarketingPageShell>
  );
}

export function AboutPage() {
  return (
    <MarketingPageShell>
      <PageHero
        eyebrow="About"
        title="ClinicFlow is built by Sevora."
        description="Sevora builds precise, long-term software for operationally serious organizations. ClinicFlow applies that standard to healthcare operations."
      />
      <section className="pb-20">
        <div className="mx-auto grid max-w-7xl gap-6 px-5 sm:px-6 lg:grid-cols-[0.9fr_1.1fr] lg:px-8">
          <div className="rounded-[2rem] border border-border bg-white p-8 shadow-soft">
            <Badge>Sevora</Badge>
            <p className="mt-6 text-3xl font-semibold tracking-[-0.04em] text-ink">
              Your Constant in an Evolving World.
            </p>
            <p className="mt-5 text-base leading-8 text-slate-600">
              ClinicFlow is part of the Sevora ecosystem: premium product systems designed with
              clarity, restraint, trust and operational excellence.
            </p>
          </div>
          <div className="grid gap-4">
            <PrincipleCard icon={ShieldCheck}>
              Every workflow is designed around better patient experiences and safer operational
              handoffs.
            </PrincipleCard>
            <PrincipleCard icon={LockKeyhole}>
              Patient privacy comes first, from product decisions to infrastructure choices.
            </PrincipleCard>
            <PrincipleCard icon={CheckCircle2}>
              Built for long-term healthcare partnerships, not short-term software demos.
            </PrincipleCard>
          </div>
        </div>
      </section>
    </MarketingPageShell>
  );
}

export function ContactPage() {
  return (
    <MarketingPageShell>
      <PageHero
        eyebrow="Contact"
        title="Start with a focused ClinicFlow conversation."
        description="Tell us where your clinic operations feel slow, manual or unclear. Sevora will help evaluate whether ClinicFlow is the right fit."
      />
      <section className="pb-20">
        <div className="mx-auto grid max-w-5xl gap-4 px-5 sm:px-6 lg:px-8">
          <div className="rounded-[2rem] border border-border bg-white p-6 shadow-product">
            <div className="grid gap-4 sm:grid-cols-2">
              <MarketingInput placeholder="Full name" aria-label="Full name" />
              <MarketingInput placeholder="Work email" type="email" aria-label="Work email" />
              <MarketingInput placeholder="Organization" aria-label="Organization" />
              <MarketingInput placeholder="Role" aria-label="Role" />
            </div>
            <textarea
              className="mt-4 min-h-32 w-full rounded-2xl border border-border bg-white px-4 py-3 text-sm text-ink outline-none transition placeholder:text-slate-400 focus:border-blue focus:ring-4 focus:ring-blue/10"
              placeholder="What operational workflow should ClinicFlow help you improve?"
              aria-label="Message"
            />
            <div className="mt-5 flex flex-wrap items-center justify-between gap-4">
              <p className="text-sm text-slate-500">
                This form is a visual placeholder. Use email for now.
              </p>
              <ButtonLink href="mailto:hello@sevora.com?subject=ClinicFlow%20Demo">
                Contact Sevora
              </ButtonLink>
            </div>
          </div>
        </div>
      </section>
    </MarketingPageShell>
  );
}

function PageHero({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description: string;
}) {
  return (
    <section className="pt-32">
      <div className="mx-auto max-w-5xl px-5 pb-16 text-center sm:px-6 lg:px-8">
        <SectionHeader eyebrow={eyebrow} title={title} description={description} />
      </div>
    </section>
  );
}
