# 02 - Technology Stack

## Technology Principles

ClinicFlow needs boring, secure, maintainable technology. The MVP should prove operational value, not framework novelty.

Selection principles:

- Prefer widely adopted tools with strong healthcare security posture.
- Keep the stack simple enough for a small team to operate.
- Use TypeScript end to end for shared contracts and maintainability.
- Use relational data as the system of record.
- Isolate vendors behind adapters.
- Avoid technology that forces deep EHR integration before product value is proven.

## Recommended Stack

| Layer | Recommendation | Justification |
| --- | --- | --- |
| Frontend | Next.js with React and TypeScript | Strong ecosystem, server-rendering options, clean routing, reusable UI patterns, good fit for staff dashboards and patient links. |
| Backend | NestJS with TypeScript | Modular architecture, dependency injection, guards/interceptors, clean service boundaries, good fit for a modular monolith. |
| API Style | REST-first with OpenAPI | Clear, inspectable, easy for dashboards and future integrations; GraphQL is unnecessary for MVP. |
| Database | PostgreSQL | Strong relational integrity, JSONB support for flexible checklist fields, mature security, strong indexing. |
| ORM / Query Layer | Prisma or Drizzle | Type-safe data access. Choose one during implementation based on team preference; do not mix. |
| Background Jobs | BullMQ with Redis | Reliable reminder sending, CSV imports, KPI refreshes, retry handling, delayed jobs. |
| Cache / Queue Store | Redis | Queue backend and short-lived cache for operational dashboards. |
| Authentication | Auth.js, Clerk, WorkOS, or custom OIDC integration depending on pilot | Pilot constraints determine buyer SSO needs. Architecture must support OIDC/SAML later. |
| Authorization | Application-level RBAC with scoped organization/location permissions | Required for clinic roles and minimum necessary access. |
| Messaging | Twilio SendGrid or equivalent provider behind adapter | SMS/email reminders are core MVP workflows. Adapter prevents vendor lock-in. |
| File Storage | S3-compatible object storage | Secure storage for import files and generated reports if needed. |
| Observability | OpenTelemetry-compatible tracing, structured logs, uptime monitoring | Required for operational reliability and support. |
| Deployment | Containerized app on managed cloud platform | Predictable deploys, environment parity, simple scaling. |
| Infrastructure | Terraform later; managed platform configuration first | Do not overbuild infrastructure before pilot. Keep production reproducible. |

## Frontend Stack Detail

### Recommended

- Next.js.
- React.
- TypeScript.
- Tailwind CSS or a component system built on accessible primitives.
- React Hook Form or equivalent for forms.
- Zod or similar schema validation shared with API contracts where appropriate.

### Why

ClinicFlow needs dense operational screens:

- Daily appointment command center.
- Intake readiness lists.
- Task board.
- Follow-up queues.
- Manager dashboard.

React and TypeScript support reusable workflow components. Next.js supports both staff authenticated routes and patient-facing secure links in one app.

### Constraints

- Do not optimize for marketing visuals.
- Do not build a native mobile app for MVP.
- Patient links must be mobile-friendly, but the staff product should prioritize desktop and tablet workflows.

## Backend Stack Detail

### Recommended

- NestJS modular monolith.
- REST controllers.
- Application services per module.
- Domain services for workflows.
- Repository layer for database access.
- Background job processors for reminders, imports, metrics, and escalations.

### Why

NestJS gives enforced structure without prematurely splitting services. This matters because ClinicFlow must be maintainable as modules grow:

- Appointments.
- Intake.
- Communications.
- Tasks.
- Follow-ups.
- Metrics.
- Audit.
- Integrations.

## Database Stack Detail

Use PostgreSQL as the primary system of record.

Recommended extensions and features:

- UUID primary keys.
- Native timestamp with timezone.
- JSONB only for configurable intake fields and external payload snapshots.
- Partial indexes for open tasks, pending follow-ups, incomplete intake, and today's appointments.
- Row-level access constraints at the application layer first; database row-level security can be added for stronger isolation later.

Do not use a document database for the MVP. The core ClinicFlow data is relational and audit-heavy.

## Background Processing

Use background jobs for:

- Reminder scheduling.
- SMS/email sending.
- Retrying failed communications.
- CSV import processing.
- KPI aggregation.
- Task escalation.
- Follow-up due-state refresh.

Jobs must be idempotent. Every job must have:

- Job type.
- Organization ID.
- Correlation ID.
- Retry policy.
- Failure state.
- Audit or operational log entry when user-visible.

## API Style

REST-first is the correct default.

Reasons:

- Easy to document with OpenAPI.
- Easy for future hospital IT teams to inspect.
- Sufficient for CRUD plus workflow actions.
- Simpler authorization and audit boundaries than GraphQL.

Use explicit workflow endpoints for state changes, not generic patch endpoints for everything.

Examples of endpoint categories:

- Organizations.
- Users.
- Patients.
- Appointments.
- Intake.
- Communications.
- Tasks.
- Follow-ups.
- Metrics.
- Imports.
- Audit.

## AI Technology Position

AI is not part of core MVP behavior.

If any AI enters the system later, use it only for:

- Operational summarization.
- Drafting staff-facing messages for human approval.
- Classifying inbound non-clinical responses.
- Explaining workflow bottlenecks.

Use provider abstraction from day one, but do not ship autonomous AI workflows.

## Integration Stack

### MVP

- Manual entry.
- CSV import.
- CSV export.
- Messaging provider integration.

### Later

- FHIR adapter.
- SMART on FHIR launch support.
- EHR scheduling read integration.
- Optional EHR write-back after pilot proof.

Keep integration code in adapter modules. Do not allow EHR-specific assumptions to leak into the core domain.

## Environments

Minimum environments:

- Local development.
- Preview/staging.
- Production.

Each environment must have separate:

- Database.
- Redis instance.
- Messaging credentials.
- Object storage.
- Secrets.
- Auth configuration.

## Technology Decisions To Make Before Build

The architecture recommends the categories above. Implementation must choose:

- Prisma vs Drizzle.
- Auth provider for MVP.
- Messaging provider.
- Hosting target.
- Object storage provider.
- Observability provider.

Selection should be based on pilot needs, security requirements, and team familiarity.
