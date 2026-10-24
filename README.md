# OxHacks

Python (FastAPI) backend + plain HTML/CSS/JS frontend. The backend serves the frontend, so one command runs everything.

## Project layout

```
backend/
  app/main.py        FastAPI app: /api/* routes, serves frontend/ at /
  tests/             pytest tests
  requirements.txt   runtime deps
  requirements-dev.txt  dev deps (pytest, ruff)
frontend/
  index.html, style.css, app.js
```

## Setup

Requires Python 3.12.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp ../.env.example ../.env       # then fill in any values
```

## Run

```bash
cd backend
uvicorn app.main:app --reload
```

Open http://localhost:8000. API routes live under `/api` (e.g. http://localhost:8000/api/health); interactive docs at http://localhost:8000/docs.

## Test and lint

```bash
cd backend
pytest
ruff check . && ruff format --check .   # `ruff format .` to auto-fix formatting
```

CI runs these on every PR.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). AI agents: read [AGENTS.md](AGENTS.md).
