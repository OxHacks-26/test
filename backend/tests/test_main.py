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


def test_species():
    response = client.get("/api/species")
    assert response.status_code == 200
    species = response.json()
    assert len(species) == 7
    assert {s["id"] for s in species} >= {"loggerhead", "green", "leatherback"}
    assert all({"common_name", "scientific_name", "color"} <= s.keys() for s in species)


def test_routes_cover_every_species():
    species_ids = {s["id"] for s in client.get("/api/species").json()}
    routes = client.get("/api/migrations").json()
    assert routes["type"] == "FeatureCollection"
    assert {f["properties"]["species"] for f in routes["features"]} == species_ids


def test_oceans():
    oceans = client.get("/api/oceans").json()
    assert {o["id"] for o in oceans} == {"pacific", "atlantic", "indian", "southern", "arctic"}
    assert all({"name", "bbox", "center"} <= o.keys() for o in oceans)


def route_ids(**params):
    response = client.get("/api/migrations", params=params)
    assert response.status_code == 200
    return {f["properties"]["id"] for f in response.json()["features"]}


def test_migrations_filter_by_species_and_ocean():
    assert route_ids(species="green") == {"green-south-atlantic-brazil-ascension"}
    assert all(i.startswith(("loggerhead", "green")) for i in route_ids(species="loggerhead,green"))
    assert "loggerhead-north-pacific-japan-baja" not in route_ids(ocean="atlantic")
    assert "green-south-atlantic-brazil-ascension" in route_ids(ocean="atlantic")


def test_migrations_filter_by_time():
    ascension = "green-south-atlantic-brazil-ascension"
    # Nov-Mar migration: in a January window, out of a July window.
    assert ascension in route_ids(**{"from": "2015-01-01", "to": "2015-01-31"})
    assert ascension not in route_ids(**{"from": "2015-07-01", "to": "2015-07-31"})
    # A whole-year window always includes it; a window before 1990 excludes it.
    assert ascension in route_ids(**{"from": "2015-01-01", "to": "2015-12-31"})
    assert route_ids(**{"from": "1950-01-01", "to": "1960-12-31"}) == set()
    assert client.get("/api/migrations", params={"from": "not-a-date"}).status_code == 422


def test_migrations_filter_by_depth():
    assert "loggerhead-north-pacific-japan-baja" in route_ids(depth=80)
    assert "green-south-atlantic-brazil-ascension" not in route_ids(depth=80)
