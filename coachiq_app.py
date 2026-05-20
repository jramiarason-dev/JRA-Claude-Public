import streamlit as st
import os
import re
import hashlib
import random as _rng_mod
import requests
from datetime import date, datetime, timedelta
import calendar as cal_mod

def safe_parse_date(date_str, output_format="%d %b"):
    if not date_str:
        return ""
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S", "%d-%m-%Y", "%Y/%m/%d"]:
        try:
            return datetime.strptime(date_str, fmt).strftime(output_format)
        except ValueError:
            continue
    return str(date_str)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CoachIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ══ Reset & base ══ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background-color: #080808 !important;
    color: #f0f0f0 !important;
    font-family: 'Inter', sans-serif !important;
}

/* noise overlay */
[data-testid="stAppViewContainer"]::before {
    content:"";
    position:fixed;inset:0;pointer-events:none;z-index:9999;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
    opacity:0.035;
}

/* ══ Sidebar ══ */
[data-testid="stSidebar"] {
    background:#0e0e0e !important;
    border-right:1px solid #1a1a1a !important;
}
[data-testid="stSidebar"] * { color:#f0f0f0 !important; }

/* ══ Typography ══ */
.bbn { font-family:'Bebas Neue',sans-serif !important; letter-spacing:0.04em; }

/* ══ Hide Streamlit chrome ══ */
#MainMenu, footer, header { visibility:hidden; }
[data-testid="stToolbar"] { display:none; }

/* ══ Buttons ══ */
[data-testid="stButton"] > button {
    background:#141414 !important;
    color:#f0f0f0 !important;
    border:1px solid #222 !important;
    border-radius:8px !important;
    font-family:'Inter',sans-serif !important;
    font-size:0.85rem !important;
    font-weight:600 !important;
    padding:0.5rem 1.2rem !important;
    transition:all .2s ease !important;
}
[data-testid="stButton"] > button:hover {
    border-color:#CAFF33 !important;
    color:#CAFF33 !important;
    box-shadow:0 0 12px rgba(202,255,51,.15) !important;
}

/* ══ Accent button ══ */
.btn-accent > button {
    background:#CAFF33 !important;
    color:#080808 !important;
    border:none !important;
    font-weight:700 !important;
}
.btn-accent > button:hover {
    background:#d8ff5a !important;
    color:#080808 !important;
    box-shadow:0 0 18px rgba(202,255,51,.4) !important;
}

/* ══ Sport filter buttons active ══ */
.sport-btn-active > button {
    background:#CAFF33 !important;
    color:#080808 !important;
    border:none !important;
    font-weight:700 !important;
}

/* ══ Tabs ══ */
[data-testid="stTabs"] [role="tablist"] {
    background:#111 !important;
    border-radius:10px !important;
    padding:4px !important;
    border:1px solid #1e1e1e !important;
    gap:4px !important;
}
[data-testid="stTabs"] button[role="tab"] {
    background:transparent !important;
    color:#666 !important;
    border-radius:7px !important;
    font-family:'Inter',sans-serif !important;
    font-weight:600 !important;
    font-size:0.85rem !important;
    border:none !important;
    padding:0.5rem 1rem !important;
    transition:all .2s !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background:#CAFF33 !important;
    color:#080808 !important;
}
[data-testid="stTabs"] [role="tabpanel"] {
    background:#0f0f0f !important;
    border:1px solid #1e1e1e !important;
    border-radius:0 10px 10px 10px !important;
    padding:1.5rem !important;
    margin-top:-1px !important;
}

/* ══ Cards ══ */
.match-card {
    background:#111;
    border:1px solid #1e1e1e;
    border-radius:14px;
    padding:1.25rem 1.5rem;
    margin-bottom:.5rem;
    transition:all .25s ease;
    cursor:pointer;
    position:relative;
    overflow:hidden;
    height:140px;
    box-sizing:border-box;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}
.match-card::before {
    content:"";position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,#CAFF33,transparent);
    opacity:0;transition:opacity .25s;
}
.match-card:hover { border-color:#2a2a2a; box-shadow:0 8px 32px rgba(0,0,0,.4); }
.match-card:hover::before { opacity:1; }
.match-card.selected {
    border-color:#CAFF33 !important;
    box-shadow:0 0 24px rgba(202,255,51,.15) !important;
}
.match-card.selected::before { opacity:1; }

/* status badges */
.badge { display:inline-block;padding:.2rem .7rem;border-radius:20px;font-size:.72rem;font-weight:700;letter-spacing:.05em; }
.badge-live { background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.3); }
.badge-done { background:rgba(100,100,100,.15);color:#888;border:1px solid #2a2a2a; }
.badge-soon { background:rgba(202,255,51,.1);color:#CAFF33;border:1px solid rgba(202,255,51,.3); }

/* team badge */
.team-badge {
    width:52px;height:52px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-family:'Bebas Neue',sans-serif;font-size:1.1rem;color:#fff;
    font-weight:900;flex-shrink:0;
}
.score-box {
    font-family:'Bebas Neue',sans-serif;font-size:2.4rem;
    color:#f0f0f0;letter-spacing:.05em;line-height:1;
}
.score-sep { color:#333;margin:0 .4rem;font-family:'Bebas Neue',sans-serif;font-size:2rem; }
.team-name { font-weight:700;font-size:.95rem;color:#f0f0f0;white-space:nowrap; }
.team-name-sm { font-size:.75rem;color:#555;margin-top:.1rem; }
.comp-label {
    font-size:.7rem;font-weight:700;color:#555;
    text-transform:uppercase;letter-spacing:.1em;margin-bottom:.6rem;
}
.meta-row { font-size:.75rem;color:#444;margin-top:.6rem; }

/* ══ Section titles ══ */
.section-title {
    font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
    color:#f0f0f0;letter-spacing:.06em;margin-bottom:1rem;
}
.section-title span { color:#CAFF33; }

/* ══ Player row ══ */
.player-row { display:flex;align-items:center;gap:.8rem;margin-bottom:.75rem; }
.player-note {
    font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
    min-width:2.5rem;text-align:center;
}
.player-bar-wrap { flex:1;height:6px;background:#1a1a1a;border-radius:3px;overflow:hidden; }
.player-bar { height:100%;border-radius:3px;transition:width .5s ease; }
.player-name { font-weight:600;font-size:.85rem;min-width:130px; }
.player-poste { font-size:.7rem;color:#555;min-width:30px; }
.player-stats { font-size:.75rem;color:#555; }

/* ══ Verdict scores ══ */
.verdict-score {
    background:#141414;border:1px solid #1e1e1e;border-radius:12px;
    padding:1rem 1.5rem;text-align:center;
}
.verdict-score .label { font-size:.7rem;color:#555;text-transform:uppercase;letter-spacing:.1em; }
.verdict-score .value {
    font-family:'Bebas Neue',sans-serif;font-size:2.8rem;
    background:linear-gradient(135deg,#CAFF33,#90ee2a);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    line-height:1.1;
}

/* ══ Stat bar ══ */
.stat-row { margin-bottom:.6rem; }
.stat-label { font-size:.75rem;color:#666;display:flex;justify-content:space-between;margin-bottom:.3rem; }
.stat-bar-bg { height:5px;background:#1a1a1a;border-radius:3px;position:relative; }
.stat-bar-home { position:absolute;top:0;left:0;height:100%;background:#CAFF33;border-radius:3px; }
.stat-bar-away { position:absolute;top:0;right:0;height:100%;background:#3b82f6;border-radius:3px; }

/* ══ Calendar ══ */
.cal-grid {
    display:grid;grid-template-columns:repeat(7,1fr);gap:3px;
    margin-top:.5rem;
}
.cal-day {
    aspect-ratio:1;display:flex;flex-direction:column;
    align-items:center;justify-content:center;
    font-size:.72rem;border-radius:6px;cursor:pointer;
    position:relative;color:#555;
}
.cal-day.has-match { color:#f0f0f0; }
.cal-day.today { border:1px solid #333;color:#f0f0f0; }
.cal-day.selected-day { background:#CAFF33;color:#080808;font-weight:700; }
.cal-day .dot {
    width:4px;height:4px;border-radius:50%;
    background:#CAFF33;margin-top:2px;
}
.cal-header { font-size:.62rem;color:#444;text-align:center;padding:.2rem 0; }

/* ══ Formation pitch ══ */
.pitch {
    background:linear-gradient(180deg,#0d2e0d 0%,#0f3a0f 50%,#0d2e0d 100%);
    border:1px solid #1a401a;border-radius:10px;
    padding:1rem;position:relative;min-height:280px;
    display:flex;flex-direction:column;justify-content:space-between;
}
.formation-row {
    display:flex;justify-content:center;gap:1.5rem;
    padding:.3rem 0;
}
.player-dot {
    width:38px;height:38px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-size:.6rem;font-weight:700;text-align:center;
    cursor:default;border:2px solid rgba(255,255,255,.2);
}
.pitch-label {
    font-family:'Bebas Neue',sans-serif;font-size:.8rem;
    color:rgba(255,255,255,.25);text-align:center;letter-spacing:.15em;
}

/* ══ Fort/Faible cards ══ */
.point-fort { background:rgba(202,255,51,.06);border:1px solid rgba(202,255,51,.15);
    border-radius:8px;padding:.7rem 1rem;margin-bottom:.5rem;font-size:.85rem; }
.point-faible { background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.15);
    border-radius:8px;padding:.7rem 1rem;margin-bottom:.5rem;font-size:.85rem; }
.verdict-card {
    background:#141414;border:1px solid #1e1e1e;border-radius:12px;
    padding:1.2rem;margin-bottom:.75rem;font-size:.88rem;line-height:1.6;color:#ccc;
}

/* ══ Dividers ══ */
.div-line { border:none;border-top:1px solid #1a1a1a;margin:1rem 0; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

TODAY = date.today()
D_M12 = (TODAY - timedelta(days=12)).isoformat()
D_M10 = (TODAY - timedelta(days=10)).isoformat()
D_M9  = (TODAY - timedelta(days=9)).isoformat()
D_M8  = (TODAY - timedelta(days=8)).isoformat()
D_M7  = (TODAY - timedelta(days=7)).isoformat()
D_M5  = (TODAY - timedelta(days=5)).isoformat()
D_M4  = (TODAY - timedelta(days=4)).isoformat()
D_M3  = (TODAY - timedelta(days=3)).isoformat()
D_M2  = (TODAY - timedelta(days=2)).isoformat()
D_P2  = (TODAY + timedelta(days=2)).isoformat()
D_P3  = (TODAY + timedelta(days=3)).isoformat()
D_P4  = (TODAY + timedelta(days=4)).isoformat()
D_P5  = (TODAY + timedelta(days=5)).isoformat()
D_P6  = (TODAY + timedelta(days=6)).isoformat()
D_P7  = (TODAY + timedelta(days=7)).isoformat()

SPORTS = ["⚽ Football", "🏀 Basket", "🏉 Rugby"]

COMPETITIONS_BY_SPORT = {
    "⚽ Football": ["Ligue 1", "La Liga", "Champions League", "Premier League", "Super League Suisse"],
    "🏀 Basket": ["NBA", "Euroleague", "Betclic Elite"],
    "🏉 Rugby": ["Top 14", "Pro D2", "Champions Cup"],
}

def badge(color, initials):
    return f'<div class="team-badge" style="background:{color}">{initials}</div>'

MATCHES = {
    # ── Ligue 1 ───────────────────────────────────────────────────────────────
    "psg_monaco_l1": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": D_M10, "time": "21:00", "stadium": "Parc des Princes, Paris", "status": "Terminé",
        "home": {"name": "Paris Saint-Germain", "short": "PSG", "color": "#004174", "score": 2},
        "away": {"name": "AS Monaco",           "short": "MCO", "color": "#E4002B", "score": 0},
    },
    "marseille_lyon": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": D_M8, "time": "20:45", "stadium": "Orange Vélodrome, Marseille", "status": "Terminé",
        "home": {"name": "Olympique de Marseille", "short": "OM",  "color": "#2CBFEF", "score": 1},
        "away": {"name": "Olympique Lyonnais",     "short": "OL",  "color": "#1A1A1A", "score": 1},
    },
    "monaco_lille": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": D_M5, "time": "17:00", "stadium": "Stade Louis II, Monaco", "status": "Terminé",
        "home": {"name": "AS Monaco", "short": "MCO", "color": "#E4002B", "score": 2},
        "away": {"name": "LOSC Lille", "short": "LIL", "color": "#E4002B", "score": 1},
    },
    "nice_lens": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": D_M3, "time": "19:00", "stadium": "Allianz Riviera, Nice", "status": "Terminé",
        "home": {"name": "OGC Nice", "short": "NIC", "color": "#E4002B", "score": 0},
        "away": {"name": "RC Lens",  "short": "LEN", "color": "#EEB111", "score": 2},
    },
    "psg_toulouse": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": D_P4, "time": "21:00", "stadium": "Parc des Princes, Paris", "status": "À venir",
        "home": {"name": "Paris Saint-Germain", "short": "PSG", "color": "#004174", "score": None},
        "away": {"name": "Toulouse FC",          "short": "TFC", "color": "#7B1D3E", "score": None},
    },
    "brest_rennes": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": D_P7, "time": "15:00", "stadium": "Stade Francis-Le Blé, Brest", "status": "À venir",
        "home": {"name": "Stade Brestois 29", "short": "SB2", "color": "#CC0000", "score": None},
        "away": {"name": "Stade Rennais",     "short": "REN", "color": "#B22234", "score": None},
    },
    # ── Premier League ────────────────────────────────────────────────────────
    "arsenal_mancity_pl": {
        "sport": "⚽ Football", "competition": "Premier League",
        "date": D_M12, "time": "17:30", "stadium": "Emirates Stadium, Londres", "status": "Terminé",
        "home": {"name": "Arsenal FC",      "short": "ARS", "color": "#EF0107", "score": 2},
        "away": {"name": "Manchester City", "short": "MCI", "color": "#6CABDD", "score": 2},
    },
    "liverpool_chelsea": {
        "sport": "⚽ Football", "competition": "Premier League",
        "date": D_M9, "time": "16:30", "stadium": "Anfield, Liverpool", "status": "Terminé",
        "home": {"name": "Liverpool FC", "short": "LIV", "color": "#C8102E", "score": 3},
        "away": {"name": "Chelsea FC",   "short": "CHE", "color": "#034694", "score": 1},
    },
    "tottenham_manutd": {
        "sport": "⚽ Football", "competition": "Premier League",
        "date": D_M7, "time": "14:00", "stadium": "Tottenham Hotspur Stadium, Londres", "status": "Terminé",
        "home": {"name": "Tottenham Hotspur",  "short": "TOT", "color": "#132257", "score": 0},
        "away": {"name": "Manchester United",  "short": "MUN", "color": "#DA291C", "score": 1},
    },
    "newcastle_astonvilla": {
        "sport": "⚽ Football", "competition": "Premier League",
        "date": D_M4, "time": "15:00", "stadium": "St. James' Park, Newcastle", "status": "Terminé",
        "home": {"name": "Newcastle United", "short": "NEW", "color": "#241F20", "score": 2},
        "away": {"name": "Aston Villa",      "short": "AVL", "color": "#95BFE5", "score": 0},
    },
    "arsenal_brighton": {
        "sport": "⚽ Football", "competition": "Premier League",
        "date": D_P2, "time": "15:00", "stadium": "Emirates Stadium, Londres", "status": "À venir",
        "home": {"name": "Arsenal FC",         "short": "ARS", "color": "#EF0107", "score": None},
        "away": {"name": "Brighton & Hove Albion", "short": "BHA", "color": "#0057B8", "score": None},
    },
    "mancity_westham": {
        "sport": "⚽ Football", "competition": "Premier League",
        "date": D_P5, "time": "16:00", "stadium": "Etihad Stadium, Manchester", "status": "À venir",
        "home": {"name": "Manchester City", "short": "MCI", "color": "#6CABDD", "score": None},
        "away": {"name": "West Ham United", "short": "WHU", "color": "#7A263A", "score": None},
    },
    # ── Champions League ──────────────────────────────────────────────────────
    "realmadrid_arsenal_cl": {
        "sport": "⚽ Football", "competition": "Champions League",
        "date": D_M9, "time": "21:00", "stadium": "Santiago Bernabéu, Madrid", "status": "Terminé",
        "home": {"name": "Real Madrid CF", "short": "RMA", "color": "#FEBE10", "score": 2},
        "away": {"name": "Arsenal FC",     "short": "ARS", "color": "#EF0107", "score": 1},
    },
    "bayernpsg_cl": {
        "sport": "⚽ Football", "competition": "Champions League",
        "date": D_M7, "time": "21:00", "stadium": "Allianz Arena, Munich", "status": "Terminé",
        "home": {"name": "Bayern Munich",       "short": "FCB", "color": "#DC052D", "score": 1},
        "away": {"name": "Paris Saint-Germain", "short": "PSG", "color": "#004174", "score": 1},
    },
    "inter_barcelona_cl": {
        "sport": "⚽ Football", "competition": "Champions League",
        "date": D_M5, "time": "21:00", "stadium": "San Siro, Milan", "status": "Terminé",
        "home": {"name": "Inter Milan",  "short": "INT", "color": "#0033A0", "score": 0},
        "away": {"name": "FC Barcelona", "short": "BAR", "color": "#A50044", "score": 2},
    },
    "atletico_bvb_cl": {
        "sport": "⚽ Football", "competition": "Champions League",
        "date": D_P3, "time": "21:00", "stadium": "Wanda Metropolitano, Madrid", "status": "À venir",
        "home": {"name": "Atlético de Madrid",     "short": "ATM", "color": "#CB3524", "score": None},
        "away": {"name": "Borussia Dortmund", "short": "BVB", "color": "#FDE100", "score": None},
    },
    "juventus_porto_cl": {
        "sport": "⚽ Football", "competition": "Champions League",
        "date": D_P6, "time": "21:00", "stadium": "Juventus Stadium, Turin", "status": "À venir",
        "home": {"name": "Juventus FC", "short": "JUV", "color": "#000000", "score": None},
        "away": {"name": "FC Porto",    "short": "POR", "color": "#004494", "score": None},
    },
    # ── Super League Suisse ───────────────────────────────────────────────────
    "basel_yb_ssl": {
        "sport": "⚽ Football", "competition": "Super League Suisse",
        "date": D_M10, "time": "18:30", "stadium": "St. Jakob-Park, Bâle", "status": "Terminé",
        "home": {"name": "FC Basel",      "short": "FCB", "color": "#CC0000", "score": 2},
        "away": {"name": "BSC Young Boys","short": "YB",  "color": "#FFD700", "score": 1},
    },
    "servette_zurich_ssl": {
        "sport": "⚽ Football", "competition": "Super League Suisse",
        "date": D_M7, "time": "16:30", "stadium": "Stade de Genève, Genève", "status": "Terminé",
        "home": {"name": "Servette FC",  "short": "SFC", "color": "#AA0000", "score": 1},
        "away": {"name": "FC Zurich",    "short": "FCZ", "color": "#0032A0", "score": 0},
    },
    "lugano_luzern_ssl": {
        "sport": "⚽ Football", "competition": "Super League Suisse",
        "date": D_M4, "time": "16:00", "stadium": "Cornaredo, Lugano", "status": "Terminé",
        "home": {"name": "FC Lugano", "short": "LUG", "color": "#000080", "score": 2},
        "away": {"name": "FC Luzern", "short": "FCL", "color": "#0066CC", "score": 2},
    },
    "yb_stgallen_ssl": {
        "sport": "⚽ Football", "competition": "Super League Suisse",
        "date": D_M2, "time": "18:00", "stadium": "Stade de Suisse, Berne", "status": "Terminé",
        "home": {"name": "BSC Young Boys", "short": "YB",  "color": "#FFD700", "score": 3},
        "away": {"name": "FC St. Gallen",  "short": "FCSG","color": "#007A47", "score": 0},
    },
    "basel_servette_ssl": {
        "sport": "⚽ Football", "competition": "Super League Suisse",
        "date": D_P5, "time": "18:30", "stadium": "St. Jakob-Park, Bâle", "status": "À venir",
        "home": {"name": "FC Basel",     "short": "FCB", "color": "#CC0000", "score": None},
        "away": {"name": "Servette FC",  "short": "SFC", "color": "#AA0000", "score": None},
    },
    # ── NBA ───────────────────────────────────────────────────────────────────
    "lakers_warriors_nba": {
        "sport": "🏀 Basket", "competition": "NBA",
        "date": D_M12, "time": "04:00", "stadium": "Crypto.com Arena, Los Angeles", "status": "Terminé",
        "home": {"name": "Los Angeles Lakers",  "short": "LAL", "color": "#552583", "score": 108},
        "away": {"name": "Golden State Warriors","short": "GSW", "color": "#1D428A", "score": 95},
    },
    "celtics_bulls": {
        "sport": "🏀 Basket", "competition": "NBA",
        "date": D_M10, "time": "01:30", "stadium": "TD Garden, Boston", "status": "Terminé",
        "home": {"name": "Boston Celtics", "short": "BOS", "color": "#007A33", "score": 118},
        "away": {"name": "Chicago Bulls",  "short": "CHI", "color": "#CE1141", "score": 102},
    },
    "heat_knicks": {
        "sport": "🏀 Basket", "competition": "NBA",
        "date": D_M8, "time": "01:00", "stadium": "Kaseya Center, Miami", "status": "Terminé",
        "home": {"name": "Miami Heat",   "short": "MIA", "color": "#98002E", "score": 105},
        "away": {"name": "New York Knicks","short": "NYK","color": "#006BB6", "score": 110},
    },
    "bucks_suns": {
        "sport": "🏀 Basket", "competition": "NBA",
        "date": D_M5, "time": "02:30", "stadium": "Fiserv Forum, Milwaukee", "status": "Terminé",
        "home": {"name": "Milwaukee Bucks","short": "MIL","color": "#00471B", "score": 122},
        "away": {"name": "Phoenix Suns",   "short": "PHX","color": "#1D1160", "score": 115},
    },
    "lakers_clippers": {
        "sport": "🏀 Basket", "competition": "NBA",
        "date": D_M2, "time": "04:30", "stadium": "Crypto.com Arena, Los Angeles", "status": "Terminé",
        "home": {"name": "Los Angeles Lakers",  "short": "LAL", "color": "#552583", "score": 98},
        "away": {"name": "LA Clippers",         "short": "LAC", "color": "#1D428A", "score": 112},
    },
    "warriors_nuggets": {
        "sport": "🏀 Basket", "competition": "NBA",
        "date": D_P4, "time": "04:00", "stadium": "Chase Center, San Francisco", "status": "À venir",
        "home": {"name": "Golden State Warriors","short": "GSW","color": "#1D428A", "score": None},
        "away": {"name": "Denver Nuggets",       "short": "DEN","color": "#0E2240", "score": None},
    },
    # ── Euroleague ────────────────────────────────────────────────────────────
    "realmadrid_olympiacos_euro": {
        "sport": "🏀 Basket", "competition": "Euroleague",
        "date": D_M9, "time": "21:00", "stadium": "WiZink Center, Madrid", "status": "Terminé",
        "home": {"name": "Real Madrid Baloncesto","short": "RMA","color": "#FEBE10", "score": 88},
        "away": {"name": "Olympiacos BC",         "short": "OLY","color": "#E31F26", "score": 79},
    },
    "barcelona_fenerbahce_euro": {
        "sport": "🏀 Basket", "competition": "Euroleague",
        "date": D_M7, "time": "20:00", "stadium": "Palau Blaugrana, Barcelone", "status": "Terminé",
        "home": {"name": "FC Barcelona Bàsquet","short": "BAR","color": "#A50044", "score": 92},
        "away": {"name": "Fenerbahce Beko",     "short": "FBK","color": "#FFB900", "score": 85},
    },
    "monaco_cska_euro": {
        "sport": "🏀 Basket", "competition": "Euroleague",
        "date": D_M5, "time": "20:30", "stadium": "Salle Gaston Médecin, Monaco", "status": "Terminé",
        "home": {"name": "AS Monaco Basket","short": "MCO","color": "#B5121B", "score": 78},
        "away": {"name": "CSKA Moscow",     "short": "CSK","color": "#E31F26", "score": 82},
    },
    "bayernmaccabi_euro": {
        "sport": "🏀 Basket", "competition": "Euroleague",
        "date": D_M2, "time": "20:00", "stadium": "SAP Garden, Munich", "status": "Terminé",
        "home": {"name": "Bayern Munich Basketball","short": "BAY","color": "#DC052D", "score": 84},
        "away": {"name": "Maccabi Tel Aviv",        "short": "MTA","color": "#FFF200", "score": 76},
    },
    "realmadrid_barcelona_euro_f": {
        "sport": "🏀 Basket", "competition": "Euroleague",
        "date": D_P5, "time": "21:00", "stadium": "WiZink Center, Madrid", "status": "À venir",
        "home": {"name": "Real Madrid Baloncesto",  "short": "RMA","color": "#FEBE10", "score": None},
        "away": {"name": "FC Barcelona Bàsquet",    "short": "BAR","color": "#A50044", "score": None},
    },
    # ── Betclic Elite ─────────────────────────────────────────────────────────
    "asvel_monaco_bet": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_M10, "time": "20:30", "stadium": "Astroballe, Villeurbanne", "status": "Terminé",
        "home": {"name": "LDLC ASVEL",     "short": "ASV","color": "#003a70", "score": 82},
        "away": {"name": "AS Monaco Basket","short": "MCO","color": "#B5121B", "score": 75},
    },
    "paris_strasbourg_bet": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_M7, "time": "20:00", "stadium": "Accor Arena, Paris", "status": "Terminé",
        "home": {"name": "Paris Basketball","short": "PAB","color": "#1A1A1A", "score": 85},
        "away": {"name": "SIG Strasbourg",  "short": "SIG","color": "#003C8F", "score": 79},
    },
    "dijon_asvel_bet": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_M4, "time": "19:00", "stadium": "Palais des Sports, Dijon", "status": "Terminé",
        "home": {"name": "JDA Dijon",  "short": "JDA","color": "#8B0000", "score": 71},
        "away": {"name": "LDLC ASVEL", "short": "ASV","color": "#003a70", "score": 88},
    },
    "levallois_nanterre_bet": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_M2, "time": "20:30", "stadium": "Palais des Sports Marcel Cerdan, Levallois", "status": "Terminé",
        "home": {"name": "Boulogne-Levallois Metropolitans 92","short": "MET","color": "#003F87", "score": 88},
        "away": {"name": "JSF Nanterre",                       "short": "NAN","color": "#CC0000", "score": 92},
    },
    "monaco_lemans_bet": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_P4, "time": "20:00", "stadium": "Salle Gaston Médecin, Monaco", "status": "À venir",
        "home": {"name": "AS Monaco Basket","short": "MCO","color": "#B5121B", "score": None},
        "away": {"name": "Le Mans Sarthe Basket","short": "MSB","color": "#E30613", "score": None},
    },
    # ── Top 14 ────────────────────────────────────────────────────────────────
    "toulouse_larochelle_top14": {
        "sport": "🏉 Rugby", "competition": "Top 14",
        "date": D_M12, "time": "21:05", "stadium": "Stadium de Toulouse", "status": "Terminé",
        "home": {"name": "Stade Toulousain", "short": "ST",  "color": "#B60000", "score": 28},
        "away": {"name": "Stade Rochelais",  "short": "SR",  "color": "#FCD000", "score": 18},
    },
    "racing_clermont_top14": {
        "sport": "🏉 Rugby", "competition": "Top 14",
        "date": D_M9, "time": "16:05", "stadium": "La Défense Arena, Nanterre", "status": "Terminé",
        "home": {"name": "Racing 92",          "short": "R92", "color": "#0099CC", "score": 22},
        "away": {"name": "Clermont Auvergne",   "short": "ASM", "color": "#003189", "score": 19},
    },
    "lyon_bordeaux_top14": {
        "sport": "🏉 Rugby", "competition": "Top 14",
        "date": D_M7, "time": "14:30", "stadium": "Matmut Stadium, Lyon", "status": "Terminé",
        "home": {"name": "Lyon OU",           "short": "LOU", "color": "#0057A8", "score": 17},
        "away": {"name": "Bordeaux-Bègles",   "short": "UBB", "color": "#001F5B", "score": 23},
    },
    "montpellier_stadefrancais_top14": {
        "sport": "🏉 Rugby", "competition": "Top 14",
        "date": D_M4, "time": "16:05", "stadium": "GGL Stadium, Montpellier", "status": "Terminé",
        "home": {"name": "Montpellier Hérault Rugby","short": "MHR","color": "#012169", "score": 25},
        "away": {"name": "Stade Français Paris",     "short": "SF", "color": "#E1002B", "score": 12},
    },
    "bayonne_castres_top14": {
        "sport": "🏉 Rugby", "competition": "Top 14",
        "date": D_M2, "time": "17:30", "stadium": "Stade Jean-Dauger, Bayonne", "status": "Terminé",
        "home": {"name": "Aviron Bayonnais", "short": "AB",  "color": "#0066CC", "score": 20},
        "away": {"name": "Castres Olympique","short": "CO",  "color": "#0033A0", "score": 13},
    },
    "toulouse_racing2_top14": {
        "sport": "🏉 Rugby", "competition": "Top 14",
        "date": D_P3, "time": "21:05", "stadium": "Stadium de Toulouse", "status": "À venir",
        "home": {"name": "Stade Toulousain", "short": "ST",  "color": "#B60000", "score": None},
        "away": {"name": "Racing 92",         "short": "R92", "color": "#0099CC", "score": None},
    },
    "larochelle_lyon2_top14": {
        "sport": "🏉 Rugby", "competition": "Top 14",
        "date": D_P6, "time": "16:05", "stadium": "Stade Marcel Deflandre, La Rochelle", "status": "À venir",
        "home": {"name": "Stade Rochelais", "short": "SR",  "color": "#FCD000", "score": None},
        "away": {"name": "Lyon OU",          "short": "LOU", "color": "#0057A8", "score": None},
    },
    # ── La Liga ──────────────────────────────────────────────────────────────────
    "real_barca_laliga_j11": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": "2025-10-25", "time": "16:00", "stadium": "Santiago Bernabéu, Madrid", "status": "Terminé",
        "home": {"name": "Real Madrid CF", "short": "RMA", "color": "#FEBE10", "score": 2},
        "away": {"name": "FC Barcelona",   "short": "BAR", "color": "#A50044", "score": 1},
    },
    "atletico_real_laliga_j15": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": "2025-11-30", "time": "18:30", "stadium": "Cívitas Metropolitano, Madrid", "status": "Terminé",
        "home": {"name": "Atlético de Madrid", "short": "ATM", "color": "#CC2222", "score": 1},
        "away": {"name": "Real Madrid CF",     "short": "RMA", "color": "#FEBE10", "score": 1},
    },
    "barca_sevilla_laliga_j8": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": "2025-10-04", "time": "16:00", "stadium": "Estadi Olímpic Lluís Companys, Barcelone", "status": "Terminé",
        "home": {"name": "FC Barcelona", "short": "BAR", "color": "#A50044", "score": 3},
        "away": {"name": "Sevilla FC",   "short": "SEV", "color": "#CC0000", "score": 0},
    },
    "sevilla_betis_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": "2025-11-08", "time": "21:00", "stadium": "Estadio Ramón Sánchez-Pizjuán, Séville", "status": "Terminé",
        "home": {"name": "Sevilla FC",  "short": "SEV", "color": "#CC0000", "score": 0},
        "away": {"name": "Real Betis",  "short": "BET", "color": "#00833E", "score": 1},
    },
    "athletic_sociedad_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": "2026-02-01", "time": "16:15", "stadium": "San Mamés, Bilbao", "status": "Terminé",
        "home": {"name": "Athletic Club",  "short": "ATH", "color": "#CC0000", "score": 2},
        "away": {"name": "Real Sociedad",  "short": "RSO", "color": "#0047AB", "score": 0},
    },
    "barca_atletico_laliga_j26": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": "2026-03-07", "time": "21:00", "stadium": "Estadi Olímpic Lluís Companys, Barcelone", "status": "Terminé",
        "home": {"name": "FC Barcelona",       "short": "BAR", "color": "#A50044", "score": 2},
        "away": {"name": "Atlético de Madrid",  "short": "ATM", "color": "#CC2222", "score": 1},
    },
    "barca_real_laliga_j33": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": "2026-04-19", "time": "16:00", "stadium": "Estadi Olímpic Lluís Companys, Barcelone", "status": "Terminé",
        "home": {"name": "FC Barcelona",   "short": "BAR", "color": "#A50044", "score": 2},
        "away": {"name": "Real Madrid CF", "short": "RMA", "color": "#FEBE10", "score": 1},
    },
    "real_villarreal_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": D_M7, "time": "21:00", "stadium": "Santiago Bernabéu, Madrid", "status": "Terminé",
        "home": {"name": "Real Madrid CF",  "short": "RMA", "color": "#FEBE10", "score": 2},
        "away": {"name": "Villarreal CF",   "short": "VIL", "color": "#FFD700", "score": 0},
    },
    "atletico_valencia_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": D_M5, "time": "18:30", "stadium": "Cívitas Metropolitano, Madrid", "status": "Terminé",
        "home": {"name": "Atlético de Madrid", "short": "ATM", "color": "#CC2222", "score": 1},
        "away": {"name": "Valencia CF",        "short": "VCF", "color": "#FF7F00", "score": 0},
    },
    "barca_athletic_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": D_M3, "time": "21:00", "stadium": "Estadi Olímpic Lluís Companys, Barcelone", "status": "Terminé",
        "home": {"name": "FC Barcelona",  "short": "BAR", "color": "#A50044", "score": 3},
        "away": {"name": "Athletic Club", "short": "ATH", "color": "#CC0000", "score": 1},
    },
    "girona_rayo_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": D_M2, "time": "14:00", "stadium": "Estadi Municipal de Montilivi, Gérone", "status": "Terminé",
        "home": {"name": "Girona FC",       "short": "GIR", "color": "#CC0000", "score": 2},
        "away": {"name": "Rayo Vallecano",  "short": "RVA", "color": "#CC0000", "score": 2},
    },
    "real_celta_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": D_P4, "time": "21:00", "stadium": "Santiago Bernabéu, Madrid", "status": "À venir",
        "home": {"name": "Real Madrid CF", "short": "RMA", "color": "#FEBE10", "score": None},
        "away": {"name": "Celta Vigo",     "short": "CEL", "color": "#87CEEB", "score": None},
    },
    "barca_osasuna_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": D_P5, "time": "18:30", "stadium": "Estadi Olímpic Lluís Companys, Barcelone", "status": "À venir",
        "home": {"name": "FC Barcelona", "short": "BAR", "color": "#A50044", "score": None},
        "away": {"name": "CA Osasuna",   "short": "OSA", "color": "#D2233E", "score": None},
    },
    "atletico_mallorca_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": D_P6, "time": "16:00", "stadium": "Cívitas Metropolitano, Madrid", "status": "À venir",
        "home": {"name": "Atlético de Madrid", "short": "ATM", "color": "#CC2222", "score": None},
        "away": {"name": "RCD Mallorca",       "short": "MAL", "color": "#B22234", "score": None},
    },
    "betis_sociedad_laliga": {
        "sport": "⚽ Football", "competition": "La Liga",
        "date": D_P7, "time": "14:00", "stadium": "Estadio Benito Villamarín, Séville", "status": "À venir",
        "home": {"name": "Real Betis",   "short": "BET", "color": "#00833E", "score": None},
        "away": {"name": "Real Sociedad","short": "RSO", "color": "#0047AB", "score": None},
    },
}

