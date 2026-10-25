import json
import re
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
# Used when the sightings file has not been merged yet.
OBSERVATION_YEARS = (2006, 2010, 2015, 2020)
_DIET_RE = re.compile(
    r"\b(eats?|eaten|diet|foods?|prey|krill|jellyfish|algae|seagrasses?|sponges?|crabs?)\b",
    re.IGNORECASE,
)
_DIET_KEYS = {"diet", "diets", "food", "foods", "prey", "food_icons", "diet_icons"}


@lru_cache
def load_json(name: str):
    return json.loads((DATA_DIR / name).read_text())


def load_optional(name: str):
    path = DATA_DIR / name
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def species() -> list[dict]:
    """Species records for the map and the per-species depth panel.

    Textboxes are the depth-window facts. Diet and food fields are omitted.
    """
    payload = load_json("species.json")
    records = payload["species"] if isinstance(payload, dict) else payload
    boxes = _textboxes_by_species()
    return [_for_panel(item, boxes) for item in records]


def sources() -> list[dict]:
    """Citation records that species textboxes point to through ``source_ids``."""
    payload = load_json("sources.json")
    if isinstance(payload, dict):
        return payload.get("sources", [])
    return payload


def oceans() -> list[dict]:
    payload = load_json("oceans.json")
    if isinstance(payload, dict):
        return payload.get("oceans", [])
    return payload


def observation_years() -> list[int]:
    sightings = load_optional("animation_sightings.json")
    years = sightings.get("years") if isinstance(sightings, dict) else None
    if years:
        return [int(year) for year in years]
    return list(OBSERVATION_YEARS)


def predictions(species_id: str | None = None, year: int | None = None) -> dict:
    """Sample positions joined to their species labels.

    ``species_year_status`` covers every species, or the one requested. ``year``
    keeps only positions and status entries from that calendar year.
    """
    payload = load_optional("animation_species_predictions.json")
    sightings = load_optional("animation_sightings.json") or {}
    status = sightings.get("species_year_status") or {}
    if species_id:
        status = {species_id: status[species_id]} if species_id in status else {}
    if year is not None:
        year_key = str(year)
        status = {
            sid: {year_key: years[year_key]}
            for sid, years in status.items()
            if isinstance(years, dict) and year_key in years
        }
    years = sightings.get("years") or list(OBSERVATION_YEARS)
    if not isinstance(payload, dict):
        return {
            "data_status": "unavailable",
            "years": years,
            "species_year_status": status,
            "predictions": [],
        }
    by_id = {item["observation_id"]: item for item in sightings.get("sightings", [])}
    rows = []
    for prediction in payload.get("predictions", []):
        if species_id and prediction.get("predicted_species_id") != species_id:
            continue
        sighting = by_id.get(prediction.get("observation_id"), {})
        observed = sighting.get("observed_at_local") or ""
        row_year = int(str(observed)[:4]) if str(observed)[:4].isdigit() else None
        if year is not None and row_year != year:
            continue
        rows.append(
            {
                **prediction,
                "coordinates": sighting.get("coordinates"),
                "observed_at_local": observed or None,
                "year": row_year,
                "month": sighting.get("month"),
            }
        )
    return {**payload, "years": years, "species_year_status": status, "predictions": rows}


def depth_profiles() -> dict:
    payload = load_optional("animation_depth_profiles.json")
    if not isinstance(payload, dict):
        return {"data_status": "unavailable", "species": []}
    return payload


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
    """GeoJSON routes matching the optional filters.

    A dated route is included when one of its positions falls in the window and
    that position's month falls in the window. Older routes that only have
    start/end use the same overlap rule.
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


def _for_panel(item: dict, boxes: dict[str, list[dict]]) -> dict:
    presented = {key: value for key, value in item.items() if key not in _DIET_KEYS}
    textboxes = boxes.get(item["id"])
    if textboxes is None:
        textboxes = _textboxes_from_facts(item.get("facts"))
    presented["textboxes"] = textboxes
    presented["facts"] = [
        fact
        for fact in presented.get("facts", [])
        if isinstance(fact, str) and fact.strip() and not _is_diet(fact)
    ]
    presented["depth_marks"] = _depth_marks(item)
    return presented


def _textboxes_by_species() -> dict[str, list[dict]]:
    payload = load_optional("textboxes.json")
    if not isinstance(payload, dict):
        return {}
    found = {}
    for item in payload.get("species", []):
        boxes = []
        for box in item.get("textboxes", []):
            text = str(box.get("text") or "").strip()
            if not text:
                continue
            boxes.append(
                {
                    "topic": box.get("topic") or "Fact",
                    "text": text,
                    "source_ids": list(box.get("source_ids") or []),
                }
            )
        if boxes:
            found[item["species_id"]] = boxes
    return found


def _textboxes_from_facts(facts) -> list[dict]:
    boxes = []
    for fact in facts or []:
        if isinstance(fact, str):
            text, topic = fact.strip(), "Fact"
        elif isinstance(fact, dict):
            text = str(fact.get("text") or "").strip()
            topic = str(fact.get("topic") or fact.get("id") or "Fact")
        else:
            continue
        if text and not _is_diet(text):
            boxes.append({"topic": topic, "text": text, "source_ids": []})
    return boxes


def _is_diet(text: str) -> bool:
    return _DIET_RE.search(text) is not None


def _depth_marks(item: dict) -> list[dict]:
    depth = item.get("depth_range_m") or {}
    shallow = depth.get("min", depth.get("typical_max"))
    deep = depth.get("max", depth.get("record_max"))
    marks = []
    if isinstance(shallow, int | float) and not isinstance(shallow, bool):
        marks.append({"id": "shallow", "label": "Shallow", "depth_m": shallow})
    if isinstance(deep, int | float) and not isinstance(deep, bool) and deep != shallow:
        marks.append({"id": "deep", "label": "Deep", "depth_m": deep})
    return marks


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
    species_id = props.get("species_id") or props.get("species")
    if species_ids and species_id not in species_ids:
        return False
    if ocean and props.get("ocean") != ocean:
        return False
    if window is None:
        return True
    window_start, window_end, months = window
    points = _dated_points(props)
    if points is not None:
        return any(window_start <= day <= window_end and month in months for day, month in points)
    if "start" not in props or "end" not in props:
        return False
    route_start = date.fromisoformat(str(props["start"])[:10])
    route_end = date.fromisoformat(str(props["end"])[:10])
    if route_start > window_end or route_end < window_start:
        return False
    return bool(months & set(props.get("months") or []))


def _dated_points(props: dict) -> list[tuple[date, int]] | None:
    raw_dates = props.get("dates")
    if not isinstance(raw_dates, list):
        return None
    months = props.get("months") or []
    points = []
    for index, value in enumerate(raw_dates):
        if not value:
            continue
        stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        month = months[index] if index < len(months) else stamp.month
        points.append((stamp.date(), int(month)))
    return points
