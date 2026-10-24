"""Export the sea-turtle JSON files to CSV.

JSON in data/ stays the source the API reads. This writes spreadsheet copies
under data/csv/. List fields are joined with " | ".

    python data/export_csv.py
    python data/export_csv.py --data-dir /path/to/data --out-dir /path/to/csv
"""

import argparse
import csv
import json
from pathlib import Path


def load(directory: Path, name: str):
    path = directory / name
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return " | ".join(cell(item) for item in value)
    return str(value)


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: cell(row.get(key)) for key in fieldnames})
    print(f"{path.name}: {len(rows)} rows")


def export(data_dir: Path, out_dir: Path) -> None:
    species_payload = load(data_dir, "species.json") or {}
    species = (
        species_payload["species"]
        if isinstance(species_payload, dict)
        else species_payload
    )
    write_csv(
        out_dir / "species.csv",
        [
            {
                "id": item["id"],
                "common_name": item.get("common_name"),
                "scientific_name": item.get("scientific_name"),
                "colour": item.get("colour") or item.get("color"),
                "distribution": item.get("distribution"),
                "depth_min_m": (item.get("depth_range_m") or {}).get("min"),
                "depth_max_m": (item.get("depth_range_m") or {}).get("max"),
                "depth_context": item.get("depth_context"),
                "study_max_dive_m": item.get("study_max_dive_m"),
                "study_max_dive_uncertainty_m": item.get(
                    "study_max_dive_uncertainty_m"
                ),
                "depth_source_ids": item.get("depth_source_ids"),
                "source_ids": item.get("source_ids"),
            }
            for item in species
        ],
        [
            "id",
            "common_name",
            "scientific_name",
            "colour",
            "distribution",
            "depth_min_m",
            "depth_max_m",
            "depth_context",
            "study_max_dive_m",
            "study_max_dive_uncertainty_m",
            "depth_source_ids",
            "source_ids",
        ],
    )

    fact_rows = []
    season_rows = []
    for item in species:
        for index, fact in enumerate(item.get("facts") or [], start=1):
            fact_rows.append(
                {"species_id": item["id"], "fact_index": index, "fact": fact}
            )
        for season in item.get("seasonality") or []:
            season_rows.append(
                {
                    "species_id": item["id"],
                    "region": season.get("region"),
                    "activity": season.get("activity"),
                    "months": season.get("months"),
                    "peak_months": season.get("peak_months"),
                    "source_ids": season.get("source_ids"),
                }
            )
    write_csv(
        out_dir / "species_facts.csv", fact_rows, ["species_id", "fact_index", "fact"]
    )
    write_csv(
        out_dir / "species_seasonality.csv",
        season_rows,
        ["species_id", "region", "activity", "months", "peak_months", "source_ids"],
    )

    textboxes = load(data_dir, "textboxes.json") or {}
    box_rows = []
    for item in textboxes.get("species") or []:
        for index, box in enumerate(item.get("textboxes") or [], start=1):
            box_rows.append(
                {
                    "species_id": item.get("species_id"),
                    "common_name": item.get("common_name"),
                    "box_index": index,
                    "topic": box.get("topic"),
                    "text": box.get("text"),
                    "source_ids": box.get("source_ids"),
                }
            )
    write_csv(
        out_dir / "textboxes.csv",
        box_rows,
        ["species_id", "common_name", "box_index", "topic", "text", "source_ids"],
    )

    sources = load(data_dir, "sources.json") or {}
    write_csv(
        out_dir / "sources.csv",
        sources.get("sources") or [],
        ["id", "title", "url", "accessed_on", "supports"],
    )

    routes = load(data_dir, "migrations.geojson") or {}
    route_rows = []
    position_rows = []
    for feature in routes.get("features") or []:
        props = feature["properties"]
        coordinates = feature["geometry"]["coordinates"]
        route_rows.append(
            {
                "route_id": props.get("route_id"),
                "species_id": props.get("species_id"),
                "region": props.get("region"),
                "data_status": props.get("data_status"),
                "is_observed": props.get("is_observed"),
                "individual_id": props.get("individual_id"),
                "position_source": props.get("position_source"),
                "date_source": props.get("date_source"),
                "source_scope": props.get("source_scope"),
                "source_ids": props.get("source_ids"),
                "position_count": len(coordinates),
            }
        )
        dates = props.get("dates") or []
        months = props.get("months") or []
        depths = props.get("depth_m") or []
        for index, (lon, lat) in enumerate(coordinates):
            date = dates[index] if index < len(dates) else ""
            position_rows.append(
                {
                    "route_id": props.get("route_id"),
                    "species_id": props.get("species_id"),
                    "position_index": index + 1,
                    "longitude": lon,
                    "latitude": lat,
                    "date": date,
                    "year": str(date)[:4] if date else "",
                    "month": months[index] if index < len(months) else "",
                    "depth_m": depths[index] if index < len(depths) else "",
                }
            )
    write_csv(
        out_dir / "migration_routes.csv",
        route_rows,
        [
            "route_id",
            "species_id",
            "region",
            "data_status",
            "is_observed",
            "individual_id",
            "position_source",
            "date_source",
            "source_scope",
            "source_ids",
            "position_count",
        ],
    )
    write_csv(
        out_dir / "migration_positions.csv",
        position_rows,
        [
            "route_id",
            "species_id",
            "position_index",
            "longitude",
            "latitude",
            "date",
            "year",
            "month",
            "depth_m",
        ],
    )

    sightings_payload = load(data_dir, "animation_sightings.json") or {}
    sighting_rows = []
    for item in sightings_payload.get("sightings") or []:
        coordinates = item.get("coordinates") or [None, None]
        observed = item.get("observed_at_local") or ""
        sighting_rows.append(
            {
                **item,
                "longitude": coordinates[0] if coordinates else "",
                "latitude": coordinates[1] if len(coordinates) > 1 else "",
                "year": observed[:4],
            }
        )
    write_csv(
        out_dir / "sightings.csv",
        sighting_rows,
        [
            "observation_id",
            "dataset_id",
            "source_id",
            "species_id",
            "taxon_label",
            "observation_label",
            "observed_at_local",
            "year",
            "month",
            "timezone",
            "longitude",
            "latitude",
            "depth_m",
            "record_type",
            "track_id",
            "provider",
            "license",
        ],
    )
    write_csv(
        out_dir / "year_availability.csv",
        [
            {
                **item,
                "available_months": item.get("available_months"),
                "dataset_source_ids": item.get("dataset_source_ids"),
            }
            for item in sightings_payload.get("year_availability") or []
        ],
        [
            "year",
            "status",
            "sample_position_count",
            "archive_record_count",
            "available_months",
            "species_specific_tracks",
            "note",
            "dataset_source_ids",
        ],
    )
    status_rows = []
    for species_id, years in (
        sightings_payload.get("species_year_status") or {}
    ).items():
        for year, status in years.items():
            status_rows.append(
                {"species_id": species_id, "year": year, "status": status}
            )
    write_csv(
        out_dir / "species_year_status.csv",
        status_rows,
        ["species_id", "year", "status"],
    )

    by_sighting = {
        item["observation_id"]: item
        for item in sightings_payload.get("sightings") or []
    }
    predictions = load(data_dir, "animation_species_predictions.json") or {}
    prediction_rows = []
    for item in predictions.get("predictions") or []:
        sighting = by_sighting.get(item.get("observation_id"), {})
        coordinates = sighting.get("coordinates") or [None, None]
        observed = sighting.get("observed_at_local") or ""
        prediction_rows.append(
            {
                **item,
                "observed_at_local": observed,
                "year": observed[:4],
                "month": sighting.get("month"),
                "longitude": coordinates[0] if coordinates else "",
                "latitude": coordinates[1] if len(coordinates) > 1 else "",
                "source_ids": item.get("source_ids"),
            }
        )
    write_csv(
        out_dir / "predictions.csv",
        prediction_rows,
        [
            "observation_id",
            "predicted_species_id",
            "predicted_common_name",
            "confidence",
            "confidence_is_calibrated",
            "rationale",
            "observed_at_local",
            "year",
            "month",
            "longitude",
            "latitude",
            "source_ids",
        ],
    )

    profiles = load(data_dir, "animation_depth_profiles.json") or {}
    depth_rows = []
    for item in profiles.get("species") or []:
        for example in item.get("study_examples") or []:
            depth_rows.append(
                {
                    "species_id": item.get("species_id"),
                    "common_name": item.get("common_name"),
                    "metric": example.get("metric"),
                    "depth_min_m": example.get("depth_min_m"),
                    "depth_max_m": example.get("depth_max_m"),
                    "sample_context": example.get("sample_context"),
                    "source_id": example.get("source_id"),
                }
            )
    write_csv(
        out_dir / "depth_examples.csv",
        depth_rows,
        [
            "species_id",
            "common_name",
            "metric",
            "depth_min_m",
            "depth_max_m",
            "sample_context",
            "source_id",
        ],
    )

    oceans_payload = load(data_dir, "oceans.json")
    if oceans_payload is not None:
        oceans = (
            oceans_payload.get("oceans")
            if isinstance(oceans_payload, dict)
            else oceans_payload
        )
        write_csv(
            out_dir / "oceans.csv",
            [
                {
                    "id": ocean.get("id"),
                    "name": ocean.get("name"),
                    "min_lon": (ocean.get("bbox") or [None, None, None, None])[0],
                    "min_lat": (ocean.get("bbox") or [None, None, None, None])[1],
                    "max_lon": (ocean.get("bbox") or [None, None, None, None])[2],
                    "max_lat": (ocean.get("bbox") or [None, None, None, None])[3],
                    "center_lon": (ocean.get("center") or [None, None])[0],
                    "center_lat": (ocean.get("center") or [None, None])[1],
                }
                for ocean in oceans or []
            ],
            [
                "id",
                "name",
                "min_lon",
                "min_lat",
                "max_lon",
                "max_lat",
                "center_lon",
                "center_lat",
            ],
        )


def main() -> None:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=root)
    parser.add_argument("--out-dir", type=Path, default=root / "csv")
    args = parser.parse_args()
    export(args.data_dir, args.out_dir)


if __name__ == "__main__":
    main()