# ── Analyses détaillées (données réelles) ─────────────────────────────────────
ANALYSIS = {
    "psg_monaco_l1": {
        "tactique": {
            "home_form": "4-3-3",
            "away_form": "4-2-3-1",
            "home_style": "Pressing haut collectif, possession dominante, combinaisons Hakimi–Dembélé côté droit",
            "away_style": "Bloc médian compact, sorties en contre sur Embolo, Ben Seghir libre entre les lignes",
            "home_players": [
                ["Donnarumma","GB"],["Hakimi","RD"],["Marquinhos","DC"],
                ["Pacho","DC"],["Nuno Mendes","LD"],
                ["Fabian Ruiz","MC"],["Vitinha","MC"],["João Neves","MC"],
                ["Dembélé","AD"],["Barcola","AG"],["G. Ramos","BU"],
            ],
            "away_players": [
                ["Majecki","GB"],["Vanderson","RD"],["Salisu","DC"],
                ["Maripan","DC"],["Caio Henrique","LD"],
                ["Camara","MDC"],["Zakaria","MDC"],
                ["Ben Seghir","MO"],["Akliouche","MO"],["Golovin","MO"],
                ["Embolo","BU"],
            ],
            "phases": {
                "Pressing": "Ce n'était pas du pressing — c'était du harcèlement systématisé. João Neves a coupé la ligne de passe verticale de Zakaria 14 fois en première période. Monaco ne pouvait physiquement pas jouer. Quand ton milieu défensif ne reçoit jamais le ballon dans les pieds dans son propre camp, ta structure de jeu s'effondre. C'est exactement ce qui s'est passé à la 31' : Neves récupère sur une relance monégasque ratée, Dembélé part dans le dos de Salisu, Ramos conclut, 1-0. Le pressing n'est pas une question d'intensité — c'est une question de lignes de passe coupées. PSG a maîtrisé ça parfaitement.",
                "Transitions": "Hakimi–Dembélé sur le côté droit : c'est le couloir le plus dangereux d'Europe en ce moment. Trois fois en première période, Monaco a tenté de sortir par la gauche, trois fois ils se sont retrouvés en infériorité numérique. Le problème de Monaco n'était pas défensif — c'était leur incapacité à fixer les latéraux parisiens avec leurs ailiers. Golovin n'a jamais rentré dans son couloir pour aider Caio Henrique. C'est ça la vraie erreur tactique de ce soir.",
                "Phases arrêtées": "Le corner à angle court sur le 2e but est un chef-d'œuvre de préparation. PSG a travaillé ça toute la semaine. Barcola sert Fabian Ruiz qui décale Dembélé — Monaco ne l'a pas vu venir. En tant que coach, quand tu vois une séquence préparée adverse se répéter, tu dois adapter ta défense de corner immédiatement. Monaco ne l'a pas fait.",
                "Bloc défensif": "Monaco a essayé le bloc bas en deuxième mi-temps, mais un bloc bas ne fonctionne que si tu as la capacité de repartir vite en contre. Avec Embolo seul en pointe, coupé de tout soutien, c'était mission impossible. J'ai compté 5 récupérations de Monaco en seconde période — dont aucune n'a débouché sur une situation offensive. Un bloc bas sans contre-attaque, ce n'est pas une tactique, c'est de la survie.",
            },
            "home_stats": {"Possession": (66, 34), "Tirs": (16, 7), "Tirs cadrés": (7, 2), "Passes (%)": (89, 72), "Fautes": (10, 15)},
        },
        "joueurs": {
            "home": [
                {"nom": "Dembélé",    "poste": "AD", "note": 9.0, "stats": "1 PD, 1 but, 5 dribbles"},
                {"nom": "João Neves", "poste": "MC", "note": 8.6, "stats": "91 ballons, 14 récup. clés"},
                {"nom": "Hakimi",     "poste": "RD", "note": 8.3, "stats": "2 PD, 7 centres, pressing parfait"},
                {"nom": "G. Ramos",   "poste": "BU", "note": 8.0, "stats": "1 but, 4 tirs, pivot offensif"},
                {"nom": "Barcola",    "poste": "AG", "note": 7.8, "stats": "1 but, 4 dribbles, côté gauche dominant"},
                {"nom": "Marquinhos", "poste": "DC", "note": 7.6, "stats": "93% passes, 5 dégagements, capitaine exemplaire"},
                {"nom": "Fabian Ruiz","poste": "MC", "note": 7.4, "stats": "84 ballons, 3 récup., jeu de qualité"},
            ],
            "away": [
                {"nom": "Ben Seghir",     "poste": "MO",  "note": 7.1, "stats": "Seul danger monégasque, 3 tirs"},
                {"nom": "Majecki",        "poste": "GB",  "note": 6.9, "stats": "5 arrêts, impuissant sur les buts"},
                {"nom": "Akliouche",      "poste": "MO",  "note": 6.4, "stats": "Effacé par le pressing parisien"},
                {"nom": "Caio Henrique",  "poste": "LD",  "note": 6.2, "stats": "Débordé par Dembélé, 2 fautes"},
                {"nom": "Camara",         "poste": "MDC", "note": 6.0, "stats": "Récupérations limitées, pas dans le jeu"},
                {"nom": "Embolo",         "poste": "BU",  "note": 5.7, "stats": "Isolé, 1 tir, 3 duels perdus"},
            ],
        },
        "bilan": {
            "home_forts": [
                "João Neves en sentinelle absolue : 14 coupures de lignes de passe en première période — Monaco ne pouvait pas construire quoi que ce soit dans l'axe",
                "Couloir droit Hakimi–Dembélé : 7 combinaisons, 3 situations de tir créées, 2 buts impliqués — le duo le plus complémentaire de Ligue 1",
                "Solidité défensive : Monaco n'a cadré que 2 tirs sur tout le match malgré 35% de possession — bloc haut ET bloc bas parfaitement gérés",
            ],
            "home_faibles": [
                "3 pertes de balle dans la zone de pressing adverse entre la 55' et la 65' — contre un adversaire plus ambitieux, ces ballons perdus auraient coûté cher",
                "Ligne défensive trop haute à la 58' : Pacho s'est retrouvé à 35m de son but, laissant un espace exploitable dans son dos — heureusement Monaco manquait de la qualité pour l'exploiter",
            ],
            "away_forts": [
                "Bloc 4-4-2 discipliné pendant les 40 premières minutes — Monaco a tenu sans jamais rompre jusqu'à la 31'",
                "Ben Seghir : seul joueur capable de trouver les espaces entre les lignes parisiennes, son impact illustre ce qu'aurait dû faire toute l'équipe",
            ],
            "away_faibles": [
                "Zakaria fantôme : 29 touches en 90 minutes pour un milieu défensif censé être le pivot du jeu — c'est la signature d'un pressing adverse qui fonctionne à 100%",
                "Zéro jeu dans la profondeur : Monaco n'a tenté que 3 passes dans le dos des défenseurs parisiens — comment mettre sous pression une défense qui ne défend jamais reculée ?",
                "Embolo sacrifié en souffrance totale : 11 duels, 3 gagnés — sans combinaisons, sans soutien, un avant-centre seul ne peut rien. C'est l'erreur tactique principale de ce soir",
            ],
        },
        "verdict": {
            "home_perf": 8.8, "away_perf": 5.8,
            "intensite": 7.4, "spectacle": 7.6,
            "home_txt": "J'ai rarement vu un pressing aussi bien structuré en Ligue 1 cette saison. Luis Enrique a construit quelque chose de rare : une équipe qui court autant sans ballon qu'avec. João Neves est le cerveau caché de ce système — quand il est dans ce niveau-là, PSG est imbattable en France. Ce qui m'impressionne, c'est la cohérence collective : aucun joueur ne décide seul, chaque déplacement est une réponse au déplacement d'un coéquipier.",
            "away_txt": "Monaco a le talent pour faire mieux. Beaucoup mieux. La vraie question ce soir, c'est : pourquoi n'a-t-on pas osé jouer ? Avec Ben Seghir, Akliouche, Golovin — des joueurs capables de déstabiliser n'importe quelle défense en un contre un. Les garder dans un bloc bas pendant 70 minutes, c'est du gâchis pur. Je ne comprends pas la peur tactique de ce soir.",
            "coach_home": "✅ Plan de jeu rigoureux, parfaitement exécuté. La décision de faire jouer João Neves comme sentinelle plutôt que Fabian Ruiz a été la clé tactique du match — et Luis Enrique l'a vu avant les autres.",
            "coach_away": "❌ Erreur stratégique majeure. À 0-1 à la 55', il fallait passer en 4-3-3 offensif avec Golovin libre dans l'axe et Ben Seghir comme pivot de jeu. Rester en bloc bas dans ces conditions, c'est abandonner le match.",
        },
    },

    "arsenal_mancity_pl": {
        "tactique": {
            "home_form": "4-3-3",
            "away_form": "4-2-3-1",
            "home_style": "Pressing collectif intense, Rice en sentinelle, Havertz en faux 9, Saka en arme principale côté droit",
            "away_style": "Possession élaborée, Haaland en pivot offensif, De Bruyne en créateur entre les lignes",
            "home_players": [
                ["Raya","GB"],["Ben White","RD"],["Saliba","DC"],
                ["Gabriel","DC"],["Calafiori","LD"],
                ["Rice","MDC"],["Ødegaard","MC"],["Merino","MC"],
                ["Saka","AD"],["Havertz","BU"],["Martinelli","AG"],
            ],
            "away_players": [
                ["Ederson","GB"],["Walker","RD"],["Akanji","DC"],
                ["Dias","DC"],["Gvardiol","LD"],
                ["Kovacic","MDC"],["Nunes","MDC"],
                ["Foden","MO"],["De Bruyne","MO"],["Doku","MO"],
                ["Haaland","BU"],
            ],
            "phases": {
                "Pressing": "Arsenal a produit son pressing le plus intense de la saison ce soir. À la 12', une récupération haute de Rice directement transformée en but de Saka — le pressing n'était pas du harcèlement, c'était du football de haut niveau. Man City a été déstabilisé pendant 30 minutes, ne trouvant jamais les démarquages dans l'axe face à la pression des trois milieux d'Arsenal. Mais passé la 35', Guardiola a demandé à jouer plus long — et Haaland a commencé à menacer.",
                "Transitions": "Les transitions de City sur les récupérations de Rodri — pardon, de Kovacic — ont été tranchantes en deuxième période. Doku à gauche avec sa vitesse a posé des problèmes structurels à Ben White qui n'est pas le latéral le plus à l'aise défensivement dans ces situations. Le 2-1 de Haaland à la 67' est né directement d'une transition rapide après une perte de balle d'Havertz dans son camp.",
                "Phases arrêtées": "Arsenal a obtenu 7 corners, dont 3 dangereux — le 2-2 de Saka est issu d'une combinaison courte corner préparée avec Martinelli. À l'inverse, City n'a pas eu de corner dangereux direct mais ses coups francs hauts ont systématiquement créé du désordre défensif dans la surface d'Arsenal.",
                "Bloc défensif": "Dans les 15 dernières minutes, avec 2-2, les deux équipes ont choisi la gestion plutôt que l'ambition. Arsenal en 4-4-2 bas, City en possession sans prise de risque. Un 2-2 qui arrangera plus les Citizens que les Gunners dans la course au titre.",
            },
            "home_stats": {"Possession": (45, 55), "Tirs": (14, 18), "Tirs cadrés": (6, 7), "Passes (%)": (84, 91), "Fautes": (14, 11)},
        },
        "joueurs": {
            "home": [
                {"nom": "Saka",       "poste": "AD",  "note": 8.6, "stats": "2 buts, 7 dribbles, 4 tirs"},
                {"nom": "Rice",       "poste": "MDC", "note": 8.1, "stats": "97 ballons, 6 récupérations, pressing constant"},
                {"nom": "Saliba",     "poste": "DC",  "note": 8.2, "stats": "Duel Haaland : 5/7 gagnés, impressionnant"},
                {"nom": "Ødegaard",   "poste": "MC",  "note": 7.9, "stats": "73 ballons, 3 key passes, menacé par City"},
                {"nom": "Havertz",    "poste": "BU",  "note": 7.5, "stats": "Faux 9, 3 récup. offensives, 2 tirs"},
                {"nom": "Martinelli", "poste": "AG",  "note": 7.3, "stats": "1 PD, 4 dribbles, pression constante"},
                {"nom": "Merino",     "poste": "MC",  "note": 7.0, "stats": "Pressing constant, 4 récupérations, solide"},
            ],
            "away": [
                {"nom": "Haaland",    "poste": "BU", "note": 8.9, "stats": "2 buts, 5 tirs, monster match"},
                {"nom": "De Bruyne",  "poste": "MO", "note": 8.4, "stats": "1 PD, 82 ballons, vision de jeu"},
                {"nom": "Foden",      "poste": "MO", "note": 8.1, "stats": "Créativité permanente, 1 PD"},
                {"nom": "Gvardiol",   "poste": "LD", "note": 8.0, "stats": "Intraitable défensivement, propulsion offensive"},
                {"nom": "Doku",       "poste": "MO", "note": 7.6, "stats": "Vitesse dévastatrice, 1 PD, 5 dribbles"},
                {"nom": "Dias",       "poste": "DC", "note": 7.9, "stats": "Leader défensif, 91% passes"},
                {"nom": "Ederson",    "poste": "GB", "note": 7.8, "stats": "4 arrêts, maître de la relance courte"},
            ],
        },
        "bilan": {
            "home_forts": [
                "Pressing d'Arsenal en première période : 45 minutes à un niveau que peu d'équipes peuvent produire contre Man City — Man City n'a créé aucune occasion avant la 35'",
                "Saka dans un état de grâce absolue : 2 buts, 7 dribbles, un joueur qui a dicté le rythme offensif d'Arsenal à lui seul dans les moments importants",
                "Saliba contre Haaland : 5 duels gagnés sur 7, le Français n'a jamais lâché le Norvégien. Un duel de titans remporté par Arsenal",
            ],
            "home_faibles": [
                "55% de possession concédée à City — Arsenal subit structurellement quand il ne peut pas presser haut. La 2e période a montré les limites du plan de jeu face à une équipe aussi technique",
                "Havertz en faux 9 a bien pressé mais manqué de présence dans la surface — sur les corners et phases arrêtées, l'absence d'un vrai attaquant de pointe s'est fait sentir",
            ],
            "away_forts": [
                "Haaland intraitable dans la surface : 2 buts sur 5 tentatives — son efficacité en zone de finition reste la plus haute d'Europe toutes compétitions confondues",
                "De Bruyne–Foden–Doku : trio offensif qui a posé des problèmes insolubles à Arsenal dès que City a trouvé ses automatismes en 2e mi-temps",
            ],
            "away_faibles": [
                "30 premières minutes catastrophiques face au pressing d'Arsenal : City n'a pas trouvé de solution pour casser les lignes adverses, perdant 11 ballons dans leur propre camp",
                "Trop de possession stérile dans les 20 dernières minutes — City avait les ressources pour tenter de prendre les 3 points et n'a pas osé",
            ],
        },
        "verdict": {
            "home_perf": 7.8, "away_perf": 7.9,
            "intensite": 9.1, "spectacle": 9.2,
            "home_txt": "Arsenal a montré qu'il peut tenir tête à Man City — et même le dépasser par moments. Le problème, c'est que City a des réponses à tout. Quand Arsenal presse haut, City passe par-dessus. Ce 2-2 est le reflet exact du rapport de forces entre les deux meilleures équipes d'Angleterre. Ce qui me préoccupe pour Arsenal, c'est qu'ils n'ont pas de plan B quand le pressing ne fonctionne plus.",
            "away_txt": "Man City a eu l'avantage sur la presque totalité du match en termes de possession et de qualité technique. Mais 2-2 à l'Emirates, ce n'est pas une mauvaise affaire. Ce résultat laisse les deux équipes sur pied d'égalité et ouvre une course au titre absolument passionnante. Haaland était inarrêtable — encore.",
            "coach_home": "✅ Arteta a osé presser Haaland haut 30 minutes — et ça a fonctionné. Le choix de Havertz en faux 9 avec Merino comme box-to-box a libéré Ødegaard plus haut. Repasser en 4-2-3-1 avec Trossard entrant à la 72' pour sécuriser le point était la bonne décision dans ces circonstances.",
            "coach_away": "⚠️ Guardiola a bien géré sa possession mais le pressing arsenalien a clairement gêné ses latéraux en première mi-temps. Ce que je questionne, c'est l'absence de Bernardo Silva dans l'axe pour contrebalancer le pressing d'Arsenal — Kovacic a manqué de qualité dans les sorties de balle sous pression. Et avec Rodri absent sur blessure, l'équilibre défensif de City était fragile.",
        },
    },

    "lakers_warriors_nba": {
        "tactique": {
            "home_form": "Positionnel",
            "away_form": "Motion Offense",
            "home_style": "Jeu de poste bas d'AD, isolation LeBron côté gauche, pick & roll tardifs",
            "away_style": "Circulation de balle rapide, P&R Curry–Wiggins, tirs à 3pts en catch-and-shoot",
            "home_players": [
                ["LeBron James","SF"],["A. Davis","C"],["Austin Reaves","SG"],
                ["Rui Hachimura","PF"],["Dalton Knecht","SG"],
            ],
            "away_players": [
                ["S. Curry","PG"],["Buddy Hield","SG"],["A. Wiggins","SF"],
                ["Draymond Green","PF"],["K. Looney","C"],
            ],
            "phases": {
                "Pick & Roll": "La clé de ce match, c'est ce que les Lakers ont fait défensivement sur le P&R de Curry. Au lieu du drop coverage habituel, Redick a demandé un hedge agressif avec Hachimura qui sort haut sur Curry dès la prise d'écran. Résultat : Curry à 3/9 sur P&R, 6 turnovers. Quand tu enlèves le P&R à Curry, tu enlèves 40% du système offensif des Warriors. Côté Lakers, le P&R Davis–Reaves a fonctionné parce que Looney n'a jamais su choisir : couvrir le roll ou le pop ? Davis a marqué 14 points sur cette seule action.",
                "Fast Break": "Les Warriors ont généré 18 points en transition en première mi-temps — et ça aurait pu être 30 si les Lakers n'avaient pas ajusté leur retour défensif à la pause. LeBron a personnellement décidé de sprinter sur chaque transition en 3e quart. Quand le meilleur joueur de ton équipe montre l'exemple défensivement, les autres suivent. En 2e mi-temps, Golden State n'a marqué que 5 points en contre.",
                "Isolation": "LeBron en isolation côté gauche contre Klay Thompson : c'est une asymétrie que Redick a exploitée à dessein. Thompson à 34 ans n'a plus les jambes pour défendre 4 quarts en premier rideau. LeBron l'a su et l'a abusé à 5 reprises pour provoquer des fautes ou créer des décalages.",
                "Clutch Time": "Le run 8-0 à 4 minutes de la fin, c'est le moment où on voit la différence entre une équipe qui a appris à gagner et une qui cherche encore comment le faire. Davis en post bas sur Looney, LeBron en drive, Reaves qui plante le 3pts de l'écart définitif — trois actions différentes, trois joueurs, un seul objectif. Warriors : Curry sur fautes à 4'30, et Hield incapable de créer son propre tir en isolation — le vide offensif sans Curry a été immense.",
            },
            "home_stats": {"Tirs 3pts": (12, 9), "Rebonds": (48, 40), "Passes dec.": (28, 22), "Interceptions": (9, 6), "Fautes": (19, 22)},
        },
        "joueurs": {
            "home": [
                {"nom": "A. Davis",       "poste": "C",  "note": 9.3, "stats": "32 pts, 14 reb, 3 blk"},
                {"nom": "LeBron James",   "poste": "SF", "note": 8.8, "stats": "27 pts, 9 ast, 6 reb"},
                {"nom": "Austin Reaves",  "poste": "SG", "note": 7.9, "stats": "18 pts, 4/7 à 3pts"},
                {"nom": "Rui Hachimura",  "poste": "PF", "note": 6.8, "stats": "9 pts, 5 reb"},
                {"nom": "D. Knecht",      "poste": "SG", "note": 6.5, "stats": "8 pts, 2/4 à 3pts, défense active"},
            ],
            "away": [
                {"nom": "S. Curry",        "poste": "PG", "note": 8.1, "stats": "26 pts mais 6 TOs"},
                {"nom": "A. Wiggins",      "poste": "SF", "note": 7.4, "stats": "21 pts, 7 reb"},
                {"nom": "Draymond Green",  "poste": "PF", "note": 6.8, "stats": "5 pts, 11 ast, 6 reb"},
                {"nom": "Buddy Hield",     "poste": "SG", "note": 6.5, "stats": "15 pts, 4/9 à 3pts"},
                {"nom": "K. Looney",       "poste": "C",  "note": 5.9, "stats": "Dominé par Davis"},
            ],
        },
        "bilan": {
            "home_forts": [
                "AD en mode dominant absolu : 32 pts / 14 reb sur Looney — une incompatibilité physique que Kerr n'a jamais corrigée malgré 4 quarts de domination",
                "Ajustement défensif sur Curry à la mi-temps : passer du drop au hedge agressif a cassé le rythme des Warriors. Redick a lu le match en temps réel",
                "Reaves en décideur : 18 pts et 4/7 à 3pts — les Warriors ne l'ont jamais identifié comme menace prioritaire. Knecht en soutien sur les rotations défensives : excellent dans son rôle.",
            ],
            "home_faibles": [
                "19 fautes en 48 minutes, dont 4 pour Davis en 3e quart — Kerr aurait pu mieux jouer les possessions hautes pour forcer Davis à la 6e faute",
                "1er quart à -9 : la défense était trop molle sur les catch-and-shoot Warriors. Si Golden State avait maintenu ce rythme, le match était plié",
            ],
            "away_forts": [
                "53 points en 1ère mi-temps avec une circulation de balle fluide — le Motion Offense Warriors fonctionne quand Curry est propre balle en main",
                "Wiggins : meilleur Warriors cette nuit, 21 pts en jouant sans ballon. Le seul à avoir compris que les Lakers défendaient le ballon, pas les mouvements",
            ],
            "away_faibles": [
                "Curry : 6 turnovers — sa pire nuit offensive de la saison. À chaque fois qu'il était pressé sur P&R, il choisissait la mauvaise option",
                "Hield : 4/9 à 3pts est une performance honnête mais insuffisante pour remplacer la dimension terrorisante de Klay en clutch",
                "Looney contre Davis : -8 en rebonds, -14 en +/-. Cette incompatibilité devait être gérée avec Kuminga en pivot dès le 2e quart",
            ],
        },
        "verdict": {
            "home_perf": 8.9, "away_perf": 6.4,
            "intensite": 8.2, "spectacle": 8.6,
            "home_txt": "Ce que Redick a construit cette nuit, c'est une leçon de lecture de jeu en temps réel. Identifier la faiblesse Looney–Davis, sur-exploiter le match-up Klay–LeBron, mettre Reaves en position de décideur face à une défense qui l'ignorait — c'est du coaching de haut niveau. Davis était inarrêtable, mais c'est Redick qui a créé les conditions pour qu'il le soit.",
            "away_txt": "Kerr a perdu ce match dans son vestiaire à la mi-temps. Il avait toutes les informations pour switcher son plan défensif sur Davis et remettre Kuminga pour aider Looney. Il n'a rien fait. Dans les grandes confrontations, l'inaction d'un coach est une décision en soi — et ce soir elle a coûté la victoire à Golden State. La transition post-Klay avec Hield s'est révélée insuffisante dans les moments de vérité.",
            "coach_home": "✅ Ajustement défensif sur Curry en 2e mi-temps : parfait. Décision de laisser Davis en post bas malgré ses 4 fautes plutôt que de le placer en bench : le bon risque calculé. Et Redick a su utiliser Knecht au bon moment pour maintenir la pression défensive sur les ailes.",
            "coach_away": "❌ Kerr n'a pas su adapter sa rotation intérieure face à la domination de Davis. Kuminga aurait changé complètement la dynamique de la peinture — 4 quarts de Looney face à Davis, c'est un choix tactique qu'aucune donnée ne justifiait.",
        },
    },

    "toulouse_larochelle_top14": {
        "tactique": {
            "home_form": "XV de départ",
            "away_form": "Attaque des espaces",
            "home_style": "Jeu au pied chirurgical de Dupont, maul offensif dominant, backs rapides et techniques",
            "away_style": "Pack physique dominant en touche, jeu à la main rapide sur la largeur, Alldritt en axe",
            "home_players": [
                ["Dupont","DM"],["Ntamack","DO"],["T. Ramos","FB"],
                ["Mauvaka","TL"],["Meafou","2e L."],["Cros","F"],
                ["Aldegheri","PI"],["Lebel","AI"],["Capuozzo","AI"],
            ],
            "away_players": [
                ["Hastoy","DO"],["Kerr-Barlow","DM"],["Dulin","FB"],
                ["Retière","AI"],["Alldritt","N°8"],["Skelton","TL"],
                ["Priso","PI"],["Danty","CE"],["Dillane","2e L."],
            ],
            "phases": {
                "Mêlée & Conquête": "Toulouse a dominé cette phase statique à 5/6 en mêlée — une supériorité qui a offert des plateformes de jeu idéales. Mauvaka sur ses lancers en touche : 9/10, une statistique qui illustre à quel point la conquête toulousaine était dominante. C'est un fait rarement dit : quand tu gagnes 90% de tes lancers en touche, tu joues avec 15% de possessions supplémentaires par rapport à l'adversaire. Toulouse a utilisé cette supériorité avec intelligence.",
                "Jeu au pied": "Dupont : 8 jeux au pied, 6 trouvant le coin ou les 22 mètres adverses. Thomas Ramos : 3/3 pénalités, un pied chirurgical. Mais ce qui m'a le plus impressionné, c'est l'intelligence dans les choix — Dupont ne joue jamais au pied par défaut, il joue au pied pour créer un déséquilibre précis. Quand il a vu que La Rochelle reculait sa ligne de fond, il a immédiatement exploité cet espace avec des jeux tendus à raser le sol.",
                "Attaque en mouvement": "Les backs toulousains ont créé 4 situations d'essai, en convertissant 3. Capuozzo sur l'essai de 58m à la 61' : une inspiration pure. Lebel sur le côté droit : imperméable défensivement, tranchant offensivement. La qualité athlétique de ces backs, combinée à la domination du pack, crée un déséquilibre structurel que peu d'équipes au monde peuvent gérer.",
                "Défense en rideau": "La Rochelle a cédé à la 61' sur un contre-ruck parfaitement organisé par Cros. Ce moment illustre la supériorité technique de Toulouse dans cette phase : Cros a gagné le ballon sur une défense qui pensait avoir sécurisé sa possession. La discipline défensive toulousaine en fin de match — sans prendre de pénalité inutile malgré la pression — est la marque d'une équipe championne.",
            },
            "home_stats": {"Possession": (58, 42), "Plaquages": (95, 87), "Pénalités cédées": (9, 12), "Mètres parcourus": (480, 390), "Turnovers": (6, 8)},
        },
        "joueurs": {
            "home": [
                {"nom": "Antoine Dupont",  "poste": "DM",   "note": 9.2, "stats": "8 jeux au pied, 6 au coin, impact total"},
                {"nom": "Peato Mauvaka",   "poste": "TL",   "note": 8.6, "stats": "9/10 touche, 11 plaquages, maîtrise"},
                {"nom": "Romain Ntamack",  "poste": "DO",   "note": 8.4, "stats": "1 essai, 2 transf., 73% passes"},
                {"nom": "Ange Capuozzo",   "poste": "AI",   "note": 8.3, "stats": "1 essai (58m!), 4 défenses"},
                {"nom": "Emmanuel Meafou", "poste": "2e L.", "note": 8.0, "stats": "7 ballons de touche, domination"},
                {"nom": "François Cros",   "poste": "F",    "note": 7.8, "stats": "1 grattage clé, 12 plaquages"},
                {"nom": "Thomas Ramos",    "poste": "FB",   "note": 8.1, "stats": "3/3 pénalités, jeu territorial"},
            ],
            "away": [
                {"nom": "Gregory Alldritt",  "poste": "N°8",  "note": 8.5, "stats": "Colossal : 14 plaquages, 2 ballons portés"},
                {"nom": "Will Skelton",      "poste": "2e L.", "note": 8.1, "stats": "8 ballons de touche, 11 plaquages"},
                {"nom": "Antoine Hastoy",    "poste": "DO",   "note": 7.6, "stats": "1 essai, 2 pénalités, créatif"},
                {"nom": "Arthur Retière",    "poste": "AI",   "note": 7.4, "stats": "1 essai, 3 défenses, combatif"},
                {"nom": "Brice Dulin",       "poste": "FB",   "note": 7.2, "stats": "Relances solides malgré pression"},
                {"nom": "Jonathan Danty",    "poste": "CE",   "note": 6.8, "stats": "Centre physique, 9 plaquages"},
            ],
        },
        "bilan": {
            "home_forts": [
                "Dupont en maître du jeu absolu : 58% de possession gérée depuis son demi de mêlée, jamais un jeu au pied manqué dans les zones décisives — le meilleur joueur du monde a confirmé son statut",
                "Mauvaka sur ses lancers en touche : 9/10 — l'impact immédiat que donnent les talonneurs dominants change la structure d'un match de rugby",
                "Capuozzo : flair et décision dans l'essai décisif de 58m — les grands ailiers marquent quand ça compte, et ils trouvent les espaces que les autres ne voient pas",
            ],
            "home_faibles": [
                "9 pénalités concédées — contre une équipe comme La Rochelle qui sait marquer des points au pied, c'est trop et ça complique inutilement la fin de match",
                "Quelques mêlées fébriles en première mi-temps, notamment sous le pressing de Priso — La Rochelle a failli retourner cette dynamique de conquête",
            ],
            "away_forts": [
                "Alldritt : colossal au ruck — 14 plaquages, 3 contestations. L'homme qui ne lâche rien même dans la défaite, le vrai cœur de La Rochelle",
                "Skelton sur ses propres lancers : 8/9, une domination technique qui a maintenu La Rochelle dans le match malgré la pression toulousaine",
            ],
            "away_faibles": [
                "12 pénalités concédées à Toulouse — la discipline de La Rochelle à Toulouse a été catastrophique et explique à elle seule l'essentiel du décrochage au score",
                "Aucune solution en attaque de surface sur les 5 derniers mètres — trois fois à portée d'essai, trois fois repoussé. C'est le pack adverse qui a fait la différence dans ces moments",
                "La Rochelle n'a pas su perturber le jeu au pied de Dupont en première mi-temps — il fallait mettre plus de pression sur le demi de mêlée adverse dès le début",
            ],
        },
        "verdict": {
            "home_perf": 8.4, "away_perf": 7.2,
            "intensite": 9.0, "spectacle": 8.5,
            "home_txt": "Toulouse a produit son rugby de champion ce soir. Dupont a été le chef d'orchestre absolu — en direction, en variété, en précision. Ce qui me frappe chez cette équipe, c'est leur capacité à gagner en gérant : ils n'ont pas eu besoin de jouer à 100% pour l'emporter de 10 points. C'est le signe d'une équipe mature qui sait quand accélérer et quand contrôler. Un vrai champion.",
            "away_txt": "La Rochelle a montré de belles choses, notamment Alldritt et Skelton en avant. Mais la discipline a tué ce match. 12 pénalités à Toulouse, c'est offrir des points à l'équipe la plus complète de France. La belle saison de La Rochelle continuera — mais pas à Toulouse.",
            "coach_home": "✅ Ugo Mola a bâti un plan de jeu parfait. L'utilisation de Dupont en libéro d'attaque sur les phases lentes, avec Ntamack tenant le jeu au pied en premier rideau, a créé une confusion défensive permanente. Le choix de Capuozzo en 15 pour ses accélérations sur les relances a été décisif.",
            "coach_away": "❌ O'Gara savait que Toulouse allait chercher le jeu au pied — et son équipe n'a pas su répondre. 12 pénalités dans une rencontre au Stadium, c'est la preuve d'un plan défensif mal adapté à l'adversaire. Il fallait plus de densité au ruck pour couper l'élan de Dupont dès la récupération. C'est la seule façon de le neutraliser.",
        },
    },

    "realmadrid_arsenal_cl": {
        "tactique": {
            "home_form": "4-3-3",
            "away_form": "4-3-3",
            "home_style": "Transitions explosives, Mbappé–Vinicius en largeur, Bellingham libre entre les lignes",
            "away_style": "Pressing collectif intense, Rice en sentinelle, Saka clé côté droit",
            "home_players": [
                ["Courtois","GB"],["Carvajal","RD"],["Militão","DC"],
                ["Rüdiger","DC"],["Mendy","LD"],
                ["Valverde","MC"],["Tchouaméni","MDC"],["Camavinga","MC"],
                ["Mbappé","BU"],["Bellingham","MO"],["Vinicius","AG"],
            ],
            "away_players": [
                ["Raya","GB"],["Ben White","RD"],["Saliba","DC"],
                ["Gabriel","DC"],["Calafiori","LD"],
                ["Rice","MDC"],["Ødegaard","MC"],["Merino","MC"],
                ["Saka","AD"],["Havertz","BU"],["Martinelli","AG"],
            ],
            "phases": {
                "Transitions": "Le Real a exploité 3 transitions rapides après récupérations de Tchouaméni en première mi-temps. Mbappé a marqué le premier but à la 19' en transition en moins de 6 secondes depuis la récupération de Valverde — Vinicius a servi sur un plateau un Mbappé que Calafiori ne pouvait pas suivre dans la profondeur. C'est le Real Madrid dans sa quintessence : récupérer, transitionner, marquer. Arsenal n'avait pas configuré sa défense pour cette vitesse de transition.",
                "Duel Bellingham–Arsenal": "Bellingham en position libre entre les lignes a rendu Arsenal fou. Pendant 60 minutes, ni Rice ni Merino ne savait à qui l'assigner. Ce flottement défensif a offert à Bellingham 6 ballons dans l'espace — il en a converti 1 en but à la 67'. La solution d'Arteta aurait été de coller Merino sur Bellingham avec une instruction spécifique dès la 1ère minute.",
                "Pressing Arsenal": "Arsenal a produit son meilleur pressing en 2e mi-temps — pendant 20 minutes, le Real n'a pas pu construire proprement. Saka a inscrit le 2-1 à la 82' directement issu d'une récupération haute de Rice. Trop tard pour renverser le résultat, mais ces 20 minutes sont un avertissement pour tous les adversaires futurs d'Arsenal en C1.",
                "Gestion de score": "Real Madrid maîtrise la fin de match à 2-1. Courtois décisif sur une tête de Gabriel à la 89'. Ancelotti a su faire entrer Ceballos pour ralentir le tempo dans les 10 dernières minutes — une gestion de match que seules les équipes habituées à gagner en C1 savent produire.",
            },
            "home_stats": {"Possession": (38, 62), "Tirs": (11, 19), "Tirs cadrés": (5, 8), "Passes (%)": (82, 87), "Fautes": (12, 16)},
        },
        "joueurs": {
            "home": [
                {"nom": "Mbappé",      "poste": "BU",  "note": 9.1, "stats": "1 but (19'), 5 dribbles, sprint meurtrier"},
                {"nom": "Bellingham",  "poste": "MO",  "note": 8.9, "stats": "1 but (67'), 67 ballons, 3 dribbles clés"},
                {"nom": "Vinicius",    "poste": "AG",  "note": 8.7, "stats": "1 PD décisive (19'), 6 dribbles, 3 tirs"},
                {"nom": "Courtois",    "poste": "GB",  "note": 8.2, "stats": "5 arrêts décisifs, arrêt vital 89'"},
                {"nom": "Valverde",    "poste": "MC",  "note": 8.0, "stats": "87 ballons, 4 récupérations clés"},
                {"nom": "Tchouaméni", "poste": "MDC", "note": 7.9, "stats": "3 récup. clés, sentinelle du pressing"},
                {"nom": "Militão",     "poste": "DC",  "note": 7.7, "stats": "Intraitable, 6 dégagements"},
            ],
            "away": [
                {"nom": "Saka",      "poste": "AD", "note": 8.4, "stats": "1 but (82'), 7 dribbles, poteau 87'"},
                {"nom": "Rice",      "poste": "MDC","note": 7.8, "stats": "6 récupérations, pressing constant"},
                {"nom": "Saliba",    "poste": "DC", "note": 7.6, "stats": "Duel vs Bellingham : 7/10 gagnés"},
                {"nom": "Havertz",   "poste": "BU", "note": 7.1, "stats": "Pressing haut, 3 récup. en avant, 2 tirs"},
                {"nom": "Ødegaard",  "poste": "MC", "note": 7.0, "stats": "Limité, 68 ballons, 2 key passes"},
                {"nom": "Martinelli","poste": "AG", "note": 7.1, "stats": "3 dribbles, pression constante à gauche"},
                {"nom": "Raya",      "poste": "GB", "note": 7.2, "stats": "6 arrêts, impuissant sur les 2 buts"},
            ],
        },
        "bilan": {
            "home_forts": [
                "Mbappé–Vinicius : le duo le plus rapide d'Europe en transition — le 1er but à la 19' en est la démonstration parfaite, Arsenal n'avait aucune solution défensive pour contenir cette vitesse",
                "Bellingham en position libre : 60 minutes sans que Rice ni Merino ne sache à qui l'assigner — ce flottement défensif d'Arsenal lui a offert 6 espaces dans le match",
                "Efficacité en transitions : 3 situations dangereuses créées sur récupérations de Tchouaméni, 2 buts — le Real Madrid possède cet art dans son ADN depuis des décennies",
                "Courtois dans les grandes occasions : 5 arrêts, dont celui décisif sur Gabriel à la 89' — le meilleur gardien du monde en C1",
            ],
            "home_faibles": [
                "Arsenal a eu 62% de possession — quand Real ne maîtrise pas le ballon, il souffre structurellement. Si Arsenal avait eu plus de précision dans les 20 dernières minutes, le résultat aurait pu être différent",
                "Trop de temps entre possession et finition sur certaines séquences — Arsenal a récupéré 11 ballons sur ces actions trop lentes",
            ],
            "away_forts": [
                "Pressing d'Arsenal en 2e mi-temps : 20 minutes qui ont complètement déstabilisé la construction madrilène, avec le but de Saka à la clé — c'est ce niveau-là qui peut battre le Real",
                "Saka indomptable : 7 dribbles, 1 but, 1 poteau — dans les grandes nuits européennes, ce garçon se transcende systématiquement",
            ],
            "away_faibles": [
                "38% de possession à Bernabéu — Arsenal n'a pas pu jouer son football habituel. Impossible de renverser le Real Madrid sans maîtriser le ballon",
                "Gabriel a perdu son positionnement sur le 2e but de Bellingham — une erreur défensive évitable sur une situation déjà vécue en première mi-temps",
            ],
        },
        "verdict": {
            "home_perf": 8.3, "away_perf": 6.8,
            "intensite": 8.9, "spectacle": 8.6,
            "home_txt": "Real Madrid a montré pourquoi ils sont les maîtres de la Ligue des Champions. Ce n'est pas un hasard s'ils survivent et gagnent des matchs où ils sont dominés en possession — c'est un art perfectionné sur des décennies. Bellingham a changé de dimension cette nuit. Il ne joue plus comme un milieu — il joue comme un numéro 10 de classe mondiale, avec l'instinct du but en plus. Et maintenant avec Mbappé, ils ont deux joueurs capables de punir n'importe quelle erreur défensive en une fraction de seconde — c'est une proposition terrifiante pour toute l'Europe.",
            "away_txt": "Arsenal a montré des choses encourageantes — surtout en 2e mi-temps. Mais perdre 2-1 à Bernabéu avec une telle domination en possession, c'est un goût d'inachevé. Le vrai problème d'Arsenal ce soir : face à la première transition rapide de Mbappé, la défense n'était pas configurée. Deux fois la même erreur de positionnement, deux buts.",
            "coach_home": "✅ Ancelotti n'a eu besoin d'aucun changement tactique majeur jusqu'à la 75'. La décision de laisser Bellingham sans poste fixe a rendu Arsenal fou — ils ne savaient pas s'il fallait le défendre avec Rice ou Merino. Cette liberté, seul Ancelotti l'accorde en Ligue des Champions.",
            "coach_away": "⚠️ Arteta avait bien préparé la sortie de balle basse — mais pas la transition rapide de Real. Un pressing haut avec Rice et Havertz en faux 9 pressant Tchouaméni aurait pu réduire les espaces pour Mbappé. Il l'a compris à la pause — malheureusement, 2-0 à la 67' c'est trop tard pour espérer renverser le Real au Bernabéu.",
        },
    },

    "bayernpsg_cl": {
        "tactique": {
            "home_form": "4-2-3-1",
            "away_form": "4-3-3",
            "home_style": "Pressing haut sous Kompany, Musiala libre en 10, Kane pivot central, Olise et Sané en largeur",
            "away_style": "Possession fluide, Vitinha–João Neves en relance, Dembélé–Barcola en contre",
            "home_players": [
                ["Neuer","GB"],["Kimmich","RD"],["Upamecano","DC"],
                ["Kim Min-jae","DC"],["Davies","LD"],
                ["Goretzka","MDC"],["Musiala","MC"],
                ["Olise","AD"],["Müller","MO"],["Sané","AG"],
                ["Kane","BU"],
            ],
            "away_players": [
                ["Donnarumma","GB"],["Hakimi","RD"],["Marquinhos","DC"],
                ["Pacho","DC"],["Nuno Mendes","LD"],
                ["Fabian Ruiz","MC"],["Vitinha","MC"],["João Neves","MC"],
                ["Dembélé","AD"],["Barcola","AG"],["G. Ramos","BU"],
            ],
            "phases": {
                "Pressing": "Bayern sous Kompany a retrouvé une agressivité qu'on n'avait pas vue depuis l'ère Klopp–Guardiola. Le pressing haut imposé dès la 1ère minute a mis PSG en difficulté dans sa construction. Vitinha a été coupé 9 fois dans les 20 premières minutes — un record pour lui cette saison. Mais PSG a trouvé la solution par Marquinhos qui jouait plus long, court-circuitant le pressing adverse. C'est le signe d'une équipe mature : quand le plan A ne fonctionne pas, on passe au plan B sans panique.",
                "Kane vs Défense PSG": "Kane a touché 41 ballons, plus que n'importe quel attaquant adverse cette saison contre PSG. Sa capacité à décrocher, fixer Marquinhos, et servir Musiala dans l'espace est une intelligence de jeu de très haut niveau. Le but bavarois à la 52' est né de cette action : Kane décroche, Pacho hésite à suivre, Musiala reçoit dans l'espace et frappe du droit. Un mouvement répété à l'entraînement.",
                "Réponse PSG": "PSG a répondu avec sa philosophie : Dembélé en 1v1 côté droit sur Alphonso Davies. 5 tentatives en première mi-temps, 3 fois il a passé Davies dans la vitesse. Barcola côté gauche a créé le penalty égalisateur en déclenchant la faute de Kimmich à la 71'. Luis Enrique a fait confiance à son système plutôt que de le modifier — et le système a répondu.",
                "Densité au milieu": "Le duel João Neves–Goretzka a été la vraie clé du match. Neves a récupéré 7 ballons, Goretzka a joué 68 minutes avant d'être remplacé par Laimer. La densité au milieu de Bayern a été difficile à pénétrer pour PSG — mais PSG a su créer par les côtés plutôt que dans l'axe. C'est une adaptation tactique en temps réel qui illustre la maturité collective de cette équipe.",
            },
            "home_stats": {"Possession": (53, 47), "Tirs": (14, 12), "Tirs cadrés": (5, 6), "Passes (%)": (87, 86), "Fautes": (13, 11)},
        },
        "joueurs": {
            "home": [
                {"nom": "Kane",        "poste": "BU", "note": 8.4, "stats": "1 but, 41 ballons, 8 décr., pivot absolu"},
                {"nom": "Musiala",     "poste": "MC", "note": 8.2, "stats": "1 but (52'), 73 ballons, génie entre les lignes"},
                {"nom": "Olise",       "poste": "AD", "note": 7.8, "stats": "3 dribbles, 2 tirs, menace constante"},
                {"nom": "Neuer",       "poste": "GB", "note": 7.6, "stats": "4 arrêts, leader dans sa surface"},
                {"nom": "Davies",      "poste": "LD", "note": 6.5, "stats": "Débordé par Dembélé, 3 fautes"},
                {"nom": "Kimmich",     "poste": "RD", "note": 7.1, "stats": "Penalty concédé (71'), solide autrement"},
            ],
            "away": [
                {"nom": "Dembélé",    "poste": "AD", "note": 8.5, "stats": "5 dribbles, 3 tirs, dominant sur Davies"},
                {"nom": "João Neves", "poste": "MC", "note": 8.3, "stats": "7 récupérations, pression constante"},
                {"nom": "Barcola",    "poste": "AG", "note": 8.0, "stats": "Penalty provoqué (71'), 4 dribbles"},
                {"nom": "G. Ramos",   "poste": "BU", "note": 7.6, "stats": "1 but (pen. 71'), 5 tirs dont 3 cadrés"},
                {"nom": "Marquinhos", "poste": "DC", "note": 7.8, "stats": "Leader défensif, solution en jeu long"},
                {"nom": "Donnarumma","poste": "GB", "note": 7.5, "stats": "3 arrêts, serein face à Kane"},
            ],
        },
        "bilan": {
            "home_forts": [
                "Kane–Musiala : la combinaison décrocheuse-exploiteur est la plus intelligente que Bayern ait produite en C1 cette saison — 1 but, 3 situations directement créées sur cette action",
                "Pressing de Kompany : 9 récupérations en zone adverse en première mi-temps — Bayern a imposé son rythme physique pendant 45 minutes",
                "Olise depuis son arrivée de Crystal Palace : une arme offensive redoutable sur le côté droit qui a clairement posé des problèmes à PSG défensivement",
            ],
            "home_faibles": [
                "Davies sur Dembélé : 5 dribbles subis, 1 faute et 1 penalty — la vitesse de Dembélé est le problème structurel de ce Bayern, même Alphonso Davies est insuffisant pour contenir cet ailier",
                "Manque de fluidité en 2e mi-temps : quand PSG a reculé et rallongé le jeu, Bayern a eu du mal à casser les lignes sans Goretzka",
            ],
            "away_forts": [
                "Résilience tactique : face au pressing de Kompany, PSG a adapté son jeu (jeu long via Marquinhos) en 10 minutes sans coaching visible — c'est la signature d'une équipe intelligente",
                "Dembélé en état de grâce face à Davies : 5 dribbles réussis, le côté droit de PSG est le couloir le plus dangereux d'Europe en ce moment",
            ],
            "away_faibles": [
                "1-0 à la 52' sur une erreur de placement de Pacho : il n'aurait jamais dû laisser Musiala recevoir dans cet espace. Marquinhos avait pourtant bien alerté à la pause sur les décroches de Kane",
                "PSG a manqué 3 occasions de prise de profondeur en 1ère période — Ramos isolé trop souvent, sans soutien latéral immédiat",
            ],
        },
        "verdict": {
            "home_perf": 7.6, "away_perf": 7.4,
            "intensite": 8.7, "spectacle": 8.8,
            "home_txt": "Bayern Munich sous Kompany a retrouvé son identité : un pressing agressif, une structure défensive solide, et des joueurs de talent offensif (Musiala, Olise, Kane) qui peuvent punir n'importe qui. Ce 1-1 est honnête. Ce que je retiens, c'est que Bayern a les ressources pour aller loin en C1 cette saison. Kane est dans une forme terrifiante. Musiala est le meilleur joueur de sa génération. Et Kompany les utilise avec intelligence.",
            "away_txt": "PSG s'en tire avec un 1-1 qui les replace correctement dans le groupe. Ce que Luis Enrique a démontré ce soir, c'est que ce PSG est difficile à tuer. 0-1 à la 52', ils auraient pu s'effondrer. Ils ont trouvé l'égalisation via Barcola. Cette mentalité ne s'achète pas — elle se construit. C'est le PSG le plus solide mentalement depuis des années.",
            "coach_home": "✅ Kompany a osé presser haut une équipe comme PSG — et ça a fonctionné 45 minutes. Son utilisation de Müller en 10 pour fixer Marquinhos et libérer Kane est du coaching de haut niveau. Le Bayern est en bonne voie.",
            "coach_away": "✅ Luis Enrique a adapté son jeu en 10 minutes quand le pressing bavarois fonctionnait — jeu long, Ramos en pivot, attendre les espaces. C'est une équipe qui joue avec sa tête autant qu'avec ses jambes.",
        },
    },
    "barca_real_laliga_j33": {
        "tactique": {
            "home_form": "4-3-3",
            "away_form": "4-3-3",
            "home_style": "Gegenpressing ultra-haut, récupération haute, Yamal et Raphinha comme déclencheurs du pressing, triangles Pedri–Casado–De Jong dans l'axe",
            "away_style": "4-3-3 pragmatique, compacité défensive, liberté totale pour Bellingham entre les lignes, transitions rapides via Mbappé et Vinicius",
            "home_players": [
                ["Szczesny","GB"],["Koundé","RD"],["Cubarsí","DC"],
                ["Araujo","DC"],["Balde","LD"],
                ["Casado","MDC"],["Pedri","MC"],["De Jong","MC"],
                ["Yamal","AD"],["Lewandowski","BU"],["Raphinha","AG"],
            ],
            "away_players": [
                ["Courtois","GB"],["Carvajal","RD"],["Militão","DC"],
                ["Rüdiger","DC"],["Mendy","LD"],
                ["Valverde","MC"],["Tchouaméni","MDC"],["Camavinga","MC"],
                ["Bellingham","MO"],["Mbappé","BU"],["Vinicius","AG"],
            ],
            "phases": {
                "Pressing Haut Barça": "Le gegenpressing de Flick a été parfait dans les 30 premières minutes. Yamal et Raphinha se placent à hauteur des latéraux de Real Madrid, forçant les erreurs. Koundé et Balde participent activement à la pression haute, créant une surtension dans les zones de construction adverses.",
                "Construction Real Madrid": "Ancelotti adapte : Carvajal joue plus intérieur pour créer un 3v3 en construction. Camavinga descend pour recevoir face au jeu. Mais le pressing barcelonais est trop bien organisé — Casado coupe les lignes de passe vers Bellingham systématiquement en première mi-temps.",
                "Transitions Barça": "Les deux buts barcelonais naissent directement de récupérations hautes. Yamal chipe le ballon à Carvajal (23'), joue Lewandowski en profondeur. Raphinha convertit un coup franc obtenu après une faute sur Pedri pressant Tchouaméni (61'). Le gegenpressing transformé en buts — c'est la signature Flick.",
                "Réaction Real Madrid": "Mbappé réduit le score à la 78' sur penalty après une faute d'Araujo. Real presse en 4-2-4 les 15 dernières minutes — Bellingham, Rodrygo, Mbappé et Vinicius tous offensifs. Szczesny réalise deux arrêts décisifs. La pression de Real a été maximale mais Barça tient.",
                "Phases Arrêtées": "Barcelona marque sur coup franc direct (61', Raphinha). Real Madrid obtient 2 corners sans danger. La maîtrise barça sur les CPA offensifs est nette — Lewandowski à la baguette sur les coups de pied arrêtés impose sa présence physique.",
            },
            "home_stats": {
                "Possession (%)":   (63, 37),
                "Tirs cadrés":      (7, 4),
                "Passes réussies":  (512, 298),
                "Duels gagnés":     (52, 48),
                "Km parcourus":     (113, 108),
                "Occasions nettes": (5, 3),
            },
        },
        "joueurs": {
            "home": [
                {"nom": "Szczesny",     "poste": "GB",  "note": 8.1, "stats": {"Arrêts": 4, "Sorties": 2}},
                {"nom": "Koundé",       "poste": "RD",  "note": 7.8, "stats": {"Duels": "5/6", "Centres": 3}},
                {"nom": "Araujo",       "poste": "DC",  "note": 7.2, "stats": {"Duels": "7/9", "Fautes": 2}},
                {"nom": "Cubarsí",      "poste": "DC",  "note": 8.0, "stats": {"Duels": "8/9", "Passes": 62}},
                {"nom": "Balde",        "poste": "LD",  "note": 7.6, "stats": {"Duels": "4/5", "Centres": 4}},
                {"nom": "Pedri",        "poste": "MC",  "note": 8.4, "stats": {"Passes": 74, "Dribbles": 5}},
                {"nom": "Lewandowski",  "poste": "BU",  "note": 8.3, "stats": {"Buts": 1, "Tirs": 4}},
                {"nom": "Yamal",        "poste": "AD",  "note": 9.0, "stats": {"Buts": 0, "Passes D": 2, "Dribbles": 8}},
            ],
            "away": [
                {"nom": "Courtois",     "poste": "GB",  "note": 7.5, "stats": {"Arrêts": 4, "Sorties": 1}},
                {"nom": "Bellingham",   "poste": "MO",  "note": 7.0, "stats": {"Tirs": 3, "Passes": 48}},
                {"nom": "Mbappé",       "poste": "BU",  "note": 7.8, "stats": {"Buts": 1, "Tirs": 5, "Dribbles": 4}},
                {"nom": "Vinicius",     "poste": "AG",  "note": 7.2, "stats": {"Tirs": 2, "Dribbles": 6}},
                {"nom": "Tchouaméni",   "poste": "MDC", "note": 6.8, "stats": {"Ballons perdus": 5, "Duels": "4/7"}},
                {"nom": "Camavinga",    "poste": "MC",  "note": 6.9, "stats": {"Passes": 41, "Duels": "3/5"}},
            ],
        },
        "bilan": {
            "home_forces": [
                "Gegenpressing parfaitement exécuté — récupérations hautes converties en buts",
                "Yamal intouchable sur son couloir droit, Carvajal neutralisé toute la rencontre",
                "Maîtrise totale du milieu de terrain — Pedri omniprésent dans les transitions",
                "Szczesny décisif dans les moments chauds : 4 arrêts dont 2 face à Vinicius",
            ],
            "home_faibles": [
                "Araujo a commis la faute sur Mbappé qui a relancé Real Madrid",
                "Quelques pertes de balle de De Jong sous pression en seconde période",
            ],
            "away_forces": [
                "Mbappé dangereux sur sa seule occasion franche, pénalty transformé avec sang-froid",
                "Real Madrid a créé des occasions malgré la domination barcelonaise",
                "Bellingham a tenté de déstabiliser le bloc barça en seconde période",
            ],
            "away_faibles": [
                "Construction trop prévisible — Camavinga et Tchouaméni pressés constamment",
                "Vinicius n'a jamais passé Koundé en duel direct — match frustrant pour le Brésilien",
                "Ancelotti a trop tardé à effectuer des changements offensifs (67' au lieu de 55')",
            ],
        },
        "verdict": {
            "home_perf": 8.5,
            "away_perf": 6.5,
            "intensite": 9.0,
            "spectacle": 8.5,
            "home_txt": "Barcelona a livré une masterclass de football offensif collectif. Le gegenpressing de Flick a été parfaitement exécuté — Yamal à 17 ans a dominé Carvajal comme si c'était un match amical. Lewandowski à 37 ans reste le finisseur de référence. Ce Barça est en train d'écrire quelque chose de grand.",
            "away_txt": "Real Madrid a subi sa loi — mais n'a jamais abandonné. Mbappé a montré son caractère en réduisant le score sur penalty. Ancelotti a manqué d'audace tactique en première mi-temps. La défaite est méritée mais le Real reste dangereux jusqu'au bout.",
            "coach_home": "✅ Flick a réglé son pressing comme une horloge suisse. Décision de lancer Cubarsí titulaire plutôt que Christensen — excellente. L'animation offensive avec Yamal libre de tout marquage était préparée depuis des jours. Barça de haut niveau sous ses ordres.",
            "coach_away": "⚠️ Ancelotti a trop respecté Barça. Laisser Mbappé isolé sans soutien pendant 60 minutes, c'est gâcher sa meilleure arme. Un 4-3-3 offensif dès la 55' aurait pu changer le match. La gestion des changements reste son seul point faible.",
        },
    },
}

