// Map frontend for the sea-turtle year.
//
// Prefers the shared API once it exists, and falls back to the stub files in
// frontend/data so this page can be demoed on its own.
//
//   GET /api/species     -> { species: [...] } or an array
//   GET /api/migrations  -> GeoJSON FeatureCollection of LineStrings
//                           properties: species, name, start, end, source
//   GET /api/oceans      -> { oceans: [...] } or an array
//                           boxes: [[[south, west], [north, east]], ...]
//                           center: [lat, lng], zoom: number

const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

const HOME = { center: [12, -155], zoom: 2 };

const state = {
  species: [],
  routes: [],
  oceans: [],
  month: 3,
  depth: 40,
  hidden: new Set(),
  selectedOcean: null,
  selectedRouteId: null,
  playing: false,
  timer: null,
  illustrative: true,
};

const ui = {
  month: document.getElementById("month"),
  monthLabel: document.getElementById("month-label"),
  play: document.getElementById("play"),
  depth: document.getElementById("depth"),
  depthReadout: document.getElementById("depth-readout"),
  depthSummary: document.getElementById("depth-summary"),
  diveChart: document.getElementById("dive-chart"),
  oceans: document.getElementById("oceans"),
  legend: document.getElementById("legend"),
  routeDetail: document.getElementById("route-detail"),
  sourceNote: document.getElementById("source-note"),
  status: document.getElementById("status"),
};

const OCEAN_SOUTH = -56;
const OCEAN_NORTH = 72;

const map = L.map("map", {
  worldCopyJump: true,
  minZoom: 2,
  zoomControl: false,
  attributionControl: true,
}).setView(HOME.center, HOME.zoom);

// The ocean tiles turn into a flat gray band past these latitudes.
// Keep the view inside the coloured water, and zoomed in far enough
// that the band cannot show above or below the window.
function frameOcean() {
  const limits = L.latLngBounds(
    [OCEAN_SOUTH, -180],
    [OCEAN_NORTH, 180],
  );
  const coverZoom = map.getBoundsZoom(limits, true);
  map.setMinZoom(Math.max(2, coverZoom));
  const center = map.getCenter();
  const lat = Math.min(OCEAN_NORTH, Math.max(OCEAN_SOUTH, center.lat));
  const zoom = Math.max(map.getZoom(), coverZoom);
  if (lat !== center.lat || zoom !== map.getZoom()) {
    map.setView([lat, center.lng], zoom, { animate: false });
  }
}

function clampLatitude() {
  const center = map.getCenter();
  const lat = Math.min(OCEAN_NORTH, Math.max(OCEAN_SOUTH, center.lat));
  if (Math.abs(lat - center.lat) > 0.01) {
    map.panTo([lat, center.lng], { animate: false });
  }
}

map.whenReady(frameOcean);
map.on("resize", frameOcean);
map.on("moveend", clampLatitude);

L.control.zoom({ position: "topright" }).addTo(map);
map.createPane("oceans");
map.getPane("oceans").style.zIndex = 350;

const oceanLayer = L.layerGroup().addTo(map);
const routeLayer = L.layerGroup().addTo(map);

const OCEAN_TILES =
  "https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}";

const tiles = L.tileLayer(OCEAN_TILES, {
  attribution: "Tiles &copy; Esri, GEBCO, NOAA, National Geographic, and others",
  maxZoom: 10,
}).addTo(map);

// bbox is [minLon, minLat, maxLon, maxLat]. Pacific crosses the date line, so minLon > maxLon.
const SEA_REGIONS = [
  {
    id: "southern",
    bbox: [-180, -90, 180, -60],
  },
  {
    id: "arctic",
    bbox: [-180, 65, 180, 90],
  },
  {
    id: "indian",
    bbox: [20, -60, 120, 30],
  },
  {
    id: "atlantic",
    bbox: [-80, -60, 20, 65],
  },
  {
    id: "pacific",
    bbox: [120, -60, -70, 60],
  },
];

