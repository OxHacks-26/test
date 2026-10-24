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
    sightings = json.loads((root / "animation_sightings.json").read_text(encoding="utf-8"))
    depth_profiles = json.loads((root / "animation_depth_profiles.json").read_text(encoding="utf-8"))
    predictions = json.loads((root / "animation_species_predictions.json").read_text(encoding="utf-8"))
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
    animation_species_ids = {item["species_id"] for item in sightings["species"]}
    assert animation_species_ids == species_ids
    assert sightings["data_status"] == "partial_occurrence_sightings_not_migration_tracks"
    animation_years = sightings["years"]
    assert animation_years == [2006, 2010, 2015, 2020]
    assert set(sightings["species_year_status"]) == species_ids
    for species_status in sightings["species_year_status"].values():
        assert {int(year) for year in species_status} == set(animation_years)
    assert {item["year"] for item in sightings["year_availability"]} == set(animation_years)
    assert all(item["species_specific_tracks"] is False for item in sightings["year_availability"])
    for item in sightings["year_availability"]:
        assert set(item["dataset_source_ids"]) <= source_ids
    assert len(sightings["sightings"]) == 4
    for sighting in sightings["sightings"]:
        assert sighting["license"] == "CC0"
        assert sighting["source_id"] in source_ids
        assert sighting["species_id"] is None
        assert sighting["track_id"] is None
        assert sighting["depth_m"] is None
        assert len(sighting["coordinates"]) == 2
        lon, lat = sighting["coordinates"]
        assert -180 <= lon <= 180 and -90 <= lat <= 90
        observed = dt.datetime.strptime(sighting["observed_at_local"], "%Y-%m-%d %H:%M:%S")
        assert observed.year == 2006 and observed.month == sighting["month"] == 7
    assert predictions["data_status"] == "speculative_unvalidated_predictions"
    assert set(predictions["method"]["source_ids"]) <= source_ids
    assert len(predictions["predictions"]) == len(sightings["sightings"])
    sighting_ids = {sighting["observation_id"] for sighting in sightings["sightings"]}
    prediction_ids = [prediction["observation_id"] for prediction in predictions["predictions"]]
    assert set(prediction_ids) == sighting_ids and len(prediction_ids) == len(set(prediction_ids))
    for prediction in predictions["predictions"]:
        assert prediction["predicted_species_id"] in species_ids
        assert prediction["confidence"] == "low"
        assert prediction["confidence_is_calibrated"] is False
        assert prediction["source_ids"]
        assert set(prediction["source_ids"]) <= source_ids
    depth_species_ids = {item["species_id"] for item in depth_profiles["species"]}
    assert depth_species_ids == species_ids
    assert depth_profiles["chart_axes"]["animation_ready"] is False
    assert depth_profiles["chart_axes"]["x"] is None
    for item in depth_profiles["species"]:
        assert item["study_examples"]
        for example in item["study_examples"]:
            assert example["source_id"] in source_ids
            assert example["sample_context"]
            minimum, maximum = example["depth_min_m"], example["depth_max_m"]
            assert minimum is None or minimum >= 0
            assert maximum is None or maximum >= 0
            assert minimum is not None or maximum is not None
            if minimum is not None and maximum is not None:
                assert minimum <= maximum
    assert routes["type"] == "FeatureCollection"
    assert routes["metadata"]["data_status"] == "illustrative_not_observed"
    assert len(routes["features"]) == 7
    assert {f["properties"]["species_id"] for f in routes["features"]} == species_ids
    for feature in routes["features"]:
        geometry, props = feature["geometry"], feature["properties"]
        assert feature["type"] == "Feature" and geometry["type"] == "LineString"
        points = geometry["coordinates"]
        assert len(points) == len(props["dates"]) == len(props["months"]) == len(props["depth_m"]) == 12
        assert props["months"] == list(range(1, 13))
        assert props["is_observed"] is False
        assert props["individual_id"] is None
        assert props["data_status"] == "illustrative_not_observed"
        assert all(depth is None for depth in props["depth_m"])
        assert set(props["source_ids"]) <= source_ids
        dates = [dt.datetime.fromisoformat(date.replace("Z", "+00:00")) for date in props["dates"]]
        assert dates == sorted(dates)
        assert [date.month for date in dates] == props["months"]
        for lon, lat in points:
            assert -180 <= lon <= 180 and -90 <= lat <= 90
    print(
        f"Valid: {len(species)} species, 7 demo routes, 84 demo positions, "
        f"{len(sightings['sightings'])} CC0 sighting markers, "
        f"{len(depth_profiles['species'])} depth profiles, {len(sources)} sources."
    )


if __name__ == "__main__":
    main()
