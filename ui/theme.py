"""Turtle Tide palette and small shared CSS layer."""

COLORS = {
    "ink": "#21465b",
    "green": "#58bd73",
    "green_dark": "#369454",
    "blue": "#48b8dc",
    "yellow": "#ffd45e",
    "orange": "#ff9c55",
    "coral": "#ff7f78",
    "paper": "#f2f8f7",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800;900&display=swap');
body, .q-card, .q-btn, .q-field { font-family: 'Nunito', sans-serif !important; }
body { background: #f2f8f7; color: #21465b; }
.tt-card { border: 2px solid #e4eeee; border-radius: 24px !important; box-shadow: 0 5px 0 #e5eeee !important; }
.tt-button { border-radius: 16px !important; font-weight: 900 !important; box-shadow: 0 4px 0 #328750 !important; transition: transform .08s, box-shadow .08s; }
.tt-button:active { transform: translateY(3px); box-shadow: 0 1px 0 #328750 !important; }
.tt-pill { border-radius: 999px !important; font-weight: 900 !important; }
.tt-progress { height: 14px; border-radius: 999px; overflow: hidden; }
.species-card { transition: transform .15s; }
.species-card:hover { transform: translateY(-3px); }
.ocean-map { min-height: 330px; border-radius: 24px; background: radial-gradient(ellipse at 50% 50%, #b5e9f4 0, #8bd6eb 56%, #66c4e0 100%); position: relative; overflow: hidden; }
.ocean-map:before,.ocean-map:after { content:''; position:absolute; inset:10%; border:2px solid #ffffff55; border-radius:50%; transform:scaleX(1.35); }
.ocean-map:after { inset:20% 28%; transform:scaleX(1.1); }
.map-wave { position:absolute; color:#ffffffbb; font-size:34px; letter-spacing:14px; transform:rotate(-12deg); }
.map-island { position:absolute; background:#a7d995; border:4px solid #87c67d; border-radius:60% 40% 53% 47%; box-shadow:inset -7px -5px #85c579; }
.info-hidden { display:none; }
"""