function seaAt(latlng) {
  const lat = latlng.lat;
  const lon = wrapLng(latlng.lng);
  return SEA_REGIONS.find((region) => {
    const [minLon, minLat, maxLon, maxLat] = region.bbox;
    if (lat < minLat || lat > maxLat) {
      return false;
    }
    if (minLon <= maxLon) {
      return lon >= minLon && lon <= maxLon;
    }
    return lon >= minLon || lon <= maxLon;
  });
}

const seaWindow = document.getElementById("sea-window");
const seaCard = seaWindow.querySelector(".sea-window-card");
const seaVisual = document.getElementById("sea-visual");
const seaWindowClose = document.getElementById("sea-window-close");
const seaDepthMeters = document.getElementById("sea-depth-meters");
const seaDepthZone = document.getElementById("sea-depth-zone");
const seaDepthSource = document.getElementById("sea-depth-source");
const diveMarks = document.querySelector(".dive-marks");
const diveWater = document.querySelector(".dive-water");

// Pelagic light zones, in metres. The seafloor itself comes from GMRT.
const LIGHT_ZONES = [
  { downTo: 200, name: "Sunlit", color: "var(--sun)" },
  { downTo: 1000, name: "Twilight", color: "var(--sun-2)" },
  { downTo: 4000, name: "Midnight", color: "var(--twilight)" },
  { downTo: 6000, name: "Abyss", color: "var(--midnight)" },
  { downTo: Infinity, name: "Hadal", color: "var(--abyss)" },
];

let diveMap = null;
let seafloorM = null;
let depthRequest = 0;

function formatMeters(meters) {
  return `${Math.round(meters).toLocaleString("en-GB")} m`;
}

function lightZone(meters) {
  return LIGHT_ZONES.find((zone) => meters <= zone.downTo) || LIGHT_ZONES[LIGHT_ZONES.length - 1];
}

function diveFraction() {
  const range = seaVisual.scrollHeight - seaVisual.clientHeight;
  if (range <= 0) {
    return 0;
  }
  return Math.min(1, Math.max(0, seaVisual.scrollTop / range));
}

function renderDive() {
  const progress = diveFraction();
  seaCard.style.setProperty("--progress", progress.toFixed(3));
  const meters = seafloorM == null ? 0 : progress >= 0.995 ? seafloorM : Math.round(progress * seafloorM);
  const lightLoss = seafloorM == null ? 0 : Math.min(1, meters / 1000);
  seaCard.style.setProperty("--dive", lightLoss.toFixed(3));
  if (seafloorM == null) {
    return;
  }
  const atFloor = progress >= 0.995;
  seaDepthMeters.textContent = meters === 0 ? "Surface" : formatMeters(meters);
  seaDepthZone.textContent = atFloor ? "Seafloor" : meters === 0 ? "Open water" : lightZone(meters).name;
}

function depthGradient(depth) {
  const blend = Math.min(80, depth * 0.04);
  const edges = [
    { at: 200, from: "var(--sun)", to: "var(--sun-2)" },
    { at: 1000, from: "var(--sun-2)", to: "var(--twilight)" },
    { at: 4000, from: "var(--twilight)", to: "var(--midnight)" },
    { at: 6000, from: "var(--midnight)", to: "var(--abyss)" },
  ];
  const stops = [
    "transparent 0px",
    "color-mix(in srgb, var(--sun) 50%, transparent) 80px",
    "var(--sun) 170px",
  ];
  const push = (meters, color) => {
    const clamped = Math.min(depth, Math.max(0, meters));
    const along = (clamped / depth).toFixed(4);
    stops.push(`${color} calc(170px + (100% - 170px) * ${along})`);
  };
  push(0, "var(--sun)");
  for (const edge of edges) {
    if (edge.at >= depth) {
      break;
    }
    push(edge.at - blend, edge.from);
    push(edge.at + blend, edge.to);
  }
  push(depth, lightZone(depth).color);
  return `linear-gradient(180deg, ${stops.join(", ")})`;
}

