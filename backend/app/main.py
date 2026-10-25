import sys
from datetime import date
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from nicegui import ui

from app import data

REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DATA_DIR = REPO_ROOT / "frontend" / "data"
UI_DIR = REPO_ROOT / "ui"

app = FastAPI(title="OxHacks API")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/species")
def list_species() -> list[dict]:
    return data.species()


@app.get("/api/sources")
def list_sources() -> list[dict]:
    return data.sources()


@app.get("/api/oceans")
def list_oceans() -> list[dict]:
    return data.oceans()


@app.get("/api/years")
def list_years() -> list[int]:
    return data.observation_years()


@app.get("/api/predictions")
def list_predictions(
    species: Annotated[str | None, Query(description="Species id")] = None,
    year: Annotated[int | None, Query(description="Calendar year")] = None,
) -> dict:
    return data.predictions(species_id=species, year=year)


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
    year: Annotated[int | None, Query(description="Calendar year")] = None,
) -> dict:
    start, end = from_, to
    if year is not None:
        year_start, year_end = date(year, 1, 1), date(year, 12, 31)
        start = year_start if start is None else max(start, year_start)
        end = year_end if end is None else min(end, year_end)
    species_ids = {part.strip() for part in species.split(",") if part.strip()} if species else None
    return data.migrations(
        start=start,
        end=end,
        species_ids=species_ids or None,
        ocean=ocean,
    )


# Stub JSON stays at /data. The map is not the site: Turtle Tide in ui/ is the
# page at /, and it embeds the map from /map/.
app.mount("/data", StaticFiles(directory=FRONTEND_DATA_DIR), name="frontend-data")

if str(UI_DIR) not in sys.path:
    sys.path.insert(0, str(UI_DIR))
_ui_spec = spec_from_file_location("turtle_ui", UI_DIR / "app.py")
_turtle_ui = module_from_spec(_ui_spec)
sys.modules["turtle_ui"] = _turtle_ui
_ui_spec.loader.exec_module(_turtle_ui)

ui.run_with(app, title="Turtle Tide", show_welcome_message=False)
