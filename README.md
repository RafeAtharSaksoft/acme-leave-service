# Acme HR Leave Service

Small internal service for requesting, approving and tracking employee leave.
FastAPI + SQLite, JWT bearer authentication.

## Run

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; use `source .venv/bin/activate` elsewhere
pip install -r requirements.txt
uvicorn app.main:app --port 8010
```

The SQLite database (`leave.db`) is created and seeded on first start. API docs at
http://localhost:8010/docs.

## Seed users

All seed users share the password `Welcome123!`.

| Email | Role | Team | Reports to |
|---|---|---|---|
| priya.nair@acme.example | hr_admin | 1 | - |
| dan.owens@acme.example | manager | 2 | Priya |
| maria.silva@acme.example | manager | 3 | Priya |
| alice.chen@acme.example | employee | 2 | Dan |
| bob.okafor@acme.example | employee | 2 | Dan |
| carol.evans@acme.example | employee | 3 | Maria |

## Reports

Managers can download a CSV of a team's leave at `GET /reports/team/{team_id}/leave.csv`.

## Configuration

| Variable | Purpose |
|---|---|
| `LEAVE_DB_PATH` | SQLite file path (default `leave.db`) |
| `LEAVE_JWT_SECRET` | Token signing key |

## Tests

```bash
pytest
```

Requirements are in `docs/requirements/leave-management.md`.
