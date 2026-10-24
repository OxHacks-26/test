from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

from app import data

REPO_ROOT = Path(__file__).resolve().parents[2]
MAP_DIR = REPO_ROOT / "map"
FRONTEND_DATA_DIR = REPO_ROOT / "frontend" / "data"

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


@app.get("/api/years")
def list_years() -> list[int]:
    return data.observation_years()


@app.get("/api/predictions")
def list_predictions() -> dict:
    return data.predictions()


@app.get("/api/depth-profiles")
def list_depth_profiles() -> dict:
    return data.depth_profiles()


@app.get("/api/migrations")
def list_migrations(
    from_: Annotated[
        date | None,
        Query(alias="from", description="Window start (ISO date)"),
    ] = None,
    to: Annotated[date | None, Query(description="Window end (ISO date)")] = None,
    species: Annotated[str | None, Query(description="Comma-separated species ids")] = None,
    ocean: Annotated[str | None, Query(description="Ocean id")] = None,
) -> dict:
    species_ids = {part.strip() for part in species.split(",") if part.strip()} if species else None
    return data.migrations(
        start=from_,
        end=to,
        species_ids=species_ids or None,
        ocean=ocean,
    )


# Must be mounted last so /api routes take precedence.
# The map page lives in map/ and is served at /. The stub JSON stays in
# frontend/data and is served at /data.
app.mount("/data", StaticFiles(directory=FRONTEND_DATA_DIR), name="frontend-data")
app.mount("/", StaticFiles(directory=MAP_DIR, html=True), name="map")
