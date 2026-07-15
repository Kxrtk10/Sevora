import { motion, type MotionValue, useScroll, useTransform } from "framer-motion";
import {
  ArrowDown,
  BarChart3,
  CalendarClock,
  CheckCircle2,
  ClipboardList,
  Clock3,
  Eye,
  HeartHandshake,
  LineChart,
  LockKeyhole,
  MessageSquareText,
  Route,
  ShieldCheck,
  Sparkles,
  UsersRound,
} from "lucide-react";
import { useRef } from "react";
import { Link } from "react-router-dom";

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

const challengeItems = [
  {
    icon: UsersRound,
    title: "Reception overload",
    text: "Front-desk teams coordinate calls, arrivals, forms, changes, and handoffs without a calm source of truth.",
  },
  {
    icon: ClipboardList,
    title: "Manual appointment work",
    text: "Scheduling decisions often happen across phones, portals, notes, and memory instead of one precise workflow.",
  },
  {
    icon: MessageSquareText,
    title: "Communication delays",
    text: "Patients wait for clarity while staff repeatedly chase confirmations, intake, and next steps.",
  },
  {
    icon: Clock3,
    title: "Unclear patient flow",
    text: "Small delays become waiting rooms, missed slots, duplicated work, and avoidable operational pressure.",
  },
];

const solutionCards = [
  {
    icon: CalendarClock,
    title: "Appointment Readiness",
    description: "A focused command center for requests, confirmations, preparation and changes.",
  },
  {
    icon: Route,
    title: "Smart Routing",
    description: "Clear operational paths from patient request to the right team member.",
  },
  {
    icon: Eye,
    title: "Queue Visibility",
    description: "Clear visibility into waiting states, routing, and reception workload.",
  },
  {
    icon: BarChart3,
    title: "Operational Intelligence",
    description: "Readable signals for leaders without turning the clinic day into a spreadsheet.",
  },
];

const workflowSteps = [
  {
    label: "Patient",
    detail: "A request begins with clear intent.",
  },
  {
    label: "AI Concierge",
    detail: "Questions are organized before staff attention is needed.",
  },
  {
    label: "Smart Routing",
    detail: "The right next step becomes visible.",
  },
  {
    label: "Reception",
    detail: "The front desk sees what needs action.",
  },
  {
    label: "Doctor",
    detail: "Clinical teams receive cleaner operational context.",
  },
  {
    label: "Follow-up",
    detail: "The loop closes with tracked next steps.",
  },
];

const trustPrinciples = [
  {
    icon: Sparkles,
    text: "AI assists healthcare professionals. It never replaces clinical judgement.",
  },
  {
    icon: HeartHandshake,
    text: "Human oversight remains essential whenever context, risk or judgement matters.",
  },
  {
    icon: LockKeyhole,
    text: "Patient privacy comes first, from product decisions to infrastructure choices.",
  },
  {
    icon: Eye,
    text: "Transparent operations help teams see ownership, status and next steps.",
  },
  {
    icon: ShieldCheck,
    text: "Built for long-term healthcare partnerships, not short-term software demos.",
  },
];

export function LandingPage() {
  const workflowRef = useRef<HTMLDivElement | null>(null);
  const { scrollYProgress } = useScroll({
    target: workflowRef,
    offset: ["start 72%", "end 32%"],
  });
  const pathScale = useTransform(scrollYProgress, [0, 1], [0.05, 1]);

  return (
    <MarketingPageShell>
      <HeroSection />
      <WorkflowSection pathScale={pathScale} workflowRef={workflowRef} />
      <ChallengeSection />
      <WhyClinicFlowSection />
      <ProductShowcaseSection />
      <TrustSection />
      <CTASection />
    </MarketingPageShell>
  );
}