function placeMarks(depth) {
  diveMarks.replaceChildren();
  const range = seaVisual.scrollHeight - seaVisual.clientHeight;
  const columnHeight = seaVisual.scrollHeight;
  if (range <= 0) {
    return;
  }
  const add = (meters, label) => {
    const progress = meters / depth;
    const y = progress * range + seaVisual.clientHeight - 72;
    const item = document.createElement("li");
    item.style.top = `${Math.min(columnHeight - 28, Math.max(0, y))}px`;
    item.textContent = label;
    diveMarks.appendChild(item);
  };
  for (const zone of LIGHT_ZONES) {
    if (zone.downTo < depth - 1) {
      add(zone.downTo, formatMeters(zone.downTo));
    }
  }
  add(depth, `Seafloor ${formatMeters(depth)}`);
}

function applySeafloor(depth) {
  seafloorM = depth;
  const viewHeight = seaVisual.clientHeight || window.innerHeight;
  const column = Math.round(Math.min(viewHeight * 4, Math.max(viewHeight * 0.9, depth * 0.42)));
  diveWater.style.height = `${column}px`;
  diveWater.style.background = depthGradient(depth);
  seaDepthSource.textContent = `Seafloor ${formatMeters(depth)} · GMRT`;
  requestAnimationFrame(() => {
    placeMarks(depth);
    renderDive();
  });
}

function clearDepthScale() {
  seafloorM = null;
  diveWater.style.removeProperty("height");
  diveWater.style.removeProperty("background");
  diveMarks.replaceChildren();
  seaCard.style.setProperty("--dive", "0");
}

async function readElevation(latlng) {
  const params = new URLSearchParams({
    latitude: String(latlng.lat),
    longitude: String(wrapLng(latlng.lng)),
    format: "json",
  });
  const response = await fetch(`https://www.gmrt.org/services/PointServer?${params}`);
  if (!response.ok) {
    throw new Error(`GMRT ${response.status}`);
  }
  const payload = await response.json();
  const elevation = Number(payload.elevation);
  if (!Number.isFinite(elevation)) {
    throw new Error("GMRT returned no elevation");
  }
  return elevation;
}

async function loadSeafloor(latlng) {
  const request = ++depthRequest;
  clearDepthScale();
  seaDepthMeters.textContent = "Reading depth";
  seaDepthZone.textContent = "";
  seaDepthSource.textContent = "";
  try {
    const elevation = await readElevation(latlng);
    if (request !== depthRequest) {
      return;
    }
    if (elevation >= 0) {
      diveWater.style.height = "0px";
      seaDepthMeters.textContent = "Above sea level";
      seaDepthZone.textContent = "No water column";
      return;
    }
    applySeafloor(Math.round(Math.abs(elevation)));
  } catch {
    if (request !== depthRequest) {
      return;
    }
    seaDepthMeters.textContent = "Depth unavailable";
    seaDepthZone.textContent = "";
    seaDepthSource.textContent = "";
  }
}

function ensureDiveMap(latlng) {
  const holder = document.getElementById("sea-dive-map");
  if (!diveMap) {
    diveMap = L.map(holder, {
      zoomControl: false,
      attributionControl: false,
      dragging: false,
      scrollWheelZoom: false,
      doubleClickZoom: false,
      boxZoom: false,
      keyboard: false,
      touchZoom: false,
    });
    L.tileLayer(OCEAN_TILES, { maxZoom: 10 }).addTo(diveMap);
  }
  diveMap.setView([latlng.lat, latlng.lng], 5, { animate: false });
  requestAnimationFrame(() => diveMap.invalidateSize());
}

function openSeaWindow(region, latlng) {
  seaVisual.dataset.region = region.id;
  seaVisual.scrollTop = 0;
  seaWindow.hidden = false;
  ensureDiveMap(latlng);
  loadSeafloor(latlng);
  seaWindowClose.focus();
  window.dispatchEvent(
    new CustomEvent("sea-open", {
      detail: {
        id: region.id,
        lat: latlng.lat,
        lng: latlng.lng,
        visual: seaVisual,
      },
    }),
  );
}

