"""Retro aquarium palette and styling for Turtle Tide."""

COLORS = {
    "deep_navy": "#122e4c",
    "ocean_blue": "#285073",
    "tank_cyan": "#35c2d8",
    "lavender": "#a69bdf",
    "mint": "#d9efa0",
    "coral": "#ff8b7f",
    "gold": "#ffd46d",
    "foam": "#eaf8f7",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Quantico:ital,wght@0,400;0,700;1,400;1,700&display=swap');
:root { --deep:#122e4c; --navy:#183653; --panel:#285073; --cyan:#35c2d8; --lav:#a69bdf; --mint:#d9efa0; --coral:#ff8b7f; --gold:#ffd46d; --foam:#eaf8f7; }
body,.q-card,.q-btn,.q-field { font-family:'Quantico',sans-serif !important; }
/* Use the same arcade typeface throughout the interface. */
.game-title,.section-kicker,.date-readout,.status-chip,.ocean-pill,.granularity-pill,.play-button { font-family:'Quantico',sans-serif !important; }
body { position:relative; background:#091b43; color:var(--foam); }
/* A pixel-grid cavern and cyan water glow sit behind the existing interface. */
body::before { content:''; position:fixed; inset:0; z-index:0; pointer-events:none; background:radial-gradient(ellipse 48% 57% at 51% 44%,#1398bc 0%,#087da7 65%,transparent 100%),linear-gradient(110deg,transparent 32%,#a5ffff0c 40%,transparent 47%),linear-gradient(120deg,transparent 55%,#b1ffff0b 61%,transparent 69%),linear-gradient(90deg,#09183f 0%,#142959 9%,#263d75 17%,transparent 25% 75%,#263d75 83%,#142959 91%,#09183f 100%),linear-gradient(180deg,#142653 0%,#142653 7%,transparent 21% 74%,#10234f 100%),repeating-linear-gradient(0deg,transparent 0 15px,#92c9ff08 15px 17px),repeating-linear-gradient(90deg,transparent 0 15px,#92c9ff08 15px 17px); }
body::after { content:''; position:fixed; inset:0; z-index:0; pointer-events:none; animation:ambient-bubbles 8s ease-in-out infinite alternate; background:radial-gradient(circle at 6% 34%,#e2ffff 0 2px,#4ad6eeaa 3px,transparent 7px),radial-gradient(circle at 12% 57%,#c3ffff 0 2px,#55dff099 3px,transparent 8px),radial-gradient(circle at 3% 76%,#c3ffff 0 2px,#55dff099 3px,transparent 7px),radial-gradient(circle at 92% 28%,#d9ffff 0 2px,#55dff099 3px,transparent 8px),radial-gradient(circle at 97% 49%,#c3ffff 0 2px,#55dff099 3px,transparent 7px),radial-gradient(circle at 88% 70%,#c3ffff 0 2px,#55dff099 3px,transparent 8px),radial-gradient(circle at 19% 84%,#c3ffff 0 2px,#55dff099 3px,transparent 7px),radial-gradient(circle at 82% 88%,#c3ffff 0 2px,#55dff099 3px,transparent 7px); }
@keyframes ambient-bubbles { to { transform:translateY(-12px); } }
.tt-page { position:relative; z-index:1; isolation:isolate; color:var(--foam); }
/* Low-poly coral silhouettes decorate the outer bottom corners only. */
.tt-page::before,.tt-page::after { content:''; position:fixed; bottom:0; z-index:-1; width:230px; height:190px; pointer-events:none; opacity:.84; background:linear-gradient(90deg,#ff817e 0%,#ed55b2 42%,#7955d2 100%); filter:drop-shadow(0 0 12px #d93fb866) drop-shadow(90px -8px 0 #7651c9aa); clip-path:polygon(0 100%,0 87%,10% 87%,10% 74%,4% 74%,4% 68%,15% 68%,15% 53%,10% 53%,10% 46%,20% 46%,20% 61%,26% 61%,26% 80%,34% 80%,34% 100%,42% 100%,42% 82%,38% 82%,38% 76%,47% 76%,47% 62%,43% 62%,43% 56%,53% 56%,53% 72%,60% 72%,60% 91%,68% 91%,68% 100%,77% 100%,77% 80%,72% 80%,72% 73%,81% 73%,81% 57%,76% 57%,76% 50%,86% 50%,86% 69%,92% 69%,92% 85%,100% 85%,100% 100%); }
.tt-page::before { left:0; }
.tt-page::after { right:0; transform:scaleX(-1); background:linear-gradient(90deg,#a43db7,#d957c4); }
.hud-bar { padding:12px 18px; border:3px solid #10213d; border-radius:7px; background:linear-gradient(110deg,#193957,#285475); box-shadow:4px 4px 0 #08172f,inset 0 0 0 1px #8ce7e755,inset 0 1px #ffffff35; }
.game-title { color:#f4f1d5; font-size:30px; font-weight:900; line-height:1.2; text-shadow:0 2px #102943; }
.subtitle { color:#a7cbdb; font-size:14px; }
.tt-card { border:3px solid #10213d !important; border-radius:8px !important; background:linear-gradient(150deg,#345f7d,#214568) !important; color:var(--foam); box-shadow:4px 4px 0 #08172f,inset 0 0 0 1px #8ce7e755,inset 0 1px #ffffff24 !important; }
.tt-card .text-xs,.tt-card .text-sm,.tt-card .text-lg,.tt-card .text-xl,.tt-card .text-2xl { color:#e6f7fa !important; }
.tt-card [class*="text-[#"] { color:#e6f7fa !important; }
.tt-card .q-btn { font-family:'Quantico',sans-serif !important; font-weight:900; }
.tt-card .q-btn.ocean-pill,.tt-card .q-btn.granularity-pill,.tt-card .q-btn.play-button { font-family:'Quantico',sans-serif !important; }
.brand-icon { color:#72e1d2; filter:drop-shadow(0 3px 5px #09233999); }
.hud-star { color:#ffd46d; font-size:20px; }
.species-column { background:linear-gradient(155deg,#355b7a,#294a6d) !important; box-shadow:4px 4px 0 #08172f,inset 0 0 0 1px #a6e8f055 !important; }
.section-kicker { color:#a9d9e6 !important; font-size:11px; font-weight:900; letter-spacing:.14em; }
.species-column { font-size:12px; }
.species-column .section-kicker { font-size:9px; }
.species-column .text-sm { font-size:12px !important; line-height:1.45 !important; }
.species-column .text-xs { font-size:10px !important; }
.turtle-mark { font-size:34px; line-height:1; filter:drop-shadow(0 3px 5px #09233999); }
.turtle-mark-small { font-size:30px; line-height:1; }
.checkpoint-tag { border:2px solid #10213d; border-radius:5px; padding:7px 11px; background:#354d78; color:#e4defb; font-family:'Quantico',sans-serif; font-size:13px; box-shadow:3px 3px 0 #08172f; }
.date-input { width:210px; }
.date-input .q-field__control { border:2px solid #10213d; border-radius:5px !important; background:#173a5c !important; color:#eaf8f7 !important; box-shadow:3px 3px 0 #08172f; }
.date-input .q-field__native,.date-input .q-field__input,.date-input input { color:#eaf8f7 !important; font-family:'Quantico',sans-serif !important; font-size:16px !important; }
.date-readout { color:#f2fdff !important; font-family:'Quantico',sans-serif !important; font-size:22px; font-weight:900; letter-spacing:.02em; text-shadow:0 2px #102943; }
.year-popup { background:linear-gradient(150deg,#2d5879,#214568) !important; border:3px solid #10213d; border-radius:5px !important; box-shadow:4px 4px 0 #08172f !important; }
.year-popup .q-item { min-height:42px; color:#e6f7fa !important; font-family:'Quantico',sans-serif !important; font-size:15px !important; }
.year-popup .q-item:hover,.year-popup .q-item--highlighted { background:#ffffff18 !important; }
.year-popup .q-item--active { background:#35c2d8 !important; color:#122e4c !important; }
.data-note { border:2px solid #10213d; border-radius:5px !important; background:linear-gradient(145deg,#173b5c,#1c4463); box-shadow:3px 3px 0 #08172f,inset 0 0 0 1px #8ce7e744; }
.empty-icon { color:#72e1d2; }
.quest-card { border:2px solid #10213d !important; border-radius:5px !important; background:linear-gradient(145deg,#536085,#3e5276) !important; box-shadow:3px 3px 0 #08172f,inset 0 0 0 1px #d4cfff55 !important; }
.tt-progress { height:13px; border-radius:99px; overflow:hidden; background:#152f4c; box-shadow:inset 0 2px 4px #061b2e88; }
.map-card { background:linear-gradient(155deg,#345f7d,#214569) !important; box-shadow:4px 4px 0 #08172f,inset 0 0 0 1px #8ce7e755 !important; }
.map-tag { border:2px solid #10213d; border-radius:5px; padding:7px 11px; background:#a69bdf; color:#183653; font-size:10px; font-weight:900; box-shadow:3px 3px 0 #08172f; }
.map-scroll,.map-expanded-scroll { height:clamp(390px,54vh,650px); overflow:auto; overscroll-behavior:contain; border:2px solid #10213d; border-radius:6px; scrollbar-color:#45c7dc #183653; scrollbar-width:thin; }
.map-scroll::-webkit-scrollbar,.map-expanded-scroll::-webkit-scrollbar { width:12px; height:12px; }
.map-scroll::-webkit-scrollbar-track,.map-expanded-scroll::-webkit-scrollbar-track { background:#183653aa; border-radius:10px; }
.map-scroll::-webkit-scrollbar-thumb,.map-expanded-scroll::-webkit-scrollbar-thumb { background:#45c7dc; border:3px solid #183653; border-radius:10px; }
.ocean-map { width:1600px; height:1100px; border:0; border-radius:5px; position:relative; background:radial-gradient(ellipse at 48% 28%,#b1fff066,transparent 42%),radial-gradient(ellipse at 76% 76%,#26a6d466,transparent 48%),linear-gradient(180deg,#3ec3dc,#27abc9 65%,#1784ae); box-shadow:0 0 28px #2ad4e033,inset 0 0 34px #c6ffff22; cursor:zoom-in; }
.map-expanded-panel { width:min(96vw,1500px); max-width:96vw; border:3px solid #10213d !important; border-radius:7px !important; padding:18px !important; background:linear-gradient(145deg,#244d70,#173a5b) !important; color:var(--foam); box-shadow:4px 4px 0 #08172f,inset 0 0 0 1px #8ce7e755 !important; }
.map-expanded-scroll { width:min(92vw,1400px); height:80vh; }
.map-expanded-canvas { width:2000px; height:1500px; border-radius:5px; background:radial-gradient(ellipse at 48% 28%,#b1fff066,transparent 42%),radial-gradient(ellipse at 76% 76%,#26a6d466,transparent 48%),linear-gradient(180deg,#3ec3dc,#27abc9 65%,#1784ae); box-shadow:inset 0 0 0 2px #d8ffff66; }
.ocean-map:before { content:''; position:absolute; inset:0; pointer-events:none; background:linear-gradient(112deg,transparent 24%,#d9ffff16 43%,transparent 61%); }
.ocean-picker { padding:2px 0; }
.ocean-pill { border:2px solid #10213d !important; border-radius:5px !important; font-weight:900 !important; box-shadow:3px 3px 0 #08172f; transition:transform .15s,filter .15s,box-shadow .15s; }
.ocean-pill:hover { transform:translateY(-3px) scale(1.04); filter:brightness(1.1); }
.controls-card { background:linear-gradient(135deg,#173a5c,#1e4667) !important; box-shadow:4px 4px 0 #08172f,inset 0 0 0 1px #8ce7e755 !important; }
.granularity-pill { border:2px solid #10213d !important; border-radius:5px !important; background:#354d78; color:#e4defb; box-shadow:3px 3px 0 #08172f; font-weight:900 !important; }
.play-button { border:2px solid #10213d !important; border-radius:5px !important; background:linear-gradient(180deg,#82e19c,#55c47a) !important; color:#143b4d !important; box-shadow:3px 3px 0 #08172f !important; font-weight:900 !important; }
.tt-button { transition:transform .12s,filter .12s,box-shadow .12s; }
.tt-button:hover { filter:brightness(1.1); transform:translateY(-2px); }
.tt-button:active { transform:translateY(3px); box-shadow:0 1px 0 #318558 !important; }
.depth-readout { border:2px solid #10213d; border-radius:5px; padding:6px 10px; background:#1d7897; color:#e9fbff; font-size:12px; font-weight:900; box-shadow:3px 3px 0 #08172f; }
.q-slider__track--active { background:#35c2d8 !important; }
.q-slider__thumb { color:#35c2d8 !important; }
.status-chip { border:2px solid #10213d; border-radius:5px; padding:9px 13px; font-weight:900; box-shadow:3px 3px 0 #08172f,inset 0 1px #fff8; }
.xp-chip { background:linear-gradient(180deg,#ebf6b9,#cee795); color:#38593b; }
.heart-chip { background:linear-gradient(180deg,#c0b6ef,#9184d5); color:#ff6584; }
.info-card { background:linear-gradient(145deg,#345f7d,#264869) !important; }
.fish-drift { position:relative; flex:none; width:100%; height:38px; overflow:hidden; pointer-events:none; }
.swimming-fish { position:absolute; left:-3rem; top:2px; z-index:2; color:#79e5ed; font-size:26px; filter:drop-shadow(0 2px 4px #09233977); animation:fish-right 25s linear infinite; }
.swim-left { left:auto; right:-3rem; animation-name:fish-left; }
.fish-b { top:17px; color:#ffb76a; font-size:20px; animation-duration:34s; animation-delay:-12s; }
.fish-c { top:0; color:#a69bdf; font-size:23px; animation-duration:30s; animation-delay:-22s; }
.fish-d { top:11px; color:#ffb76a; animation-duration:31s; animation-delay:-8s; }
.fish-e { top:1px; color:#79e5ed; font-size:21px; animation-duration:27s; animation-delay:-19s; }
.fish-f { top:16px; color:#a69bdf; font-size:25px; animation-duration:36s; animation-delay:-27s; }
@keyframes fish-right { from { left:-3rem; transform:scaleX(-1); } to { left:calc(100% + 3rem); transform:scaleX(-1); } }
@keyframes fish-left { from { right:-3rem; } to { right:calc(100% + 3rem); } }
.bubble { position:absolute; bottom:0; width:9px; height:9px; border:1px solid #bffaff; border-radius:50%; background:radial-gradient(circle at 30% 25%,#fff,#a6f5f5 45%,#47b9db); box-shadow:0 0 8px #83efff99; animation:bubble-rise 4.6s ease-in infinite; }
.bubble-a { left:17%; animation-delay:-2s; }
.bubble-b { left:78%; width:6px; height:6px; animation-delay:-3.5s; }
.bubble-c { left:28%; width:7px; height:7px; animation-delay:-1.2s; }
.bubble-d { left:72%; animation-delay:-4s; }
@keyframes bubble-rise { 0% { opacity:0; transform:translateY(8px) scale(.7); } 20% { opacity:.8; } 100% { opacity:0; transform:translateY(-40px) scale(1.15); } }
@media (prefers-reduced-motion:reduce) { body::after,.swimming-fish,.bubble,.tt-button,.ocean-pill { animation:none !important; transition:none !important; } }
@media (max-width:1050px) { .tt-dashboard { flex-wrap:wrap !important; } .species-column { flex:1 1 220px; } .map-column { flex:4 1 520px; } }
@media (max-width:650px) { .tt-page { padding-left:10px !important; padding-right:10px !important; } .map-scroll { height:380px; } .ocean-map { width:1150px; height:850px; } .map-expanded-canvas { width:1500px; height:1200px; } .map-expanded-scroll { height:75vh; } .game-title { font-size:24px; } }
"""
