// Fish shown in the sea dive. These are illustrations of well-known fish for each
// ocean, not a survey and not a record of what swims at the clicked point.
// Depth ranges are typical habitat depths; a fish is only drawn when it fits
// inside the real water column (seafloor from GMRT) and the clicked latitude.
//   kind  - which template draws it (see fishSvg)
//   w     - drawn width in px (height is 0.4 of that)
//   min/max - typical depth range in metres
//   at    - where in that range it is drawn (0 top, 1 bottom)
//   floor - demersal: lives on the bottom, drawn just above the seafloor
//   lat   - [south, north] (or a list of those) where the species is drawn
//   school - drawn as a small school (schooling species)

const FISH = {
  "atlantic-herring": { name: "Atlantic herring", latin: "Clupea harengus", kind: "slender", back: "#3b6a86", belly: "#e3ecee", fin: "#8aa2ae", w: 74, t: 7.2, min: 10, max: 200, at: 0.35, lat: [40, 75], school: 3 },
  "atlantic-mackerel": { name: "Atlantic mackerel", latin: "Scomber scombrus", kind: "mackerel", back: "#2f7f80", belly: "#e8efe9", fin: "#3d6c73", w: 82, t: 7.4, min: 10, max: 200, at: 0.55, lat: [30, 70], school: 2 },
  "atlantic-bluefin": { name: "Atlantic bluefin tuna", latin: "Thunnus thynnus", kind: "tuna", back: "#1c3552", belly: "#cdd6dc", fin: "#2a3f55", finlet: "#c0a93c", w: 128, t: 10.5, min: 0, max: 500, at: 0.3, lat: [10, 70], swim: 15 },
  "atlantic-cod": { name: "Atlantic cod", latin: "Gadus morhua", kind: "cod", back: "#7b7a4c", belly: "#dbd6bb", fin: "#8c8658", w: 104, t: 11, min: 30, max: 600, floor: true, lat: [40, 75] },
  "skipjack-tuna": { name: "Skipjack tuna", latin: "Katsuwonus pelamis", kind: "tuna", stripes: true, back: "#223f66", belly: "#d3dbe0", fin: "#2c4766", finlet: "#8a98a4", w: 104, t: 10, min: 0, max: 260, at: 0.42, lat: [-40, 40], school: 2, swim: 14 },
  "yellowfin-tuna": { name: "Yellowfin tuna", latin: "Thunnus albacares", kind: "tuna", yellow: true, back: "#1f3f63", belly: "#d9dde0", fin: "#e3c53c", finlet: "#e3c53c", w: 120, t: 10.5, min: 0, max: 250, at: 0.5, lat: [-40, 40], swim: 15 },
  "pacific-sardine": { name: "Pacific sardine", latin: "Sardinops sagax", kind: "slender", spots: true, back: "#3a6b86", belly: "#e6eeee", fin: "#86a0ac", w: 66, t: 6.8, min: 5, max: 200, at: 0.3, lat: [[-45, -5], [20, 55]], school: 3 },
  "sockeye-salmon": { name: "Sockeye salmon", latin: "Oncorhynchus nerka", kind: "salmon", back: "#2f5d83", belly: "#dfe7ec", fin: "#7a94a6", w: 92, t: 8.6, min: 0, max: 250, at: 0.2, lat: [38, 66], swim: 18 },
  "indian-oil-sardine": { name: "Indian oil sardine", latin: "Sardinella longiceps", kind: "slender", gill: true, back: "#3c6f78", belly: "#e8efe9", fin: "#8fa9ab", w: 62, t: 6.6, min: 5, max: 200, at: 0.25, lat: [5, 26], school: 3 },
  "indian-mackerel": { name: "Indian mackerel", latin: "Rastrelliger kanagurta", kind: "slender", band: "#d6b24a", back: "#2a6e72", belly: "#e8eee6", fin: "#7f9f98", w: 76, t: 8.2, min: 5, max: 90, at: 0.5, lat: [-25, 30], school: 2 },
  sailfish: { name: "Indo-Pacific sailfish", latin: "Istiophorus platypterus", kind: "sailfish", back: "#1f4b7a", belly: "#cbd5dc", fin: "#2c5f96", w: 138, t: 7, min: 0, max: 200, at: 0.4, lat: [-35, 30], swim: 13 },
  "polar-cod": { name: "Polar cod", latin: "Boreogadus saida", kind: "slendercod", back: "#5b5545", belly: "#c9ccc4", fin: "#7d7867", w: 66, t: 6.6, min: 0, max: 400, at: 0.3, lat: [60, 90], school: 3 },
  capelin: { name: "Capelin", latin: "Mallotus villosus", kind: "slender", back: "#5c8570", belly: "#e3eae6", fin: "#9bb0a8", w: 58, t: 5.8, min: 0, max: 300, at: 0.25, lat: [55, 90], school: 3 },
  "greenland-halibut": { name: "Greenland halibut", latin: "Reinhardtius hippoglossoides", kind: "flat", back: "#4a3f36", belly: "#4a3f36", fin: "#6a5b4a", w: 104, t: 0, min: 200, max: 2000, floor: true, lat: [55, 90] },
  "antarctic-silverfish": { name: "Antarctic silverfish", latin: "Pleuragramma antarctica", kind: "slender", glass: true, back: "#7c9eb4", belly: "#e9f1f4", fin: "#a8c0cc", w: 64, t: 5.8, min: 0, max: 900, at: 0.3, lat: [-90, -55], school: 3 },
  "mackerel-icefish": { name: "Mackerel icefish", latin: "Champsocephalus gunnari", kind: "icefish", back: "#8aa5b2", belly: "#e2eaee", fin: "#a9bfc9", w: 88, t: 6.4, min: 0, max: 700, at: 0.4, lat: [-90, -45], school: 2 },
  "antarctic-toothfish": { name: "Antarctic toothfish", latin: "Dissostichus mawsoni", kind: "toothfish", back: "#4a4f55", belly: "#a9b0b3", fin: "#5d6369", w: 124, t: 10.8, min: 500, max: 2200, floor: true, lat: [-90, -60] },
  "patagonian-toothfish": { name: "Patagonian toothfish", latin: "Dissostichus eleginoides", kind: "toothfish", back: "#4d5148", belly: "#b0b4ab", fin: "#62665d", w: 124, t: 10.8, min: 300, max: 3500, floor: true, lat: [-62, -40] },
  lanternfish: { name: "Lanternfish", latin: "Myctophidae", kind: "lantern", back: "#1a242c", belly: "#243038", fin: "#243038", w: 66, t: 6.2, min: 200, max: 1000, at: 0.45, lat: [-90, 75], school: 2 },
};

