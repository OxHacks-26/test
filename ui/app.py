"""Run the Turtle Tide demo with ``python ui/app.py``."""

import json
from datetime import date
from pathlib import Path

from nicegui import ui

if __package__:
    from .state import state
    from .theme import COLORS, CSS
else:  # Support direct execution from the repository root.
    from state import state
    from theme import COLORS, CSS

SPECIES = json.loads((Path(__file__).resolve().parents[1] / "data" / "species.json").read_text(encoding="utf-8"))
OCEANS = ["Pacific", "Atlantic", "Indian", "Southern", "Arctic"]
GRANULARITIES = ["Weeks", "Months", "Years", "Decades"]
MIN_DAY = date(2000, 1, 1).toordinal()
MAX_DAY = date(2035, 12, 31).toordinal()
ui.add_css(CSS)


@ui.page("/")
def home() -> None:
    """Build the game dashboard; event handlers mutate the shared state."""
    with ui.column().classes("w-full max-w-[1500px] mx-auto px-5 py-5 gap-4"):
        with ui.row().classes("w-full items-center justify-between flex-wrap gap-3"):
            with ui.row().classes("items-center gap-3"):
                ui.label("🐢").classes("text-4xl")
                with ui.column().classes("gap-0"):
                    ui.label("Turtle Tide").classes("text-3xl font-black text-[#21465b]")
                    ui.label("A little time travel for a big blue planet").classes("text-sm text-[#70909a]")
            with ui.row().classes("items-center gap-2"):
                xp_label = ui.label(f"✨ {state.xp} XP").classes("rounded-full bg-[#fff0b9] px-4 py-2 font-black text-[#9b6a15]")
                ui.label("🔥 4 day streak").classes("rounded-full bg-[#ffe1d4] px-4 py-2 font-black text-[#b75c37]")
                ui.label("❤️ ❤️ ❤️").classes("rounded-full bg-white px-4 py-2 text-lg")

        with ui.row().classes("w-full items-start gap-4 flex-nowrap"):
            # Species chooser and discovery status.
            with ui.card().classes("tt-card w-[245px] min-w-[220px] p-4"):
                ui.label("YOUR TURTLES").classes("text-xs font-black tracking-widest text-[#7a9ba2]")
                species_list = ui.column().classes("w-full gap-2 mt-3")

            with ui.column().classes("min-w-0 flex-1 gap-4"):
                # The map placeholder is deliberately data-independent for now.
                with ui.card().classes("tt-card w-full p-4"):
                    with ui.row().classes("w-full items-center justify-between flex-wrap gap-2"):
                        with ui.column().classes("gap-0"):
                            ui.label("MIGRATION ATLAS").classes("text-xs font-black tracking-widest text-[#7a9ba2]")
                            date_label = ui.label().classes("text-xl font-black text-[#21465b]")
                        ui.label("◉  ILLUSTRATIVE ROUTES").classes("rounded-full bg-[#e5f8ed] px-3 py-2 text-xs font-black text-[#37965c]")
                    with ui.element("div").classes("ocean-map w-full mt-3"):
                        ui.label("NORTH PACIFIC CURRENT").classes("absolute left-[32%] top-[18%] text-[10px] font-black tracking-widest text-white/80")
                        ui.label("🐢").classes("absolute left-[47%] top-[43%] text-4xl drop-shadow")
                        ui.label("🐢").classes("absolute left-[70%] top-[62%] text-3xl drop-shadow")
                        ui.label("🐢").classes("absolute left-[22%] top-[67%] text-2xl drop-shadow")
                        ui.element("div").classes("map-island left-[8%] top-[18%] h-24 w-36 -rotate-12")
                        ui.element("div").classes("map-island right-[8%] top-[10%] h-28 w-40 rotate-12")
                        ui.element("div").classes("map-island right-[12%] bottom-[8%] h-20 w-28 -rotate-6")
                        with ui.row().classes("absolute bottom-3 left-3 rounded-2xl bg-white/90 p-2 shadow-sm"):
                            ui.label("🐢  Following migration paths across the blue").classes("text-xs font-bold text-[#39758a]")
                    with ui.row().classes("items-center gap-2 mt-3 flex-wrap"):
                        ui.label("EXPLORE OCEAN").classes("mr-1 text-[10px] font-black tracking-widest text-[#7a9ba2]")
                        for ocean in OCEANS:
                            ui.button(ocean, on_click=lambda _, name=ocean: open_ocean(name)).props("no-caps unelevated").classes("tt-pill bg-[#e9f7fb] px-3 text-[#367e97]")

                # Time and depth controls share one bar below the map.
                with ui.card().classes("tt-card w-full p-4"):
                    with ui.row().classes("w-full items-center justify-between flex-wrap gap-3"):
                        with ui.row().classes("items-center gap-2"):
                            ui.label("⏳  TIME TRAVEL").classes("text-xs font-black tracking-widest text-[#7a9ba2]")
                            granularity_buttons = {}
                            for granularity in GRANULARITIES:
                                granularity_buttons[granularity] = ui.button(
                                    granularity, on_click=lambda _, value=granularity: set_granularity(value)
                                ).props("no-caps flat").classes("tt-pill text-xs")
                        play_button = ui.button("▶  Play", on_click=lambda: toggle_play()).props("no-caps unelevated").classes("tt-button bg-[#58bd73] px-4 text-white")
                    date_slider = ui.slider(
                        min=MIN_DAY, max=MAX_DAY, step=1, value=state.date.toordinal(),
                        on_change=lambda event: set_date(date.fromordinal(int(event.value))),
                    ).props("label-always color=positive").classes("w-full mt-2")
                    with ui.row().classes("w-full items-center justify-between mt-2 gap-4 flex-wrap"):
                        ui.label("🌊  DIVE DEPTH").classes("text-xs font-black tracking-widest text-[#7a9ba2]")
                        depth_label = ui.label().classes("text-sm font-black text-[#3985a0]")
                    depth_slider = ui.range(
                        min=0, max=1200, step=10,
                        value={"min": state.depth_range[0], "max": state.depth_range[1]},
                        on_change=lambda event: set_depth(event.value),
                    ).props("label-always color=info").classes("w-full")

            # Right-side notes stay tucked away until the player makes a choice.
            info_panel = ui.card().classes("tt-card w-[270px] min-w-[230px] p-4")
            info_panel.set_visibility(False)

    def draw_species() -> None:
        species_list.clear()
        with species_list:
            for turtle in SPECIES:
                discovered = turtle["id"] in state.discovered
                icon = "✅" if discovered else "🔒"
                with ui.card().classes("species-card w-full cursor-pointer border-2 p-3").style(
                    f"border-color: {turtle['color']}55"
                ).on("click", lambda _, item=turtle: open_species(item)):
                    with ui.row().classes("w-full items-center gap-2 no-wrap"):
                        ui.label("🐢").classes("text-2xl")
                        with ui.column().classes("min-w-0 flex-1 gap-0"):
                            ui.label(turtle["name"]).classes("font-black text-[#21465b]")
                            low, high = turtle["depth_range"]
                            ui.label(f"{low}–{high} m depth").classes("text-xs text-[#7a9ba2]")
                        ui.label(icon).classes("text-lg")

    def draw_info(title: str, body: str, extra: str = "") -> None:
        info_panel.clear()
        info_panel.set_visibility(True)
        with info_panel:
            with ui.row().classes("w-full items-center justify-between"):
                ui.label("FIELD NOTES").classes("text-xs font-black tracking-widest text-[#7a9ba2]")
                ui.button("×", on_click=lambda: info_panel.set_visibility(False)).props("flat round dense")
            ui.label(title).classes("mt-3 text-2xl font-black text-[#21465b]")
            ui.label(body).classes("mt-2 text-sm leading-6 text-[#58727e]")
            if extra:
                ui.label(extra).classes("mt-4 rounded-xl bg-[#f1f8f5] p-3 text-xs text-[#6e8d88]")

    def open_species(turtle: dict) -> None:
        first_discovery = turtle["id"] not in state.discovered
        state.focused_species = turtle["id"]
        state.selected_species.add(turtle["id"])
        if first_discovery:
            state.discovered.add(turtle["id"])
            state.xp += 10
            xp_label.text = f"✨ {state.xp} XP"
            ui.notify(f"🎉✨ New turtle discovered! +10 XP ✨🎉", type="positive", position="top")
        draw_species()
        low, high = turtle["depth_range"]
        draw_info(turtle["name"], turtle["fun_fact"], f"Typical depth: {low}–{high} m  ·  Source: {turtle['citation']}")

    def open_ocean(name: str) -> None:
        state.selected_ocean = name
        state.focused_species = None
        draw_info(f"{name} Ocean", f"Explore sea turtle migration routes across the {name.lower()} Ocean.", "Ocean view selected · Illustrative migration atlas")

    def set_date(value: date) -> None:
        state.date = value
        date_label.text = value.strftime("%B %Y")

    def set_granularity(value: str) -> None:
        state.granularity = value
        for name, button in granularity_buttons.items():
            button.props("unelevated" if name == value else "flat")
            button.classes(replace="bg-[#48b8dc] text-white" if name == value else "text-[#62818c]")

    def set_depth(value: dict) -> None:
        state.depth_range = (int(value["min"]), int(value["max"]))
        depth_label.text = f"{state.depth_range[0]}–{state.depth_range[1]} m"

    def advance_time() -> None:
        step = {"Weeks": 7, "Months": 30, "Years": 365, "Decades": 3650}[state.granularity]
        next_day = min(MAX_DAY, state.date.toordinal() + step)
        if next_day == MAX_DAY:
            timer.deactivate()
            play_button.text = "▶  Play"
        date_slider.value = next_day
        set_date(date.fromordinal(next_day))

    def toggle_play() -> None:
        if timer.active:
            timer.deactivate()
            play_button.text = "▶  Play"
        else:
            timer.activate()
            play_button.text = "Ⅱ  Pause"

    timer = ui.timer(1.5, advance_time, active=False)
    draw_species()
    set_date(state.date)
    set_depth({"min": state.depth_range[0], "max": state.depth_range[1]})
    set_granularity(state.granularity)


if __name__ == "__main__":
    ui.run(title="Turtle Tide", favicon="🐢", reload=False)
