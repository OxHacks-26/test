// Top-down field marks. These are not the design colours in species.json.
// Costal pairs: green 4, loggerhead 5, hawksbill 4 overlapping,
// Kemp's ridley 5, olive ridley 6+, flatback 4.
// Leatherback has no scutes, seven ridges, and long front flippers.
// Prefrontal pairs: green and flatback 1, the others 2.
// Hawksbill adds a pointed beak and a serrated rear margin.

const TURTLE_LOOK = {
  green: {
    shell: "#5e6b3c",
    dark: "#3a4424",
    skin: "#cbb892",
    rx: 22,
    ry: 28,
    head: 6.8,
    costals: 4,
    prefrontals: 1,
    reach: 1,
    stroke: "1.15s",
    size: 50,
  },
  loggerhead: {
    shell: "#8d4e2c",
    dark: "#5c3018",
    skin: "#d7a36a",
    rx: 21,
    ry: 26,
    head: 9.2,
    costals: 5,
    prefrontals: 2,
    reach: 1,
    stroke: "1.2s",
    size: 50,
  },
  leatherback: {
    shell: "#1a2330",
    dark: "#0e141c",
    skin: "#243140",
    spot: "#d5d0c4",
    ridges: 7,
    rx: 18,
    ry: 32,
    head: 6.4,
    reach: 1.28,
    stroke: "1.45s",
    size: 62,
  },
  hawksbill: {
    shell: "#c4843a",
    dark: "#6e3e16",
    mottle: "#f0d7a0",
    skin: "#e2c48a",
    rx: 20,
    ry: 26,
    head: 7,
    costals: 4,
    prefrontals: 2,
    beak: true,
    serrated: true,
    overlap: true,
    reach: 1,
    stroke: "1.05s",
    size: 44,
  },
  "kemps-ridley": {
    shell: "#7d8a72",
    dark: "#4e5948",
    skin: "#ddd4c0",
    rx: 22,
    ry: 22,
    head: 6.6,
    costals: 5,
    prefrontals: 2,
    reach: 1,
    stroke: "0.82s",
    size: 36,
  },
  "olive-ridley": {
    shell: "#6d734c",
    dark: "#434832",
    skin: "#cfc3a4",
    rx: 22,
    ry: 23,
    head: 6.8,
    costals: 6,
    prefrontals: 2,
    reach: 1,
    stroke: "0.95s",
    size: 40,
  },
  flatback: {
    shell: "#a3aa8c",
    dark: "#5e6854",
    skin: "#ead9b4",
    rim: "#f3ecda",
    rx: 25,
    ry: 23,
    head: 7,
    costals: 4,
    prefrontals: 1,
    reach: 1,
    stroke: "1.12s",
    size: 48,
  },
};

