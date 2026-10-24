"""Run Turtle Tide with ``python ui/app.py``."""

from datetime import date

from nicegui import ui

if __package__:
    from .state import state
    from .theme import CSS
else:
    from state import state
    from theme import CSS

OCEANS = ["Pacific", "Atlantic", "Indian", "Southern", "Arctic"]
OCEAN_COLORS = {
    "Pacific": ("#35c2d8", "#294d6d"),
    "Atlantic": ("#a69bdf", "#354d70"),
    "Indian": ("#ffb35f", "#574d67"),
    "Southern": ("#67d99c", "#244e5d"),
    "Arctic": ("#f48b9c", "#56445d"),
}
DEPTH_LIMITS = {"Pacific": 4080, "Atlantic": 3646, "Indian": 3741, "Southern": 3270, "Arctic": 1205}
MIN_YEAR = 1995
MAX_YEAR = 2025
YEAR_CHECKPOINTS = list(range(MIN_YEAR, MAX_YEAR + 1, 5))
ui.add_css(CSS, shared=True)


@ui.page("/")
def home() -> None:
    """Build the interactive, data-ready game dashboard."""
    quest_steps: set[str] = set()
    state.date = min(max(state.date, date(MIN_YEAR, 1, 1)), date(MAX_YEAR, 12, 31))
    state.granularity = "5 Years"

    with ui.column().classes("tt-page w-full max-w-[1550px] mx-auto px-5 py-4 gap-3"):
        with ui.row().classes("hud-bar w-full items-center justify-between flex-wrap gap-3"):
            with ui.row().classes("items-center gap-3"):
                ui.label(chr(0x1F422)).classes("brand-icon turtle-mark")
                with ui.column().classes("gap-0"):
                    ui.label("Turtle Tide").classes("game-title")
                    ui.label("Ocean migration console").classes("subtitle")
            with ui.row().classes("items-center gap-2"):
                ui.icon("auto_awesome").classes("hud-star")
                ui.label(f"{state.xp} XP").classes("status-chip xp-chip")
                with ui.row().classes("status-chip heart-chip items-center gap-1"):
                    for _ in range(3):
                        ui.icon("favorite")

        with ui.element("div").classes("fish-drift fish-top"):
            ui.element("div").classes("bubble bubble-a")
            ui.element("div").classes("bubble bubble-b")
            ui.label(chr(0x1F420)).classes("swimming-fish fish-a swim-right")
            ui.label(chr(0x1F41F)).classes("swimming-fish fish-b swim-left")
            ui.label(chr(0x1F421)).classes("swimming-fish fish-c swim-right")

        map_dialog = ui.dialog()
        with map_dialog, ui.card().classes("map-expanded-panel"):
            with ui.row().classes("w-full items-center justify-between"):
                ui.label("Migration map").classes("game-title")
                ui.button("Close", on_click=lambda: map_dialog.close()).props("no-caps")
            with ui.element("div").classes("map-expanded-scroll"):
                ui.element("div").classes("map-expanded-canvas")

        with ui.row().classes("tt-dashboard w-full items-start gap-4 flex-nowrap"):
            with ui.card().classes("tt-card species-column w-[245px] min-w-[220px] p-4"):
                ui.label("TURTLE CREW").classes("section-kicker")
                with ui.column().classes("data-note w-full gap-2 mt-3 p-4"):
                    ui.label(chr(0x1F422)).classes("empty-icon turtle-mark-small")
                    ui.label("Turtle cards are on their way!").classes("font-black")
                    ui.label("Migration data will bring this crew to life.").classes("text-sm leading-5")
                with ui.card().classes("quest-card w-full mt-4 p-4"):
                    ui.label("TODAY'S QUEST").classes("section-kicker")
                    ui.label("Choose an ocean, travel through time, and set your dive depth.").classes("mt-2 text-sm font-bold leading-5")
                    quest_progress = ui.linear_progress(value=0, color="orange").props("rounded track-color=orange-2").classes("tt-progress mt-3")
                    quest_label = ui.label("0 of 3 explorer steps").classes("mt-2 text-xs font-black")

            with ui.column().classes("map-column min-w-0 flex-1 gap-3"):
                with ui.card().classes("tt-card map-card w-full p-4"):
                    with ui.row().classes("w-full items-center justify-between flex-wrap gap-2"):
                        with ui.column().classes("gap-0"):
                            ui.label("MIGRATION ATLAS").classes("section-kicker")
                            date_label = ui.label().classes("date-readout")
                        ui.button("Enlarge map", on_click=lambda: map_dialog.open()).props("no-caps unelevated").classes("tt-button enlarge-button")
                    # The map layer is intentionally blank for the teammate to build.
                    with ui.element("div").classes("map-scroll w-full mt-3"):
                        ui.element("div").classes("ocean-map").on("click", lambda _: map_dialog.open())
                    with ui.row().classes("ocean-picker items-center gap-2 mt-3 flex-wrap"):
                        ui.label("SELECT OCEAN").classes("section-kicker mr-1")
                        ocean_buttons = {}
                        for ocean in OCEANS:
                            ocean_buttons[ocean] = ui.button(
                                ocean, on_click=lambda _, name=ocean: open_ocean(name)
                            ).props("no-caps unelevated").classes("ocean-pill px-3")

                with ui.card().classes("tt-card controls-card w-full p-4"):
                    with ui.row().classes("w-full items-center justify-between flex-wrap gap-3"):
                        with ui.row().classes("items-center gap-2 flex-wrap"):
                            ui.label("TIME TRAVEL").classes("section-kicker")
                            ui.label("5-YEAR CHECKPOINTS").classes("checkpoint-tag")
                        play_button = ui.button("Play", on_click=lambda: toggle_play()).props("no-caps unelevated").classes("tt-button play-button px-4")
                    with ui.row().classes("date-entry-row w-full items-center justify-between gap-3 flex-wrap"):
                        ui.label("Jump to a year").classes("section-kicker")
                        date_input = ui.select(
                            YEAR_CHECKPOINTS,
                            value=state.date.year,
                            on_change=lambda event: on_year_input(event),
                            with_input=True,
                        ).props('popup-content-class="year-popup"').classes("date-input")
                    date_slider = ui.slider(
                        min=MIN_YEAR,
                        max=MAX_YEAR,
                        step=5,
                        value=MIN_YEAR + round((state.date.year - MIN_YEAR) / 5) * 5,
                        on_change=lambda event: set_date(date(int(event.value), 1, 1)),
                    ).props("color=positive").classes("w-full mt-2")
                    with ui.row().classes("w-full items-center justify-between mt-3 gap-3 flex-wrap"):
                        ui.label("DIVE DEPTH").classes("section-kicker")
                        depth_label = ui.label().classes("depth-readout")
                    depth_slider = ui.range(
                        min=0,
                        max=DEPTH_LIMITS[state.selected_ocean],
                        step=1,
                        value={"min": state.depth_range[0], "max": state.depth_range[1]},
                        on_change=lambda event: set_depth(event.value),
                    ).props("label-always color=info").classes("w-full")

                info_panel = ui.card().classes("tt-card info-card w-full p-4")
                info_panel.set_visibility(False)

        with ui.element("div").classes("fish-drift fish-bottom"):
            ui.element("div").classes("bubble bubble-c")
            ui.element("div").classes("bubble bubble-d")
            ui.label(chr(0x1F41F)).classes("swimming-fish fish-d swim-left")
            ui.label(chr(0x1F420)).classes("swimming-fish fish-e swim-right")
            ui.label(chr(0x1F421)).classes("swimming-fish fish-f swim-left")

    def complete_quest_step(step: str) -> None:
        quest_steps.add(step)
        quest_progress.value = len(quest_steps) / 3
        quest_label.text = f"{len(quest_steps)} of 3 explorer steps"

    def draw_info(title: str, body: str) -> None:
        info_panel.clear()
        info_panel.set_visibility(True)
        with info_panel:
            with ui.row().classes("w-full items-center justify-between"):
                ui.label("FIELD NOTES").classes("section-kicker")
                ui.button("Close", on_click=lambda: info_panel.set_visibility(False)).props("no-caps flat dense")
            ui.label(title).classes("mt-2 text-xl font-black")
            ui.label(body).classes("mt-2 text-sm")

    def paint_ocean_buttons() -> None:
        for name, button in ocean_buttons.items():
            bright, dark = OCEAN_COLORS[name]
            selected = name == state.selected_ocean
            button.style(
                f"background:{bright if selected else dark};"
                f"color:{'#17344e' if selected else '#e6f7fa'};"
                f"box-shadow:{'0 4px 0 ' + bright if selected else 'none'};"
                f"transform:{'translateY(-2px)' if selected else 'none'}"
            )

    def open_ocean(name: str) -> None:
        state.selected_ocean = name
        state.focused_species = None
        maximum = DEPTH_LIMITS[name]
        low = min(state.depth_range[0], maximum)
        high = min(state.depth_range[1], maximum)
        depth_slider.props(f"max={maximum}")
        depth_slider.value = {"min": low, "max": max(low, high)}
        set_depth({"min": low, "max": max(low, high)})
        paint_ocean_buttons()
        complete_quest_step("ocean")
        draw_info(name, f"Explore sea turtle migration routes across the {name.lower()} Ocean. Depth range: 0-{maximum:,} m.")

    def set_date(value: date) -> None:
        year = min(max(value.year, MIN_YEAR), MAX_YEAR)
        year = MIN_YEAR + round((year - MIN_YEAR) / 5) * 5
        year = min(MAX_YEAR, max(MIN_YEAR, year))
        value = date(year, 1, 1)
        state.date = value
        date_input.value = year
        date_slider.value = year
        now = date.today()
        years_ago = now.year - value.year
        if years_ago > 0:
            unit = "year" if years_ago == 1 else "years"
            date_label.text = f"{value.year} - {years_ago} {unit} ago"
        elif years_ago < 0:
            date_label.text = f"{value.year} - in {abs(years_ago)} years"
        else:
            date_label.text = f"{value.year} - this year"

    def on_year_input(event) -> None:
        if event.value is not None:
            try:
                year = int(event.value)
                if year in YEAR_CHECKPOINTS:
                    set_date(date(year, 1, 1))
            except (TypeError, ValueError):
                pass

    def set_depth(value: dict) -> None:
        maximum = DEPTH_LIMITS[state.selected_ocean]
        low = min(max(0, int(value["min"])), maximum)
        high = min(max(low, int(value["max"])), maximum)
        state.depth_range = (low, high)
        depth_label.text = f"{low} to {high} m"

    def advance_time() -> None:
        next_year = min(MAX_YEAR, MIN_YEAR + ((state.date.year - MIN_YEAR) // 5 + 1) * 5)
        if next_year == MAX_YEAR:
            timer.deactivate()
            play_button.text = "Play"
        set_date(date(next_year, 1, 1))
        complete_quest_step("time")

    def toggle_play() -> None:
        if timer.active:
            timer.deactivate()
            play_button.text = "Play"
        else:
            timer.activate()
            play_button.text = "Pause"

    timer = ui.timer(1.5, advance_time, active=False)
    set_date(state.date)
    set_depth({"min": state.depth_range[0], "max": state.depth_range[1]})
    paint_ocean_buttons()


if __name__ == "__main__":
    ui.run(title="Turtle Tide", reload=False)