function closeSeaWindow() {
  depthRequest += 1;
  seaWindow.hidden = true;
  seaVisual.scrollTop = 0;
  clearDepthScale();
  seaDepthMeters.textContent = "Surface";
  seaDepthZone.textContent = "Open water";
  seaDepthSource.textContent = "";
  delete seaVisual.dataset.region;
}

seaVisual.addEventListener("scroll", () => {
  renderDive();
}, { passive: true });

window.addEventListener("resize", () => {
  if (seafloorM != null && !seaWindow.hidden) {
    applySeafloor(seafloorM);
  }
});

seaWindowClose.addEventListener("click", closeSeaWindow);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !seaWindow.hidden) {
    closeSeaWindow();
  }
});

map.on("click", (event) => {
  const region = seaAt(event.latlng);
  if (!region) {
    return;
  }
  openSeaWindow(region, event.latlng);
});

let tilesFailed = false;
tiles.on("tileerror", () => {
  if (tilesFailed) {
    return;
  }
  tilesFailed = true;
  map.removeLayer(tiles);
  L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png", {
    attribution: "&copy; OpenStreetMap &copy; CARTO",
    subdomains: "abcd",
    maxZoom: 12,
  }).addTo(map);
});

// The page is the ocean map only until species data and the tracker UI exist.
// Those controls use #month, #depth, #play, #oceans, #legend, and #dive-chart.
// When that markup is on the page, this wires the routes up. It does not call
// the API on its own, and it does not draw the placeholder species.
if (ui.month && ui.depth && ui.play && ui.oceans && ui.legend && ui.diveChart) {
  ui.month.addEventListener("input", () => {
    stopPlayback();
    state.month = Number(ui.month.value);
    render();
  });

  ui.depth.addEventListener("input", () => {
    state.depth = Number(ui.depth.value);
    render();
  });

  ui.play.addEventListener("click", () => {
    if (state.playing) {
      stopPlayback();
      return;
    }
    state.playing = true;
    ui.play.textContent = "Pause";
    ui.play.setAttribute("aria-pressed", "true");
    state.timer = window.setInterval(() => {
      state.month = (state.month + 1) % 12;
      render();
    }, 900);
  });

  init().catch((error) => {
    if (ui.sourceNote) {
      ui.sourceNote.textContent = "The map data could not be loaded.";
    }
    console.error(error);
  });
}

async function init() {
  const [speciesResult, routeResult, oceanResult] = await Promise.all([
    loadFirst("/api/species", "data/species.json", normalizeSpecies),
    loadFirst("/api/migrations", "data/migrations.geojson", normalizeMigrations),
    loadFirst("/api/oceans", "data/oceans.json", normalizeOceans),
  ]);

  state.species = speciesResult.data;
  state.routes = routeResult.data;
  state.oceans = oceanResult.data;
  state.illustrative = speciesResult.fallback || routeResult.fallback || oceanResult.fallback;

  buildOceanControls();
  buildLegend();
  drawOceans();
  map.on("click", (event) => {
    const ocean = oceanAt(event.latlng);
    if (ocean) {
      focusOcean(ocean);
    }
  });
  render();
  checkHealth();
}

async function loadFirst(apiUrl, fallbackUrl, normalize) {
  for (const [url, fallback] of [
    [apiUrl, false],
    [fallbackUrl, true],
  ]) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        continue;
      }
      return { data: normalize(await response.json()), fallback };
    } catch {
      // Try the stub files if the API is missing or shaped differently.
    }
  }
  throw new Error(`Could not load ${fallbackUrl}`);
}