function HeroSection() {
  return (
    <section className="relative overflow-hidden pt-28">
      <div className="absolute inset-x-0 top-0 h-[680px] bg-[linear-gradient(180deg,rgba(232,240,255,0.95),rgba(247,249,252,0))]" />
      <div className="relative mx-auto grid min-h-[calc(100vh-4rem)] max-w-7xl items-center gap-16 px-5 pb-24 sm:px-6 lg:grid-cols-[0.95fr_1.05fr] lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55, ease: "easeOut" }}
        >
          <h1 className="text-7xl font-semibold leading-[0.88] tracking-[-0.075em] text-ink sm:text-8xl lg:text-9xl">
            ClinicFlow
          </h1>
          <p className="mt-8 text-4xl font-semibold tracking-[-0.055em] text-ink sm:text-5xl lg:text-6xl">
            Helping Healthcare Flow Better.
          </p>
          <p className="mt-5 text-xl font-medium tracking-[-0.025em] text-blue">
            Where Smarter Operations Meet Better Care.
          </p>
          <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-600">
            An intelligent operations platform that helps clinics and hospitals streamline
            appointments, simplify patient communication and modernize front-desk operations,
            allowing healthcare professionals to focus on what matters most: patient care.
          </p>
          <div className="mt-9 flex flex-wrap gap-3">
            <ButtonLink href="#demo">Book a Demo</ButtonLink>
            <ButtonLink href="#workflow" variant="secondary">
              Explore ClinicFlow
            </ButtonLink>
          </div>
          <div className="mt-10 border-l border-border pl-5">
            <p className="text-sm font-semibold text-ink">A Sevora Product</p>
            <p className="mt-1 text-sm italic text-slate-500">
              Your Constant in an Evolving World.
            </p>
          </div>
        </motion.div>

        <HeroProductPreview />
      </div>
    </section>
  );
}

