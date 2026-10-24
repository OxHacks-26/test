from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

from app import data

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app = FastAPI(title="OxHacks API")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/species")
def list_species() -> list[dict]:
    return data.species()


@app.get("/api/oceans")
def list_oceans() -> list[dict]:
    return data.oceans()


@app.get("/api/migrations")
def list_migrations(
    from_: Annotated[
        date | None, Query(alias="from", description="Window start (ISO date)")
    ] = None,
    to: Annotated[date | None, Query(description="Window end (ISO date)")] = None,
    species: Annotated[str | None, Query(description="Comma-separated species ids")] = None,
    ocean: Annotated[str | None, Query(description="Ocean id")] = None,
    depth: Annotated[float | None, Query(ge=0, description="Depth in metres")] = None,
) -> dict:
    species_ids = {s.strip() for s in species.split(",") if s.strip()} if species else None
    return data.migrations(start=from_, end=to, species_ids=species_ids, ocean=ocean, depth=depth)


# Raw data files, mostly for debugging; the frontend should use /api/*.
app.mount("/data", StaticFiles(directory=data.DATA_DIR), name="data")
# Must be mounted last so /api and /data take precedence.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
