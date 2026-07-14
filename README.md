# SevoraOS

SevoraOS is the internal operating system for Sevora. It holds the company foundation, product portfolio, industry solution strategy, website plan, operating playbooks, reusable templates, and execution roadmap.

This repository is not a client project. It is the durable source of truth for how Sevora thinks, builds, sells, and scales.

## Structure

- [company](company/) - constitution, business blueprint, decision history, and operating playbook.
- [knowledge](knowledge/) - AI research, industry intelligence, opportunities, and research notes.
- [products](products/) - owned products, reference solutions, and engineering standards.
- [solutions](solutions/) - industry solution narratives that reference products instead of duplicating product docs.
- [website](website/) - site architecture, content strategy, page map, and animation direction.
- [branding](branding/) - brand voice, visual identity, design principles, and assets.
- [operations](operations/) - business development, finance, hiring, legal, and operating records.
- [templates](templates/) - reusable document templates for delivery and internal work.
- [scripts](scripts/) - utility scripts for maintaining SevoraOS.

## Sources of Truth

- [MASTER_ROADMAP.md](MASTER_ROADMAP.md) is the company execution roadmap.
- [NEXT_ACTIONS.md](NEXT_ACTIONS.md) is the next ten engineering tasks, ordered for immediate execution.
- [company/constitution](company/constitution/) defines Sevora's durable principles.
- [products/engineering](products/engineering/) defines the build standard.

## Contribution Standard

Keep documents specific, useful, and current. Link to related material instead of duplicating it. Move outdated strategy into the right archive or index only when it remains useful.

## ClinicFlow Development

ClinicFlow implementation starts from two top-level application folders:

- [frontend](frontend/) - React, TypeScript, Vite, TailwindCSS, React Router, TanStack Query, and React Hook Form.
- [backend](backend/) - FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, and Pydantic Settings.

### Prerequisites

- Node.js 22 or newer.
- Python 3.12 or newer.
- Docker and Docker Compose for containerized development.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Useful commands:

```bash
npm run build
npm run lint
npm run typecheck
npm run format
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The API is versioned under `/api/v1`. The health endpoint is:

```bash
GET http://localhost:8000/api/v1/health
```

### Docker

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

### Foundation Boundaries

This codebase is intentionally limited to the engineering foundation. It includes layouts, routing, configuration, database model shells, API versioning, health checks, Docker, linting, formatting, and authentication boundaries. ClinicFlow business logic, AI, and appointment workflows are intentionally not implemented yet.
