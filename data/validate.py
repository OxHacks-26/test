"""Validate the checked-in data contract without network access: py data/validate.py."""

import datetime as dt
import json
from pathlib import Path
import re


def main():
    root = Path(__file__).resolve().parent
    species = json.loads((root / "species.json").read_text(encoding="utf-8"))["species"]
    sources = json.loads((root / "sources.json").read_text(encoding="utf-8"))["sources"]
    routes = json.loads((root / "migrations.geojson").read_text(encoding="utf-8"))
    source_ids = {source["id"] for source in sources}
    species_ids = {item["id"] for item in species}
    assert len(species) == len(species_ids) == 7
    assert len(source_ids) == len(sources)
    assert len({item["colour"] for item in species}) == 7
    for item in species:
        assert re.fullmatch(r"#[0-9A-Fa-f]{6}", item["colour"])
        assert 0 <= item["depth_range_m"]["min"] <= item["depth_range_m"]["max"]
        assert item["depth_context"]
        assert set(item["source_ids"]) <= source_ids
        assert set(item["depth_source_ids"]) <= source_ids
        for season in item["seasonality"]:
            assert season["months"] and set(season["months"]) <= set(range(1, 13))
            assert set(season.get("peak_months", [])) <= set(season["months"])
            assert set(season["source_ids"]) <= source_ids
    assert routes["type"] == "FeatureCollection"
    assert routes["metadata"]["data_status"] == "illustrative_sample_prediction"
    assert routes["metadata"]["years"] == [2006, 2010, 2015, 2020]
    assert len(routes["features"]) == 28
    assert {f["properties"]["species_id"] for f in routes["features"]} == species_ids
    depth_ranges = {item["id"]: item["depth_range_m"] for item in species}
    years_by_species = {}
    for feature in routes["features"]:
        geometry, props = feature["geometry"], feature["properties"]
        assert feature["type"] == "Feature" and geometry["type"] == "LineString"
        points = geometry["coordinates"]
        assert (
            len(points)
            == len(props["dates"])
            == len(props["months"])
            == len(props["depth_m"])
            == 12
        )
        assert props["months"] == list(range(1, 13))
        assert props["is_observed"] is False
        assert props["individual_id"] is None
        assert props["data_status"] == "illustrative_sample_prediction"
        assert props["year"] in (2006, 2010, 2015, 2020)
        assert props["ocean"] in {"pacific", "atlantic", "indian", "southern", "arctic"}
        depth_range = depth_ranges[props["species_id"]]
        assert all(
            depth_range["min"] <= depth <= depth_range["max"]
            for depth in props["depth_m"]
        )
        assert set(props["source_ids"]) <= source_ids
        dates = [
            dt.datetime.fromisoformat(date.replace("Z", "+00:00"))
            for date in props["dates"]
        ]
        assert dates == sorted(dates)
        assert [date.year for date in dates] == [props["year"]] * 12
        assert [date.month for date in dates] == props["months"]
        years_by_species.setdefault(props["species_id"], set()).add(props["year"])
        for lon, lat in points:
            assert -180 <= lon <= 180 and -90 <= lat <= 90
    assert all(years == {2006, 2010, 2015, 2020} for years in years_by_species.values())
    print(
        f"Valid: {len(species)} species, {len(routes['features'])} sample routes, "
        f"{12 * len(routes['features'])} dated positions, {len(sources)} sources."
    )


if __name__ == "__main__":
    main()
