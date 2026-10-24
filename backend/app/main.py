from pathlib import Path

from fastapi import FastAPI
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


# Must be mounted last so /api routes take precedence.
# The map page lives in map/ and is served at /. The stub JSON stays in
# frontend/data and is served at /data.
app.mount("/data", StaticFiles(directory=FRONTEND_DATA_DIR), name="frontend-data")
app.mount("/", StaticFiles(directory=MAP_DIR, html=True), name="map")
