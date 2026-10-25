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
    assert len(routes["features"]) == 28
    species_ids = {item["id"] for item in client.get("/api/species").json()}
    years_by_species = {}
    for feature in routes["features"]:
        props = feature["properties"]
        years_by_species.setdefault(props["species_id"], set()).add(props["year"])
        assert {date[:4] for date in props["dates"]} == {str(props["year"])}
    assert set(years_by_species) == species_ids
    assert all(years == {2006, 2010, 2015, 2020} for years in years_by_species.values())


def test_migrations_filter_by_species_and_date():
    green = client.get("/api/migrations", params={"species": "green"}).json()["features"]
    assert len(green) == 4
    assert {feature["properties"]["year"] for feature in green} == {2006, 2010, 2015, 2020}

    species_ids = {item["id"] for item in client.get("/api/species").json()}
    for year in (2006, 2010, 2015, 2020):
        window = client.get("/api/migrations", params={"year": year}).json()["features"]
        assert len(window) == 7
        assert {feature["properties"]["species_id"] for feature in window} == species_ids
        assert {feature["properties"]["year"] for feature in window} == {year}

    one = client.get("/api/migrations", params={"species": "green", "year": 2006}).json()[
        "features"
    ]
    assert len(one) == 1
    assert one[0]["properties"]["route_id"] == "green-2006"
    july = client.get(
        "/api/migrations", params={"from": "2015-07-01", "to": "2015-07-31", "species": "green"}
    ).json()["features"]
    assert len(july) == 1
    assert july[0]["properties"]["year"] == 2015
    assert client.get("/api/migrations", params={"year": 2025}).json()["features"] == []
    indian = client.get("/api/migrations", params={"ocean": "indian", "year": 2010}).json()[
        "features"
    ]
    assert [feature["properties"]["species_id"] for feature in indian] == ["flatback"]
    assert client.get("/api/migrations", params={"from": "not-a-date"}).status_code == 422


def test_migrations_does_not_filter_by_depth():
    assert len(client.get("/api/migrations", params={"depth": 4100}).json()["features"]) == 28


def test_years_and_predictions():
    species_ids = {item["id"] for item in client.get("/api/species").json()}
    assert client.get("/api/years").json() == [2006, 2010, 2015, 2020]
    predictions = client.get("/api/predictions").json()
    assert predictions["data_status"] == "illustrative_sample_predictions"
    assert predictions["years"] == [2006, 2010, 2015, 2020]
    assert set(predictions["species_year_status"]) == species_ids
    pairs = {(row["predicted_species_id"], row["year"]) for row in predictions["predictions"]}
    assert pairs == {
        (species_id, year) for species_id in species_ids for year in (2006, 2010, 2015, 2020)
    }
    assert all(row["coordinates"] for row in predictions["predictions"])
    green = client.get("/api/predictions", params={"species": "green", "year": 2015}).json()
    assert green["predictions"]
    assert {row["predicted_species_id"] for row in green["predictions"]} == {"green"}
    assert {row["year"] for row in green["predictions"]} == {2015}
    assert set(green["species_year_status"]) == {"green"}
    profiles = client.get("/api/depth-profiles").json()
    assert {item["species_id"] for item in profiles["species"]} == species_ids


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


def test_sources_have_titles_and_links():
    sources = client.get("/api/sources").json()
    assert sources
    assert all({"id", "title", "url"} <= source.keys() for source in sources)
