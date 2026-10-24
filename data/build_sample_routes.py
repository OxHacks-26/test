"""Build example migration routes for 2006, 2010, 2015, and 2020.

Each of the seven species gets one 12-month path per year. Positions follow a
published corridor (nesting beach toward a foraging area and back) and then
shift slightly by year. They are sample predictions for the animation, not
observed tracks.

    python data/build_sample_routes.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
YEARS = (2006, 2010, 2015, 2020)
# Stretch and slide the base path so the four years are not copies.
YEAR_STRETCH = {2006: 0.92, 2010: 1.0, 2015: 1.08, 2020: 0.97}
YEAR_SHIFT = {
    2006: (0.45, -0.35),
    2010: (0.0, 0.0),
    2015: (-0.55, 0.4),
    2020: (0.25, 0.55),
}

# One position per month, January through December: (longitude, latitude).
BASE_ROUTES = {
    "loggerhead": [
        (152.4, -24.8),
        (152.8, -24.4),
        (155.2, -23.2),
        (158.6, -22.0),
        (162.4, -21.2),
        (165.8, -21.6),
        (166.6, -22.2),
        (165.2, -21.4),
        (161.0, -22.2),
        (157.0, -23.4),
        (154.0, -24.4),
        (152.6, -24.9),
    ],
    "green": [
        (-18.5, -8.2),
        (-15.2, -7.9),
        (-14.4, -7.9),
        (-14.5, -8.0),
        (-16.8, -8.4),
        (-24.0, -9.5),
        (-32.5, -11.5),
        (-38.2, -12.8),
        (-39.4, -10.5),
        (-37.0, -8.0),
        (-32.0, -7.2),
        (-24.5, -7.6),
    ],
    "leatherback": [
        (-58.5, 16.0),
        (-60.2, 13.0),
        (-61.2, 10.6),
        (-61.0, 10.7),
        (-60.8, 11.2),
        (-60.4, 12.5),
        (-59.0, 18.0),
        (-57.5, 28.0),
        (-58.5, 36.0),
        (-61.5, 43.5),
        (-59.0, 34.0),
        (-58.0, 22.0),
    ],
    "hawksbill": [
        (-65.2, 18.1),
        (-66.4, 18.4),
        (-68.5, 18.8),
        (-71.0, 19.6),
        (-73.5, 20.8),
        (-75.8, 22.2),
        (-77.4, 24.2),
        (-77.0, 24.6),
        (-75.2, 23.4),
        (-72.0, 21.2),
        (-68.2, 19.2),
        (-65.6, 18.0),
    ],
    "kemps-ridley": [
        (-90.4, 28.7),
        (-91.6, 28.2),
        (-94.5, 26.0),
        (-97.2, 23.8),
        (-97.8, 23.2),
        (-97.7, 23.3),
        (-97.5, 23.5),
        (-95.2, 25.4),
        (-92.4, 27.4),
        (-90.6, 28.8),
        (-89.6, 29.2),
        (-90.2, 28.9),
    ],
    "olive-ridley": [
        (-108.0, 6.2),
        (-110.5, 5.4),
        (-109.0, 7.8),
        (-104.0, 8.4),
        (-98.5, 9.2),
        (-93.0, 9.6),
        (-88.2, 10.1),
        (-85.8, 10.0),
        (-85.7, 9.7),
        (-86.4, 10.3),
        (-92.5, 8.6),
        (-100.5, 7.0),
    ],
    "flatback": [
        (114.7, -21.6),
        (114.5, -21.2),
        (114.0, -19.6),
        (114.6, -18.2),
        (115.8, -16.8),
        (117.0, -16.0),
        (117.6, -15.6),
        (116.8, -16.2),
        (115.4, -17.6),
        (114.6, -19.4),
        (114.5, -20.8),
        (114.8, -21.7),
    ],
}

# Keep each year's slide inside the same corridor.
BOUNDS = {
    "loggerhead": (148.0, 175.0, -28.5, -16.0),
    "green": (-45.0, -12.0, -18.0, -3.0),
    "leatherback": (-70.0, -50.0, 8.0, 48.0),
    "hawksbill": (-79.0, -63.0, 16.0, 26.5),
    "kemps-ridley": (-99.0, -88.0, 22.0, 30.5),
    "olive-ridley": (-115.0, -84.0, 2.0, 14.0),
    "flatback": (112.0, 119.5, -23.5, -14.5),
}

DEPTH = {
    "loggerhead": (0.0, 30.0),
    "green": (0.0, 20.0),
    "leatherback": (0.0, 200.0),
    "hawksbill": (0.0, 10.0),
    "kemps-ridley": (2.0, 3.0),
    "olive-ridley": (20.1, 46.7),
    "flatback": (0.0, 29.0),
}

NESTING_MONTHS = {
    "loggerhead": {11, 12, 1, 2},
    "green": {12, 1, 2, 3, 4},
    "leatherback": {3, 4, 5, 6, 7},
    "hawksbill": {7, 8, 9, 10},
    "kemps-ridley": {4, 5, 6, 7},
    "olive-ridley": {8, 9, 10, 11},
    "flatback": {11, 12, 1, 2},
}

# A nesting month and a foraging month, copied into the sightings sample.
SAMPLE_MONTHS = {
    "loggerhead": (1, 7),
    "green": (3, 8),
    "leatherback": (4, 10),
    "hawksbill": (7, 1),
    "kemps-ridley": (5, 11),
    "olive-ridley": (9, 2),
    "flatback": (12, 7),
}

DETAILS = {
    "loggerhead": {
        "ocean": "pacific",
        "region": "Southwest Pacific, Queensland to the Coral Sea (sample)",
        "name": "Loggerhead Queensland–Coral Sea sample",
    },
    "green": {
        "ocean": "atlantic",
        "region": "Brazil foraging grounds to Ascension Island (sample)",
        "name": "Green turtle Brazil–Ascension sample",
    },
    "leatherback": {
        "ocean": "atlantic",
        "region": "Trinidad nesting beach to the Nova Scotia shelf (sample)",
        "name": "Leatherback Trinidad–Nova Scotia sample",
    },
    "hawksbill": {
        "ocean": "atlantic",
        "region": "Eastern Caribbean reefs to the Bahamas (sample)",
        "name": "Hawksbill Caribbean reef sample",
    },
    "kemps-ridley": {
        "ocean": "atlantic",
        "region": "Rancho Nuevo to the northern Gulf of Mexico (sample)",
        "name": "Kemp's ridley Gulf of Mexico sample",
    },
    "olive-ridley": {
        "ocean": "pacific",
        "region": "Ostional, Costa Rica to the eastern tropical Pacific (sample)",
        "name": "Olive ridley Ostional sample",
    },
    "flatback": {
        "ocean": "indian",
        "region": "Western Australia nesting beaches and nearby shelf (sample)",
        "name": "Flatback Western Australia shelf sample",
    },
}


def vary(species_id: str, year: int) -> list[tuple[float, float]]:
    points = BASE_ROUTES[species_id]
    centre_lon = sum(lon for lon, _lat in points) / len(points)
    centre_lat = sum(lat for _lon, lat in points) / len(points)
    stretch = YEAR_STRETCH[year]
    shift_lon, shift_lat = YEAR_SHIFT[year]
    min_lon, max_lon, min_lat, max_lat = BOUNDS[species_id]
    varied = []
    for lon, lat in points:
        lon = centre_lon + (lon - centre_lon) * stretch + shift_lon
        lat = centre_lat + (lat - centre_lat) * stretch + shift_lat
        lon = min(max(lon, min_lon), max_lon)
        lat = min(max(lat, min_lat), max_lat)
        varied.append((round(lon, 2), round(lat, 2)))
    return varied


def depth(species_id: str, month: int, year: int) -> float:
    shallow, deep = DEPTH[species_id]
    span = deep - shallow
    if month in NESTING_MONTHS[species_id]:
        placed = 0.12
    else:
        placed = 0.45 + 0.4 * (month % 3) / 2
    placed += ((year - 2006) / 14) * 0.08
    value = shallow + span * min(placed, 1)
    value = min(max(round(value, 1), shallow), deep)
    return value


def build():
    species_records = json.loads((ROOT / "species.json").read_text())["species"]
    by_id = {item["id"]: item for item in species_records}
    features = []
    sightings = []
    predictions = []
    year_status = {}

    for species_id, detail in DETAILS.items():
        record = by_id[species_id]
        year_status[species_id] = {
            str(year): "sample_migration_available" for year in YEARS
        }
        for year in YEARS:
            coords = vary(species_id, year)
            months = list(range(1, 13))
            dates = [f"{year}-{month:02d}-15T00:00:00Z" for month in months]
            depths = [depth(species_id, month, year) for month in months]
            route_id = f"{species_id}-{year}"
            features.append(
                {
                    "type": "Feature",
                    "id": route_id,
                    "geometry": {"type": "LineString", "coordinates": coords},
                    "properties": {
                        "species_id": species_id,
                        "species": species_id,
                        "route_id": route_id,
                        "name": f"{detail['name']} {year}",
                        "year": year,
                        "ocean": detail["ocean"],
                        "region": detail["region"],
                        "data_status": "illustrative_sample_prediction",
                        "is_observed": False,
                        "individual_id": None,
                        "position_source": "sample_prediction",
                        "date_source": "sample_year_month",
                        "source_ids": list(record["source_ids"]),
                        "source_scope": (
                            "Example path for the animation. Citations support the species "
                            "and the broad region only, not these coordinates or dates."
                        ),
                        "start": dates[0][:10],
                        "end": dates[-1][:10],
                        "dates": dates,
                        "months": months,
                        "depth_m": depths,
                    },
                }
            )
            for month in SAMPLE_MONTHS[species_id]:
                lon, lat = coords[month - 1]
                observation_id = f"{species_id}-{year}-m{month:02d}"
                observed = f"{year}-{month:02d}-15 12:00:00"
                role = "nesting" if month in NESTING_MONTHS[species_id] else "foraging"
                sightings.append(
                    {
                        "observation_id": observation_id,
                        "dataset_id": "sample-routes",
                        "source_id": record["source_ids"][0],
                        "species_id": species_id,
                        "taxon_label": record["scientific_name"],
                        "observation_label": f"{record['common_name']} sample {role} position",
                        "observed_at_local": observed,
                        "timezone": "UTC",
                        "month": month,
                        "coordinates": [lon, lat],
                        "depth_m": depths[month - 1],
                        "record_type": "sample_route_position",
                        "track_id": route_id,
                        "provider": "Project sample",
                        "license": "sample",
                    }
                )
                predictions.append(
                    {
                        "observation_id": observation_id,
                        "predicted_species_id": species_id,
                        "predicted_common_name": record["common_name"],
                        "confidence": "low",
                        "confidence_is_calibrated": False,
                        "rationale": (
                            f"Example {role} position on the {year} sample route. "
                            f"{detail['region']}"
                        ),
                        "source_ids": list(record["source_ids"]),
                    }
                )

    migrations = {
        "type": "FeatureCollection",
        "schema_version": "1.0.0",
        "metadata": {
            "data_status": "illustrative_sample_prediction",
            "notice": (
                "Example migration paths for the animation. One route per species for "
                "2006, 2010, 2015, and 2020. Coordinates, months, and depths are invented "
                "along published corridors. They are not satellite tracks or predictions "
                "from a fitted model."
            ),
            "coordinate_reference_system": "WGS84",
            "coordinate_order": "longitude,latitude",
            "years": list(YEARS),
            "time_basis": "Each route is one calendar year. Month positions are the 15th.",
            "depth_notice": (
                "depth_m values are sample drawing depths inside the species' stated "
                "range, shallower in nesting months. They are not measured dives."
            ),
        },
        "features": features,
    }
    sightings_doc = {
        "schema_version": "1.0.0",
        "title": "Sample migration positions for the four animation years",
        "data_status": "illustrative_sample_prediction",
        "description": (
            "Two example positions per species per year, taken from the sample routes "
            "in migrations.geojson: one nesting month and one foraging month. These are "
            "not OBIS observations and must not be cited as sightings."
        ),
        "years": list(YEARS),
        "species": [
            {"species_id": item["id"], "common_name": item["common_name"]}
            for item in species_records
        ],
        "year_availability": [
            {
                "year": year,
                "status": "sample_routes_available",
                "sample_position_count": 14,
                "available_months": list(range(1, 13)),
                "species_specific_tracks": True,
                "note": (
                    "Example positions for every species. The map route is the matching "
                    "LineString in migrations.geojson. Not an observed track."
                ),
            }
            for year in YEARS
        ],
        "sightings": sightings,
        "species_year_status": year_status,
    }
    predictions_doc = {
        "schema_version": "1.0.0",
        "title": "Sample species labels for the example migration positions",
        "data_status": "illustrative_sample_predictions",
        "description": (
            "Each sample position is labelled with the species of the route it was "
            "taken from. Confidence is low because the coordinates are invented."
        ),
        "method": {
            "name": "sample route position",
            "summary": (
                "Positions are copied from the example migration for that species and year. "
                "No classifier was trained."
            ),
            "limitations": [
                "Coordinates and dates are hand-built examples.",
                "Do not treat the labels as identifications of wild turtles.",
                "Do not report these paths as conservation results.",
            ],
            "source_ids": [],
        },
        "predictions": predictions,
    }
    (ROOT / "migrations.geojson").write_text(json.dumps(migrations, indent=2) + "\n")
    (ROOT / "animation_sightings.json").write_text(
        json.dumps(sightings_doc, indent=2) + "\n"
    )
    (ROOT / "animation_species_predictions.json").write_text(
        json.dumps(predictions_doc, indent=2) + "\n"
    )
    print(
        f"Wrote {len(features)} routes, {len(sightings)} sample positions, "
        f"{len(predictions)} predictions."
    )


if __name__ == "__main__":
    build()