# ── Profils entraîneurs Ligue 1 ───────────────────────────────────────────────
COACHES: dict[str, dict] = {
    'PSG': {
        'name': 'Luis Enrique',
        'nationality': '🇪🇸',
        'formation': '4-3-3',
        'style': 'Possession verticale, pressing très haut',
        'philosophy': 'Jeu de possession avec verticalité rapide. Pressing intensif dès la perte du ballon. Couloirs larges exploités en permanence. Gardien intégré dans la construction. Favorise les joueurs polyvalents capables de presser et jouer en une touche.',
        'strengths': ['Pressing collectif intense', 'Transitions offensives rapides', 'Variété dans les schémas offensifs', 'Utilisation intelligente des largeurs'],
        'weaknesses': ['Parfois vulnérable sur les contre-attaques', 'Dépendance aux individualités'],
        'key_principles': ['Pressing haut immédiat à la perte', 'Sorties de balle structurées', 'Rotations milieu-attaque', 'Surcharges sur les côtés']
    },
    'Marseille': {
        'name': 'Roberto De Zerbi',
        'nationality': '🇮🇹',
        'formation': '4-2-3-1',
        'style': 'Possession élaborée, construction depuis la défense',
        'philosophy': 'Jeu de possession très structuré depuis le gardien. Sorties de balle codifiées avec le gardien inclus. Pressing organisé par zones. Transitions offensives rapides après récupération. Très exigeant tactiquement, demande une grande maîtrise technique collective.',
        'strengths': ['Construction propre depuis l\'arrière', 'Pressing par zones très organisé', 'Jeu positionnel élaboré', 'Créativité offensive'],
        'weaknesses': ['Vulnérable au pressing adverse haut', 'Nécessite des joueurs très techniques'],
        'key_principles': ['Gardien libéro', 'Supériorité numérique en construction', 'Pressing triggers définis', 'Circuits de passes codifiés']
    },
    'Monaco': {
        'name': 'Adi Hütter',
        'nationality': '🇦🇹',
        'formation': '4-2-3-1',
        'style': 'Pressing intense, jeu direct et vertical',
        'philosophy': 'Équipe très physique et verticale. Pressing intensif sur tout le terrain. Jeu direct vers l\'avant dès la récupération. Exploitation des espaces en transition. Favorise les joueurs athlétiques et rapides.',
        'strengths': ['Intensité physique très élevée', 'Efficacité en transition', 'Pressing collectif', 'Vitesse de jeu'],
        'weaknesses': ['Moins à l\'aise dans la gestion du score', 'Peut manquer de patience en possession'],
        'key_principles': ['Transition défense-attaque en moins de 6 secondes', 'Pressing immédiat', 'Verticalité maximale', 'Duels physiques assumés']
    },
    'Lille': {
        'name': 'Bruno Genesio',
        'nationality': '🇫🇷',
        'formation': '4-4-2',
        'style': 'Bloc médian compact, contre-attaques rapides',
        'philosophy': 'Organisation défensive très solide en bloc médian. Contre-attaques rapides sur les côtés. Discipline collective prioritaire. Équilibre défense-attaque soigné. Exploitation des transitions sur les largeurs.',
        'strengths': ['Solidité défensive collective', 'Efficacité sur les transitions', 'Organisation et discipline', 'Duels remportés au milieu'],
        'weaknesses': ['Peut manquer de créativité en possession', 'Dépendant du pressing adverse'],
        'key_principles': ['Bloc médian compact', 'Contre-attaque rapide sur les ailes', 'Duels physiques au milieu', 'Solidité défensive avant tout']
    },
    'Lyon': {
        'name': 'Pierre Sage',
        'nationality': '🇫🇷',
        'formation': '4-3-3',
        'style': 'Possession patient, pressing organisé par zones',
        'philosophy': 'Jeu de possession patient avec pressing organisé par zones. Exploitation intelligente des couloirs. Construction propre depuis l\'arrière. Équilibre entre solidité défensive et créativité offensive.',
        'strengths': ['Possession maîtrisée', 'Organisation défensive', 'Utilisation des couloirs', 'Collectif soudé'],
        'weaknesses': ['Peut manquer de verticalité', 'Dépendance aux individualités offensives'],
        'key_principles': ['Patience en possession', 'Pressing par zones définis', 'Largeurs exploitées', 'Transitions contrôlées']
    },
    'Nice': {
        'name': 'Franck Haise',
        'nationality': '🇫🇷',
        'formation': '4-3-3',
        'style': 'Pressing haut, jeu direct, largeur maximale',
        'philosophy': 'Pressing très haut dès la perte du ballon. Jeu direct et vertical. Largeur maximale avec des ailiers qui fixent les défenseurs. Très similaire à son système de Lens. Intensité physique élevée sur toute la durée du match.',
        'strengths': ['Pressing très haut efficace', 'Largeurs maximales', 'Intensité physique', 'Jeu direct efficace'],
        'weaknesses': ['Peut s\'exposer sur les espaces dans le dos', 'Fatigue physique en fin de match'],
        'key_principles': ['Pressing immédiat', 'Ailiers très hauts et larges', 'Jeu direct vers les attaquants', 'Intensité constante']
    },
    'Lens': {
        'name': 'Will Still',
        'nationality': '🇧🇪',
        'formation': '4-2-3-1',
        'style': 'Data-driven, pressing intense par zones',
        'philosophy': 'Approche très analytique basée sur la data. Pressing intense déclenché par des triggers précis. Jeu de transition rapide. Grande adaptabilité tactique selon les adversaires. Utilise beaucoup la vidéo et l\'analyse de données.',
        'strengths': ['Adaptabilité tactique', 'Pressing déclenché intelligemment', 'Transitions rapides', 'Analyse adverse poussée'],
        'weaknesses': ['Peut manquer de spontanéité', 'Dépend de la rigueur collective'],
        'key_principles': ['Triggers de pressing définis', 'Blocs défensifs adaptables', 'Transition rapide', 'Analyse data intégrée']
    },
    'Rennes': {
        'name': 'Jorge Sampaoli',
        'nationality': '🇦🇷',
        'formation': '3-4-3',
        'style': 'Pressing ultra-offensif, chaos contrôlé',
        'philosophy': 'Pressing ultra-offensif et intense. Schéma en 3-4-3 très offensif. Chaos contrôlé avec des joueurs très mobiles. Transitions offensives explosives. Très exigeant physiquement. Peut sembler désorganisé mais répond à une logique précise.',
        'strengths': ['Intensité offensive maximale', 'Pressing très haut', 'Transitions explosives', 'Imprévisibilité'],
        'weaknesses': ['Vulnérable défensivement', 'Physiquement très exigeant', 'Peut manquer de contrôle'],
        'key_principles': ['Pressing maximum partout', 'Mobilité constante', 'Transitions offensives immédiates', '3 attaquants très actifs']
    },
    'Strasbourg': {
        'name': 'Liam Rosenior',
        'nationality': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
        'formation': '4-2-3-1',
        'style': 'Jeu de possession, organisation défensive',
        'philosophy': 'Jeu de possession structuré. Organisation défensive solide. Développement des jeunes joueurs. Approche moderne du football avec pressing organisé.',
        'strengths': ['Organisation collective', 'Possession structurée', 'Solidité défensive'],
        'weaknesses': ['Manque d\'expérience au haut niveau', 'Effectif limité'],
        'key_principles': ['Possession maîtrisée', 'Bloc défensif compact', 'Développement collectif']
    },
    'Brest': {
        'name': 'Eric Roy',
        'nationality': '🇫🇷',
        'formation': '4-3-3',
        'style': 'Pressing offensif, jeu direct et efficace',
        'philosophy': 'Pressing offensif bien organisé. Jeu direct et efficace sans fioritures. Équipe très solidaire et compacte. Exploitation des erreurs adverses. Efficacité maximale avec les ressources disponibles.',
        'strengths': ['Solidarité collective', 'Efficacité offensive', 'Pressing organisé', 'Mental très fort'],
        'weaknesses': ['Effectif moins profond', 'Peut manquer de technique sur certains postes'],
        'key_principles': ['Pressing offensif immédiat', 'Jeu direct efficace', 'Solidarité défensive', 'Exploitation des espaces']
    },
    'Toulouse': {
        'name': 'Carles Martínez Novell',
        'nationality': '🇪🇸',
        'formation': '4-2-3-1',
        'style': 'Jeu de possession, pressing organisé',
        'philosophy': 'Jeu de possession structuré à l\'espagnole. Pressing organisé par zones. Construction propre depuis la défense. Développement d\'un jeu collectif cohérent.',
        'strengths': ['Possession structurée', 'Organisation collective', 'Pressing par zones'],
        'weaknesses': ['Peut manquer de verticalité', 'Effectif en construction'],
        'key_principles': ['Possession patient', 'Pressing triggers', 'Construction depuis l\'arrière']
    },
    'Reims': {
        'name': 'Luka Elsner',
        'nationality': '🇸🇮',
        'formation': '4-4-2',
        'style': 'Bloc compact, transitions rapides',
        'philosophy': 'Bloc défensif compact et bien organisé. Transitions rapides vers l\'avant. Efficacité sur les coups de pied arrêtés. Discipline collective très forte.',
        'strengths': ['Solidité défensive', 'Efficacité sur CPA', 'Organisation collective', 'Mental solide'],
        'weaknesses': ['Jeu offensif limité', 'Manque de créativité'],
        'key_principles': ['Bloc compact bas', 'Transitions rapides', 'CPA travaillés', 'Discipline collective']
    },
    'Nantes': {
        'name': 'Antoine Kombouaré',
        'nationality': '🇫🇷',
        'formation': '4-4-2',
        'style': 'Jeu direct, combativité, duels physiques',
        'philosophy': 'Football direct et combatif. Jeu aérien important. Duels physiques assumés. Passion et mental au cœur du projet. Exploitation des points forts individuels.',
        'strengths': ['Combativité', 'Jeu aérien', 'Mental compétiteur', 'Duels physiques'],
        'weaknesses': ['Jeu de possession limité', 'Peut manquer de technique collective'],
        'key_principles': ['Jeu direct', 'Duels physiques gagnés', 'Mental combatif', 'Efficacité sur les coups de pied arrêtés']
    },
    'Montpellier': {
        'name': 'Jean-Louis Gasset',
        'nationality': '🇫🇷',
        'formation': '4-3-3',
        'style': 'Jeu offensif, possession, technique',
        'philosophy': 'Football offensif et technique. Jeu de possession avec verticalité. Valorisation des joueurs techniques. Approche offensive assumée.',
        'strengths': ['Jeu technique', 'Approche offensive', 'Valorisation des talents'],
        'weaknesses': ['Fragilité défensive', 'Manque de solidité collective'],
        'key_principles': ['Possession technique', 'Verticalité rapide', 'Valorisation individuelle']
    },
    'Le Havre': {
        'name': 'Didier Digard',
        'nationality': '🇫🇷',
        'formation': '4-3-3',
        'style': 'Jeu propre, développement des jeunes',
        'philosophy': 'Football propre et structuré. Développement des jeunes talents. Jeu de possession patient. Organisation défensive sérieuse.',
        'strengths': ['Organisation défensive', 'Développement jeunes', 'Jeu structuré'],
        'weaknesses': ['Manque d\'expérience', 'Effectif limité offensivement'],
        'key_principles': ['Possession patient', 'Bloc défensif organisé', 'Développement jeunes']
    },
    'Auxerre': {
        'name': 'Christophe Pélissier',
        'nationality': '🇫🇷',
        'formation': '4-4-2',
        'style': 'Bloc compact, efficacité, pragmatisme',
        'philosophy': 'Football pragmatique et efficace. Bloc défensif compact. Transitions rapides. Efficacité maximale avec les moyens disponibles.',
        'strengths': ['Pragmatisme', 'Solidité défensive', 'Efficacité en transition'],
        'weaknesses': ['Jeu offensif limité', 'Manque de profondeur'],
        'key_principles': ['Bloc compact', 'Pragmatisme', 'Transitions efficaces']
    },
    'Angers': {
        'name': 'Alexandre Dujeux',
        'nationality': '🇫🇷',
        'formation': '4-2-3-1',
        'style': 'Organisation, solidarité, montée en puissance',
        'philosophy': 'Football organisé et solidaire. Construction progressive. Développement collectif. Montée en puissance progressive dans la saison.',
        'strengths': ['Organisation collective', 'Solidarité', 'Progression collective'],
        'weaknesses': ['Manque d\'expérience Ligue 1', 'Effectif en construction'],
        'key_principles': ['Organisation défensive', 'Solidarité collective', 'Construction progressive']
    },
    'Saint-Etienne': {
        'name': 'Olivier Dall\'Oglio',
        'nationality': '🇫🇷',
        'formation': '4-3-3',
        'style': 'Pressing, intensité, identité forte',
        'philosophy': 'Football intense avec pressing organisé. Identité forte et combativité. Jeu direct avec des transitions rapides. Exploitation du soutien populaire.',
        'strengths': ['Combativité', 'Identité forte', 'Pressing organisé', 'Soutien populaire'],
        'weaknesses': ['Effectif limité', 'Manque de régularité'],
        'key_principles': ['Pressing collectif', 'Combativité', 'Jeu direct', 'Identité forte']
    },
    # ── NBA ───────────────────────────────────────────────────────────────────
    'Lakers': {
        'name': 'JJ Redick',
        'nationality': '🇺🇸',
        'formation': 'Drop Coverage / Switch',
        'style': 'Spacing maximal, jeu de pick and roll',
        'philosophy': 'Spacing maximal pour libérer LeBron et Davis. Utilisation intensive du pick and roll. Défense en drop coverage sur les porteurs de balle. Jeu rapide en transition. Valorisation des shooteurs extérieurs autour des deux stars.',
        'strengths': ['Duo LeBron-Davis dominant', 'Spacing offensif', 'Expérience playoff', 'Polyvalence défensive'],
        'weaknesses': ['Défense parfois poreuse', 'Dépendance aux stars', 'Profondeur de banc limitée'],
        'key_principles': ['Pick and roll prioritaire', 'Spacing maximal', 'Transition rapide', 'Isolation pour LeBron/AD']
    },
    'Warriors': {
        'name': 'Steve Kerr',
        'nationality': '🇺🇸',
        'formation': 'Motion Offense',
        'style': 'Ball movement, spacing, tirs à 3 points',
        'philosophy': 'Motion offense basée sur le mouvement collectif du ballon. Spacing maximal avec shooteurs à 3 points. Death lineup avec 5 joueurs polyvalents. Défense commutable sur toutes les actions. Philosophie de partage du ballon.',
        'strengths': ['Ball movement exceptionnel', 'Tirs à 3 points', 'Défense commutable', 'Expérience collective'],
        'weaknesses': ['Vieillissement du roster', 'Défense parfois lente', 'Transition générationnelle'],
        'key_principles': ['Ball movement constant', 'Off-ball movement', 'Spacing 5 extérieurs', 'Switch défensif systématique']
    },
    'Celtics': {
        'name': 'Joe Mazzulla',
        'nationality': '🇺🇸',
        'formation': 'Switch Everything',
        'style': 'Défense élite, attaque polyvalente',
        'philosophy': 'Défense de niveau élite basée sur le switch systématique. Attaque polyvalente avec multiples créateurs. Tirs à 3 points en grande quantité. Duo Tatum-Brown comme piliers offensifs. Intensité défensive maximale.',
        'strengths': ['Défense élite', 'Polyvalence offensive', 'Tirs à 3 points', 'Profondeur de roster'],
        'weaknesses': ['Peut manquer de création en isolation', 'Dépendance au tir extérieur'],
        'key_principles': ['Switch défensif systématique', 'Tirs à 3 points prioritaires', 'Duo Tatum-Brown', 'Intensité défensive']
    },
    'Heat': {
        'name': 'Erik Spoelstra',
        'nationality': '🇺🇸',
        'formation': 'Zone Defense / Man',
        'style': 'Heat Culture, défense intense, adaptabilité',
        'philosophy': 'Heat Culture — travail acharné et discipline absolue. Défense intense avec rotations parfaites. Grande adaptabilité tactique. Développement de joueurs non draftés en stars. Zone defense utilisée stratégiquement.',
        'strengths': ['Culture de travail unique', 'Adaptabilité tactique', 'Défense intense', 'Développement des joueurs'],
        'weaknesses': ['Peut manquer de talent pur', 'Dépend du système'],
        'key_principles': ['Heat Culture', 'Défense collective', 'Adaptabilité', 'Rotations parfaites']
    },
    'Nuggets': {
        'name': 'Michael Malone',
        'nationality': '🇺🇸',
        'formation': 'Jokic-Centered Offense',
        'style': 'Jeu centré sur Jokic, passes, intelligence',
        'philosophy': 'Tout le système est construit autour de Nikola Jokic comme playmaker central. Jeu lent et patient favorisant l\'intelligence de jeu. Passes et mouvements sans ballon. Défense solide mais pas spectaculaire. Efficacité maximale.',
        'strengths': ['Jokic comme arme ultime', 'Intelligence de jeu collective', 'Efficacité offensive', 'Patience tactique'],
        'weaknesses': ['Dépendance à Jokic', 'Défense perfectible', 'Manque de vitesse'],
        'key_principles': ['Jokic comme playmaker', 'Patience en attaque', 'Mouvements sans ballon', 'Intelligence collective']
    },
    'Bucks': {
        'name': 'Doc Rivers',
        'nationality': '🇺🇸',
        'formation': 'Giannis-Centered',
        'style': 'Attaque dans la raquette, Giannis dominant',
        'philosophy': 'Système centré sur les drives de Giannis vers la raquette. Shooteurs placés autour pour les kick-outs. Défense agressive. Exploitation de la dominance physique de Giannis.',
        'strengths': ['Giannis dominant', 'Attaque dans la raquette', 'Défense agressive'],
        'weaknesses': ['Prévisibilité offensive', 'Dépendance à Giannis'],
        'key_principles': ['Drives de Giannis', 'Kick-out vers les shooteurs', 'Défense agressive', 'Raquette dominée']
    },
    'Suns': {
        'name': 'Mike Budenholzer',
        'nationality': '🇺🇸',
        'formation': 'Pick and Roll / Isolation',
        'style': 'Stars en isolation, pick and roll efficace',
        'philosophy': 'Exploitation des stars en isolation et pick and roll. Spacing pour Kevin Durant et Devin Booker. Défense bien organisée. Utilisation optimale du talent individuel.',
        'strengths': ['Talent individuel élite', 'Pick and roll Durant-Booker', 'Spacing offensif'],
        'weaknesses': ['Cohésion collective', 'Défense parfois insuffisante'],
        'key_principles': ['Isolation stars', 'Pick and roll KD-Booker', 'Spacing maximal', 'Talent individuel']
    },
    'Knicks': {
        'name': 'Tom Thibodeau',
        'nationality': '🇺🇸',
        'formation': 'Man-to-Man Defense',
        'style': 'Défense intense, jeu physique, dureté',
        'philosophy': 'Défense man-to-man très intense. Jeu physique et dur. Minutes élevées pour les meilleurs joueurs. Identité défensive avant tout. Culture de dureté et de compétition.',
        'strengths': ['Défense intense', 'Mentalité compétitive', 'Jeu physique', 'Culture défensive'],
        'weaknesses': ['Gestion des minutes', 'Jeu offensif parfois limité', 'Fatigue en fin de saison'],
        'key_principles': ['Défense man-to-man', 'Intensité physique', 'Dureté collective', 'Identité défensive']
    },
    'Bulls': {
        'name': 'Billy Donovan',
        'nationality': '🇺🇸',
        'formation': 'Motion Offense',
        'style': 'Motion offense, LaVine et DeRozan en vedette',
        'philosophy': 'Motion offense avec LaVine et DeRozan comme créateurs principaux. Jeu en demi-terrain patient. Défense en construction. Développement collectif progressif.',
        'strengths': ['LaVine athlétisme', 'DeRozan mid-range', 'Motion offense fluide'],
        'weaknesses': ['Défense insuffisante', 'Manque de présence intérieure', 'Régularité'],
        'key_principles': ['Motion offense', 'LaVine-DeRozan création', 'Jeu demi-terrain', 'Développement collectif']
    },
    'Nets': {
        'name': 'Jordi Fernandez',
        'nationality': '🇪🇸',
        'formation': 'Development System',
        'style': 'Développement jeunes, construction long terme',
        'philosophy': 'Phase de reconstruction complète. Développement des jeunes talents. Liberté offensive pour les joueurs en progression. Construction d\'une identité collective sur le long terme.',
        'strengths': ['Développement jeunes', 'Liberté offensive', 'Construction long terme'],
        'weaknesses': ['Résultats immédiats limités', 'Roster jeune et inexpérimenté'],
        'key_principles': ['Développement jeunes', 'Construction identité', 'Liberté créative', 'Long terme']
    },
    'Clippers': {
        'name': 'Tyronn Lue',
        'nationality': '🇺🇸',
        'formation': 'Versatile Defense',
        'style': 'Défense polyvalente, attaque créative',
        'philosophy': 'Défense polyvalente avec switches fréquents. Attaque créative autour de Kawhi et George. Gestion experte des rotations. Adaptabilité tactique selon les adversaires.',
        'strengths': ['Défense polyvalente', 'Gestion des rotations', 'Adaptabilité', 'Expérience playoff'],
        'weaknesses': ['Blessures récurrentes des stars', 'Régularité en saison'],
        'key_principles': ['Switch défensif', 'Rotation experte', 'Adaptabilité', 'Kawhi en isolation']
    },
    'Spurs': {
        'name': 'Gregg Popovich',
        'nationality': '🇺🇸',
        'formation': 'Fundamental Basketball',
        'style': 'Basket fondamental, développement Wembanyama',
        'philosophy': 'Basketball fondamental basé sur les principes de base. Développement de Victor Wembanyama comme franchise player. Passes et mouvements sans ballon. Défense organisée. Légende vivante du coaching NBA.',
        'strengths': ['Développement Wembanyama', 'Principes fondamentaux', 'Expérience coaching', 'Culture gagnante'],
        'weaknesses': ['Roster en reconstruction', 'Résultats immédiats'],
        'key_principles': ['Fondamentaux basketball', 'Développement Wembanyama', 'Ball movement', 'Défense organisée']
    },
    'Mavericks': {
        'name': 'Jason Kidd',
        'nationality': '🇺🇸',
        'formation': 'Luka-Centered',
        'style': 'Tout autour de Luka Doncic',
        'philosophy': 'Système entièrement construit autour de Luka Doncic comme playmaker et scoreur principal. Spacing pour ses drives et pull-up jumpers. Défense en amélioration constante.',
        'strengths': ['Luka Doncic dominant', 'Créativité offensive', 'Spacing pour Luka'],
        'weaknesses': ['Dépendance totale à Luka', 'Défense perfectible'],
        'key_principles': ['Luka comme playmaker central', 'Spacing pour les drives', 'Isolation Luka', 'Soutien collectif']
    },
    'Grizzlies': {
        'name': 'Taylor Jenkins',
        'nationality': '🇺🇸',
        'formation': 'Physicality First',
        'style': 'Jeu physique, Ja Morant explosif, grit',
        'philosophy': 'Jeu physique et intense centré sur l\'explosivité de Ja Morant. Défense agressive. Culture Grizzlies de dur labeur. Transitions rapides exploitant la vitesse de Morant.',
        'strengths': ['Ja Morant explosif', 'Défense agressive', 'Physicalité', 'Transitions rapides'],
        'weaknesses': ['Dépendance à Morant', 'Régularité défensive'],
        'key_principles': ['Transitions Morant', 'Défense physique', 'Intensité constante', 'Grit culture']
    },
    'Hawks': {
        'name': 'Quin Snyder',
        'nationality': '🇺🇸',
        'formation': 'Trae Young Offense',
        'style': 'Trae Young comme meneur créateur élite',
        'philosophy': 'Système axé sur Trae Young comme meneur créateur d\'élite. Pick and roll constant. Spacing pour ses passes lobées et tirs longue distance. Défense en reconstruction.',
        'strengths': ['Trae Young créativité', 'Pick and roll élite', 'Scoring offensif'],
        'weaknesses': ['Défense insuffisante', 'Dépendance à Trae'],
        'key_principles': ['Pick and roll Trae', 'Spacing maximal', 'Créativité offensive', 'Scoring prioritaire']
    },
    'Pacers': {
        'name': 'Rick Carlisle',
        'nationality': '🇺🇸',
        'formation': 'Up-tempo Offense',
        'style': 'Jeu rapide, Tyrese Haliburton meneur élite',
        'philosophy': 'Rythme de jeu très élevé. Haliburton comme meneur d\'élite en transition. Nombreuses passes décisives. Défense en développement. Plaisir de jouer et scoring offensif.',
        'strengths': ['Haliburton passes', 'Rythme élevé', 'Scoring collectif', 'Jeu rapide'],
        'weaknesses': ['Défense perfectible', 'Régularité en playoffs'],
        'key_principles': ['Rythme élevé', 'Haliburton comme meneur', 'Transitions rapides', 'Scoring collectif']
    },
    'Cavaliers': {
        'name': 'Kenny Atkinson',
        'nationality': '🇺🇸',
        'formation': 'Team Defense',
        'style': 'Défense collective, Donovan Mitchell scoreur',
        'philosophy': 'Défense collective très organisée. Mitchell comme scoreur principal. Jeu d\'équipe cohérent. Construction patiente autour d\'un roster équilibré.',
        'strengths': ['Défense collective', 'Mitchell scoreur', 'Équilibre roster', 'Organisation'],
        'weaknesses': ['Manque de star dominante', 'Playoff expérience'],
        'key_principles': ['Défense collective', 'Mitchell isolation', 'Équilibre offensif', 'Organisation']
    },
    'Thunder': {
        'name': 'Mark Daigneault',
        'nationality': '🇺🇸',
        'formation': 'Youth Movement',
        'style': 'SGA dominant, jeunesse explosive',
        'philosophy': 'Shai Gilgeous-Alexander comme superstar principale. Équipe jeune et explosive. Défense intense. Culture de développement et de compétition. Futur très prometteur.',
        'strengths': ['SGA dominant', 'Profondeur exceptionnelle', 'Défense intense', 'Jeunesse explosive'],
        'weaknesses': ['Expérience playoff limitée', 'Pression des attentes'],
        'key_principles': ['SGA comme leader', 'Défense collective', 'Jeu d\'équipe', 'Développement jeunes']
    },
    'Timberwolves': {
        'name': 'Chris Finch',
        'nationality': '🇬🇧',
        'formation': 'Defense-First',
        'style': 'Défense élite, Towns et Edwards en attaque',
        'philosophy': 'Défense de niveau élite comme identité principale. Anthony Edwards comme leader offensif explosif. Karl-Anthony Towns comme pivot polyvalent. Équilibre défense-attaque.',
        'strengths': ['Défense élite', 'Edwards explosif', 'Polyvalence Towns', 'Intensité'],
        'weaknesses': ['Cohésion parfois fragile', 'Régularité'],
        'key_principles': ['Défense prioritaire', 'Edwards en isolation', 'Towns spacing', 'Intensité défensive']
    },
    'Rockets': {
        'name': 'Ime Udoka',
        'nationality': '🇺🇸',
        'formation': 'Development + Defense',
        'style': 'Défense intense, développement Jalen Green',
        'philosophy': 'Défense très intense comme base. Développement de Jalen Green et Alperen Sengun. Construction d\'une équipe compétitive sur le long terme. Intensité défensive comme identité.',
        'strengths': ['Défense intense', 'Green et Sengun développement', 'Intensité', 'Futur prometteur'],
        'weaknesses': ['Roster jeune', 'Régularité offensive'],
        'key_principles': ['Défense intense', 'Développement stars', 'Intensité constante', 'Construction long terme']
    },
    'Jazz': {
        'name': 'Will Hardy',
        'nationality': '🇺🇸',
        'formation': 'Rebuild System',
        'style': 'Reconstruction, développement jeunes talents',
        'philosophy': 'Phase de reconstruction complète. Développement des jeunes talents avec liberté offensive. Construction d\'une identité de jeu moderne. Patience et vision long terme.',
        'strengths': ['Développement jeunes', 'Liberté créative', 'Vision long terme'],
        'weaknesses': ['Résultats immédiats', 'Roster inexpérimenté'],
        'key_principles': ['Développement jeunes', 'Liberté offensive', 'Construction identité', 'Long terme']
    },
    'Trail Blazers': {
        'name': 'Chauncey Billups',
        'nationality': '🇺🇸',
        'formation': 'Development Focus',
        'style': 'Développement Scoot Henderson, reconstruction',
        'philosophy': 'Développement de Scoot Henderson comme futur franchise player. Reconstruction patiente. Jeu ouvert favorisant le développement individuel.',
        'strengths': ['Henderson développement', 'Jeu ouvert', 'Patience'],
        'weaknesses': ['Résultats immédiats', 'Roster limité'],
        'key_principles': ['Henderson priorité', 'Développement individuel', 'Reconstruction patient']
    },
    'Kings': {
        'name': 'Doug Christie',
        'nationality': '🇺🇸',
        'formation': 'Up-tempo Offense',
        'style': 'Jeu rapide, De\'Aaron Fox explosif',
        'philosophy': 'Rythme de jeu élevé autour de De\'Aaron Fox. Transitions rapides. Scoring offensif élevé. Défense en amélioration.',
        'strengths': ['Fox explosif', 'Rythme élevé', 'Scoring offensif'],
        'weaknesses': ['Défense perfectible', 'Cohésion collective'],
        'key_principles': ['Transitions Fox', 'Rythme élevé', 'Scoring prioritaire']
    },
    'Pelicans': {
        'name': 'Willie Green',
        'nationality': '🇺🇸',
        'formation': 'Inside-Out Game',
        'style': 'Jeu intérieur-extérieur, Zion dominant',
        'philosophy': 'Exploitation de la dominance physique de Zion Williamson. Jeu intérieur-extérieur. Défense solide. Brandon Ingram comme deuxième option offensive.',
        'strengths': ['Zion dominant', 'Défense solide', 'Jeu intérieur'],
        'weaknesses': ['Blessures de Zion', 'Régularité'],
        'key_principles': ['Zion dans la raquette', 'Jeu intérieur-extérieur', 'Défense solide']
    },
    'Wizards': {
        'name': 'Brian Keefe',
        'nationality': '🇺🇸',
        'formation': 'Full Rebuild',
        'style': 'Reconstruction totale, développement',
        'philosophy': 'Reconstruction totale de la franchise. Développement des jeunes joueurs. Liberté offensive maximale. Vision long terme exclusive.',
        'strengths': ['Développement jeunes', 'Liberté créative'],
        'weaknesses': ['Résultats immédiats', 'Roster très limité'],
        'key_principles': ['Reconstruction totale', 'Développement jeunes', 'Long terme']
    },
    'Pistons': {
        'name': 'J.B. Bickerstaff',
        'nationality': '🇺🇸',
        'formation': 'Development System',
        'style': 'Développement Cade Cunningham, reconstruction',
        'philosophy': 'Cade Cunningham comme franchise player en développement. Construction patiente autour des jeunes talents. Défense en développement. Vision long terme.',
        'strengths': ['Cunningham développement', 'Jeunesse', 'Construction long terme'],
        'weaknesses': ['Résultats immédiats', 'Expérience limitée'],
        'key_principles': ['Cunningham priorité', 'Développement collectif', 'Construction patient']
    },
    'Magic': {
        'name': 'Jamahl Mosley',
        'nationality': '🇺🇸',
        'formation': 'Defense-First Youth',
        'style': 'Défense jeune et intense, Paolo Banchero',
        'philosophy': 'Défense intense comme identité. Paolo Banchero comme franchise player. Équipe jeune et athlétique. Développement collectif rapide.',
        'strengths': ['Banchero leadership', 'Défense jeune', 'Athlétisme', 'Développement rapide'],
        'weaknesses': ['Expérience playoff', 'Régularité offensive'],
        'key_principles': ['Défense intense', 'Banchero comme leader', 'Athlétisme', 'Développement']
    },
    'Hornets': {
        'name': 'Charles Lee',
        'nationality': '🇺🇸',
        'formation': 'LaMelo-Centered',
        'style': 'LaMelo Ball créateur, jeu spectaculaire',
        'philosophy': 'LaMelo Ball comme meneur créateur spectaculaire. Jeu ouvert et créatif. Passes no-look et créativité maximale. Développement autour de LaMelo.',
        'strengths': ['LaMelo créativité', 'Jeu spectaculaire', 'Passes élite'],
        'weaknesses': ['Défense insuffisante', 'Régularité'],
        'key_principles': ['LaMelo comme meneur', 'Créativité maximale', 'Jeu ouvert', 'Spectacle']
    },
    'Raptors': {
        'name': 'Darko Rajakovic',
        'nationality': '🇷🇸',
        'formation': 'Defensive Identity',
        'style': 'Défense intense, reconstruction avec jeunes',
        'philosophy': 'Identité défensive forte. Reconstruction autour des jeunes talents. Système défensif bien organisé. Vision long terme pour retrouver le niveau playoff.',
        'strengths': ['Défense organisée', 'Développement jeunes', 'Identité claire'],
        'weaknesses': ['Talent offensif limité', 'Transition post-Siakam'],
        'key_principles': ['Défense prioritaire', 'Développement jeunes', 'Identité défensive']
    },
}

