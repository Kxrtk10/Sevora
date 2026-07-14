# Deployment Standards

Deployments should be repeatable, observable, and reversible.

## Standards

- Use environment-specific configuration and never commit secrets.
- Document required environment variables.
- Run migrations intentionally and with rollback awareness.
- Verify production health after deployment.
- Keep release notes focused on user-facing changes and operational risk.
- Prefer small, frequent releases over large, fragile releases.
