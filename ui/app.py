"""Run Turtle Tide with ``python ui/app.py``."""

import importlib.util
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import Query
from fastapi.staticfiles import StaticFiles
from nicegui import app, core, ui

if __package__:
    from .state import state
    from .theme import CSS
else:
    from state import state
    from theme import CSS

# Serve the bundled Pixelify Sans body font and Jersey 15 logo font locally.
app.add_static_files("/ui-assets", Path(__file__).resolve().parent / "fonts")

# The migration map (Leaflet) lives in map/ and is shown inside the atlas card in an
# iframe at /map/. It reads the same /api routes the backend serves, so they are
# registered here too and `python ui/app.py` works on its own.
REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("turtle_data", REPO_ROOT / "backend" / "app" / "data.py")
turtle_data = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(turtle_data)


@app.get("/api/health")
def api_health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/species")
def api_species() -> list[dict]:
    return turtle_data.species()


@app.get("/api/sources")
def api_sources() -> list[dict]:
    return turtle_data.sources()


@app.get("/api/migrations")
def api_migrations(
    from_: Annotated[date | None, Query(alias="from")] = None,
    to: Annotated[date | None, Query()] = None,
    species: Annotated[str | None, Query()] = None,
    ocean: Annotated[str | None, Query()] = None,
    year: Annotated[int | None, Query()] = None,
) -> dict:
    start, end = from_, to
    if year is not None:
        year_start, year_end = date(year, 1, 1), date(year, 12, 31)
        start = year_start if start is None else max(start, year_start)
        end = year_end if end is None else min(end, year_end)
    species_ids = {part.strip() for part in species.split(",") if part.strip()} if species else None
    return turtle_data.migrations(
        start=start,
        end=end,
        species_ids=species_ids or None,
        ocean=ocean,
    )


app.mount("/map", StaticFiles(directory=REPO_ROOT / "map", html=True), name="map")

OCEANS = ["Pacific", "Atlantic", "Indian", "Southern", "Arctic"]
DEPTH_LIMITS = {"Pacific": 4080, "Atlantic": 3646, "Indian": 3741, "Southern": 3270, "Arctic": 1205}
OCEAN_WEATHER_POINTS = {
    "Pacific": (8, -160),
    "Atlantic": (12, -35),
    "Indian": (-14, 80),
    "Southern": (-50, 20),
    "Arctic": (66, -20),
}
MIN_YEAR = 2006
MAX_YEAR = 2020
MIN_DATE = date(MIN_YEAR, 1, 1)
MAX_DATE = date(MAX_YEAR, 12, 31)
# Only these four years have data, so they are the only years the timeline offers.
FIVE_YEAR_CHECKPOINTS = (MIN_YEAR, MIN_YEAR + 4, MIN_YEAR + 9, MAX_YEAR)
YEAR_CHECKPOINTS = list(FIVE_YEAR_CHECKPOINTS)
MONTH_NAMES = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
GRANULARITIES = ("5-Year", "Decades")
YEAR_TICKS = FIVE_YEAR_CHECKPOINTS


def timeline_dates(granularity: str) -> list[date]:
    """Return the date stops represented by the selected timeline mode."""
    if granularity == "Decades":
        return [MIN_DATE, MAX_DATE]
    return [date(year, 1, 1) for year in FIVE_YEAR_CHECKPOINTS]


def nearest_timeline_index(value: date, stops: list[date]) -> int:
    """Find the discrete timeline stop nearest a calendar date."""
    return min(range(len(stops)), key=lambda index: abs((stops[index] - value).days))

