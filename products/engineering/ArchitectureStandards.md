# Architecture Standards

Architecture must make Sevora products easier to evolve.

## Standards

- Define domain entities, workflows, and boundaries before implementation.
- Keep product modules loosely coupled and explicitly named.
- Use typed contracts for API, database, and integration boundaries.
- Isolate third-party services behind adapters.
- Avoid premature platform abstractions until at least two real products need the same capability.
- Record architecture decisions in an ADR when they affect future delivery.
