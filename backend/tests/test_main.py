import json
from datetime import date
from pathlib import Path

from fastapi.testclient import TestClient

from app.data import months_in_window
from app.main import app

client = TestClient(app)
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load(name):
    return json.loads((DATA_DIR / name).read_text())


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
    assert {item["id"] for item in species} >= {"loggerhead", "green", "leatherback"}
    assert all({"common_name", "scientific_name", "colour"} <= item.keys() for item in species)


def test_species_depth_window_has_textboxes_and_no_diet():
    species = client.get("/api/species").json()
    topics = {"Habitat", "Population and extinction risk", "Life expectancy"}
    for item in species:
        assert _DIET_KEYS_ABSENT(item)
        assert {box["topic"] for box in item["textboxes"]} == topics
        assert all(box["text"] for box in item["textboxes"])
        served = " ".join(item["facts"]).lower()
        assert "prey" not in served
        assert "seagrasses and algae" not in served
        marks = {mark["id"]: mark["depth_m"] for mark in item["depth_marks"]}
        assert marks["shallow"] == item["depth_range_m"]["min"]
        assert marks["deep"] == item["depth_range_m"]["max"]


def _DIET_KEYS_ABSENT(item):
    return {"diet", "food", "foods", "prey", "food_icons", "diet_icons"}.isdisjoint(item)


def test_migrations():
    response = client.get("/api/migrations")
    assert response.status_code == 200
    routes = response.json()
    assert routes["type"] == "FeatureCollection"
    assert len(routes["features"]) == 7
    assert {feature["properties"]["species_id"] for feature in routes["features"]} == {
        item["id"] for item in client.get("/api/species").json()
    }


def test_migrations_filter_by_species_and_date():
    green = client.get("/api/migrations", params={"species": "green"}).json()["features"]
    assert len(green) == 1
    assert green[0]["properties"]["species_id"] == "green"

    march = client.get(
        "/api/migrations", params={"from": "2025-03-01", "to": "2025-03-31", "species": "green"}
    ).json()["features"]
    assert len(march) == 1
    # The checked-in demo positions are in 2025, so an observation year has no route.
    assert (
        client.get("/api/migrations", params={"from": "2015-01-01", "to": "2015-12-31"}).json()[
            "features"
        ]
        == []
    )
    assert client.get("/api/migrations", params={"from": "not-a-date"}).status_code == 422


def test_migrations_does_not_filter_by_depth():
    assert len(client.get("/api/migrations", params={"depth": 4100}).json()["features"]) == 7


def test_years_and_predictions():
    assert client.get("/api/years").json() == [2006, 2010, 2015, 2020]
    predictions = client.get("/api/predictions").json()
    assert predictions["data_status"] == "speculative_unvalidated_predictions"
    assert predictions["predictions"]
    assert all(
        row["predicted_species_id"] and row["coordinates"] for row in predictions["predictions"]
    )
    profiles = client.get("/api/depth-profiles").json()
    assert {item["species_id"] for item in profiles["species"]} == {
        item["id"] for item in client.get("/api/species").json()
    }


def test_oceans():
    response = client.get("/api/oceans")
    assert response.status_code == 200
    assert {ocean["id"] for ocean in response.json()} == {
        "pacific",
        "atlantic",
        "indian",
        "southern",
        "arctic",
    }


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


def test_months_in_window():
    assert months_in_window(date(2015, 7, 15), date(2015, 7, 15)) == {7}
    assert months_in_window(date(2015, 1, 1), date(2015, 12, 31)) == set(range(1, 13))
