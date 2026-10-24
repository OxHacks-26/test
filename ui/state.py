"""Shared in-memory state for the Turtle Tide interface."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class AppState:
    """Values shared by UI controls and the future map renderer."""

    date: date = field(default_factory=date.today)
    granularity: str = "Months"
    selected_species: set[str] = field(default_factory=set)
    selected_ocean: str = "Pacific"
    depth_range: tuple[int, int] = (0, 300)
    focused_species: str | None = None
    xp: int = 0
    discovered: set[str] = field(default_factory=set)


# Teammates can import this same object to read the current map selections.
state = AppState()
