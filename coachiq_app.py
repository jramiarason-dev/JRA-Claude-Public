import streamlit as st
import os
import re
from datetime import date, datetime, timedelta
import calendar as cal_mod

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
    margin-bottom:1rem;
    transition:all .25s ease;
    cursor:pointer;
    position:relative;
    overflow:hidden;
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
D10 = (TODAY - timedelta(days=4)).isoformat()
D14 = TODAY.isoformat()
D17 = (TODAY + timedelta(days=3)).isoformat()

SPORTS = ["⚽ Football", "🏀 Basket", "🏉 Rugby"]

COMPETITIONS_BY_SPORT = {
    "⚽ Football": ["Ligue 1", "Champions League", "Premier League", "Super League Suisse"],
    "🏀 Basket": ["NBA", "Euroleague", "Betclic Elite"],
    "🏉 Rugby": ["Top 14", "Pro D2", "Champions Cup"],
}

def badge(color, initials):
    return f'<div class="team-badge" style="background:{color}">{initials}</div>'

MATCHES = {
    "psg_monaco": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": D10, "time": "21:00", "stadium": "Parc des Princes, Paris",
        "status": "Terminé",
        "home": {"name": "Paris Saint-Germain", "short": "PSG", "color": "#004174", "score": 3},
        "away": {"name": "AS Monaco", "short": "MCO", "color": "#E4002B", "score": 1},
    },
    "real_arsenal": {
        "sport": "⚽ Football", "competition": "Champions League",
        "date": D14, "time": "21:00", "stadium": "Santiago Bernabéu, Madrid",
        "status": "Live",
        "home": {"name": "Real Madrid", "short": "RMA", "color": "#FEBE10", "score": 2},
        "away": {"name": "Arsenal FC", "short": "ARS", "color": "#EF0107", "score": 1},
    },
    "arsenal_mancity": {
        "sport": "⚽ Football", "competition": "Premier League",
        "date": D17, "time": "17:30", "stadium": "Emirates Stadium, Londres",
        "status": "À venir",
        "home": {"name": "Arsenal FC", "short": "ARS", "color": "#EF0107", "score": None},
        "away": {"name": "Manchester City", "short": "MCI", "color": "#6CABDD", "score": None},
    },
    "sl_bale_yb": {
        "sport": "⚽ Football", "competition": "Super League Suisse",
        "date": D14, "time": "18:00", "stadium": "St. Jakob-Park, Bâle",
        "status": "Terminé",
        "home": {"name": "FC Basel", "short": "FCB", "color": "#CC0000", "score": 2},
        "away": {"name": "BSC Young Boys", "short": "YB", "color": "#FFD700", "score": 2},
    },
    "lakers_warriors": {
        "sport": "🏀 Basket", "competition": "NBA",
        "date": D10, "time": "03:30", "stadium": "Crypto.com Arena, Los Angeles",
        "status": "Terminé",
        "home": {"name": "Los Angeles Lakers", "short": "LAL", "color": "#552583", "score": 108},
        "away": {"name": "Golden State Warriors", "short": "GSW", "color": "#1D428A", "score": 95},
    },
    "real_barca_euro": {
        "sport": "🏀 Basket", "competition": "Euroleague",
        "date": D17, "time": "21:00", "stadium": "WiZink Center, Madrid",
        "status": "À venir",
        "home": {"name": "Real Madrid", "short": "RMA", "color": "#FEBE10", "score": None},
        "away": {"name": "FC Barcelona", "short": "BAR", "color": "#A50044", "score": None},
    },
    "asvel_monaco_b": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D14, "time": "20:30", "stadium": "Astroballe, Villeurbanne",
        "status": "À venir",
        "home": {"name": "LDLC ASVEL", "short": "ASV", "color": "#003a70", "score": None},
        "away": {"name": "Monaco Basket", "short": "MCO", "color": "#B5121B", "score": None},
    },
    "toulouse_racing": {
        "sport": "🏉 Rugby", "competition": "Top 14",
        "date": D14, "time": "20:45", "stadium": "Stadium de Toulouse",
        "status": "À venir",
        "home": {"name": "Stade Toulousain", "short": "ST", "color": "#B60000", "score": None},
        "away": {"name": "Racing 92", "short": "R92", "color": "#0099CC", "score": None},
    },
    "bordeaux_larochelle": {
        "sport": "🏉 Rugby", "competition": "Champions Cup",
        "date": D10, "time": "16:05", "stadium": "Stade Chaban-Delmas, Bordeaux",
        "status": "Terminé",
        "home": {"name": "Bordeaux-Bègles", "short": "UBB", "color": "#001F5B", "score": 24},
        "away": {"name": "Stade Rochelais", "short": "SR", "color": "#FCD000", "score": 27},
    },
    "lyon_montpellier": {
        "sport": "🏉 Rugby", "competition": "Pro D2",
        "date": D17, "time": "19:00", "stadium": "Matmut Stadium, Lyon",
        "status": "À venir",
        "home": {"name": "Lyon OU", "short": "LOU", "color": "#0057A8", "score": None},
        "away": {"name": "Montpellier HR", "short": "MHR", "color": "#E3000F", "score": None},
    },
}

