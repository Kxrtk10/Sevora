# 10 - Engineering Roadmap

## Roadmap Mandate

This roadmap turns the approved Product Bible and architecture into implementation order. It avoids code-level detail and focuses on build sequencing.

Engineering must not implement features outside the MVP unless this roadmap is updated and approved.

## Phase 0: Architecture Approval

Outcome: implementation is safe to begin.

Tasks:

- Review and approve all architecture documents.
- Select final stack choices: ORM, auth provider, messaging provider, hosting provider, observability provider.
- Approve data classification and minimum necessary patient fields.
- Approve role and permission matrix.
- Approve patient token rules.
- Approve MVP success metrics.

Exit criteria:

- Architecture docs accepted.
- Technology choices locked for MVP.
- Security and deployment assumptions accepted.

## Phase 1: Product And Domain Specification

Outcome: engineers have unambiguous domain rules.

Tasks:

- Create PRD from Product Bible.
- Define workflow diagrams for appointment readiness, intake, task ownership, and follow-up.
- Define domain state machines.
- Define audit event catalog.
- Define OpenAPI contract draft.
- Define database schema draft.
- Define pilot data import format.

Exit criteria:

- PRD approved.
- API contract approved.
- Database schema approved.
- State transitions approved.

## Phase 2: Foundation

Outcome: secure app shell and core infrastructure.

Tasks:

- Set up application workspace.
- Configure environments.
- Configure database.
- Configure job queue.
- Configure auth.
- Implement RBAC foundation.
- Implement audit foundation.
- Implement observability foundation.
- Implement CI checks.

Exit criteria:

- Staff can authenticate.
- Role checks work.
- Audit events can be written.
- Health checks pass.
- Deployment pipeline reaches staging.

## Phase 3: Core Operational Data

Outcome: ClinicFlow can represent the clinic day.

Tasks:

- Implement organizations and locations.
- Implement users and location access.
- Implement patient registry.
- Implement appointment model.
- Implement appointment readiness state.
- Implement CSV/manual appointment import.

Exit criteria:

- Daily schedule can be loaded.
- Appointment readiness can be computed.
- Import errors are visible.
- Data is organization and location scoped.

## Phase 4: Appointment Command Center

Outcome: staff can manage appointment readiness.

Tasks:

- Build daily appointment command center.
- Add filters by date, location, provider, status, readiness.
- Add appointment detail view.
- Add workflow actions: confirm, cancel, request reschedule, mark arrived, mark no-show.
- Add audit for appointment state changes.

Exit criteria:

- Staff can run the daily schedule from ClinicFlow.
- Managers can see at-risk appointments.
- Every appointment state change is audited.

## Phase 5: Intake Workflow

Outcome: pre-visit readiness becomes measurable.

Tasks:

- Implement intake templates.
- Implement patient secure intake links.
- Implement intake submission tracking.
- Implement missing-item visibility.
- Implement staff review.
- Update appointment readiness based on intake status.

Exit criteria:

- Patient can complete intake through secure link.
- Staff can see incomplete intake.
- Appointment readiness updates automatically.
- Intake completion KPI is measurable.

## Phase 6: Communications

Outcome: reminders and patient responses are tracked.

Tasks:

- Implement messaging adapter.
- Implement reminder send workflow.
- Implement delivery status webhook.
- Implement inbound response webhook.
- Implement confirmation capture.
- Implement cancellation/reschedule request capture.
- Add communication audit events.

Exit criteria:

- Reminder can be sent.
- Delivery and response states are tracked.
- Patient responses route to staff queues.
- Communication failures are visible.

## Phase 7: Task Board

Outcome: operational work has ownership.

Tasks:

- Implement task model.
- Implement assignment, status, due dates, priority, aging.
- Implement task filters.
- Implement escalation.
- Create tasks from appointment, intake, communication, and follow-up workflows.

Exit criteria:

- No operational task is ownerless.
- Overdue work is visible.
- Task aging KPI is measurable.

## Phase 8: Follow-Up Tracker

Outcome: follow-up reliability is measurable.

Tasks:

- Implement follow-up model.
- Implement due dates and ownership.
- Implement patient response state.
- Implement missed follow-up queue.
- Implement completion tracking.
- Connect follow-ups to appointments and tasks.

Exit criteria:

- Follow-ups remain visible until completed or cancelled.
- Missed follow-ups are measurable.
- Follow-up completion KPI is measurable.

## Phase 9: Metrics And Dashboard

Outcome: buyer value is visible.

Tasks:

- Implement today's operational dashboard.
- Implement metric snapshots.
- Implement pilot success metrics.
- Implement trend reporting.
- Implement dashboard refresh jobs.

Exit criteria:

- Dashboard shows ready visits, incomplete intake, unconfirmed visits, open tasks, overdue follow-ups.
- Trends show no-show rate, intake completion, task aging, follow-up completion, response time.
- Pilot success criteria can be measured.

## Phase 10: Security, QA, And Pilot Readiness

Outcome: ClinicFlow can be safely piloted.

Tasks:

- Security review.
- Role and permission test coverage.
- Patient token abuse testing.
- Audit coverage review.
- Backup and restore test.
- Messaging failure test.
- Import failure test.
- Performance smoke test.
- Pilot runbook.

Exit criteria:

- Security checklist passed.
- Critical workflows tested.
- Production environment ready.
- Pilot runbook approved.

## Post-MVP Candidates

Only consider after pilot evidence:

- FHIR scheduling read integration.
- EHR write-back.
- Predictive no-show modeling.
- Prior authorization workflow.
- Call center integration.
- Multilingual communication.
- Enterprise analytics.
- AI operational summaries.

## Engineering Definition Of Done

Every completed feature must include:

- Product Bible alignment.
- API contract.
- Database migration if needed.
- Authorization checks.
- Audit events.
- Validation.
- Error handling.
- Tests for domain behavior.
- Observability.
- Documentation update.

## Roadmap Acceptance Criteria

The roadmap is approved when:

- It builds MVP value in the right order.
- It avoids postponed features.
- It supports immediate implementation after architecture approval.
- It preserves security and audit requirements.
- It makes pilot KPIs measurable before external launch.