function normalizeSpecies(data) {
  const list = Array.isArray(data) ? data : data.species;
  if (!Array.isArray(list)) {
    throw new Error("species");
  }
  return list.map((item) => ({
    id: item.id,
    commonName: item.common_name || item.commonName || item.name,
    scientificName: item.scientific_name || item.scientificName || "",
    color: safeColor(item.color),
    depthMin: numberOr(item.depth_m && item.depth_m.min, item.depth_min, 0),
    depthMax: numberOr(item.depth_m && item.depth_m.max, item.depth_max, 0),
    typicalDepth: numberOr(item.depth_m && item.depth_m.typical, item.typical_depth, 0),
    diveProfile: item.dive_profile || item.diveProfile || [],
    fact: item.fact || "",
  }));
}

function normalizeMigrations(data) {
  const features = data.features || data.migrations;
  if (!Array.isArray(features)) {
    throw new Error("migrations");
  }
  return features.map((feature, index) => {
    const properties = feature.properties || feature;
    const coordinates = (feature.geometry && feature.geometry.coordinates) || feature.coordinates;
    if (!properties.species || !Array.isArray(coordinates)) {
      throw new Error("route");
    }
    return {
      id: properties.id || `${properties.species}-${index}`,
      species: properties.species,
      name: properties.name || "Corridor",
      start: properties.start,
      end: properties.end,
      source: properties.source || "illustrative, based on published studies",
      coordinates,
    };
  });
}

function normalizeOceans(data) {
  const list = Array.isArray(data) ? data : data.oceans;
  if (!Array.isArray(list)) {
    throw new Error("oceans");
  }
  return list.map((ocean) => ({
    id: ocean.id,
    name: ocean.name,
    center: ocean.center,
    zoom: ocean.zoom || 3,
    boxes: ocean.boxes || (ocean.bounds ? [ocean.bounds] : []),
  }));
}

function buildOceanControls() {
  ui.oceans.replaceChildren();
  ui.oceans.append(oceanButton("World", null));
  for (const ocean of state.oceans) {
    ui.oceans.append(oceanButton(ocean.name, ocean.id));
  }
}

function oceanButton(label, id) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = label;
  button.dataset.ocean = id || "";
  button.setAttribute("aria-pressed", id === null ? "true" : "false");
  button.addEventListener("click", () => {
    if (id === null) {
      focusWorld();
      return;
    }
    focusOcean(state.oceans.find((ocean) => ocean.id === id));
  });
  return button;
}

function buildLegend() {
  ui.legend.replaceChildren();
  for (const species of state.species) {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.setAttribute("aria-pressed", "true");
    const swatch = document.createElement("span");
    swatch.className = "swatch";
    swatch.style.background = species.color;
    const name = document.createElement("span");
    name.className = "species-name";
    name.textContent = species.commonName;
    button.append(swatch, name);
    button.addEventListener("click", () => {
      if (state.hidden.has(species.id)) {
        state.hidden.delete(species.id);
      } else {
        state.hidden.add(species.id);
      }
      render();
    });
    item.append(button);
    ui.legend.append(item);
  }
}

function drawOceans() {
  oceanLayer.clearLayers();
  for (const ocean of state.oceans) {
    for (const box of ocean.boxes) {
      L.rectangle(box, {
        pane: "oceans",
        className: "ocean-box",
        color: "#0e3a4d",
        weight: 1,
        opacity: 0.35,
        fillColor: "#1a6b8a",
        fillOpacity: 0.04,
        interactive: false,
      }).addTo(oceanLayer);
    }
    const icon = L.divIcon({
      className: "ocean-label",
      html: `<span>${escapeHtml(ocean.name)}</span>`,
      iconSize: [120, 24],
      iconAnchor: [60, 12],
    });
    L.marker(ocean.center, { icon, keyboard: true, title: ocean.name })
      .on("click", () => focusOcean(ocean))
      .addTo(oceanLayer);
  }
}

function oceanAt(latlng) {
  return state.oceans.find((ocean) =>
    ocean.boxes.some((box) => {
      const [[south, west], [north, east]] = box;
      return latlng.lat >= south && latlng.lat <= north && latlng.lng >= west && latlng.lng <= east;
    }),
  );
}