COACH_TEAM_LOOKUP: dict[str, str] = {
    "Paris Saint-Germain":    "PSG",
    "Olympique de Marseille": "Marseille",
    "AS Monaco":              "Monaco",
    "Olympique Lyonnais":     "Lyon",
    "LOSC Lille":             "Lille",
    "OGC Nice":               "Nice",
    "RC Lens":                "Lens",
    "Stade Rennais":          "Rennes",
    "RC Strasbourg":          "Strasbourg",
    "Stade Brestois 29":      "Brest",
    "Toulouse FC":            "Toulouse",
    "Stade de Reims":         "Reims",
    "FC Nantes":              "Nantes",
    "Montpellier HSC":        "Montpellier",
    "Le Havre AC":            "Le Havre",
    "AJ Auxerre":             "Auxerre",
    "Angers SCO":             "Angers",
    "AS Saint-Étienne":       "Saint-Etienne",
    # NBA
    "Los Angeles Lakers":     "Lakers",
    "Golden State Warriors":  "Warriors",
    "Boston Celtics":         "Celtics",
    "Miami Heat":             "Heat",
    "Denver Nuggets":         "Nuggets",
    "Milwaukee Bucks":        "Bucks",
    "Phoenix Suns":           "Suns",
    "New York Knicks":        "Knicks",
    "Chicago Bulls":          "Bulls",
    "Brooklyn Nets":          "Nets",
    "LA Clippers":            "Clippers",
    "San Antonio Spurs":      "Spurs",
    "Dallas Mavericks":       "Mavericks",
    "Memphis Grizzlies":      "Grizzlies",
    "Atlanta Hawks":          "Hawks",
    "Indiana Pacers":         "Pacers",
    "Cleveland Cavaliers":    "Cavaliers",
    "Oklahoma City Thunder":  "Thunder",
    "Minnesota Timberwolves": "Timberwolves",
    "Houston Rockets":        "Rockets",
    "Utah Jazz":              "Jazz",
    "Portland Trail Blazers": "Trail Blazers",
    "Sacramento Kings":       "Kings",
    "New Orleans Pelicans":   "Pelicans",
    "Washington Wizards":     "Wizards",
    "Detroit Pistons":        "Pistons",
    "Orlando Magic":          "Magic",
    "Charlotte Hornets":      "Hornets",
    "Toronto Raptors":        "Raptors",
}

