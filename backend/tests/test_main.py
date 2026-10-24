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
    assert 'id="map"' in response.text


def test_stub_routes_cover_every_species():
    species = client.get("/data/species.json").json()["species"]
    routes = client.get("/data/migrations.geojson").json()
    oceans = client.get("/data/oceans.json").json()["oceans"]

    assert routes["type"] == "FeatureCollection"
    assert {item["id"] for item in species} == {
        feature["properties"]["species"] for feature in routes["features"]
    }
    assert {ocean["id"] for ocean in oceans} == {
        "pacific",
        "atlantic",
        "indian",
        "southern",
        "arctic",
    }