# Small hand-drawn SVGs keep every decorative icon in one consistent style.
SVG = {
    "turtle": '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M8 12 6 8l5 2a13 13 0 0 1 10 0l5-2-2 5a8 8 0 0 1 2 5H6a8 8 0 0 1 2-6Z"/><path d="M11 14v6m5-8v8m5-6v6M8 22l-2 3m18-3 2 3M13 18h6"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 2.3 7.7L22 12l-7.7 2.3L12 22l-2.3-7.7L2 12l7.7-2.3L12 2Z"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21S3 15.2 3 8.9A4.9 4.9 0 0 1 12 6a4.9 4.9 0 0 1 9 2.9C21 15.2 12 21 12 21Z"/></svg>',
    "fish": '<svg viewBox="0 0 40 24" shape-rendering="crispEdges" aria-hidden="true"><path d="M4 8h5V5h6V3h9v3h6v3h4v3h-4v3h-6v3h-9v-2H9v-3H4l-3-3Z"/><path d="M12 9h2v2h-2Z" fill="#0b2340" stroke="none"/></svg>',
    # Pixel blocks make the cave scenery crisp while staying an inline asset.
    "cave": '<svg viewBox="0 0 1920 1080" preserveAspectRatio="none" aria-hidden="true"><g shape-rendering="crispEdges"><path fill="#10294f" d="M0 0h1920v112h-42v38h-48v-24h-42v56h-54v-32h-50v48h-54v-32h-54v64h-60v-38h-56v34h-58v-58h-44v32h-52v-28h-52v50h-58v-30h-48v22h-64v-48h-58v26h-54v-42h-55v30h-61v-34h-53v27h-49v-41h-54v34h-56v-28h-44v-32H0Z"/><path fill="#163665" d="M0 116h46v54h42v34h38v44h-46v42h56v44h-42v46h58v54h-46v52h54v58h-40v44h52v58h-48v52h62v54h-44v54h44v58h-46v110H0Zm1920 0h-54v46h-44v50h-54v42h52v44h-62v48h48v46h-56v44h60v48h-54v52h48v46h-58v48h60v48h-54v46h58v52h-60v44h58v66h132Z"/><path fill="#20477a" d="M0 183h55v41h47v38H58v42h55v42H66v44h58v44H73v45h60v42H76v46h66v42H85v46h65v48H91v42h62v46H99v44h55v70H0Zm1920 0h-69v39h-47v42h65v39h-57v45h61v42h-52v45h67v42h-61v45h62v45h-57v45h62v44h-62v45h61v45h-60v41h65v70h86Z"/><path fill="#11284e" d="M0 985h198v-36h62v-44h54v-38h58v-34h65v-48h54v-42h68v-28h72v-32h62v-23h576v30h56v37h68v37h54v46h58v42h66v48h73v46h83v134H0Z"/><g fill="#f47fae"><path d="M92 998h12v-34h12v22h12v-42h12v28h12v-18h12v44h12v34H92Zm1680 0h12v-40h12v20h12v-34h12v26h12v-15h12v42h14v34h-86Z"/></g><g fill="#ff817e"><path d="M132 1016h12v-28h10v18h12v-34h12v26h12v18h12v22h-70Zm1550 0h12v-27h12v16h12v-36h12v25h12v22h12v22h-72Z"/></g><g fill="#a678ed"><path d="M48 1048h10v-28h10v-24h10v24h10v28h10v32H48Zm1780 0h10v-28h10v-24h10v24h10v28h10v32h-50ZM310 1044h10v-25h10v-20h10v20h10v25h10v36h-50Zm1300 0h10v-25h10v-20h10v20h10v25h10v36h-50Z"/></g><g fill="#9d65dd"><path d="M235 1018h8v-34h8v-30h8v30h8v34h8v35h-40Zm1430 0h8v-34h8v-30h8v30h8v34h8v35h-40Z"/></g></g></svg>',
    # Extra top-corner overhangs and coral keep the cave art around the full viewport.
    "top_reef": '<svg viewBox="0 0 1920 1080" preserveAspectRatio="none" aria-hidden="true"><g shape-rendering="crispEdges"><path fill="#10294f" d="M0 0h460v48h-52v26h-44v28h-56v-18h-48v42h-62v-28h-54v40h-62v-28h-40v52h-42Zm1920 0h-480v48h54v26h48v28h52v-18h54v42h60v-28h52v40h62v-28h42v52h42Z"/><path fill="#20477a" d="M0 0h224v38h-38v22h-42v27h-48v-18H48v46H0Zm1920 0h-224v38h38v22h42v27h48v-18h48v46h48Z"/><g fill="#f47fae"><path d="M78 164h12v-26h12v18h12v-38h12v24h12v-14h12v38h12v32h-72Zm1662-20h12v-25h12v17h12v-38h12v25h12v-16h12v37h12v34h-72Z"/><path d="M320 126h10v-19h10v15h10v-28h10v19h10v-14h10v27h10v25h-60Zm1250-1h10v-19h10v15h10v-28h10v19h10v-14h10v27h10v25h-60Z"/></g><g fill="#ff817e"><path d="M116 178h10v-22h10v16h10v-34h10v23h10v-14h10v32h10v28h-60Zm1598-20h10v-22h10v16h10v-34h10v23h10v-14h10v32h10v28h-60Z"/><path d="M880 96h10v-20h10v15h10V64h10v23h10V74h10v22h10v24h-60Z"/></g><g fill="#a678ed"><path d="M190 130h10v-20h10v-24h10v24h10v20h10v29h-50Zm1480 0h10v-20h10v-24h10v24h10v20h10v29h-50Zm-770 4h10v-16h10V97h10v21h10v16h10v23h-50Z"/><path d="M520 72h8V54h8V40h8v14h8v18h8v18h-40Zm850 0h8V54h8V40h8v14h8v18h8v18h-40Z"/></g></g></svg>',
    "wave": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 8c3 0 3-3 6-3s3 3 6 3 3-3 6-3m-18 9c3 0 3-3 6-3s3 3 6 3 3-3 6-3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l4 2"/></svg>',
    "depth": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v16m-6-6 6 6 6-6M5 22h14"/></svg>',
    "compass": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2.2 5-4.8 2 2-4.8 5-2.2Z"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3m-4 4v3"/></svg>',
    "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m4 12 5 5L20 6"/></svg>',
    "alert": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2.8 20h18.4L12 3Z"/><path d="M12 9v5m0 3h.01"/></svg>',
    "spinner": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v6h-6"/></svg>',
}
ACHIEVEMENTS = [
    ("first_ocean", "First Current", "Explore an ocean", "wave"),
    ("ocean_hopper", "Ocean Hopper", "Visit all five oceans", "compass"),
    ("time_traveler", "Time Traveler", "Visit another checkpoint", "clock"),
    ("depth_seeker", "Depth Seeker", "Adjust the dive range", "depth"),
    ("deep_diver", "Deep Diver", "Reach below 1,000 m", "spark"),
    ("turtle_tracker", "Turtle Tracker", "Discover a turtle species", "turtle"),
]
# Session achievements stay separate from the teammate-facing shared AppState.
UNLOCKED_BADGES: set[str] = set()
VISITED_OCEANS: set[str] = set()
ui.add_css(CSS, shared=True)
ui.add_css(
    "#map-frame { position:absolute; inset:0; width:100%; height:100%; border:0; display:block; background:#0c3d5c; }"
    "body.tt-dive-open .map-tools, body.tt-dive-open .map-coordinates, body.tt-dive-open #map-modal-close { display:none !important; }"
    # backdrop-filter on the card would trap the enlarged (position:fixed) map inside it.
    "body.map-modal-open .map-card { backdrop-filter:none !important; -webkit-backdrop-filter:none !important; }"
    # The map covers the card, so blurring behind it every frame is wasted work.
    ".map-card { backdrop-filter:none !important; -webkit-backdrop-filter:none !important; background:rgba(10,35,65,.92) !important; }",
    shared=True,
)


