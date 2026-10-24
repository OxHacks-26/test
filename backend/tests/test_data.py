import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

SPECIES_KEYS = {"id", "common_name", "scientific_name", "color", "depth_range_m", "iucn_status"}
ROUTE_KEYS = {"id", "species", "name", "ocean", "start", "end", "months", "depth_m", "confidence"}


def load(name):
    return json.loads((DATA_DIR / name).read_text())


def test_species_file():
    species = load("species.json")
    assert len(species) == 7
    for s in species:
        assert SPECIES_KEYS <= s.keys(), s["id"]


def test_migrations_reference_known_species_and_oceans():
    species_ids = {s["id"] for s in load("species.json")}
    ocean_ids = {o["id"] for o in load("oceans.json")}
    routes = load("migrations.geojson")["features"]
    assert routes
    for route in routes:
        props = route["properties"]
        assert ROUTE_KEYS <= props.keys(), props["id"]
        assert props["species"] in species_ids, props["id"]
        assert props["ocean"] in ocean_ids, props["id"]
        assert route["geometry"]["type"] == "LineString"
        assert all(1 <= m <= 12 for m in props["months"])
