# 05 - Authentication

## Authentication Mandate

ClinicFlow handles healthcare operations and may handle PHI. Authentication must be secure enough for hospital review while remaining practical for the MVP.

The Product Bible requires:

- Role-based permissions.
- Minimum necessary access.
- Activity logs for staff and patient communication changes.
- Patient-facing intake links without building a native patient app.

## User Types

| User Type | Authentication Method | Notes |
| --- | --- | --- |
| Clinic staff | Email/password with MFA or OIDC/SAML depending on pilot | Staff must access authenticated app. |
| Clinic manager | Same as staff, elevated permissions | Access to dashboard and reports. |
| Organization admin | Same as staff, admin permissions | Manages users, roles, locations, templates. |
| Sevora support | Separate support role with strict audit | Access only when contractually allowed. |
| Patient | Secure one-time or short-lived token link | No patient account in MVP. |

## Recommended MVP Approach

Use a managed authentication provider if the first pilot does not require custom enterprise SSO.

Acceptable provider categories:

- OIDC-capable managed auth.
- SAML/OIDC enterprise auth provider.
- Healthcare-ready identity provider if pilot demands it.

Why:

- Faster secure implementation.
- MFA support.
- Session management.
- Password reset.
- Future enterprise SSO path.

Do not build custom password storage unless absolutely required.

## Authorization Model

Use RBAC with organization and location scoping.

### Roles

| Role | Permissions |
| --- | --- |
| Admin | Manage users, locations, templates, settings, all operational data. |
| Manager | View all operational workflows and dashboards for assigned locations. |
| Scheduler | Manage appointments, reminders, confirmations, reschedule requests. |
| Front Desk | Manage check-in readiness, intake state, communication queues. |
| MA / Nurse | Manage assigned tasks and follow-ups, view relevant patient operational info. |
| Care Coordinator | Manage follow-ups and patient communication queues. |
| Read Only | View operational data without state changes. |
| Support | Limited support access with explicit audit and approval. |

### Scope Rules

- Every user belongs to one organization.
- Every user has access to one or more locations.
- Role permissions apply only within assigned organization and locations.
- Patient links are scoped to a single patient action and do not grant staff access.

## Permission Matrix

| Capability | Admin | Manager | Scheduler | Front Desk | MA / Nurse | Care Coordinator | Read Only |
| --- | --- | --- | --- | --- | --- | --- | --- |
| View appointments | Yes | Yes | Yes | Yes | Assigned/location | Assigned/location | Yes |
| Create appointment | Yes | Yes | Yes | Limited | No | No | No |
| Change appointment status | Yes | Yes | Yes | Yes | Limited | No | No |
| Send reminder | Yes | Yes | Yes | Yes | No | Limited | No |
| Manage intake | Yes | Yes | Limited | Yes | Limited | No | No |
| Manage tasks | Yes | Yes | Assigned/location | Assigned/location | Assigned | Assigned | No |
| Manage follow-ups | Yes | Yes | No | Limited | Assigned | Yes | No |
| View dashboard | Yes | Yes | Limited | Limited | Limited | Limited | Yes |
| Manage users | Yes | No | No | No | No | No | No |
| View audit | Yes | Yes | No | No | No | No | No |

Implementation can refine role names after discovery, but the permission boundaries must remain.

## Patient Link Authentication

MVP does not require patient accounts.

Use secure token links for:

- Intake submission.
- Appointment confirmation.
- Cancellation request.
- Reschedule request.

Token requirements:

- Random, high-entropy, non-guessable.
- Scoped to one patient action or appointment.
- Expiration window.
- Single-use where appropriate.
- Revocable.
- No sensitive patient data in URL.
- Rate-limited.

Patient link pages should display only the minimum data needed for confirmation and intake completion.

## Session Requirements

Staff sessions must support:

- Secure cookies.
- Short idle timeout.
- Absolute session lifetime.
- MFA for privileged roles.
- Device/session revocation.
- CSRF protection where applicable.
- SameSite cookie policy.

## Support Access

Sevora support access must be:

- Disabled by default.
- Granted per organization.
- Time-limited.
- Audited.
- Visible to organization admins when appropriate.

Support users must not be able to silently inspect patient data.

## Authentication Events To Audit

Audit:

- Login success.
- Login failure threshold exceeded.
- MFA enrollment or change.
- Password reset.
- User invitation.
- Role change.
- Location access change.
- Support access grant.
- Patient token creation.
- Patient token use.
- Patient token expiration or revocation.

## Future SSO

Architecture must support:

- OIDC.
- SAML.
- SCIM provisioning later if enterprise pilots require it.

Do not implement SCIM in MVP unless required by a signed pilot.

## Acceptance Criteria

Authentication is ready when:

- Staff auth provider is selected.
- MFA policy is defined.
- Role and location access rules are implemented in design.
- Patient token flow is specified.
- Audit events are mapped.
- Support access policy is documented.
