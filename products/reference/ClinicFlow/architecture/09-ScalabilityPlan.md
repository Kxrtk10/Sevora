# 09 - Scalability Plan

## Scalability Mandate

ClinicFlow must scale from a single pilot clinic to multisite outpatient operations without premature complexity.

The MVP should optimize for:

- Product learning.
- Workflow reliability.
- Maintainability.
- Security.
- Measured operational improvement.

Do not introduce distributed architecture before the product has usage patterns that require it.

## Scaling Stages

### Stage 1: MVP Pilot

Target:

- 1 organization.
- 1-5 locations.
- Hundreds to low thousands of appointments per week.
- Manual entry or CSV import.
- SMS/email reminders.

Architecture:

- Modular monolith.
- Single PostgreSQL database.
- Redis-backed job queue.
- One web process.
- One worker process.

### Stage 2: Multisite Pilot

Target:

- 2-10 organizations.
- 5-50 locations.
- Thousands to tens of thousands of appointments per week.
- More dashboard usage.
- More communication volume.

Enhancements:

- Horizontal app scaling.
- Separate worker scaling.
- Read replicas for reporting if needed.
- Stronger tenant isolation review.
- Better import tooling.
- More robust metrics snapshots.

### Stage 3: Enterprise Healthcare Deployment

Target:

- Large clinic networks or hospital outpatient systems.
- EHR scheduling read integration.
- Strong SSO and enterprise security requirements.
- Higher reporting volume.

Enhancements:

- Dedicated tenant option for large customers.
- FHIR adapter.
- Event stream for analytics.
- Data warehouse export.
- Advanced audit reporting.
- More granular permissions.

### Stage 4: Product Platform

Target:

- Reusable operational modules for future Sevora healthcare or operations products.

Enhancements:

- Extract shared modules if justified.
- Shared communication service.
- Shared audit service.
- Shared metrics service.
- Shared integration framework.

## Scaling Dimensions

| Dimension | MVP Approach | Scaling Path |
| --- | --- | --- |
| Web traffic | Single container | Horizontal containers behind load balancer |
| Background jobs | One worker | Separate queues by job type and priority |
| Database reads | Primary database | Indexing, query optimization, read replicas |
| Database writes | Primary database | Batched writes, careful transactions, partitioning later |
| Communication volume | Provider adapter | Queue throttling, provider failover |
| Imports | Background jobs | Chunked imports, validation workers |
| Metrics | Snapshot tables | Dedicated analytics store later |
| Tenancy | Shared DB, org-scoped rows | Dedicated tenant database for large customers if needed |

## Performance Targets

Initial targets:

- Appointment command center loads in under 2 seconds for a daily schedule.
- Task board loads in under 2 seconds for assigned/location tasks.
- Patient intake link opens in under 2 seconds on mobile network.
- Reminder job dispatch begins within 1 minute of scheduled job time.
- Dashboard daily counts refresh within 5 minutes.
- API p95 under 500 ms for common reads after warmup.

Targets should be refined after real pilot workload.

## Queue Scaling

Use separate job queues or priority lanes for:

- Patient communication.
- Imports.
- Metrics refresh.
- Escalations.
- Webhook processing.

Communication jobs must not be blocked by large imports.

## Database Scaling

First optimize:

- Correct indexes.
- Query shape.
- Pagination.
- Snapshot metrics.
- Avoiding N+1 queries.
- Avoiding large JSON payloads.

Later options:

- Read replicas.
- Table partitioning for audit events and communication events.
- Dedicated reporting store.
- Customer-specific database for enterprise accounts.

## Caching Strategy

Use caching carefully.

Good candidates:

- Role permissions for current session.
- Configuration.
- Dashboard aggregate snapshots.

Avoid caching:

- Appointment readiness state unless invalidation is strong.
- Patient token validation.
- Sensitive patient details.

## Modularity For Reuse

The following modules should be designed as reusable Sevora primitives:

- Audit module.
- Communication adapter module.
- Task ownership module.
- Metrics snapshot module.
- Import validation module.
- RBAC module.

Reuse must not compromise ClinicFlow's healthcare-specific security requirements.

## When To Extract Services

Only consider service extraction when one of these is true:

- A module has independent scaling needs that harm the monolith.
- A module must be reused by another production product.
- A module has a separate security or compliance boundary.
- Team ownership requires independent deployment.

Likely first extraction candidates:

- Communications.
- Audit.
- Metrics.

Do not extract appointment, intake, task, and follow-up workflows early; they are tightly connected.

## Scalability Risks

- Overusing JSONB for operational state.
- Running dashboard aggregates live on every page load.
- Allowing imports to block communication jobs.
- Failing to index organization and location filters.
- Building microservices too early.
- Letting tenant-specific EHR logic leak into core domain.

## Acceptance Criteria

Scalability plan is ready when:

- MVP performance targets are defined.
- Queue separation strategy is documented.
- Database indexing strategy is defined.
- Metrics snapshot approach is accepted.
- Service extraction criteria are explicit.
- Tenant scaling path is documented.