// Most popular fish first. The first four that fit the place are shown, then
// the lanternfish family once the water reaches the twilight.
const OCEAN_FISH = {
  atlantic: ["atlantic-herring", "atlantic-mackerel", "atlantic-bluefin", "atlantic-cod", "yellowfin-tuna", "skipjack-tuna", "patagonian-toothfish"],
  pacific: ["skipjack-tuna", "yellowfin-tuna", "pacific-sardine", "sockeye-salmon", "patagonian-toothfish"],
  indian: ["yellowfin-tuna", "skipjack-tuna", "indian-mackerel", "sailfish", "indian-oil-sardine", "patagonian-toothfish"],
  arctic: ["polar-cod", "capelin", "greenland-halibut"],
  southern: ["antarctic-silverfish", "mackerel-icefish", "antarctic-toothfish"],
};

function fishForPlace(place, seafloor) {
  if (!place || !seafloor) {
    return [];
  }
  const margin = Math.max(8, seafloor * 0.04);
  const chosen = [];
  for (const id of OCEAN_FISH[place.id] || []) {
    const fish = FISH[id];
    const ranges = Array.isArray(fish.lat[0]) ? fish.lat : [fish.lat];
    if (!ranges.some(([south, north]) => place.lat >= south && place.lat <= north)) {
      continue;
    }
    let depth;
    if (fish.floor) {
      if (seafloor < fish.min || seafloor > fish.max) {
        continue;
      }
      depth = seafloor - margin;
    } else {
      const deepest = Math.min(fish.max, seafloor * 0.85);
      if (deepest < fish.min + 4) {
        continue;
      }
      depth = fish.min + (deepest - fish.min) * fish.at;
    }
    chosen.push({ id, depth });
    if (chosen.length === 4) {
      break;
    }
  }
  const lantern = FISH.lanternfish;
  if (seafloor > lantern.min + 80 && place.id !== "arctic") {
    const deepest = Math.min(lantern.max, seafloor * 0.85);
    chosen.push({ id: "lanternfish", depth: lantern.min + (deepest - lantern.min) * lantern.at });
  }
  return chosen;
}