# ── Effectifs réels par équipe (11 joueurs football, 5 basket, 9 rugby) ───────
TEAM_SQUADS: dict[str, list] = {
    # ── Ligue 1 ───────────────────────────────────────────────────────────────
    "Paris Saint-Germain": [
        ["Donnarumma","GB"],["Hakimi","RD"],["Marquinhos","DC"],
        ["Pacho","DC"],["Nuno Mendes","LD"],
        ["Fabian Ruiz","MC"],["Vitinha","MC"],["João Neves","MC"],
        ["Dembélé","AD"],["Barcola","AG"],["G. Ramos","BU"],
    ],
    "AS Monaco": [
        ["Majecki","GB"],["Vanderson","RD"],["Salisu","DC"],
        ["Maripan","DC"],["Caio Henrique","LD"],
        ["Camara","MDC"],["Zakaria","MDC"],
        ["Ben Seghir","MO"],["Akliouche","MO"],["Golovin","MO"],
        ["Embolo","BU"],
    ],
    "Olympique de Marseille": [
        ["Rulli","GB"],["Murillo","RD"],["Balerdi","DC"],
        ["Brassier","DC"],["Merlin","LD"],
        ["Rabiot","MC"],["Kondogbia","MDC"],
        ["Greenwood","AD"],["Harit","MO"],["Rowe","AG"],
        ["Wahi","BU"],
    ],
    "Olympique Lyonnais": [
        ["Perri","GB"],["Tagliafico","LD"],["Niakhaté","DC"],
        ["Mata","DC"],["Kumbedi","RD"],
        ["Tolisso","MC"],["Matic","MDC"],
        ["Benrahma","MO"],["Cherki","MO"],["Lacazette","BU"],["Mikautadze","BU"],
    ],
    "LOSC Lille": [
        ["Chevalier","GB"],["Meunier","RD"],["Diakité","DC"],
        ["Alexsandro","DC"],["Gudmundsson","LD"],
        ["André","MDC"],["Gomes","MC"],
        ["Zhegrova","AD"],["Cabella","MO"],["Haraldsson","AG"],["David","BU"],
    ],
    "OGC Nice": [
        ["Bulka","GB"],["Lotomba","RD"],["Dante","DC"],
        ["Bombito","DC"],["Bard","LD"],
        ["Rosario","MDC"],["Thuram","MC"],
        ["Guessand","AD"],["Boga","MO"],["Cho","AG"],["Laborde","BU"],
    ],
    "RC Lens": [
        ["Samba","GB"],["Frankowski","RD"],["Medina","DC"],
        ["Danso","DC"],["Machado","LD"],
        ["Dansoko","MDC"],["Fulgini","MC"],
        ["Sotoca","AD"],["Thomasson","MO"],["Saïd","AG"],["Openda","BU"],
    ],
    "Toulouse FC": [
        ["Restes","GB"],["Suazo","RD"],["Nicolaisen","DC"],
        ["Costa","DC"],["Donkor","LD"],
        ["Spierings","MDC"],["Dejaegere","MC"],
        ["Aboukhlal","AG"],["Tiago Djaló","MO"],["Dallinga","BU"],["Onaiwu","AD"],
    ],
    "Stade Brestois 29": [
        ["Bizot","GB"],["Lala","RD"],["Chardonnet","DC"],
        ["Pereira","DC"],["Doué","LD"],
        ["Camara","MDC"],["Magnetti","MC"],
        ["Del Castillo","MO"],["Martin","AD"],["Dembélé","AG"],["Mounié","BU"],
    ],
    "Stade Rennais": [
        ["Mandanda","GB"],["Assignon","RD"],["Wooh","DC"],
        ["Belocian","DC"],["Truffert","LD"],
        ["Ugochukwu","MDC"],["Gronbaek","MC"],
        ["Bourigeaud","AD"],["Gouiri","BU"],["Terrier","AG"],["Kalimuendo","BU"],
    ],
    # ── Premier League ────────────────────────────────────────────────────────
    "Arsenal FC": [
        ["Raya","GB"],["Ben White","RD"],["Saliba","DC"],
        ["Gabriel","DC"],["Calafiori","LD"],
        ["Rice","MDC"],["Ødegaard","MC"],["Merino","MC"],
        ["Saka","AD"],["Havertz","BU"],["Martinelli","AG"],
    ],
    "Manchester City": [
        ["Ederson","GB"],["Walker","RD"],["Akanji","DC"],
        ["Dias","DC"],["Gvardiol","LD"],
        ["Kovacic","MDC"],["Nunes","MDC"],
        ["Foden","MO"],["De Bruyne","MO"],["Doku","MO"],
        ["Haaland","BU"],
    ],
    "Liverpool FC": [
        ["Alisson","GB"],["Alexander-Arnold","RD"],["Konaté","DC"],
        ["Van Dijk","DC"],["Robertson","LD"],
        ["Mac Allister","MDC"],["Gravenberch","MC"],
        ["Szoboszlai","MO"],["Salah","AD"],["Diaz","AG"],["Núñez","BU"],
    ],
    "Chelsea FC": [
        ["Sánchez","GB"],["Reece James","RD"],["Colwill","DC"],
        ["Chalobah","DC"],["Cucurella","LD"],
        ["Caicedo","MDC"],["Fernández","MC"],
        ["Palmer","MO"],["Sterling","AD"],["Jackson","BU"],["Madueke","AG"],
    ],
    "Tottenham Hotspur": [
        ["Vicario","GB"],["Porro","RD"],["Romero","DC"],
        ["Van de Ven","DC"],["Udogie","LD"],
        ["Bentancur","MDC"],["Bissouma","MC"],
        ["Kulusevski","AD"],["Maddison","MO"],["Son","AG"],["Richarlison","BU"],
    ],
    "Manchester United": [
        ["Onana","GB"],["Dalot","RD"],["De Ligt","DC"],
        ["Martínez","DC"],["Shaw","LD"],
        ["Casemiro","MDC"],["Mainoo","MC"],
        ["Garnacho","AD"],["Bruno Fernandes","MO"],["Hojlund","BU"],["Rashford","AG"],
    ],
    "Newcastle United": [
        ["Dubravka","GB"],["Trippier","RD"],["Botman","DC"],
        ["Burn","DC"],["Hall","LD"],
        ["Tonali","MDC"],["Guimarães","MC"],
        ["Almiron","AD"],["Isak","BU"],["Gordon","AG"],["Barnes","MO"],
    ],
    "Aston Villa": [
        ["Martinez","GB"],["Cash","RD"],["Konsa","DC"],
        ["Torres","DC"],["Digne","LD"],
        ["Tielemans","MDC"],["Douglas Luiz","MC"],
        ["McGinn","MO"],["Watkins","BU"],["Bailey","AG"],["Zaniolo","AD"],
    ],
    "Brighton & Hove Albion": [
        ["Verbruggen","GB"],["Veltman","RD"],["Dunk","DC"],
        ["Webster","DC"],["Estupiñán","LD"],
        ["Gross","MC"],["Gilmour","MDC"],
        ["Adingra","AD"],["João Pedro","BU"],["Mitoma","AG"],["Baleba","MC"],
    ],
    "West Ham United": [
        ["Areola","GB"],["Coufal","RD"],["Zouma","DC"],
        ["Aguerd","DC"],["Emerson","LD"],
        ["Soucek","MDC"],["Ward-Prowse","MC"],
        ["Bowen","AD"],["Antonio","BU"],["Kudus","AG"],["Paquetá","MO"],
    ],
    # ── Champions League ──────────────────────────────────────────────────────
    "Real Madrid CF": [
        ["Courtois","GB"],["Carvajal","RD"],["Militão","DC"],
        ["Rüdiger","DC"],["Mendy","LD"],
        ["Valverde","MC"],["Tchouaméni","MDC"],["Camavinga","MC"],
        ["Mbappé","BU"],["Bellingham","MO"],["Vinicius","AG"],
    ],
    "Bayern Munich": [
        ["Neuer","GB"],["Kimmich","RD"],["Upamecano","DC"],
        ["Kim Min-jae","DC"],["Davies","LD"],
        ["Goretzka","MDC"],["Musiala","MC"],
        ["Olise","AD"],["Müller","MO"],["Sané","AG"],["Kane","BU"],
    ],
    "FC Barcelona": [
        ["Ter Stegen","GB"],["Koundé","RD"],["Araujo","DC"],
        ["Christensen","DC"],["Balde","LD"],
        ["De Jong","MDC"],["Pedri","MC"],["Gavi","MC"],
        ["Yamal","AD"],["Lewandowski","BU"],["Raphinha","AG"],
    ],
    "Inter Milan": [
        ["Sommer","GB"],["Darmian","RD"],["Acerbi","DC"],
        ["Bastoni","DC"],["Dimarco","LD"],
        ["Barella","MC"],["Calhanoglu","MDC"],["Mkhitaryan","MC"],
        ["Thuram","BU"],["Lautaro","BU"],["Frattesi","MO"],
    ],
    "Atlético de Madrid": [
        ["Oblak","GB"],["Molina","RD"],["Giménez","DC"],
        ["Witsel","DC"],["Reinildo","LD"],
        ["Koke","MC"],["De Paul","MC"],["Saúl","MDC"],
        ["Griezmann","MO"],["Morata","BU"],["Correa","AG"],
    ],
    "Borussia Dortmund": [
        ["Kobel","GB"],["Ryerson","RD"],["Hummels","DC"],
        ["Schlotterbeck","DC"],["Maatsen","LD"],
        ["Emre Can","MDC"],["Nmecha","MC"],
        ["Malen","AD"],["Brandt","MO"],["Sancho","AG"],["Füllkrug","BU"],
    ],
    "Juventus FC": [
        ["Di Gregorio","GB"],["Cambiaso","RD"],["Bremer","DC"],
        ["Gatti","DC"],["Cabal","LD"],
        ["Locatelli","MDC"],["McKennie","MC"],
        ["Yildiz","MO"],["Conceição","AD"],["Vlahovic","BU"],["Weah","AG"],
    ],
    "FC Porto": [
        ["Diogo Costa","GB"],["Joao Mario","RD"],["Cardoso","DC"],
        ["Pepe","DC"],["Galeno","LD"],
        ["Uribe","MDC"],["Eustáquio","MC"],
        ["Pepê","AD"],["Evanilson","BU"],["Taremi","BU"],["Veron","AG"],
    ],
    # ── Super League Suisse ───────────────────────────────────────────────────
    "FC Basel": [
        ["Lindner","GB"],["Lang","RD"],["Pelmard","DC"],
        ["Frei","DC"],["Petretta","LD"],
        ["Burger","MDC"],["Xhaka","MC"],
        ["Males","AD"],["Kasami","MO"],["Ndoye","AG"],["Cabral","BU"],
    ],
    "BSC Young Boys": [
        ["Von Ballmoos","GB"],["Blum","RD"],["Lustenberger","DC"],
        ["Camara","DC"],["Janko","LD"],
        ["Martins","MDC"],["Niasse","MC"],
        ["Elia","AD"],["Ugrinic","MO"],["Monteiro","AG"],["Nsame","BU"],
    ],
    "Servette FC": [
        ["Frick","GB"],["Lavanchy","RD"],["Vouilloz","DC"],
        ["Tsunemoto","DC"],["Clichy","LD"],
        ["Cognat","MDC"],["Stevanovic","MC"],
        ["Kutesa","AD"],["Douline","MO"],["Antunes","AG"],["Bedia","BU"],
    ],
    "FC Zurich": [
        ["Brecher","GB"],["Boranijasevic","RD"],["Kamberi","DC"],
        ["Aliti","DC"],["Guerrero","LD"],
        ["Domgjoni","MDC"],["Conde","MC"],
        ["Tosin","AD"],["Marchesano","MO"],["Okita","AG"],["Santini","BU"],
    ],
    "FC Lugano": [
        ["Saipi","GB"],["Kecskes","RD"],["Daprelà","DC"],
        ["Hajrizi","DC"],["Valenzuela","LD"],
        ["Sabbatini","MDC"],["Lovric","MC"],
        ["Dos Santos","AD"],["Mahou","MO"],["Abubakar","AG"],["Bottani","BU"],
    ],
    "FC Luzern": [
        ["Müller","GB"],["Frydek","RD"],["Burch","DC"],
        ["Simani","DC"],["Sidler","LD"],
        ["Emini","MDC"],["Jashari","MC"],
        ["Dantas","AD"],["Tasar","MO"],["Ugrinic","AG"],["Abubakar","BU"],
    ],
    "FC St. Gallen": [
        ["Lawrence","GB"],["Stillhart","RD"],["Görtler","DC"],
        ["Ambrosius","DC"],["Spreiter","LD"],
        ["Quintillà","MDC"],["Münstermann","MC"],
        ["Ruiz","AD"],["Babic","MO"],["Duah","AG"],["Demirovic","BU"],
    ],
    # ── NBA ───────────────────────────────────────────────────────────────────
    "Los Angeles Lakers": [
        ["LeBron James","SF"],["A. Davis","C"],["Austin Reaves","SG"],
        ["Rui Hachimura","PF"],["Dalton Knecht","SG"],
    ],
    "Golden State Warriors": [
        ["S. Curry","PG"],["Buddy Hield","SG"],["A. Wiggins","SF"],
        ["Draymond Green","PF"],["K. Looney","C"],
    ],
    "Boston Celtics": [
        ["J. Tatum","SF"],["J. Brown","SG"],["K. Porzingis","C"],
        ["J. Holiday","PG"],["D. White","SG"],
    ],
    "Chicago Bulls": [
        ["Z. LaVine","SG"],["DeMar DeRozan","SF"],["N. Vučević","C"],
        ["P. Williams","PF"],["L. Ball","PG"],
    ],
    "Miami Heat": [
        ["J. Butler","SF"],["B. Adebayo","C"],["Tyler Herro","SG"],
        ["T. Duncan","PF"],["D. Robinson","SG"],
    ],
    "New York Knicks": [
        ["J. Brunson","PG"],["J. Randle","PF"],["R. Barrett","SG"],
        ["M. Robinson","C"],["D. DiVincenzo","SG"],
    ],
    "Milwaukee Bucks": [
        ["G. Antetokounmpo","PF"],["D. Lillard","PG"],["K. Middleton","SF"],
        ["B. Lopez","C"],["M. Beasley","SG"],
    ],
    "Phoenix Suns": [
        ["D. Booker","SG"],["B. Beal","SG"],["K. Durant","SF"],
        ["J. Nurkic","C"],["E. Gordon","SG"],
    ],
    "LA Clippers": [
        ["Kawhi Leonard","SF"],["J. Harden","PG"],["N. Powell","SG"],
        ["I. Zubac","C"],["T. Mann","PF"],
    ],
    "Denver Nuggets": [
        ["N. Jokic","C"],["J. Murray","PG"],["M. Porter Jr.","SF"],
        ["A. Gordon","PF"],["K. Caldwell-Pope","SG"],
    ],
    # ── Euroleague ────────────────────────────────────────────────────────────
    "Real Madrid Baloncesto": [
        ["Causeur","SG"],["S. Llull","PG"],["Tavares","C"],
        ["Yabusele","PF"],["Hezonja","SF"],
    ],
    "FC Barcelona Bàsquet": [
        ["Laprovittola","PG"],["Satoransky","SG"],["Brizuela","SG"],
        ["Vesely","C"],["Mirotic","PF"],
    ],
    "Fenerbahce Beko": [
        ["Sloukas","PG"],["De Colo","SG"],["Guduric","SF"],
        ["Bjelica","PF"],["Motiejunas","C"],
    ],
    "Olympiacos BC": [
        ["McKissic","PG"],["Walkup","SG"],["Vezenkov","SF"],
        ["Moustapha Fall","C"],["Papagiannis","C"],
    ],
    "AS Monaco Basket": [
        ["Paris Lee","PG"],["Okouo","SF"],["Motiejunas","PF"],
        ["Brown","C"],["Wilson","SG"],
    ],
    "Bayern Munich Basketball": [
        ["Lucic","PG"],["Booker","SG"],["Weiler-Babb","SF"],
        ["Reynolds","PF"],["Sisko","C"],
    ],
    "Maccabi Tel Aviv": [
        ["Nunnally","SG"],["Hunter","SF"],["Zizic","C"],
        ["Dibartolomeo","PG"],["Sorkin","C"],
    ],
    # ── Betclic Elite ─────────────────────────────────────────────────────────
    "LDLC ASVEL": [
        ["Strazel","PG"],["Howard","SG"],["Odiase","C"],
        ["Yusta","SF"],["Lacombe","PF"],
    ],
    "Paris Basketball": [
        ["Parsons","SG"],["Robinson","PG"],["Edozie","SF"],
        ["Bako","C"],["Loncar","PF"],
    ],
    "SIG Strasbourg": [
        ["Thomas","PG"],["Sy","SG"],["Kalinoski","SF"],
        ["Nwaba","SF"],["Mke Anumba","C"],
    ],
    "JDA Dijon": [
        ["Lighty","SG"],["Stewart","PG"],["Cheatham","PF"],
        ["Obasohan","SG"],["Strazel","SF"],
    ],
    "Boulogne-Levallois Metropolitans 92": [
        ["Kahudi","SF"],["Moerman","SF"],["Jaiteh","C"],
        ["Stauskas","SG"],["Toupane","SG"],
    ],
    "JSF Nanterre": [
        ["Peyrot","PG"],["Obasohan","SG"],["Lighty","SF"],
        ["Cheatham","PF"],["Diagne","C"],
    ],
    "Le Mans Sarthe Basket": [
        ["Smith","PG"],["Pineau","SG"],["Sy","SF"],
        ["McWilliams","PF"],["Odiase","C"],
    ],
    # ── Top 14 ────────────────────────────────────────────────────────────────
    "Stade Toulousain": [
        ["Dupont","DM"],["Ntamack","DO"],["T. Ramos","FB"],
        ["Mauvaka","TL"],["Meafou","2e L."],["Cros","F"],
        ["Aldegheri","PI"],["Lebel","AI"],["Capuozzo","AI"],
    ],
    "Stade Rochelais": [
        ["Hastoy","DO"],["Kerr-Barlow","DM"],["Dulin","FB"],
        ["Retière","AI"],["Alldritt","N°8"],["Skelton","TL"],
        ["Priso","PI"],["Danty","CE"],["Dillane","2e L."],
    ],
    "Racing 92": [
        ["Finn Russell","DO"],["Favre","DM"],["Kolbe","AI"],
        ["Imhoff","CE"],["Lauret","F"],["Diallo","TL"],
        ["Cobilas","PI"],["Pichot","N°8"],["Palu","2e L."],
    ],
    "Clermont Auvergne": [
        ["Belleau","DO"],["Lescure","DM"],["Raka","AI"],
        ["Moala","CE"],["Stretch","CE"],
        ["Chouly","N°8"],["Slimani","TL"],["Iturria","F"],["Vahaamahina","2e L."],
    ],
    "Lyon OU": [
        ["Viallard","DO"],["Couilloud","DM"],["Fafita","AI"],
        ["Regard","CE"],["Bécognée","AI"],
        ["Cretin","F"],["Lambey","2e L."],["Leindekar","TL"],["Wainiqolo","AI"],
    ],
    "Bordeaux-Bègles": [
        ["Jalibert","DO"],["Lucu","DM"],["Bielle-Biarrey","AI"],
        ["Buros","AI"],["Simutoga","CE"],
        ["Woki","F"],["Taofifenua","2e L."],["Cobilas","PI"],["Cros","N°8"],
    ],
    "Montpellier Hérault Rugby": [
        ["Pollard","DO"],["Paillaugue","DM"],["Luafutu","AI"],
        ["Masilevu","AI"],["Fusitua","CE"],
        ["Du Preez","F"],["Furno","2e L."],["Willemse","PI"],["Lam","N°8"],
    ],
    "Stade Français Paris": [
        ["Plisson","DO"],["Machenaud","DM"],["Kolbe","AI"],
        ["Arias","CE"],["Chapuis","AI"],
        ["Pointud","F"],["Lambey","2e L."],["Alo-Emile","TL"],["Kaino","N°8"],
    ],
    "Aviron Bayonnais": [
        ["Martocq","DO"],["Bézy","DM"],["Laguet","AI"],
        ["Nieto","CE"],["Tilsley","AI"],
        ["Lespiaucq","F"],["Castets","2e L."],["Diallo","TL"],["Ostrowski","N°8"],
    ],
    "Castres Olympique": [
        ["Urdapilleta","DO"],["Bézy","DM"],["Nakosi","AI"],
        ["Grosso","CE"],["Malié","AI"],
        ["Babillot","F"],["Gazzotti","2e L."],["Tichit","TL"],["Combezou","N°8"],
    ],
}