function focusOcean(ocean) {
  state.selectedOcean = ocean.id;
  map.setView(ocean.center, ocean.zoom);
  render();
}

function focusWorld() {
  state.selectedOcean = null;
  map.setView(HOME.center, HOME.zoom);
  render();
}

function render() {
  ui.month.value = String(state.month);
  ui.month.setAttribute("aria-valuenow", String(state.month));
  ui.month.setAttribute("aria-valuetext", MONTHS[state.month]);
  ui.monthLabel.textContent = MONTHS[state.month];
  ui.depthReadout.textContent = `${state.depth} m`;
  ui.depth.setAttribute("aria-valuenow", String(state.depth));
  ui.depth.setAttribute("aria-valuetext", `${state.depth} metres`);

  const present = state.species.filter(
    (species) =>
      inDepth(species, state.depth) &&
      !state.hidden.has(species.id) &&
      state.routes.some((route) => route.species === species.id && activeInMonth(route, state.month)),
  );
  ui.depthSummary.textContent = present.length
    ? `On the map at ${state.depth} m: ${present.map((species) => species.commonName).join(", ")}.`
    : `No corridor this month reaches ${state.depth} m.`;

  ui.sourceNote.textContent = state.illustrative
    ? "Illustrative corridors, based on published studies. Not telemetry."
    : "Corridors loaded from the project API.";

  for (const button of ui.oceans.querySelectorAll("button")) {
    const id = button.dataset.ocean || null;
    button.setAttribute("aria-pressed", String(id === state.selectedOcean));
  }

  const buttons = ui.legend.querySelectorAll("button");
  state.species.forEach((species, index) => {
    const button = buttons[index];
    const shown = !state.hidden.has(species.id);
    const inSeason = state.routes.some(
      (route) => route.species === species.id && activeInMonth(route, state.month),
    );
    button.setAttribute("aria-pressed", String(shown));
    button.classList.toggle("is-quiet", shown && (!inSeason || !inDepth(species, state.depth)));
  });

  drawRoutes();
  drawDiveChart();
  updateRouteDetail();
}

function drawRoutes() {
  routeLayer.clearLayers();
  for (const route of state.routes) {
    if (!activeInMonth(route, state.month)) {
      continue;
    }
    const species = state.species.find((item) => item.id === route.species);
    if (!species) {
      continue;
    }
    const shown = !state.hidden.has(species.id);
    const inRange = inDepth(species, state.depth);
    const active = shown && inRange;
    const unwrapped = unwrapCoords(route.coordinates);
    const progress = progressInMonth(route, state.month);
    const traveled = slicePoints(unwrapped, progress);

    const selectRoute = (event) => {
      L.DomEvent.stopPropagation(event);
      state.selectedRouteId = route.id;
      render();
    };
    for (const segment of splitAntimeridian(unwrapped)) {
      L.polyline(segment, {
        color: "#ffffff",
        weight: 7,
        opacity: active ? 0.8 : 0.25,
      })
        .on("click", selectRoute)
        .addTo(routeLayer);
      L.polyline(segment, {
        color: species.color,
        weight: 3,
        opacity: active ? 0.28 : 0.12,
      })
        .on("click", selectRoute)
        .addTo(routeLayer);
    }

    const traveledStyle = {
      color: species.color,
      weight: active ? 4 : 2,
      opacity: active ? 0.95 : 0.16,
    };
    for (const segment of splitAntimeridian(traveled)) {
      if (segment.length < 2) {
        continue;
      }
      L.polyline(segment, traveledStyle).on("click", selectRoute).addTo(routeLayer);
    }

    const tip = traveled[traveled.length - 1];
    if (active && tip) {
      L.circleMarker([tip.lat, wrapLng(tip.lng)], {
        radius: 5.5,
        color: "#ffffff",
        weight: 2,
        fillColor: species.color,
        fillOpacity: 1,
      })
        .on("click", selectRoute)
        .addTo(routeLayer);
    }
  }
}

