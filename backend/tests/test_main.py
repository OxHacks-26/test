import json
from datetime import date
from pathlib import Path

from fastapi.testclient import TestClient

from app.data import months_in_window
from app.main import app

client = TestClient(app)
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

GREEN = "green-south-atlantic-brazil-ascension"
LOGGERHEAD = "loggerhead-north-pacific-japan-baja"


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


def load(name):
    return json.loads((DATA_DIR / name).read_text())


def features(params=None):
    response = client.get("/api/migrations", params=params)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["type"] == "FeatureCollection"
    return body["features"]


def route_ids(params=None):
    return {feature["properties"]["id"] for feature in features(params)}


def test_months_in_window():
    assert months_in_window(date(2015, 7, 15), date(2015, 7, 15)) == {7}
    assert months_in_window(date(2015, 1, 1), date(2015, 1, 31)) == {1}
    assert months_in_window(date(2015, 12, 15), date(2016, 2, 15)) == {12, 1, 2}
    assert months_in_window(date(2015, 4, 1), date(2015, 10, 31)) == {4, 5, 6, 7, 8, 9, 10}
    assert months_in_window(date(2015, 1, 1), date(2015, 11, 30)) == set(range(1, 12))
    assert months_in_window(date(2015, 1, 1), date(2015, 12, 31)) == set(range(1, 13))
    # February through the following January touches every month.
    assert months_in_window(date(2015, 2, 1), date(2016, 1, 31)) == set(range(1, 13))
    # March through the following January misses February.
    assert months_in_window(date(2015, 3, 1), date(2016, 1, 31)) == {
        1,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
    }


def test_migrations_serves_geojson_file():
    response = client.get("/api/migrations")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json() == load("migrations.geojson")


def test_filter_examples_match_checked_in_routes():
    routes = {
        feature["properties"]["id"]: feature["properties"]
        for feature in load("migrations.geojson")["features"]
    }
    green = routes[GREEN]
    assert green["species"] == "green"
    assert green["ocean"] == "atlantic"
    assert (green["start"], green["end"]) == ("1990-01-01", "2030-12-31")
    assert green["months"] == [11, 12, 1, 2, 3]
    assert green["depth_m"] == {"min": 0, "max": 40}

    loggerhead = routes[LOGGERHEAD]
    assert loggerhead["species"] == "loggerhead"
    assert loggerhead["ocean"] == "pacific"
    assert (loggerhead["start"], loggerhead["end"]) == ("1990-01-01", "2030-12-31")
    assert loggerhead["months"] == list(range(1, 13))
    assert loggerhead["depth_m"] == {"min": 0, "max": 100}


def test_migrations_filter_by_species():
    file_features = load("migrations.geojson")["features"]
    assert route_ids({"species": "green"}) == {
        feature["properties"]["id"]
        for feature in file_features
        if feature["properties"]["species"] == "green"
    }
    assert route_ids({"species": "loggerhead, green"}) == route_ids({"species": "loggerhead,green"})
    assert route_ids({"species": "loggerhead,green"}) == {
        feature["properties"]["id"]
        for feature in file_features
        if feature["properties"]["species"] in {"loggerhead", "green"}
    }
    assert route_ids({"species": "leatherback"}) == set()
    assert route_ids({"species": "log"}) == set()


def test_migrations_filter_by_ocean():
    file_features = load("migrations.geojson")["features"]
    assert route_ids({"ocean": "atlantic"}) == {
        feature["properties"]["id"]
        for feature in file_features
        if feature["properties"]["ocean"] == "atlantic"
    }
    assert route_ids({"ocean": "pacific"}) == {
        feature["properties"]["id"]
        for feature in file_features
        if feature["properties"]["ocean"] == "pacific"
    }
    assert route_ids({"ocean": "southern"}) == set()