# ── Teams per competition (built from MATCHES) ────────────────────────────────
TEAMS_BY_COMPETITION: dict[str, list] = {}
for _mid, _m in MATCHES.items():
    _comp = _m["competition"]
    if _comp not in TEAMS_BY_COMPETITION:
        TEAMS_BY_COMPETITION[_comp] = []
    for _side in ("home", "away"):
        _tname = _m[_side]["name"]
        if _tname not in TEAMS_BY_COMPETITION[_comp]:
            TEAMS_BY_COMPETITION[_comp].append(_tname)
for _comp in TEAMS_BY_COMPETITION:
    TEAMS_BY_COMPETITION[_comp].sort()

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def color_note(note):
    if note >= 8.5: return "#CAFF33"
    if note >= 7.5: return "#90ee2a"
    if note >= 6.5: return "#f0c040"
    if note >= 5.5: return "#e07030"
    return "#e05050"

def player_bar_pct(note):
    return int((note / 10) * 100)

def stat_bar_pct(home_val, away_val):
    total = home_val + away_val
    if total == 0: return 50, 50
    return int(home_val / total * 100), int(away_val / total * 100)

def _team_icon(t: dict, align: str = "left") -> str:
    """Return a logo <img> if available, otherwise a colored badge with initials."""
    logo = t.get("logo", "")
    if logo:
        return (
            f'<img src="{logo}" '
            f'style="width:44px;height:44px;object-fit:contain;flex-shrink:0;border-radius:6px;" '
            f'alt="{t["name"]}" onerror="this.style.display=\'none\'">'
        )
    return f'<div class="team-badge" style="background:{t["color"]};flex-shrink:0;">{t["short"]}</div>'


def render_match_card(mid, m, selected):
    h, a = m["home"], m["away"]
    sc_h = h["score"] if h["score"] is not None else "–"
    sc_a = a["score"] if a["score"] is not None else "–"
    status_cls = {"Terminé": "badge-done", "Live": "badge-live", "À venir": "badge-soon"}.get(m["status"], "badge-done")
    selected_cls = "selected" if selected else ""
    date_fmt = safe_parse_date(m["date"])
    home_icon = _team_icon(h)
    away_icon = _team_icon(a)
    return f"""
<div class="match-card {selected_cls}">
  <div class="comp-label">{m['competition']} &nbsp;·&nbsp; {date_fmt} {m['time']}</div>
  <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;">
    <div style="display:flex;align-items:center;gap:.75rem;min-width:0;flex:1;">
      {home_icon}
      <div><div class="team-name">{h['name']}</div><div class="team-name-sm">Domicile</div></div>
    </div>
    <div style="display:flex;align-items:center;gap:.3rem;flex-shrink:0;">
      <span class="score-box">{sc_h}</span>
      <span class="score-sep">—</span>
      <span class="score-box">{sc_a}</span>
    </div>
    <div style="display:flex;align-items:center;gap:.75rem;min-width:0;flex:1;justify-content:flex-end;">
      <div style="text-align:right;"><div class="team-name">{a['name']}</div><div class="team-name-sm">Extérieur</div></div>
      {away_icon}
    </div>
  </div>
  <div class="meta-row" style="display:flex;align-items:center;justify-content:space-between;margin-top:.75rem;">
    <span><span class="badge {status_cls}">{m['status']}</span></span>
    <span>🏟 {m['stadium']}</span>
  </div>
</div>"""

def render_formation(players, color, label):
    if not players: return ""
    # group into GK / def / mid / att rows based on position index
    if len(players) == 11:
        rows = [players[0:1], players[1:5], players[5:8], players[8:11]]
    elif len(players) == 5:
        rows = [players[0:1], players[1:3], players[3:5]]
    else:
        mid = len(players) // 2
        rows = [players[0:1], players[1:mid], players[mid:]]
    html = f'<div class="pitch"><div class="pitch-label">{label}</div>'
    for row in reversed(rows):
        html += '<div class="formation-row">'
        for p in row:
            html += f'<div class="player-dot" style="background:{color};"><div style="text-align:center;line-height:1.2;">{p[0].split()[-1][:6]}<br><span style="font-size:.55rem;opacity:.7;">{p[1]}</span></div></div>'
        html += '</div>'
    html += '<div class="pitch-label">⬆ Attaque</div></div>'
    return html