function updateRouteDetail() {
  const route = state.routes.find((item) => item.id === state.selectedRouteId);
  const species = route && state.species.find((item) => item.id === route.species);
  ui.routeDetail.replaceChildren();
  if (!route || !species || !activeInMonth(route, state.month)) {
    ui.routeDetail.textContent = "Click a coloured path to read the corridor.";
    return;
  }
  const title = document.createElement("strong");
  title.textContent = `${species.commonName}: ${route.name}`;
  const meta = document.createElement("span");
  meta.textContent = ` ${formatRange(route.start, route.end)}. ${species.fact} ${route.source}.`;
  ui.routeDetail.append(title, meta);
}

function drawDiveChart() {
  const width = 320;
  const height = 150;
  const left = 38;
  const right = 8;
  const top = 12;
  const bottom = 8;
  const plotWidth = width - left - right;
  const plotHeight = height - top - bottom;
  const maxDepth = 1200;
  const yFor = (depth) => top + (Math.min(depth, maxDepth) / maxDepth) * plotHeight;
  const xFor = (t) => left + t * plotWidth;
  const parts = [
    `<title id="dive-title">Dive profiles at ${state.depth} metres</title>`,
    `<line x1="${left}" y1="${yFor(0)}" x2="${left}" y2="${yFor(maxDepth)}" stroke="#8aa0ab" stroke-width="1"/>`,
  ];

  for (const tick of [0, 400, 800, 1200]) {
    const y = yFor(tick).toFixed(1);
    parts.push(
      `<text x="${left - 6}" y="${Number(y) + 3}" text-anchor="end" font-size="9" fill="#5c6b73">${tick}</text>`,
      `<line x1="${left}" y1="${y}" x2="${width - right}" y2="${y}" stroke="#eadfd2" stroke-width="1"/>`,
    );
  }

  const depthY = yFor(state.depth).toFixed(1);
  parts.push(
    `<line x1="${left}" y1="${depthY}" x2="${width - right}" y2="${depthY}" stroke="#0e3a4d" stroke-width="1.5" stroke-dasharray="4 3"/>`,
  );

  for (const species of state.species) {
    const present = inDepth(species, state.depth) && !state.hidden.has(species.id);
    const profile = species.diveProfile.length
      ? species.diveProfile
      : [
          { t: 0, depth_m: 0 },
          { t: 0.5, depth_m: species.typicalDepth || species.depthMax },
          { t: 1, depth_m: 0 },
        ];
    const points = profile
      .map((point) => `${xFor(point.t).toFixed(1)},${yFor(point.depth_m).toFixed(1)}`)
      .join(" ");
    parts.push(
      `<polyline points="${points}" fill="none" stroke="${species.color}" stroke-width="${present ? 2.5 : 1.4}" stroke-opacity="${present ? 0.95 : 0.16}" stroke-linejoin="round" stroke-linecap="round"/>`,
    );
  }

  ui.diveChart.innerHTML = parts.join("");
}

function inDepth(species, depth) {
  return depth >= species.depthMin && depth <= species.depthMax;
}

function seasonSpan(route) {
  const start = new Date(`${route.start}T00:00:00Z`).getUTCMonth();
  const end = new Date(`${route.end}T00:00:00Z`).getUTCMonth();
  const length = start <= end ? end - start + 1 : 12 - start + end + 1;
  return { start, end, length };
}

function activeInMonth(route, month) {
  const span = seasonSpan(route);
  if (span.start <= span.end) {
    return month >= span.start && month <= span.end;
  }
  return month >= span.start || month <= span.end;
}

function progressInMonth(route, month) {
  const span = seasonSpan(route);
  const offset = month >= span.start ? month - span.start : month + 12 - span.start;
  return Math.min(1, Math.max(0, (offset + 0.5) / span.length));
}

