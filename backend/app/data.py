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
    """Calendar months (1-12) touched by an inclusive date window.

    A span of twelve months or more covers every month. Measured in calendar
    months, January through December of one year (a difference of 11) is a
    full year.
    """
    month_span = (end.year - start.year) * 12 + (end.month - start.month)
    if month_span >= 11:
        return set(range(1, 13))
    months: set[int] = set()
    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        months.add(month)
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return months


def migrations(
    *,
    start: date | None = None,
    end: date | None = None,
    species_ids: set[str] | None = None,
    ocean: str | None = None,
    depth: float | None = None,
) -> dict:
    """GeoJSON FeatureCollection of routes matching the optional filters.

    A route is in a time window when its start-end span overlaps the window
    and at least one of its months falls inside the window. A depth matches
    when depth_m.min <= depth <= depth_m.max.
    """
    collection = load_json("migrations.geojson")
    if start is not None and end is not None and start > end:
        return {**collection, "features": []}

    window = _time_window(start, end)
    features = [
        feature
        for feature in collection["features"]
        if _route_matches(
            feature["properties"],
            window=window,
            species_ids=species_ids,
            ocean=ocean,
            depth=depth,
        )
    ]
    return {**collection, "features": features}


def _time_window(start: date | None, end: date | None) -> tuple[date, date, set[int]] | None:
    if start is None and end is None:
        return None
    window_start = start if start is not None else date.min
    window_end = end if end is not None else date.max
    return (window_start, window_end, months_in_window(window_start, window_end))


def _route_matches(
    props: dict,
    *,
    window: tuple[date, date, set[int]] | None,
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
    if window is None:
        return True
    window_start, window_end, months = window
    if date.fromisoformat(props["start"]) > window_end:
        return False
    if date.fromisoformat(props["end"]) < window_start:
        return False
    return bool(months & set(props["months"]))
