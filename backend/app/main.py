from pathlib import Path

from fastapi import FastAPI
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


# Must be mounted last so /api routes take precedence.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
