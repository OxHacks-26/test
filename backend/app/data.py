import json
from datetime import date
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


@lru_cache
def load_json(name: str):
    return json.loads((DATA_DIR / name).read_text())


def species() -> list[dict]:
    return load_json("species.json")


def oceans() -> list[dict]:
    return load_json("oceans.json")


def months_in_window(start: date, end: date) -> set[int]:
    """Calendar months (1-12) touched by the window; a window of a year or more covers all."""
    if (end.year - start.year) * 12 + (end.month - start.month) >= 11:
        return set(range(1, 13))
    months, y, m = set(), start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.add(m)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return months


def route_matches(
    props: dict,
    *,
    start: date | None,
    end: date | None,
    species_ids: set[str] | None,
    ocean: str | None,
    depth: float | None,
) -> bool:
    if species_ids and props["species"] not in species_ids:
        return False
    if ocean and props["ocean"] != ocean:
        return False
    if depth is not None and not (props["depth_m"]["min"] <= depth <= props["depth_m"]["max"]):
        return False
    if start or end:
        window_start = start or date.min
        window_end = end or date.max
        if window_start > window_end:
            return False
        if date.fromisoformat(props["start"]) > window_end:
            return False
        if date.fromisoformat(props["end"]) < window_start:
            return False
        if not months_in_window(window_start, window_end) & set(props["months"]):
            return False
    return True


def migrations(
    *,
    start: date | None = None,
    end: date | None = None,
    species_ids: set[str] | None = None,
    ocean: str | None = None,
    depth: float | None = None,
) -> dict:
    collection = load_json("migrations.geojson")
    features = [
        f
        for f in collection["features"]
        if route_matches(
            f["properties"],
            start=start,
            end=end,
            species_ids=species_ids,
            ocean=ocean,
            depth=depth,
        )
    ]
    return {"type": "FeatureCollection", "features": features}