def test_migrations_time_window_uses_overlap_and_months():
    # Green is Nov-Mar. Loggerhead is year-round. Both are active 1990-2030.
    january = {"from": "2015-01-01", "to": "2015-01-31"}
    july = {"from": "2015-07-01", "to": "2015-07-31"}
    assert GREEN in route_ids(january)
    assert LOGGERHEAD in route_ids(january)
    assert GREEN not in route_ids(july)
    assert LOGGERHEAD in route_ids(july)
    for feature in features(july):
        props = feature["properties"]
        assert props["start"] <= "2015-07-31"
        assert props["end"] >= "2015-07-01"
        assert 7 in props["months"]

    year = {"from": "2015-01-01", "to": "2015-12-31"}
    assert {GREEN, LOGGERHEAD} <= route_ids(year)

    winter = {"from": "2015-12-15", "to": "2016-02-15"}
    assert GREEN in route_ids(winter)
    for feature in features(winter):
        assert set(feature["properties"]["months"]) & {12, 1, 2}

    spring_to_autumn = {"from": "2015-04-01", "to": "2015-10-31"}
    assert GREEN not in route_ids(spring_to_autumn)
    assert LOGGERHEAD in route_ids(spring_to_autumn)

    assert GREEN not in route_ids({"from": "1950-01-01", "to": "1960-12-31"})
    assert LOGGERHEAD not in route_ids({"from": "1950-01-01", "to": "1960-12-31"})
    assert GREEN not in route_ids({"from": "2040-01-01", "to": "2041-12-31"})
    assert GREEN in route_ids({"from": "1989-12-01", "to": "1990-01-31"})
    assert GREEN in route_ids({"from": "2030-12-01", "to": "2031-01-15"})
    assert GREEN not in route_ids({"from": "2031-01-01", "to": "2031-03-31"})


def test_migrations_open_ended_and_inverted_windows():
    # An open end covers every later month, so July as a start still includes Nov-Mar.
    assert GREEN in route_ids({"from": "2020-07-01"})
    assert GREEN not in route_ids({"from": "2040-01-01"})
    assert GREEN in route_ids({"to": "2010-07-01"})
    assert GREEN not in route_ids({"to": "1980-01-01"})
    for feature in features({"from": "2020-07-01"}):
        assert feature["properties"]["end"] >= "2020-07-01"
    for feature in features({"to": "2010-07-01"}):
        assert feature["properties"]["start"] <= "2010-07-01"
    assert route_ids({"from": "2015-08-01", "to": "2015-01-01"}) == set()


def test_migrations_rejects_bad_dates_and_depth():
    assert client.get("/api/migrations", params={"from": "not-a-date"}).status_code == 422
    assert client.get("/api/migrations", params={"to": "2015-13-01"}).status_code == 422
    assert client.get("/api/migrations", params={"depth": -1}).status_code == 422
    assert client.get("/api/migrations", params={"depth": "deep"}).status_code == 422


def test_migrations_filter_by_depth():
    file_features = load("migrations.geojson")["features"]
    for depth in (0, 40, 40.1, 80, 100, 100.1):
        expected = {
            feature["properties"]["id"]
            for feature in file_features
            if feature["properties"]["depth_m"]["min"]
            <= depth
            <= feature["properties"]["depth_m"]["max"]
        }
        assert route_ids({"depth": depth}) == expected
    assert LOGGERHEAD in route_ids({"depth": 80})
    assert GREEN not in route_ids({"depth": 80})


def test_migrations_filters_are_combined():
    params = {
        "species": "green,loggerhead",
        "ocean": "atlantic",
        "from": "2015-01-01",
        "to": "2015-01-31",
        "depth": 20,
    }
    assert GREEN in route_ids(params)
    assert LOGGERHEAD not in route_ids(params)
    for feature in features(params):
        props = feature["properties"]
        assert props["species"] in {"green", "loggerhead"}
        assert props["ocean"] == "atlantic"
        assert props["depth_m"]["min"] <= 20 <= props["depth_m"]["max"]
        assert props["start"] <= "2015-01-31"
        assert props["end"] >= "2015-01-01"
        assert 1 in props["months"]
    assert route_ids({"species": "green", "ocean": "pacific"}) == set()
    assert GREEN not in route_ids({"species": "green", "depth": 80})


def test_filtered_routes_keep_file_properties():
    by_id = {
        feature["properties"]["id"]: feature for feature in load("migrations.geojson")["features"]
    }
    for feature in features({"ocean": "pacific"}):
        assert feature == by_id[feature["properties"]["id"]]


def test_migrations_query_parameter_names():
    schema = client.get("/openapi.json").json()
    params = schema["paths"]["/api/migrations"]["get"]["parameters"]
    assert {param["name"] for param in params} == {"from", "to", "species", "ocean", "depth"}
    assert all(not param["required"] for param in params)


def test_oceans():
    response = client.get("/api/oceans")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json() == load("oceans.json")