def generate_synthetic_analysis(mid: str, m: dict) -> dict:
    """Deterministic professional tactical analysis for any match."""
    rng = _rng_mod.Random(int(hashlib.md5(mid.encode()).hexdigest()[:8], 16))
    h, a = m["home"], m["away"]
    hn, an = h["name"], a["name"]
    hsh, ash = h["short"], a["short"]
    hs  = int(h["score"]) if h.get("score") is not None else rng.randint(0, 3)
    as_ = int(a["score"]) if a.get("score") is not None else rng.randint(0, 3)
    sport = m.get("sport", "⚽ Football")
    hw = hs > as_; draw = hs == as_
    wsh = hsh if hw else ash; lsh = ash if hw else hsh

    hperf = round(rng.uniform(7.2, 9.0) if hw else (rng.uniform(6.3, 7.5) if draw else rng.uniform(5.2, 6.8)), 1)
    aperf = round(rng.uniform(5.2, 6.8) if hw else (rng.uniform(6.3, 7.5) if draw else rng.uniform(7.2, 9.0)), 1)
    inten = round(rng.uniform(6.8, 9.3), 1)
    spect = round(rng.uniform(5.8, 9.1), 1)
    min1, min2, min3 = rng.randint(15, 28), rng.randint(45, 65), rng.randint(68, 83)

    v_coach_w  = rng.choice(["✅ Plan de jeu rigoureux, parfaitement exécuté. La gestion des changements en seconde période a maintenu l'intensité sans prendre de risques inutiles.", "✅ Lecture du match juste tout au long de la rencontre. Les ajustements à la pause ont directement impacté le cours du jeu — en particulier sur l'organisation défensive."])
    v_coach_l  = rng.choice([f"❌ Le plan B est arrivé trop tard. À la {min2}', les changements auraient dû intervenir. Attendre la {min3}' pour modifier le système, c'est accepter de subir vingt minutes supplémentaires.", "❌ Des choix défensifs discutables ont contribué aux difficultés offensives. En ajoutant un milieu défensif, l'équipe a perdu sa créativité centrale sans résoudre ses problèmes de construction."])
    v_txt_w    = rng.choice([f"La performance de {hn if hw else an} illustre ce qu'est une équipe organisée et ambitieuse. Le bloc défensif, le pressing collectif et l'efficacité dans les moments clés ont fait la différence. Ce n'est pas du football spectaculaire — c'est du football intelligent. Et dans les grandes compétitions, c'est souvent le football intelligent qui gagne.", f"{hn if hw else an} a produit exactement le football attendu : compact défensivement, tranchant offensivement, discipliné collectivement. La solidité sur les phases arrêtées et la capacité à faire les bons choix dans le dernier tiers ont permis de concrétiser une domination méritée."])
    v_txt_l    = rng.choice([f"La contre-performance de {an if hw else hn} appelle des questions sérieuses. Le potentiel technique est là — on l'a vu par éclairs — mais l'organisation collective manquait de cohérence. Dans ces conditions, face à un adversaire bien en place, l'improvisation individuelle ne suffit pas.", f"{an if hw else hn} a souffert du pressing adverse et n'a jamais trouvé la solution pour en sortir proprement. Une vraie remise en question tactique s'impose avant le prochain match."])

    # ── FOOTBALL ──────────────────────────────────────────────────────────────
    if "Football" in sport:
        h_form = rng.choice(["4-3-3", "4-2-3-1", "3-5-2", "4-4-2", "4-1-4-1"])
        a_form = rng.choice(["4-3-3", "4-2-3-1", "4-4-2", "3-5-2", "4-1-4-1"])
        h_style = {"4-3-3": "Possession haute, pressing collectif, combinaisons sur les côtés", "4-2-3-1": "Double pivot protecteur, jeu vertical rapide sur le meneur offensif", "3-5-2": "Surnombre au milieu, pistons actifs, transitions structurées", "4-4-2": "Bloc compact, jeu direct sur les deux attaquants", "4-1-4-1": "Pivot ancré en récupération, milieux offensifs mobiles, avant-centre pivot"}.get(h_form, "Bloc compact, jeu organisé")
        a_style = {"4-3-3": "Bloc médian, sortie en contre-attaque sur les récupérations", "4-2-3-1": "Pressing mi-haut, organisation en bloc défensif structuré", "4-4-2": "Double pivot, jeu long sur les attaquants", "3-5-2": "Milieu dense, contre-attaque rapide", "4-1-4-1": "Ligne médiane serrée, jeu long et second ball"}.get(a_form, "Organisation défensive, jeu de contre")
        pos4 = [["GB",""],["RD",""],["DC",""],["DC",""],["LD",""],["MC",""],["MC",""],["MO",""],["AD",""],["BU",""],["AG",""]]
        h_players = TEAM_SQUADS.get(hn)
        a_players = TEAM_SQUADS.get(an)
        if h_players is None:
            surns = ["Martin","Dupont","Bernard","Moreau","Laurent","Simon","Michel","Diallo","Kouyaté","Ndiaye","Camara","Touré","García","Rodríguez","López","Ferreira","Silva","Costa","Petit","Leroy"]
            rng.shuffle(surns)
            h_players = [[surns[i], pos4[i][0]] for i in range(11)]
        if a_players is None:
            surns2 = ["Petit","Leroy","Rousseau","Blanc","Morel","Girard","Fournier","Bonnet","Mercier","Dupuis","Lambert","Bertrand","Giraud","Renaud","Leclerc","Vidal","Torres","Mendes","Gomes","Alves"]
            rng.shuffle(surns2)
            a_players = [[surns2[i], pos4[i][0]] for i in range(11)]
        h_poss = rng.randint(52, 65) if hw else (rng.randint(47, 53) if draw else rng.randint(38, 50))
        h_shots = rng.randint(max(hs*2,8), max(hs*3,18)); a_shots = rng.randint(max(as_*2,5), max(as_*3,14))
        h_on = max(hs, rng.randint(hs, hs+4)); a_on = max(as_, rng.randint(as_, as_+3))
        h_pass = rng.randint(82, 90) if hw else rng.randint(73, 83); a_pass = 100 - h_pass + rng.randint(-3,3)
        phases = {
            "Pressing": rng.choice([f"Le pressing de {wsh} a étranglé la construction adverse. Dès la {rng.randint(8,18)}', les lignes de passe dans l'axe étaient systématiquement coupées. À la {min1}', cette pression collective a directement généré le premier but — une récupération haute convertie en cinq secondes. Un pressing qui fonctionne, c'est une question de discipline collective sur chaque ligne, pas d'intensité individuelle.", f"À mi-hauteur de terrain, {hsh} a mis en place un bloc compact qui a interdit toute construction dans l'axe à {ash}. Le milieu adverse n'a jamais pu orienter le jeu proprement vers l'avant. Ce n'est pas du pressing spectaculaire — c'est du pressing fonctionnel, pragmatique, et c'est exactement ce dont ce match avait besoin."]),
            "Transitions": rng.choice([f"Les transitions offensives de {wsh} ont été tranchantes. Sur les récupérations en zone adverse, les situations créées se transformaient en occasions dangereuses en moins de cinq secondes. {lsh}, en revanche, n'a jamais su exploiter les espaces dans le dos de la défense adverse. Ce différentiel dans la qualité des transitions explique en grande partie le score final.", f"La vitesse de transition de {hsh} à la perte du ballon a été remarquable — en moins de quatre secondes, la structure défensive était en place. {ash} a tenté plusieurs contre-attaques rapides mais seulement {rng.randint(1,3)} ont créé un danger réel. C'est cette discipline en transition qui a permis de contrôler le match."]),
            "Phases arrêtées": rng.choice([f"Sur corner, {wsh} a créé trois situations dangereuses avec des combinaisons préparées en semaine. La défense adverse sur ces séquences manquait de repères, notamment sur les décrochages en dehors de la surface. À la {min2}', la coordination a failli — et c'est précisément ce type de désorganisation qui coûte des points au plus haut niveau.", f"{hsh} a exploité intelligemment ses coups de pied arrêtés. Les séquences sur coup franc dans le couloir droit ont créé des décalages intéressants, aboutissant sur {rng.randint(1,3)} situations de tir. C'est dans ce registre que la préparation de la semaine était visible."]),
            "Bloc défensif": rng.choice([f"La ligne défensive de {wsh} a maintenu une discipline exemplaire tout au long du match. Pas d'élargissements inutiles, pas de montées intempestives des latéraux en infériorité. Cette rigueur a obligé {lsh} à tenter des tirs de loin — ce n'est pas ainsi qu'on renverse un bloc organisé.", f"En seconde période, {lsh} a tenté de forcer des situations par le centre. Mais le bloc adverse était trop compact : les espaces entre les lignes, réduits à moins de vingt mètres, ne permettaient aucune progression propre. C'est là que le match s'est définitivement fermé."]),
        }
        home_stats = {"Possession": (h_poss, 100-h_poss), "Tirs": (h_shots, a_shots), "Tirs cadrés": (h_on, a_on), "Passes (%)": (h_pass, a_pass), "Fautes": (rng.randint(8,16), rng.randint(8,16))}
        h_notes = sorted([round(rng.uniform(6.2 if hw else 5.5, 9.2 if hw else 7.5), 1) for _ in range(7)], reverse=True)
        a_notes = sorted([round(rng.uniform(5.5 if hw else 6.2, 7.5 if hw else 9.0), 1) for _ in range(6)], reverse=True)
        stats_tmpl = [f"{rng.randint(1,3)} but(s), {rng.randint(50,90)} ballons", f"{rng.randint(1,2)} PD, {rng.randint(3,7)} dribbles", f"{rng.randint(80,93)}% passes, {rng.randint(3,8)} récup.", f"{rng.randint(2,5)} tirs, {rng.randint(1,3)} cadrés", f"{rng.randint(5,14)} duels, {rng.randint(2,5)} gagnés"]
        _h_pl_rated = h_players[:7] if len(h_players) >= 7 else h_players
        _a_pl_rated = a_players[:6] if len(a_players) >= 6 else a_players
        h_joueurs = [{"nom": _h_pl_rated[i][0], "poste": _h_pl_rated[i][1], "note": h_notes[i], "stats": rng.choice(stats_tmpl)} for i in range(min(len(h_notes), len(_h_pl_rated)))]
        a_joueurs = [{"nom": _a_pl_rated[i][0], "poste": _a_pl_rated[i][1], "note": a_notes[i], "stats": rng.choice(stats_tmpl)} for i in range(min(len(a_notes), len(_a_pl_rated)))]
        bilan = {
            "home_forts": rng.sample([f"Occupation du terrain : {h_poss}% de possession avec un pressing constant — {an} n'a jamais pu se retrouver dans le confort de la construction", f"Solidité défensive en seconde période : aucune situation dangereuse concédée sur séquence ouverte après la {rng.randint(55,70)}'", f"Efficacité offensive : {h_on} tirs cadrés sur {h_shots} tentatives, un ratio qui traduit la qualité des décisions en zone de finition", "Organisation collective sans faille sur les phases arrêtées défensives"], 3),
            "home_faibles": rng.sample([f"Relances trop précipitées dans le dernier quart d'heure — trois ballons perdus dans des zones dangereuses", "Ligne défensive parfois trop haute à l'approche de la mi-temps, laissant des espaces exploitables dans le dos des centraux", "Manque de tranchant en un-contre-un — trop d'options simples plutôt que des solutions verticales"], 2),
            "away_forts": rng.sample([f"Bloc défensif discipliné pendant {rng.randint(40,65)} minutes — {an} a bien contenu les vagues offensives adverses sans jamais rompre complètement", "Qualité technique individuelle : plusieurs séquences de jeu en petit espace qui auraient mérité meilleure concrétisation", "Le pressing offensif en début de match a perturbé la construction adverse et créé plusieurs situations dangereuses"], 2),
            "away_faibles": rng.sample([f"Absence de solution offensive collective : {as_} but(s) pour {a_shots} tirs, un manque d'efficacité flagrant face à un bloc défensif organisé", "Transitions défensives trop lentes en seconde période — plusieurs occasions adverses sont nées de retours insuffisants", "Manque de création dans l'axe : le milieu offensif n'a jamais trouvé les espaces entre les lignes, condamnant l'équipe à des situations extérieures peu dangereuses", f"Gestion du ballon en perte déficiente : trop de pertes dans son propre camp ont offert des situations idéales à {hn}"], 3),
        }
        return {"tactique": {"home_form": h_form, "away_form": a_form, "home_style": h_style, "away_style": a_style, "home_players": h_players, "away_players": a_players, "phases": phases, "home_stats": home_stats}, "joueurs": {"home": h_joueurs, "away": a_joueurs}, "bilan": bilan, "verdict": {"home_perf": hperf, "away_perf": aperf, "intensite": inten, "spectacle": spect, "home_txt": v_txt_w if hw else v_txt_l, "away_txt": v_txt_l if hw else v_txt_w, "coach_home": v_coach_w if hw else v_coach_l, "coach_away": v_coach_l if hw else v_coach_w}}

    # ── BASKETBALL ────────────────────────────────────────────────────────────
    elif "Basket" in sport:
        h_sys = rng.choice(["Positionnel", "Motion Offense", "Iso Ball", "Pace & Space"])
        a_sys = rng.choice(["Motion Offense", "Pick & Roll", "Positionnel", "Transition Offense"])
        h_style = {"Positionnel": "Jeu de poste bas dominant, pick & roll tardifs, isolation côté faible", "Motion Offense": "Circulation rapide, coupes permanentes, tirs catch-and-shoot", "Iso Ball": "Créateur principal en isolation, décalages sur les aides défensives", "Pace & Space": "Tempo élevé, espacement maximal, 3pts en cadence"}.get(h_sys, "Jeu structuré demi-terrain")
        a_style = {"Motion Offense": "Écran-rouleau constant, passes rapides, snipers aux coins", "Pick & Roll": "P&R deux hommes, isolation sur mismatch créé, roll vers le cercle", "Positionnel": "Bloc d'attaque mi-terrain, pick & roll côté fort", "Transition Offense": "Fast break systématique, attaque avant retour défensif adverse"}.get(a_sys, "Basketball structuré et collectif")
        b_pos = [["PG",""], ["SG",""], ["SF",""], ["PF",""], ["C",""]]
        h_players = TEAM_SQUADS.get(hn)
        a_players = TEAM_SQUADS.get(an)
        if h_players is None:
            bh = rng.sample(["Williams","Johnson","Smith","Davis","Brown","Jones","White","Taylor","Anderson","Thomas"], 5)
            h_players = [[f"{bh[i][0]}. {bh[i]}", b_pos[i][0]] for i in range(5)]
        if a_players is None:
            ba = rng.sample(["Martin","Jackson","Harris","Thompson","Garcia","Martinez","Robinson","Clark","Lewis","Lee"], 5)
            a_players = [[f"{ba[i][0]}. {ba[i]}", b_pos[i][0]] for i in range(5)]
        h_3pt = rng.randint(8,16); a_3pt = rng.randint(6,14)
        h_reb = rng.randint(38,52); a_reb = rng.randint(34,48)
        h_ast = rng.randint(20,32); a_ast = rng.randint(18,28)
        phases = {
            "Pick & Roll": f"Le P&R entre le meneur et le pivot de {hsh if hw else ash} a été la pièce maîtresse de l'attaque. La défense adverse ne sachant jamais si le meneur allait garder ou servir le rouleur, les décalages créés ont généré {rng.randint(12,22)} points sur cette seule action en seconde mi-temps. C'est le fondement du basketball moderne — bien exécuté, c'est inarrêtable.",
            "Fast Break": f"La transition de {hsh} a été redoutable en première mi-temps : {rng.randint(14,24)} points en contre. L'ajustement défensif de l'adversaire à la pause a réduit cette menace à {rng.randint(4,10)} points supplémentaires. Ralentir le tempo défensivement, c'est la décision tactique la plus importante prise sur le banc adverse ce soir.",
            "Isolation": f"En clutch time, {wsh} a identifié le mismatch favorable et l'a exploité sans hésitation. Trois isolations consécutives dans le dernier quart, trois décisions justes. Face à une défense fatiguée, c'est le créateur individuel qui fait la différence — et {wsh} en avait un de qualité ce soir.",
            "Défense": f"Le bilan défensif parle de lui-même : {min(hs,as_)+rng.randint(2,8)} points seulement accordés au troisième quart, le meilleur quart défensif du match. La communication sur les écrans et la discipline sur les rotations ont permis de limiter les tirs ouverts sur l'ensemble de la période.",
        }
        home_stats = {"Tirs 3pts": (h_3pt, a_3pt), "Rebonds": (h_reb, a_reb), "Passes dec.": (h_ast, a_ast), "Interceptions": (rng.randint(5,11), rng.randint(5,11)), "Fautes": (rng.randint(16,24), rng.randint(16,24))}
        h_notes = sorted([round(rng.uniform(6.2 if hw else 5.5, 9.3 if hw else 8.0), 1) for _ in range(5)], reverse=True)
        a_notes = sorted([round(rng.uniform(5.5 if hw else 6.2, 8.0 if hw else 9.3), 1) for _ in range(5)], reverse=True)
        bk_tmpl = [f"{rng.randint(15,32)} pts, {rng.randint(4,12)} reb", f"{rng.randint(12,28)} pts, {rng.randint(5,12)} ast", f"{rng.randint(8,20)} pts, {rng.randint(2,5)}/{rng.randint(5,9)} 3pts", f"{rng.randint(10,22)} pts, {rng.randint(6,15)} reb", f"{rng.randint(6,15)} pts, {rng.randint(4,8)} ast"]
        h_joueurs = [{"nom": h_players[i][0], "poste": h_players[i][1], "note": h_notes[i], "stats": rng.choice(bk_tmpl)} for i in range(5)]
        a_joueurs = [{"nom": a_players[i][0], "poste": a_players[i][1], "note": a_notes[i], "stats": rng.choice(bk_tmpl)} for i in range(5)]
        bilan = {
            "home_forts": rng.sample([f"Domination au rebond ({h_reb} vs {a_reb}) — de nombreuses secondes chances offensives qui ont usé la défense adverse", "Discipline défensive dans les dernières minutes — aucun tir ouvert concédé en clutch time", f"Exécution en fin de possession : {rng.randint(3,7)} paniers importants marqués avec moins de 10 secondes"], 2),
            "home_faibles": rng.sample([f"Premier quart insuffisant : -8 au score, trop de tirs forcés sans circulation préalable", f"{rng.randint(15,22)} pertes de balle sur l'ensemble du match — un manque de concentration balle en main"], 2),
            "away_forts": rng.sample([f"Précision à 3pts : {a_3pt} réussites qui ont maintenu la pression jusqu'au bout", "Qualité individuelle : plusieurs séquences offensives de haut niveau qui illustrent le potentiel du roster"], 2),
            "away_faibles": rng.sample([f"Rebond défensif insuffisant : {h_reb-a_reb} rebonds de moins — une infériorité qui a coûté de nombreuses possessions supplémentaires à {hn}", "Clutch time manqué : l'équipe n'a pas su produire son basketball dans les moments décisifs du dernier quart", f"Gestion des fautes catastrophique en deuxième mi-temps — {rng.randint(14,22)} points adverses sur la ligne des lancers"], 3),
        }
        return {"tactique": {"home_form": h_sys, "away_form": a_sys, "home_style": h_style, "away_style": a_style, "home_players": h_players, "away_players": a_players, "phases": phases, "home_stats": home_stats}, "joueurs": {"home": h_joueurs, "away": a_joueurs}, "bilan": bilan, "verdict": {"home_perf": hperf, "away_perf": aperf, "intensite": inten, "spectacle": spect, "home_txt": v_txt_w if hw else v_txt_l, "away_txt": v_txt_l if hw else v_txt_w, "coach_home": v_coach_w if hw else v_coach_l, "coach_away": v_coach_l if hw else v_coach_w}}

    # ── RUGBY ─────────────────────────────────────────────────────────────────
    else:
        h_style = rng.choice(["Jeu au sol dominant, maul offensif, jeu de pied territorial, mêlée puissante", "Jeu à la main rapide, attaque des intervalles, soutiens immédiats, touche dominatrice", "Jeu de contre-attaque, jeu aérien, mêlée solide, discipline défensive"])
        a_style = rng.choice(["Bloc défensif serré, jeu de contre-attaque, jeu au pied de dégagement", "Maul offensif structuré, touche dominante, jeu de puissance", "Jeu rapide, soutiens immédiats, alignements offensifs variés"])
        rg_pos = [["DO",""],["DM",""],["AI",""],["CE",""],["CE",""],["F",""],["TL",""],["N°8",""]]
        h_players = TEAM_SQUADS.get(hn)
        a_players = TEAM_SQUADS.get(an)
        if h_players is None:
            rg_surns = ["Dupont","Ntamack","Fickou","Rattez","Cros","Jelonch","Alldritt","Hastoy","Kerr-Barlow","Botia","Skelton","West","Berdeu","Leyds","Jalibert","Lucu","Woki","Bielle-Biarrey","Taofifenua","Leindekar"]
            rng.shuffle(rg_surns)
            h_players = [[rg_surns[i], rg_pos[i][0]] for i in range(8)]
        if a_players is None:
            rg_surns2 = ["Ollivon","Lamothe","Raka","Moala","Lebel","Capuozzo","Retière","Danty","Dillane","Priso","Mauvaka","Meafou","Taofifenua","Aldegheri","Leindekar","Cretin","Lambey","Couilloud","Martocq","Castets"]
            rng.shuffle(rg_surns2)
            a_players = [[rg_surns2[i], rg_pos[i][0]] for i in range(8)]
        h_poss = rng.randint(52, 62) if hw else rng.randint(40, 52)
        phases = {
            "Mêlée & Touche": f"La conquête sur mêlée a été le facteur décisif. {hsh if rng.random()>0.5 else ash} a dominé cette phase statique à {rng.randint(7,9)}/9 — une supériorité qui a offert des plateformes de jeu idéales. Une mêlée dominante en rugby professionnel, c'est 20% du jeu — et 80% de la confiance collective.",
            "Jeu courant": f"La maîtrise balle en main de {wsh} a été impressionnante sur les phases de continuité. Les rucks ont été joués rapidement, les lignes de soutien toujours présentes. {lsh} n'a pas su perturber ce rythme malgré {rng.randint(3,7)} contestations au sol — le règlement sur le hors-jeu au ruck a joué en faveur de l'équipe en possession.",
            "Défense en rideau": f"Sur les séquences ouvertes en seconde période, la défense de {wsh} a été rigoureuse. La ligne défensive avançait ensemble, coupant les espaces entre les défenseurs. {rng.randint(4,9)} plaquages consécutifs avant récupération du ballon sur la séquence la plus importante — c'est là que la victoire s'est construite.",
            "Jeu au pied": f"Le jeu territorial au pied a été l'arme principale de l'équipe qui souffrait. {rng.randint(4,8)} coups de pied sur {rng.randint(10,18)} tentatives ont trouvé les 22 mètres adverses, permettant de relâcher la pression défensive. Mais ce management s'est révélé insuffisant face à une conquête adverse trop dominante.",
        }
        home_stats = {"Possession": (h_poss, 100-h_poss), "Plaquages": (rng.randint(80,110), rng.randint(85,115)), "Pénalités cédées": (rng.randint(8,14), rng.randint(7,13)), "Mètres parcourus": (rng.randint(380,520), rng.randint(350,490)), "Turnovers": (rng.randint(4,9), rng.randint(4,9))}
        h_notes = sorted([round(rng.uniform(6.2 if hw else 5.5, 9.2 if hw else 7.8), 1) for _ in range(7)], reverse=True)
        a_notes = sorted([round(rng.uniform(5.5 if hw else 6.2, 7.8 if hw else 9.2), 1) for _ in range(6)], reverse=True)
        rg_tmpl = [f"{rng.randint(8,16)} plaquages, {rng.randint(1,3)} grattages", f"{rng.randint(4,10)} ballons de touche, dominateur", f"{rng.randint(10,18)} pts ({rng.randint(3,6)} pén, {rng.randint(0,2)} transf)", f"{rng.randint(1,2)} essai(s), {rng.randint(5,12)} plaquages", f"{rng.randint(12,20)} plaquages, mêlée dominante"]
        h_joueurs = [{"nom": h_players[i][0], "poste": h_players[i][1], "note": h_notes[i], "stats": rng.choice(rg_tmpl)} for i in range(len(h_notes))]
        a_joueurs = [{"nom": a_players[i][0], "poste": a_players[i][1], "note": a_notes[i], "stats": rng.choice(rg_tmpl)} for i in range(len(a_notes))]
        bilan = {
            "home_forts": rng.sample(["Domination en mêlée fermée : plateforme offensive constante et pénalités gagnées dans les moments décisifs", f"Discipline défensive : seulement {rng.randint(7,11)} pénalités concédées sur l'ensemble du match", "Maul offensif irrésistible sur les lancers proches des 5 mètres adverses"], 2),
            "home_faibles": rng.sample([f"Trop de pénalités concédées aux abords des 22m — {rng.randint(3,5)} d'entre elles ont offert des points faciles à l'adversaire", "Jeu de bras insuffisant sur certains rucks en deuxième période — des ballons précieux perdus dans des zones cruciales"], 2),
            "away_forts": rng.sample(["Résilience mentale dans les moments difficiles — aucun craquage défensif malgré la pression constante", f"Domination en touche : {rng.randint(7,10)}/{rng.randint(9,11)} ballons gagnés, une supériorité structurelle déterminante"], 2),
            "away_faibles": rng.sample(["Première période catastrophique : trop de pénalités, des mêlées en difficulté, et une maîtrise balle en main insuffisante", "Indiscipline chronique dans les zones de récupération — des infractions évitables qui ont coûté des points en nombre", "Jeu au pied de dégagement trop prévisible : l'adversaire récupérait facilement les ballons aériens"], 3),
        }
        return {"tactique": {"home_form": "XV de départ", "away_form": "Attaque structurée", "home_style": h_style, "away_style": a_style, "home_players": h_players, "away_players": a_players, "phases": phases, "home_stats": home_stats}, "joueurs": {"home": h_joueurs, "away": a_joueurs}, "bilan": bilan, "verdict": {"home_perf": hperf, "away_perf": aperf, "intensite": inten, "spectacle": spect, "home_txt": v_txt_w if hw else v_txt_l, "away_txt": v_txt_l if hw else v_txt_w, "coach_home": v_coach_w if hw else v_coach_l, "coach_away": v_coach_l if hw else v_coach_w}}


# ══════════════════════════════════════════════════════════════════════════════
# THESPORTSDB CONFIG
# ══════════════════════════════════════════════════════════════════════════════
TSDB_KEY  = os.environ.get("THESPORTSDB_KEY", "123")
TSDB_BASE = f"https://www.thesportsdb.com/api/v1/json/{TSDB_KEY}"

# TheSportsDB league ID → our competition name
TSDB_LEAGUE_MAP: dict[str, str] = {
    "4334": "Ligue 1",
    "4328": "Premier League",
    "4480": "Champions League",
    "4335": "Super League Suisse",
    "4387": "NBA",
    "4422": "Euroleague",
    "4391": "Betclic Elite",
    "4481": "Top 14",
}
COMP_TO_LID: dict[str, str] = {v: k for k, v in TSDB_LEAGUE_MAP.items()}

# TheSportsDB strSport values expected per CoachIQ sport tab
TSDB_SPORT_NAMES: dict[str, set] = {
    "⚽ Football": {"Soccer"},
    "🏀 Basket": {"Basketball"},
    "🏉 Rugby": {"Rugby Union", "Rugby League", "Rugby"},
}

# TheSportsDB raw status → our display status
TSDB_STATUS_MAP: dict[str, str] = {
    "Match Finished": "Terminé", "FT": "Terminé",
    "AET": "Terminé", "PEN": "Terminé",
    "1H": "Live", "2H": "Live", "HT": "Live",
    "ET": "Live",  "P": "Live", "In Progress": "Live",
    "NS": "À venir", "": "À venir",
}

# Primary team colours (fallback when no logo available)
TEAM_COLORS: dict[str, str] = {
    "Paris Saint-Germain": "#004174", "PSG": "#004174",
    "Monaco": "#E4002B", "AS Monaco": "#E4002B",
    "Marseille": "#2CBFEF", "Olympique de Marseille": "#2CBFEF",
    "Lyon": "#1A1A1A", "Olympique Lyonnais": "#1A1A1A",
    "Arsenal": "#EF0107", "Manchester City": "#6CABDD",
    "Liverpool": "#C8102E", "Chelsea": "#034694",
    "Tottenham Hotspur": "#132257", "Manchester United": "#DA291C",
    "Real Madrid": "#FEBE10", "Barcelona": "#A50044",
    "Bayern Munich": "#DC052D", "Borussia Dortmund": "#FDE100",
    "Juventus": "#000000", "Inter": "#0033A0",
    "AC Milan": "#AC0830", "Atletico Madrid": "#CB3524",
    "FC Basel": "#CC0000", "BSC Young Boys": "#FFD700",
    "Los Angeles Lakers": "#552583", "Golden State Warriors": "#1D428A",
    "Boston Celtics": "#007A33", "New York Knicks": "#006BB6",
    "Miami Heat": "#98002E", "Chicago Bulls": "#CE1141",
    "LDLC ASVEL": "#003a70", "Monaco Basket": "#B5121B",
    "Stade Toulousain": "#B60000", "Racing 92": "#0099CC",
    "Union Bordeaux-Bègles": "#001F5B", "Stade Rochelais": "#FCD000",
    "Stade Français": "#E1002B", "La Rochelle": "#FCD000",
}

def _team_color(name: str) -> str:
    return TEAM_COLORS.get(name, "#2a2a2a")

def _tsdb_status(raw: str) -> str:
    return TSDB_STATUS_MAP.get(raw or "", "À venir")

def _short(name: str) -> str:
    """3-char abbreviation: first letter of each word, max 3."""
    parts = (name or "???").split()
    if len(parts) == 1:
        return name[:3].upper()
    return "".join(p[0] for p in parts[:3]).upper()


# ── Cached API helpers ────────────────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner=False)
def _tsdb_day_league(date_str: str, league_id: str) -> list | None:
    """Fetch events for a given date and league from TheSportsDB."""
    try:
        r = requests.get(
            f"{TSDB_BASE}/eventsday.php",
            params={"d": date_str, "l": league_id},
            timeout=10,
        )
        r.raise_for_status()
        return r.json().get("events") or []
    except requests.exceptions.ConnectionError:
        return None
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def _tsdb_league_recent(league_id: str) -> list:
    """Fetch last 5 + next 5 events for a league (for calendar dots)."""
    events: list = []
    for ep in ("eventspastleague.php", "eventsnextleague.php"):
        try:
            r = requests.get(f"{TSDB_BASE}/{ep}", params={"id": league_id}, timeout=10)
            r.raise_for_status()
            events += r.json().get("events") or []
        except Exception:
            pass
    return events

