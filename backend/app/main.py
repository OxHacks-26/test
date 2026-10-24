from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app = FastAPI(title="OxHacks API")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Must be mounted last so /api routes take precedence.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