def svg_icon(name: str, classes: str = ""):
    """Render one of the local inline SVG icons."""
    return ui.html(SVG[name], sanitize=False).classes(f"svg-icon {classes}")


def run_ui_script(script: str) -> None:
    """Run a browser script once the server loop is up.

    Building the page also calls this, and a test client has no loop yet.
    """
    if core.loop is None:
        return
    ui.run_javascript(script)


@ui.page("/")
def home() -> None:
    """Build the interactive, data-ready game dashboard."""
    quest_steps: set[str] = set()
    if not MIN_DATE <= state.date <= MAX_DATE:
        state.date = MIN_DATE
    state.granularity = "5-Year"
    slider_stops = timeline_dates(state.granularity)
    visited_oceans: set[str] = set(VISITED_OCEANS)
    has_traveled = False
    has_tuned_depth = False

    # Pan the placeholder by moving its repeating background, never its element.
    ui.add_body_html("""
    <script>
      (() => {
        // Warn in the browser console if either bundled face is missing or fails to decode.
        document.fonts.ready.then(async () => {
          for (const [face, sample] of [['Pixelify Sans', '500 18px'], ['Jersey 15', '400 32px']]) {
            const font = `${sample} "${face}"`;
            try {
              await document.fonts.load(font);
              if (!document.fonts.check(font)) console.warn(`[Turtle Tide] ${face} did not load; check ui/fonts and the /ui-assets path.`);
            } catch (error) {
              console.warn(`[Turtle Tide] ${face} did not load; check ui/fonts and the /ui-assets path.`, error);
            }
          }
        });
        let map, coordinateReadout, zoom = 1, panX = 0, panY = 0;
        const pointers = new Map();
        const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        let lastPoint = null, pressPoint = null, pinchStart = 0, pinchZoom = 1;
        let dragged = false, altPress = false, velocityX = 0, velocityY = 0, lastMoveAt = 0, inertiaFrame = 0;
        const TILE = 512, clampZoom = value => Math.min(4, Math.max(.5, value));
        const mod = (value, divisor) => ((value % divisor) + divisor) % divisor;
        const draw = () => {
          if (!map) return;
          const size = TILE * zoom;
          map.style.backgroundSize = `${size}px ${size}px`;
          map.style.backgroundPosition = `${mod(panX, size)}px ${mod(panY, size)}px`;
          if (coordinateReadout) coordinateReadout.textContent = `X ${Math.round(panX)} · Y ${Math.round(panY)} · ${zoom.toFixed(2)}×`;
        };
        const stopInertia = () => { if (inertiaFrame) cancelAnimationFrame(inertiaFrame); inertiaFrame = 0; };
        const startInertia = () => {
          if (reducedMotion.matches || (Math.abs(velocityX) + Math.abs(velocityY) < .025)) return;
          let previous = 0;
          const tick = time => {
            if (!previous) previous = time;
            const elapsed = Math.min(32, time - previous); previous = time;
            panX += velocityX * elapsed; panY += velocityY * elapsed;
            const damping = Math.pow(.91, elapsed / 16);
            velocityX *= damping; velocityY *= damping;
            draw();
            if (Math.abs(velocityX) + Math.abs(velocityY) > .025) inertiaFrame = requestAnimationFrame(tick);
            else inertiaFrame = 0;
          };
          inertiaFrame = requestAnimationFrame(tick);
        };
        const zoomAt = (nextZoom, clientX, clientY) => {
          const rect = map.getBoundingClientRect(), x = clientX - rect.left, y = clientY - rect.top;
          const next = clampZoom(nextZoom), ratio = next / zoom;
          panX = x - (x - panX) * ratio; panY = y - (y - panY) * ratio;
          zoom = next; draw();
        };
        const resized = () => window.dispatchEvent(new CustomEvent('mapResized'));
        // Send a command to the embedded Leaflet map (same origin, see map/app.js).
        window.ttMapCommand = mapCommand;
        function mapCommand(action, extra = {}) {
          const frame = document.getElementById('map-frame');
          if (frame && frame.contentWindow) frame.contentWindow.postMessage({ type: 'tt-map', action, ...extra }, window.location.origin);
        }
        const open = () => {
          if (document.body.classList.contains('map-modal-open')) return;
          document.body.classList.add('map-modal-open');
          window.setTimeout(() => { map.focus(); resized(); }, 340);
        };
        const close = () => {
          if (!document.body.classList.contains('map-modal-open')) return;
          document.body.classList.remove('map-modal-open');
          window.setTimeout(resized, 340);
        };
        document.addEventListener('click', event => {
          if (event.target.closest('#map-enlarge')) open();
          else if (event.target.closest('#map-modal-close') || event.target.closest('#map-modal-backdrop')) close();
          // The real map lives in the #map-frame iframe; these buttons drive it.
          else if (event.target.closest('#map-zoom-in')) mapCommand('zoomIn');
          else if (event.target.closest('#map-zoom-out')) mapCommand('zoomOut');
          else if (event.target.closest('#map-reset')) mapCommand('reset');
        });
        window.addEventListener('message', event => {
          if (event.origin !== window.location.origin || !event.data) return;
          // A dive covers the map, so the page's map buttons step aside while it is open.
          if (event.data.type === 'tt-map-dive') document.body.classList.toggle('tt-dive-open', !!event.data.open);
          if (event.data.type !== 'tt-map-view') return;
          const readout = document.getElementById('map-coordinates');
          if (!readout) return;
          const { lat, lng, zoom: level } = event.data;
          readout.textContent = `${Math.abs(lat).toFixed(1)}°${lat < 0 ? 'S' : 'N'} · ${Math.abs(lng).toFixed(1)}°${lng < 0 ? 'W' : 'E'} · z${level.toFixed(1)}`;
        });
        document.addEventListener('keydown', event => {
          if (event.key === 'Escape' && document.body.classList.contains('map-modal-open')) { close(); return; }
          if (!map || !(document.activeElement === map || document.body.classList.contains('map-modal-open'))) return;
          const key = event.key.toLowerCase(), step = 48;
          if (key === 'arrowleft' || key === 'a') panX += step;
          else if (key === 'arrowright' || key === 'd') panX -= step;
          else if (key === 'arrowup' || key === 'w') panY += step;
          else if (key === 'arrowdown' || key === 's') panY -= step;
          else return;
          event.preventDefault(); draw();
        });
        const attach = () => {
          map = document.getElementById('map');
          if (!map) { window.requestAnimationFrame(attach); return; }
          coordinateReadout = document.getElementById('map-coordinates');
          draw();
          map.addEventListener('pointerdown', event => {
            if (event.pointerType === 'mouse' && event.button !== 0) return;
            stopInertia();
            map.setPointerCapture(event.pointerId);
            const point = {x:event.clientX,y:event.clientY};
            pointers.set(event.pointerId, point);
            if (pointers.size === 1) {
              pressPoint = point; lastPoint = point; dragged = false; altPress = event.altKey;
              velocityX = 0; velocityY = 0; lastMoveAt = performance.now();
            }
            if (pointers.size === 2) {
              const pair = [...pointers.values()];
              pinchStart = Math.hypot(pair[0].x-pair[1].x,pair[0].y-pair[1].y); pinchZoom = zoom;
              dragged = true; velocityX = 0; velocityY = 0;
            }
            map.classList.add('is-dragging');
          });
          map.addEventListener('pointermove', event => {
            if (!pointers.has(event.pointerId)) return;
            const oldPair = [...pointers.values()];
            const oldCenter = oldPair.length > 1 ? {x:(oldPair[0].x+oldPair[1].x)/2,y:(oldPair[0].y+oldPair[1].y)/2} : null;
            pointers.set(event.pointerId, {x:event.clientX,y:event.clientY});
            if (pointers.size > 1) {
              const pair = [...pointers.values()];
              const center = {x:(pair[0].x+pair[1].x)/2,y:(pair[0].y+pair[1].y)/2};
              panX += center.x - oldCenter.x; panY += center.y - oldCenter.y;
              const distance = Math.hypot(pair[0].x-pair[1].x,pair[0].y-pair[1].y);
              if (pinchStart) zoomAt(pinchZoom * distance / pinchStart, center.x, center.y);
            } else if (lastPoint) {
              const dx = event.clientX-lastPoint.x, dy = event.clientY-lastPoint.y, now = performance.now();
              panX += dx; panY += dy;
              if (pressPoint && Math.hypot(event.clientX-pressPoint.x,event.clientY-pressPoint.y) > 5) dragged = true;
              const elapsed = Math.max(1,now-lastMoveAt);
              velocityX = dx/elapsed; velocityY = dy/elapsed; lastMoveAt = now;
              lastPoint = {x:event.clientX,y:event.clientY}; draw();
            }
          });
          const endPointer = event => {
            pointers.delete(event.pointerId);
            if (pointers.size === 1) { lastPoint = [...pointers.values()][0]; pressPoint = lastPoint; velocityX = 0; velocityY = 0; }
            if (!pointers.size) {
              map.classList.remove('is-dragging'); lastPoint = null;
              if (event.type === 'pointerup' && !dragged && pressPoint) zoomAt(zoom * (altPress ? 1/1.5 : 1.5), event.clientX, event.clientY);
              else if (dragged && event.type === 'pointerup') startInertia();
              pressPoint = null;
            }
          };
          map.addEventListener('pointerup', endPointer); map.addEventListener('pointercancel', endPointer);
          map.addEventListener('wheel', event => {
            event.preventDefault(); zoomAt(zoom * Math.exp(-event.deltaY * .001), event.clientX, event.clientY);
          }, {passive:false});
        };
        attach();
      })();
    </script>
    """)

    with ui.column().classes("tt-page w-full max-w-[1550px] mx-auto px-5 py-4 gap-3"):
        ui.html(SVG["cave"], sanitize=False).classes("cave-art")
        ui.html(SVG["top_reef"], sanitize=False).classes("top-reef-art")
        with ui.row().classes("hud-bar glass w-full items-center justify-between flex-wrap gap-3"):
            with ui.row().classes("items-center gap-3"):
                svg_icon("turtle", "brand-icon turtle-mark")
                with ui.column().classes("gap-0"):
                    ui.label("TURTLE TIDE").props('data-text="TURTLE TIDE"').classes("brand-title")
                    ui.label("Ocean migration console").classes("subtitle")
            with ui.column().classes("header-status items-end gap-1"):
                today_label = ui.label(date.today().strftime("%A, %d %B %Y")).classes("today-date")
                weather_label = ui.label("Loading live marine weather…").props("id=tt-live-weather").classes("weather-readout")
                ui.label("Open-Meteo · DWD").classes("weather-credit")
                weather_label.tooltip("Current sea-surface temperature and wave height")
                viewing_label = ui.label().classes("viewing-readout")
        with ui.element("div").classes("fish-drift fish-top"):
            for bubble_name in ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"):
                ui.element("span").classes(f"bubble bubble-{bubble_name}")
            svg_icon("fish", "swimming-fish fish-a swim-right")
            svg_icon("fish", "swimming-fish fish-b swim-left")
            svg_icon("fish", "swimming-fish fish-c swim-right")
            svg_icon("fish", "swimming-fish fish-g swim-left")
            svg_icon("fish", "swimming-fish fish-i swim-right")
            svg_icon("fish", "swimming-fish fish-j swim-left")

        with ui.row().classes("tt-dashboard w-full items-start gap-4"):
            with ui.card().classes("tt-card species-column w-[245px] min-w-[220px] p-4"):
                ui.label("TURTLE CREW").classes("section-kicker")
                crew_box = ui.column().classes("crew-list w-full gap-2 mt-3")
                with ui.card().classes("quest-card glass w-full mt-4 p-4"):
                    ui.label("TODAY'S QUEST").classes("section-kicker")
                    ui.label("Choose an ocean, travel through time, and click the map to find field badge depths.").classes("mt-2 text-sm font-bold leading-5")
                    quest_progress = ui.linear_progress(value=0).props("rounded").classes("tt-progress mt-3")
                    with ui.row().classes("w-full items-center justify-between mt-2"):
                        ui.label("EXPLORER STEPS").classes("quest-progress-caption")
                        quest_label = ui.label("0/3").classes("quest-progress-label")
                with ui.card().classes("achievement-card glass w-full mt-3 p-3"):
                    with ui.row().classes("w-full items-center justify-between"):
                        ui.label("FIELD BADGES").classes("section-kicker")
                        achievement_count = ui.label().classes("badge-count")
                    badge_cards = {}
                    with ui.element("div").classes("badge-grid mt-2"):
                        for key, title, description, icon_name in ACHIEVEMENTS:
                            with ui.element("div").classes("badge-card is-locked") as badge_card:
                                svg_icon(icon_name, "badge-icon")
                                with ui.column().classes("badge-copy gap-0"):
                                    badge_name = ui.label(title).classes("badge-name")
                                    ui.label(description).classes("badge-description")
                                lock_icon = svg_icon("lock", "badge-lock")
                                badge_cards[key] = (badge_card, badge_name, lock_icon)

            with ui.column().classes("map-column min-w-0 flex-1 gap-3"):
                with ui.card().classes("tt-card map-card w-full p-4"):
                    with ui.row().classes("w-full items-center justify-between flex-wrap gap-2"):
                        with ui.column().classes("gap-0"):
                            ui.label("MIGRATION ATLAS").classes("section-kicker")
                            date_label = ui.label().classes("date-readout")
                        enlarge_button = ui.button("Enlarge map").props("id=map-enlarge no-caps unelevated").classes("tt-button enlarge-button")
                        enlarge_button.tooltip("Open the near-fullscreen map view")
                    with ui.row().classes("map-state-wrap w-full"):
                        map_states = {}
                        for key, icon_name, title, description in [
                            ("empty", "wave", "Route data is on its way", "This map is ready for the migration layer."),
                            ("loading", "spinner", "Loading migration routes", "Gathering the selected time and depth slice."),
                            ("error", "alert", "Map data unavailable", "Try again later, or keep exploring another ocean."),
                        ]:
                            with ui.row().classes(f"map-state-panel state-{key} items-center gap-2") as state_panel:
                                svg_icon(icon_name, "map-state-icon")
                                with ui.column().classes("gap-0"):
                                    state_title = ui.label(title).classes("map-state-title")
                                    ui.label(description).classes("map-state-description")
                            state_panel.set_visibility(False)  # the live map has data; panels return for load/error states
                            map_states[key] = (state_panel, state_title)
                    # The Leaflet migration map (map/) fills the #map node through an iframe.
                    with ui.element("div").classes("map-scroll w-full mt-3"):
                        with ui.element("div").props('id=map role=application aria-label="Sea turtle migration map"').classes("ocean-map"):
                            ui.element("iframe").props('id=map-frame src="/map/?embed=1&year=2006" title="Sea turtle migration map"')
                        with ui.row().classes("map-tools items-center gap-2"):
                            ui.button("+").props("id=map-zoom-in no-caps unelevated").classes("map-tool-button").tooltip("Zoom in")
                            ui.button("-").props("id=map-zoom-out no-caps unelevated").classes("map-tool-button").tooltip("Zoom out")
                            ui.button("Reset").props("id=map-reset no-caps unelevated").classes("map-tool-button").tooltip("Reset map view")
                        ui.label("X 0 · Y 0 · 1.00×").props("id=map-coordinates aria-live=polite").classes("map-coordinates")
                with ui.column().classes("ocean-picker glass w-full"):
                    ui.label("SELECT OCEAN").classes("section-kicker")
                    with ui.row().classes("ocean-button-row items-center gap-2 flex-wrap"):
                        ocean_buttons = {}
                        for ocean in OCEANS:
                            ocean_buttons[ocean] = ui.button(
                                ocean, on_click=lambda _, name=ocean: open_ocean(name)
                            ).props("no-caps unelevated").classes("ocean-pill px-3")
                            ocean_buttons[ocean].tooltip(f"Explore the {ocean} Ocean")

                with ui.card().classes("tt-card glass controls-card w-full p-4"):
                    with ui.column().classes("control-grid w-full"):
                        with ui.column().classes("time-controls min-w-0"):
                            with ui.row().classes("w-full items-center justify-between flex-wrap gap-2"):
                                with ui.row().classes("items-center gap-2 flex-wrap"):
                                    ui.label("TIME TRAVEL").classes("section-kicker")
                                    granularity_buttons = {}
                                    for mode in GRANULARITIES:
                                        granularity_buttons[mode] = ui.button(
                                            mode, on_click=lambda _, selected=mode: set_granularity(selected)
                                        ).props("no-caps unelevated").classes("granularity-pill")
                                play_button = ui.button("Play", on_click=lambda: toggle_play()).props("no-caps unelevated").classes("tt-button play-button px-4")
                                play_button.tooltip("Advance the timeline by the selected interval")
                            with ui.row().classes("date-entry-row w-full items-center justify-between gap-2 flex-wrap"):
                                ui.label("Jump to a year").classes("section-kicker")
                                date_input = ui.select(
                                    YEAR_CHECKPOINTS,
                                    value=state.date.year,
                                    on_change=lambda event: on_year_input(event),
                                    with_input=True,
                                ).props('popup-content-class="year-popup"').classes("date-input")
                                date_input.tooltip("Choose 2006, 2010, 2015 or 2020")
                            date_slider = ui.slider(
                                min=0,
                                max=len(slider_stops) - 1,
                                step=1,
                                value=nearest_timeline_index(state.date, slider_stops),
                                on_change=lambda event: on_slider_change(event),
                            ).classes("w-full mt-2")
                            date_slider.tooltip(f"Move through the {MIN_DATE:%Y-%m} to {MAX_DATE:%Y-%m} timeline")
                            with ui.row().classes("timeline-ticks w-full items-center justify-between"):
                                timeline_tick_labels = {}
                                for year in YEAR_TICKS:
                                    timeline_tick_labels[year] = ui.label(str(year)).classes("timeline-tick")
                                timeline_current_label = ui.label().classes("timeline-current")
                        with ui.column().classes("depth-controls min-w-0"):
                            ui.label("DIVE DEPTH").classes("section-kicker")
                            ui.label("Click the map to see what depth earns a field badge.").classes("depth-note")

                info_panel = ui.card().classes("tt-card info-card w-full p-4")
                info_panel.set_visibility(False)

        ui.element("div").props("id=map-modal-backdrop").classes("map-modal-backdrop")
        close_map = ui.button("Close map").props("id=map-modal-close no-caps unelevated").classes("map-modal-close tt-button")
        close_map.tooltip("Close fullscreen map (Esc)")

        with ui.element("div").classes("fish-drift fish-bottom"):
            for bubble_name in ("m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x"):
                ui.element("span").classes(f"bubble bubble-{bubble_name}")
            svg_icon("fish", "swimming-fish fish-d swim-left")
            svg_icon("fish", "swimming-fish fish-e swim-right")
            svg_icon("fish", "swimming-fish fish-f swim-left")
            svg_icon("fish", "swimming-fish fish-h swim-right")
            svg_icon("fish", "swimming-fish fish-k swim-right")
            svg_icon("fish", "swimming-fish fish-l swim-left")

        toast = ui.card().classes("achievement-toast")
        with toast:
            svg_icon("spark", "toast-icon")
            with ui.column().classes("gap-0"):
                ui.label("BADGE UNLOCKED").classes("toast-kicker")
                toast_title = ui.label().classes("toast-title")
            for confetti_index in range(8):
                ui.element("span").classes(f"confetti confetti-{confetti_index}")
        toast.set_visibility(False)

    welcome = ui.dialog().props("persistent")
    with welcome, ui.card().classes("welcome-card"):
        svg_icon("turtle", "welcome-mark")
        ui.label("TURTLE TIDE").props('data-text="TURTLE TIDE"').classes("welcome-title brand-title welcome-brand-title")
        ui.label("Explore migration routes through time and depth.").classes("welcome-copy")
        with ui.column().classes("tutorial-steps w-full"):
            for number, heading, copy in [
                ("01", "Pick an ocean", "Choose a basin to focus your expedition."),
                ("02", "Travel through time", "Move through the timeline in five-year steps."),
                ("03", "Explore depth", "Click the map to see what depth earns a field badge."),
            ]:
                with ui.row().classes("tutorial-step items-center gap-3"):
                    ui.label(number).classes("step-number")
                    with ui.column().classes("gap-0"):
                        ui.label(heading).classes("step-heading")
                        ui.label(copy).classes("step-copy")
        start_button = ui.button("Start exploring", on_click=lambda: dismiss_welcome()).props("no-caps unelevated id=tt-welcome-start").classes("tt-button start-button")
        start_button.tooltip("Start exploring Turtle Tide")
    welcome.open()
    def dismiss_welcome() -> None:
        """Close the tutorial after the user chooses to start exploring."""
        welcome.close()

    def complete_quest_step(step: str) -> None:
        quest_steps.add(step)
        quest_progress.value = len(quest_steps) / 3
        quest_label.text = f"{len(quest_steps)}/3"

    def refresh_header_status(load_weather: bool = False) -> None:
        """Show the real date and current ocean/year selection in the header."""
        viewing_label.text = f"Now viewing: {state.selected_ocean}, {state.date.year}"
        if not load_weather:
            return

        latitude, longitude = OCEAN_WEATHER_POINTS[state.selected_ocean]
        weather_label.text = "Loading live marine weather…"
        script = """
        (() => {
          const weather = document.getElementById('tt-live-weather');
          if (!weather) return;
          const request = (window.ttMarineWeatherRequest || 0) + 1;
          window.ttMarineWeatherRequest = request;
          const url = new URL('https://marine-api.open-meteo.com/v1/marine');
          url.search = new URLSearchParams({
            latitude: '__LATITUDE__', longitude: '__LONGITUDE__',
            current: 'sea_surface_temperature,wave_height',
            timezone: 'auto', cell_selection: 'sea'
          });
          fetch(url, {cache: 'no-store'})
            .then(response => { if (!response.ok) throw new Error('Weather request failed'); return response.json(); })
            .then(data => {
              if (request !== window.ttMarineWeatherRequest) return;
              const current = data.current || {};
              const parts = [];
              if (Number.isFinite(current.sea_surface_temperature)) parts.push(`Sea ${current.sea_surface_temperature.toFixed(1)}°C`);
              if (Number.isFinite(current.wave_height)) parts.push(`Waves ${current.wave_height.toFixed(1)} m`);
              weather.textContent = parts.length ? parts.join(' · ') : 'Live marine weather unavailable';
            })
            .catch(() => {
              if (request === window.ttMarineWeatherRequest) weather.textContent = 'Live marine weather unavailable';
            });
        })();
        """.replace("__LATITUDE__", str(latitude)).replace("__LONGITUDE__", str(longitude))
        run_ui_script(script)

    def refresh_badges() -> None:
        for key, (badge_card, _, lock_icon) in badge_cards.items():
            unlocked = key in UNLOCKED_BADGES
            badge_card.classes(
                add="is-unlocked" if unlocked else "is-locked",
                remove="is-locked" if unlocked else "is-unlocked",
            )
            lock_icon.set_visibility(not unlocked)
        count = sum(key in UNLOCKED_BADGES for key, *_ in ACHIEVEMENTS)
        achievement_count.text = f"{count} / 6"

    def show_achievement_toast(title: str) -> None:
        toast_title.text = title
        toast.set_visibility(True)
        ui.timer(2.8, lambda: toast.set_visibility(False), once=True)

    def unlock_badge(key: str) -> None:
        if key in UNLOCKED_BADGES:
            return
        UNLOCKED_BADGES.add(key)
        state.xp += 10
        refresh_badges()
        title = next(name for badge_key, name, *_ in ACHIEVEMENTS if badge_key == key)
        show_achievement_toast(title)

    def set_map_state(kind: str) -> None:
        """Switch map empty/loading/error status for a future map-data hook."""
        for key, (panel, _) in map_states.items():
            panel.set_visibility(key == kind)

    def draw_info(title: str = "", body: str = "", status: str = "ready") -> None:
        info_panel.clear()
        info_panel.set_visibility(True)
        with info_panel:
            with ui.row().classes("w-full items-center justify-between"):
                with ui.row().classes("items-center gap-2"):
                    icon_name = {"empty": "wave", "loading": "spinner", "error": "alert"}.get(status, "compass")
                    svg_icon(icon_name, "info-state-icon")
                    ui.label("FIELD NOTES").classes("section-kicker")
                close_info = ui.button("Close", on_click=lambda: info_panel.set_visibility(False)).props("no-caps flat dense")
                close_info.tooltip("Close field notes")
            default_title = {"empty": "No field notes yet", "loading": "Preparing field notes", "error": "Field notes unavailable"}.get(status, "Field notes")
            default_body = {
                "empty": "Choose an ocean or turtle to see details here.",
                "loading": "Loading details for this expedition.",
                "error": "We could not load these details. Try another selection.",
            }.get(status, "")
            ui.label(title or default_title).classes("mt-2 text-xl font-black")
            ui.label(body or default_body).classes("mt-2 text-sm")
            if status == "loading":
                ui.linear_progress(value=None).classes("state-progress mt-2")

    def paint_ocean_buttons() -> None:
        for name, button in ocean_buttons.items():
            selected = name == state.selected_ocean
            background = "var(--c-cyan)" if selected else "var(--c-teal)"
            button.style(
                f"background:{background};"
                f"color:var(--c-navy);"
                f"box-shadow:var(--shadow-raised);"
            )

    def open_ocean(name: str) -> None:
        state.selected_ocean = name
        state.focused_species = None
        refresh_header_status(load_weather=True)
        visited_oceans.add(name)
        VISITED_OCEANS.add(name)
        unlock_badge("first_ocean")
        if len(visited_oceans) == len(OCEANS):
            unlock_badge("ocean_hopper")
        maximum = DEPTH_LIMITS[name]
        low = min(state.depth_range[0], maximum)
        high = min(state.depth_range[1], maximum)
        set_depth({"min": low, "max": max(low, high)}, record=False)
        paint_ocean_buttons()
        run_ui_script(f"window.ttMapCommand && window.ttMapCommand('ocean', {{ocean: '{name.lower()}'}})")
        complete_quest_step("ocean")
        draw_info(name, f"Explore sea turtle migration routes across the {name.lower()} Ocean. Depth range: 0-{maximum:,} m.")

    def refresh_timeline_marks() -> None:
        """Keep the fixed reference ticks and active year in sync with the slider."""
        current_year = state.date.year
        if state.granularity == "Decades":
            tick_text = {MIN_YEAR: "2000s", MAX_YEAR: "2010s"}
            active_bucket = MIN_YEAR if current_year < MAX_YEAR - 10 else MAX_YEAR
            for year, label in timeline_tick_labels.items():
                label.text = tick_text.get(year, str(year))
                label.set_visibility(year in tick_text)
                label.classes(
                    add="is-current" if year == active_bucket else "",
                    remove="is-current" if year != active_bucket else "",
                )
            timeline_current_label.text = str(current_year)
            timeline_current_label.set_visibility(True)
        else:
            for year, label in timeline_tick_labels.items():
                label.text = str(year)
                label.set_visibility(True)
                label.classes(
                    add="is-current" if year == current_year else "",
                    remove="is-current" if year != current_year else "",
                )
            timeline_current_label.text = str(current_year) if current_year not in YEAR_TICKS else ""
            timeline_current_label.set_visibility(current_year not in YEAR_TICKS)

    def paint_granularity_buttons() -> None:
        for mode, button in granularity_buttons.items():
            active = mode == state.granularity
            button.style(
                f"background:{'var(--c-cyan)' if active else 'var(--c-teal)'};"
                f"color:{'var(--c-navy)' if active else 'white'};"
            )

    def render_crew(year: int) -> None:
        """One card per species for the chosen year, from the sample positions."""
        crew_box.clear()
        positions: dict[str, list[dict]] = {}
        payload = turtle_data.predictions(year=year)
        for item in payload.get("predictions", []):
            positions.setdefault(item["predicted_species_id"], []).append(item)
        with crew_box:
            for species in turtle_data.species():
                rows = sorted(positions.get(species["id"], []), key=lambda item: item.get("month", 0))
                with ui.column().classes("crew-card w-full gap-1 p-3").style(f"border-left:4px solid {species['colour']}"):
                    ui.label(species["common_name"]).classes("crew-name")
                    ui.label(species["scientific_name"]).classes("crew-latin")
                    if not rows:
                        ui.label(f"No sample route for {year}").classes("crew-row")
                    for item in rows:
                        lng, lat = item["coordinates"]
                        kind = "Nesting" if "nesting" in item.get("rationale", "").lower() else "Foraging"
                        month = MONTH_NAMES[item["month"] - 1] if item.get("month") else ""
                        place = f"{abs(lat):.1f}°{'N' if lat >= 0 else 'S'} {abs(lng):.1f}°{'E' if lng >= 0 else 'W'}"
                        ui.label(f"{kind} · {month} · {place}").classes("crew-row")
            ui.label(f"Illustrative sample positions for {year}, not observed tracking.").classes("crew-note")

    def set_date(value: date, record: bool = True) -> None:
        nonlocal has_traveled
        value = min(max(value, MIN_DATE), MAX_DATE)
        slider_index = nearest_timeline_index(value, slider_stops)
        value = slider_stops[slider_index]
        changed = value != state.date
        state.date = value
        date_input.value = value.year
        run_ui_script(f"window.ttMapCommand && window.ttMapCommand('year', {{year: {value.year}}})")
        date_slider.value = slider_index
        refresh_header_status()
        render_crew(value.year)
        if value.year >= MAX_YEAR:
            date_label.text = f"{MAX_YEAR} - Latest data"
        else:
            years_before = MAX_YEAR - value.year
            unit = "year" if years_before == 1 else "years"
            date_label.text = f"{value.year} - {years_before} {unit} before {MAX_YEAR}"
        refresh_timeline_marks()
        if record and changed and not has_traveled:
            has_traveled = True
            unlock_badge("time_traveler")

    def set_granularity(mode: str) -> None:
        nonlocal slider_stops
        if mode not in GRANULARITIES:
            return
        state.granularity = mode
        slider_stops = timeline_dates(mode)
        date_slider.props(f"min=0 max={len(slider_stops) - 1} step=1")
        set_date(state.date, record=False)
        paint_granularity_buttons()

    def on_slider_change(event) -> None:
        index = min(max(round(float(event.value)), 0), len(slider_stops) - 1)
        set_date(slider_stops[index])

    def on_year_input(event) -> None:
        if event.value is not None:
            try:
                year = int(event.value)
                if year in YEAR_CHECKPOINTS:
                    set_date(date(year, 1, 1))
            except (TypeError, ValueError):
                pass

    def set_depth(value: dict, record: bool = True) -> None:
        nonlocal has_tuned_depth
        maximum = DEPTH_LIMITS[state.selected_ocean]
        low = min(max(0, int(value["min"])), maximum)
        high = min(max(low, int(value["max"])), maximum)
        changed = (low, high) != state.depth_range
        state.depth_range = (low, high)
        if record and changed:
            if not has_tuned_depth:
                has_tuned_depth = True
                unlock_badge("depth_seeker")
            if high >= 1000:
                unlock_badge("deep_diver")

    def advance_time() -> None:
        next_index = (nearest_timeline_index(state.date, slider_stops) + 1) % len(slider_stops)
        set_date(slider_stops[next_index])
        complete_quest_step("time")

    def toggle_play() -> None:
        if timer.active:
            timer.deactivate()
            play_button.text = "Play"
        else:
            timer.activate()
            play_button.text = "Pause"

    timer = ui.timer(1.5, advance_time, active=False)
    draw_info(status="empty")
    info_panel.set_visibility(False)
    set_date(state.date, record=False)
    paint_granularity_buttons()
    set_depth({"min": state.depth_range[0], "max": state.depth_range[1]}, record=False)
    if state.discovered:
        unlock_badge("turtle_tracker")
    refresh_badges()
    paint_ocean_buttons()
    refresh_header_status(load_weather=True)


if __name__ == "__main__":
    # show=False: NiceGUI's automatic browser launch crashes in this environment
    # and leaves an untitled tab that never finishes loading. Open the printed URL.
    ui.run(title="Turtle Tide", host="0.0.0.0", port=8080, reload=False, show=False)