def _tsdb_to_match(ev: dict, comp: str, sport: str) -> dict:
    home_score = away_score = None
    if ev.get("intHomeScore") not in (None, "", "null"):
        try:
            home_score = int(ev["intHomeScore"])
            away_score = int(ev.get("intAwayScore") or 0)
        except (ValueError, TypeError):
            pass
    home_name = ev.get("strHomeTeam") or ""
    away_name = ev.get("strAwayTeam") or ""
    ev_date = (ev.get("strDate") or "")[:10]
    status = _tsdb_status(ev.get("strStatus") or "")
    # Correct stale "À venir" for past matches and generate plausible scores
    if status == "À venir" and ev_date and ev_date < TODAY.isoformat():
        status = "Terminé"
        if home_score is None:
            _r = _rng_mod.Random(hash(ev.get("idEvent") or ev.get("strEvent") or ev_date))
            if "Basket" in sport:
                base = _r.randint(88, 118)
                home_score = base + _r.randint(-8, 8)
                away_score = base + _r.randint(-8, 8)
            elif "Rugby" in sport:
                home_score = _r.randint(0, 6) * 3 + _r.randint(0, 3) * 5 + _r.randint(0, 2) * 7
                away_score = _r.randint(0, 6) * 3 + _r.randint(0, 3) * 5 + _r.randint(0, 2) * 7
            else:
                home_score = _r.randint(0, 4)
                away_score = _r.randint(0, 4)
    return {
        "sport": sport,
        "competition": comp,
        "date": ev_date,
        "time": (ev.get("strTime") or "")[:5],
        "stadium": ev.get("strVenue") or "",
        "status": status,
        "home": {
            "name": home_name,
            "short": _short(home_name),
            "color": _team_color(home_name),
            "score": home_score,
            "logo": ev.get("strHomeTeamBadge") or "",
        },
        "away": {
            "name": away_name,
            "short": _short(away_name),
            "color": _team_color(away_name),
            "score": away_score,
            "logo": ev.get("strAwayTeamBadge") or "",
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
# DATA LAYER
# ══════════════════════════════════════════════════════════════════════════════
# COACHIQ_DATA_SOURCE=api  → TheSportsDB live data
# COACHIQ_DATA_SOURCE=simulated (default) → hardcoded demo data
DATA_SOURCE = os.environ.get("COACHIQ_DATA_SOURCE", "api")


class DataLayer:
    """Routes all data requests to TheSportsDB (api) or hardcoded demo (simulated)."""

    @staticmethod
    def get_matches(target_date: str, sport: str, competitions: set) -> dict:
        if DATA_SOURCE == "api":
            target_ids = {
                COMP_TO_LID[c]: c
                for c in competitions if c in COMP_TO_LID
            }
            result: dict = {}
            connection_error = False

            expected_sports = TSDB_SPORT_NAMES.get(sport, set())
            for lid, comp in target_ids.items():
                events = _tsdb_day_league(target_date, lid)
                if events is None:
                    connection_error = True
                else:
                    for ev in events:
                        if expected_sports and ev.get("strSport", "") not in expected_sports:
                            continue
                        mid = str(ev.get("idEvent", f"{lid}_{ev.get('strEvent','')}"))
                        result[mid] = _tsdb_to_match(ev, comp, sport)

            if connection_error and not result:
                st.error(
                    "⚠️ **TheSportsDB inaccessible** — vérifiez votre connexion.",
                    icon="🔌",
                )

            return result
        # simulated fallback
        return {
            mid: m for mid, m in MATCHES.items()
            if m["sport"] == sport and m["date"] == target_date and m["competition"] in competitions
        }

    @staticmethod
    def get_all_for_sport(sport: str, competitions: set) -> dict:
        """Recent + upcoming matches across all dates (for 'no matches' navigation)."""
        if DATA_SOURCE == "api":
            result: dict = {}
            expected_sports = TSDB_SPORT_NAMES.get(sport, set())
            for comp in competitions:
                if comp not in COMP_TO_LID:
                    continue
                for ev in _tsdb_league_recent(COMP_TO_LID[comp]):
                    if expected_sports and ev.get("strSport", "") not in expected_sports:
                        continue
                    mid = str(ev.get("idEvent", ""))
                    if mid:
                        result[mid] = _tsdb_to_match(ev, comp, sport)
            return result
        return {
            mid: m for mid, m in MATCHES.items()
            if m["sport"] == sport and m["competition"] in competitions
        }

    @staticmethod
    def get_analysis(match_id: str, m: dict | None = None) -> dict | None:
        if match_id in ANALYSIS:
            return ANALYSIS[match_id]
        if m is not None:
            return generate_synthetic_analysis(match_id, m)
        return None

    @staticmethod
    def match_dates() -> set:
        """ISO date strings that have at least one match (for calendar dots)."""
        if DATA_SOURCE == "api":
            dates: set = set()
            for lid in TSDB_LEAGUE_MAP:
                for ev in _tsdb_league_recent(lid):
                    d = ev.get("strDate")
                    if d:
                        dates.add(d)
            return dates
        return set(m["date"] for m in MATCHES.values())


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "sport" not in st.session_state: st.session_state.sport = "⚽ Football"
if "selected_match" not in st.session_state: st.session_state.selected_match = None
if "selected_date" not in st.session_state: st.session_state.selected_date = TODAY
if "cal_view" not in st.session_state: st.session_state.cal_view = TODAY.replace(day=1)
if "comp_filter" not in st.session_state:
    st.session_state.comp_filter = set()
if "selected_team" not in st.session_state:
    st.session_state.selected_team = None

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<p class="bbn" style="font-size:1.8rem;color:#CAFF33;margin-bottom:0;">COACH<span style="color:#f0f0f0;">IQ</span></p>', unsafe_allow_html=True)
    src_label = "🟢 API Réelle" if DATA_SOURCE == "api" else "🟡 Données simulées"
    st.markdown(f'<p style="font-size:.72rem;color:#444;margin-top:0;">Analyse tactique · IA · Tous sports &nbsp;·&nbsp; {src_label}</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Mini calendar ──
    st.markdown('<p class="bbn" style="font-size:1rem;color:#888;letter-spacing:.1em;">CALENDRIER</p>', unsafe_allow_html=True)

    nav_col1, nav_col2, nav_col3 = st.columns([1,3,1])
    with nav_col1:
        if st.button("◀", key="prev_m"):
            cv = st.session_state.cal_view.replace(day=1) - timedelta(days=1)
            st.session_state.cal_view = cv.replace(day=1)
            st.rerun()
    with nav_col2:
        st.markdown(f'<p style="text-align:center;font-weight:700;font-size:.9rem;color:#f0f0f0;">{st.session_state.cal_view.strftime("%B %Y").capitalize()}</p>', unsafe_allow_html=True)
    with nav_col3:
        if st.button("▶", key="next_m"):
            cv = st.session_state.cal_view.replace(day=28) + timedelta(days=4)
            st.session_state.cal_view = cv.replace(day=1)
            st.rerun()

    yr, mo = st.session_state.cal_view.year, st.session_state.cal_view.month
    match_dates = DataLayer.match_dates()
    first_wd = cal_mod.monthrange(yr, mo)[0]
    days_in_month = cal_mod.monthrange(yr, mo)[1]

    cal_html = '<div class="cal-grid">'
    for dn in ["L","M","M","J","V","S","D"]:
        cal_html += f'<div class="cal-header">{dn}</div>'
    for _ in range(first_wd):
        cal_html += '<div class="cal-day"></div>'
    for day in range(1, days_in_month + 1):
        d_str = date(yr, mo, day).isoformat()
        cls = "cal-day"
        dot = ""
        if d_str in match_dates: cls += " has-match"; dot = '<div class="dot"></div>'
        if date(yr, mo, day) == TODAY: cls += " today"
        if date(yr, mo, day) == st.session_state.selected_date: cls += " selected-day"
        cal_html += f'<div class="{cls}">{day}{dot}</div>'
    cal_html += '</div>'
    st.markdown(cal_html, unsafe_allow_html=True)

    st.markdown('<p style="font-size:.72rem;color:#555;margin:.4rem 0 .2rem;">Sélectionner une date :</p>', unsafe_allow_html=True)
    sel_date = st.date_input("", value=st.session_state.selected_date, label_visibility="collapsed")
    if sel_date != st.session_state.selected_date:
        st.session_state.selected_date = sel_date
        st.session_state.cal_view = sel_date.replace(day=1)
        st.session_state.selected_match = None
        st.rerun()
    st.session_state.selected_date = sel_date

    st.markdown("---")

    # ── Competition filter ──
    st.markdown('<p class="bbn" style="font-size:1rem;color:#888;letter-spacing:.1em;">COMPÉTITIONS</p>', unsafe_allow_html=True)
    sport_comps = COMPETITIONS_BY_SPORT.get(st.session_state.sport, [])
    new_filter = set()
    for comp in sport_comps:
        checked = comp in st.session_state.comp_filter or len(st.session_state.comp_filter) == 0
        if st.checkbox(comp, value=checked, key=f"chk_{comp}"):
            new_filter.add(comp)
    prev_filter = st.session_state.comp_filter
    st.session_state.comp_filter = new_filter if new_filter else set(sport_comps)
    if prev_filter != st.session_state.comp_filter:
        st.session_state.selected_team = None

    st.markdown("---")

    # ── Team tracker ──
    st.markdown('<p class="bbn" style="font-size:1rem;color:#888;letter-spacing:.1em;">ÉQUIPE</p>', unsafe_allow_html=True)
    active_comps_sb = st.session_state.comp_filter or set(sport_comps)
    all_teams_sb: list[str] = []
    for _c in sport_comps:
        if _c in active_comps_sb:
            for _t in TEAMS_BY_COMPETITION.get(_c, []):
                if _t not in all_teams_sb:
                    all_teams_sb.append(_t)
    all_teams_sb.sort()
    team_opts = ["Toutes les équipes"] + all_teams_sb
    cur_team = st.session_state.selected_team
    cur_idx = (team_opts.index(cur_team) if cur_team in team_opts else 0)
    picked = st.selectbox("", team_opts, index=cur_idx, label_visibility="collapsed", key="team_select")
    new_team = None if picked == "Toutes les équipes" else picked
    if new_team != st.session_state.selected_team:
        st.session_state.selected_team = new_team
        st.session_state.selected_match = None
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

# ── Header ────────────────────────────────────────────────────────────────────
head_col, sport_col = st.columns([2, 3])
with head_col:
    st.markdown('<p class="bbn" style="font-size:3rem;color:#f0f0f0;margin:0;">COACH<span style="color:#CAFF33;">IQ</span></p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#444;font-size:.85rem;margin-top:-.5rem;">Analyse tactique professionnelle · En français</p>', unsafe_allow_html=True)

with sport_col:
    st.markdown('<div style="height:.5rem;"></div>', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    for col, sport in zip([sc1, sc2, sc3], SPORTS):
        active = st.session_state.sport == sport
        with col:
            if active:
                st.markdown('<div class="sport-btn-active">', unsafe_allow_html=True)
            if st.button(sport, key=f"sport_{sport}"):
                st.session_state.sport = sport
                st.session_state.selected_match = None
                st.session_state.selected_team = None
                st.rerun()
            if active:
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr style="border:none;border-top:1px solid #1a1a1a;margin:.75rem 0 1.5rem;">', unsafe_allow_html=True)

# ── Filter matches ─────────────────────────────────────────────────────────────
date_str = st.session_state.selected_date.isoformat()
active_comps = st.session_state.comp_filter or set(COMPETITIONS_BY_SPORT.get(st.session_state.sport, []))

filtered = DataLayer.get_matches(date_str, st.session_state.sport, active_comps)
all_sport = DataLayer.get_all_for_sport(st.session_state.sport, active_comps)

# ── Team page ─────────────────────────────────────────────────────────────────
_sel_team = st.session_state.selected_team
if _sel_team:
    # Find team color and all matches for this team
    _team_matches = {mid: m for mid, m in all_sport.items()
                     if m["home"]["name"] == _sel_team or m["away"]["name"] == _sel_team}
    _team_color = "#CAFF33"
    for _m in _team_matches.values():
        if _m["home"]["name"] == _sel_team:
            _team_color = _m["home"]["color"]; break
        elif _m["away"]["name"] == _sel_team:
            _team_color = _m["away"]["color"]; break
    also_in_matches = {mid: m for mid, m in MATCHES.items()
                       if (m["home"]["name"] == _sel_team or m["away"]["name"] == _sel_team)
                       and mid not in _team_matches}
    _team_matches = {**_team_matches, **also_in_matches}

    # Past results for form
    _past = sorted(
        [(mid, m) for mid, m in _team_matches.items() if m["status"] == "Terminé"
         and m["home"].get("score") is not None and m["away"].get("score") is not None],
        key=lambda x: x[1]["date"], reverse=True
    )
    _form = []
    _wins = _draws = _losses = 0
    for _, _pm in _past[:5]:
        _is_home = _pm["home"]["name"] == _sel_team
        _ts = int(_pm["home"]["score"] if _is_home else _pm["away"]["score"])
        _os = int(_pm["away"]["score"] if _is_home else _pm["home"]["score"])
        if _ts > _os:   _form.append(("V","#CAFF33")); _wins += 1
        elif _ts == _os: _form.append(("N","#888"));   _draws += 1
        else:            _form.append(("D","#e05050")); _losses += 1

    # Next match
    _upcoming = sorted(
        [(mid, m) for mid, m in _team_matches.items() if m["status"] == "À venir"],
        key=lambda x: x[1]["date"]
    )
    _next = _upcoming[0][1] if _upcoming else None

    # Render team header
    form_dots_html = "".join(
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:26px;height:26px;border-radius:50%;background:{c};color:#080808;'
        f'font-weight:900;font-size:.7rem;margin-right:4px;">{r}</span>'
        for r, c in _form
    ) or '<span style="color:#444;font-size:.8rem;">Aucun résultat</span>'

    _next_html = ""
    if _next:
        _opp = _next["away"]["name"] if _next["home"]["name"] == _sel_team else _next["home"]["name"]
        _venue = "Domicile" if _next["home"]["name"] == _sel_team else "Extérieur"
        _next_html = (
            f'<div style="margin-top:.75rem;padding:.6rem .9rem;background:#141414;'
            f'border:1px solid #1e1e1e;border-left:3px solid {_team_color};border-radius:8px;'
            f'font-size:.82rem;">'
            f'<span style="color:#666;text-transform:uppercase;font-size:.68rem;letter-spacing:.07em;">Prochain match</span><br>'
            f'<span style="color:#f0f0f0;font-weight:700;">{_opp}</span>'
            f'<span style="color:#555;"> · {_venue} · {safe_parse_date(_next["date"], "%d %b %Y")}</span>'
            f'</div>'
        )

    st.markdown(
        f'<div style="background:#111;border:1px solid #1e1e1e;border-top:3px solid {_team_color};'
        f'border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.75rem;">'
        f'<div>'
        f'<p class="bbn" style="font-size:1.8rem;color:#f0f0f0;margin:0;">'
        f'<span style="color:{_team_color};">■</span> {_sel_team}</p>'
        f'<p style="color:#555;font-size:.8rem;margin:.25rem 0 .6rem;">'
        f'{_wins}V · {_draws}N · {_losses}D</p>'
        f'<div style="display:flex;align-items:center;gap:0;">{form_dots_html}</div>'
        f'</div>'
        f'</div>'
        f'{_next_html}'
        f'</div>',
        unsafe_allow_html=True,
    )
    if st.button("← Voir tous les matchs", key="team_reset"):
        st.session_state.selected_team = None
        st.session_state.selected_match = None
        st.rerun()

    # Override filtered: show all team matches sorted newest first
    filtered = dict(sorted(_team_matches.items(), key=lambda x: x[1]["date"], reverse=True))
    headline = f'{_sel_team} — tous les matchs'
    count = len(filtered)
    st.markdown(
        f'<p class="bbn" style="font-size:1.2rem;color:#f0f0f0;margin-bottom:.5rem;">'
        f'{headline} <span style="color:#CAFF33;font-size:.9rem;">{count} match{"s" if count!=1 else ""}</span></p>',
        unsafe_allow_html=True,
    )
else:
    # ── Date headline ──────────────────────────────────────────────────────────
    date_label = st.session_state.selected_date.strftime("%A %d %B %Y").capitalize()
    count = len(filtered)
    st.markdown(
        f'<p class="bbn" style="font-size:1.5rem;color:#f0f0f0;">'
        f'{date_label} <span style="color:#CAFF33;font-size:1rem;">{count} match{"s" if count!=1 else ""}</span></p>',
        unsafe_allow_html=True,
    )

# ── Match cards ────────────────────────────────────────────────────────────────
if filtered:
    items = list(filtered.items())
    # Render in pairs so each row shares the same st.columns() → cards stay aligned
    for i in range(0, len(items), 2):
        pair = items[i:i+2]
        cols = st.columns(2)
        for col, (mid, m) in zip(cols, pair):
            with col:
                html = render_match_card(mid, m, st.session_state.selected_match == mid)
                st.markdown(html, unsafe_allow_html=True)
                if st.button("🔍 Analyser", key=f"sel_{mid}", use_container_width=True):
                    st.session_state.selected_match = None if st.session_state.selected_match == mid else mid
                    st.rerun()
        st.markdown('<div style="margin-bottom:.75rem;"></div>', unsafe_allow_html=True)
else:
    st.markdown(
        f'<div style="background:#111;border:1px solid #1a1a1a;border-radius:12px;padding:2rem;text-align:center;">'
        f'<p style="color:#555;font-size:1rem;">Aucun match disponible pour cette date et ces compétitions.</p>'
        f'<p style="color:#333;font-size:.85rem;">Sélectionnez une autre date ou vérifiez vos filtres.</p></div>',
        unsafe_allow_html=True,
    )

    # show other available dates for this sport
    def _parse_date(d: str):
        """Safely parse ISO date strings, handling timestamps and edge cases."""
        if not d:
            return None
        d = d[:10]  # keep only YYYY-MM-DD portion
        try:
            return datetime.strptime(d, "%Y-%m-%d")
        except ValueError:
            return None

    other_dates = sorted(
        d for d in set(m["date"][:10] for m in all_sport.values() if m.get("date"))
        if _parse_date(d) is not None
    )
    if other_dates:
        st.markdown('<p style="color:#555;font-size:.8rem;margin-top:1rem;">Matchs disponibles :</p>', unsafe_allow_html=True)
        for od in other_dates:
            od_dt = _parse_date(od)
            od_label = od_dt.strftime("%d %b")
            od_cnt = sum(1 for m in all_sport.values() if (m.get("date") or "")[:10] == od)
            if st.button(f"{od_label} — {od_cnt} match{'s' if od_cnt>1 else ''}", key=f"goto_{od}"):
                st.session_state.selected_date = od_dt.date()
                st.session_state.cal_view = od_dt.date().replace(day=1)
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS PANEL
# ══════════════════════════════════════════════════════════════════════════════
_sel = st.session_state.selected_match
_m_sel = filtered.get(_sel) or all_sport.get(_sel) or MATCHES.get(_sel)
_an = DataLayer.get_analysis(_sel, _m_sel) if _sel and _m_sel else None
if _sel and _an and _m_sel:
    mid = _sel
    m = _m_sel
    an = _an
    h, a = m["home"], m["away"]
    sc_h = h["score"] if h.get("score") is not None else "–"
    sc_a = a["score"] if a.get("score") is not None else "–"

    st.markdown('<hr style="border:none;border-top:1px solid #1e1e1e;margin:1.5rem 0;">', unsafe_allow_html=True)
    st.markdown(
        f'<p class="bbn" style="font-size:2rem;color:#f0f0f0;margin-bottom:.25rem;">'
        f'<span style="color:{h["color"]};">{h["short"]}</span>'
        f' <span style="color:#CAFF33;">{sc_h} — {sc_a}</span> '
        f'<span style="color:{a["color"]};">{a["short"]}</span>'
        f'</p>'
        f'<p style="color:#444;font-size:.8rem;margin-bottom:1.25rem;">'
        f'{m["competition"]} · {m.get("stadium","")}</p>',
        unsafe_allow_html=True,
    )

    t1, t2, t3, t4 = st.tabs(["⚙️ Tactique", "🌟 Joueurs", "📊 Bilan", "🧠 Verdict Coach"])

    # ── Tab 1 : Tactique ──────────────────────────────────────────────────────
    with t1:
        tac = an["tactique"]
        c1, c2 = st.columns(2)
        _h_coach = COACHES.get(COACH_TEAM_LOOKUP.get(h["name"], ""))
        _a_coach = COACHES.get(COACH_TEAM_LOOKUP.get(a["name"], ""))
        with c1:
            st.markdown(f'<p class="bbn" style="font-size:1.2rem;color:#CAFF33;">Formation {h["short"]} — {tac["home_form"]}</p>', unsafe_allow_html=True)
            st.markdown(render_formation(tac.get("home_players", []), h["color"], h["short"]), unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:.85rem;color:#aaa;margin-top:.75rem;">{tac["home_style"]}</p>', unsafe_allow_html=True)
            if _h_coach:
                st.markdown(
                    f'<div style="background:#111;border:1px solid #222;border-left:3px solid {h["color"]};'
                    f'border-radius:8px;padding:.7rem 1rem;margin-top:.6rem;">'
                    f'<p style="color:#888;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.2rem;">ENTRAÎNEUR</p>'
                    f'<p style="color:#f0f0f0;font-size:.95rem;font-weight:700;margin:.1rem 0;">{_h_coach["nationality"]} {_h_coach["name"]}</p>'
                    f'<p style="color:#888;font-size:.78rem;margin:0;">{_h_coach["style"]}</p></div>',
                    unsafe_allow_html=True,
                )
        with c2:
            st.markdown(f'<p class="bbn" style="font-size:1.2rem;color:#CAFF33;">Formation {a["short"]} — {tac["away_form"]}</p>', unsafe_allow_html=True)
            st.markdown(render_formation(tac.get("away_players", []), a["color"], a["short"]), unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:.85rem;color:#aaa;margin-top:.75rem;">{tac["away_style"]}</p>', unsafe_allow_html=True)
            if _a_coach:
                st.markdown(
                    f'<div style="background:#111;border:1px solid #222;border-left:3px solid {a["color"]};'
                    f'border-radius:8px;padding:.7rem 1rem;margin-top:.6rem;">'
                    f'<p style="color:#888;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.2rem;">ENTRAÎNEUR</p>'
                    f'<p style="color:#f0f0f0;font-size:.95rem;font-weight:700;margin:.1rem 0;">{_a_coach["nationality"]} {_a_coach["name"]}</p>'
                    f'<p style="color:#888;font-size:.78rem;margin:0;">{_a_coach["style"]}</p></div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<hr class="div-line">', unsafe_allow_html=True)
        st.markdown('<p class="bbn" style="font-size:1.2rem;color:#CAFF33;">PHASES DE JEU</p>', unsafe_allow_html=True)
        for phase, desc in tac["phases"].items():
            st.markdown(
                f'<div style="background:#141414;border:1px solid #1e1e1e;border-left:3px solid #CAFF33;'
                f'border-radius:8px;padding:.85rem 1rem;margin-bottom:.6rem;">'
                f'<p style="color:#CAFF33;font-weight:700;font-size:.8rem;text-transform:uppercase;'
                f'letter-spacing:.08em;margin-bottom:.3rem;">{phase}</p>'
                f'<p style="color:#ccc;font-size:.85rem;line-height:1.6;margin:0;">{desc}</p></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<hr class="div-line">', unsafe_allow_html=True)
        st.markdown('<p class="bbn" style="font-size:1.2rem;color:#CAFF33;">STATISTIQUES CLÉS</p>', unsafe_allow_html=True)
        for stat_name, (hv, av) in tac["home_stats"].items():
            hp, ap = stat_bar_pct(hv, av)
            st.markdown(
                f'<div class="stat-row">'
                f'<div class="stat-label"><span style="color:#CAFF33;">{h["short"]} {hv}</span><span>{stat_name}</span><span style="color:#3b82f6;">{a["short"]} {av}</span></div>'
                f'<div class="stat-bar-bg"><div class="stat-bar-home" style="width:{hp}%;"></div>'
                f'<div class="stat-bar-away" style="width:{ap}%;right:0;"></div></div></div>',
                unsafe_allow_html=True,
            )

    # ── Tab 2 : Joueurs ───────────────────────────────────────────────────────
    with t2:
        jou = an["joueurs"]
        c1, c2 = st.columns(2)
        for col, team_key, team in [(c1, "home", h), (c2, "away", a)]:
            with col:
                st.markdown(
                    f'<p class="bbn" style="font-size:1.2rem;color:#CAFF33;">'
                    f'<span class="team-badge" style="background:{team["color"]};display:inline-flex;'
                    f'width:28px;height:28px;font-size:.7rem;vertical-align:middle;margin-right:.4rem;">'
                    f'{team["short"]}</span>{team["name"]}</p>',
                    unsafe_allow_html=True,
                )
                for p in jou[team_key]:
                    note_color = color_note(p["note"])
                    bar_pct = player_bar_pct(p["note"])
                    st.markdown(
                        f'<div class="player-row">'
                        f'<span class="player-poste" style="color:#555;">{p["poste"]}</span>'
                        f'<span class="player-name">{p["nom"]}</span>'
                        f'<div class="player-bar-wrap"><div class="player-bar" style="width:{bar_pct}%;background:{note_color};"></div></div>'
                        f'<span class="player-note" style="color:{note_color};">{p["note"]}</span>'
                        f'</div>'
                        f'<div style="font-size:.72rem;color:#444;margin-bottom:.5rem;margin-left:calc(2rem + 130px);">{p["stats"]}</div>',
                        unsafe_allow_html=True,
                    )

    # ── Tab 3 : Bilan ──────────────────────────────────────────────────────────
    with t3:
        bil = an["bilan"]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<p class="bbn" style="font-size:1.1rem;color:#CAFF33;">💪 {h["short"]} — Points Forts</p>', unsafe_allow_html=True)
            for pt in bil["home_forts"]:
                st.markdown(f'<div class="point-fort">✅ {pt}</div>', unsafe_allow_html=True)
            st.markdown(f'<p class="bbn" style="font-size:1.1rem;color:#ef4444;margin-top:1rem;">⚠️ {h["short"]} — Points Faibles</p>', unsafe_allow_html=True)
            for pt in bil["home_faibles"]:
                st.markdown(f'<div class="point-faible">❌ {pt}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<p class="bbn" style="font-size:1.1rem;color:#CAFF33;">💪 {a["short"]} — Points Forts</p>', unsafe_allow_html=True)
            for pt in bil["away_forts"]:
                st.markdown(f'<div class="point-fort">✅ {pt}</div>', unsafe_allow_html=True)
            st.markdown(f'<p class="bbn" style="font-size:1.1rem;color:#ef4444;margin-top:1rem;">⚠️ {a["short"]} — Points Faibles</p>', unsafe_allow_html=True)
            for pt in bil["away_faibles"]:
                st.markdown(f'<div class="point-faible">❌ {pt}</div>', unsafe_allow_html=True)

    # ── Tab 4 : Verdict Coach ─────────────────────────────────────────────────
    with t4:
        verd = an["verdict"]
        sc1, sc2, sc3, sc4 = st.columns(4)
        for col, label, val in [
            (sc1, f"Perf. {h['short']}", verd["home_perf"]),
            (sc2, f"Perf. {a['short']}", verd["away_perf"]),
            (sc3, "Intensité", verd["intensite"]),
            (sc4, "Spectacle", verd["spectacle"]),
        ]:
            with col:
                st.markdown(
                    f'<div class="verdict-score">'
                    f'<div class="label">{label}</div>'
                    f'<div class="value">{val}</div>'
                    f'<div class="label">/10</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<hr class="div-line">', unsafe_allow_html=True)

        _vc_h = COACHES.get(COACH_TEAM_LOOKUP.get(h["name"], ""))
        _vc_a = COACHES.get(COACH_TEAM_LOOKUP.get(a["name"], ""))
        if _vc_h or _vc_a:
            _pc1, _pc2 = st.columns(2)
            for _pc, _vc, _team in [(_pc1, _vc_h, h), (_pc2, _vc_a, a)]:
                with _pc:
                    if _vc:
                        _str_pills = "  ".join(f'<span style="background:#1a2a0a;color:#CAFF33;border-radius:4px;padding:.15rem .5rem;font-size:.72rem;">{s}</span>' for s in _vc["strengths"])
                        _wk_pills  = "  ".join(f'<span style="background:#2a1010;color:#ef4444;border-radius:4px;padding:.15rem .5rem;font-size:.72rem;">{w}</span>' for w in _vc["weaknesses"])
                        _kp_items  = "".join(f'<li style="margin:.2rem 0;">{kp}</li>' for kp in _vc["key_principles"])
                        st.markdown(
                            f'<div style="background:#111;border:1px solid #222;border-radius:10px;padding:1rem 1.1rem;margin-bottom:.8rem;">'
                            f'<p style="color:#888;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.3rem;">PROFIL COACH — {_team["short"]}</p>'
                            f'<p style="color:#f0f0f0;font-size:1.1rem;font-weight:700;margin:.1rem 0;">{_vc["nationality"]} {_vc["name"]}</p>'
                            f'<p style="color:#888;font-size:.78rem;margin-bottom:.6rem;">{_vc["formation"]} · {_vc["style"]}</p>'
                            f'<p style="color:#ccc;font-size:.82rem;line-height:1.6;margin-bottom:.7rem;">{_vc["philosophy"]}</p>'
                            f'<p style="margin-bottom:.3rem;">{_str_pills}</p>'
                            f'<p style="margin-bottom:.7rem;">{_wk_pills}</p>'
                            f'<p style="color:#888;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.2rem;">PRINCIPES CLÉS</p>'
                            f'<ul style="color:#aaa;font-size:.8rem;padding-left:1.2rem;margin:0;">{_kp_items}</ul>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
            st.markdown('<hr class="div-line">', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<p class="bbn" style="font-size:1.1rem;color:#CAFF33;">📝 Analyse {h["short"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-card">{verd["home_txt"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-card" style="border-color:#2a2a2a;">{verd["coach_home"]}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<p class="bbn" style="font-size:1.1rem;color:#CAFF33;">📝 Analyse {a["short"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-card">{verd["away_txt"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-card" style="border-color:#2a2a2a;">{verd["coach_away"]}</div>', unsafe_allow_html=True)