function WorkflowSection({
  pathScale,
  workflowRef,
}: {
  pathScale: MotionValue<number>;
  workflowRef: React.RefObject<HTMLDivElement | null>;
}) {
  return (
    <section id="workflow" ref={workflowRef} className="border-y border-border bg-white py-20">
      <div className="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8">
        <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr] lg:items-center">
          <SectionHeader
            eyebrow="How It Works"
            title="A clearer path through the clinic day."
            description="ClinicFlow explains work as it moves from patient intent to routed action, reception coordination, clinical handoff and follow-up."
            align="left"
          />
          <div className="relative">
            <motion.div
              className="absolute left-5 top-7 hidden h-[calc(100%-3.5rem)] w-px origin-top bg-blue md:block"
              style={{ scaleY: pathScale }}
            />
            <div className="space-y-3">
              {workflowSteps.map((step, index) => (
                <motion.div
                  key={step.label}
                  initial={{ opacity: 0, x: 16 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, margin: "-80px" }}
                  transition={{ duration: 0.42, delay: index * 0.04 }}
                  className="relative flex gap-4 rounded-3xl border border-border bg-muted p-4"
                >
                  <span className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl border border-blue/15 bg-white text-blue shadow-soft">
                    {index === workflowSteps.length - 1 ? (
                      <CheckCircle2 className="h-4 w-4" />
                    ) : (
                      <ArrowDown className="h-4 w-4" />
                    )}
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-ink">{step.label}</p>
                    <p className="mt-1 text-sm leading-6 text-slate-600">{step.detail}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function HeroProductPreview() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 22 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.65, ease: "easeOut", delay: 0.08 }}
      className="relative"
      aria-label="ClinicFlow premium product preview"
    >
      <div className="rounded-[2rem] border border-white bg-white/90 p-3 shadow-product backdrop-blur">
        <div className="overflow-hidden rounded-[1.5rem] border border-border bg-white">
          <div className="flex items-center justify-between border-b border-border px-5 py-4">
            <div>
              <p className="text-xs font-semibold uppercase text-slate-400">Reception overview</p>
              <p className="mt-1 text-sm font-semibold text-ink">Today&apos;s Clinic Flow</p>
            </div>
            <span className="rounded-full bg-greenSoft px-3 py-1 text-xs font-semibold text-emerald-700">
              24 ready visits
            </span>
          </div>
          <div className="grid gap-4 p-5 md:grid-cols-[0.85fr_1.15fr]">
            <div className="space-y-3">
              {["Confirmed", "Needs intake", "Follow-up due"].map((label, index) => (
                <div key={label} className="rounded-2xl border border-border bg-muted p-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-ink">{label}</p>
                    <p className="text-sm font-semibold text-blue">{[18, 7, 5][index]}</p>
                  </div>
                  <div className="mt-3 h-2 rounded-full bg-white">
                    <motion.div
                      className="h-2 rounded-full bg-blue"
                      initial={{ width: 0 }}
                      animate={{ width: `${[82, 48, 36][index]}%` }}
                      transition={{ duration: 0.9, delay: 0.2 + index * 0.1 }}
                    />
                  </div>
                </div>
              ))}
            </div>
            <div className="rounded-2xl border border-border bg-white p-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-semibold text-ink">Priority patient flow</p>
                <LineChart className="h-4 w-4 text-blue" />
              </div>
              <div className="mt-5 space-y-3">
                {["AI Concierge routed", "Reception reviewing", "Doctor schedule aligned"].map(
                  (item) => (
                    <div key={item} className="flex items-center gap-3 rounded-xl bg-muted p-3">
                      <span className="flex h-8 w-8 items-center justify-center rounded-full bg-blueSoft text-blue">
                        <CheckCircle2 className="h-4 w-4" />
                      </span>
                      <span className="text-sm font-medium text-slate-700">{item}</span>
                    </div>
                  ),
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function ChallengeSection() {
  return (
    <section className="border-y border-border bg-white py-20">
      <div className="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="The Challenge"
          title="Healthcare operations break down in the spaces between systems."
          description="ClinicFlow focuses on measurable operational pressure: reception load, appointment coordination, communication delay and patient flow."
        />
        <div className="mt-12 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {challengeItems.map((item) => (
            <FeatureCard
              key={item.title}
              icon={item.icon}
              title={item.title}
              description={item.text}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

function WhyClinicFlowSection() {
  return (
    <section className="py-20">
      <div className="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:items-start">
          <SectionHeader
            eyebrow="Why ClinicFlow"
            title="Designed for operational excellence, not software clutter."
            description="ClinicFlow is intentionally narrow: it helps teams understand what is happening, route what matters and coordinate work with confidence."
            align="left"
          />
          <div className="grid gap-4 sm:grid-cols-2">
            {solutionCards.map((item, index) => (
              <FeatureCard
                key={item.title}
                icon={item.icon}
                title={item.title}
                description={item.description}
                tone={index % 2 === 0 ? "blue" : "teal"}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function ProductShowcaseSection() {
  return (
    <section id="showcase" className="border-y border-border bg-white py-20">
      <div className="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8">
        <SectionHeader
          eyebrow="Product Showcase"
          title="Realistic previews of a calmer clinic day."
          description="Five product surfaces establish the ClinicFlow design standard: bright, precise, readable and built for high-trust operational work."
        />
        <div className="mt-12 grid gap-6 lg:grid-cols-2">
          <ProductPreviewCard
            title="Patient Portal"
            description="A simple place for readiness, confirmations and next steps."
          >
            <PatientPortalMockup />
          </ProductPreviewCard>
          <ProductPreviewCard
            title="Reception Dashboard"
            description="Front-desk load, waiting states and immediate action."
          >
            <ReceptionMockup />
          </ProductPreviewCard>
          <ProductPreviewCard
            title="Admin Dashboard"
            description="Operational intelligence for clinic leaders."
          >
            <AdminMockup />
          </ProductPreviewCard>
          <ProductPreviewCard
            title="AI Concierge"
            description="Guided routing that keeps people in control."
          >
            <ConciergeMockup />
          </ProductPreviewCard>
          <div className="lg:col-span-2">
            <ProductPreviewCard
              title="Doctor Scheduling"
              description="A clear schedule layer for availability, preparation and handoffs."
            >
              <DoctorSchedulingMockup />
            </ProductPreviewCard>
          </div>
        </div>
      </div>
    </section>
  );
}

function TrustSection() {
  return (
    <section className="py-20">
      <div className="mx-auto grid max-w-7xl gap-12 px-5 sm:px-6 lg:grid-cols-[0.78fr_1.22fr] lg:px-8">
        <SectionHeader
          eyebrow="Trust & Commitment"
          title="Built around people, privacy and long-term partnership."
          description="ClinicFlow should feel modern without asking healthcare teams to gamble with judgement, accountability or patient trust."
          align="left"
        />
        <div className="grid gap-4 sm:grid-cols-2">
          {trustPrinciples.map((principle) => (
            <PrincipleCard key={principle.text} icon={principle.icon}>
              {principle.text}
            </PrincipleCard>
          ))}
        </div>
      </div>
    </section>
  );
}

export function PatientPortalMockup() {
  return (
    <div className="rounded-2xl bg-white p-5">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-ink">Welcome, Maya</p>
          <p className="text-xs text-slate-500">Your cardiology visit is almost ready.</p>
        </div>
        <span className="rounded-full bg-greenSoft px-3 py-1 text-xs font-semibold text-emerald-700">
          82% complete
        </span>
      </div>
      <div className="mt-5 space-y-3">
        {["Confirm appointment", "Complete intake", "Review arrival instructions"].map(
          (item, index) => (
            <div key={item} className="flex items-center gap-3 rounded-xl border border-border p-3">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-blueSoft text-blue">
                {index + 1}
              </span>
              <span className="text-sm font-medium text-ink">{item}</span>
            </div>
          ),
        )}
      </div>
    </div>
  );
}

export function ReceptionMockup() {
  return (
    <div className="rounded-2xl bg-white p-5">
      <div className="grid gap-3 sm:grid-cols-3">
        {["Ready", "Needs intake", "Waiting"].map((label, index) => (
          <div key={label} className="rounded-xl bg-muted p-4">
            <p className="text-xs text-slate-500">{label}</p>
            <p className="mt-2 text-2xl font-semibold text-ink">{[24, 7, 5][index]}</p>
          </div>
        ))}
      </div>
      <div className="mt-4 rounded-xl border border-border p-4">
        <div className="flex items-center justify-between">
          <p className="text-sm font-semibold">Reception capacity</p>
          <p className="text-xs font-semibold text-blue">Healthy</p>
        </div>
        <div className="mt-3 h-2 rounded-full bg-blueSoft">
          <div className="h-2 w-3/4 rounded-full bg-blue" />
        </div>
      </div>
    </div>
  );
}

export function AdminMockup() {
  return (
    <div className="rounded-2xl bg-white p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-ink">Operational trend</p>
        <BarChart3 className="h-4 w-4 text-blue" />
      </div>
      <div className="mt-6 flex h-36 items-end gap-3">
        {[42, 64, 58, 78, 70, 88, 82].map((height) => (
          <div key={height} className="flex flex-1 items-end rounded-full bg-blueSoft">
            <div className="w-full rounded-full bg-blue" style={{ height: `${height}%` }} />
          </div>
        ))}
      </div>
    </div>
  );
}

export function ConciergeMockup() {
  return (
    <div className="rounded-2xl bg-white p-5">
      <div className="flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-tealSoft text-teal-700">
          <Sparkles className="h-5 w-5" />
        </span>
        <div>
          <p className="text-sm font-semibold text-ink">ClinicFlow Concierge</p>
          <p className="text-xs text-slate-500">Routes requests with transparent handoff.</p>
        </div>
      </div>
      <div className="mt-5 space-y-3">
        <div className="rounded-2xl bg-muted p-4 text-sm text-slate-600">
          I need to reschedule my appointment.
        </div>
        <div className="rounded-2xl bg-blueSoft p-4 text-sm text-blue">
          I can route this to reception and include your preferred time window.
        </div>
      </div>
    </div>
  );
}

export function DoctorSchedulingMockup() {
  return (
    <div className="grid gap-4 rounded-2xl bg-white p-5 md:grid-cols-[0.8fr_1.2fr]">
      <div className="rounded-2xl bg-muted p-4">
        <p className="text-sm font-semibold text-ink">Dr. Rao</p>
        <p className="mt-1 text-xs text-slate-500">Cardiology - morning session</p>
        <div className="mt-5 space-y-2">
          {["9:00", "9:30", "10:00", "10:30"].map((time, index) => (
            <div key={time} className="flex items-center justify-between rounded-xl bg-white px-3 py-2">
              <span className="text-sm font-medium text-ink">{time}</span>
              <span className="text-xs text-slate-500">{index === 1 ? "Review" : "Ready"}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="rounded-2xl border border-border p-4">
        <p className="text-sm font-semibold text-ink">Preparation queue</p>
        <div className="mt-4 space-y-3">
          {["Intake complete", "Reception handoff", "Follow-up plan pending"].map((item) => (
            <div key={item} className="flex items-center gap-3 rounded-xl bg-muted p-3">
              <CheckCircle2 className="h-4 w-4 text-blue" />
              <span className="text-sm text-slate-700">{item}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function CTASection() {
  return (
    <section id="demo" className="py-20">
      <div className="mx-auto max-w-5xl px-5 text-center sm:px-6 lg:px-8">
        <Badge>Built by Sevora</Badge>
        <h2 className="mt-5 text-4xl font-semibold tracking-[-0.05em] text-ink sm:text-6xl">
          Ready to Modernize Your Clinic?
        </h2>
        <p className="mx-auto mt-5 max-w-2xl text-base leading-8 text-slate-600">
          Book a focused conversation about your appointment flow, patient communication and
          front-desk operations.
        </p>
        <div className="mx-auto mt-8 grid max-w-xl gap-3 sm:grid-cols-[1fr_auto]">
          <MarketingInput placeholder="work email" type="email" aria-label="Work email" />
          <ButtonLink href="mailto:hello@sevora.com?subject=ClinicFlow%20Demo">
            Book a Demo
          </ButtonLink>
        </div>
        <div className="mt-5">
          <Link to="/contact" className="text-sm font-semibold text-blue transition hover:text-blue/80">
            Contact Sevora
          </Link>
        </div>
      </div>
    </section>
  );
}
