import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

SPECIES_KEYS = {"id", "common_name", "scientific_name", "colour", "depth_range_m"}
ROUTE_KEYS = {"route_id", "species_id", "months", "depth_m"}


def load(name):
    return json.loads((DATA_DIR / name).read_text())


def test_species_file():
    species = load("species.json")["species"]
    assert len(species) == 7
    for item in species:
        assert SPECIES_KEYS <= item.keys(), item["id"]


def test_migrations_reference_known_species_and_oceans():
    species_ids = {item["id"] for item in load("species.json")["species"]}
    routes = load("migrations.geojson")["features"]
    assert routes
    for route in routes:
        props = route["properties"]
        assert ROUTE_KEYS <= props.keys(), props["route_id"]
        assert props["species_id"] in species_ids, props["route_id"]
        assert route["geometry"]["type"] == "LineString"
        assert all(1 <= month <= 12 for month in props["months"])
