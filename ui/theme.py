"""Token-based design system and responsive styles for Turtle Tide."""

CSS = """
/* Fonts are served from ui/fonts through the local NiceGUI static route. */
@font-face { font-family:'Pixelify Sans'; src:url('/ui-assets/pixelify-sans.woff2') format('woff2'); font-weight:400 700; font-style:normal; font-display:swap; }
@font-face { font-family:'Jersey 15'; src:url('/ui-assets/jersey-15.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }

/* Shared palette, spacing, shape, and elevation tokens. */
:root {
  --c-navy:#0b2340; --c-teal:#236477; --c-green:#77d99a;
  --c-cyan:#53d4e5; --c-gold:#ffd46b; --c-coral:#ff817e;
  --r-sm:6px; --r-md:12px; --r-lg:20px;
  --space-1:8px; --space-2:16px; --space-3:24px; --space-4:32px;
  --glass-bg:rgba(10, 35, 65, 0.4);
  --glass-border:rgba(160, 235, 255, 0.35);
  --glass-highlight:rgba(255, 255, 255, 0.18);
  --glass-blur:14px;
  --shadow-soft:0 6px 18px color-mix(in srgb,var(--c-navy) 52%,transparent);
  --shadow-raised:0 4px 0 color-mix(in srgb,var(--c-navy) 88%,transparent),0 10px 24px color-mix(in srgb,var(--c-navy) 40%,transparent);
  --font-pixel:'Pixelify Sans',sans-serif;
  --font-title:'Jersey 15',sans-serif;
}

/* Allow the document to grow; decorative art stays pinned behind it. */
*,*::before,*::after { box-sizing:border-box; font-family:inherit !important; line-height:1.5 !important; letter-spacing:.02em; font-weight:500 !important; }
html,body { font-family:var(--font-pixel) !important; font-size:18px; line-height:1.5; letter-spacing:.02em; font-weight:500; }
button,input,select,textarea,option { font-family:inherit; font-size:inherit; letter-spacing:inherit; }
/* Draw the select caret in CSS so it stays an icon, not a font glyph name. */
.date-input .q-select__dropdown-icon { display:grid; width:20px; height:20px; flex:none; place-items:center; overflow:hidden; color:transparent !important; font-size:0 !important; line-height:0; }
.date-input .q-select__dropdown-icon::after { content:""; width:0; height:0; border-top:7px solid #081d38; border-right:6px solid transparent; border-left:6px solid transparent; }
html,body { min-height:100%; }
body,.q-page,.q-page-container { height:auto !important; min-height:100dvh !important; max-height:none !important; overflow-x:hidden !important; overflow-y:auto !important; }
body { position:relative; isolation:isolate; margin:0; background:linear-gradient(180deg,#071a38 0%,#0d2a50 46%,#081c3d 100%); color:#e9f8f7; font-size:18px; line-height:1.5; letter-spacing:.02em; font-weight:500; }
.tt-page { position:relative; z-index:1; display:flex; box-sizing:border-box; width:100%; min-height:100dvh; height:auto; max-height:none; overflow:visible; padding:var(--space-2) !important; gap:var(--space-2) !important; color:#e9f8f7; }

/* Cyan light in the center and pixel cave walls in the inline SVG layer. */
body::before { content:''; position:fixed; inset:0; z-index:-2; pointer-events:none; background:radial-gradient(ellipse 46% 72% at 50% 43%,color-mix(in srgb,var(--c-cyan) 32%,transparent),transparent 100%),linear-gradient(180deg,#071a38,#0d2a50 52%,#071a38); }
.cave-art { position:fixed !important; inset:0; z-index:-1; display:block; width:100vw; height:100vh; overflow:hidden; pointer-events:none; opacity:.96; }
.cave-art svg { display:block; width:100%; height:100%; shape-rendering:crispEdges; }
.top-reef-art { position:fixed !important; inset:0; z-index:-1; display:block; width:100vw; height:100vh; overflow:hidden; pointer-events:none; opacity:.98; }
.top-reef-art svg { display:block; width:100%; height:100%; shape-rendering:crispEdges; }
.tt-page > .q-html { position:fixed; inset:0; }
.tt-page > .q-html.cave-art { z-index:-1; }

/* Six fish and bubbles are separate from the map and never catch pointer input. */
.fish-drift { position:fixed !important; inset:0; z-index:-1; width:100vw; height:100vh; overflow:hidden; pointer-events:none; }
.swimming-fish { position:absolute; top:16vh; left:-64px; color:var(--c-cyan); filter:drop-shadow(0 2px 4px color-mix(in srgb,var(--c-navy) 75%,transparent)); animation:fish-right 38s linear infinite; }
.swimming-fish svg { display:block; width:64px; height:42px; fill:currentColor; stroke:color-mix(in srgb,var(--c-cyan) 30%,white); stroke-width:1; shape-rendering:crispEdges; animation:fish-bob 2.8s ease-in-out infinite; }
.swim-left { left:auto; right:-64px; transform:scaleX(-1); animation-name:fish-left; }
.fish-a { top:20vh; color:var(--c-cyan); animation-duration:34s; animation-delay:-9s; }
.fish-b { top:39vh; color:var(--c-gold); animation-duration:43s; animation-delay:-21s; }
.fish-c { top:59vh; color:var(--c-green); animation-duration:31s; animation-delay:-4s; }
.fish-d { top:27vh; color:var(--c-coral); animation-duration:39s; animation-delay:-15s; }
.fish-e { top:69vh; color:var(--c-cyan); animation-duration:46s; animation-delay:-28s; }
.fish-f { top:48vh; color:#b693ff; animation-duration:35s; animation-delay:-11s; }
.fish-g { top:82vh; color:var(--c-gold); animation-duration:48s; animation-delay:-33s; }
.fish-h { top:12vh; color:var(--c-coral); animation-duration:41s; animation-delay:-26s; }
.fish-i { top:33vh; color:var(--c-cyan); animation-duration:37s; animation-delay:-22s; }
.fish-j { top:74vh; color:var(--c-green); animation-duration:50s; animation-delay:-12s; }
.fish-k { top:17vh; color:var(--c-gold); animation-duration:40s; animation-delay:-29s; }
.fish-l { top:53vh; color:var(--c-coral); animation-duration:45s; animation-delay:-6s; }
@keyframes fish-right { from { left:-64px; } to { left:calc(100vw + 64px); } }
@keyframes fish-left { from { right:-64px; } to { right:calc(100vw + 64px); } }
@keyframes fish-bob { 0%,100% { transform:translateY(-3px); } 50% { transform:translateY(4px); } }
.bubble { position:absolute; bottom:-16px; left:5%; width:10px; height:10px; border:1px solid color-mix(in srgb,var(--c-cyan) 78%,white); border-radius:50%; background:radial-gradient(circle at 30% 25%,white,var(--c-cyan) 58%,var(--c-teal)); box-shadow:0 0 8px color-mix(in srgb,var(--c-cyan) 56%,transparent); animation:bubble-rise 9s ease-in-out infinite; }
.bubble-a{left:5%;width:6px;height:6px;animation-delay:-1s}.bubble-b{left:12%;width:11px;height:11px;animation-delay:-5s}.bubble-c{left:19%;animation-delay:-7s}.bubble-d{left:27%;width:5px;height:5px;animation-delay:-3s}.bubble-e{left:34%;width:10px;height:10px;animation-delay:-6s}.bubble-f{left:41%;animation-delay:-2s}.bubble-g{left:48%;width:6px;height:6px;animation-delay:-8s}.bubble-h{left:55%;width:12px;height:12px;animation-delay:-4s}.bubble-i{left:63%;width:7px;height:7px;animation-delay:-1.5s}.bubble-j{left:70%;width:5px;height:5px;animation-delay:-6.5s}.bubble-k{left:77%;width:10px;height:10px;animation-delay:-3.5s}.bubble-l{left:84%;width:6px;height:6px;animation-delay:-7.5s}.bubble-m{left:92%;width:12px;height:12px;animation-delay:-2.5s}.bubble-n{left:9%;width:9px;height:9px;animation-delay:-8.5s}.bubble-o{left:31%;width:7px;height:7px;animation-delay:-5.5s}.bubble-p{left:59%;width:5px;height:5px;animation-delay:-4.5s}.bubble-q{left:73%;width:8px;height:8px;animation-delay:-9s}.bubble-r{left:96%;width:6px;height:6px;animation-delay:-6s}
.bubble-s{left:15%;width:13px;height:13px;animation-delay:-1.8s}.bubble-t{left:37%;width:8px;height:8px;animation-delay:-7.8s}.bubble-u{left:52%;width:11px;height:11px;animation-delay:-3.8s}.bubble-v{left:66%;width:7px;height:7px;animation-delay:-6.8s}.bubble-w{left:88%;width:14px;height:14px;animation-delay:-2.8s}.bubble-x{left:97%;width:9px;height:9px;animation-delay:-5.8s}
@keyframes bubble-rise { 0% { opacity:0; transform:translate(0,0) scale(.65); } 15% { opacity:.8; } 55% { transform:translate(8px,-52vh) scale(1); } 100% { opacity:0; transform:translate(-5px,-108vh) scale(1.08); } }

/* Shared arcade surfaces and clear text hierarchy. */
.hud-bar,.tt-card,.data-note,.quest-card,.achievement-card,.map-expanded-panel,.year-popup,.map-state-panel,.glass { border:0 !important; outline:0 !important; border-radius:var(--r-md) !important; background:var(--glass-bg) !important; -webkit-backdrop-filter:blur(var(--glass-blur)) saturate(140%); backdrop-filter:blur(var(--glass-blur)) saturate(140%); box-shadow:0 8px 24px rgba(0,0,0,.18) !important; color:#e9f8f7; }
.glass { position:relative; isolation:isolate; box-sizing:border-box; min-width:0; }
.glass::after { content:none; }
.glass > * { position:relative; z-index:1; min-width:0; }
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))) { .glass { background:rgba(10,35,65,0.85) !important; } }
.hud-bar { flex:none; min-width:0; min-height:64px; box-sizing:border-box; overflow:visible; padding:var(--space-3) var(--space-2); }
.game-title,.section-kicker,.date-readout,.checkpoint-tag,.toast-kicker,.welcome-title,.step-number,.step-heading { font-weight:700; }
.game-title { color:white; font-size:clamp(26px,calc(2.3vw + 2px),34px); }
.subtitle { color:color-mix(in srgb,var(--c-cyan) 35%,white); font-size:15px; text-shadow:0 0 8px color-mix(in srgb,var(--c-cyan) 40%,transparent); }
.hud-bar > .items-center.gap-3 { min-width:0; max-width:100%; }
.brand-title { position:relative; z-index:0; isolation:isolate; display:inline-block; max-width:calc(100vw - 120px); overflow:visible; color:#FFE066 !important; -webkit-text-fill-color:#FFE066 !important; background:none !important; -webkit-background-clip:border-box; background-clip:border-box; -webkit-text-stroke:0; text-shadow:-2px -2px 0 #FF4FA3,-1px -2px 0 #FF4FA3,0 -2px 0 #FF4FA3,1px -2px 0 #FF4FA3,2px -2px 0 #FF4FA3,-2px -1px 0 #FF4FA3,2px -1px 0 #FF4FA3,-2px 0 0 #FF4FA3,2px 0 0 #FF4FA3,-2px 1px 0 #FF4FA3,2px 1px 0 #FF4FA3,-2px 2px 0 #FF4FA3,-1px 2px 0 #FF4FA3,0 2px 0 #FF4FA3,1px 2px 0 #FF4FA3,2px 2px 0 #FF4FA3,1px 1px 0 #3B1E6B,2px 2px 0 #3B1E6B,3px 3px 0 #3B1E6B,4px 4px 0 #3B1E6B,5px 5px 0 #3B1E6B; font-family:var(--font-pixel) !important; font-size:clamp(3rem,6vw,5rem); font-weight:400 !important; letter-spacing:.06em; line-height:1.5; text-transform:uppercase; white-space:normal; overflow-wrap:normal; animation:brand-float 3s ease-in-out infinite; }
.brand-title::before { content:none; }
@keyframes brand-float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-4px); } }
.section-kicker { color:color-mix(in srgb,var(--c-cyan) 25%,white) !important; font-size:15px; }
.tt-card { padding:var(--space-2) !important; min-width:0; }
.tt-card .text-xs { font-size:15px !important; }
.tt-card .text-sm { font-size:18px !important; }
.tt-card .text-xl { font-size:22px !important; }
.date-readout { color:white !important; font-size:24px; }
.header-status { min-width:0; max-width:min(560px,48vw); text-align:right; }
.today-date { color:white; font-size:18px; font-weight:700; }
.weather-readout,.viewing-readout { max-width:100%; color:color-mix(in srgb,var(--c-cyan) 28%,white); font-size:15px; text-align:right; overflow-wrap:anywhere; }
.weather-credit { color:color-mix(in srgb,var(--c-cyan) 36%,white); font-size:12px; text-align:right; }
.tt-progress .q-linear-progress__label { display:none !important; }
.svg-icon { display:inline-flex; flex:none; align-items:center; justify-content:center; line-height:0; }
.svg-icon svg { display:block; width:1.35em; height:1.35em; fill:none; stroke:currentColor; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }
.brand-icon { color:var(--c-green); }

/* Desktop dashboard uses a quarter-width sidebar beside the map workspace. */
.tt-dashboard { display:grid !important; grid-template-columns:minmax(220px,1fr) minmax(0,3fr); align-items:start !important; gap:var(--space-2) !important; min-height:0; width:100%; }
.species-column { display:flex; flex-direction:column; gap:0; width:100%; min-width:0; height:auto; overflow:visible; font-size:18px; }
.species-column .section-kicker { font-size:15px; }
.species-column .text-sm { font-size:18px !important; }
.species-column .text-xs { font-size:15px !important; }
.data-note { padding:var(--space-2) !important; }
.quest-card,.achievement-card { padding:var(--space-2) !important; min-width:0; }
.map-column { display:flex; flex-direction:column; gap:var(--space-1) !important; min-width:0; width:100%; height:auto; }
.map-card { display:flex; flex-direction:column; min-width:0; max-width:100%; }
.map-scroll { position:relative; flex:none; width:100%; height:72vh; min-height:520px; min-width:0; overflow:hidden; border:0 !important; outline:0 !important; border-radius:var(--r-sm); box-shadow:none !important; }
/* Preserve the teammate's map node and its map-scroll container; it fills the viewport. */
.ocean-map { position:relative; top:0; left:0; width:100%; height:100%; min-width:0; border:0; border-radius:0; background-color:#2ba9c4; background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='512' height='512' viewBox='0 0 512 512'%3E%3Cg fill='none' stroke-linecap='round'%3E%3Cpath stroke='%2387f2e5' stroke-opacity='.20' stroke-width='3' d='M-128 96q64-28 128 0t128 0 128 0 128 0 128 0M-128 224q64-28 128 0t128 0 128 0 128 0 128 0M-128 352q64-28 128 0t128 0 128 0 128 0 128 0M-128 480q64-28 128 0t128 0 128 0 128 0 128 0'/%3E%3Cpath stroke='%23c3fff0' stroke-opacity='.13' stroke-width='2' d='M-128 112q64-20 128 0t128 0 128 0 128 0 128 0M-128 240q64-20 128 0t128 0 128 0 128 0 128 0M-128 368q64-20 128 0t128 0 128 0 128 0 128 0'/%3E%3Cpath stroke='%23fff6cf' stroke-opacity='.23' stroke-width='2' d='M44 152q34-17 68 0t68 0M300 300q34-17 68 0t68 0M132 430q34-17 68 0t68 0'/%3E%3C/g%3E%3Cg fill='%23dcffff' fill-opacity='.58'%3E%3Ccircle cx='74' cy='70' r='3'/%3E%3Ccircle cx='80' cy='58' r='2'/%3E%3Ccircle cx='84' cy='45' r='1.5'/%3E%3Ccircle cx='438' cy='336' r='3'/%3E%3Ccircle cx='432' cy='324' r='2'/%3E%3Ccircle cx='428' cy='311' r='1.5'/%3E%3Ccircle cx='264' cy='270' r='2'/%3E%3Ccircle cx='270' cy='258' r='1'/%3E%3C/g%3E%3C/svg%3E"); background-size:512px 512px; background-position:0 0; background-repeat:repeat; cursor:grab; touch-action:none; user-select:none; }
.ocean-map.is-dragging { cursor:grabbing; }
.ocean-map:focus-visible { outline:3px solid var(--c-gold); outline-offset:-4px; }
.crew-card { border-radius:var(--r-sm) !important; background:rgba(255,255,255,.07) !important; color:#e9f8f7; }
.crew-name { font-size:15px; font-weight:800; line-height:1.2; }
.crew-latin { font-size:12px; font-style:italic; opacity:.75; }
.crew-row { font-size:12px; line-height:1.35; opacity:.92; }
.crew-note { font-size:11px; line-height:1.35; opacity:.7; }
.map-coordinates { position:absolute; z-index:3; right:12px; bottom:12px; max-width:calc(100% - 24px); padding:6px 10px; border:0; border-radius:var(--r-sm); background:rgba(10,35,65,.88); color:#fff; font-size:15px; pointer-events:none; }
.map-state-wrap { flex:none; }
.map-state-panel { width:100%; min-height:48px; box-sizing:border-box; padding:var(--space-1); }
.state-empty .map-state-icon { color:var(--c-cyan); }.state-loading .map-state-icon { color:var(--c-gold); animation:icon-spin 1.5s linear infinite; }.state-error .map-state-icon { color:var(--c-coral); }
@keyframes icon-spin { to { transform:rotate(360deg); } }
.map-state-title { font-size:22px; }.map-state-description { font-size:15px; color:color-mix(in srgb,var(--c-cyan) 25%,white); }
.ocean-picker { flex:none; min-height:48px; padding:var(--space-2) !important; gap:var(--space-1) !important; }
.ocean-button-row { display:flex; width:100%; min-width:0; gap:var(--space-1) !important; flex-wrap:wrap; }
.ocean-picker .section-kicker { line-height:1.4; }
.controls-card { flex:none; }
.control-grid { display:grid !important; grid-template-columns:minmax(0,3fr) minmax(0,2fr); align-items:center; gap:var(--space-2); min-width:0; }
.time-controls,.depth-controls { min-width:0; }
.info-card { flex:none; max-height:160px; min-width:0; overflow:auto; background:var(--glass-bg) !important; -webkit-backdrop-filter:blur(var(--glass-blur)) saturate(140%); backdrop-filter:blur(var(--glass-blur)) saturate(140%); box-shadow:0 8px 24px rgba(0,0,0,.18) !important; border:0 !important; outline:0 !important; }
.date-readout { overflow-wrap:anywhere; }
.checkpoint-tag { padding:var(--space-1); border-radius:var(--r-sm); background:color-mix(in srgb,var(--c-teal) 72%,var(--c-navy)); color:white; font-size:15px; }
.granularity-pill { min-height:32px !important; padding:0 8px !important; font-size:15px !important; }
.timeline-ticks { min-height:28px; padding:0 4px; }
.timeline-tick { position:relative; padding-top:6px; color:color-mix(in srgb,var(--c-cyan) 35%,white); font-size:15px; }
.timeline-tick::before { content:""; position:absolute; top:0; left:50%; width:1px; height:5px; background:color-mix(in srgb,var(--c-cyan) 60%,white); }
.timeline-tick.is-current,.timeline-current { color:var(--c-gold) !important; font-weight:900; }
.timeline-current { padding:2px 6px; border-radius:var(--r-sm); background:rgba(10,35,65,.88); font-size:15px; }
.date-input { flex:0 1 210px; width:min(210px,48%); min-width:0; max-width:100%; }
.date-entry-row,.date-entry-row > * { min-width:0; }
.date-input .q-field__control { min-height:40px; border:0 !important; border-radius:var(--r-sm) !important; background:color-mix(in srgb,var(--c-navy) 60%,var(--c-teal)) !important; box-shadow:none !important; outline:0 !important; }
.date-input .q-field__control,.date-input .q-field__native,.date-input .q-field__input,.date-input input { color:white !important; font-size:20px !important; }
.year-popup { border:0 !important; outline:0 !important; border-radius:var(--r-sm) !important; background:var(--c-navy) !important; box-shadow:0 8px 24px rgba(0,0,0,.18) !important; }
.year-popup .q-item { min-height:40px; color:white !important; font-size:17px !important; }.year-popup .q-item:hover,.year-popup .q-item--highlighted { background:color-mix(in srgb,var(--c-cyan) 22%,var(--c-navy)) !important; }.year-popup .q-item--active { background:var(--c-cyan) !important; color:var(--c-navy) !important; }
.depth-readout { max-width:100%; margin:4px 0; padding:var(--space-1); border:0; border-radius:var(--r-sm); background:color-mix(in srgb,var(--c-teal) 66%,var(--c-navy)); color:white; font-size:15px; box-shadow:none; }
.depth-note { padding:var(--space-2); border-radius:var(--r-sm); background:color-mix(in srgb,var(--c-navy) 42%,var(--c-teal)); color:color-mix(in srgb,var(--c-cyan) 25%,white); font-size:18px; }
.q-slider__track--active { background:var(--c-green) !important; }.q-slider__thumb,.q-slider__pin { color:var(--c-cyan) !important; }

/* Quest and badge cards keep their labels inside their own grid cells. */
.tt-progress { height:10px; overflow:hidden; border-radius:var(--r-sm); background:color-mix(in srgb,var(--c-navy) 75%,var(--c-teal)); box-shadow:none; }
.tt-progress .q-linear-progress__model { background:var(--c-gold) !important; }
.quest-progress-caption { color:color-mix(in srgb,var(--c-cyan) 25%,white); font-size:15px; }
.quest-progress-label { color:var(--c-gold); font-size:15px; }
.badge-count { color:var(--c-gold); font-size:15px; }
.badge-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); grid-auto-rows:1fr; gap:var(--space-1); }
.badge-card { position:relative; display:grid; grid-template-columns:20px minmax(0,1fr); align-items:center; gap:var(--space-1); min-width:0; min-height:56px; padding:var(--space-1); padding-right:22px; border:0; outline:0; box-shadow:none; border-radius:var(--r-sm); background:color-mix(in srgb,var(--c-navy) 48%,var(--c-teal)); }
.badge-card.is-locked { opacity:.62; filter:saturate(.55); }.badge-card.is-unlocked { border-color:var(--c-gold); background:color-mix(in srgb,var(--c-gold) 13%,var(--c-navy)); }
.badge-icon { color:var(--c-gold); }.badge-icon svg { width:18px; height:18px; }.badge-copy { display:flex; flex-direction:column; min-width:0; gap:2px !important; }
.badge-name { display:block; max-width:100%; overflow:hidden; color:white; font-size:15px; text-overflow:ellipsis; white-space:nowrap; }
.badge-description { display:-webkit-box; max-width:100%; overflow:hidden; color:color-mix(in srgb,var(--c-cyan) 22%,white); font-size:15px; text-overflow:ellipsis; -webkit-box-orient:vertical; -webkit-line-clamp:2; }
.badge-lock { position:absolute; top:4px; right:4px; color:color-mix(in srgb,var(--c-cyan) 25%,white); }.badge-lock svg { width:12px; height:12px; }

/* Buttons retain the arcade press feel with tokenized states and focus rings. */
.tt-button,.ocean-pill,.granularity-pill,.depth-readout,.status-chip { border-radius:var(--r-sm) !important; }
.q-btn { min-height:40px; max-width:100%; font-size:16px; font-weight:800 !important; transition:transform .14s ease,filter .14s ease,box-shadow .14s ease; }
.q-btn:hover { filter:brightness(1.08); transform:translateY(-2px); }.q-btn:active { filter:brightness(.96); transform:translateY(2px) scale(.99); box-shadow:var(--shadow-soft) !important; }
.q-btn:focus-visible { outline:2px solid var(--c-gold); outline-offset:2px; }
.tt-button,.ocean-pill,.granularity-pill { border:1px solid color-mix(in srgb,var(--c-cyan) 35%,var(--c-teal)) !important; box-shadow:var(--shadow-raised); }
.enlarge-button { background:var(--c-cyan) !important; color:var(--c-navy) !important; }
.play-button,.start-button { background:var(--c-green) !important; color:var(--c-navy) !important; }.ocean-pill { background:var(--c-teal); color:white; }.granularity-pill { background:color-mix(in srgb,var(--c-teal) 65%,var(--c-navy)); color:white; }
.status-chip { padding:var(--space-1); border:0; color:white; }.info-state-icon { color:var(--c-cyan); }.info-card .state-progress .q-linear-progress__model { background:var(--c-cyan) !important; }
.map-tag { padding:var(--space-1); border-radius:var(--r-sm); background:var(--c-gold); color:var(--c-navy); font-size:15px; font-weight:900; }

/* The same #map node expands in place so Leaflet/MapLibre can observe resize. */
.map-tools { position:absolute; z-index:3; top:12px; right:12px; display:flex; max-width:calc(100% - 24px); padding:8px; border:0; border-radius:var(--r-sm); background:rgba(10,35,65,.92); }
.map-tool-button { min-width:40px; min-height:36px !important; padding:0 10px !important; background:var(--c-teal) !important; color:white !important; box-shadow:var(--shadow-soft); }
.map-modal-backdrop { position:fixed; inset:0; z-index:5008; visibility:hidden; opacity:0; background:rgba(3,10,24,.76); -webkit-backdrop-filter:blur(7px); backdrop-filter:blur(7px); pointer-events:none; transition:opacity .3s ease,visibility .3s ease; }
.map-modal-close { position:fixed !important; top:calc(5vh + 12px); right:calc(2.5vw + 12px); z-index:5012; display:none; background:var(--c-coral) !important; color:var(--c-navy) !important; box-shadow:var(--shadow-raised); }
body.map-modal-open { overflow:hidden !important; }
body.map-modal-open #map-modal-backdrop { visibility:visible; opacity:1; pointer-events:auto; }
body.map-modal-open #map { position:fixed !important; top:5vh; left:2.5vw; z-index:5010; width:95vw; height:90vh; border:0; border-radius:0; box-shadow:none; }
body.map-modal-open #map-modal-close { display:inline-flex; }
body.map-modal-open .map-tools { position:fixed; top:calc(5vh + 12px); right:calc(2.5vw + 132px); z-index:5011; }
body.map-modal-open .map-coordinates { position:fixed; right:calc(2.5vw + 12px); bottom:calc(5vh + 12px); z-index:5011; }
@media (max-width:560px) { body.map-modal-open .map-tools { right:auto; left:calc(2.5vw + 12px); } }

/* Welcome tutorial and reward feedback. */
.welcome-card { width:min(600px,92vw); padding:var(--space-3) !important; border:1px solid color-mix(in srgb,var(--c-cyan) 42%,var(--c-teal)) !important; border-radius:var(--r-lg) !important; background:linear-gradient(145deg,var(--c-teal),var(--c-navy)) !important; color:white; box-shadow:var(--shadow-raised) !important; }
.welcome-mark { margin:0 auto; color:var(--c-green); }.welcome-mark svg { width:56px; height:56px; }.welcome-title { margin-top:var(--space-1); color:white; font-size:25px; text-align:center; }.welcome-title.brand-title { align-self:center; width:100%; max-width:100%; font-size:clamp(3rem,6vw,5rem); text-align:center; }.welcome-copy { margin:var(--space-1) 0 var(--space-2); color:color-mix(in srgb,var(--c-cyan) 25%,white); font-size:18px; text-align:center; }
.tutorial-steps { gap:var(--space-1); }.tutorial-step { padding:var(--space-1); border:1px solid color-mix(in srgb,var(--c-cyan) 25%,var(--c-teal)); border-radius:var(--r-sm); background:color-mix(in srgb,var(--c-navy) 50%,var(--c-teal)); }.step-number { display:grid; width:40px; height:40px; flex:none; place-items:center; border-radius:var(--r-sm); background:var(--c-cyan); color:var(--c-navy); }.step-heading { color:white; font-size:22px; }.step-copy { color:color-mix(in srgb,var(--c-cyan) 25%,white); font-size:15px; }
.achievement-toast { position:fixed; z-index:6000; top:var(--space-3); right:var(--space-3); display:flex; flex-direction:row; align-items:center; gap:var(--space-1); min-width:240px; padding:var(--space-2) !important; border:1px solid var(--c-gold) !important; border-radius:var(--r-md) !important; background:color-mix(in srgb,var(--c-navy) 90%,var(--c-gold)) !important; color:white; box-shadow:var(--shadow-raised) !important; animation:toast-in .25s ease-out both; }
.toast-icon { color:var(--c-gold); }.toast-kicker { color:var(--c-gold); font-size:15px; }.toast-title { color:white; font-size:22px; font-weight:900; }.confetti { position:absolute; top:-5px; width:7px; height:7px; border-radius:2px; background:var(--c-gold); animation:confetti-pop .8s ease-out both; }
.confetti-0{left:12%;background:var(--c-coral)}.confetti-1{left:27%;animation-delay:.04s}.confetti-2{left:41%;background:var(--c-cyan);animation-delay:.08s}.confetti-3{left:56%;background:var(--c-green);animation-delay:.12s}.confetti-4{left:68%;animation-delay:.16s}.confetti-5{left:79%;background:var(--c-coral);animation-delay:.2s}.confetti-6{left:89%;background:var(--c-cyan);animation-delay:.24s}.confetti-7{left:97%;animation-delay:.28s}
@keyframes confetti-pop { from { opacity:0; transform:translateY(14px) rotate(0); } 35% { opacity:1; } to { opacity:0; transform:translateY(-24px) rotate(150deg); } } @keyframes toast-in { from { opacity:0; transform:translateY(-8px); } to { opacity:1; transform:translateY(0); } }
.q-tooltip { max-width:240px; border:1px solid color-mix(in srgb,var(--c-cyan) 35%,var(--c-teal)); border-radius:var(--r-sm); background:var(--c-navy) !important; color:white !important; font-size:15px !important; box-shadow:var(--shadow-soft); }

/* Narrow screens stack the sidebar and workspace, then stack their controls. */
@media (max-width:900px) {
  .tt-dashboard { grid-template-columns:minmax(0,1fr); }
  .species-column { width:100%; }
  .control-grid { grid-template-columns:minmax(0,1fr); }
  .map-scroll { height:64vh; min-height:420px; }
}
@media (max-width:560px) {
  .tt-page { padding:var(--space-1) !important; }
  .hud-bar { flex-wrap:wrap; padding:var(--space-1); }
  .header-status { align-items:flex-start !important; width:100%; max-width:100%; text-align:left; }
  .weather-readout,.viewing-readout,.weather-credit { text-align:left; }
  .map-scroll { height:56vh; min-height:340px; }
  .ocean-picker { gap:4px !important; }.ocean-pill { padding-left:8px !important; padding-right:8px !important; }
  .badge-grid { gap:4px; }.badge-card { gap:4px; padding:6px; padding-right:18px; }
  .badge-name { font-size:14px; }.badge-description { font-size:14px; }
}
@media (max-width:700px) {
  .hud-bar { padding:var(--space-3) var(--space-2); }
  .brand-title { line-height:1.35; }
}
@media (prefers-reduced-motion:reduce) {
  *,*::before,*::after { scroll-behavior:auto !important; animation:none !important; transition:none !important; }
  .brand-title { animation:none !important; }
}

/* Final typography and surface overrides for the requested polish pass. */
body .text-xs { font-size:15px !important; }
.section-kicker,.badge-name,.badge-description,.quest-progress-caption,.quest-progress-label,.badge-count,.timeline-tick,.timeline-current,.depth-readout,.toast-kicker,.step-copy,.weather-readout,.viewing-readout,.q-tooltip { font-size:15px !important; }
.q-field__label,.q-item,.q-field__native,.q-field__input { font-size:15px !important; }
.date-input .q-field__control,.date-input .q-field__native,.date-input .q-field__input,.date-input input { font-size:20px !important; }
.q-btn { font-size:18px !important; }
.step-heading,.toast-title { font-size:22px !important; }
.map-state-panel { border:0 !important; outline:0 !important; box-shadow:none !important; }
.ocean-map:focus-visible { outline:0 !important; }
.data-note,.quest-card,.achievement-card,.info-card,.ocean-picker,.controls-card,.tt-card,.hud-bar,.map-state-panel { min-width:0; }
.tt-progress { box-shadow:none !important; }
.date-input .q-field__control,.date-input .q-field__control:before,.date-input .q-field__control:after { border:0 !important; outline:0 !important; box-shadow:none !important; }
.year-popup,.badge-card,.map-scroll,.status-chip,.map-tools { border:0 !important; outline:0 !important; }
.map-scroll { box-shadow:none !important; }
.hud-bar,.tt-card,.data-note,.quest-card,.achievement-card,.map-expanded-panel,.year-popup,.map-state-panel,.glass,.info-card { background:var(--glass-bg) !important; -webkit-backdrop-filter:blur(var(--glass-blur)) saturate(140%); backdrop-filter:blur(var(--glass-blur)) saturate(140%); box-shadow:0 8px 24px rgba(0,0,0,.18) !important; }
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))) {
  .hud-bar,.tt-card,.data-note,.quest-card,.achievement-card,.map-expanded-panel,.year-popup,.map-state-panel,.glass,.info-card { background:rgba(10,35,65,.85) !important; }
}
"""
