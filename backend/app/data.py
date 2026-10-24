import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


@lru_cache
def load_json(name: str):
    return json.loads((DATA_DIR / name).read_text())


def species() -> list[dict]:
    payload = load_json("species.json")
    if isinstance(payload, dict):
        return payload["species"]
    return payload