const TURTLE_MONTHS = [
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

const TURTLE_YEAR_MS = 22000;
const TURTLE_HOLD_MS = 1600;

function turtleAppearance(id) {
  return TURTLE_LOOK[id];
}

// Side-on turtle art. Colours come from TURTLE_LOOK (field colours, not the
// design hex in species.json). Shading is a neutral light/dark overlay so the
// species colour stays true instead of shifting toward grey.
function sideTurtleSvg(id) {
  const look = TURTLE_LOOK[id];
  if (!look) {
    return "";
  }
  const uid = `st-${id}`;
  const leather = Boolean(look.ridges);
  const shellPath = sideShellPath(id);
  const flipperPath = "M116 48 C112 58, 94 70, 72 80 C66 83, 70 88, 78 86 C98 82, 116 72, 122 58 Z";
  const rearPath = "M54 52 C42 54, 32 64, 35 74 C41 78, 54 72, 62 60 Z";
  const reach = leather ? 1.3 : 1;
  const flipperXf = `translate(116 52) scale(${reach}) translate(-116 -52)`;
  const farXf = `translate(8 3) translate(116 52) scale(${reach}) translate(-116 -52)`;
  const head = sideHead(id, look);
  const body = leather ? leatherBody(look) : hardShellBody(look, uid, id);
  const scaleLines = (path, opacity) => `<path d="${path}" fill="none" stroke="${look.dark}" stroke-width="0.7" opacity="${opacity}" stroke-linecap="round"/>`;
  const flipperMarks = leather
    ? ""
    : scaleLines("M112 56 C104 62, 92 70, 80 78", 0.35) + scaleLines("M116 60 C108 66, 98 72, 88 80", 0.3);
  return `<svg class="side-turtle" viewBox="0 0 180 96" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
    <defs>
      <linearGradient id="${uid}-lit" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ffffff" stop-opacity="0.26"/>
        <stop offset="0.45" stop-color="#ffffff" stop-opacity="0"/>
        <stop offset="1" stop-color="#000000" stop-opacity="0.4"/>
      </linearGradient>
      <radialGradient id="${uid}-spec" cx="0.42" cy="0.18" r="0.55">
        <stop offset="0" stop-color="#ffffff" stop-opacity="${leather ? 0.28 : 0.2}"/>
        <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
      </radialGradient>
      <clipPath id="${uid}-clip"><path d="${shellPath}"/></clipPath>
    </defs>
    <g class="side-body">
      <g transform="${farXf}">
        <path d="${flipperPath}" fill="${look.skin}"/>
        <path d="${flipperPath}" fill="#000000" opacity="0.42"/>
      </g>
      <path d="M104 34 C112 30, 122 32, 128 38 L130 52 C122 56, 110 56, 102 50 Z" fill="${look.skin}"/>
      <path d="M104 34 C112 30, 122 32, 128 38 L130 52 C122 56, 110 56, 102 50 Z" fill="url(#${uid}-lit)"/>
      <path d="${rearPath}" fill="${look.skin}"/>
      <path d="${rearPath}" fill="url(#${uid}-lit)"/>
      ${body}
      <g transform="${flipperXf}">
        <path d="${flipperPath}" fill="${look.skin}"/>
        <path d="${flipperPath}" fill="url(#${uid}-lit)"/>
        ${flipperMarks}
        <path d="${flipperPath}" fill="none" stroke="${look.dark}" stroke-width="0.6" opacity="0.6"/>
      </g>
      ${head}
    </g>
  </svg>`;
}

function hardShellBody(look, uid, id) {
  const count = look.costals || 4;
  let seams = "";
  for (let i = 1; i < count; i += 1) {
    const x = 42 + (80 * i) / count;
    seams += `<path d="M${x + 7} 10 C${x + 4} 30, ${x} 46, ${x - 8} 72" fill="none" stroke="${look.dark}" stroke-width="1" opacity="0.5"/>`;
  }
  seams += `<path d="M38 31 C62 23, 100 23, 128 37" fill="none" stroke="${look.dark}" stroke-width="1" opacity="0.5"/>`;
  seams += `<path d="M40 56 C62 63, 100 63, 120 54" fill="none" stroke="${look.dark}" stroke-width="5" stroke-dasharray="1.2 6.5" opacity="0.35"/>`;
  let mottle = "";
  if (look.mottle) {
    const marks = [[56, 34, 20], [74, 28, 8], [90, 40, 30], [66, 48, -14], [104, 34, -8], [84, 52, 18], [50, 46, 40], [112, 46, 10]];
    mottle = marks
      .map(([x, y, rot]) => `<ellipse cx="${x}" cy="${y}" rx="7" ry="2.4" transform="rotate(${rot} ${x} ${y})" fill="${look.dark}" opacity="0.38"/>`)
      .join("");
    mottle += `<ellipse cx="82" cy="30" rx="16" ry="3" fill="${look.mottle}" opacity="0.4"/>`;
  }
  const rim = look.rim
    ? `<path d="${sideShellPath(id)}" fill="none" stroke="${look.rim}" stroke-width="2.6" stroke-linejoin="round"/>`
    : "";
  return `<path d="M44 57 C64 66, 102 66, 120 55 C102 61, 62 62, 44 57 Z" fill="${look.skin}" opacity="0.95"/>
      <g clip-path="url(#${uid}-clip)">
        <rect x="0" y="0" width="180" height="96" fill="${look.shell}"/>
        ${mottle}
        ${seams}
        <rect x="0" y="0" width="180" height="96" fill="url(#${uid}-lit)"/>
        <ellipse cx="82" cy="32" rx="40" ry="16" fill="url(#${uid}-spec)"/>
      </g>
      <path d="${sideShellPath(id)}" fill="none" stroke="${look.dark}" stroke-width="1.3" stroke-linejoin="round" opacity="0.85"/>
      ${rim}`;
}

function leatherBody(look) {
  let ridges = "";
  for (let k = 0; k < 7; k += 1) {
    const y0 = 27 + k * 4;
    ridges += `<path d="M118 ${y0} C90 ${y0 - 6 + k * 0.7}, 48 ${y0 - 2 + k * 1.5}, 16 53" fill="none" stroke="#b9c2cc" stroke-width="${k === 3 ? 1.1 : 0.8}" opacity="0.5" stroke-linecap="round"/>`;
  }
  const spots = [[60, 38], [76, 33], [92, 31], [70, 46], [88, 44], [104, 38], [50, 46], [110, 46]]
    .map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.1" fill="${look.spot}" opacity="0.7"/>`)
    .join("");
  return `<g clip-path="url(#st-leatherback-clip)">
        <rect x="0" y="0" width="180" height="96" fill="${look.shell}"/>
        ${ridges}
        ${spots}
        <rect x="0" y="0" width="180" height="96" fill="url(#st-leatherback-lit)"/>
        <ellipse cx="80" cy="30" rx="40" ry="12" fill="url(#st-leatherback-spec)"/>
      </g>
      <path d="${sideShellPath("leatherback")}" fill="none" stroke="${look.dark}" stroke-width="1.2" opacity="0.8"/>`;
}

function sideHead(id, look) {
  const shapes = {
    default: {
      path: "M124 36 C130 28, 144 28, 152 34 C158 38, 156 46, 150 48 C144 50, 134 50, 128 49 C122 46, 120 40, 124 36 Z",
      mouth: "M134 46 C142 47, 149 46, 154 42",
      eye: [143, 35],
      scale: 1,
    },
    loggerhead: {
      path: "M124 36 C130 28, 144 28, 152 34 C158 38, 156 46, 150 48 C144 50, 134 50, 128 49 C122 46, 120 40, 124 36 Z",
      mouth: "M134 46 C142 47, 149 46, 154 42",
      eye: [143, 35],
      scale: 1.24,
    },
    hawksbill: {
      path: "M124 37 C130 31, 144 31, 154 36 C162 40, 167 45, 166 49 C158 49, 150 49, 142 49 C134 51, 126 51, 123 46 Z",
      mouth: "M136 47 C146 48, 156 48, 163 46",
      eye: [143, 37],
      scale: 1,
    },
    leatherback: {
      path: "M124 38 C130 31, 142 31, 148 36 C152 40, 150 47, 144 49 C138 51, 130 51, 126 48 Z",
      mouth: "M134 47 C140 48, 146 47, 149 44",
      eye: [141, 37],
      scale: 1,
    },
    flatback: {
      path: "M124 37 C130 30, 143 30, 150 35 C155 39, 153 46, 148 48 C142 50, 134 50, 128 49 C123 46, 121 41, 124 37 Z",
      mouth: "M134 46 C141 47, 147 46, 151 43",
      eye: [141, 36],
      scale: 0.92,
    },
  };
  const spec = shapes[id] || shapes.default;
  const uid = `st-${id}`;
  const [ex, ey] = spec.eye;
  const crown = id === "leatherback"
    ? `<ellipse cx="134" cy="33" rx="4" ry="1.8" fill="#e4a4a0" opacity="0.55"/>`
    : `<path d="M130 34 C134 32, 140 32, 144 34" fill="none" stroke="${look.dark}" stroke-width="0.6" opacity="0.45"/>
       <path d="M128 40 C132 38, 136 38, 140 40" fill="none" stroke="${look.dark}" stroke-width="0.6" opacity="0.35"/>`;
  const hook = id === "hawksbill"
    ? `<path d="M160 41 C165 42, 168 46, 165 50" fill="none" stroke="${look.dark}" stroke-width="1.2" stroke-linecap="round"/>`
    : "";
  const notch = id === "leatherback"
    ? `<path d="M147 43 L149 47 L145 46 Z" fill="${look.dark}" opacity="0.7"/>`
    : "";
  const xf = spec.scale === 1
    ? ""
    : ` transform="translate(124 42) scale(${spec.scale}) translate(-124 -42)"`;
  return `<g${xf}>
      <path d="${spec.path}" fill="${look.skin}"/>
      <path d="${spec.path}" fill="url(#${uid}-lit)"/>
      ${crown}
      <path d="${spec.mouth}" fill="none" stroke="${look.dark}" stroke-width="0.9" stroke-linecap="round" opacity="0.8"/>
      ${hook}
      ${notch}
      <circle cx="${ex}" cy="${ey}" r="2.1" fill="#1b120c"/>
      <circle cx="${ex + 0.7}" cy="${ey - 0.7}" r="0.6" fill="#ffffff" opacity="0.9"/>
      <path d="M${ex - 3.4} ${ey - 2.4} C${ex - 1} ${ey - 4}, ${ex + 2} ${ey - 4}, ${ex + 3.6} ${ey - 2.6}" fill="none" stroke="${look.dark}" stroke-width="0.7" opacity="0.6"/>
      <path d="${spec.path}" fill="none" stroke="${look.dark}" stroke-width="0.6" opacity="0.6"/>
    </g>`;
}

function sideShellPath(id) {
  if (id === "leatherback") {
    return "M12 54 C26 34, 70 18, 118 26 C134 30, 134 46, 118 54 C90 66, 36 68, 12 54 Z";
  }
  if (id === "hawksbill") {
    return "M34 52 L29 48 L36 46 L30 41 L38 38 C44 26, 66 18, 94 18 C116 18, 128 32, 122 48 C118 58, 100 62, 82 62 C60 62, 44 60, 34 52 Z";
  }
  if (id === "kemps-ridley" || id === "olive-ridley") {
    return "M42 48 C42 28, 64 18, 90 18 C114 18, 128 30, 122 48 C118 58, 98 62, 80 62 C58 62, 44 60, 42 48 Z";
  }
  if (id === "flatback") {
    return "M32 50 C34 37, 62 31, 92 31 C116 31, 128 39, 124 50 C120 58, 100 62, 78 62 C54 62, 34 60, 32 50 Z";
  }
  return "M36 50 C34 30, 62 18, 94 18 C116 18, 128 32, 122 48 C118 58, 100 62, 80 62 C58 62, 38 60, 36 50 Z";
}

// One route per species is drawn for the selected sample year. The other
// years stay off the map so the four versions of a corridor do not stack.
const MIGRATION_YEARS = [2006, 2010, 2015, 2020];

function migrationYearFromPage() {
  const requested = Number(new URLSearchParams(window.location.search).get("year"));
  return MIGRATION_YEARS.includes(requested) ? requested : 2020;
}

let migrationYear = migrationYearFromPage();
window.migrationYear = migrationYear;

window.setMigrationYear = (year) => {
  const next = Number(year);
  if (!MIGRATION_YEARS.includes(next) || next === migrationYear) {
    return;
  }
  migrationYear = next;
  window.migrationYear = next;
  if (window.__refreshMigrationYear) {
    window.__refreshMigrationYear();
  }
};

function mountTurtles(map) {
  const monthLabel = document.getElementById("turtle-month");
  const layer = L.layerGroup().addTo(map);
  loadTurtles(map, layer, monthLabel);
}

function routesForYear(features, year) {
  const seen = new Set();
  return features.filter((feature) => {
    const props = feature.properties || {};
    const speciesId = props.species_id;
    if (Number(props.year) !== year || !speciesId || seen.has(speciesId)) {
      return false;
    }
    seen.add(speciesId);
    return true;
  });
}

async function loadTurtles(map, layer, monthLabel) {
  let speciesPayload;
  try {
    const speciesResponse = await fetch("/api/species");
    if (!speciesResponse.ok) {
      return;
    }
    speciesPayload = await speciesResponse.json();
  } catch (error) {
    return;
  }

  const species = Array.isArray(speciesPayload)
    ? speciesPayload
    : speciesPayload.species || [];
  const byId = new Map(species.map((item) => [item.id, item]));
  const animate = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let turtles = [];
  let requestToken = 0;

  async function showYear() {
    const token = ++requestToken;
    const year = migrationYear;
    let features = [];
    try {
      const response = await fetch(`/api/migrations?year=${year}`);
      if (!response.ok || token !== requestToken) {
        return;
      }
      const payload = await response.json();
      features = routesForYear(payload.features || [], year);
    } catch (error) {
      return;
    }
    if (token !== requestToken) {
      return;
    }
    layer.clearLayers();
    turtles = [];
    features.forEach((feature) => {
    const props = feature.properties || {};
    const kind = byId.get(props.species_id);
    const look = TURTLE_LOOK[props.species_id];
    const coords = feature.geometry && feature.geometry.coordinates;
    if (!kind || !look || !coords || coords.length < 2) {
      return;
    }

    const shift = routeShift(coords, map.getCenter().lng);
    const guide = L.polyline(coords.map((coord) => shiftedLatLng(coord, shift)), {
      color: kind.colour,
      weight: 2,
      opacity: 0.4,
      dashArray: "1 8",
      lineCap: "round",
      interactive: false,
    }).addTo(layer);

    const trail = L.polyline([shiftedLatLng(coords[0], shift)], {
      color: kind.colour,
      weight: 2.5,
      opacity: 0.9,
      lineCap: "round",
      lineJoin: "round",
      interactive: false,
    }).addTo(layer);

    const marker = L.marker(shiftedLatLng(coords[0], shift), {
      icon: L.divIcon({
        className: "turtle-pin",
        html: `<div class="turtle-rot"><div class="turtle-swim" style="--stroke:${look.stroke}">${turtleSvg(look, animate)}</div></div>`,
        iconSize: [look.size, look.size],
        iconAnchor: [look.size / 2, look.size / 2],
      }),
      zIndexOffset: look.size,
      title: `${kind.common_name}. Illustrative route, not observed tracking.`,
    }).addTo(layer);

    const card = turtleCard(kind, props.region, look, animate, props.year);
    marker.bindTooltip(card, {
      className: "turtle-tip",
      direction: "top",
      offset: [0, -look.size / 2],
      opacity: 1,
    });
    marker.bindPopup(card, {
      className: "turtle-pop",
      closeButton: true,
      maxWidth: 340,
      autoPanPadding: [24, 80],
      offset: [0, -look.size / 2],
    });

    marker.on("click", (event) => {
      L.DomEvent.stopPropagation(event);
      marker.closeTooltip();
      marker.openPopup();
      const shown = L.latLngBounds(coords.map((coord) => shiftedLatLng(coord, routeShift(coords, map.getCenter().lng))));
      map.fitBounds(shown.pad(0.8), {
        padding: [80, 80],
        maxZoom: 7,
        animate: true,
      });
    });

    const element = marker.getElement();
    const rot = element && element.querySelector(".turtle-rot");
    if (!rot) {
      return;
    }
    turtles.push({
      coords,
      marker,
      guide,
      shift,
      trail,
      rot,
      svg: rot.querySelector("svg"),
      heading: 0,
    });
    });
  }

  window.__refreshMigrationYear = () => {
    showYear();
  };
  await showYear();

  // Painting the trails rebuilds SVG paths, which is the costly part. The markers move
  // every frame; the trails only need to catch up a few times a second.
  function paintTurtles(u, withTrails = true) {
    const viewLng = map.getCenter().lng;
    turtles.forEach((turtle) => {
      const next = sampleRoute(turtle.coords, u, turtle.heading);
      const shift = routeShift(turtle.coords, viewLng);
      turtle.heading = next.bearing;
      turtle.marker.setLatLng([next.latlng[0], next.latlng[1] + shift]);
      if (withTrails) {
        turtle.trail.setLatLngs(next.trail.map((point) => [point[0], point[1] + shift]));
      }
      if (turtle.shift !== shift) {
        turtle.guide.setLatLngs(turtle.coords.map((coord) => shiftedLatLng(coord, shift)));
        turtle.shift = shift;
      }
      turtle.rot.style.transform = `rotate(${next.bearing}deg)`;
    });
  }

  // Flipper strokes are SVG animations that repaint on the main thread, so they only
  // run while the map is still, zoomed in far enough to see them, and not under a dive.
  const diveWindow = document.getElementById("sea-window");
  let interacting = false;
  let flippersOn = true;
  let lastTrailPaint = 0;

  function setFlippers(active) {
    if (active === flippersOn) {
      return;
    }
    flippersOn = active;
    turtles.forEach((turtle) => {
      if (turtle.svg && turtle.svg.pauseAnimations) {
        if (active) {
          turtle.svg.unpauseAnimations();
        } else {
          turtle.svg.pauseAnimations();
        }
      }
    });
  }

  map.on("movestart zoomstart", () => {
    interacting = true;
    setFlippers(false);
  });
  map.on("moveend zoomend", () => {
    interacting = false;
  });

  const slider = document.getElementById("turtle-time");
  const playButton = document.getElementById("turtle-play");
  let progress = readProgress(slider);
  let playing = animate;
  let last = performance.now();
  let holdUntil = 0;

  function showMonth(u) {
    const safe = Number.isFinite(u) ? Math.min(Math.max(u, 0), 0.999) : 0;
    const name = TURTLE_MONTHS[Math.floor(safe * 12)];
    if (monthLabel) {
      monthLabel.textContent = name;
    }
    if (slider) {
      slider.setAttribute("aria-valuetext", name);
    }
  }

  function setPlaying(next) {
    playing = next;
    if (!playing) {
      holdUntil = 0;
    }
    if (!playButton) {
      return;
    }
    playButton.textContent = playing ? "Pause" : "Play";
    playButton.setAttribute("aria-pressed", playing ? "true" : "false");
  }

  if (slider) {
    slider.addEventListener("pointerdown", () => setPlaying(false));
    slider.addEventListener("input", () => {
      setPlaying(false);
      progress = readProgress(slider);
      showMonth(progress);
      paintTurtles(progress);
    });
  }

  if (playButton) {
    setPlaying(playing);
    playButton.addEventListener("click", () => {
      if (!playing && progress >= 1) {
        progress = 0;
      }
      setPlaying(!playing);
      last = performance.now();
    });
  }

  map.on("moveend", () => paintTurtles(progress));
  showMonth(progress);
  paintTurtles(progress);

  function frame(now) {
    if (playing) {
      if (holdUntil) {
        progress = 1;
        if (now >= holdUntil) {
          holdUntil = 0;
          progress = 0;
        }
      } else {
        progress += (now - last) / TURTLE_YEAR_MS;
        if (!Number.isFinite(progress)) {
          progress = 0;
        }
        if (progress >= 1) {
          progress = 1;
          holdUntil = now + TURTLE_HOLD_MS;
        }
      }
      if (slider) {
        slider.value = String(Math.round(progress * 1000));
      }
      showMonth(progress);
      const covered = diveWindow && !diveWindow.hidden;
      if (!interacting && !covered) {
        const trailsDue = now - lastTrailPaint >= 90 || progress >= 1;
        paintTurtles(progress, trailsDue);
        if (trailsDue) {
          lastTrailPaint = now;
        }
      }
    }
    const resting = !interacting && !(diveWindow && !diveWindow.hidden);
    setFlippers(animate && resting && map.getZoom() >= 4);
    last = now;
    requestAnimationFrame(frame);
  }
  last = performance.now();
  setFlippers(false);
  requestAnimationFrame(frame);
}

function readProgress(slider) {
  const parsed = Number(slider && slider.value);
  if (!Number.isFinite(parsed)) {
    return 0;
  }
  return Math.min(1, Math.max(0, parsed / 1000));
}

function routeShift(coords, centerLng) {
  const mid = coords[Math.floor(coords.length / 2)][0];
  let shown = mid;
  while (shown - centerLng > 180) {
    shown -= 360;
  }
  while (centerLng - shown > 180) {
    shown += 360;
  }
  return shown - mid;
}

function shiftedLatLng(coord, shift) {
  return [coord[1], coord[0] + shift];
}

function turtleLatLng(coord) {
  return [coord[1], coord[0]];
}

function sampleRoute(coords, u, heading) {
  const last = coords.length - 1;
  if (u >= 1) {
    return {
      latlng: turtleLatLng(coords[last]),
      bearing: routeBearing(coords[last - 1], coords[last], heading),
      trail: coords.map(turtleLatLng),
    };
  }

  const span = u * last;
  const index = Math.min(last - 1, Math.floor(span));
  const fraction = span - index;
  const start = coords[index];
  const end = coords[index + 1];
  const trail = coords.slice(0, index + 1).map(turtleLatLng);
  const latlng = [
    start[1] + (end[1] - start[1]) * fraction,
    start[0] + (end[0] - start[0]) * fraction,
  ];
  trail.push(latlng);
  return {
    latlng,
    bearing: routeBearing(start, end, heading),
    trail,
  };
}

function routeBearing(start, end, fallback) {
  if (Math.abs(end[0] - start[0]) + Math.abs(end[1] - start[1]) < 1e-6) {
    return fallback;
  }
  const lon1 = (start[0] * Math.PI) / 180;
  const lat1 = (start[1] * Math.PI) / 180;
  const lon2 = (end[0] * Math.PI) / 180;
  const lat2 = (end[1] * Math.PI) / 180;
  const y = Math.sin(lon2 - lon1) * Math.cos(lat2);
  const x = Math.cos(lat1) * Math.sin(lat2)
    - Math.sin(lat1) * Math.cos(lat2) * Math.cos(lon2 - lon1);
  return ((Math.atan2(y, x) * 180) / Math.PI + 360) % 360;
}

function turtleCard(species, region, look, animate, year) {
  const place = region ? `<span>${escapeHtml(region)}</span>` : "";
  const when = year ? `<span>${escapeHtml(year)}</span>` : "";
  return `<div class="turtle-card">
    <div class="turtle-swim" style="--stroke:${look.stroke}">${turtleSvg(look, animate)}</div>
    <div class="turtle-card-copy">
      <strong>${escapeHtml(species.common_name)}</strong>
      <em>${escapeHtml(species.scientific_name)}</em>
      ${when}
      ${place}
      <span>Illustrative route — not observed tracking</span>
    </div>
  </div>`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function turtleSvg(look, animate) {
  return `<svg class="turtle" viewBox="0 0 120 120" aria-hidden="true">
    ${rearFlipper(-1, look, animate)}
    ${rearFlipper(1, look, animate)}
    ${shellShape(look)}
    ${carapaceMarks(look)}
    ${frontFlipper(-1, look, animate)}
    ${frontFlipper(1, look, animate)}
    ${headShape(look)}
  </svg>`;
}

function frontFlipper(side, look, animate) {
  const shoulderX = 60 + side * 14;
  const shoulderY = 58;
  const reach = look.reach;
  const tipX = 60 + side * 52 * reach;
  const midX = 60 + side * 32 * reach;
  const path = `M ${shoulderX} ${shoulderY - 7} C ${midX} ${shoulderY - 22}, ${tipX - side * 4} ${shoulderY - 8}, ${tipX} ${shoulderY + 4} C ${tipX - side * 6} ${shoulderY + 16}, ${midX} ${shoulderY + 14}, ${shoulderX} ${shoulderY + 8} Z`;
  const from = side < 0 ? 22 : -22;
  const to = side < 0 ? -26 : 26;
  return `<g class="paddle paddle-${side < 0 ? "left" : "right"}">${flipperMotion(animate, shoulderX, shoulderY, from, to, look.stroke)}<path d="${path}" fill="${look.skin}" stroke="${look.dark}" stroke-width="0.45"/></g>`;
}

function rearFlipper(side, look, animate) {
  const originX = 60 + side * 10;
  const originY = 92;
  const path = side < 0
    ? "M 50 86 C 36 88, 34 102, 46 104 C 54 102, 56 92, 50 86 Z"
    : "M 70 86 C 84 88, 86 102, 74 104 C 66 102, 64 92, 70 86 Z";
  const from = side < 0 ? 8 : -8;
  const to = side < 0 ? -10 : 10;
  return `<g class="paddle rear-${side < 0 ? "left" : "right"}">${flipperMotion(animate, originX, originY, from, to, look.stroke)}<path d="${path}" fill="${look.skin}" stroke="${look.dark}" stroke-width="0.4"/></g>`;
}

function flipperMotion(animate, x, y, from, to, duration) {
  if (!animate) {
    return "";
  }
  return `<animateTransform attributeName="transform" type="rotate" values="${from} ${x} ${y}; ${to} ${x} ${y}; ${from} ${x} ${y}" dur="${duration}" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1; 0.42 0 0.58 1"/>`;
}

function shellShape(look) {
  if (look.ridges) {
    return `<path d="M60 40 C 46 44, 40 58, 42 78 C 46 96, 54 102, 60 104 C 66 102, 74 96, 78 78 C 80 58, 74 44, 60 40 Z" fill="${look.shell}" stroke="${look.dark}" stroke-width="1"/>`;
  }
  if (look.serrated) {
    return `<path d="M60 42 C 40 44, 36 58, 38 74 L 44 84 L 50 76 L 56 86 L 60 78 L 64 86 L 70 76 L 76 84 L 82 74 C 84 58, 80 44, 60 42 Z" fill="${look.shell}" stroke="${look.dark}" stroke-width="1"/>`;
  }
  const rim = look.rim
    ? `<ellipse cx="60" cy="68" rx="${look.rx + 3.5}" ry="${look.ry + 2.5}" fill="${look.rim}"/>`
    : "";
  return `${rim}<ellipse cx="60" cy="68" rx="${look.rx}" ry="${look.ry}" fill="${look.shell}" stroke="${look.dark}" stroke-width="1.1"/>`;
}

function carapaceMarks(look) {
  if (look.ridges) {
    const ridges = [];
    for (let i = 0; i < look.ridges; i += 1) {
      const x = 46 + (i * 28) / 6;
      const bend = (i - 3) * 1.2;
      ridges.push(`<path d="M${(x + bend * 0.2).toFixed(1)} 46 Q ${(x + bend).toFixed(1)} 72 ${(60 + (x - 60) * 0.35).toFixed(1)} 98" fill="none" stroke="#9aa3ae" stroke-width="${i === 3 ? 1.5 : 0.85}" stroke-linecap="round" opacity="0.85"/>`);
    }
    [[54, 58], [66, 64], [50, 74], [63, 82], [70, 52], [57, 90]].forEach(([x, y]) => {
      ridges.push(`<circle cx="${x}" cy="${y}" r="1.4" fill="${look.spot}"/>`);
    });
    return ridges.join("");
  }

  const top = 68 - look.ry + 8;
  const bottom = 68 + look.ry - 6;
  const left = 60 - look.rx + 5;
  const right = 60 + look.rx - 5;
  const marks = [`<path d="M60 ${top} L60 ${bottom}" fill="none" stroke="${look.dark}" stroke-width="0.8" opacity="0.75"/>`];
  for (let i = 0; i < look.costals; i += 1) {
    const y = top + ((bottom - top) * i) / (look.costals - 1);
    const lift = look.overlap ? (i % 2 ? 3.5 : -3.5) : -3;
    marks.push(`<path d="M${left} ${y.toFixed(1)} Q 60 ${(y + lift).toFixed(1)} ${right} ${y.toFixed(1)}" fill="none" stroke="${look.dark}" stroke-width="0.9" opacity="0.8"/>`);
  }
  if (look.mottle) {
    marks.push(`<ellipse cx="52" cy="62" rx="6" ry="4" fill="${look.mottle}" opacity="0.5"/>`);
    marks.push(`<ellipse cx="69" cy="74" rx="5" ry="3" fill="${look.dark}" opacity="0.25"/>`);
    marks.push(`<ellipse cx="57" cy="80" rx="4" ry="2.6" fill="${look.mottle}" opacity="0.4"/>`);
  }
  marks.push(`<ellipse cx="54" cy="60" rx="${(look.rx * 0.28).toFixed(1)}" ry="${(look.ry * 0.18).toFixed(1)}" fill="#ffffff" opacity="0.13"/>`);
  return marks.join("");
}

function headShape(look) {
  const head = look.head;
  const parts = [
    `<ellipse cx="60" cy="40" rx="${(head * 0.72).toFixed(1)}" ry="5" fill="${look.skin}"/>`,
    `<ellipse cx="60" cy="26" rx="${head}" ry="${(head * 1.15).toFixed(1)}" fill="${look.skin}" stroke="${look.dark}" stroke-width="0.4"/>`,
  ];
  if (look.beak) {
    parts.push(`<polygon points="60,11 53,24 67,24" fill="${look.dark}"/>`);
  }
  parts.push(`<circle cx="${(60 - head * 0.42).toFixed(1)}" cy="24" r="1.15" fill="#1c140c"/>`);
  parts.push(`<circle cx="${(60 + head * 0.42).toFixed(1)}" cy="24" r="1.15" fill="#1c140c"/>`);
  if (look.prefrontals === 1) {
    parts.push(`<path d="M60 16.5 L60 28" fill="none" stroke="${look.dark}" stroke-width="0.6" opacity="0.7"/>`);
  } else {
    const offset = (head * 0.28).toFixed(1);
    parts.push(`<path d="M${60 - offset} 16 L${60 - offset} 28" fill="none" stroke="${look.dark}" stroke-width="0.55" opacity="0.65"/>`);
    parts.push(`<path d="M${60 + offset} 16 L${60 + offset} 28" fill="none" stroke="${look.dark}" stroke-width="0.55" opacity="0.65"/>`);
  }
  return parts.join("");
}