function bodyPath(t, hx, blunt) {
  const nose = blunt ? 3 : 1.2;
  return `M22 18.2 C36 ${20 - t}, 64 ${20 - t * 1.02}, ${hx - 6} ${20 - t * 0.6} Q${hx + nose} ${20 - t * 0.1}, ${hx} 20.6 Q${hx + nose} ${20 + t * 0.3}, ${hx - 6} ${20 + t * 0.58} C64 ${20 + t * 0.98}, 36 ${20 + t * 0.9}, 22 21.8 Z`;
}

function tailPath(shape, tl) {
  if (shape === "lunate") {
    return `M27 20 C18 17, 12 12, 6 ${20 - tl} C11 18, 11 22, 6 ${20 + tl} C12 28, 18 23, 27 20 Z`;
  }
  if (shape === "round") {
    return `M27 20 C17 ${20 - tl}, 5 ${20 - tl + 1}, 5 20 C5 ${20 + tl - 1}, 17 ${20 + tl}, 27 20 Z`;
  }
  if (shape === "square") {
    return `M27 20 L7 ${20 - tl} L11 20 L7 ${20 + tl} Z`;
  }
  return `M27 20 L7 ${20 - tl} Q13 20 7 ${20 + tl} Z`;
}

function topFin(x0, x1, h, t) {
  return `M${x0} ${20 - t * 0.72} Q${x0 + (x1 - x0) * 0.3} ${20 - t - h}, ${x1} ${20 - t * 0.8} Z`;
}

function lowFin(x0, x1, h, t) {
  return `M${x0} ${20 + t * 0.7} Q${x0 + (x1 - x0) * 0.4} ${20 + t + h}, ${x1} ${20 + t * 0.78} Z`;
}

function finlets(t, color) {
  let out = "";
  for (let i = 0; i < 5; i += 1) {
    const x = 28 + i * 4.6;
    out += `<path d="M${x} ${20 - t * 0.7} L${x + 2.2} ${20 - t - 1.6} L${x + 4} ${20 - t * 0.74} Z" fill="${color}"/>`;
    out += `<path d="M${x} ${20 + t * 0.7} L${x + 2.2} ${20 + t + 1.6} L${x + 4} ${20 + t * 0.74} Z" fill="${color}"/>`;
  }
  return out;
}