# ── Full analysis data (for finished/live matches) ────────────────────────────
ANALYSIS = {
    "psg_monaco": {
        "tactique": {
            "home_form": "4-3-3",
            "away_form": "4-2-3-1",
            "home_style": "Possession haute, pressing collectif en zone adverse, jeu en combinaisons sur les côtés",
            "away_style": "Bloc médian compact, sortie en contre-attaque rapide sur les récupérations",
            "home_players": [
                ["Donnarumma","GB"],["Hakimi","RD"],["Marquinhos","DC"],
                ["Skriniar","DC"],["Nuno","LD"],
                ["Fabian","MC"],["Vitinha","MC"],["Zaire","MO"],
                ["Dembélé","AD"],["Barcola","AG"],["Kolo Muani","BU"],
            ],
            "away_players": [
                ["Majecki","GB"],["Vanderson","RD"],["Camara","DC"],
                ["Maripan","DC"],["Caio Henrique","LD"],
                ["Fofana","MDC"],["Zakaria","MDC"],
                ["Ben Seghir","MO"],["Akliouche","MO"],["Minamino","MO"],
                ["Embolo","BU"],
            ],
            "phases": {
                "Pressing": "PSG PPDA : 7.2 — pressing haut dès la relance monégasque. 14 récupérations dans le camp adverse, dont 3 ayant mené à des tirs.",
                "Transitions": "Transitions offensives fulgurantes via les couloirs. Hakimi–Dembélé à droite : 6 combinaisons, 3 centres, 2 buts. Monaco trop exposé dans le dos de ses latéraux.",
                "Phases arrêtées": "5 corners PSG (2 occasions directes), 2 Monaco. Corner travaillé en angle court sur le 3e but. Monaco dangereux sur un coup-franc à 25m (Majecki sauve sa barre).",
                "Bloc défensif": "Monaco en 4-4-2 bas en récupération, ligne à 35m. PSG : bloc haut à 55m, ligne défensive agressive. Monaco a subi 18 tirs (9 cadrés).",
            },
            "home_stats": {"Possession": (64,36), "Tirs": (18,8), "Tirs cadrés": (9,3), "Passes réussies": (87,71), "Fautes": (11,16)},
        },
        "joueurs": {
            "home": [
                {"nom":"Dembélé","poste":"ATT","note":9.1,"stats":"2 buts, 1 PD, 4 dribbles","color":"#CAFF33"},
                {"nom":"Fabian Ruiz","poste":"MC","note":8.5,"stats":"87 ballons, 3 récup.","color":"#90ee2a"},
                {"nom":"Hakimi","poste":"RD","note":8.2,"stats":"2 PD, 6 centres","color":"#90ee2a"},
                {"nom":"Marquinhos","poste":"DC","note":7.8,"stats":"92% passes, 4 dégagements","color":"#60d060"},
                {"nom":"Donnarumma","poste":"GB","note":7.5,"stats":"3 arrêts décisifs","color":"#60d060"},
                {"nom":"Barcola","poste":"AG","note":7.4,"stats":"1 but, 4 dribbles","color":"#60d060"},
                {"nom":"Kolo Muani","poste":"BU","note":6.9,"stats":"1 but, 3 tirs","color":"#f0c040"},
            ],
            "away": [
                {"nom":"Ben Seghir","poste":"MO","note":7.2,"stats":"1 but, 71 ballons","color":"#60d060"},
                {"nom":"Majecki","poste":"GB","note":6.8,"stats":"6 arrêts","color":"#f0c040"},
                {"nom":"Minamino","poste":"MO","note":6.9,"stats":"2 tirs, 1 passement","color":"#f0c040"},
                {"nom":"Fofana","poste":"MDC","note":6.2,"stats":"Récupérations limitées","color":"#e07030"},
                {"nom":"Camara","poste":"DC","note":6.0,"stats":"3 fautes, 1 avert.","color":"#e07030"},
                {"nom":"Embolo","poste":"BU","note":5.8,"stats":"Isolé, 0 tir cadré","color":"#e05050"},
            ],
        },
        "bilan": {
            "home_forts": [
                "Maîtrise totale du milieu : Fabian + Vitinha dictent le tempo",
                "Efficacité offensive : 3 buts sur 9 tirs cadrés (33%)",
                "Pressing collectif : 14 récupérations en zone haute",
                "Couloir droit dominant — Hakimi–Dembélé combinaison redoutable",
            ],
            "home_faibles": [
                "Quelques pertes de balle risquées dans la construction basse",
                "Indiscipline défensive sur 2 corners encaissés (fautes dans la surface)",
            ],
            "away_forts": [
                "Bloc défensif 0-0 solide en première période",
                "Réalisme sur le seul corner travaillé : but de Ben Seghir",
            ],
            "away_faibles": [
                "Incapacité à sortir proprement face au pressing : 47% pertes de balle dans leur camp",
                "Seulement 3 tirs cadrés sur 8 tirs : manque de finition en transition",
                "Gestion du ballon défaillante après le 2-0 (retraite trop profonde)",
                "Embolo totalement coupé du jeu : 0 duel gagné en attaque",
            ],
        },
        "verdict": {
            "home_perf": 8.7, "away_perf": 5.9,
            "intensite": 7.5, "spectacle": 7.8,
            "home_txt": "Le PSG a livré une prestation aboutie. Luis Enrique a parfaitement exploité les espaces laissés par Monaco avec un pressing collectif exemplaire. Fabian Ruiz, métronome du milieu, a permis une possession de haute qualité (87% de passes réussies).",
            "away_txt": "Monaco a manqué d'ambition en seconde période. Après le 2-0, conserver un bloc bas était suicidaire. Adi Hütter aurait dû libérer Ben Seghir et passer en 4-3-3 offensif dès la 60'.",
            "coach_home": "✅ Choix tactiques validés. Sortie calculée de Mbappé à 70' (ménagement). Hakimi maintenu haut malgré les contre-attaques monégasques : prise de risque assumée et maîtrisée.",
            "coach_away": "⚠️ Erreur de lecture manifeste. Rester en bloc bas après le 2-0 a privé Monaco de tout espoir de renversement. Embolo devait sortir dès la 55' pour faire entrer Gölovin.",
        },
    },
    "lakers_warriors": {
        "tactique": {
            "home_form": "Positionnel",
            "away_form": "Motion Offense",
            "home_style": "Jeu de poste bas d'AD, isolation LeBron sur le côté gauche, P&R tardifs",
            "away_style": "Circulation de balle rapide, P&R Curry–Wiggins, tirs à 3pts en catch-and-shoot",
            "home_players": [
                ["LeBron","SF"],["A. Davis","C"],["D'Angelo","PG"],
                ["Reaves","SG"],["Hachimura","PF"],
            ],
            "away_players": [
                ["Curry","PG"],["Klay","SG"],["Wiggins","SF"],
                ["Looney","C"],["GP2","PF"],
            ],
            "phases": {
                "Pick & Roll": "Lakers : 18 P&R, 14 pts générés (efficacité 0.78 ppt). Warriors : 22 P&R, mais défense Lakers agressive sur le ball-handler — Curry limité à 3/9 sur P&R.",
                "Fast Break": "Warriors génèrent 18 pts en transition (meilleure attaque en contre). Lakers réduisent les transitions à 11 en seconde mi-temps grâce à un meilleur retour défensif.",
                "Isolation": "LeBron en isolation côté gauche : 5/9, 14 pts, 3 fautes provoquées. Klay Thompson trop statique : isolation peu productive (2/7).",
                "Clutch Time": "Q4 : Lakers prennent le contrôle à 95-85 (8-0 run). Curry sort sur fautes à 4'30. Davis domine la peinture : 8 pts dans le 4e quart.",
            },
            "home_stats": {"Tirs 3pts": (12,9), "Rebonds": (48,40), "Interceptions": (9,6), "Passes dec.": (28,22), "Fautes": (19,22)},
        },
        "joueurs": {
            "home": [
                {"nom":"A. Davis","poste":"C","note":9.3,"stats":"32 pts, 14 reb, 3 blk","color":"#CAFF33"},
                {"nom":"LeBron James","poste":"SF","note":8.8,"stats":"27 pts, 9 ast, 6 reb","color":"#90ee2a"},
                {"nom":"Austin Reaves","poste":"SG","note":7.9,"stats":"18 pts, 4/7 à 3pts","color":"#60d060"},
                {"nom":"D'Angelo Russell","poste":"PG","note":7.2,"stats":"14 pts, 7 ast","color":"#f0c040"},
                {"nom":"Rui Hachimura","poste":"PF","note":6.8,"stats":"9 pts, 5 reb","color":"#f0c040"},
            ],
            "away": [
                {"nom":"S. Curry","poste":"PG","note":8.1,"stats":"26 pts mais 6 TOs","color":"#90ee2a"},
                {"nom":"A. Wiggins","poste":"SF","note":7.4,"stats":"21 pts, 7 reb","color":"#60d060"},
                {"nom":"Klay Thompson","poste":"SG","note":6.2,"stats":"13 pts, 3/11 à 3pts","color":"#e07030"},
                {"nom":"Draymond Green","poste":"PF","note":6.8,"stats":"5 pts, 11 ast, 6 reb","color":"#f0c040"},
                {"nom":"K. Looney","poste":"C","note":5.9,"stats":"Dominé par Davis","color":"#e05050"},
            ],
        },
        "bilan": {
            "home_forts": [
                "Davis dominateur en peinture : 32 pts / 14 rebonds (impossible à stopper)",
                "Défense sur Curry efficace en 2e mi-temps : 3 interceptions sur ses P&R",
                "Exécution clutch parfaite au 4e quart (8-0 run décisif)",
                "Reaves surprenant à 3pts : 4/7, énorme impact offensif",
            ],
            "home_faibles": [
                "19 fautes concédées, risque de mise en foul trouble pour Davis en 3e quart",
                "Début de match poussif : -7 au score à 8' du 2e quart",
            ],
            "away_forts": [
                "Jeu en mouvement rapide efficace en 1ère mi-temps : 53 pts à la pause",
                "Wiggins surprenant : meilleur marqueur côté Warriors",
            ],
            "away_faibles": [
                "Curry dans ses pires soirées sur P&R : 3/9, face à une défense physique",
                "Klay Thompson en manque de rythme : 3/11 à 3pts, aucune influence au clutch",
                "Looney écrasé par Davis : -8 en rebonds offensifs",
                "6 turnovers de Curry au total : trop de décisions précipitées",
            ],
        },
        "verdict": {
            "home_perf": 8.9, "away_perf": 6.4,
            "intensite": 8.2, "spectacle": 8.6,
            "home_txt": "Les Lakers ont parfaitement construit leur victoire. JJ Redick a eu la bonne idée d'orienter le jeu vers Davis dès le 3e quart et de réduire les isolations LeBron. La discipline défensive sur Curry en 2e mi-temps a été déterminante.",
            "away_txt": "Steve Kerr a manqué d'ajustements. Thompson aurait dû être sorti à la mi-temps au profit d'un shooter plus en jambes. La gestion des fautes de Curry (sortir plus tôt) aurait pu changer la dynamique du 4e quart.",
            "coach_home": "✅ Plan de jeu optimal. Mise en valeur de Davis dans le pick & pop et dans le post bas a déstabilisé toute la défense Golden State.",
            "coach_away": "⚠️ Kerr trop fidèle à un Klay Thompson inexistant (43 min jouées). La rotation Kuminga aurait pu changer le rapport de forces en peinture.",
        },
    },
    "bordeaux_larochelle": {
        "tactique": {
            "home_form": "XV de départ classique",
            "away_form": "Attaque des espaces",
            "home_style": "Jeu au sol dominateur, mêlée puissante, maul offensif, jeu au pied de Jalibert",
            "away_style": "Jeu à la main rapide, attaque des intervalles, soutiens immédiats, touche dominatrice",
            "home_players": [
                ["Jalibert","DO"],["Lucu","DM"],["Dubié","AI"],
                ["Buros","CE"],["Bielle-Biarrey","AI"],
                ["Woki","N°8"],["Cramont","F"],["Cobilas","F"],
            ],
            "away_players": [
                ["Hastoy","DO"],["Kerr-Barlow","DM"],["Leyds","AI"],
                ["Berjon","CE"],["Botia","CE"],
                ["Alldritt","N°8"],["Skelton","TL"],["Priso","PI"],
            ],
            "phases": {
                "Ruck & Maul": "Bordeaux domine les rucks en 1ère période (15 rucks gagnés vs 11). La Rochelle réagit en 2e mi-temps avec des mauls offensifs : 3 pénalités obtenues dans les 5 dernières mètres.",
                "Touche & Mêlée": "La Rochelle dominatrice en touche (86% ball won). Bordeaux solide en mêlée fermée (5 mêlées gagnées). Skelton omniprésent dans les airs (8 ballons saisis).",
                "Jeu au pied": "Jalibert : 5/6 en pénalités, 1 transformation. Jeu territorial précis (60% au-delà des 22m). Hastoy répond par des coups de pied rasants dans les couloirs.",
                "Défense en ligne": "La Rochelle en rideau défensif efficace en 2e mi-temps. UBB concède 3 pénalités sous pression dans les 20 dernières minutes — coûteuses.",
            },
            "home_stats": {"Possession": (54,46), "Mêlées gagnées": (5,3), "Plaquages": (85,94), "Pénalités concédées": (11,9), "Km parcourus": (90,98)},
        },
        "joueurs": {
            "home": [
                {"nom":"Matthieu Jalibert","poste":"DO","note":8.4,"stats":"18 pts (5 pén, 1 transf), jeu au pied précis","color":"#90ee2a"},
                {"nom":"L. Bielle-Biarrey","poste":"AI","note":8.0,"stats":"1 essai, 3 défenses","color":"#60d060"},
                {"nom":"Maxime Lucu","poste":"DM","note":7.5,"stats":"Jeu rapide, 1 passe décisive","color":"#60d060"},
                {"nom":"Cameron Woki","poste":"N°8","note":7.2,"stats":"8 plaquages, 1 grattage","color":"#f0c040"},
            ],
            "away": [
                {"nom":"Alldritt","poste":"N°8","note":9.0,"stats":"Colossal : 14 plaquages, 2 essais provoqués","color":"#CAFF33"},
                {"nom":"Will Skelton","poste":"TL","note":8.6,"stats":"8 ballons de touche, dominateur","color":"#90ee2a"},
                {"nom":"Ihaia West","poste":"DO","note":8.0,"stats":"12 pts, 3 drops tentés","color":"#60d060"},
                {"nom":"Léo Berdeu","poste":"AI","note":7.3,"stats":"1 essai décisif à la 76'","color":"#60d060"},
            ],
        },
        "bilan": {
            "home_forts": [
                "Domination en mêlée fermée (5/5), plateforme de jeu fiable",
                "Jalibert en état de grâce au pied : 83% de succès en pénalités",
                "Maîtrise du tempo en 1ère période avec 54% de possession",
            ],
            "home_faibles": [
                "Discipline en berne : 11 pénalités concédées, 3 cruciales en fin de match",
                "Jeu trop prévisible en attaque : La Rochelle lit les schemes de UBB",
                "Incapacité à conclure dans les 5m adverses (2 mauls arrêtés)",
            ],
            "away_forts": [
                "Résilience mentale : derrière au score jusqu'à la 73', retournement final",
                "Alldritt — meilleur joueur du match, performance physique exceptionnelle",
                "Domination totale en touche : Skelton insurpassable dans les airs",
                "Essai décisif de Berdeu à la 76' : finition clinique",
            ],
            "away_faibles": [
                "Première période décevante : trop de fautes et de ballons perdus",
                "Mêlée sous pression face aux piliers de Bordeaux",
            ],
        },
        "verdict": {
            "home_perf": 6.8, "away_perf": 8.1,
            "intensite": 9.2, "spectacle": 8.7,
            "home_txt": "Bordeaux s'est montré trop indiscipliné en fin de match. Une avance de 21-13 à la 60' ne devrait pas suffire à perdre ce match. Yannick Bru aurait dû demander un jeu plus conservateur dans les 15 dernières minutes plutôt que continuer à attaquer.",
            "away_txt": "La Rochelle a montré un mental d'acier. Ronan O'Gara a parfaitement ajusté son équipe après la mi-temps avec un jeu plus rapide et un Skelton utilisé comme pivot de toutes les attaques en touche.",
            "coach_home": "⚠️ Bru aurait dû passer en mode gestion à 21-13. Continuer à attaquer était risqué et a conduit à 3 pénalités coûteuses. Sortir Woki frais en 2e mi-temps était aussi une erreur.",
            "coach_away": "✅ O'Gara a su repositionner son équipe. Le changement tactique à la mi-temps (jeu plus direct, utilisation de Skelton en cible) a totalement retourné le match.",
        },
    },
}

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

