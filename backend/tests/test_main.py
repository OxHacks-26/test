from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_serves_frontend():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_species():
    response = client.get("/api/species")
    assert response.status_code == 200
    species = response.json()
    assert len(species) == 7
    assert {s["id"] for s in species} >= {"loggerhead", "green", "leatherback"}
    assert all({"common_name", "scientific_name", "color"} <= s.keys() for s in species)