function fishSvg(id) {
  const f = FISH[id];
  if (!f) {
    return "";
  }
  if (f.kind === "lantern") {
    return lanternSvg();
  }
  if (f.kind === "flat") {
    return flatfishSvg(f);
  }
  const t = f.t;
  const kind = f.kind;
  const hx = kind === "sailfish" ? 80 : kind === "icefish" ? 95 : 92;
  const blunt = kind === "cod" || kind === "toothfish" || kind === "slendercod";
  const body = bodyPath(t, hx, blunt);
  const dark = "#0d1519";
  const eyeX = hx - (kind === "toothfish" ? 11 : 10);
  const eyeY = 20 - t * 0.2;
  const eyeR = f.glass || kind === "icefish" ? 2.2 : kind === "toothfish" ? 2.4 : 1.8;
  const tailShape = kind === "tuna" || kind === "sailfish" ? "lunate" : kind === "cod" || kind === "toothfish" ? "round" : kind === "salmon" ? "square" : "fork";
  const tailLen = kind === "tuna" ? 13 : kind === "sailfish" ? 11 : kind === "cod" || kind === "toothfish" ? 10 : kind === "mackerel" ? 9 : 8;
  const fin = f.fin;
  const opacity = f.glass ? 0.82 : 1;
  let behind = "";
  let marks = "";
  let front = "";

  if (kind === "slender" || kind === "slendercod") {
    behind += `<path d="${topFin(44, 57, 3.4, t)}" fill="${fin}"/>`;
    behind += `<path d="${lowFin(38, 50, 3, t)}" fill="${fin}"/>`;
    behind += `<path d="${lowFin(56, 64, 2.4, t)}" fill="${fin}"/>`;
  }
  if (kind === "slendercod") {
    behind += `<path d="${topFin(30, 38, 2.6, t)}" fill="${fin}"/>`;
    behind += `<path d="${topFin(60, 68, 2.4, t)}" fill="${fin}"/>`;
  }
  if (kind === "mackerel") {
    behind += `<path d="${topFin(40, 54, 5.4, t)}" fill="${fin}"/>`;
    behind += `<path d="${topFin(60, 67, 2.8, t)}" fill="${fin}"/>`;
    behind += `<path d="${lowFin(58, 66, 2.6, t)}" fill="${fin}"/>`;
    behind += finlets(t, fin);
    for (let x = 30; x < 86; x += 5.4) {
      marks += `<path d="M${x} ${20 - t} C${x + 3} ${20 - t * 0.6}, ${x - 2} ${20 - t * 0.4}, ${x + 2.4} ${20 - t * 0.02}" fill="none" stroke="#10323a" stroke-width="1.2" opacity="0.8"/>`;
    }
  }
  if (kind === "tuna") {
    behind += `<path d="${topFin(44, 58, 6.5, t)}" fill="${f.yellow ? "#b89c2c" : fin}"/>`;
    if (f.yellow) {
      behind += `<path d="M60 ${20 - t * 0.74} Q66 ${20 - t - 5.6}, 79 ${20 - t - 2.4} Q70 ${20 - t * 0.9}, 68 ${20 - t * 0.8} Z" fill="#e3c53c"/>`;
      behind += `<path d="M60 ${20 + t * 0.74} Q66 ${20 + t + 5.4}, 79 ${20 + t + 2.4} Q70 ${20 + t * 0.9}, 68 ${20 + t * 0.82} Z" fill="#e3c53c"/>`;
    } else {
      behind += `<path d="${topFin(62, 69, 3.4, t)}" fill="${fin}"/>`;
      behind += `<path d="${lowFin(62, 69, 3.2, t)}" fill="${fin}"/>`;
    }
    behind += finlets(t, f.finlet);
    if (f.yellow) {
      marks += `<path d="M30 ${20 - t * 0.1} C52 ${20 - t * 0.28}, 72 ${20 - t * 0.22}, 88 ${20 - t * 0.08}" fill="none" stroke="#e3c53c" stroke-width="1.7" opacity="0.9"/>`;
    }
    if (f.stripes) {
      for (let i = 0; i < 5; i += 1) {
        marks += `<path d="M${34 + i * 1.2} ${20 + t * (0.2 + i * 0.13)} L${78 - i * 1.5} ${20 + t * (0.2 + i * 0.13)}" fill="none" stroke="#2a3340" stroke-width="0.9" opacity="0.65"/>`;
      }
    }
  }
  if (kind === "salmon") {
    behind += `<path d="${topFin(46, 58, 4.6, t)}" fill="${fin}"/>`;
    behind += `<ellipse cx="31" cy="${20 - t * 0.78}" rx="2.4" ry="1.3" fill="${fin}"/>`;
    behind += `<path d="${lowFin(44, 55, 3.6, t)}" fill="${fin}"/>`;
    behind += `<path d="${lowFin(60, 68, 2.4, t)}" fill="${fin}"/>`;
  }
  if (kind === "sailfish") {
    behind += `<path d="M34 ${20 - t * 0.8} Q40 ${20 - t - 13}, 52 3 L72 ${20 - t - 12} Q76 ${20 - t - 4}, 74 ${20 - t * 0.78} Z" fill="${fin}"/>`;
    for (let i = 0; i < 6; i += 1) {
      behind += `<circle cx="${44 + i * 5}" cy="${14 - Math.abs(i - 2.2) * 1.3}" r="0.9" fill="#0e2438" opacity="0.55"/>`;
    }
    behind += `<path d="${lowFin(58, 66, 2.6, t)}" fill="${fin}"/>`;
    behind += `<path d="M52 ${20 + t * 0.6} Q50 ${20 + t + 8}, 46 ${20 + t + 10} Q54 ${20 + t + 4}, 58 ${20 + t * 0.6} Z" fill="${fin}"/>`;
    behind += `<path d="M${hx - 6} 19 L100 20 L${hx - 6} 21 Z" fill="#2a3340"/>`;
  }
  if (kind === "icefish") {
    behind += `<path d="${topFin(40, 50, 8.4, t)}" fill="#2b3a44"/>`;
    behind += `<path d="${topFin(56, 72, 4, t)}" fill="${fin}"/>`;
    behind += `<path d="${lowFin(58, 74, 3.6, t)}" fill="${fin}"/>`;
  }
  if (kind === "cod") {
    behind += `<path d="${topFin(36, 47, 5.4, t)}" fill="${fin}"/>`;
    behind += `<path d="${topFin(49, 60, 5.4, t)}" fill="${fin}"/>`;
    behind += `<path d="${topFin(62, 71, 4.2, t)}" fill="${fin}"/>`;
    behind += `<path d="${lowFin(46, 58, 4.4, t)}" fill="${fin}"/>`;
    behind += `<path d="${lowFin(60, 72, 3.6, t)}" fill="${fin}"/>`;
    marks += `<path d="M34 ${20 - t * 0.2} C50 ${20 - t * 0.46}, 70 ${20 - t * 0.34}, 86 ${20 - t * 0.04}" fill="none" stroke="#efe9cc" stroke-width="1" opacity="0.8"/>`;
    [[40, 12], [54, 10], [68, 13], [48, 17], [62, 16], [76, 14], [34, 15]].forEach(([x, y]) => {
      marks += `<ellipse cx="${x}" cy="${y}" rx="3.6" ry="2" fill="#4c4a2c" opacity="0.4"/>`;
    });
  }
  if (kind === "toothfish") {
    behind += `<path d="${topFin(38, 56, 4.2, t)}" fill="${fin}"/>`;
    behind += `<path d="${topFin(60, 74, 3.2, t)}" fill="${fin}"/>`;
    behind += `<path d="${lowFin(62, 78, 3.2, t)}" fill="${fin}"/>`;
    [[36, 14], [50, 12], [64, 14], [78, 16], [44, 22], [58, 24], [72, 22]].forEach(([x, y]) => {
      marks += `<ellipse cx="${x}" cy="${y}" rx="4.4" ry="2.2" fill="#2a2e33" opacity="0.45"/>`;
    });
  }

  if (f.spots) {
    for (let i = 0; i < 7; i += 1) {
      marks += `<circle cx="${38 + i * 6}" cy="${20 - t * 0.3 + (i % 2) * 1.2}" r="0.9" fill="#16313f" opacity="0.75"/>`;
    }
  }
  if (f.band) {
    marks += `<path d="M28 ${20 - t * 0.12} C50 ${20 - t * 0.32}, 70 ${20 - t * 0.28}, 88 ${20 - t * 0.1}" fill="none" stroke="${f.band}" stroke-width="1.7" opacity="0.85"/>`;
    marks += `<circle cx="${hx - 20}" cy="${20 - t * 0.1}" r="1" fill="#10242a" opacity="0.7"/>`;
  }
  if (f.gill) {
    marks += `<circle cx="${hx - 17}" cy="${20 - t * 0.2}" r="1.5" fill="#12282d" opacity="0.7"/>`;
  }
  if (kind === "salmon") {
    marks += `<path d="M30 ${20 - t * 0.1} C52 ${20 - t * 0.18}, 70 ${20 - t * 0.14}, 86 ${20 - t * 0.04}" fill="none" stroke="#b8cfdc" stroke-width="0.8" opacity="0.55"/>`;
  }
  if (kind === "slendercod") {
    marks += `<path d="M${hx - 8} ${20 + t * 0.55} L${hx - 9} ${20 + t * 0.55 + 3}" stroke="${f.back}" stroke-width="0.9"/>`;
  }

  front += `<path d="M${hx - 22} ${20 + t * 0.2} Q${hx - 31} ${20 + t * 0.8 + 3}, ${hx - 35} ${20 + t * 0.7 + 4} Q${hx - 27} ${20 + t * 0.3}, ${hx - 18} ${20 + t * 0.02} Z" fill="${fin}" opacity="0.9"/>`;
  const gillCover = `<path d="M${hx - 14} ${20 - t * 0.55} Q${hx - 18} 20 ${hx - 14} ${20 + t * 0.5}" fill="none" stroke="${dark}" stroke-width="0.8" opacity="0.35"/>`;
  const mouth = kind === "toothfish" || kind === "cod"
    ? `<path d="M${hx} 20.8 Q${hx - 7} ${20 + t * 0.34}, ${hx - 12} ${20 + t * 0.24}" fill="none" stroke="${dark}" stroke-width="0.9" opacity="0.75"/>`
    : `<path d="M${hx - 0.5} 20.7 L${hx - 6} 21.4" stroke="${dark}" stroke-width="0.8" opacity="0.7"/>`;

  return `<svg viewBox="0 0 100 40" aria-hidden="true">
    <defs>
      <linearGradient id="fg-${id}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${f.back}"/>
        <stop offset="0.44" stop-color="${f.back}"/>
        <stop offset="0.64" stop-color="${f.belly}"/>
        <stop offset="1" stop-color="${f.belly}"/>
      </linearGradient>
      <linearGradient id="fs-${id}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ffffff" stop-opacity="0.3"/>
        <stop offset="0.5" stop-color="#ffffff" stop-opacity="0"/>
        <stop offset="1" stop-color="#000000" stop-opacity="0.18"/>
      </linearGradient>
      <clipPath id="fc-${id}"><path d="${body}"/></clipPath>
    </defs>
    <g opacity="${opacity}">
      <g class="fish-tail"><path d="${tailPath(tailShape, tailLen)}" fill="${f.yellow ? "#8a7f3a" : fin}"/></g>
      ${behind}
      <path d="${body}" fill="url(#fg-${id})"/>
      <g clip-path="url(#fc-${id})">${marks}<path d="${body}" fill="url(#fs-${id})"/></g>
      ${front}
      ${gillCover}
      ${mouth}
      <circle cx="${eyeX}" cy="${eyeY}" r="${eyeR + 0.3}" fill="#e3e9ea" opacity="0.55"/>
      <circle cx="${eyeX}" cy="${eyeY}" r="${eyeR - 0.2}" fill="#0b1114"/>
      <circle cx="${eyeX + 0.6}" cy="${eyeY - 0.6}" r="0.5" fill="#ffffff"/>
    </g>
  </svg>`;
}

