"""Fetch a bounded OBIS occurrence sample; never turn unrelated records into tracks.

Run from any directory: py data/fetch_obis.py --size 100
Uses only Python's standard library. Requires network access.
"""

import argparse
import datetime as dt
import json
import math
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=100)
    args = parser.parse_args()
    if not 1 <= args.size <= 1000:
        parser.error("--size must be between 1 and 1000 per species")
    output = ROOT / "obis_sample"
    if output.exists():
        parser.error("obis_sample already exists; archive it before fetching a new sample")

    species = json.loads((ROOT / "species.json").read_text(encoding="utf-8"))["species"]
    features, manifest, raw_responses = [], [], {}
    for item in species:
        url = "https://api.obis.org/v3/occurrence?" + urlencode(
            {"scientificname": item["scientific_name"], "size": args.size}
        )
        print("Fetching", item["scientific_name"], flush=True)
        request = Request(url, headers={"User-Agent": "OxHacks-SeaTurtle-Data/1.0"})
        with urlopen(request, timeout=60) as response:
            payload = json.load(response)
        records = payload.get("results")
        if not isinstance(records, list):
            raise ValueError(f"Unexpected OBIS response for {item['id']}; no files written")
        raw_responses[item["id"]] = payload
        accepted = 0
        for record in records:
            if record.get("dropped") or record.get("absence"):
                continue
            # Only accept the requested taxon, rather than silently relabel records.
            if record.get("scientificName") != item["scientific_name"]:
                continue
            lon, lat = record.get("decimalLongitude"), record.get("decimalLatitude")
            if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in (lon, lat)):
                continue
            if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                continue
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {
                    "species_id": item["id"],
                    "data_status": "provider_reported_occurrence",
                    "obis_id": record.get("id"),
                    "occurrence_id": record.get("occurrenceID"),
                    "dataset_id": record.get("dataset_id"),
                    "event_date": record.get("eventDate"),
                    "date_start": record.get("date_start"),
                    "date_end": record.get("date_end"),
                    "coordinate_uncertainty_m": record.get("coordinateUncertaintyInMeters"),
                    "basis_of_record": record.get("basisOfRecord"),
                    "license": record.get("license"),
                    "rights_holder": record.get("rightsHolder"),
                    "bibliographic_citation": record.get("bibliographicCitation"),
                    "references": record.get("references"),
                    "quality_flags": record.get("flags"),
                    "reported_minimum_depth_m": record.get("minimumDepthInMeters"),
                    "reported_maximum_depth_m": record.get("maximumDepthInMeters"),
                    "measured_turtle_depth_m": None,
                    "individual_id": None,
                    "source_url": url,
                },
            })
            accepted += 1
        manifest.append({"species_id": item["id"], "url": url, "received": len(records), "accepted": accepted})

    # Stage all requests in memory so a failed request leaves no partial sample.
    output.mkdir()
    for species_id, payload in raw_responses.items():
        (output / f"{species_id}.raw.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    collection = {
        "type": "FeatureCollection",
        "metadata": {
            "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "notice": "Bounded API sample, not comprehensive, random, live tracking, or individual migration routes. Check source dataset licenses before redistribution. Missing values remain null.",
            "queries": manifest,
        },
        "features": features,
    }
    (output / "occurrences.geojson").write_text(json.dumps(collection, indent=2), encoding="utf-8")
    print(f"Saved {len(features)} occurrence points to {output}")


if __name__ == "__main__":
    main()
