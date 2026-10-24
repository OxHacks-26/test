import json
from datetime import date
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
# Years with an observable migration pattern for the seven species.
OBSERVATION_YEARS = (2006, 2010, 2015, 2020)


@lru_cache
def load_json(name: str):
    return json.loads((DATA_DIR / name).read_text())


def species() -> list[dict]:
    """Species records for the map and the per-species depth panel.

    `facts` fills the info textboxes. A `facts` list on the file wins; otherwise
    the panel gets one overview fact from `blurb`. `depth_marks` are the depths
    at which that species is drawn.
    """
    return [_with_depth_panel(item) for item in load_json("species.json")]


def _with_depth_panel(item: dict) -> dict:
    presented = dict(item)
    presented["facts"] = _facts(item)
    presented["depth_marks"] = _depth_marks(item)
    return presented


def _facts(item: dict) -> list[dict]:
    supplied = item.get("facts")
    if isinstance(supplied, list):
        facts = []
        for index, fact in enumerate(supplied, start=1):
            if not isinstance(fact, dict):
                continue
            text = str(fact.get("text") or "").strip()
            if not text:
                continue
            facts.append({"id": str(fact.get("id") or f"fact-{index}"), "text": text})
        if facts:
            return facts
    blurb = str(item.get("blurb") or "").strip()
    if blurb:
        return [{"id": "overview", "text": blurb}]
    return []


def _depth_marks(item: dict) -> list[dict]:
    depth = item.get("depth_range_m") or {}
    typical = depth.get("typical_max")
    record = depth.get("record_max")
    marks = []
    if isinstance(typical, int | float) and not isinstance(typical, bool):
        marks.append({"id": "typical", "label": "Typical depth", "depth_m": typical})
    if isinstance(record, int | float) and not isinstance(record, bool) and record != typical:
        marks.append({"id": "record", "label": "Record depth", "depth_m": record})
    return marks


def oceans() -> list[dict]:
    return load_json("oceans.json")


def observation_years() -> list[int]:
    return list(OBSERVATION_YEARS)


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
) -> dict:
    """GeoJSON FeatureCollection of routes matching the optional filters.

    A route is in a time window when its start-end span overlaps the window,
    at least one of its months falls inside the window, and the window contains
    an observation year (2006, 2010, 2015, or 2020) that the route also covers.
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
) -> bool:
    if species_ids and props["species"] not in species_ids:
        return False
    if ocean and props["ocean"] != ocean:
        return False
    if window is None:
        return True
    window_start, window_end, months = window
    route_start = date.fromisoformat(props["start"])
    route_end = date.fromisoformat(props["end"])
    if route_start > window_end or route_end < window_start:
        return False
    if not _covered_observation_years(route_start, route_end, window_start, window_end):
        return False
    return bool(months & set(props["months"]))


def _covered_observation_years(
    route_start: date, route_end: date, window_start: date, window_end: date
) -> bool:
    """True when an observation year falls in both the route span and the window."""
    for year in OBSERVATION_YEARS:
        year_start = date(year, 1, 1)
        year_end = date(year, 12, 31)
        in_window = year_start <= window_end and year_end >= window_start
        in_route = year_start <= route_end and year_end >= route_start
        if in_window and in_route:
            return True
    return False
