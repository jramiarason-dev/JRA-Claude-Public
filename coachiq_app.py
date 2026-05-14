import streamlit as st
import os
import re
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
                "Pressing": "Ce n'était pas du pressing — c'était du harcèlement systématisé. Fabian Ruiz a coupé la ligne de passe verticale de Zakaria 17 fois en première période. Monaco ne pouvait physiquement pas jouer. Quand ton milieu défensif ne reçoit jamais ballon dans les pieds dans son propre camp, ta structure de jeu s'effondre. C'est exactement ce qui s'est passé à la 34' : Ruiz récupère le ballon sur une relance monégasque ratée, Dembélé part dans le dos de Maripan, 1-0. Le pressing n'est pas une question d'intensité — c'est une question de lignes de passe coupées. PSG a maîtrisé ça parfaitement.",
                "Transitions": "Hakimi–Dembélé sur le côté droit : c'est le couloir le plus dangereux d'Europe en ce moment. Trois fois en première période, Monaco a tenté de sortir par la gauche, trois fois ils se sont retrouvés pris en supériorité numérique. Le problème de Monaco n'était pas défensif — c'était leur incapacité à fixer les latéraux parisiens avec leurs ailiers. Minamino n'a jamais rentré dans son côté pour aider Caio Henrique. C'est ça la vraie erreur tactique de ce soir.",
                "Phases arrêtées": "Le coin à angle court sur le 3e but est un chef-d'œuvre de préparation. PSG a travaillé ça toute la semaine. Barcola sert Fabian qui décale Dembélé — Monaco ne l'a pas vu venir malgré deux répétitions similaires dans la mi-temps. En tant que coach, quand tu vois une séquence se reproduire deux fois, tu dois adapter ta défense de corner immédiatement. Hütter ne l'a pas fait.",
                "Bloc défensif": "Monaco a essayé le bloc bas, mais un bloc bas ne fonctionne que si tu as la capacité de repartir vite en contre. Avec Embolo seul en pointe, coupé de tout soutien, c'était mission impossible. J'ai compté 6 récupérations de Monaco en seconde période — dont aucune n'a débouché sur une situation offensive. Un bloc bas sans contre-attaque, ce n'est pas une tactique, c'est de la survie.",
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
                "Occupation de l'espace : 64% de possession AVEC pressing haut — combinaison rarissime qui signifie que Monaco n'a jamais pu respirer ni reposer",
                "Permutation Ruiz–Vitinha parfaite : quand l'un montait presser, l'autre couvrait dans l'axe — automatisme d'un niveau Champions League évident",
                "Dembélé en faux ailier droit : ses décrochages attiraient Maripan, libérant les courses de Barcola dans l'espace. Monaco ne savait jamais qui marquer",
                "Gestion de score sans ego à 3-1 : Luis Enrique sort Mbappé à 70' pour préserver les jambes avant un déplacement crucial. Priorité collective, zéro concession aux statistiques individuelles",
            ],
            "home_faibles": [
                "3 relances courtes perdues entre la 55' et la 65' dans le camp adverse — face à un Monaco plus ambitieux, ces ballons perdus en zone de pressing auraient pu coûter très cher",
                "Ligne défensive trop haute à 2-0 : sur le but de Ben Seghir, Skriniar est à 40m de sa cage. Ce relâchement est inacceptable. Un champion du monde ne se permet jamais ça",
            ],
            "away_forts": [
                "Solidité défensive jusqu'à la 38' avec un bloc 4-4-2 bien compacté — Monaco a forcé PSG à 18 passes avant chaque tir en première période",
                "Ben Seghir, seul joueur qui a su trouver les espaces entre les lignes parisiennes — son but illustre ce qu'aurait dû faire toute l'équipe : jouer vite, entre les lignes",
            ],
            "away_faibles": [
                "Zakaria fantôme : 31 touches en 90 minutes pour un milieu défensif censé être le pivot du jeu — c'est la signature d'un pressing adverse qui fonctionne à 100%",
                "Zéro jeu dans la profondeur : Monaco n'a tenté que 4 passes dans le dos des défenseurs parisiens sur tout le match — comment mettre sous pression une défense qui ne défend jamais reculée ?",
                "Embolo en souffrance totale : 12 duels, 3 gagnés — sans combinaisons, sans soutien, un avant-centre seul ne peut rien. Hütter l'a sacrifié en ne lui donnant aucun point d'appui",
                "Transitions défensives indignes du niveau Ligue 1 sur les 2e et 3e buts : Caio Henrique ne sprinte pas pour revenir, Fofana ne ferme pas le couloir — deux buts que la discipline seule pouvait éviter",
            ],
        },
        "verdict": {
            "home_perf": 8.7, "away_perf": 5.9,
            "intensite": 7.5, "spectacle": 7.8,
            "home_txt": "J'ai rarement vu un pressing aussi bien structuré en Ligue 1 cette saison. Luis Enrique a construit quelque chose de rare : une équipe qui court autant sans ballon qu'avec. Fabian Ruiz est le cerveau caché de ce système — quand il est dans ce niveau-là, PSG est imbattable en France. Ce qui m'impressionne, c'est la cohérence collective : aucun joueur ne décide seul, chaque déplacement est une réponse au déplacement d'un coéquipier. C'est du football de haute intensité intellectuelle.",
            "away_txt": "Monaco a le talent pour faire mieux. Beaucoup mieux. La vraie question ce soir, c'est : pourquoi Hütter n'a-t-il pas osé jouer ? Avec Ben Seghir, Akliouche, Minamino — tu as des joueurs capables de déstabiliser n'importe quelle défense en un contre un. Les garder dans un bloc bas pendant 70 minutes, c'est du gâchis pur. Je ne comprends pas la peur tactique de ce soir.",
            "coach_home": "✅ Plan de jeu rigoureux, parfaitement exécuté. La sortie de Mbappé à 70' est la décision la plus intelligente de la soirée — protéger le collectif sur le long terme plutôt que flatter les stats d'un joueur. C'est ça, une mentalité de champion.",
            "coach_away": "❌ Erreur stratégique majeure. À 0-2 à la 60', Hütter devait passer en 4-3-3 offensif avec Gölovin entrant, Ben Seghir libre dans l'axe et Embolo remplacé par un deuxième milieu. Rester en bloc bas dans ces conditions, c'est abandonner le match. Inacceptable.",
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
                "Pick & Roll": "La clé de ce match, c'est ce que les Lakers ont fait défensivement sur le P&R de Curry. Au lieu du drop coverage habituel, Redick a demandé un hedge agressif avec Hachimura qui sort haut sur Curry dès la prise d'écran. Résultat : Curry à 3/9 sur P&R, 6 turnovers. Quand tu enlèves le P&R à Curry, tu enlèves 40% du système offensif des Warriors. Côté Lakers, le P&R Davis–Russell a fonctionné parce que Looney n'a jamais su choisir : couvrir le roll ou le pop ? Davis a marqué 14 points sur cette seule action.",
                "Fast Break": "Les Warriors ont généré 18 points en transition en première mi-temps — et ça aurait pu être 30 si les Lakers n'avaient pas ajusté leur retour défensif à la pause. LeBron a personnellement décidé de sprinter sur chaque transition en 3e quart. Quand le meilleur joueur de ton équipe montre l'exemple défensivement, les autres suivent. C'est du leadership, pas de la tactique. En 2e mi-temps, Golden State n'a marqué que 5 points en contre. Ajustement parfait.",
                "Isolation": "LeBron en isolation côté gauche contre Klay Thompson : c'est une asymétrie que Redick a exploitée à dessein. Thompson à 34 ans n'a plus les jambes pour défendre 4 quarts en premier rideau. LeBron l'a su et l'a abusé à 5 reprises pour provoquer des fautes ou créer des décalages. En face, les isolations Warriors étaient prévisibles et mal servies — Draymond prenait trop de temps pour choisir entre passer et attaquer.",
                "Clutch Time": "Le run 8-0 à 4 minutes de la fin, c'est le moment où on voit la différence entre une équipe qui a appris à gagner et une qui cherche encore comment le faire. Davis en post bas sur Looney, LeBron en drive, Reaves qui plante le 3pts de l'écart définitif — trois actions différentes, trois joueurs différents, un seul objectif. C'est ça une culture de clutch. Warriors : Curry sur fautes à 4'30, aucun autre créateur de shoot capable de prendre ses responsabilités. Le vide a été immense.",
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
                "AD en mode dominant absolu : 32 pts / 14 reb sur Looney, c'est une incompatibilité physique. Kerr aurait dû switcher dès le 2e quart — il ne l'a jamais fait",
                "Ajustement défensif sur Curry à la mi-temps : passer du drop au hedge agressif a complètement cassé le rythme des Warriors en 2e mi-temps. Redick a lu le match",
                "Reaves en décideur : 18 pts et 4/7 à 3pts en sortant du double-écran — les Warriors ne l'ont jamais identifié comme menace prioritaire. Erreur de scouting",
                "Culture clutch : quand Curry sort sur fautes, Lakers ont 3 créateurs différents capables de prendre le match. Golden State n'en a qu'un",
            ],
            "home_faibles": [
                "19 fautes en 48 minutes, dont 4 pour Davis en 3e quart — si Kerr avait mieux joué les possessions hautes, Davis aurait pu sortir à 6 fautes",
                "1er quart à -9 : la défense était trop molle sur les catch-and-shoot Warriors. Si Golden State avait maintenu ce rythme, le match était plié à la mi-temps",
            ],
            "away_forts": [
                "53 points en 1ère mi-temps avec une circulation de balle fluide — le Motion Offense Warriors fonctionne encore quand Curry est propre balle en main",
                "Wiggins : meilleur Warriors cette nuit, 21 pts en jouant sans ballon. Le seul à avoir compris que les Lakers défendaient le ballon, pas les mouvements",
            ],
            "away_faibles": [
                "Curry : 6 turnovers, c'est sa pire nuit de la saison sur ce plan. À chaque fois qu'il était pressé sur P&R, il choisissait la mauvaise option. La défense Lakers l'a lu",
                "Klay Thompson : 43 minutes jouées pour 13 points à 3/11. Kerr lui est trop fidèle. Klay n'a plus les jambes pour défendre ET shooter à ce niveau 4 quarts de suite",
                "Looney contre Davis : -8 en rebonds offensifs, score négatif en +/- (-14). Cette incompatibilité physique devait être gérée avec Kuminga ou Wiseman en pivot",
                "Aucun créateur de clutch hormis Curry : quand il sort sur fautes, Golden State n'a personne capable de créer du shoot en isolation. Lacune structurelle du roster",
            ],
        },
        "verdict": {
            "home_perf": 8.9, "away_perf": 6.4,
            "intensite": 8.2, "spectacle": 8.6,
            "home_txt": "Ce que Redick a construit cette nuit, c'est une leçon de lecture de jeu en temps réel. Identifier la faiblesse Looney–Davis, sur-exploiter le match-up Klay–LeBron, et mettre Reaves en position de décideur face à une défense qui l'ignorait — c'est du coaching de haut niveau. Les jeunes coaches ont intérêt à étudier les ajustements de mi-temps de ce soir. Davis était inarrêtable, mais c'est Redick qui a créé les conditions pour qu'il le soit.",
            "away_txt": "Kerr a perdu ce match dans son vestiaire à la mi-temps. Il avait toutes les informations pour sortir Klay, switcher son plan défensif sur Davis, et remettre Kuminga pour aider Looney. Il n'a rien fait. Dans les grandes confrontations, l'inaction d'un coach est une décision en soi. Ce soir, sa fidélité à des joueurs sur le déclin a coûté la victoire à Golden State.",
            "coach_home": "✅ Ajustement défensif sur Curry en 2e mi-temps : parfait. Décision de laisser Davis en post bas malgré ses 4 fautes plutôt que de le plonger en bench : le bon risque calculé. C'est l'instinct des grands coaches.",
            "coach_away": "❌ Kerr n'a pas vu — ou n'a pas voulu voir — que Klay Thompson n'avait plus rien à apporter offensivement après le 2e quart. 43 minutes pour 3/11 à 3pts, c'est indéfendable. Kuminga aurait changé complètement la dynamique de la peinture.",
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
                "Ruck & Maul": "Le maul est la grande arme de La Rochelle, et O'Gara l'a sorti au bon moment. En 2e mi-temps, sur chaque touche proche des 22m, La Rochelle poussait en maul fermé — et Bordeaux fauchait. 3 pénalités sur maul en 20 minutes. Ce n'est pas de la malchance, c'est une stratégie. O'Gara savait que Bordeaux ne pouvait pas arrêter le maul légalement face à Skelton et Alldritt — alors il les a forcés à fauter. C'est du rugby d'intellectuel.",
                "Touche & Mêlée": "Skelton contre les sauteurs bordelais, c'est un rapport de forces inégal. 8 ballons saisis sur 9 lancers — tu ne perds jamais une touche avec ça. La Rochelle avait une supériorité structurelle en touche que Bordeaux ne pouvait pas corriger en cours de match sans effectuer un changement majeur dans ses alignements. Bru n'a pas eu la lucidité de modifier ses lineouts. En mêlée, Bordeaux a dominé mais n'a pas su transformer cette domination en points.",
                "Jeu au pied": "Jalibert a été brillant au pied : 5/6 pénalités, territoire parfaitement géré en 1ère période. Mais ce qui m'a frappé, c'est qu'après le 3-1 au score en points, Bordeaux a arrêté de jouer au pied pour attaquer à mains nues. Erreur de lecture. Contre La Rochelle, tu gardes le pied — tu les pousses dans leur camp, tu les fatigues, tu attends leurs erreurs. Vouloir marquer des essais supplémentaires quand tu mènes de 8 en fin de match, c'est de l'ego, pas de la tactique.",
                "Défense en ligne": "La défense en rideau de La Rochelle en 2e mi-temps a été irréprochable sur les séquences ouvertes. Bordeaux a tenté 6 combinaisons côté ouvert dans les 25 dernières minutes — 6 fois repoussées. La Rochelle avait compris le jeu de Bordeaux mieux que Bordeaux lui-même. Quand ta défense lit toutes tes attaques, tu dois changer de plan. Bordeaux n'a pas su.",
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
                "Mêlée : 5/5, c'est une domination totale. Les piliers bordelais ont étouffé le pack rochelais — cette plateforme de jeu aurait dû être la base d'une victoire clinique",
                "Jalibert au pied : 5/6 en pénalités, jeu territorial précis qui a mis La Rochelle en difficulté constante dans son propre camp en 1ère période",
                "Construction du jeu propre et rapide en 1ère mi-temps : Lucu a bien géré le rythme, Bordeaux a dominé sans forcément risquer",
            ],
            "home_faibles": [
                "11 pénalités concédées — c'est 11 cadeaux offerts à La Rochelle. En rugby professionnel, perdre à 3 pénalités près dans les 20 dernières minutes quand tu mènes de 8, c'est une faute professionnelle collective",
                "Schémas d'attaque trop lisibles en 2e mi-temps : Bordeaux a répété les mêmes combinations sur le côté ouvert 4 fois de suite — La Rochelle a fini par les anticiper les yeux fermés",
                "2 mauls arrêtés dans les 5 mètres adverses : quand tu es à 5m et que tu n'arrives pas à marquer, tu offres un momentum psychologique immense à l'adversaire",
            ],
            "away_forts": [
                "Alldritt : 14 plaquages, ballons portés décisifs, présence constante au ruck. Ce type est le meilleur N°8 du Top 14 et il l'a prouvé une fois de plus sous la pression maximale",
                "Skelton en touche : 8 ballons saisis, 86% de maîtrise. C'est lui qui a permis à La Rochelle de relancer son jeu à chaque possession en 2e mi-temps — un avantage structurel énorme",
                "Résilience mentale : mener 21-13 contre toi à la 60', à Bordeaux, dans une demi de Champions Cup — et continuer à croire. C'est ça une équipe bâtie par O'Gara",
                "Essai de Berdeu à la 76' : timing parfait, décision de passer ou courir prise en une fraction de seconde. Les champions marquent quand ça compte",
            ],
            "away_faibles": [
                "1ère période catastrophique : trop de pénalités, trop de ballons perdus en touche défensive — La Rochelle a offert à Bordeaux 18 points qu'ils n'auraient jamais dû concéder",
                "Mêlée sous pression en 1ère période : les piliers de Bordeaux ont mis Priso et les siens en difficulté, forçant des fautes à des moments clés",
            ],
        },
        "verdict": {
            "home_perf": 6.8, "away_perf": 8.1,
            "intensite": 9.2, "spectacle": 8.7,
            "home_txt": "Bordeaux a perdu un match qu'il ne pouvait pas perdre. 21-13 à la 60', à domicile, en Champions Cup — cette défaite va marquer les esprits pour longtemps. Ce que je n'accepte pas, c'est la gestion des 20 dernières minutes. Quand tu mènes de 8 et que l'adversaire n'a pas cassé ta défense, tu n'attaques plus. Tu gardes le ballon. Tu cours les phases. Tu fais fauter l'adversaire. Bordeaux a continué à jouer court et ouvert — et c'est là qu'ils ont concédé les 3 pénalités fatales. C'est un problème de culture et de maturité collective.",
            "away_txt": "O'Gara a fait un travail exceptionnel à la mi-temps. Changer le point d'attaque, utiliser Skelton comme cible prioritaire, et simplifier le jeu en allant droit devant — c'est l'analyse exacte d'un entraîneur qui sait lire un match. La Rochelle a été mauvaise 40 minutes et excellente 40 minutes. C'est les équipes de champions qui peuvent faire ça — être mauvais et quand même gagner grâce à l'organisation et au mental.",
            "coach_home": "❌ Bru a commis une erreur de gestion fondamentale. À 21-13, tu passes en mode conservation : maul, jeu au pied rasant, phases lentes, tu épuises le temps. Continuer à attaquer à mains nues dans les 22m adverses à ce moment du match, c'est prendre des risques inutiles. La sortie de Woki trop tôt a aussi affaibli sa conquête en fin de match — c'est inexplicable.",
            "coach_away": "✅ O'Gara mérite 10/10 pour ses ajustements de mi-temps. Il a identifié que Skelton était le facteur X en touche, que Bordeaux ne pouvait pas stopper le maul, et que la discipline adverse allait craquer sous pression en fin de match. Il avait tout vu. Et son équipe a exécuté.",
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
    return {
        "sport": sport,
        "competition": comp,
        "date": (ev.get("strDate") or "")[:10],
        "time": (ev.get("strTime") or "")[:5],
        "stadium": ev.get("strVenue") or "",
        "status": _tsdb_status(ev.get("strStatus") or ""),
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
            debug_info: dict = {}
            connection_error = False

            for lid, comp in target_ids.items():
                events = _tsdb_day_league(target_date, lid)
                if events is None:
                    connection_error = True
                    debug_info[comp] = "❌ Connexion impossible"
                else:
                    debug_info[comp] = f"{len(events)} événement(s)"
                    for ev in events:
                        mid = str(ev.get("idEvent", f"{lid}_{ev.get('strEvent','')}"))
                        result[mid] = _tsdb_to_match(ev, comp, sport)

            with st.expander("🔍 Debug API TheSportsDB", expanded=False):
                st.caption(f"Date : `{target_date}` · Compétitions filtrées : {list(target_ids.values())}")
                for comp, info in debug_info.items():
                    lid = COMP_TO_LID.get(comp, "?")
                    st.caption(f"**{comp}** (id={lid}) → {info}")

            if connection_error and not result:
                st.error(
                    "⚠️ **TheSportsDB inaccessible** — vérifiez votre connexion. "
                    "Les données simulées sont affichées à la place.",
                    icon="🔌",
                )
            elif not result:
                st.info("Aucun match trouvé pour cette date dans les compétitions sélectionnées.", icon="📭")

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
            for comp in competitions:
                if comp not in COMP_TO_LID:
                    continue
                for ev in _tsdb_league_recent(COMP_TO_LID[comp]):
                    mid = str(ev.get("idEvent", ""))
                    if mid:
                        result[mid] = _tsdb_to_match(ev, comp, sport)
            return result
        return {
            mid: m for mid, m in MATCHES.items()
            if m["sport"] == sport and m["competition"] in competitions
        }

    @staticmethod
    def get_analysis(match_id: str) -> dict | None:
        # Analysis always comes from the hardcoded expert data for now.
        # Future: call an AI provider here when match_id is a live TSDB event ID.
        return ANALYSIS.get(match_id)

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
if "comp_filter" not in st.session_state:
    st.session_state.comp_filter = set()

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
            d = st.session_state.selected_date.replace(day=1) - timedelta(days=1)
            st.session_state.selected_date = d.replace(day=min(st.session_state.selected_date.day, cal_mod.monthrange(d.year, d.month)[1]))
    with nav_col2:
        st.markdown(f'<p style="text-align:center;font-weight:700;font-size:.9rem;color:#f0f0f0;">{st.session_state.selected_date.strftime("%B %Y").capitalize()}</p>', unsafe_allow_html=True)
    with nav_col3:
        if st.button("▶", key="next_m"):
            d = st.session_state.selected_date.replace(day=28) + timedelta(days=4)
            st.session_state.selected_date = d.replace(day=min(st.session_state.selected_date.day, cal_mod.monthrange(d.year, d.month)[1]))

    yr, mo = st.session_state.selected_date.year, st.session_state.selected_date.month
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

filtered = DataLayer.get_matches(date_str, st.session_state.sport, active_comps)
all_sport = DataLayer.get_all_for_sport(st.session_state.sport, active_comps)

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
    items = list(filtered.items())
    # Render in pairs so each row shares the same st.columns() → cards stay aligned
    for i in range(0, len(items), 2):
        pair = items[i:i+2]
        cols = st.columns(2)
        for col, (mid, m) in zip(cols, pair):
            with col:
                html = render_match_card(mid, m, st.session_state.selected_match == mid)
                st.markdown(html, unsafe_allow_html=True)
                if DataLayer.get_analysis(mid) is not None:
                    if st.button("🔍 Analyser", key=f"sel_{mid}", use_container_width=True):
                        st.session_state.selected_match = None if st.session_state.selected_match == mid else mid
                        st.rerun()
                else:
                    st.button("📅 À venir", key=f"sel_{mid}", disabled=True, use_container_width=True)
        st.markdown('<div style="margin-bottom:.75rem;"></div>', unsafe_allow_html=True)
else:
    st.markdown(
        f'<div style="background:#111;border:1px solid #1a1a1a;border-radius:12px;padding:2rem;text-align:center;">'
        f'<p style="color:#444;font-size:1rem;">Aucun match {st.session_state.sport} le {date_label}.</p>'
        f'<p style="color:#333;font-size:.85rem;">Essayez une autre date.</p></div>',
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
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS PANEL
# ══════════════════════════════════════════════════════════════════════════════
_sel = st.session_state.selected_match
_an = DataLayer.get_analysis(_sel) if _sel else None
if _sel and _an and _sel in MATCHES:
    mid = _sel
    m = MATCHES[mid]
    an = _an
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