function flatfishSvg(f) {
  const body = "M10 20 C20 7, 66 4, 88 15 C94 18, 94 22, 88 25 C66 36, 20 33, 10 20 Z";
  return `<svg viewBox="0 0 100 40" aria-hidden="true">
    <defs>
      <linearGradient id="fg-flat" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#5a4d41"/>
        <stop offset="1" stop-color="#3b322a"/>
      </linearGradient>
    </defs>
    <g class="fish-tail"><path d="M14 20 L4 13 Q8 20 4 27 Z" fill="${f.fin}"/></g>
    <path d="M12 20 C22 3, 66 0, 90 14 C70 6, 28 8, 12 20 Z" fill="${f.fin}" opacity="0.8"/>
    <path d="M12 20 C22 37, 66 40, 90 26 C70 34, 28 32, 12 20 Z" fill="${f.fin}" opacity="0.8"/>
    <path d="${body}" fill="url(#fg-flat)"/>
    <path d="M22 20 C40 17, 66 17, 84 19" fill="none" stroke="#7a6a58" stroke-width="0.8" opacity="0.6"/>
    <circle cx="82" cy="15.6" r="1.7" fill="#c9cfcb"/><circle cx="82.3" cy="15.4" r="1.1" fill="#0b1114"/>
    <circle cx="86" cy="18.2" r="1.5" fill="#c9cfcb"/><circle cx="86.3" cy="18" r="1" fill="#0b1114"/>
    <path d="M91 21 Q87 23 83 22.5" fill="none" stroke="#1a1410" stroke-width="0.8"/>
  </svg>`;
}

function lanternSvg() {
  return `<svg viewBox="0 0 78 32" aria-hidden="true">
    <g class="fish-tail"><path d="M16 16 L4 7 L8 16 L4 25 Z" fill="#243038"/></g>
    <path d="M16 16 C26 7, 52 6, 64 14 C70 16, 64 18, 58 16 C50 26, 24 25, 16 16 Z" fill="#1a242c"/>
    <path d="M42 9 L48 3 L46 12 Z" fill="#243038"/>
    <circle cx="58" cy="13" r="3.1" fill="#d5e4ea"/>
    <circle cx="58.7" cy="13" r="1.5" fill="#10161a"/>
    <circle cx="28" cy="20.2" r="0.8" fill="#b7ffe6"/>
    <circle cx="34" cy="21.2" r="0.8" fill="#b7ffe6"/>
    <circle cx="40" cy="21.4" r="0.8" fill="#b7ffe6"/>
    <circle cx="46" cy="20.6" r="0.8" fill="#b7ffe6"/>
  </svg>`;
}