def render_match_card(mid, m, selected):
    h, a = m["home"], m["away"]
    sc_h = h["score"] if h["score"] is not None else "–"
    sc_a = a["score"] if a["score"] is not None else "–"
    status_cls = {"Terminé": "badge-done", "Live": "badge-live", "À venir": "badge-soon"}.get(m["status"], "badge-done")
    selected_cls = "selected" if selected else ""
    date_fmt = datetime.strptime(m["date"], "%Y-%m-%d").strftime("%d %b")
    return f"""
<div class="match-card {selected_cls}">
  <div class="comp-label">{m['competition']} &nbsp;·&nbsp; {date_fmt} {m['time']}</div>
  <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;">
    <div style="display:flex;align-items:center;gap:.75rem;min-width:0;flex:1;">
      <div class="team-badge" style="background:{h['color']};flex-shrink:0;">{h['short']}</div>
      <div><div class="team-name">{h['name']}</div><div class="team-name-sm">Domicile</div></div>
    </div>
    <div style="display:flex;align-items:center;gap:.3rem;flex-shrink:0;">
      <span class="score-box">{sc_h}</span>
      <span class="score-sep">—</span>
      <span class="score-box">{sc_a}</span>
    </div>
    <div style="display:flex;align-items:center;gap:.75rem;min-width:0;flex:1;justify-content:flex-end;">
      <div style="text-align:right;"><div class="team-name">{a['name']}</div><div class="team-name-sm">Extérieur</div></div>
      <div class="team-badge" style="background:{a['color']};flex-shrink:0;">{a['short']}</div>
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

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "sport" not in st.session_state: st.session_state.sport = "⚽ Football"
if "selected_match" not in st.session_state: st.session_state.selected_match = None
if "selected_date" not in st.session_state: st.session_state.selected_date = TODAY
if "comp_filter" not in st.session_state:
    st.session_state.comp_filter = set()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<p class="bbn" style="font-size:1.8rem;color:#CAFF33;margin-bottom:0;">COACH<span style="color:#f0f0f0;">IQ</span></p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:.75rem;color:#444;margin-top:0;">Analyse tactique · IA · Tous sports</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Mini calendar ──
    st.markdown('<p class="bbn" style="font-size:1rem;color:#888;letter-spacing:.1em;">CALENDRIER</p>', unsafe_allow_html=True)

    nav_col1, nav_col2, nav_col3 = st.columns([1,3,1])
    with nav_col1:
        if st.button("◀", key="prev_m"):
            d = st.session_state.selected_date.replace(day=1) - timedelta(days=1)
            st.session_state.selected_date = d.replace(day=min(st.session_state.selected_date.day, cal_mod.monthrange(d.year, d.month)[1]))
    with nav_col2:
        st.markdown(f'<p style="text-align:center;font-weight:700;font-size:.9rem;color:#f0f0f0;">{st.session_state.selected_date.strftime("%B %Y").capitalize()}</p>', unsafe_allow_html=True)
    with nav_col3:
        if st.button("▶", key="next_m"):
            d = st.session_state.selected_date.replace(day=28) + timedelta(days=4)
            st.session_state.selected_date = d.replace(day=min(st.session_state.selected_date.day, cal_mod.monthrange(d.year, d.month)[1]))

    yr, mo = st.session_state.selected_date.year, st.session_state.selected_date.month
    match_dates = set(m["date"] for m in MATCHES.values())
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

    sel_date = st.date_input("", value=st.session_state.selected_date, label_visibility="collapsed")
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
    st.session_state.comp_filter = new_filter if new_filter else set(sport_comps)

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
                st.rerun()
            if active:
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr style="border:none;border-top:1px solid #1a1a1a;margin:.75rem 0 1.5rem;">', unsafe_allow_html=True)

# ── Filter matches ─────────────────────────────────────────────────────────────
date_str = st.session_state.selected_date.isoformat()
active_comps = st.session_state.comp_filter or set(COMPETITIONS_BY_SPORT.get(st.session_state.sport, []))

filtered = {
    mid: m for mid, m in MATCHES.items()
    if m["sport"] == st.session_state.sport
    and m["date"] == date_str
    and m["competition"] in active_comps
}

all_sport = {
    mid: m for mid, m in MATCHES.items()
    if m["sport"] == st.session_state.sport
    and m["competition"] in active_comps
}

# ── Date headline ──────────────────────────────────────────────────────────────
date_label = st.session_state.selected_date.strftime("%A %d %B %Y").capitalize()
count = len(filtered)
st.markdown(
    f'<p class="bbn" style="font-size:1.5rem;color:#f0f0f0;">'
    f'{date_label} <span style="color:#CAFF33;font-size:1rem;">{count} match{"s" if count!=1 else ""}</span></p>',
    unsafe_allow_html=True,
)

# ── Match cards ────────────────────────────────────────────────────────────────
if filtered:
    left_col, right_col = st.columns([1, 1])
    items = list(filtered.items())
    for i, (mid, m) in enumerate(items):
        col = left_col if i % 2 == 0 else right_col
        with col:
            html = render_match_card(mid, m, st.session_state.selected_match == mid)
            st.markdown(html, unsafe_allow_html=True)
            btn_label = "🔍 Analyser" if mid in ANALYSIS else "📅 À venir"
            if mid in ANALYSIS:
                if st.button(btn_label, key=f"sel_{mid}"):
                    st.session_state.selected_match = None if st.session_state.selected_match == mid else mid
                    st.rerun()
            else:
                st.button(btn_label, key=f"sel_{mid}", disabled=True)
else:
    st.markdown(
        f'<div style="background:#111;border:1px solid #1a1a1a;border-radius:12px;padding:2rem;text-align:center;">'
        f'<p style="color:#444;font-size:1rem;">Aucun match {st.session_state.sport} le {date_label}.</p>'
        f'<p style="color:#333;font-size:.85rem;">Essayez une autre date.</p></div>',
        unsafe_allow_html=True,
    )

    # show other available dates for this sport
    other_dates = sorted(set(m["date"] for m in all_sport.values()))
    if other_dates:
        st.markdown('<p style="color:#555;font-size:.8rem;margin-top:1rem;">Matchs disponibles :</p>', unsafe_allow_html=True)
        for od in other_dates:
            od_label = datetime.strptime(od, "%Y-%m-%d").strftime("%d %b")
            od_cnt = sum(1 for m in all_sport.values() if m["date"] == od)
            if st.button(f"{od_label} — {od_cnt} match{'s' if od_cnt>1 else ''}", key=f"goto_{od}"):
                st.session_state.selected_date = datetime.strptime(od, "%Y-%m-%d").date()
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS PANEL
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.selected_match and st.session_state.selected_match in ANALYSIS:
    mid = st.session_state.selected_match
    m = MATCHES[mid]
    an = ANALYSIS[mid]
    h, a = m["home"], m["away"]

    st.markdown('<hr style="border:none;border-top:1px solid #1e1e1e;margin:1.5rem 0;">', unsafe_allow_html=True)
    st.markdown(
        f'<p class="bbn" style="font-size:2rem;color:#f0f0f0;margin-bottom:.25rem;">'
        f'<span style="color:{h["color"]};">{h["short"]}</span>'
        f' <span style="color:#CAFF33;">{h["score"]} — {a["score"]}</span> '
        f'<span style="color:{a["color"]};">{a["short"]}</span>'
        f'</p>'
        f'<p style="color:#444;font-size:.8rem;margin-bottom:1.25rem;">'
        f'{m["competition"]} · {m["stadium"]}</p>',
        unsafe_allow_html=True,
    )

    t1, t2, t3, t4 = st.tabs(["⚙️ Tactique", "🌟 Joueurs", "📊 Bilan", "🧠 Verdict Coach"])

    # ── Tab 1 : Tactique ──────────────────────────────────────────────────────
    with t1:
        tac = an["tactique"]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<p class="bbn" style="font-size:1.2rem;color:#CAFF33;">Formation {h["short"]} — {tac["home_form"]}</p>', unsafe_allow_html=True)
            st.markdown(render_formation(tac.get("home_players", []), h["color"], h["short"]), unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:.85rem;color:#aaa;margin-top:.75rem;">{tac["home_style"]}</p>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<p class="bbn" style="font-size:1.2rem;color:#CAFF33;">Formation {a["short"]} — {tac["away_form"]}</p>', unsafe_allow_html=True)
            st.markdown(render_formation(tac.get("away_players", []), a["color"], a["short"]), unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:.85rem;color:#aaa;margin-top:.75rem;">{tac["away_style"]}</p>', unsafe_allow_html=True)

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
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<p class="bbn" style="font-size:1.1rem;color:#CAFF33;">📝 Analyse {h["short"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-card">{verd["home_txt"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-card" style="border-color:#2a2a2a;">{verd["coach_home"]}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<p class="bbn" style="font-size:1.1rem;color:#CAFF33;">📝 Analyse {a["short"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-card">{verd["away_txt"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="verdict-card" style="border-color:#2a2a2a;">{verd["coach_away"]}</div>', unsafe_allow_html=True)