function formatRange(start, end) {
  const s = new Date(`${start}T00:00:00Z`).getUTCMonth();
  const e = new Date(`${end}T00:00:00Z`).getUTCMonth();
  return `${MONTHS_SHORT[s]}–${MONTHS_SHORT[e]}`;
}

function unwrapCoords(lngLats) {
  const points = [{ lng: lngLats[0][0], lat: lngLats[0][1] }];
  for (let index = 1; index < lngLats.length; index += 1) {
    let lng = lngLats[index][0];
    const previous = points[index - 1].lng;
    while (lng - previous > 180) {
      lng -= 360;
    }
    while (previous - lng > 180) {
      lng += 360;
    }
    points.push({ lng, lat: lngLats[index][1] });
  }
  return points;
}

function slicePoints(points, progress) {
  if (points.length === 1 || progress <= 0) {
    return [points[0]];
  }
  const lengths = [];
  let total = 0;
  for (let index = 1; index < points.length; index += 1) {
    const distance = haversine(points[index - 1], points[index]);
    lengths.push(distance);
    total += distance;
  }
  const target = total * Math.min(progress, 1);
  let covered = 0;
  const sliced = [points[0]];
  for (let index = 0; index < lengths.length; index += 1) {
    const length = lengths[index];
    if (covered + length >= target) {
      const fraction = length === 0 ? 0 : (target - covered) / length;
      const from = points[index];
      const to = points[index + 1];
      sliced.push({
        lng: from.lng + (to.lng - from.lng) * fraction,
        lat: from.lat + (to.lat - from.lat) * fraction,
      });
      return sliced;
    }
    covered += length;
    sliced.push(points[index + 1]);
  }
  return points;
}

function splitAntimeridian(points) {
  if (!points.length) {
    return [];
  }
  const segments = [];
  let current = [[points[0].lat, wrapLng(points[0].lng)]];
  for (let index = 1; index < points.length; index += 1) {
    const previous = points[index - 1];
    const point = points[index];
    const previousEdge = Math.floor((previous.lng + 180) / 360);
    const edge = Math.floor((point.lng + 180) / 360);
    if (previousEdge !== edge && point.lng !== previous.lng) {
      const boundary = (edge > previousEdge ? previousEdge + 1 : previousEdge) * 360 - 180;
      const fraction = (boundary - previous.lng) / (point.lng - previous.lng);
      const lat = previous.lat + (point.lat - previous.lat) * fraction;
      const direction = Math.sign(point.lng - previous.lng) || 1;
      current.push([lat, wrapLng(boundary - direction * 0.0001)]);
      segments.push(current);
      current = [[lat, wrapLng(boundary + direction * 0.0001)]];
    }
    current.push([point.lat, wrapLng(point.lng)]);
  }
  segments.push(current);
  return segments;
}

function haversine(from, to) {
  const radius = 6371;
  const lat1 = (from.lat * Math.PI) / 180;
  const lat2 = (to.lat * Math.PI) / 180;
  const dLat = lat2 - lat1;
  const dLng = ((to.lng - from.lng) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLng / 2) ** 2;
  return 2 * radius * Math.asin(Math.min(1, Math.sqrt(a)));
}

function wrapLng(lng) {
  return (((lng + 180) % 360) + 360) % 360 - 180;
}

function safeColor(color) {
  return typeof color === "string" && /^#[0-9a-fA-F]{6}$/.test(color) ? color : "#335566";
}

function numberOr(first, second, fallback) {
  if (typeof first === "number") {
    return first;
  }
  if (typeof second === "number") {
    return second;
  }
  return fallback;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function stopPlayback() {
  state.playing = false;
  ui.play.textContent = "Play year";
  ui.play.setAttribute("aria-pressed", "false");
  if (state.timer !== null) {
    window.clearInterval(state.timer);
    state.timer = null;
  }
}

async function checkHealth() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    ui.status.textContent = data.status === "ok" ? "API connected" : "API unavailable";
  } catch {
    ui.status.textContent = "API unreachable";
  }
}
