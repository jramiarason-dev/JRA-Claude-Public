import streamlit as st
import os
import re
import hashlib
import random as _rng_mod
import json
from pathlib import Path
from datetime import date, datetime, timedelta
import calendar as cal_mod

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CoachIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""<style>
body, .stApp { background: #070b14 !important; }
#MainMenu, footer, header { visibility: hidden; height: 0; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
[data-testid="stSidebar"] { display: none; }
iframe { border: 0 !important; }
</style>""", unsafe_allow_html=True)


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
    "monaco_partizan_euro": {
        "sport": "🏀 Basket", "competition": "Euroleague",
        "date": D_M5, "time": "20:30", "stadium": "Salle Gaston Médecin, Monaco", "status": "Terminé",
        "home": {"name": "AS Monaco Basket","short": "MCO","color": "#B5121B", "score": 78},
        "away": {"name": "Partizan Belgrade","short": "PAR","color": "#000000", "score": 82},
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
    "gravelines_nancy_bet": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_M2, "time": "20:30", "stadium": "Sportica, Gravelines-Dunkerque", "status": "Terminé",
        "home": {"name": "BCM Gravelines-Dunkerque","short": "GRA","color": "#E31B23", "score": 88},
        "away": {"name": "SLUC Nancy Basket",        "short": "NAN","color": "#0055A4", "score": 82},
    },
    "monaco_lemans_bet": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_P4, "time": "20:00", "stadium": "Salle Gaston Médecin, Monaco", "status": "À venir",
        "home": {"name": "AS Monaco Basket","short": "MCO","color": "#B5121B", "score": None},
        "away": {"name": "Le Mans Sarthe Basket","short": "MSB","color": "#E30613", "score": None},
    },
    "asvel_monaco_basket": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_M9, "time": "20:00", "stadium": "Astroballe, Villeurbanne", "status": "Terminé",
        "home": {"name": "LDLC ASVEL",        "short": "ASV", "color": "#C8102E", "score": 88},
        "away": {"name": "AS Monaco Basket",  "short": "MCB", "color": "#B5121B", "score": 79},
    },
    "paris_basket_strasbourg": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_M7, "time": "19:00", "stadium": "Salle Pierre de Coubertin, Paris", "status": "Terminé",
        "home": {"name": "Paris Basketball", "short": "PAB", "color": "#1A1A1A", "score": 92},
        "away": {"name": "SIG Strasbourg",   "short": "SIG", "color": "#003C8F", "score": 80},
    },
    "asvel_paris_basket": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_P3, "time": "20:00", "stadium": "Astroballe, Villeurbanne", "status": "À venir",
        "home": {"name": "LDLC ASVEL",       "short": "ASV", "color": "#C8102E", "score": None},
        "away": {"name": "Paris Basketball", "short": "PAB", "color": "#1A1A1A", "score": None},
    },
    "monaco_basket_nanterre": {
        "sport": "🏀 Basket", "competition": "Betclic Elite",
        "date": D_P5, "time": "19:30", "stadium": "Salle Gaston Médecin, Monaco", "status": "À venir",
        "home": {"name": "AS Monaco Basket", "short": "MCB", "color": "#B5121B", "score": None},
        "away": {"name": "JSF Nanterre",     "short": "NAN", "color": "#CC0000", "score": None},
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
    # ── Ligue 1 2025-26 résultats réels ──────────────────────────────────────
    "psg_toulouse_l1_aug": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": "2025-08-30", "time": "21:00", "stadium": "Parc des Princes, Paris", "status": "Terminé",
        "home": {"name": "Paris Saint-Germain", "short": "PSG", "color": "#004174", "score": 6},
        "away": {"name": "Toulouse FC", "short": "TFC", "color": "#6B2D8B", "score": 3},
    },
    "lorient_lille_l1_aug": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": "2025-08-30", "time": "17:00", "stadium": "Stade du Moustoir, Lorient", "status": "Terminé",
        "home": {"name": "FC Lorient", "short": "LOR", "color": "#FF6600", "score": 1},
        "away": {"name": "LOSC Lille", "short": "LIL", "color": "#C41E3A", "score": 7},
    },
    "strasbourg_angers_l1_oct": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": "2025-10-05", "time": "15:00", "stadium": "Stade de la Meinau, Strasbourg", "status": "Terminé",
        "home": {"name": "RC Strasbourg", "short": "RCS", "color": "#1A5C9C", "score": 5},
        "away": {"name": "Angers SCO", "short": "ANG", "color": "#000000", "score": 0},
    },
    "lille_metz_l1_oct": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": "2025-10-26", "time": "15:00", "stadium": "Stade Pierre-Mauroy, Lille", "status": "Terminé",
        "home": {"name": "LOSC Lille", "short": "LIL", "color": "#C41E3A", "score": 6},
        "away": {"name": "FC Metz", "short": "MET", "color": "#8B0000", "score": 1},
    },
    "marseille_brest_l1_nov": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": "2025-11-08", "time": "21:00", "stadium": "Stade Vélodrome, Marseille", "status": "Terminé",
        "home": {"name": "Olympique de Marseille", "short": "OM", "color": "#009BDE", "score": 3},
        "away": {"name": "Stade Brestois", "short": "SB29", "color": "#E63329", "score": 0},
    },
    "psg_rennes_l1_dec": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": "2025-12-06", "time": "21:00", "stadium": "Parc des Princes, Paris", "status": "Terminé",
        "home": {"name": "Paris Saint-Germain", "short": "PSG", "color": "#004174", "score": 5},
        "away": {"name": "Stade Rennais", "short": "SRF", "color": "#DD0000", "score": 0},
    },
    "monaco_lorient_l1_jan": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": "2026-01-16", "time": "21:00", "stadium": "Stade Louis-II, Monaco", "status": "Terminé",
        "home": {"name": "AS Monaco", "short": "ASM", "color": "#E8231A", "score": 1},
        "away": {"name": "FC Lorient", "short": "LOR", "color": "#FF6600", "score": 3},
    },
    "psg_marseille_clasico": {
        "sport": "⚽ Football", "competition": "Ligue 1",
        "date": "2026-02-08", "time": "21:00", "stadium": "Parc des Princes, Paris", "status": "Terminé",
        "home": {"name": "Paris Saint-Germain", "short": "PSG", "color": "#004174", "score": 5},
        "away": {"name": "Olympique de Marseille", "short": "OM", "color": "#009BDE", "score": 0},
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
        'name': 'Jean-Louis Gasset (fév 2026)',
        'nationality': '🇫🇷',
        'formation': '4-2-3-1',
        'style': 'Jeu offensif, organisation, nouveau projet après De Zerbi',
        'philosophy': 'Football offensif et technique. Après le départ de De Zerbi (11 fév 2026), nouveau projet avec Gasset depuis le 18 fév 2026.',
        'strengths': ['Greenwood meilleur buteur L1', 'Vélodrome 12ème homme', 'Effectif international'],
        'weaknesses': ['Transition coaching difficile', 'Vulnérable aux contres'],
        'key_principles': ['Jeu offensif assumé', 'Largeurs exploitées', 'Transitions rapides']
    },
    'Monaco': {
        'name': 'Luca Mancini (depuis oct 2025)',
        'nationality': '🇮🇹',
        'formation': '4-2-3-1',
        'style': 'Pressing intense, jeu direct et vertical',
        'philosophy': 'Hütter licencié le 9 oct 2025, nouveau coach depuis le 11 oct 2025. Équipe très physique et verticale avec Ansu Fati comme option offensive.',
        'strengths': ['Intensité physique très élevée', 'Efficacité en transition', 'Pressing collectif'],
        'weaknesses': ['Transition coaching en cours', 'Peut manquer de patience en possession'],
        'key_principles': ['Transition défense-attaque rapide', 'Pressing immédiat', 'Verticalité maximale']
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
        'name': 'Nouveau coach (jan 2026)',
        'nationality': '🇫🇷',
        'formation': '4-3-3',
        'style': 'Pressing haut, jeu direct, largeur maximale',
        'philosophy': 'Haise licencié le 29 déc 2025, nouveau coach depuis jan 2026. Équipe en difficulté (15e), Sofiane Diop principal danger offensif.',
        'strengths': ['Pressing haut', 'Largeurs maximales', 'Diop talent offensif'],
        'weaknesses': ['Bas du classement', 'Transition coaching difficile', 'Pire défense (44 BC)'],
        'key_principles': ['Pressing immédiat', 'Ailiers hauts', 'Jeu direct']
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
        'name': 'Nouveau coach (jan 2026)',
        'nationality': '🇫🇷',
        'formation': '4-2-3-1',
        'style': 'Jeu de possession, organisation défensive',
        'philosophy': 'Rosenior parti à Chelsea le 6 jan 2026, nouveau coach depuis jan 2026. Panichelli (12 buts) reste le danger principal.',
        'strengths': ['Organisation collective', 'Panichelli meilleur buteur', 'Solidité défensive'],
        'weaknesses': ['Transition coaching', 'Effectif sous pression'],
        'key_principles': ['Possession maîtrisée', 'Bloc défensif compact', 'Exploitation Panichelli']
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
    'Nantes': {
        'name': 'Nouveau coach (déc 2025)',
        'nationality': '🇫🇷',
        'formation': '4-4-2',
        'style': 'Jeu direct, combativité, duels physiques',
        'philosophy': 'Coach démissionné le 11 déc 2025, nouveau depuis le 16 déc. Football direct et combatif, maintien difficile en bas de classement.',
        'strengths': ['Combativité', 'Jeu aérien', 'Mental compétiteur'],
        'weaknesses': ['Bas du classement', 'Effectif en manque de confiance'],
        'key_principles': ['Jeu direct', 'Duels physiques gagnés', 'Mental combatif']
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
    'lorient_coach': {
        'name': 'Régis Le Bris',
        'nationality': '🇫🇷 Français',
        'formation': '4-3-3',
        'style': 'Jeu offensif direct, transitions rapides, identité bretonne',
        'philosophy': 'Football offensif, pressing haut, identité régionale forte',
        'strengths': ['Transitions rapides', 'Pressing', 'Cohésion'],
        'weaknesses': ['Maintien niveau Ligue 1', 'Effectif limité'],
        'key_principles': ['Pressing haut', 'Fast break offensif', 'Compacité défensive']
    },
    'kombouare': {
        'name': 'Antoine Kombouaré',
        'nationality': '🇫🇷 Français',
        'formation': '4-4-2',
        'style': 'Organisation défensive, pragmatisme, expérience Ligue 1',
        'philosophy': 'Solidité défensive avant tout, exploitation des transitions',
        'strengths': ['Organisation défensive', 'Expérience L1', 'Solidité'],
        'weaknesses': ['Jeu offensif limité', 'Nouveau en L1 après 46 ans'],
        'key_principles': ['Bloc bas organisé', 'Contre-attaques', 'Solidité défensive']
    },
    'metz_coach': {
        'name': 'À confirmer (poste vacant suite licenciement 20 jan 2026)',
        'nationality': '🇫🇷',
        'formation': '4-5-1',
        'style': 'Reconstruction difficile, retour en L1 compliqué',
        'philosophy': 'Solidité défensive pour tenter le maintien',
        'strengths': ['Stade historique', 'Soutien supporters'],
        'weaknesses': ['Dernière place', 'Pire défense L1 (-31)'],
        'key_principles': ['Défense compacte', 'Limiter les dégâts', 'Transition']
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
        'name': 'Mike Brown',
        'nationality': '🇺🇸',
        'formation': 'Up-tempo Offense',
        'style': 'Jeu rapide, De\'Aaron Fox explosif, Sabonis playmaker intérieur',
        'philosophy': 'Rythme de jeu élevé autour de De\'Aaron Fox. Sabonis comme playmaker intérieur unique. Transitions rapides et scoring offensif élevé. Défense organisée sous Mike Brown.',
        'strengths': ['Fox explosif', 'Sabonis playmaker', 'Rythme élevé', 'Scoring offensif'],
        'weaknesses': ['Défense perfectible', 'Cohésion collective'],
        'key_principles': ['Transitions Fox', 'Sabonis playmaker intérieur', 'Rythme élevé', 'Scoring prioritaire']
    },
    '76ers': {
        'name': 'Nick Nurse',
        'nationality': '🇺🇸',
        'formation': 'Versatile Defense / Pick and Roll',
        'style': 'Défense polyvalente, Embiid-Maxey duo dominant',
        'philosophy': 'Défense d\'élite avec rotations parfaites sous Nick Nurse. Attaque centrée sur Embiid en isolation et pick and roll. Maxey comme meneur explosif. Tirs à 3 points pour George. Adaptabilité tactique maximale.',
        'strengths': ['Embiid dominant', 'Défense polyvalente', 'Maxey explosif', 'George shooteur'],
        'weaknesses': ['Blessures Embiid', 'Cohésion collective', 'Régularité'],
        'key_principles': ['Embiid isolation', 'Pick and roll Embiid-Maxey', 'Défense polyvalente', 'George spacing']
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
    # ── La Liga ───────────────────────────────────────────────────────────────
    'Real Madrid': {
        'name': 'Carlo Ancelotti',
        'nationality': '🇮🇹',
        'formation': '4-3-3 / 4-4-2',
        'style': 'Pragmatisme élégant, liberté aux stars',
        'philosophy': 'Gestionnaire de stars hors pair. Laisse une grande liberté aux joueurs de talent. S\'adapte tactiquement selon les adversaires. Défense solide basée sur la compacité. Transitions rapides exploitant Vinicius et Mbappé. Calme et expérience en toutes circonstances.',
        'strengths': ['Gestion des stars', 'Adaptabilité tactique', 'Expérience Champions League', 'Calme sous pression'],
        'weaknesses': ['Peut manquer de pressing organisé', 'Plan B parfois trop conservateur'],
        'key_principles': ['Liberté créative aux stars', 'Compacité défensive', 'Transitions rapides', 'Pragmatisme']
    },
    'Barcelona': {
        'name': 'Hansi Flick',
        'nationality': '🇩🇪',
        'formation': '4-2-3-1 / 4-3-3',
        'style': 'Gegenpressing très haut, jeu offensif total',
        'philosophy': 'Pressing très haut inspiré du gegenpressing allemand. Récupération haute du ballon convertie directement en occasions. Jeu offensif total avec participation de tous les joueurs. Yamal et Pedri comme piliers du jeu. Exigence tactique maximale. Retour aux valeurs du jeu barcelonais.',
        'strengths': ['Gegenpressing ultra-efficace', 'Jeu offensif total', 'Yamal-Pedri comme colonne vertébrale', 'Récupération haute'],
        'weaknesses': ['Vulnérable aux contres rapides', 'Physiquement exigeant sur la durée'],
        'key_principles': ['Gegenpressing immédiat', 'Récupération haute', 'Jeu offensif total', 'Pressing coordonné']
    },
    'Atletico': {
        'name': 'Diego Simeone',
        'nationality': '🇦🇷',
        'formation': '4-4-2 / 5-3-2',
        'style': 'Défense ultra-solide, transitions meurtrières',
        'philosophy': 'Le Cholo system — défense ultra-solide et compacte. Bloc très bas en phase défensive. Transitions offensives meurtrières vers Griezmann et Julián Álvarez. Intensité physique et mentale maximale. Pression psychologique sur les adversaires. L\'un des meilleurs coachs défensifs de l\'histoire.',
        'strengths': ['Défense légendaire', 'Transitions meurtrières', 'Intensité physique et mentale', 'Mental d\'acier collectif'],
        'weaknesses': ['Parfois prévisible offensivement', 'Dépendance au bloc bas'],
        'key_principles': ['Bloc bas compact', 'Transition ultra-rapide', 'Intensité physique maximale', 'Mental collectif']
    },
    'Sevilla': {
        'name': 'García Pimienta',
        'nationality': '🇪🇸',
        'formation': '4-2-3-1',
        'style': 'Possession structurée, organisation défensive',
        'philosophy': 'Football de possession structuré. Organisation défensive sérieuse. Développement collectif progressif. Reconstruction de Séville après années difficiles. Circuits de passes bien définis.',
        'strengths': ['Organisation défensive', 'Possession structurée', 'Développement collectif'],
        'weaknesses': ['Manque de profondeur offensive', 'Résultats irréguliers'],
        'key_principles': ['Possession patient', 'Organisation défensive', 'Construction collective']
    },
    'Betis': {
        'name': 'Manuel Pellegrini',
        'nationality': '🇨🇱',
        'formation': '4-2-3-1 / 4-3-3',
        'style': 'Possession élégante, football propre et technique',
        'philosophy': 'Football élégant basé sur la possession. Jeu de passes fluide et agréable à regarder. Organisation défensive solide. Valorisation des joueurs techniques comme Isco et Lo Celso. Patience en possession et création d\'espaces.',
        'strengths': ['Possession élégante', 'Joueurs techniques valorisés', 'Organisation défensive', 'Jeu fluide'],
        'weaknesses': ['Peut manquer d\'efficacité offensive', 'Vulnérable sur les contres'],
        'key_principles': ['Possession technique', 'Jeu fluide et patient', 'Équilibre défensif', 'Valorisation des créateurs']
    },
    'Athletic': {
        'name': 'Ernesto Valverde',
        'nationality': '🇪🇸',
        'formation': '4-2-3-1 / 4-3-3',
        'style': 'Pressing intense, identité basque, physique',
        'philosophy': 'Identité basque au cœur absolu du projet. Pressing intense et physique. Jeu direct exploitant la vitesse des Williams. Solidarité collective absolue. Fierté et appartenance comme moteurs permanents. L\'exception basque du football mondial.',
        'strengths': ['Identité basque incomparable', 'Pressing physique intense', 'Solidarité collective', 'Williams Brothers'],
        'weaknesses': ['Recrutement limité à la Cantera basque', 'Peut manquer de créativité technique'],
        'key_principles': ['Pressing intense', 'Jeu direct Williams', 'Identité basque', 'Solidarité absolue']
    },
    'Villarreal': {
        'name': 'Marcelino',
        'nationality': '🇪🇸',
        'formation': '4-4-2 / 4-3-3',
        'style': 'Organisation défensive, collectif efficace',
        'philosophy': 'Organisation défensive très solide comme priorité. Jeu collectif bien rodé. Exploitation des individualités offensives. Efficacité sur les coups de pied arrêtés. Solidité tactique comme arme principale.',
        'strengths': ['Organisation défensive', 'Efficacité collective', 'CPA bien travaillés'],
        'weaknesses': ['Manque de star offensive', 'Résultats irréguliers'],
        'key_principles': ['Organisation défensive', 'Efficacité collective', 'CPA', 'Solidité tactique']
    },
    'Real Sociedad': {
        'name': 'Imanol Alguacil',
        'nationality': '🇪🇸',
        'formation': '4-3-3',
        'style': 'Possession technique, pressing organisé',
        'philosophy': 'Football de possession technique à l\'espagnole. Pressing bien organisé par zones. Exploitation des couloirs avec des ailiers rapides. Développement des jeunes de la Cantera basque. Jeu offensif propre et agréable.',
        'strengths': ['Possession technique', 'Pressing organisé', 'Développement jeunes', 'Jeu offensif propre'],
        'weaknesses': ['Manque de profondeur en playoffs européens', 'Irrégularité défensive'],
        'key_principles': ['Possession technique', 'Pressing zones', 'Couloirs exploités', 'Cantera valorisée']
    },
    'Valencia': {
        'name': 'Carlos Corberán',
        'nationality': '🇪🇸',
        'formation': '4-2-3-1',
        'style': 'Pressing intense, identité forte, résilience',
        'philosophy': 'Pressing intense malgré les difficultés du club. Identité forte et résilience collective. Jeu direct et physique. Exploitation de la vitesse de Duro et Dani Gómez. Construction dans l\'adversité.',
        'strengths': ['Intensité physique', 'Résilience collective', 'Pressing organisé'],
        'weaknesses': ['Contexte financier difficile', 'Effectif limité'],
        'key_principles': ['Pressing intense', 'Jeu direct', 'Résilience', 'Identité forte']
    },
    'Osasuna': {
        'name': 'Vicente Moreno',
        'nationality': '🇪🇸',
        'formation': '4-4-2',
        'style': 'Bloc compact, physique, efficacité',
        'philosophy': 'Bloc défensif très compact et bien organisé. Football physique et direct. Efficacité maximale avec les moyens disponibles. Contre-attaques rapides. Culture de la solidarité collective.',
        'strengths': ['Solidité défensive', 'Physicalité', 'Contre-attaques', 'Solidarité'],
        'weaknesses': ['Jeu offensif limité', 'Manque de technique collective'],
        'key_principles': ['Bloc compact', 'Physicalité', 'Contre-attaques', 'Solidarité']
    },
    'Girona': {
        'name': 'Míchel',
        'nationality': '🇪🇸',
        'formation': '4-3-3',
        'style': 'Pressing haut, jeu offensif, intensité',
        'philosophy': 'Pressing très haut et jeu offensif courageux. Héritage de la révolution Girona sous Míchel. Équipe compacte et difficile à jouer. Exploitation des espaces en transition rapide.',
        'strengths': ['Pressing offensif', 'Intensité collective', 'Courage tactique'],
        'weaknesses': ['Effectif limité', 'Irrégularité en saison longue'],
        'key_principles': ['Pressing haut', 'Jeu offensif', 'Transitions rapides', 'Intensité']
    },
    'Rayo': {
        'name': 'Íñigo Pérez',
        'nationality': '🇪🇸',
        'formation': '4-4-2 / 4-3-3',
        'style': 'Jeu direct, pressing, identité de quartier',
        'philosophy': 'Football direct et combat. Identité populaire de Vallecas au cœur du projet. Pressing intense malgré le budget limité. Jeu direct et combatif. Fierté du quartier comme moteur.',
        'strengths': ['Combativité', 'Identité forte', 'Pressing intense', 'Mental collectif'],
        'weaknesses': ['Effectif très limité', 'Manque de technique collective'],
        'key_principles': ['Jeu direct', 'Combativité', 'Identité Vallecas', 'Pressing']
    },
    # ── Betclic Elite ─────────────────────────────────────────────────────────
    'Monaco Basket': {
        'name': 'Sasa Obradovic',
        'nationality': '🇷🇸',
        'formation': 'Iso James / Pick & Roll Heavy',
        'style': 'Isolation Mike James, pick and roll intense, défense agressive Mirotic spacing',
        'philosophy': 'Exploitation maximale de l\'isolation de Mike James. Pick and roll avec Motiejunas. Mirotic comme spacing intérieur. Défense agressive show & recover. Rythme modéré avec tempo maîtrisé.',
        'strengths': ['Mike James intenable', 'Mirotic spacing élite', 'Pick & Roll', 'Défense agressive'],
        'weaknesses': ['Dépendance à Mike James', 'Cohésion à construire'],
        'key_principles': ['Iso James prioritaire', 'Pick & Roll', 'Défense show & recover', 'Mirotic spacing']
    },
    'Paris Basket': {
        'name': 'Tuomas Iisalo',
        'nationality': '🇫🇮',
        'formation': 'Ultra High Pace / Press',
        'style': 'Tempo ultra-rapide, pression full court, jeu de steals',
        'philosophy': 'Rythme extrêmement élevé avec pression défensive sur tout le terrain. Drag screens pour accélérer les transitions. Full court press pour générer des steals. Jeu offensif frénétique autour de TJ Shorts et Fredrick.',
        'strengths': ['TJ Shorts exceptionnel', 'Rythme ultra-élevé', 'Pression défensive', 'Kahudi expérience'],
        'weaknesses': ['Fatigue physique accumulée', 'Dépendance au tempo'],
        'key_principles': ['Full court press', 'Drag screens transition', 'Rythme maximal', 'TJ Shorts libre']
    },
    'ASVEL': {
        'name': 'TJ Parker',
        'nationality': '🇫🇷',
        'formation': 'Pick & Roll / Motion Offense',
        'style': 'Jeu dynamique autour de Larkin et Bogdanovic, scoring élite, défense physique',
        'philosophy': 'Construction du jeu autour de Shane Larkin meneur clutch. Bogdanovic scoreur élite extérieur. De Colo vétéran expérimenté. Culture gagnante ASVEL sous Tony Parker.',
        'strengths': ['Larkin clutch Euroleague', 'Bogdanovic scoring élite', 'De Colo expérience', 'Culture gagnante'],
        'weaknesses': ['Fatigue cumul Euroleague-ProA', 'Pression des attentes'],
        'key_principles': ['PnR Larkin', 'Bogdanovic scoring', 'Drop coverage', 'Leadership De Colo']
    },
    'JL Bourg': {
        'name': 'Frédéric Fauthoux',
        'nationality': '🇫🇷',
        'formation': 'Motion Offense / Extra Pass',
        'style': 'Motion offense fluide, extra pass, switching défensif',
        'philosophy': 'Motion offense basée sur la circulation du ballon et les passes supplémentaires. Défense par switching sur les écrans. Rythme de jeu équilibré. Exploitation de Castaneda et Ayayi comme créateurs.',
        'strengths': ['Système collectif cohérent', 'Spacing offensif', 'Switch défensif', 'Profondeur roster'],
        'weaknesses': ['Manque de superstar', 'Régularité défensive'],
        'key_principles': ['Extra pass', 'Motion offense', 'Screen switching', 'Rythme équilibré']
    },
    'Cholet': {
        'name': 'Fabrice Lefrançois',
        'nationality': '🇫🇷',
        'formation': 'Low Post / Hard Hedge',
        'style': 'Jeu intérieur Vautier, écrans successifs, hedge agressif',
        'philosophy': 'Exploitation du poste bas de Bastien Vautier comme ancre offensive. Écrans successifs (stagger screens) pour libérer les tireurs. Défense hard hedge agressive sur les ball screens. Identité défensive forte.',
        'strengths': ['Vautier dominant intérieur', 'Défense hard hedge', 'Culture club solide', 'Formation locale'],
        'weaknesses': ['Budget modeste', 'Profondeur offensive limitée'],
        'key_principles': ['Low post Vautier', 'Stagger screens', 'Hard hedge défensif', 'Jeu lent et patient']
    },
    'Nanterre 92': {
        'name': 'Philippe Da Silva',
        'nationality': '🇫🇷',
        'formation': 'Run & Gun / 3PT Heavy',
        'style': 'Jeu rapide, tirs à 3 points massifs, pression défensive',
        'philosophy': 'Run & gun à haut rythme avec multiplication des tentatives à 3 points. Pression défensive avec rotation rapide. Frank Jackson comme scoreur principal. Exploitation du spacing et des déplacements sans ballon.',
        'strengths': ['Jackson scoreur élite', 'Rythme élevé', 'Volume 3 points', 'Pression défensive'],
        'weaknesses': ['Irrégularité tir extérieur', 'Défense en transition'],
        'key_principles': ['Run & gun', '3PT volume élevé', 'Garde pression ballon', 'Jackson scoreur']
    },
    'Saint-Quentin': {
        'name': 'Julien Mahé',
        'nationality': '🇫🇷',
        'formation': 'Half-Court Execution / No Middle',
        'style': 'Exécution demi-terrain, set plays, défense no-middle élite',
        'philosophy': 'Maîtrise totale de l\'exécution en demi-terrain avec des set plays parfaitement huilés. Défense half-court de niveau élite avec interdiction du milieu. Boucaud comme meneur organisateur. Discipline collective maximale.',
        'strengths': ['Exécution set plays', 'Défense half-court élite', 'Discipline collective', 'Fatiguer adverse'],
        'weaknesses': ['Rythme trop lent par moments', 'Scoring limité en transition'],
        'key_principles': ['Half-court execution', 'No middle defense', 'Set plays', 'Discipline collective']
    },
    'Le Mans': {
        'name': 'Guillaume Vizade',
        'nationality': '🇫🇷',
        'formation': 'Drive & Kick / Rim Protection',
        'style': 'Drive & kick, spacing athlétique, protection cercle',
        'philosophy': 'Drive and kick autour de Buchanan et Ndoye comme pénétrateurs. Spacing athlétique pour les kick-outs. Protection du cercle par Mawugbe. Défense de déni sur les ailes.',
        'strengths': ['Buchanan dynamique', 'Protection cercle Mawugbe', 'Spacing offensif', 'Athlétisme'],
        'weaknesses': ['Manque de shooteurs réguliers', 'Profondeur limitée'],
        'key_principles': ['Drive & kick', 'Mawugbe rim protection', 'Deny wings', 'Athlétisme collectif']
    },
    'JDA Dijon': {
        'name': 'Jean-Christophe Prat',
        'nationality': '🇫🇷',
        'formation': 'Holston PnR / Full Court Trap',
        'style': 'Pick and roll Holston, trap full court, défense agressive',
        'philosophy': 'Exploitation du pick and roll de David Holston comme architecte offensif. Bibbins et Babb comme options scoring extérieur. Défense agressive avec trap plein terrain et harcèlement constant. Identité combative.',
        'strengths': ['Holston clutch vétéran', 'Défense agressive', 'Trap déstabilisateur', 'Ambiance salle'],
        'weaknesses': ['Dépendance à Holston', 'Budget contraint'],
        'key_principles': ['Holston PnR', 'Baseline cuts', 'Full court trap', 'Harcèlement défensif']
    },
    'Strasbourg Basket': {
        'name': 'Laurent Vila',
        'nationality': '🇫🇷',
        'formation': 'Inside-Out / Drop Coverage',
        'style': 'Jeu intérieur-extérieur, Dessert roll, drop coverage',
        'philosophy': 'Utilisation de Brice Dessert comme pivot roulant dans le pick and roll. Jeu intérieur-extérieur équilibré. Drop coverage pour protéger le cercle. Spacing créé par Invernizzi et Roberson aux ailes.',
        'strengths': ['Dessert rolling élite', 'Défense drop solide', 'Équilibre attaque-défense', 'Spacing offensif'],
        'weaknesses': ['Manque de création pure', 'Budget contraint'],
        'key_principles': ['Dessert roll PnR', 'Inside-out game', 'Drop coverage', 'Spacing ailes']
    },
    'Limoges CSP': {
        'name': 'Jean-Marc Dupraz',
        'nationality': '🇫🇷',
        'formation': 'Off-Screen Spacing / Match-up Zone',
        'style': 'Spacing Lang, écrans, zone match-up défensive',
        'philosophy': 'Exploitation des déplacements off-screen de Nicolas Lang pour créer des tirs ouverts. Système flex avec fluidité de rotation. Défense zone match-up pour perturber les offenses structurées. Histoire légendaire comme motivation.',
        'strengths': ['Lang shooteur élite', 'Zone déstabilisatrice', 'Histoire légendaire', 'Soutien populaire'],
        'weaknesses': ['Budget très limité', 'Reconstruction difficile'],
        'key_principles': ['Lang off-screen', 'Flex offense', 'Zone match-up', 'Culture Beaublanc']
    },
    'Élan Chalon': {
        'name': 'Elric Delord',
        'nationality': '🇫🇷',
        'formation': 'Motion Offense / Pack-Line',
        'style': 'Motion offense, exploitation des jeunes talents français, pack-line défensif',
        'philosophy': 'Développement des jeunes talents français comme Leray et Nadolny. Jeu offensif collectif basé sur le mouvement. Défense pack-line disciplinée. Polyvalence de Mutts comme ancre tactique.',
        'strengths': ['Leray talent français', 'Nadolny jeune prometteur', 'Mutts polyvalent', 'Jeu collectif'],
        'weaknesses': ['Équipe en reconstruction', 'Budget limité'],
        'key_principles': ['Motion offense', 'Pack-line defense', 'Développement jeunes français', 'Mutts polyvalence']
    },
    'ESSM': {
        'name': 'Eric Girard',
        'nationality': '🇫🇷',
        'formation': 'Spread PnR / Deny Defense',
        'style': 'Pick and roll Zoriks, spread, déni défensif agressif',
        'philosophy': 'Zoriks comme playmaker principal du pick and roll avec spacing maximal. Déni défensif très agressif sur tous les porteurs de ballon. Focus rebond défensif pour limiter les secondes chances adverses. Combativité comme identité.',
        'strengths': ['Zoriks playmaker créatif', 'Déni défensif intense', 'Rebond défensif', 'Combativité'],
        'weaknesses': ['Profondeur roster courte', 'Budget limité'],
        'key_principles': ['Spread PnR Zoriks', 'Déni agressif', 'Rebond défensif', 'Combativité collective']
    },
    'BCM Gravelines': {
        'name': 'Jean-Marc Dupraz',
        'nationality': '🇫🇷',
        'formation': '3PT Shooting / Switch 1-4',
        'style': 'Volume 3 points, staggers, switch 1-4 défensif, Denis organisateur',
        'philosophy': 'Volume de tirs à 3 points élevé avec Tyree et Bluiett comme menaces. Denis comme organisateur français. Switch défensif 1-4 pour contrer les pick and rolls adverses. Aide faible côté rapide. Combativité et culture défensive historique.',
        'strengths': ['Denis organisation', 'Volume 3 points', 'Switch défensif cohérent', 'Culture locale'],
        'weaknesses': ['Budget très limité', 'Roster court'],
        'key_principles': ['Baseline staggers', '3PT volume', 'Switch 1-4', 'Help weakside rapide']
    },
    'SLUC Nancy': {
        'name': 'Sylvain Lautié',
        'nationality': '🇫🇷',
        'formation': 'Lob Threat Thompson / Zone 2-3',
        'style': 'Lob threat Thompson, isolation Clemons, zone alternée',
        'philosophy': 'Exploitation de la menace lob de Shevon Thompson pour déstabiliser les défenses. Isolation de Chris Clemons comme scoreur principal. Alternance zone 2-3 et man-to-man pour perturber adverse. Box-out physique du centre.',
        'strengths': ['Thompson lob déstabilisateur', 'Clemons scoreur', 'Zone 2-3 efficace', 'Boyer physique'],
        'weaknesses': ['Manque de profondeur', 'Irrégularité offensive'],
        'key_principles': ['Thompson lob threat', 'Clemons isolation', 'Zone 2-3 alternation', 'Box-out physique']
    },
    'Stade Rochelais Basket': {
        'name': 'Julien Cortey',
        'nationality': '🇫🇷',
        'formation': 'Motion Passing / High Post Hub',
        'style': 'Passes en mouvement, hub poste haut, pression on-ball',
        'philosophy': 'Motion offense basée sur les passes en mouvement et le poste haut comme hub de distribution. Pression intensive on-ball défensive. Box-and-one ponctuel pour neutraliser les stars adverses. Sessoms comme meneur dynamique.',
        'strengths': ['Sessoms dynamique', 'Motion passing fluide', 'Pression défensive intense', 'Adaptabilité'],
        'weaknesses': ['Équipe jeune en développement', 'Manque d\'expérience élite'],
        'key_principles': ['High post hub', 'Motion passing', 'Intense on-ball pressure', 'Box-and-one options']
    },
    # ── Betclic Elite nouvelles équipes ──────────────────────────────────────
    'pluvy': {
        'name': 'Laurent Pluvy',
        'nationality': '🇫🇷 Français',
        'formation': '3-2 Zone / Motion',
        'style': 'Jeu rapide et collectif, développement de jeunes talents',
        'philosophy': 'Développer les jeunes, jeu de mouvement offensif intense',
        'strengths': ['Transition rapide', 'Développement jeunes', 'Cohésion collective'],
        'weaknesses': ['Effectif limité', 'Inexpérience sur gros matchs'],
        'key_principles': ['Fast break prioritaire', 'Spacing agressif', 'Pression défensive haute']
    },
    'fauthoux': {
        'name': 'Frédéric Fauthoux',
        'nationality': '🇫🇷',
        'formation': 'Motion Offense / Extra Pass',
        'style': 'Motion offense fluide, extra pass, switching défensif',
        'philosophy': 'Motion offense basée sur la circulation du ballon et les passes supplémentaires. Défense par switching sur les écrans. Exploitation de McGhee et Mokoka en transition. Rythme de jeu équilibré.',
        'strengths': ['McGhee scoreur explosif', 'Mokoka athlétisme', 'Mitchell mobilité', 'Jeu collectif'],
        'weaknesses': ['Manque de superstar', 'Régularité défensive'],
        'key_principles': ['Extra pass', 'Motion offense', 'Screen switching', 'Transition rapide']
    },
    'menard': {
        'name': 'Alexandre Ménard',
        'nationality': '🇫🇷',
        'formation': 'Drive & Kick / Pick & Roll',
        'style': 'Pick and roll Warner, drive & kick, défense agressive Williams',
        'philosophy': 'Exploitation d\'Angelo Warner en création pick and roll. K.J. Williams dominant en intérieur. Malik Fitts comme ailier fort polyvalent. Défense physique agressive avec présence de Williams au cercle.',
        'strengths': ['Warner scoreur explosif', 'Williams dominant intérieur', 'Fitts polyvalence', 'Combativité'],
        'weaknesses': ['Budget limité', 'Profondeur roster'],
        'key_principles': ['PnR Warner', 'Williams rim protection', 'Drive & kick', 'Défense agressive']
    },
    'giuitta': {
        'name': 'Elric Delord',
        'nationality': '🇫🇷',
        'formation': 'Motion Offense / Pack-Line',
        'style': 'Motion offense, exploitation des jeunes talents français, pack-line défensif',
        'philosophy': 'Développement des jeunes talents français comme Leray et Nadolny. Jeu offensif collectif basé sur le mouvement. Défense pack-line disciplinée. Polyvalence de Mutts comme ancre tactique.',
        'strengths': ['Leray talent français', 'Nadolny jeune prometteur', 'Mutts polyvalent', 'Jeu collectif'],
        'weaknesses': ['Équipe en reconstruction', 'Budget limité'],
        'key_principles': ['Motion offense', 'Pack-line defense', 'Développement jeunes français', 'Mutts polyvalence']
    },
    'kunter': {
        'name': 'Erman Kunter',
        'nationality': '🇹🇷 Turc',
        'formation': '4-3 Motion',
        'style': 'Formation de jeunes talents, jeu offensif moderne, identité historique',
        'philosophy': 'Jeu offensif ouvert, développement des jeunes, mouvement constant du ballon',
        'strengths': ['Formation jeunes', 'Jeu offensif', 'Histoire du club'],
        'weaknesses': ['Régularité défensive', 'Effectif jeune'],
        'key_principles': ['Motion offense', 'Spacing 5-out', 'Développement de jeunes']
    },
    'kiritzé': {
        'name': 'Rémi Kiritzé-Topor',
        'nationality': '🇫🇷 Français',
        'formation': '1-3-1 Zone',
        'style': 'Défense intense, jeu rapide en reconstruction, pression constante',
        'philosophy': 'Reconstruction par la défense et l\'intensité collective',
        'strengths': ['Défense intense', 'Pression haute', 'Esprit collectif'],
        'weaknesses': ['Attaque limitée', 'Effectif en reconstruction'],
        'key_principles': ['Défense 1-3-1', 'Pression haute permanente', 'Jeu rapide en transition']
    },
    'mahe': {
        'name': 'Julien Mahé',
        'nationality': '🇫🇷 Français',
        'formation': '3-2 Zone',
        'style': 'Jeu physique nordiste, défense agressive, identité régionale forte',
        'philosophy': 'Intensité défensive, jeu physique, culture nordiste gagnante',
        'strengths': ['Défense physique', 'Intensité', 'Identité régionale'],
        'weaknesses': ['Attaque parfois limitée', 'Dépendance aux imports'],
        'key_principles': ['Défense agressive', 'Rebond offensif', 'Identité physique']
    },
    # ── Euroleague nouvelles équipes ──────────────────────────────────────────
    'dubai_coach': {
        'name': 'Sasa Obradovic',
        'nationality': '🇷🇸 Serbe',
        'formation': '4-1 Spread',
        'style': 'Jeu offensif ambitieux, recrutement international, approche moderne',
        'philosophy': 'Basket spectaculaire, recrutement stars, ambition maximale',
        'strengths': ['Budget élevé', 'Recrutement international', 'Salle moderne'],
        'weaknesses': ['Manque histoire', 'Cohésion à construire'],
        'key_principles': ['Jeu offensif ouvert', 'Stars en isolation', 'Transition rapide']
    },
    'partizan_coach': {
        'name': 'Željko Obradović',
        'nationality': '🇷🇸 Serbe',
        'formation': '4-1 Low Post',
        'style': 'Défense légendaire, culture gagnante serbe, jeu très physique et discipliné',
        'philosophy': 'Défense et discipline, culture serbe gagnante, jeu collectif',
        'strengths': ['Défense légendaire', 'Culture gagnante', 'Atmosphère intimidante'],
        'weaknesses': ['Budget limité vs top clubs', 'Rotation courte'],
        'key_principles': ['Défense ultra-intense', 'Discipline tactique', 'Jeu physique imposé']
    },
    'valencia_coach': {
        'name': 'Álex Mumbrú',
        'nationality': '🇪🇸 Espagnol',
        'formation': '4-1 Horns',
        'style': 'Jeu collectif espagnol, possession, organisation tactique rigoureuse',
        'philosophy': 'Jeu collectif, possession contrôlée, organisation espagnole',
        'strengths': ['Organisation tactique', 'Jeu collectif', 'Tradition espagnole'],
        'weaknesses': ['Manque stars offensives', 'Budget moyen Euroleague'],
        'key_principles': ['Possession contrôlée', 'Mouvements collectifs', 'Défense organisée']
    },
    'panathinaikos_coach': {
        'name': 'Ergin Ataman',
        'nationality': '🇹🇷 Turc',
        'formation': '4-1 Motion',
        'style': 'Défense très intense, supporters légendaires, culture gagnante grecque, haute pression',
        'philosophy': 'Intensité défensive maximale, culture gagnante, pression constante',
        'strengths': ['Défense très intense', 'Fans légendaires', 'Culture gagnante'],
        'weaknesses': ['Pression externe énorme', 'Irrégularité offensive'],
        'key_principles': ['Pression défensive maximale', 'Fast break', 'Intensité 40 minutes']
    },
    'efes_coach': {
        'name': 'Ergin Ataman',
        'nationality': '🇹🇷 Turc',
        'formation': '4-1 PnR',
        'style': 'Pick and roll élite Micic, jeu positionnel, expérience Euroleague maximale, défense organisée',
        'philosophy': 'Pick and roll de haute qualité autour de Micic, exploitation de Valanciunas en intérieur, roster international expérimenté',
        'strengths': ['Micic meneur élite Euroleague', 'Valanciunas dominant intérieur', 'Expérience Euroleague', 'Jeu positionnel'],
        'weaknesses': ['Âge du roster', 'Profondeur de banc'],
        'key_principles': ['Pick and roll Micic élite', 'Positional play', 'Contrôle du tempo', 'Valanciunas au poste']
    },
    'baskonia_coach': {
        'name': 'Dusko Ivanovic',
        'nationality': '🇷🇸 Serbe',
        'formation': '4-1 Motion',
        'style': 'Défense physique, jeu collectif espagnol, identité Euroleague',
        'philosophy': 'Rigueur défensive, jeu collectif, basket européen structuré',
        'strengths': ['Défense physique', 'Expérience Euroleague', 'Collectif'],
        'weaknesses': ['Roster vieillissant', 'Budget moyen top'],
        'key_principles': ['Défense physique', 'Motion offense', 'Contrôle du tempo']
    },
    'zvezda_coach': {
        'name': 'Dejan Radonjic',
        'nationality': '🇷🇸 Serbe',
        'formation': '4-1 Motion',
        'style': 'Défense agressive serbe, supporters ultra-passionnés, jeu physique',
        'philosophy': 'Intensité défensive, culture gagnante Belgrade',
        'strengths': ['Défense intense', 'Fans légendaires', 'Rivalité Partizan'],
        'weaknesses': ['Irrégularité', 'Budget moyen'],
        'key_principles': ['Défense 100%', 'Intensité', 'Culture gagnante']
    },
    'milano_coach': {
        'name': 'Ettore Messina',
        'nationality': '🇮🇹 Italien',
        'formation': '4-1 Flex',
        'style': 'Défense organisée, jeu collectif italien, expérience internationale, basket structuré',
        'philosophy': 'Défense collective, basket structuré, exploitation de l\'expérience',
        'strengths': ['Défense organisée', 'Expérience collective', 'Jeu structuré'],
        'weaknesses': ['Manque explosivité', 'Scoring limité'],
        'key_principles': ['Défense collective', 'Spacing intelligent', 'Mouvement de balle']
    },
    'virtus_coach': {
        'name': 'Luca Banchi',
        'nationality': '🇮🇹 Italien',
        'formation': '4-1 Motion',
        'style': 'Talent individuel, expérience internationale, jeu offensif créatif, identité italienne',
        'philosophy': 'Talent individuel au service du collectif, jeu offensif de haute qualité',
        'strengths': ['Talent individuel', 'Expérience internationale', 'Jeu offensif'],
        'weaknesses': ['Défense parfois poreuse', 'Irrégularité'],
        'key_principles': ['Talent individuel', 'Jeu offensif de création', 'Motion offense']
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
    "FC Nantes":              "Nantes",
    "Le Havre AC":            "Le Havre",
    "AJ Auxerre":             "Auxerre",
    "Angers SCO":             "Angers",
    "FC Lorient":             "lorient_coach",
    "Paris FC":               "kombouare",
    "FC Metz":                "metz_coach",
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
    "Philadelphia 76ers":     "76ers",
    # La Liga
    "Real Madrid CF":        "Real Madrid",
    "FC Barcelona":          "Barcelona",
    "Atlético de Madrid":    "Atletico",
    "Sevilla FC":            "Sevilla",
    "Real Betis":            "Betis",
    "Athletic Club":         "Athletic",
    "Villarreal CF":         "Villarreal",
    "Real Sociedad":         "Real Sociedad",
    "Valencia CF":           "Valencia",
    "CA Osasuna":            "Osasuna",
    "Girona FC":             "Girona",
    "Rayo Vallecano":        "Rayo",
    # Betclic Elite
    "AS Monaco Basket":           "Monaco Basket",
    "Paris Basketball":           "Paris Basket",
    "LDLC ASVEL":                 "ASVEL",
    "JL Bourg-en-Bresse":         "fauthoux",
    "Chalon-sur-Saône":           "giuitta",
    "Cholet Basket":              "kunter",
    "Nanterre 92":                "Nanterre 92",
    "Saint-Quentin Basket-Ball":  "Saint-Quentin",
    "Le Mans Sarthe Basket":      "Le Mans",
    "JDA Dijon":                  "JDA Dijon",
    "SIG Strasbourg":             "Strasbourg Basket",
    "Limoges CSP":                "Limoges CSP",
    "Élan Chalon":                "Élan Chalon",
    "ESSM Le Portel":             "ESSM",
    "BCM Gravelines-Dunkerque":   "mahe",
    "SLUC Nancy Basket":          "kiritzé",
    "Stade Rochelais Basket":     "Stade Rochelais Basket",
    "Boulazac Basket Dordogne":   "menard",
    # Euroleague nouvelles équipes
    "Dubai BC":                   "dubai_coach",
    "Partizan Belgrade":          "partizan_coach",
    "Valence Basket":             "valencia_coach",
    "Panathinaikos":              "panathinaikos_coach",
    "Anadolu Efes Istanbul":      "efes_coach",
    "EA7 Emporio Armani Milano":  "milano_coach",
    "Virtus Segafredo Bologna":   "virtus_coach",
    "Baskonia Vitoria-Gasteiz":   "baskonia_coach",
    "Crvena Zvezda Meridianbet Belgrade": "zvezda_coach",
}

# ── Fiches scouting par équipe ────────────────────────────────────────────────
SCOUTING_SHEETS: dict[str, dict] = {
    # ══ BETCLIC ELITE ═══════════════════════════════════════════════════════════
    "AS Monaco Basket": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Monaco", "arena": "Salle Gaston Médecin", "capacity": 3500,
        "founded": 1928, "president": "Oleg Petrov", "coach": "Sasa Obradovic",
        "budget_rank": 2, "euroleague": True,
        "season_objective": "Playoffs Euroleague + Betclic Elite",
        "playing_style": "Isolation Mike James, pick & roll intensif, Mirotic spacing, défense agressive show & recover",
        "offensive_system": "Iso James en création pure, Begarin athlétisme extérieur, Mirotic spacing, Theis pivot mobile",
        "defensive_system": "Show & recover agressif, Theis protection cercle, man-to-man strict",
        "key_players": [
            {"name": "Mike James",      "pos": "PG", "flag": "🇺🇸", "age": 34, "strengths": "Scoring, clutch, création",                    "role": "Meneur star clutch Euroleague"},
            {"name": "Nikola Mirotic",  "pos": "PF", "flag": "🇲🇪", "age": 34, "strengths": "Tir 3pts, scoring, expérience NBA",            "role": "Ailier fort shooteur élite"},
            {"name": "Juhann Begarin",  "pos": "SG", "flag": "🇫🇷", "age": 22, "strengths": "Athletisme, défense, potentiel",              "role": "Arrière français prometteur"},
            {"name": "Alpha Diallo",    "pos": "SF", "flag": "🇫🇷", "age": 27, "strengths": "Athlétisme, rebonds, défense intensive",       "role": "Ailier athlétique, intensité défensive"},
            {"name": "Daniel Theis",    "pos": "C",  "flag": "🇩🇪", "age": 32, "strengths": "Pick and roll, défense, mobilité",            "role": "Pivot mobile NBA expérimenté"},
        ],
        "strengths": ["Mike James intenable", "Mirotic spacing élite", "Pick & Roll", "Défense agressive"],
        "weaknesses": ["Dépendance totale à Mike James", "Cohésion à construire"],
        "stats_profile": {"Rythme": "Modéré (74.5)", "Taux 3pts": "Moyen", "Défense": "Très bonne", "Rebonds": "Correct"},
        "rivals": ["LDLC ASVEL", "Paris Basketball"],
        "recent_titles": ["Champion Pro A 2019"],
    },
    "Paris Basketball": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Paris", "arena": "Salle Pierre de Coubertin", "capacity": 4500,
        "founded": 2015, "president": "David Khelfa", "coach": "Tuomas Iisalo",
        "budget_rank": 3, "euroleague": False,
        "season_objective": "Titre Betclic Elite + EuroCup",
        "playing_style": "Ultra high pace, pression full court, drag screens, TJ Shorts orchestrateur, Kahudi expérience",
        "offensive_system": "Shorts en création haute vitesse, Fredrick scoring extérieur, Hayes dans la raquette, Kahudi leadership",
        "defensive_system": "Full court press pour steals, rotation rapide, intensité collective maximale",
        "key_players": [
            {"name": "T.J. Shorts",     "pos": "PG", "flag": "🇺🇸", "age": 25, "strengths": "Création, passing, floater, vision jeu",  "role": "Meneur star, architecte du jeu"},
            {"name": "Zam Fredrick",    "pos": "SG", "flag": "🇺🇸", "age": 25, "strengths": "Tir extérieur, scoring, création",        "role": "Arrière scoreur, deuxième option"},
            {"name": "Charles Kahudi",  "pos": "SF", "flag": "🇫🇷", "age": 35, "strengths": "Leadership, défense, expérience, tir",    "role": "Ailier vétéran, leadership"},
            {"name": "Matt Costello",   "pos": "PF", "flag": "🇺🇸", "age": 31, "strengths": "Rebonds, écrans, présence, défense",      "role": "Ailier fort physique"},
            {"name": "Kevarrius Hayes", "pos": "C",  "flag": "🇺🇸", "age": 29, "strengths": "Athlétisme, rebonds, protection cercle",  "role": "Pivot athlétique, ancre défensive"},
        ],
        "strengths": ["TJ Shorts exceptionnel", "Rythme ultra-élevé", "Pression full court", "Kahudi expérience"],
        "weaknesses": ["Fatigue physique accumulée", "Dépendance au rythme"],
        "stats_profile": {"Rythme": "Très rapide (78.2)", "Taux 3pts": "Très élevé", "Défense": "Bonne", "Rebonds": "Moyen"},
        "rivals": ["LDLC ASVEL", "AS Monaco Basket"],
        "recent_titles": ["Champion Betclic Elite 2024"],
    },
    "LDLC ASVEL": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Villeurbanne", "arena": "Astroballe", "capacity": 5000,
        "founded": 1948, "president": "Tony Parker", "coach": "TJ Parker",
        "budget_rank": 1, "euroleague": True,
        "season_objective": "Titre Betclic Elite + Euroleague Top 8",
        "playing_style": "Pick & roll Larkin, Bogdanovic scoring élite, De Colo expérience, défense physique",
        "offensive_system": "Pick and roll Larkin meneur clutch, Bogdanovic scoreur extérieur élite, De Colo vétéran leadership, Koné ancre intérieur",
        "defensive_system": "Drop coverage sur ball screens, containment physique, Koné protection cercle",
        "key_players": [
            {"name": "Shane Larkin",       "pos": "PG", "flag": "🇺🇸", "age": 33, "strengths": "Scoring, pick and roll, leadership",          "role": "Meneur clutch Euroleague"},
            {"name": "Bogdan Bogdanovic",   "pos": "SG", "flag": "🇷🇸", "age": 32, "strengths": "Tir 3pts, création, scoring",               "role": "Arrière scoreur élite"},
            {"name": "Nando De Colo",       "pos": "SF", "flag": "🇫🇷", "age": 38, "strengths": "Expérience, clutch, leadership",             "role": "Vétéran emblématique français"},
            {"name": "Melvin Ajinca",       "pos": "PF", "flag": "🇫🇷", "age": 22, "strengths": "Mobilité, finitions, potentiel NBA",         "role": "Jeune ailier fort prometteur"},
            {"name": "Bakary Koné",         "pos": "C",  "flag": "🇫🇷", "age": 27, "strengths": "Protection cercle, rebonds, physique",       "role": "Pivot défensif, ancre intérieure"},
        ],
        "strengths": ["Larkin clutch Euroleague", "Bogdanovic scoring élite", "De Colo expérience", "Culture gagnante"],
        "weaknesses": ["Fatigue cumul Euroleague+ProA", "Pression des attentes"],
        "stats_profile": {"Rythme": "Modéré (73.0)", "Taux 3pts": "Élevé", "Défense": "Élite", "Rebonds": "Dominant"},
        "rivals": ["AS Monaco Basket", "Paris Basketball"],
        "recent_titles": ["Champion Betclic Elite 2022", "Champion Betclic Elite 2023"],
    },
    "JL Bourg-en-Bresse": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Bourg-en-Bresse", "arena": "Ekinox", "capacity": 5000,
        "coach": "Frédéric Fauthoux",
        "season_objective": "Top 8 Betclic Elite",
        "playing_style": "Motion offense fluide, extra pass, transition Mokoka, switching défensif",
        "offensive_system": "McGhee scoreur explosif, Mokoka transition athlétique, Mitchell mobilité intérieur, Shumate ancre",
        "defensive_system": "Switch défensif, pression défensive haute, zone 3-2 ponctuelle",
        "key_players": [
            {"name": "Darius McGhee",   "pos": "PG", "flag": "🇺🇸", "age": 26, "strengths": "Scoring, vitesse, tir 3pts, explosivité",   "role": "Meneur scoreur explosif"},
            {"name": "Adam Mokoka",     "pos": "SG", "flag": "🇨🇦", "age": 26, "strengths": "Athlétisme, défense, transition, drives",   "role": "Arrière athlétique, moteur transition"},
            {"name": "Tre Mitchell",    "pos": "PF", "flag": "🇺🇸", "age": 24, "strengths": "Tir mi-distance, mobilité, polyvalence",    "role": "Ailier fort mobile, shooteur"},
        ],
        "stats_profile": {"Rythme": "Élevé", "Défense": "Switch 1-5", "3pts": "35%", "Rebonds": "Mid"},
        "strengths": ["McGhee explosif", "Mokoka athlétisme", "Mitchell mobilité", "Jeu collectif"],
        "weaknesses": ["Profondeur d'effectif", "Régularité défensive"],
        "rivals": ["LDLC ASVEL", "Chalon-sur-Saône"],
        "recent_titles": ["Finaliste Pro B 2022"],
        "sport": "🏀 Basket",
    },
    "Cholet Basket": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Cholet", "arena": "Skiovision Arena", "capacity": 5000,
        "coach": "Erman Kunter",
        "season_objective": "Top 6 Betclic Elite",
        "playing_style": "Formation de jeunes, jeu offensif moderne, motion offense et spacing, identité historique du club",
        "offensive_system": "Motion offense 5-out, dribble drive, pick and roll avec Ajinca",
        "defensive_system": "Man-to-man agressive, quelques zones, pressing par moments",
        "key_players": [
            {"name": "Killian Tillie",   "pos": "PF", "flag": "🇫🇷", "age": 26, "strengths": "Tir extérieur, défense, polyvalence",  "role": "Ailier fort polyvalent"},
            {"name": "Ousmane Camara",   "pos": "PG", "flag": "🇫🇷", "age": 24, "strengths": "Vitesse, pénétrations, création",      "role": "Jeune meneur explosif"},
            {"name": "Melvin Ajinca",    "pos": "C",  "flag": "🇫🇷", "age": 21, "strengths": "Mobilité, finitions, potentiel NBA",   "role": "Jeune pivot prometteur"},
        ],
        "stats_profile": {"Rythme": "Élevé", "Défense": "Man-to-man", "3pts": "36%", "Rebonds": "Mid"},
        "strengths": ["Formation jeunes", "Jeu offensif créatif", "Histoire et identité"],
        "weaknesses": ["Irrégularité défensive", "Effectif inexpérimenté"],
        "rivals": ["JL Bourg-en-Bresse", "LDLC ASVEL"],
        "recent_titles": ["Champion de France 2010", "Multiple titres historiques"],
        "sport": "🏀 Basket",
    },
    "Nanterre 92": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Nanterre", "arena": "Palais des Sports de Nanterre", "capacity": 3500,
        "founded": 1930, "president": "Pascal Donnadieu", "coach": "Philippe Da Silva",
        "budget_rank": 8, "euroleague": False,
        "season_objective": "Top 8 Betclic Elite",
        "playing_style": "Run & gun, volume 3 points massif, pression défensive ballon",
        "offensive_system": "Barbitch meneur organisateur, Jackson scoreur principal, Tillman intérieur",
        "defensive_system": "Pression on-ball garde, flaring rapide sur les ailes, Tillman protection cercle",
        "key_players": [
            {"name": "Milan Barbitch",  "pos": "PG", "flag": "🇷🇸", "age": 27, "strengths": "Vision jeu, passes, tir extérieur",          "role": "Meneur organisateur"},
            {"name": "Frank Jackson",   "pos": "SG", "flag": "🇺🇸", "age": 27, "strengths": "Scoring, tir, création isolation",           "role": "Scoreur principal, 2ème option"},
            {"name": "Desi Rodriguez",  "pos": "PF", "flag": "🇵🇷", "age": 29, "strengths": "Tir 3 points, spacing, défense",             "role": "Ailier fort shooteur"},
            {"name": "Justin Tillman",  "pos": "C",  "flag": "🇺🇸", "age": 29, "strengths": "Scoring intérieur, rebonds, écrans",         "role": "Pivot offensif, finisseur"},
        ],
        "strengths": ["Jackson scoreur élite", "Volume 3 points", "Rythme élevé", "Pression défensive"],
        "weaknesses": ["Irrégularité tir extérieur", "Défense en transition"],
        "stats_profile": {"Rythme": "Rapide (76.5)", "Taux 3pts": "Très élevé", "Défense": "Correcte", "Rebonds": "Moyen"},
        "rivals": ["SIG Strasbourg", "BCM Gravelines-Dunkerque"],
        "recent_titles": [],
    },
    "Saint-Quentin Basket-Ball": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Saint-Quentin", "arena": "Palais des Sports Jean-Pierre Dumont", "capacity": 4500,
        "founded": 2001, "president": "Julien Mahé", "coach": "Julien Mahé",
        "budget_rank": 12, "euroleague": False,
        "season_objective": "Top 6 Betclic Elite",
        "playing_style": "Exécution demi-terrain, set plays parfaits, défense half-court élite no-middle",
        "offensive_system": "Set plays construits autour de Boucaud, Robinson scoreur, Olejniczak intérieur",
        "defensive_system": "Défense half-court élite, interdiction milieu, Olejniczak protection périmètre",
        "key_players": [
            {"name": "Lucas Boucaud",        "pos": "PG", "flag": "🇫🇷", "age": 28, "strengths": "Passes, vision jeu, leadership, clutch",   "role": "Meneur organisateur, cerveau"},
            {"name": "Jerome Robinson",      "pos": "SG", "flag": "🇺🇸", "age": 27, "strengths": "Scoring, tir extérieur, création",         "role": "Scoreur principal"},
            {"name": "Noah Kirkwood",        "pos": "SF", "flag": "🇺🇸", "age": 24, "strengths": "Défense, athlétisme, tir",                 "role": "Ailier 3/D, défenseur"},
            {"name": "Giovan Oniangue",      "pos": "PF", "flag": "🇫🇷", "age": 30, "strengths": "Défense, rebonds, physique",               "role": "Ailier fort défensif, rebondeur"},
            {"name": "Dominik Olejniczak",   "pos": "C",  "flag": "🇵🇱", "age": 28, "strengths": "Taille, présence, rebonds, protection",    "role": "Pivot protecteur, rebondeur"},
        ],
        "strengths": ["Set plays exécution parfaite", "Défense half-court élite", "Discipline collective", "Boucaud cerebral"],
        "weaknesses": ["Rythme offensif parfois lent", "Scoring limité en transition"],
        "stats_profile": {"Rythme": "Lent (71.0)", "Taux 3pts": "Moyen", "Défense": "Élite", "Rebonds": "Bon"},
        "rivals": ["LDLC ASVEL", "Cholet Basket"],
        "recent_titles": [],
    },
    "Le Mans Sarthe Basket": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Le Mans", "arena": "Antarès Arena", "capacity": 5000,
        "founded": 1949, "president": "Frédéric Gervais", "coach": "Guillaume Vizade",
        "budget_rank": 10, "euroleague": False,
        "season_objective": "Top 8 Betclic Elite",
        "playing_style": "Drive & kick, spacing athlétique, protection cercle Mawugbe",
        "offensive_system": "Buchanan pénétrateur, Ndoye transition, Narace et DiLeo spacing extérieur",
        "defensive_system": "Rim protection Mawugbe, déni sur ailes, man-to-man collectif",
        "key_players": [
            {"name": "Tray Buchanan",    "pos": "PG", "flag": "🇺🇸", "age": 27, "strengths": "Finition, vitesse, pénétration, transition",  "role": "Meneur pénétrateur dynamique"},
            {"name": "Abdoulaye Ndoye",  "pos": "SG", "flag": "🇸🇳", "age": 24, "strengths": "Athlétisme, défense, transition",             "role": "Arrière athlétique, transition"},
            {"name": "David DiLeo",      "pos": "SF", "flag": "🇮🇹", "age": 30, "strengths": "Tir extérieur, spacing, expérience",          "role": "Ailier shooteur, spacing"},
            {"name": "Williams Narace",  "pos": "PF", "flag": "🇫🇷", "age": 27, "strengths": "Polyvalence, défense, tir mi-distance",       "role": "Ailier fort polyvalent"},
            {"name": "Selom Mawugbe",    "pos": "C",  "flag": "🇺🇸", "age": 27, "strengths": "Protection cercle, rebonds, présence physique","role": "Pivot protecteur, ancre défensive"},
        ],
        "strengths": ["Buchanan dynamique", "Mawugbe protection cercle", "Spacing offensif", "Athlétisme collectif"],
        "weaknesses": ["Manque de shooteurs réguliers", "Profondeur limitée"],
        "stats_profile": {"Rythme": "Modéré (74.0)", "Taux 3pts": "Moyen", "Défense": "Correcte", "Rebonds": "Bon"},
        "rivals": ["Élan Chalon", "Cholet Basket"],
        "recent_titles": [],
    },
    "JDA Dijon": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Dijon", "arena": "Palais des Sports de Dijon", "capacity": 5800,
        "founded": 1934, "president": "Sébastien Leloup", "coach": "Jean-Christophe Prat",
        "budget_rank": 9, "euroleague": False,
        "season_objective": "Top 8 Betclic Elite",
        "playing_style": "Pick and roll Holston, baseline cuts, trap full court agressif",
        "offensive_system": "Holston créateur pick and roll, Skoupak ancre intérieure, Bibbins arrière scoring, Babb spacing",
        "defensive_system": "Trap agressif full court, harcèlement constant, Fofana physique",
        "key_players": [
            {"name": "David Holston",   "pos": "PG", "flag": "🇺🇸", "age": 38, "strengths": "Tir longue distance, clutch, leadership",   "role": "Meneur vétéran star, clutch"},
            {"name": "Justin Bibbins",  "pos": "SG", "flag": "🇺🇸", "age": 28, "strengths": "Tir extérieur, scoring, défense",           "role": "Arrière scoreur polyvalent"},
            {"name": "Chris Babb",      "pos": "SF", "flag": "🇺🇸", "age": 32, "strengths": "Tir 3pts, défense, expérience",             "role": "Ailier shooteur 3/D vétéran"},
            {"name": "Vafessa Fofana",  "pos": "PF", "flag": "🇫🇷", "age": 29, "strengths": "Défense, physique, rebonds, polyvalence",   "role": "Ailier fort défensif"},
            {"name": "Rob Skoupak",     "pos": "C",  "flag": "🇺🇸", "age": 27, "strengths": "Protection cercle, rebonds, présence",      "role": "Pivot protecteur, ancre"},
        ],
        "strengths": ["Holston clutch légendaire", "Défense trap agressive", "Salle mythique", "Ambiance"],
        "weaknesses": ["Dépendance à Holston", "Budget contraint"],
        "stats_profile": {"Rythme": "Modéré (73.5)", "Taux 3pts": "Élevé", "Défense": "Agressive", "Rebonds": "Bon"},
        "rivals": ["SIG Strasbourg", "Élan Chalon"],
        "recent_titles": ["Champion Pro A 2016"],
    },
    "SIG Strasbourg": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Strasbourg", "arena": "Rhénus Sport", "capacity": 4800,
        "founded": 1940, "president": "Jean-Pierre Amann", "coach": "Laurent Vila",
        "budget_rank": 5, "euroleague": False,
        "season_objective": "Top 6 Betclic Elite",
        "playing_style": "Inside-out Dessert roll, drop coverage, spacing Invernizzi/Roberson",
        "offensive_system": "Dessert roulant dans le pick and roll, Maxhuni meneur créateur, Roberson spacing",
        "defensive_system": "Drop coverage sur pivots, Dessert protection périmètre, man-to-man collectif",
        "key_players": [
            {"name": "Edon Maxhuni",   "pos": "PG", "flag": "🇽🇰", "age": 26, "strengths": "Création, tir extérieur, vitesse",          "role": "Meneur créateur"},
            {"name": "Dominic Artis",  "pos": "SG", "flag": "🇺🇸", "age": 30, "strengths": "Défense, vitesse, playmaking",              "role": "Arrière défenseur, organisateur"},
            {"name": "Hugo Invernizzi","pos": "SF", "flag": "🇫🇷", "age": 27, "strengths": "Tir extérieur, spacing, jeunesse",          "role": "Ailier shooteur, développement"},
            {"name": "Jeff Roberson",  "pos": "PF", "flag": "🇺🇸", "age": 29, "strengths": "Tir 3 points, défense, polyvalence",        "role": "Ailier fort 3/D"},
            {"name": "Brice Dessert",  "pos": "C",  "flag": "🇫🇷", "age": 29, "strengths": "Roll au cercle, présence, rebonds, screens","role": "Pivot roulant, ancre pick & roll"},
        ],
        "strengths": ["Dessert rolling élite", "Drop coverage solide", "Équilibre attaque-défense", "Culture club historique"],
        "weaknesses": ["Manque de création pure", "Budget contraint"],
        "stats_profile": {"Rythme": "Modéré (74.2)", "Taux 3pts": "Moyen", "Défense": "Bonne", "Rebonds": "Correct"},
        "rivals": ["LDLC ASVEL", "JDA Dijon"],
        "recent_titles": ["Champion Pro B 2019"],
    },
    "Limoges CSP": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Limoges", "arena": "Palais des Sports de Beaublanc", "capacity": 5738,
        "founded": 1929, "president": "François Doleyres", "coach": "Jean-Marc Dupraz",
        "budget_rank": 13, "euroleague": False,
        "season_objective": "Maintien en Betclic Elite",
        "playing_style": "Spacing Lang off-screen, flex offense, zone match-up défensive",
        "offensive_system": "Lang sur écrans pour tirs ouverts, Terry playmaker, Chassang intérieur technique",
        "defensive_system": "Zone match-up pour perturber offenses, guard containment, Chassang protection",
        "key_players": [
            {"name": "Tyrell Terry",       "pos": "PG", "flag": "🇺🇸", "age": 24, "strengths": "Tir extérieur, finition, vitesse, vision",   "role": "Meneur shooteur, créateur"},
            {"name": "Nicolas Lang",       "pos": "SG", "flag": "🇫🇷", "age": 29, "strengths": "Tir off-screen, spacing, mouvement",          "role": "Shooteur off-screen élite"},
            {"name": "Kenny Baptiste",     "pos": "SF", "flag": "🇫🇷", "age": 27, "strengths": "Athlétisme, défense, rebonds",                "role": "Ailier athlétique défensif"},
            {"name": "Malik Osborne",      "pos": "PF", "flag": "🇺🇸", "age": 26, "strengths": "Tir 3 points, défense, polyvalence",          "role": "Ailier fort 3/D"},
            {"name": "Alexandre Chassang", "pos": "C",  "flag": "🇫🇷", "age": 27, "strengths": "Technique intérieure, passes, rebonds",       "role": "Pivot technique, passeur"},
        ],
        "strengths": ["Lang shooteur d'élite", "Zone match-up déstabilisante", "Histoire légendaire", "Soutien populaire"],
        "weaknesses": ["Budget très limité", "Reconstruction difficile"],
        "stats_profile": {"Rythme": "Lent (72.0)", "Taux 3pts": "Moyen", "Défense": "Correcte", "Rebonds": "Correct"},
        "rivals": ["Élan Chalon", "JDA Dijon"],
        "recent_titles": ["Champion Pro A 2000"],
    },
    "Élan Chalon": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Chalon-sur-Saône", "arena": "Axel Champion Arena", "capacity": 4300,
        "founded": 1936, "president": "Rémi Giuitta", "coach": "Elric Delord",
        "budget_rank": 14, "euroleague": False,
        "season_objective": "Maintien en Betclic Elite",
        "playing_style": "Motion offense, développement des jeunes talents français, pack-line défensif",
        "offensive_system": "Leray créateur jeune, Nadolny arrière français, Hill spacing, Mutts polyvalent intérieur",
        "defensive_system": "Pack-line discipliné, fermeture des lignes, Anochili-Killen ancre",
        "key_players": [
            {"name": "Mathéo Leray",            "pos": "PG", "flag": "🇫🇷", "age": 23, "strengths": "Vitesse, création, potentiel, drives",       "role": "Jeune meneur français prometteur"},
            {"name": "Clarence Nadolny",        "pos": "SG", "flag": "🇫🇷", "age": 22, "strengths": "Tir, athlétisme, potentiel, jeunesse",        "role": "Arrière français talentueux"},
            {"name": "Justyn Mutts",            "pos": "PF", "flag": "🇺🇸", "age": 25, "strengths": "Polyvalence, rebond, scoring, mobilité",      "role": "Ailier fort polyvalent, ancre"},
            {"name": "Jeremiah Hill",           "pos": "SF", "flag": "🇺🇸", "age": 26, "strengths": "Tir extérieur, défense, polyvalence",         "role": "Ailier 3/D"},
            {"name": "Obinna Anochili-Killen",  "pos": "C",  "flag": "🇺🇸", "age": 25, "strengths": "Protection cercle, rebonds, présence",        "role": "Pivot ancre défensive"},
        ],
        "strengths": ["Leray talent français", "Nadolny potentiel", "Mutts polyvalence", "Jeu collectif"],
        "weaknesses": ["Budget très limité", "Jeunesse de l'effectif"],
        "stats_profile": {"Rythme": "Modéré (72.5)", "Taux 3pts": "Moyen", "Défense": "Correcte", "Rebonds": "Bon"},
        "rivals": ["Limoges CSP", "JDA Dijon"],
        "recent_titles": [],
    },
    "ESSM Le Portel": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Le Portel", "arena": "Salle Olivier Raufast", "capacity": 2500,
        "founded": 1971, "president": "Thierry Doukhan", "coach": "Eric Girard",
        "budget_rank": 15, "euroleague": False,
        "season_objective": "Maintien en Betclic Elite",
        "playing_style": "Spread pick & roll Zoriks, déni défensif agressif, focus rebond défensif",
        "offensive_system": "Zoriks playmaker spread PnR, Gholston scoring, Ba ancre intérieure",
        "defensive_system": "Déni agressif sur porteurs, rebond défensif prioritaire, Ba protection cercle",
        "key_players": [
            {"name": "DeAndre Gholston", "pos": "PG", "flag": "🇺🇸", "age": 29, "strengths": "Scoring, création, finition, vitesse",      "role": "Meneur scoreur principal"},
            {"name": "Kristers Zoriks",  "pos": "SG", "flag": "🇱🇻", "age": 28, "strengths": "Playmaking, tir, vision jeu, IQ basket",    "role": "Playmaker créateur, cerveau"},
            {"name": "Ivan Février",     "pos": "SF", "flag": "🇫🇷", "age": 30, "strengths": "Défense, expérience, leadership",           "role": "Ailier défenseur vétéran"},
            {"name": "Jack Nunge",       "pos": "PF", "flag": "🇺🇸", "age": 25, "strengths": "Tir extérieur pivot, rebonds, polyvalence",  "role": "Ailier fort shooteur"},
            {"name": "Idrissa Ba",       "pos": "C",  "flag": "🇫🇷", "age": 27, "strengths": "Présence physique, rebonds, protection cercle","role": "Pivot physique, ancre défensive"},
        ],
        "strengths": ["Zoriks playmaker créatif", "Déni défensif intense", "Rebond défensif", "Combativité"],
        "weaknesses": ["Budget limité", "Profondeur roster courte"],
        "stats_profile": {"Rythme": "Modéré (73.0)", "Taux 3pts": "Moyen", "Défense": "Agressive", "Rebonds": "Bon"},
        "rivals": ["Cholet Basket", "BCM Gravelines-Dunkerque"],
        "recent_titles": [],
    },
    "BCM Gravelines-Dunkerque": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Gravelines-Dunkerque", "arena": "Sportica", "capacity": 4000,
        "coach": "Jean-Marc Dupraz",
        "season_objective": "Top 8 Betclic Elite",
        "playing_style": "Jeu physique et défensif, identité nordiste forte, pression constante sur adversaires",
        "offensive_system": "Denis meneur organisateur, Tyree et Bluiett scoring, pick and roll, transition après turnover",
        "defensive_system": "Zone 3-2, man agressif, Quarters protection cercle, rotations rapides",
        "key_players": [
            {"name": "Gauthier Denis",  "pos": "PG", "flag": "🇫🇷", "age": 29, "strengths": "Vision jeu, organisation, expérience",       "role": "Meneur organisateur français"},
            {"name": "Breein Tyree",    "pos": "SG", "flag": "🇺🇸", "age": 27, "strengths": "Vitesse, drives, scoring, tir extérieur",   "role": "Arrière explosif, scoreur"},
            {"name": "Trevon Bluiett",  "pos": "SF", "flag": "🇺🇸", "age": 29, "strengths": "Tir extérieur, scoring, créativité",        "role": "Ailier scoreur principal"},
            {"name": "Frank Bartley",   "pos": "PF", "flag": "🇺🇸", "age": 30, "strengths": "Rebonds, défense, physique, écrans",        "role": "Ailier fort physique"},
            {"name": "Brian Quarters",  "pos": "C",  "flag": "🇺🇸", "age": 29, "strengths": "Protection cercle, rebonds, présence",      "role": "Pivot ancre défensive"},
        ],
        "stats_profile": {"Rythme": "Mid", "Défense": "Zone 3-2", "3pts": "34%", "Rebonds": "Élevé"},
        "strengths": ["Défense physique", "Identité nordiste", "Intensité", "Denis organisation"],
        "weaknesses": ["Profondeur effectif", "Attaque limitée sans transition"],
        "rivals": ["SLUC Nancy Basket", "JL Bourg-en-Bresse"],
        "recent_titles": ["Champion de France 2016"],
        "sport": "🏀 Basket",
    },
    "SLUC Nancy Basket": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Nancy", "arena": "Palais des Sports de Nancy", "capacity": 4200,
        "coach": "Rémi Kiritzé-Topor",
        "season_objective": "Maintien Betclic Elite",
        "playing_style": "Reconstruction par la défense, intensité physique, jeu rapide pour exploiter les erreurs adverses",
        "offensive_system": "Transition rapide, pick and roll, isolation Marcus Thornton",
        "defensive_system": "Zone 1-3-1, pression haute, traps agressifs",
        "key_players": [
            {"name": "Marcus Thornton", "pos": "PG", "flag": "🇺🇸", "age": 35, "strengths": "Scoring, experience, tir extérieur",  "role": "Vétéran scoreur meneur"},
            {"name": "Axel Julien",     "pos": "SG", "flag": "🇫🇷", "age": 27, "strengths": "Défense, tir 3pts, énergie",          "role": "Arrière défenseur"},
            {"name": "Jordan Davis",    "pos": "SF", "flag": "🇺🇸", "age": 28, "strengths": "Athletisme, défense, drives",         "role": "Ailier polyvalent"},
        ],
        "stats_profile": {"Rythme": "Rapide", "Défense": "Zone 1-3-1", "3pts": "33%", "Rebonds": "Mid"},
        "strengths": ["Défense intense", "Énergie collective", "Jeu en transition"],
        "weaknesses": ["Attaque limitée", "Effectif court"],
        "rivals": ["Chalon-sur-Saône", "BCM Gravelines-Dunkerque"],
        "recent_titles": ["Champion Pro B 2018"],
        "sport": "🏀 Basket",
    },
    "Stade Rochelais Basket": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "La Rochelle", "arena": "Salle Georges Charbonnier", "capacity": 3000,
        "founded": 1993, "president": "Bruno Richet", "coach": "Julien Cortey",
        "budget_rank": 16, "euroleague": False,
        "season_objective": "Maintien en Betclic Elite",
        "playing_style": "Motion passing, hub poste haut, pression on-ball intensive",
        "offensive_system": "Sessoms meneur dynamique, hub poste haut pour distribution, Hawkins finisseur",
        "defensive_system": "Pression on-ball intense, box-and-one ponctuel pour étouffer les stars, aide organisée",
        "key_players": [
            {"name": "Sam Sessoms",    "pos": "PG", "flag": "🇺🇸", "age": 26, "strengths": "Vitesse, finition, créativité, pression",    "role": "Meneur dynamique, pénétrateur"},
            {"name": "Gaetan Clerc",   "pos": "SG", "flag": "🇫🇷", "age": 25, "strengths": "Tir extérieur, défense, développement",      "role": "Arrière 3/D, jeune talent"},
            {"name": "Jérôme Sanchez", "pos": "SF", "flag": "🇫🇷", "age": 28, "strengths": "Défense, polyvalence, intelligence",         "role": "Ailier défenseur, 3/D"},
            {"name": "Jubrile Belo",   "pos": "PF", "flag": "🇫🇷", "age": 27, "strengths": "Athlétisme, défense, rebonds",               "role": "Ailier fort athlétique"},
            {"name": "Ryan Hawkins",   "pos": "C",  "flag": "🇺🇸", "age": 27, "strengths": "Tir extérieur pivot, rebonds, écrans",       "role": "Pivot shooteur, spacing intérieur"},
        ],
        "strengths": ["Sessoms dynamique", "Motion passing fluide", "Pression défensive intense", "Adaptabilité"],
        "weaknesses": ["Équipe en développement", "Manque d'expérience élite", "Budget minimal"],
        "stats_profile": {"Rythme": "Modéré (72.2)", "Taux 3pts": "Moyen", "Défense": "Agressive", "Rebonds": "Correct"},
        "rivals": ["Cholet Basket", "ESSM Le Portel"],
        "recent_titles": [],
    },
    "Chalon-sur-Saône": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Chalon-sur-Saône", "arena": "Espace Chalon", "capacity": 4200,
        "coach": "Elric Delord",
        "season_objective": "Maintien Betclic Elite",
        "playing_style": "Motion offense, développement des jeunes talents français, pack-line défensif",
        "offensive_system": "Leray créateur jeune, Nadolny arrière français, Hill spacing, Mutts polyvalent intérieur",
        "defensive_system": "Pack-line discipliné, fermeture des lignes, Anochili-Killen ancre",
        "key_players": [
            {"name": "Mathéo Leray",           "pos": "PG", "flag": "🇫🇷", "age": 23, "strengths": "Vitesse, création, potentiel",       "role": "Jeune meneur français prometteur"},
            {"name": "Clarence Nadolny",       "pos": "SG", "flag": "🇫🇷", "age": 22, "strengths": "Tir, athlétisme, potentiel",         "role": "Arrière français talentueux"},
            {"name": "Justyn Mutts",           "pos": "PF", "flag": "🇺🇸", "age": 25, "strengths": "Polyvalence, rebond, scoring",       "role": "Ailier fort polyvalent"},
        ],
        "stats_profile": {"Rythme": "Modéré", "Défense": "Pack-line", "3pts": "33%", "Rebonds": "Élevé"},
        "strengths": ["Leray talent français", "Nadolny potentiel", "Mutts polyvalence"],
        "weaknesses": ["Jeunesse de l'effectif", "Budget limité"],
        "rivals": ["JL Bourg-en-Bresse", "Cholet Basket"],
        "recent_titles": ["Champion Betclic Elite 2017"],
        "sport": "🏀 Basket",
    },
    "Boulazac Basket Dordogne": {
        "competition": "Betclic Elite", "sport": "🏀 Basket",
        "city": "Boulazac", "arena": "Archipel de Périgueux", "capacity": 5000,
        "coach": "Alexandre Ménard",
        "season_objective": "Maintien en Betclic Elite",
        "playing_style": "Pick and roll Warner, drive & kick, défense physique Williams au cercle",
        "offensive_system": "Warner créateur pick and roll, Fitts ailier fort polyvalent, Williams ancre intérieure",
        "defensive_system": "Défense physique agressive, Williams protection cercle, man-to-man pressant",
        "key_players": [
            {"name": "Angelo Warner",            "pos": "PG", "flag": "🇺🇸", "age": 24, "strengths": "Vitesse, scoring, drives, création",       "role": "Meneur scoreur rapide"},
            {"name": "K.J. Williams",            "pos": "C",  "flag": "🇺🇸", "age": 24, "strengths": "Rebond, intérieur dominant, présence",     "role": "Pivot dominant, ancre défensive"},
            {"name": "Malik Fitts",              "pos": "PF", "flag": "🇺🇸", "age": 27, "strengths": "Tir extérieur, défense, polyvalence",      "role": "Ailier fort polyvalent"},
            {"name": "Cyrille Eliezer-Vanerot",  "pos": "SG", "flag": "🇫🇷", "age": 28, "strengths": "Tir, défense, expérience française",       "role": "Arrière français expérimenté"},
            {"name": "Tony Snell",               "pos": "SF", "flag": "🇺🇸", "age": 33, "strengths": "Tir 3pts, spacing, expérience",            "role": "Ailier shooteur vétéran"},
        ],
        "strengths": ["Warner explosif", "Williams dominant", "Fitts polyvalence", "Combativité"],
        "weaknesses": ["Budget limité", "Profondeur roster"],
        "stats_profile": {"Rythme": "Modéré (73.0)", "Taux 3pts": "Moyen", "Défense": "Physique", "Rebonds": "Bon"},
        "rivals": ["Le Mans Sarthe Basket", "ESSM Le Portel"],
        "recent_titles": [],
        "sport": "🏀 Basket",
    },
    # ── Euroleague nouvelles équipes ─────────────────────────────────────────
    "dubai_bc": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Dubai", "arena": "Coca-Cola Arena", "capacity": 17000,
        "coach": "Sasa Obradovic",
        "season_objective": "Playoffs Euroleague",
        "playing_style": "Club ambitieux, recrutement international, jeu offensif moderne, pick and roll Satoransky",
        "offensive_system": "Pick and roll Satoransky, isolation Gentile, spacing Wieskamp, Jaiteh ancre intérieure",
        "defensive_system": "Man-to-man, rotations organisées, Jaiteh protection cercle",
        "key_players": [
            {"name": "Tomas Satoransky",     "pos": "PG", "flag": "🇨🇿", "age": 34, "strengths": "Vision, passes, pick and roll",       "role": "Meneur créateur NBA expérimenté"},
            {"name": "Alessandro Gentile",   "pos": "SF", "flag": "🇮🇹", "age": 32, "strengths": "Scoring, tir extérieur, expérience",  "role": "Ailier scoreur Euroleague"},
            {"name": "Mouhammadou Jaiteh",   "pos": "PF", "flag": "🇫🇷", "age": 30, "strengths": "Défense, rebond, pick and roll",      "role": "Pivot intérieur physique"},
        ],
        "stats_profile": {"Rythme": "Élevé", "Défense": "Man-to-man", "3pts": "36%", "Rebonds": "Mid"},
        "strengths": ["Budget ambitieux", "Infrastructure moderne", "Recrutement international"],
        "weaknesses": ["Cohésion à construire", "Manque histoire Euroleague"],
        "rivals": ["Panathinaikos", "Anadolu Efes Istanbul"],
        "recent_titles": [],
        "sport": "🏀 Basket",
        "euroleague": True,
    },
    "partizan": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Belgrade", "arena": "Stark Arena", "capacity": 18000,
        "coach": "Željko Obradović",
        "season_objective": "Final Four Euroleague",
        "playing_style": "Défense légendaire, culture serbe gagnante, jeu très physique discipliné, supporters parmi les meilleurs au monde",
        "offensive_system": "Post-up Lessort, isolation Punter, motion offense disciplinée",
        "defensive_system": "Man-to-man ultra-intense, help defense, trap sur porteur",
        "key_players": [
            {"name": "Kevin Punter",     "pos": "PG", "flag": "🇺🇸", "age": 31, "strengths": "Scoring, clutch, leadership",         "role": "Meneur scoreur clutch"},
            {"name": "Mathias Lessort",  "pos": "C",  "flag": "🇫🇷", "age": 28, "strengths": "Défense, rebond, intimidation",       "role": "Pivot dominant défensif"},
            {"name": "Dante Exum",       "pos": "SG", "flag": "🇦🇺", "age": 29, "strengths": "Athletisme, passes, défense",         "role": "Arrière athlétique créateur"},
        ],
        "stats_profile": {"Rythme": "Physique", "Défense": "Man intense", "3pts": "33%", "Rebonds": "Élevé"},
        "strengths": ["Défense légendaire", "Culture gagnante", "Soutien des fans"],
        "weaknesses": ["Budget moyen Euroleague", "Pression énorme"],
        "rivals": ["Crvena Zvezda", "Panathinaikos"],
        "recent_titles": ["EuroLeague 1992", "EuroLeague 1976"],
        "sport": "🏀 Basket",
        "euroleague": True,
    },
    "valencia": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Valence", "arena": "Fuente de San Luis", "capacity": 9000,
        "coach": "Álex Mumbrú",
        "season_objective": "Top 8 Euroleague",
        "playing_style": "Jeu collectif espagnol par excellence, possession contrôlée, mouvements d'équipe précis, défense organisée",
        "offensive_system": "Horns, motion offense, pick and roll Hermannsson-Rivero, extra pass",
        "defensive_system": "Man-to-man discipliné, rotations collectives, pressure défensive",
        "key_players": [
            {"name": "Klemen Prepelic",     "pos": "SG", "flag": "🇸🇮", "age": 31, "strengths": "Tir 3pts, volume scoring, clutch",  "role": "Arrière scoreur extérieur"},
            {"name": "Martin Hermannsson",  "pos": "PG", "flag": "🇮🇸", "age": 30, "strengths": "Vision, passes, leadership",        "role": "Meneur créateur de jeu"},
            {"name": "Jasiel Rivero",       "pos": "C",  "flag": "🇨🇺", "age": 27, "strengths": "Pick and roll, finitions, mobilité", "role": "Pivot mobile offensif"},
        ],
        "stats_profile": {"Rythme": "Positionnel", "Défense": "Man discipliné", "3pts": "37%", "Rebonds": "Mid"},
        "strengths": ["Organisation tactique", "Tradition espagnole", "Jeu collectif"],
        "weaknesses": ["Manque stars", "Budget moyen"],
        "rivals": ["Real Madrid", "Barça"],
        "recent_titles": ["EuroLeague 2022", "EuroCup 2010"],
        "sport": "🏀 Basket",
        "euroleague": True,
    },
    "panathinaikos": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Athènes", "arena": "OAKA Arena", "capacity": 18000,
        "coach": "Ergin Ataman",
        "season_objective": "Champion Euroleague",
        "playing_style": "Défense très intense, supporters légendaires, culture gagnante grecque, haute pression défensive, jeu collectif offensif",
        "offensive_system": "Motion offense, transition rapide, isolation Brown, pick and roll",
        "defensive_system": "Man-to-man ultra-intense, traps, pression plein terrain",
        "key_players": [
            {"name": "Lorenzo Brown",       "pos": "PG", "flag": "🇺🇸", "age": 33, "strengths": "Leadership, vision, scoring",       "role": "Meneur créateur expérimenté"},
            {"name": "Georgios Papagiannis","pos": "C",  "flag": "🇬🇷", "age": 28, "strengths": "Intérieur, rebond, présence",        "role": "Pivot national dominant"},
            {"name": "Mathias Lessort",     "pos": "SF", "flag": "🇫🇷", "age": 28, "strengths": "Athletisme, défense, dunks",         "role": "Ailier fort athlétique"},
        ],
        "stats_profile": {"Rythme": "Élevé", "Défense": "Man intense", "3pts": "35%", "Rebonds": "Élevé"},
        "strengths": ["Fans légendaires", "Défense intense", "Culture gagnante"],
        "weaknesses": ["Pression médiatique", "Irrégularité offensive"],
        "rivals": ["Partizan Belgrade", "Olympiakos"],
        "recent_titles": ["EuroLeague 2024", "EuroLeague 2011"],
        "sport": "🏀 Basket",
        "euroleague": True,
    },
    "efes": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Istanbul", "arena": "Sinan Erdem Dome", "capacity": 22000,
        "coach": "Ergin Ataman",
        "season_objective": "Final Four Euroleague",
        "playing_style": "Pick and roll d'élite Micic, jeu positionnel contrôlé, Valanciunas dominant intérieur, roster internationaux expérimentés",
        "offensive_system": "Pick and roll Micic-Valanciunas, isolation Finney-Smith, horns, spacing 4-out avec Beaubois",
        "defensive_system": "Drop coverage sur PnR, man-to-man organisé, rotations disciplinées",
        "key_players": [
            {"name": "Vasilije Micic",       "pos": "PG", "flag": "🇷🇸", "age": 30, "strengths": "Pick and roll, clutch, leadership",    "role": "Meneur créateur élite Euroleague"},
            {"name": "Jonas Valančiūnas",    "pos": "C",  "flag": "🇱🇹", "age": 33, "strengths": "Rebond, poste bas, présence",          "role": "Pivot dominant intérieur"},
            {"name": "Dorian Finney-Smith",  "pos": "SF", "flag": "🇺🇸", "age": 31, "strengths": "Tir 3pts, défense, spacing",           "role": "3-and-D ailier NBA"},
            {"name": "Rodrigue Beaubois",    "pos": "SG", "flag": "🇫🇷", "age": 35, "strengths": "Tir, expérience, clutch",              "role": "Arrière vétéran expérimenté"},
            {"name": "Isaia Cordinier",      "pos": "PF", "flag": "🇮🇹", "age": 27, "strengths": "Polyvalence, défense, tir 3pts",       "role": "Ailier fort polyvalent défensif"},
        ],
        "stats_profile": {"Rythme": "Positionnel", "Défense": "Drop coverage", "3pts": "34%", "Rebonds": "Élevé"},
        "strengths": ["Micic meneur élite", "Valanciunas dominant", "PnR élite", "Expérience Euroleague"],
        "weaknesses": ["Âge roster", "Profondeur de banc"],
        "rivals": ["Panathinaikos", "Fenerbahçe"],
        "recent_titles": ["EuroLeague 2022", "EuroLeague 2021"],
        "sport": "🏀 Basket",
        "euroleague": True,
    },
    "milano": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Milan", "arena": "Mediolanum Forum", "capacity": 12700,
        "coach": "Ettore Messina",
        "season_objective": "Playoffs Euroleague",
        "playing_style": "Défense organisée, jeu collectif structuré à l'italienne, exploitation de l'expérience, basket intelligent",
        "offensive_system": "Flex offense, pick and roll Napier-Hines, mouvements collectifs, spacing",
        "defensive_system": "Man-to-man organisé, help defense disciplinée, rotations collectives",
        "key_players": [
            {"name": "Shabazz Napier",  "pos": "PG", "flag": "🇺🇸", "age": 33, "strengths": "Leadership, scoring, organisation",        "role": "Meneur créateur expérimenté"},
            {"name": "Kyle Hines",      "pos": "C",  "flag": "🇺🇸", "age": 37, "strengths": "Défense, rebond, écran, leadership",       "role": "Pivot vétéran défensif légendaire"},
            {"name": "Nico Mannion",    "pos": "SG", "flag": "🇮🇹", "age": 23, "strengths": "Création, vision, potentiel",              "role": "Jeune arrière national prometteur"},
        ],
        "stats_profile": {"Rythme": "Contrôlé", "Défense": "Man organisé", "3pts": "35%", "Rebonds": "Mid"},
        "strengths": ["Défense organisée", "Expérience collective", "Tradition italienne"],
        "weaknesses": ["Manque explosivité", "Scoring limité"],
        "rivals": ["Virtus Bologna", "Fenerbahçe"],
        "recent_titles": ["EuroLeague 2022", "Scudetto 2022"],
        "sport": "🏀 Basket",
        "euroleague": True,
    },
    "virtus": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Bologne", "arena": "Unipol Arena", "capacity": 8000,
        "coach": "Luca Banchi",
        "season_objective": "Final Four Euroleague",
        "playing_style": "Talent individuel au service du collectif, jeu offensif créatif, expérience internationale, identité bolognaise forte",
        "offensive_system": "Motion offense, isolation Belinelli et Cordinier, pick and roll frères Shengelia",
        "defensive_system": "Man-to-man, rotations collectives, pressure défensive",
        "key_players": [
            {"name": "Marco Belinelli",  "pos": "SG", "flag": "🇮🇹", "age": 38, "strengths": "Tir extérieur, clutch, expérience NBA",      "role": "Vétéran NBA scoreur emblématique"},
            {"name": "Toko Shengelia",   "pos": "PF", "flag": "🇬🇪", "age": 31, "strengths": "Scoring, rebond, polyvalence",              "role": "Ailier fort polyvalent dominant"},
            {"name": "Iffe Lundberg",    "pos": "PG", "flag": "🇩🇰", "age": 26, "strengths": "Passes, scoring, vision",                   "role": "Meneur créateur moderne"},
        ],
        "stats_profile": {"Rythme": "Offensif", "Défense": "Man-to-man", "3pts": "37%", "Rebonds": "Mid"},
        "strengths": ["Talent individuel", "Expérience internationale", "Jeu offensif"],
        "weaknesses": ["Défense parfois poreuse", "Irrégularité"],
        "rivals": ["EA7 Milano", "Fenerbahçe"],
        "recent_titles": ["EuroLeague 2023 (Final Four)", "Scudetto 2021", "Scudetto 2022"],
        "sport": "🏀 Basket",
        "euroleague": True,
    },
    "baskonia": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Vitoria-Gasteiz", "arena": "Fernando Buesa Arena", "capacity": 15200,
        "coach": "Dusko Ivanovic",
        "season_objective": "Playoffs Euroleague",
        "playing_style": "Défense physique, jeu collectif espagnol structuré, identité forte Euroleague",
        "offensive_system": "Motion offense, pick and roll Llull, isolation Musa",
        "defensive_system": "Man-to-man physique, rotations disciplinées",
        "key_players": [
            {"name": "Sergio Llull",               "pos": "PG", "flag": "🇪🇸", "age": 37, "strengths": "Expérience, clutch, leadership",       "role": "Meneur légende Euroleague"},
            {"name": "Dzanan Musa",                "pos": "SF", "flag": "🇧🇦", "age": 27, "strengths": "Scoring, tir extérieur, drives",        "role": "Ailier scoreur moderne"},
            {"name": "Timothé Luwawu-Cabarrot",    "pos": "PF", "flag": "🇫🇷", "age": 29, "strengths": "Athlétisme, défense, tir 3pts",         "role": "Ailier fort polyvalent français"},
            {"name": "Toney Douglas",              "pos": "SG", "flag": "🇺🇸", "age": 37, "strengths": "Scoring, tir, expérience",              "role": "Arrière vétéran scoreur"},
            {"name": "Okko Spijkerman",            "pos": "C",  "flag": "🇳🇱", "age": 25, "strengths": "Présence, rebond, pick and roll",       "role": "Pivot intérieur"},
        ],
        "stats_profile": {"Rythme": "Contrôlé", "Défense": "Man physique", "3pts": "35%", "Rebonds": "Élevé"},
        "strengths": ["Expérience Euroleague", "Défense physique", "Tradition espagnole"],
        "weaknesses": ["Roster âgé", "Budget moyen"],
        "rivals": ["Real Madrid", "Valencia"],
        "recent_titles": ["EuroLeague 2021"],
        "sport": "🏀 Basket",
        "euroleague": True,
    },
    "zvezda": {
        "competition": "Euroleague", "sport": "🏀 Basket",
        "city": "Belgrade", "arena": "Stark Arena", "capacity": 18000,
        "coach": "Dejan Radonjic",
        "season_objective": "Playoffs Euroleague",
        "playing_style": "Défense agressive, intensité maximale, supporters parmi les plus passionnés au monde, derby Belgrade légendaire",
        "offensive_system": "Motion offense, Gudurić shooter, Shengelia en poste",
        "defensive_system": "Man-to-man ultra-intense, traps, pression haute",
        "key_players": [
            {"name": "Tornike Shengelia",  "pos": "PF", "flag": "🇬🇪", "age": 31, "strengths": "Scoring, rebond, polyvalence",              "role": "Ailier fort dominant"},
            {"name": "Marko Gudurić",      "pos": "SG", "flag": "🇷🇸", "age": 29, "strengths": "Tir 3pts, scoring, clutch",                "role": "Arrière scoreur extérieur"},
            {"name": "Danilo Andjusic",    "pos": "PG", "flag": "🇷🇸", "age": 34, "strengths": "Leadership, expérience, organisation",     "role": "Meneur vétéran expérimenté"},
            {"name": "Nikola Kalinić",     "pos": "SF", "flag": "🇷🇸", "age": 34, "strengths": "Tir 3pts, expérience, scoring",            "role": "Ailier vétéran scoreur"},
            {"name": "Charles Springer",   "pos": "C",  "flag": "🇺🇸", "age": 25, "strengths": "Physique, défense, présence",              "role": "Pivot ancre défensive"},
        ],
        "stats_profile": {"Rythme": "Physique", "Défense": "Man intense", "3pts": "34%", "Rebonds": "Élevé"},
        "strengths": ["Fans légendaires", "Derby Belgrade", "Défense intense"],
        "weaknesses": ["Irrégularité", "Pression"],
        "rivals": ["Partizan Belgrade"],
        "recent_titles": ["EuroLeague 2004"],
        "sport": "🏀 Basket",
        "euroleague": True,
    },

    # ══ LIGUE 1 (condensé) ══════════════════════════════════════════════════════
    "Paris Saint-Germain": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Paris", "arena": "Parc des Princes", "capacity": 48712,
        "founded": 1970, "president": "Nasser Al-Khelaifi", "coach": "Luis Enrique",
        "budget_rank": 1, "euroleague": False,
        "season_objective": "Ligue 1 + Champions League",
        "playing_style": "Possession verticale, pressing très haut, jeu collectif",
        "offensive_system": "Dembélé-Barcola larges, João Neves pivot bas, Ramos en pivot",
        "defensive_system": "Pressing très haut dès la perte, bloc mi-haut, Donnarumma libéro",
        "key_players": [
            {"name": "Dembélé",         "pos": "AD", "flag": "🇫🇷", "age": 27, "strengths": "Vitesse, dribble, finition — 8 buts",   "role": "Ailier droit star, meilleur buteur"},
            {"name": "Barcola",         "pos": "AG", "flag": "🇫🇷", "age": 22, "strengths": "Vitesse, dribble, jeunesse — 7 buts",   "role": "Ailier gauche explosif"},
            {"name": "Lucas Chevalier", "pos": "GB", "flag": "🇫🇷", "age": 24, "strengths": "Réflexes, 9 clean sheets, leadership",  "role": "Gardien titulaire élite"},
            {"name": "João Neves",      "pos": "MC", "flag": "🇵🇹", "age": 20, "strengths": "Récupération, passe, intelligence",     "role": "Milieu récupérateur"},
        ],
        "strengths": ["Effectif le plus profond de L1", "Pressing collectif élite", "Dembélé-Barcola redoutables"],
        "weaknesses": ["Pression attentes maximale", "Fatigue si parcours européen"],
        "stats_profile": {"Classement": "1er · 57pts", "BP": "53", "BC": "19", "Diff": "+34", "Buteur": "Dembélé 8, Barcola 7"},
        "rivals": ["Olympique de Marseille", "AS Monaco"],
        "recent_titles": ["Champion Ligue 1 2024", "Champion Ligue 1 2023"],
    },
    "Olympique de Marseille": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Marseille", "arena": "Orange Vélodrome", "capacity": 67394,
        "founded": 1899, "president": "Pablo Longoria", "coach": "Jean-Louis Gasset (fév 2026)",
        "budget_rank": 3, "euroleague": False,
        "season_objective": "Top 4 Ligue 1",
        "playing_style": "Jeu offensif avec Greenwood, nouveau projet après départ De Zerbi (11 fév 2026)",
        "offensive_system": "Greenwood meilleur buteur L1, largeurs exploitées, jeu direct",
        "defensive_system": "Organisation en transition, nouveau coach depuis 18 fév 2026",
        "key_players": [
            {"name": "Mason Greenwood", "pos": "AD", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "age": 23, "strengths": "Vitesse, dribble, finition — 14 buts", "role": "Meilleur buteur L1, ailier droit"},
            {"name": "Rabiot",         "pos": "MC", "flag": "🇫🇷",     "age": 29, "strengths": "Physique, passes, box-to-box",       "role": "Milieu box-to-box"},
            {"name": "Harit",          "pos": "MO", "flag": "🇲🇦",     "age": 27, "strengths": "Créativité, dribble, passes",        "role": "Meneur de jeu offensif"},
        ],
        "strengths": ["Greenwood meilleur buteur L1", "Vélodrome 12ème homme", "Effectif international"],
        "weaknesses": ["Transition coaching", "Défense parfois fragile"],
        "stats_profile": {"Classement": "4e · 40pts", "BP": "48", "BC": "31", "Diff": "+17", "Buteur": "Greenwood 14"},
        "rivals": ["Paris Saint-Germain", "Olympique Lyonnais"],
        "recent_titles": ["Champion Ligue 1 2010"],
    },
    "AS Monaco": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Monaco", "arena": "Stade Louis II", "capacity": 18523,
        "founded": 1924, "president": "Dmitry Rybolovlev", "coach": "Luca Mancini (oct 2025)",
        "budget_rank": 2, "euroleague": False,
        "season_objective": "Top 8 Ligue 1",
        "playing_style": "Pressing intense, jeu direct et vertical, Ansu Fati option offensive",
        "offensive_system": "Ansu Fati option offensive, Akliouche-Ben Seghir créateurs, transition rapide",
        "defensive_system": "Pressing haut, bloc compact, Camara-Zakaria en sentinelles",
        "key_players": [
            {"name": "Ansu Fati",  "pos": "AG", "flag": "🇪🇸", "age": 22, "strengths": "Vitesse, dribble, finition — 7 buts", "role": "Ailier gauche dynamique"},
            {"name": "Akliouche", "pos": "MO", "flag": "🇫🇷", "age": 22, "strengths": "Technique, créativité, jeunesse",       "role": "Meneur de jeu offensif"},
            {"name": "Embolo",    "pos": "BU", "flag": "🇨🇲", "age": 27, "strengths": "Puissance, vitesse, finition",           "role": "Avant-centre physique"},
        ],
        "strengths": ["Pressing intense", "Effectif physique et rapide", "Stade Louis-II forteresse"],
        "weaknesses": ["Transition coaching (Hütter licencié oct 2025)", "Salle de petite capacité"],
        "stats_profile": {"Classement": "7e · 37pts", "BP": "40", "BC": "36", "Diff": "+4", "Buteur": "Ansu Fati 7"},
        "rivals": ["Paris Saint-Germain", "Olympique de Marseille"],
        "recent_titles": ["Champion Ligue 1 2017", "Champion Ligue 1 2000"],
    },

    # ══ LIGUE 1 COMPLETE (autres équipes) ═══════════════════════════════════════
    "RC Lens": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Lens", "arena": "Stade Bollaert-Delelis", "capacity": 38223,
        "coach": "Will Still",
        "season_objective": "Top 3 Ligue 1",
        "playing_style": "Pressing intense data-driven, transitions rapides, bloc médian adaptatif",
        "offensive_system": "Saïd-Édouard en attaque, jeu direct, exploitation des transitions",
        "defensive_system": "Pressing déclenché par triggers, bloc adaptable, Robin Risser en gardien",
        "key_players": [
            {"name": "Wesley Saïd",      "pos": "AG",  "flag": "🇫🇷", "age": 27, "role": "Ailier gauche meilleur buteur",   "strengths": "Vitesse, finition, 10 buts"},
            {"name": "Odsonne Édouard",  "pos": "BU",  "flag": "🇫🇷", "age": 27, "role": "Avant-centre polyvalent",         "strengths": "Technique, finition, 8 buts"},
            {"name": "Robin Risser",     "pos": "GB",  "flag": "🇫🇷", "age": 25, "role": "Gardien titulaire",               "strengths": "Réflexes, organisation défensive"},
        ],
        "stats_profile": {"Classement": "2e · 53pts", "BP": "45", "BC": "21", "Diff": "+24", "Buteur": "Saïd 10, Édouard 8"},
        "strengths": ["Saïd-Édouard redoutables", "Pressing data-driven", "Bollaert forteresse"],
        "weaknesses": ["Adaptabilité au très haut niveau", "Dépendance aux individualités"],
        "rivals": ["Lille", "Rennes"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },
    "Olympique Lyonnais": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Lyon", "arena": "Groupama Stadium", "capacity": 59186,
        "coach": "Pierre Sage",
        "season_objective": "Top 5 Ligue 1",
        "playing_style": "Possession patient, pressing organisé par zones, Šulc meilleur buteur",
        "offensive_system": "Šulc en création offensive, Lacazette référence, Cherki entre les lignes",
        "defensive_system": "Pressing par zones définis, Dominik Greif gardien solide",
        "key_players": [
            {"name": "Pavel Šulc",       "pos": "MO",  "flag": "🇨🇿", "age": 24, "role": "Meneur offensif meilleur buteur", "strengths": "Tir, dribble, 10 buts"},
            {"name": "Lacazette",        "pos": "BU",  "flag": "🇫🇷", "age": 33, "role": "Avant-centre vétéran leader",     "strengths": "Finition, expérience, leadership"},
            {"name": "Dominik Greif",    "pos": "GB",  "flag": "🇸🇰", "age": 28, "role": "Gardien titulaire solide",        "strengths": "Réflexes, organisation"},
        ],
        "stats_profile": {"Classement": "3e · 45pts", "BP": "37", "BC": "23", "Diff": "+14", "Buteur": "Šulc 10"},
        "strengths": ["Šulc talent offensif", "Groupama Stadium ambiance", "Sage coach de talent"],
        "weaknesses": ["Défense perfectible", "Manque de profondeur"],
        "rivals": ["Saint-Etienne", "Marseille"],
        "recent_titles": ["Champion Ligue 1 2008"],
        "sport": "⚽ Football",
    },
    "LOSC Lille": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Lille", "arena": "Stade Pierre-Mauroy", "capacity": 50186,
        "coach": "Bruno Genesio",
        "season_objective": "Top 5 Ligue 1 + Europe",
        "playing_style": "Bloc médian compact, contre-attaques rapides, organisation défensive",
        "offensive_system": "David en pivot, Zhegrova ailier, Cabella créateur",
        "defensive_system": "Bloc médian compact 4-4-2, duels physiques au milieu",
        "key_players": [
            {"name": "Jonathan David", "pos": "BU",  "flag": "🇨🇦", "age": 25, "role": "Avant-centre de référence",        "strengths": "Finition, vitesse, efficacité"},
            {"name": "Zhegrova",       "pos": "AD",  "flag": "🇽🇰", "age": 25, "role": "Ailier droit créateur",            "strengths": "Dribble, vitesse, créativité"},
            {"name": "Lucas Chevalier","pos": "GB",  "flag": "🇫🇷", "age": 24, "role": "Gardien élite Ligue 1",            "strengths": "Réflexes, organisation, 9 clean sheets"},
        ],
        "stats_profile": {"Classement": "5e · 40pts", "BP": "37", "BC": "31", "Diff": "+6"},
        "strengths": ["David redoutable", "Bloc défensif solide", "Genesio organisation"],
        "weaknesses": ["Jeu offensif parfois limité", "Dépendance à David"],
        "rivals": ["Lens", "Paris Saint-Germain"],
        "recent_titles": ["Champion Ligue 1 2021"],
        "sport": "⚽ Football",
    },
    "Stade Rennais": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Rennes", "arena": "Roazhon Park", "capacity": 29778,
        "coach": "Jorge Sampaoli",
        "season_objective": "Top 6 Ligue 1",
        "playing_style": "Pressing ultra-offensif, chaos contrôlé, Lepaul meilleur buteur",
        "offensive_system": "Lepaul en avant-centre, 3-4-3 offensif, transitions explosives",
        "defensive_system": "Pressing ultra-haut, collectif mobile, parfois exposé",
        "key_players": [
            {"name": "Esteban Lepaul", "pos": "BU",  "flag": "🇫🇷", "age": 23, "role": "Avant-centre explosif meilleur buteur", "strengths": "Vitesse, finition, 11 buts"},
            {"name": "Bourigeaud",     "pos": "AD",  "flag": "🇫🇷", "age": 30, "role": "Ailier droit expérimenté",               "strengths": "Tir, passes, constance"},
        ],
        "stats_profile": {"Classement": "6e · 40pts", "BP": "38", "BC": "35", "Diff": "+3", "Buteur": "Lepaul 11"},
        "strengths": ["Lepaul talent brut", "Pressing offensif dévastateur", "Roazhon Park ambiance"],
        "weaknesses": ["Vulnérable défensivement", "Physiquement exigeant"],
        "rivals": ["Nantes", "Lorient", "Brest"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },
    "RC Strasbourg": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Strasbourg", "arena": "Stade de la Meinau", "capacity": 26109,
        "coach": "Nouveau coach (jan 2026)",
        "season_objective": "Top 8 Ligue 1",
        "playing_style": "Jeu de possession, Panichelli 2e buteur L1, pressing organisé",
        "offensive_system": "Panichelli meilleur buteur, jeu offensif construit, largeurs exploitées",
        "defensive_system": "Bloc organisé, possession maîtrisée, transition après Rosenior",
        "key_players": [
            {"name": "Joaquín Panichelli", "pos": "BU",  "flag": "🇦🇷", "age": 25, "role": "2e buteur L1, avant-centre argentin", "strengths": "Finition, technique, 12 buts"},
        ],
        "stats_profile": {"Classement": "8e · 35pts", "BP": "40", "BC": "31", "Diff": "+9", "Buteur": "Panichelli 12"},
        "strengths": ["Panichelli 2e buteur L1", "Jeu de possession", "La Meinau ambiance"],
        "weaknesses": ["Transition coach (Rosenior parti jan 2026)", "Régularité défensive"],
        "rivals": ["Nancy", "Metz"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },
    "Stade Brestois": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Brest", "arena": "Stade Francis-Le Blé", "capacity": 15097,
        "coach": "Eric Roy",
        "season_objective": "Maintien Ligue 1",
        "playing_style": "Pressing offensif direct, Del Castillo créateur, solidarité collective",
        "offensive_system": "Del Castillo créateur principal, Mounié en pivot, jeu direct",
        "defensive_system": "Pressing organisé, compacité défensive, bloc médian",
        "key_players": [
            {"name": "Romain Del Castillo", "pos": "MO",  "flag": "🇫🇷", "age": 29, "role": "Meneur offensif, 7 buts",       "strengths": "Technique, dribble, 7 buts"},
            {"name": "Mounié",              "pos": "BU",  "flag": "🇧🇯", "age": 30, "role": "Avant-centre physique",          "strengths": "Puissance, aérien, finition"},
        ],
        "stats_profile": {"Classement": "9e · 33pts", "BP": "32", "BC": "34", "Diff": "-2", "Buteur": "Del Castillo 7"},
        "strengths": ["Del Castillo talent", "Solidarité collective", "Identité forte"],
        "weaknesses": ["Effectif limité", "Stade de petite capacité"],
        "rivals": ["Rennes", "Lorient", "Nantes"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },
    "Toulouse FC": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Toulouse", "arena": "Stadium de Toulouse", "capacity": 33150,
        "coach": "Carles Martínez Novell",
        "season_objective": "Top 10 Ligue 1",
        "playing_style": "Possession structurée à l'espagnole, pressing par zones, jeu collectif",
        "offensive_system": "Dallinga en pivot, Aboukhlal ailier, jeu de possession",
        "defensive_system": "Bloc compact, pressing triggers, organisation défensive",
        "key_players": [
            {"name": "Dallinga",    "pos": "BU",  "flag": "🇳🇱", "age": 24, "role": "Avant-centre néerlandais",   "strengths": "Finition, puissance, efficacité"},
            {"name": "Aboukhlal",   "pos": "AG",  "flag": "🇲🇦", "age": 24, "role": "Ailier gauche rapide",       "strengths": "Vitesse, dribble, créativité"},
        ],
        "stats_profile": {"Classement": "11e · 31pts", "BP": "33", "BC": "28", "Diff": "+5"},
        "strengths": ["Possession structurée", "Organisation collective", "Stadium ambiance"],
        "weaknesses": ["Manque de régularité", "Effectif en construction"],
        "rivals": ["Montpellier", "Bordeaux"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },
    "Angers SCO": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Angers", "arena": "Stade Raymond-Kopa", "capacity": 18029,
        "coach": "Alexandre Dujeux",
        "season_objective": "Maintien Ligue 1",
        "playing_style": "Organisation défensive, solidarité, jeu collectif progressif",
        "offensive_system": "Lepaul option offensive, jeu direct, contre-attaques",
        "defensive_system": "Bloc défensif organisé, Koffi gardien solide, compacité",
        "key_players": [
            {"name": "Esteban Lepaul", "pos": "BU",  "flag": "🇫🇷", "age": 23, "role": "Avant-centre, 11 buts",           "strengths": "Vitesse, finition, 11 buts"},
            {"name": "Hervé Koffi",    "pos": "GB",  "flag": "🇧🇫", "age": 28, "role": "Gardien solide, 8 clean sheets",  "strengths": "Réflexes, leadership, 8 CS"},
        ],
        "stats_profile": {"Classement": "12e · 29pts", "BP": "22", "BC": "30", "Diff": "-8"},
        "strengths": ["Organisation défensive", "Koffi gardien solide", "Combativité"],
        "weaknesses": ["Attaque limitée", "Effectif en construction"],
        "rivals": ["Rennes", "Nantes"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },
    "Le Havre AC": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Le Havre", "arena": "Stade Océane", "capacity": 25178,
        "coach": "Didier Digard",
        "season_objective": "Maintien Ligue 1",
        "playing_style": "Jeu propre et structuré, développement des jeunes, organisation défensive",
        "offensive_system": "Jeu de possession patient, construction propre, jeunes talents",
        "defensive_system": "Bloc défensif organisé, discipline collective",
        "key_players": [],
        "stats_profile": {"Classement": "13e · 26pts", "BP": "20", "BC": "30", "Diff": "-10"},
        "strengths": ["Organisation défensive", "Développement jeunes", "Stade Océane"],
        "weaknesses": ["Attaque limitée (20 BP)", "Manque d'expérience"],
        "rivals": ["Caen", "Rouen"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },
    "OGC Nice": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Nice", "arena": "Allianz Riviera", "capacity": 35624,
        "coach": "Nouveau coach (jan 2026)",
        "season_objective": "Maintien Ligue 1",
        "playing_style": "Pressing haut, Diop option offensive, reconstruction après licenciement Haise",
        "offensive_system": "Diop créateur principal, jeu direct, largeurs exploitées",
        "defensive_system": "Pressing haut réorganisé, pire défense milieu tableau",
        "key_players": [
            {"name": "Sofiane Diop", "pos": "MO",  "flag": "🇫🇷", "age": 24, "role": "Créateur offensif principal",  "strengths": "Technique, dribble, 7 buts"},
        ],
        "stats_profile": {"Classement": "15e · 24pts", "BP": "30", "BC": "44", "Diff": "-14", "Buteur": "Diop 7"},
        "strengths": ["Diop talent offensif", "Allianz Riviera ambiance", "Cadre Nice attractif"],
        "weaknesses": ["Pire défense (44 BC)", "Haise licencié déc 2025", "Transition difficile"],
        "rivals": ["Monaco", "Marseille"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },
    "AJ Auxerre": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Auxerre", "arena": "Stade Abbé-Deschamps", "capacity": 19508,
        "coach": "Christophe Pélissier",
        "season_objective": "Maintien Ligue 1",
        "playing_style": "Bloc compact pragmatique, transitions, efficacité maximale",
        "offensive_system": "Jeu direct, transitions rapides, pragmatisme offensif",
        "defensive_system": "Bloc compact bas, compacité centrale, discipline collective",
        "key_players": [],
        "stats_profile": {"Classement": "16e · 18pts", "BP": "19", "BC": "35", "Diff": "-16"},
        "strengths": ["Pragmatisme", "Stade Abbé-Deschamps", "Identité historique"],
        "weaknesses": ["Attaque limitée (19 BP)", "Bas du classement", "Manque de profondeur"],
        "rivals": ["Troyes", "Dijon"],
        "recent_titles": ["Champion Ligue 2 2022"],
        "sport": "⚽ Football",
    },
    "FC Nantes": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Nantes", "arena": "Stade de la Beaujoire", "capacity": 35322,
        "coach": "Nouveau coach (déc 2025)",
        "season_objective": "Maintien Ligue 1",
        "playing_style": "Jeu direct et combatif, duels physiques, coach changé déc 2025",
        "offensive_system": "Jeu direct aérien, combativité offensive",
        "defensive_system": "Bloc compact, duels physiques, discipline collective",
        "key_players": [],
        "stats_profile": {"Classement": "17e · 17pts", "BP": "22", "BC": "41", "Diff": "-19"},
        "strengths": ["Histoire du club", "Beaujoire ambiance", "Combativité"],
        "weaknesses": ["Bas du classement", "Coach démissionnaire déc 2025", "Défense fragile"],
        "rivals": ["Rennes", "Lorient", "Brest"],
        "recent_titles": ["Coupe de France 2022"],
        "sport": "⚽ Football",
    },
    "lorient": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Lorient", "arena": "Stade du Moustoir", "capacity": 18890,
        "coach": "Régis Le Bris",
        "season_objective": "Maintien Ligue 1",
        "playing_style": "Football direct et offensif, pressing haut, identité bretonne forte, transitions rapides exploitant la vitesse des ailiers",
        "offensive_system": "4-3-3 offensif, ailiers larges, jeu direct en transition, pressing haut pour récupérer haut",
        "defensive_system": "Pressing haut agressif, compacité en bloc médian, récupération rapide du ballon",
        "key_players": [
            {"name": "Pablo Pagis",      "flag": "🇫🇷", "pos": "AG",  "age": 24, "role": "Ailier gauche rapide",       "strengths": "Vitesse, dribbles, 7 buts saison"},
            {"name": "Alexandre Mendy", "flag": "🇫🇷", "pos": "BU",  "age": 29, "role": "Attaquant de surface",       "strengths": "Finitions, jeu dos au but, présence"},
        ],
        "stats_profile": {"Classement": "10e · 33pts", "BP": "34", "BC": "38", "Buts": "Pagis 7"},
        "strengths": ["Pressing offensif", "Identité de jeu", "Cohésion promus"],
        "weaknesses": ["Maintien difficile", "Effectif limité"],
        "rivals": ["Rennes", "Brest", "Nantes"],
        "recent_titles": ["Champion Ligue 2 2024-25"],
    },
    "paris_fc": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Paris", "arena": "Stade Jean-Bouin", "capacity": 20000,
        "coach": "Antoine Kombouaré",
        "season_objective": "Maintien historique Ligue 1",
        "playing_style": "Organisation défensive pragmatique, retour historique en L1 après 46 ans d'absence, jeu direct et efficace",
        "offensive_system": "4-4-2 compact, jeu direct sur Kebbal, contre-attaques rapides",
        "defensive_system": "Bloc bas organisé, 4-4-2 défensif, compacité centrale",
        "key_players": [
            {"name": "Ilan Kebbal", "flag": "🇩🇿", "pos": "MDC", "age": 27, "role": "Milieu créateur offensif — 8 buts", "strengths": "Tir extérieur, dribbles, 8 buts saison"},
        ],
        "stats_profile": {"Classement": "14e · 26pts", "BP": "28", "BC": "40", "Buts": "Kebbal 8"},
        "strengths": ["Organisation défensive", "Combativité", "Histoire unique"],
        "weaknesses": ["Retour après 46 ans", "Effectif limité"],
        "rivals": ["PSG", "Red Star"],
        "recent_titles": ["Champion Ligue 2 2024-25"],
        "sport": "⚽ Football",
    },
    "metz": {
        "competition": "Ligue 1", "sport": "⚽ Football",
        "city": "Metz", "arena": "Stade Saint-Symphorien", "capacity": 28786,
        "coach": "Vacant (licenciement jan 2026)",
        "season_objective": "Maintien Ligue 1 (difficile)",
        "playing_style": "Équipe en grande difficulté, pire défense du championnat, reconstruction urgente nécessaire",
        "offensive_system": "Jeu direct sur Mikautadze, peu de possession, recherche de l'exploit",
        "defensive_system": "Bloc bas par nécessité, nombreux buts encaissés (53)",
        "key_players": [
            {"name": "Georges Mikautadze", "flag": "🇬🇪", "pos": "BU",  "age": 24, "role": "Attaquant international géorgien", "strengths": "Dribbles, finitions, vitesse"},
            {"name": "Farid Boulaya",      "flag": "🇫🇷", "pos": "AD",  "age": 29, "role": "Ailier créateur vétéran",          "strengths": "Technique, tir, expérience L1"},
        ],
        "stats_profile": {"Classement": "18e · 13pts", "BP": "22", "BC": "53", "Diff": "-31"},
        "strengths": ["Capacité stade", "Histoire club"],
        "weaknesses": ["Pire défense L1", "Manque de points"],
        "rivals": ["Nancy", "Strasbourg"],
        "recent_titles": [],
        "sport": "⚽ Football",
    },

    # ══ LA LIGA (condensé) ══════════════════════════════════════════════════════
    "Real Madrid CF": {
        "competition": "La Liga", "sport": "⚽ Football",
        "city": "Madrid", "arena": "Santiago Bernabéu", "capacity": 81044,
        "founded": 1902, "president": "Florentino Pérez", "coach": "Carlo Ancelotti",
        "budget_rank": 1, "euroleague": False,
        "season_objective": "La Liga + Champions League",
        "playing_style": "Pragmatisme élégant, liberté aux stars, transitions Mbappé-Vinicius",
        "offensive_system": "Mbappé-Vinicius larges, Bellingham entre les lignes, verticalité",
        "defensive_system": "Compacité défensive, transitions défensives rapides, Tchouaméni sentinelle",
        "key_players": [
            {"name": "Mbappé",     "pos": "BU", "flag": "🇫🇷", "age": 26, "strengths": "Vitesse, finition, puissance",    "role": "Attaquant star, top scorer"},
            {"name": "Vinicius",   "pos": "AG", "flag": "🇧🇷", "age": 24, "strengths": "Dribble, vitesse, créativité",    "role": "Ailier gauche dévastateur"},
            {"name": "Bellingham", "pos": "MO", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "age": 21, "strengths": "Box-to-box, tir, leadership", "role": "Milieu offensif box-to-box"},
        ],
        "strengths": ["Trio Mbappé-Vinicius-Bellingham", "Expérience C1 légendaire", "Bernabéu forteresse"],
        "weaknesses": ["Peut manquer de pressing organisé", "Dépendance aux stars"],
        "stats_profile": {"Possession": "58%", "Pressing PPDA": "10.2", "xG/match": "2.5", "Buts/match": "2.4"},
        "rivals": ["FC Barcelona", "Atlético de Madrid"],
        "recent_titles": ["Champions League 2024", "La Liga 2024"],
    },
    "FC Barcelona": {
        "competition": "La Liga", "sport": "⚽ Football",
        "city": "Barcelone", "arena": "Estadi Olímpic Lluís Companys", "capacity": 55926,
        "founded": 1899, "president": "Joan Laporta", "coach": "Hansi Flick",
        "budget_rank": 2, "euroleague": False,
        "season_objective": "La Liga + Champions League",
        "playing_style": "Gegenpressing ultra-haut, jeu offensif total, Yamal-Pedri",
        "offensive_system": "Yamal-Raphinha larges, Lewandowski pivot, pressing haut récupération",
        "defensive_system": "Gegenpressing immédiat, récupération haute, Casado sentinelle",
        "key_players": [
            {"name": "Yamal",        "pos": "AD", "flag": "🇪🇸", "age": 17, "strengths": "Génie technique, dribble, vitesse",  "role": "Ailier prodige, game-changer"},
            {"name": "Pedri",        "pos": "MC", "flag": "🇪🇸", "age": 22, "strengths": "Technique, vision, intelligence",    "role": "Pilier créatif du milieu"},
            {"name": "Lewandowski",  "pos": "BU", "flag": "🇵🇱", "age": 37, "strengths": "Finition, technique, expérience",   "role": "9 de référence, buteur élite"},
        ],
        "strengths": ["Yamal phénomène mondial", "Flick gegenpressing redoutable", "Pedri cerveau du jeu"],
        "weaknesses": ["Fragilité défensive sur les contres", "Camp Nou en travaux"],
        "stats_profile": {"Possession": "63%", "Pressing PPDA": "6.8", "xG/match": "2.7", "Buts/match": "2.6"},
        "rivals": ["Real Madrid CF", "Atlético de Madrid"],
        "recent_titles": ["La Liga 2023", "La Liga 2019"],
    },
    "Atlético de Madrid": {
        "competition": "La Liga", "sport": "⚽ Football",
        "city": "Madrid", "arena": "Cívitas Metropolitano", "capacity": 68456,
        "founded": 1903, "president": "Enrique Cerezo", "coach": "Diego Simeone",
        "budget_rank": 3, "euroleague": False,
        "season_objective": "Top 3 La Liga + C1",
        "playing_style": "Défense ultra-solide, transitions meurtrières, intensité maximale",
        "offensive_system": "Transitions Griezmann-Álvarez, bloc bas puis frappe rapide",
        "defensive_system": "Bloc très bas compact, 4-4-2 défensif, duels physiques",
        "key_players": [
            {"name": "Griezmann",       "pos": "MO", "flag": "🇫🇷", "age": 33, "strengths": "Technique, vision, finition, leadership", "role": "Meneur de jeu et finisseur"},
            {"name": "Julián Álvarez",  "pos": "BU", "flag": "🇦🇷", "age": 25, "strengths": "Travail, finition, puissance",            "role": "Avant-centre travailleur"},
            {"name": "Oblak",           "pos": "GB", "flag": "🇸🇮", "age": 32, "strengths": "Arrêts, leadership, fiabilité absolue",   "role": "Gardien de référence mondiale"},
        ],
        "strengths": ["Simeone génie défensif", "Oblak meilleur gardien", "Griezmann clutch légendaire"],
        "weaknesses": ["Jeu offensif parfois prévisible", "Dépendance au bloc bas"],
        "stats_profile": {"Possession": "44%", "Pressing PPDA": "13.5", "xG/match": "1.7", "Buts/match": "1.6"},
        "rivals": ["Real Madrid CF", "FC Barcelona"],
        "recent_titles": ["La Liga 2021", "La Liga 2014"],
    },

    # ══ PREMIER LEAGUE (condensé) ════════════════════════════════════════════════
    "Arsenal FC": {
        "competition": "Premier League", "sport": "⚽ Football",
        "city": "Londres", "arena": "Emirates Stadium", "capacity": 60704,
        "founded": 1886, "president": "Stan Kroenke", "coach": "Mikel Arteta",
        "budget_rank": 3, "euroleague": False,
        "season_objective": "Titre Premier League + C1",
        "playing_style": "Pressing haut intense, construction propre, largeurs Saka-Martinelli",
        "offensive_system": "Saka-Martinelli larges, Havertz faux 9, Ødegaard libre",
        "defensive_system": "Pressing très haut, Rice sentinelle, compacité défensive",
        "key_players": [
            {"name": "Saka",      "pos": "AD", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "age": 23, "strengths": "Dribble, finition, vitesse, constance", "role": "Ailier droit indispensable"},
            {"name": "Ødegaard", "pos": "MO", "flag": "🇳🇴",     "age": 26, "strengths": "Vision, passe, technique, leadership",    "role": "Capitaine, meneur de jeu"},
            {"name": "Rice",      "pos": "MDC","flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "age": 26, "strengths": "Récupération, passe, physique",         "role": "Sentinelle élite"},
        ],
        "strengths": ["Arteta pressing élite", "Saka-Martinelli larges redoutables", "Rice milieu de contrôle"],
        "weaknesses": ["Parfois stérile en blocage adverse", "Expérience titre manquante"],
        "stats_profile": {"Possession": "59%", "Pressing PPDA": "7.8", "xG/match": "2.3", "Buts/match": "2.1"},
        "rivals": ["Manchester City", "Liverpool FC"],
        "recent_titles": ["FA Cup 2020"],
    },
    "Manchester City": {
        "competition": "Premier League", "sport": "⚽ Football",
        "city": "Manchester", "arena": "Etihad Stadium", "capacity": 53400,
        "founded": 1880, "president": "Khaldoon Al Mubarak", "coach": "Pep Guardiola",
        "budget_rank": 1, "euroleague": False,
        "season_objective": "Titre Premier League + C1",
        "playing_style": "Possession totale, circuits de passes codifiés, positional play",
        "offensive_system": "Haaland pivot, De Bruyne créateur, faux latéraux, possession",
        "defensive_system": "Pressing haut, position haute défensive, Rodri absent (blessé)",
        "key_players": [
            {"name": "Haaland",    "pos": "BU", "flag": "🇳🇴", "age": 25, "strengths": "Finition, vitesse, puissance, efficacité",  "role": "Machine à buts, n°9 de référence"},
            {"name": "De Bruyne",  "pos": "MO", "flag": "🇧🇪", "age": 33, "strengths": "Vision, passe, tir, intelligence",         "role": "Playmaker mondial"},
            {"name": "Foden",      "pos": "MO", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "age": 24, "strengths": "Technique, créativité, polyvalence",   "role": "Meneur de jeu créatif"},
        ],
        "strengths": ["Guardiola génie tactique", "Haaland machine à buts", "Profondeur roster"],
        "weaknesses": ["Rodri absent (blessé long terme)", "Vieillissement du noyau dur"],
        "stats_profile": {"Possession": "65%", "Pressing PPDA": "7.0", "xG/match": "2.6", "Buts/match": "2.5"},
        "rivals": ["Arsenal FC", "Liverpool FC"],
        "recent_titles": ["Champion PL 2024", "Champion PL 2023", "Champion PL 2022"],
    },
    "Liverpool FC": {
        "competition": "Premier League", "sport": "⚽ Football",
        "city": "Liverpool", "arena": "Anfield", "capacity": 61276,
        "founded": 1892, "president": "Tom Werner", "coach": "Arne Slot",
        "budget_rank": 2, "euroleague": False,
        "season_objective": "Titre Premier League + C1",
        "playing_style": "Pressing intense, jeu rapide, Salah clutch",
        "offensive_system": "Salah-Diaz larges, Núñez pivot, transitions rapides",
        "defensive_system": "Pressing très haut, Mac Allister sentinelle, bloc haut",
        "key_players": [
            {"name": "Salah",       "pos": "AD", "flag": "🇪🇬", "age": 32, "strengths": "Finition, vitesse, constance légendaire",  "role": "Ailier star, top scorer historique"},
            {"name": "Van Dijk",    "pos": "DC", "flag": "🇳🇱", "age": 33, "strengths": "Domination aérienne, leadership, passe",   "role": "Capitaine, défenseur central élite"},
            {"name": "Mac Allister","pos": "MDC","flag": "🇦🇷", "age": 26, "strengths": "Récupération, passe, vision, pressing",    "role": "Sentinelle et distributeur"},
        ],
        "strengths": ["Salah légende encore au top", "Anfield forteresse", "Slot transition réussie"],
        "weaknesses": ["Van Dijk vieillissant", "Núñez parfois décisif ou invisible"],
        "stats_profile": {"Possession": "58%", "Pressing PPDA": "7.5", "xG/match": "2.4", "Buts/match": "2.2"},
        "rivals": ["Manchester City", "Arsenal FC"],
        "recent_titles": ["Champion PL 2020", "Champions League 2019"],
    },

    # ══ NBA (condensé — Top franchises) ═════════════════════════════════════════
    "Los Angeles Lakers": {
        "competition": "NBA", "sport": "🏀 Basket",
        "city": "Los Angeles", "arena": "Crypto.com Arena", "capacity": 20000,
        "founded": 1947, "president": "Rob Pelinka", "coach": "JJ Redick",
        "budget_rank": 3, "euroleague": False,
        "season_objective": "Titre NBA",
        "playing_style": "Pick and roll LeBron-AD, spacing, expérience playoff",
        "offensive_system": "LeBron orchestrateur, Davis dominant intérieur, shooteurs larges",
        "defensive_system": "Drop coverage, switch sur les pick and roll, LeBron polyvalent",
        "key_players": [
            {"name": "D'Angelo Russell","pos": "PG", "flag": "🇺🇸", "age": 29, "strengths": "Tir longue distance, création pick and roll","role": "Meneur, initiateur d'attaque"},
            {"name": "Austin Reaves",  "pos": "SG", "flag": "🇺🇸", "age": 27, "strengths": "Tir clutch, défense, intelligence",          "role": "3ème option, clutch performer"},
            {"name": "LeBron James",   "pos": "SF", "flag": "🇺🇸", "age": 40, "strengths": "Vision, leadership, finition, longévité",   "role": "GOAT, orchestrateur, leader"},
            {"name": "Rui Hachimura",  "pos": "PF", "flag": "🇯🇵", "age": 27, "strengths": "Tir à mi-distance, verticalité, défense",   "role": "4ème option, spacing intérieur"},
            {"name": "Anthony Davis",  "pos": "C",  "flag": "🇺🇸", "age": 32, "strengths": "Scoring intérieur, protection cercle",       "role": "Pivot dominant, double menace"},
        ],
        "strengths": ["LeBron à 40 ans encore décisif", "Davis dominant", "Expérience playoff"],
        "weaknesses": ["Profondeur de banc limitée", "LeBron vieillissement"],
        "stats_profile": {"Rythme": "Modéré", "Rating offensif": "112.5", "Rating défensif": "110.8", "Taux 3pts": "36%"},
        "rivals": ["Golden State Warriors", "Boston Celtics"],
        "recent_titles": ["Champion NBA 2020"],
    },
    "Boston Celtics": {
        "competition": "NBA", "sport": "🏀 Basket",
        "city": "Boston", "arena": "TD Garden", "capacity": 19156,
        "founded": 1946, "president": "Brad Stevens", "coach": "Joe Mazzulla",
        "budget_rank": 2, "euroleague": False,
        "season_objective": "Titre NBA (repeat)",
        "playing_style": "Défense élite, tirs à 3 points, Tatum-Brown duo dominant",
        "offensive_system": "Tatum-Brown isolation, spacing 5 extérieurs, switch offensif",
        "defensive_system": "Switch systématique élite, intensité maximale, aide rapide",
        "key_players": [
            {"name": "Jrue Holiday",    "pos": "PG", "flag": "🇺🇸", "age": 35, "strengths": "Défense d'élite, clutch, steal",            "role": "Meneur, défenseur élite"},
            {"name": "Derrick White",   "pos": "SG", "flag": "🇺🇸", "age": 30, "strengths": "Défense, tir à 3pts, polyvalence",          "role": "3/D élite, 3ème option"},
            {"name": "Jaylen Brown",    "pos": "SF", "flag": "🇺🇸", "age": 28, "strengths": "Athlétisme, défense, scoring, clutch",      "role": "Co-star, deuxième option offensive"},
            {"name": "Jayson Tatum",    "pos": "PF", "flag": "🇺🇸", "age": 27, "strengths": "Scoring, clutch, tir, isolation",           "role": "Franchise player, scoreur principal"},
            {"name": "Kristaps Porzingis","pos":"C", "flag": "🇱🇻", "age": 29, "strengths": "Tir à 3pts pivot, verticalité, spacing",    "role": "Pivot shooteur, protection cercle"},
        ],
        "strengths": ["Champion NBA 2024 en titre", "Défense élite switch", "Profondeur roster exceptionnelle"],
        "weaknesses": ["Dépendance au tir extérieur", "Peuvent manquer de création en isolation"],
        "stats_profile": {"Rythme": "Modéré", "Rating offensif": "122.2", "Rating défensif": "110.6", "Taux 3pts": "39%"},
        "rivals": ["Los Angeles Lakers", "Miami Heat"],
        "recent_titles": ["Champion NBA 2024"],
    },
    "Golden State Warriors": {
        "competition": "NBA", "sport": "🏀 Basket",
        "city": "San Francisco", "arena": "Chase Center", "capacity": 18064,
        "founded": 1946, "president": "Joe Lacob", "coach": "Steve Kerr",
        "budget_rank": 1, "euroleague": False,
        "season_objective": "Playoffs + Titre possible",
        "playing_style": "Ball movement, spacing 5 extérieurs, Curry à 3 points",
        "offensive_system": "Curry off-ball movement, motion offense, death lineup",
        "defensive_system": "Switch défensif, compacité, Draymond Green conductor",
        "key_players": [
            {"name": "Stephen Curry",     "pos": "PG", "flag": "🇺🇸", "age": 37, "strengths": "Tir légendaire, off-ball, clutch absolu",  "role": "GOAT shooter, franchise player"},
            {"name": "Brandin Podziemski","pos": "SG", "flag": "🇺🇸", "age": 22, "strengths": "Vision jeu, rebond, tir, jeunesse",        "role": "Meneur suppléant, talent émergent"},
            {"name": "Andrew Wiggins",    "pos": "SF", "flag": "🇨🇦", "age": 30, "strengths": "Défense, athlétisme, scoring",             "role": "3/D, défenseur d'élite"},
            {"name": "Jonathan Kuminga",  "pos": "PF", "flag": "🇨🇩", "age": 22, "strengths": "Athlétisme, scoring, verticalité, jeunesse","role": "Ailier fort explosif, avenir"},
            {"name": "Draymond Green",    "pos": "C",  "flag": "🇺🇸", "age": 34, "strengths": "QI basket, défense, passes, leadership",   "role": "Conductor défensif, IQ élite"},
        ],
        "strengths": ["Curry encore au top absolu", "Kerr expérience titres", "Culture ball movement"],
        "weaknesses": ["Vieillissement roster", "Transition générationnelle difficile"],
        "stats_profile": {"Rythme": "Rapide", "Rating offensif": "116.8", "Rating défensif": "113.2", "Taux 3pts": "40%"},
        "rivals": ["Los Angeles Lakers", "Phoenix Suns"],
        "recent_titles": ["Champion NBA 2022"],
    },

    # ══ TOP 14 (condensé) ═══════════════════════════════════════════════════════
    "Stade Toulousain": {
        "competition": "Top 14", "sport": "🏉 Rugby",
        "city": "Toulouse", "arena": "Stade Ernest-Wallon", "capacity": 19500,
        "founded": 1907, "president": "Didier Lacroix", "coach": "Ugo Mola",
        "budget_rank": 1, "euroleague": False,
        "season_objective": "Bouclier de Brennus + Champions Cup",
        "playing_style": "Jeu de passes fluide, Dupont orchestrateur, vitesse et technique",
        "offensive_system": "Dupont demi de mêlée, Ntamack à l'ouverture, jeu au large",
        "defensive_system": "Défense en ligne, ruck rapide, plaquages bas collectifs",
        "key_players": [
            {"name": "Antoine Dupont", "pos": "DM", "flag": "🇫🇷", "age": 28, "strengths": "Vitesse, passes, jeu au pied, leadership",  "role": "Meilleur joueur du monde"},
            {"name": "Romain Ntamack", "pos": "DO", "flag": "🇫🇷", "age": 25, "strengths": "Tir, jeu à la main, créativité",            "role": "Ouvreur de classe mondiale"},
            {"name": "Thomas Ramos",   "pos": "FB", "flag": "🇫🇷", "age": 27, "strengths": "Tir, relances, polyvalence",                "role": "Arrière, buteur titulaire"},
        ],
        "strengths": ["Dupont phénomène mondial", "Effectif le plus profond du Top 14", "Culture gagner"],
        "weaknesses": ["Pression du titre à défendre", "Fatigue si double compétition"],
        "stats_profile": {"Possession": "55%", "Mêlées gagnées": "82%", "Mauls": "Très fort", "Jeu au pied": "Excellent"},
        "rivals": ["Stade Rochelais", "Racing 92"],
        "recent_titles": ["Bouclier de Brennus 2024", "Bouclier de Brennus 2023", "Champions Cup 2024"],
    },
    "Stade Rochelais": {
        "competition": "Top 14", "sport": "🏉 Rugby",
        "city": "La Rochelle", "arena": "Stade Marcel Deflandre", "capacity": 18500,
        "founded": 1901, "president": "Vincent Merling", "coach": "Ronan O'Gara",
        "budget_rank": 2, "euroleague": False,
        "season_objective": "Top 4 + Champions Cup",
        "playing_style": "Puissance physique, jeu aux avants, Alldritt dominant",
        "offensive_system": "Mauls offensifs, Alldritt porteur, Hastoy à l'ouverture",
        "defensive_system": "Défense en ligne, pilonnage physique, Skelton dominant",
        "key_players": [
            {"name": "Grégory Alldritt", "pos": "N°8", "flag": "🇫🇷", "age": 27, "strengths": "Puissance, portée balle, leadership",  "role": "N°8 de référence mondiale"},
            {"name": "Will Skelton",     "pos": "TL",  "flag": "🇦🇺", "age": 33, "strengths": "Puissance mêlée, mauls, présence",     "role": "Talonneur dominant, monster"},
            {"name": "Antoine Hastoy",   "pos": "DO",  "flag": "🇫🇷", "age": 27, "strengths": "Tir, passe, jeu à la main",           "role": "Ouvreur créateur"},
        ],
        "strengths": ["Alldritt meilleur N°8 Europe", "Puissance physique exceptionnelle", "O'Gara coach de talent"],
        "weaknesses": ["Peut manquer de vitesse sur les ailes", "Marcel Deflandre en travaux"],
        "stats_profile": {"Possession": "51%", "Mêlées gagnées": "79%", "Mauls": "Dominant", "Jeu au pied": "Bon"},
        "rivals": ["Stade Toulousain", "Racing 92"],
        "recent_titles": ["Champions Cup 2022", "Champions Cup 2023"],
    },
}

# Maps MATCHES team names → SCOUTING_SHEETS keys
SCOUTING_TEAM_LOOKUP: dict[str, str] = {
    # Betclic Elite
    "AS Monaco Basket":           "AS Monaco Basket",
    "Paris Basketball":           "Paris Basketball",
    "LDLC ASVEL":                 "LDLC ASVEL",
    "JL Bourg-en-Bresse":         "JL Bourg-en-Bresse",
    "Chalon-sur-Saône":           "Chalon-sur-Saône",
    "Cholet Basket":              "Cholet Basket",
    "Nanterre 92":                "Nanterre 92",
    "Saint-Quentin Basket-Ball":  "Saint-Quentin Basket-Ball",
    "Le Mans Sarthe Basket":      "Le Mans Sarthe Basket",
    "JDA Dijon":                  "JDA Dijon",
    "SIG Strasbourg":             "SIG Strasbourg",
    "Limoges CSP":                "Limoges CSP",
    "Élan Chalon":                "Élan Chalon",
    "ESSM Le Portel":             "ESSM Le Portel",
    "BCM Gravelines-Dunkerque":   "BCM Gravelines-Dunkerque",
    "SLUC Nancy Basket":          "SLUC Nancy Basket",
    "Stade Rochelais Basket":     "Stade Rochelais Basket",
    # Euroleague nouvelles équipes
    "Dubai BC":                   "dubai_bc",
    "Partizan Belgrade":          "partizan",
    "Valence Basket":             "valencia",
    "Panathinaikos":              "panathinaikos",
    "Anadolu Efes Istanbul":      "efes",
    "EA7 Emporio Armani Milano":  "milano",
    "Virtus Segafredo Bologna":   "virtus",
    "Baskonia Vitoria-Gasteiz":   "baskonia",
    "Crvena Zvezda Meridianbet Belgrade": "zvezda",
    # Ligue 1
    "Paris Saint-Germain":                    "Paris Saint-Germain",
    "Olympique de Marseille":                 "Olympique de Marseille",
    "AS Monaco":                              "AS Monaco",
    "RC Lens":                                "RC Lens",
    "Olympique Lyonnais":                     "Olympique Lyonnais",
    "LOSC Lille":                             "LOSC Lille",
    "Stade Rennais":                          "Stade Rennais",
    "RC Strasbourg":                          "RC Strasbourg",
    "Stade Brestois 29":                      "Stade Brestois",
    "Toulouse FC":                            "Toulouse FC",
    "Angers SCO":                             "Angers SCO",
    "Le Havre AC":                            "Le Havre AC",
    "OGC Nice":                               "OGC Nice",
    "AJ Auxerre":                             "AJ Auxerre",
    "FC Nantes":                              "FC Nantes",
    "FC Lorient":                             "lorient",
    "Paris FC":                               "paris_fc",
    "FC Metz":                                "metz",
    # La Liga
    "Real Madrid CF":                         "Real Madrid CF",
    "FC Barcelona":                           "FC Barcelona",
    "Atlético de Madrid":                     "Atlético de Madrid",
    # Premier League
    "Arsenal FC":                             "Arsenal FC",
    "Manchester City":                        "Manchester City",
    "Liverpool FC":                           "Liverpool FC",
    # NBA
    "Los Angeles Lakers":                     "Los Angeles Lakers",
    "Boston Celtics":                         "Boston Celtics",
    "Golden State Warriors":                  "Golden State Warriors",
    # Top 14
    "Stade Toulousain":                       "Stade Toulousain",
    "Stade Rochelais":                        "Stade Rochelais",
}

# ── Playbook : référentiel tactique basketball ────────────────────────────────
PLAYBOOK: dict[str, dict] = {
    # ── ATTAQUE PLACÉE ────────────────────────────────────────────────────────
    "pick_and_roll": {
        "categorie": "Attaque placée / PnR",
        "objectif": "Créer un avantage numérique 2c1 entre porteur et pivot",
        "principe": "Le pivot pose un écran sur le défenseur du porteur. Deux options : le porteur attaque la séparation, le pivot roule ou pop vers la cible.",
        "avantages": "Polyvalent, difficile à défendre seul, crée déséquilibres en chaîne",
        "limites": "Lecture requise des deux joueurs, inefficace si pivot pop faible ou porteur lent",
        "reconnaître": "PG monte haut, C monte pour poser écran, action PG/C synchronisée",
        "vs_defense": "vs Drop : attaquer le mid-range du porteur. vs Hedge : roll rapide. vs Switch : chercher le mismatch. vs Ice : changer de côté",
        "contre_mesures": "Drop coverage, Hedge/Show agressif, Switch, Ice/Angle, Blitz double équipe",
    },
    "handoff": {
        "categorie": "Attaque placée",
        "objectif": "Créer un avantage de vitesse via transfert de balle courte distance",
        "principe": "Le porteur passe la balle à la main à un coéquipier qui coupe, avec ou sans écran du passeur",
        "avantages": "Crée confusion défensive porteur/receveur, difficile à défendre si timing parfait",
        "limites": "Requiert timing précis, facile à perturbertrap si anticipé",
        "reconnaître": "Joueur avec balle statique près de la raquette, partenaire qui coupe à côté",
        "vs_defense": "vs Switch : chercher mismatch immédiat. vs Hedge : accélérer la coupe",
        "contre_mesures": "Switch systématique, under tight pour empêcher la réception",
    },
    "isolation": {
        "categorie": "Attaque placée / Iso",
        "objectif": "Créer un 1c1 pur pour le meilleur créateur offensif",
        "principe": "Les 4 autres joueurs s'écartent (empty side ou quatre coins), le porteur attaque en 1c1",
        "avantages": "Simple à exécuter, exploite un mismatch, efficace pour clutch moments",
        "limites": "Dépendance à un joueur, fatigue physique, défenses peuvent réduire les aides",
        "reconnaître": "4 joueurs aux coins/ailes, porteur au milieu ou aile, espace vide côté fort",
        "vs_defense": "vs Help rapide : drive opposé ou mid-range. vs Zone : difficile, mieux vaut éviter",
        "contre_mesures": "Défense à deux, help agressive, force vers la faible main",
    },
    "post_up": {
        "categorie": "Attaque placée / Post",
        "objectif": "Exploiter un joueur dominant dans la raquette ou en poste bas",
        "principe": "Joueur reçoit balle dos au panier, jeux de pied pour créer tir ou passes à l'extérieur",
        "avantages": "Difficile à stopper si pivot technique, crée fautes, variété de moves",
        "limites": "Lent, difficile contre zones, efficacité dépend du niveau du pivot",
        "reconnaître": "C ou PF reçoit balle à mi-hauteur dos au panier, isolation des 4 autres",
        "vs_defense": "vs Double team : kick-out rapide vers shooteurs. vs Front : lob",
        "contre_mesures": "Double-team anticipée, front defense, empêcher la réception",
    },
    "motion_offense": {
        "categorie": "Attaque placée / Systèmes collectifs",
        "objectif": "Créer des tirs ouverts par le mouvement continu du ballon et des joueurs",
        "principe": "5 joueurs en mouvement permanent, passes + cuts + écrans sans séquences prédéfinies, lecture spontanée",
        "avantages": "Difficile à scouter, fatigue les défenseurs, nécessite peu de stars",
        "limites": "Requiert QI basket élevé de tous les joueurs, erreurs de lecture coûteuses",
        "reconnaître": "Mouvement perpétuel de tous les joueurs, pas de set plays évidents, passages de balle fluides",
        "vs_defense": "vs Zone : espacements modifiés, perçage des espaces. vs Switch : chercher les mismatches créés",
        "contre_mesures": "Deny agressif, communication défensive parfaite",
    },
    "princeton": {
        "categorie": "Attaque placée / Systèmes collectifs",
        "objectif": "Créer des layups faciles par des backdoor cuts et passes de poste haut",
        "principe": "Pivot haut (elbow), garde coupe backdoor quand défenseur over-joue, jeu court-long entre extérieurs et poste haut",
        "avantages": "Crée des layups contre défenses agressives, peu de tirs difficiles",
        "limites": "Extrêmement lent, requiert une discipline parfaite, facile à contrer avec défense droite",
        "reconnaître": "5 posté haut (elbow), coupes backdoor répétées, beaucoup de jeu à 2 hand-to-hand au poste haut",
        "vs_defense": "vs Drop : pull-up mid du porteur. vs Sur-play : backdoor cut",
        "contre_mesures": "Défense droite sans sur-jouer, bonne communication sur les backdoors",
    },
    "horns": {
        "categorie": "Attaque placée / Sets",
        "objectif": "Créer plusieurs options de lecture depuis une position de double poste haut",
        "principe": "Deux joueurs aux elbows (cornes), PG au sommet, les deux extérieurs aux coins. PG peut : drive, PnR avec un des pivots, passer à l'ailier qui coupe",
        "avantages": "Multiples options immédiates, difficile à scouter défensivement, base de nombreux ATO",
        "limites": "Requiert lecture rapide du PG, pivots doivent être bons en PnR et en pop",
        "reconnaître": "Formation initiale : 1 au sommet, 2 aux elbows, 2 aux coins",
        "vs_defense": "vs Zone 2-3 : attaque les espaces de la zone. vs Switch : exploiter les gros lents",
        "contre_mesures": "Communiquer sur qui prend le PG, not commit sur les leurres",
    },
    "flex": {
        "categorie": "Attaque placée / Systèmes collectifs",
        "objectif": "Créer des tirs sous cloche ou en poste bas via des séquences d'écrans",
        "principe": "Combinaison d'un écran de bas du poste (flex screen) + écran transversal en haut (down screen), joueurs tournent en séquence",
        "avantages": "Difficile à défendre si équipe bien synchronisée, crée des layups et des tirs ouverts",
        "limites": "Mécanique, prévisible, requiert entraînement important",
        "reconnaître": "Séquences répétées écran-coupe-écran, joueurs qui traversent la raquette",
        "vs_defense": "vs physique : varier les angles d'écran. vs under : pop vers 3pts",
        "contre_mesures": "Over les écrans sur les bons tireurs, under sur les non-tireurs",
    },
    "spread_offense": {
        "categorie": "Attaque placée / Spacing",
        "objectif": "Maximiser l'espace pour les drives et le pick and roll par espacement maximal",
        "principe": "5 joueurs capables de tirer à 3 points forcent la défense à être sur la ligne des 3pts, créant des couloirs de drive immenses",
        "avantages": "Crée des espaces énormes pour les pénétrateurs, impossible à défendre en zone",
        "limites": "Requiert 5 joueurs qui menacent de 3pts, peu efficace si tirs froids",
        "reconnaître": "Tous les joueurs sur ou hors de la ligne des 3pts, espace énorme dans la raquette",
        "vs_defense": "vs Zone : presque impossible à jouer en zone contre 5 tireurs",
        "contre_mesures": "Man-to-man avec helps tardives, couvrir les tireurs en priorité",
    },
    "dribble_drive": {
        "categorie": "Attaque placée / Drive",
        "objectif": "Créer des pénétrations à répétition en exploitant l'espace de la spread",
        "principe": "Porteur agresse gap du défenseur, les 4 autres restent aux coins/ailes, joueurs perchés font des kick-outs ou suivent le drive",
        "avantages": "Génère beaucoup de fautes, crée layups ou tirs ouverts kick-out",
        "limites": "Exige pénétrateurs élite, peu de jeu intérieur posté",
        "reconnaître": "Porteur cherche systématiquement le gap, coupes de caddie ou lob, kick-outs fréquents",
        "vs_defense": "vs help : kick-out aux coins. vs pack : score au cercle ou mi-distance",
        "contre_mesures": "Pack-line defense, contester tôt le drive, communiquer sur les kick-outs",
    },
    "transition_offense": {
        "categorie": "Transition",
        "objectif": "Attaquer avant que la défense soit replacée pour créer des tirs faciles",
        "principe": "Après rebond défensif ou interception, course rapide pour créer surnombre (3c2, 2c1), ou avancer le ballon avant set de la défense",
        "avantages": "Tirs très faciles (layups, 3pts ouverts), fatigue la défense",
        "limites": "Faible si adversaire bon en transition défensive, risque de perte de balle à la hâte",
        "reconnaître": "Sortie rapide du rebond, outlet pass, courses longues des ailes",
        "vs_defense": "vs défense qui recule : accélérer. vs défense qui sprinte : ralentir et setter",
        "contre_mesures": "Sprint au retour, protéger le cercle en premier, ne pas surengager en attaque",
    },
    "zone_offense": {
        "categorie": "Attaque placée / vs Zone",
        "objectif": "Trouver et exploiter les trous dans les zones défensives",
        "principe": "Attaquer les espaces entre défenseurs (gap), utiliser les passes rapides pour déplacer la zone, trouver le haut du cercle (souvent non couvert)",
        "avantages": "Déstabilise les zones si exécution rapide, crée des tirs ouverts aux espaces",
        "limites": "Requiert entraînement spécifique, moins efficace si balle lente",
        "reconnaître": "Attaque à la zone est identifiable : espacement modifié, flash au poste haut, perçage des gaps",
        "vs_defense": "vs 2-3 : attaquer le milieu haut, corners. vs 3-2 : baseline",
        "contre_mesures": "Ralentir la balle, forcer à jouer en dessous de la ligne de fond",
    },
    "ato": {
        "categorie": "Situations spéciales / ATO",
        "objectif": "Créer un tir ouvert de qualité en 5 secondes après un timeout",
        "principe": "Set play dessiné pendant le temps mort, exploitant un mismatch ou une action que l'adversaire n'a pas préparé",
        "avantages": "Très efficace si équipe adverse sort de la défense, joueur star libre",
        "limites": "L'adversaire peut contrer si le set est connu, nécessite une exécution parfaite sous pression",
        "reconnaître": "Tous les joueurs partent de la même position initiale (souvent horns ou stack), action rapide",
        "vs_defense": "vs toutes défenses : lire le mismatch immédiatement et adapter",
        "contre_mesures": "Communication rapide des défenseurs, sprint aux postes clés, pas de switch surprise",
    },
    "slob": {
        "categorie": "Situations spéciales / SLOB",
        "objectif": "Marquer ou avancer facilement depuis une remise en jeu latérale",
        "principe": "Depuis la touche côté, créer un tir ouvert pour le meilleur joueur via 1-2 écrans. Peut être une action pour playmaker ou tireur extérieur",
        "avantages": "Temps illimité pour dessiner, action souvent mémorisée en entraînement",
        "limites": "5 secondes maximum, défense souvent bien organisée sur SLOB",
        "reconnaître": "Remise en jeu latérale, stack de joueurs qui explosent, souvent après faute ou stoppage",
        "vs_defense": "vs switch : chercher le mismatch. vs no-switch : attaquer le tireur libre",
        "contre_mesures": "Communication sur tous les écrans, pas de switch sur les mauvais matchups",
    },
    "blob": {
        "categorie": "Situations spéciales / BLOB",
        "objectif": "Marquer depuis une remise en jeu sous le panier adverse",
        "principe": "Stack ou ligne de joueurs qui explosent dans différentes directions via écrans. Options : tir rapproché, lob, pass de retour pour 3pts corner",
        "avantages": "Très proche du panier, bon scoring avec bonne exécution",
        "limites": "Défense souvent très organisée, angle de passe difficile",
        "reconnaître": "Remise en jeu sous panier, stack initial compact, explosions multiples",
        "vs_defense": "vs défense qui switch : lob immédiat. vs défense droite : écran doublé pour tireur corner",
        "contre_mesures": "Défendre le lob en premier, couvrir les corners, ne pas switch sur les pivots",
    },
    # ── DÉFENSE ───────────────────────────────────────────────────────────────
    "defense_homme": {
        "categorie": "Défense / Homme à homme",
        "objectif": "Marquer chaque attaquant individuellement, conserver la responsabilité individuelle",
        "principe": "Chaque défenseur est assigné à un attaquant précis. Communication sur les écrans : switch ou go-through",
        "avantages": "Responsabilité claire, difficile de trouver des joueurs libres si bien exécuté",
        "limites": "Vulnérable aux good screeners, requiert niveau physique élevé de tous",
        "reconnaître": "Défenseur colle son attaquant partout, communication verbale constante",
        "vs_offense": "vs PnR : choisir switch, hedge, drop, ice selon joueurs",
        "contre_mesures": "Écrans multiples, PnR ciblant le défenseur le plus faible",
    },
    "defense_zone": {
        "categorie": "Défense / Zone",
        "objectif": "Défendre par secteur géographique plutôt qu'individu, protéger la raquette",
        "principe": "Chaque défenseur couvre une zone du terrain, coopération pour couvrir les espaces entre zones",
        "avantages": "Protège les défenseurs en faute, déstabilise les équipes peu entraînées au zone offense",
        "limites": "Vulnérable aux bonnes passes et aux équipes avec spacing extérieur",
        "reconnaître": "Défenseurs se déplacent en miroir de la balle en secteur, pas de marquage individuel",
        "vs_offense": "vs passes rapides : attaquer les espaces gap. vs corner : le corner est souvent ouvert en 2-3",
        "contre_mesures": "Passes rapides, écrans dans la zone, trouver le flash haut",
    },
    "press_terrain": {
        "categorie": "Défense / Press",
        "objectif": "Provoquer des pertes de balle et fatiguer l'adversaire par pression sur tout le terrain",
        "principe": "Défense agressive dès la remise en jeu ou le rebond, forcer l'adversaire à dribbler sous pression sur tout le terrain",
        "avantages": "Génère des interceptions, met en difficulté les équipes lentes, crée un rythme élevé",
        "limites": "Très exigeant physiquement, vulnérable aux équipes calmes et aux bons dribbleurs",
        "reconnaître": "Défenseurs qui courent jusqu'au rebond adverse, pression dès la remise en jeu",
        "vs_offense": "vs press : dribbleur calme + passes longues + flash center",
        "contre_mesures": "Passes sûres court terme, jouer avec 5 relayeurs, balle au meilleur dribbleur",
    },
    "trap": {
        "categorie": "Défense / Trap",
        "objectif": "Forcer une perte de balle en doublant brusquement le porteur aux coins ou aux dribbles",
        "principe": "Deux défenseurs convergent sur le porteur au moment précis où il est piégé (corner, sur côté), les 3 autres interceptent",
        "avantages": "Génère des pertes de balle, déstabilise les meneurs moins expérimentés",
        "limites": "3 autres joueurs doivent couvrir 4 adversaires, risky si mal exécuté",
        "reconnaître": "Deux défenseurs sur un porteur, positionnement en triangle des 3 autres",
        "vs_offense": "vs trap : passer avant que le deuxième défenseur arrive",
        "contre_mesures": "Trap au corner, sur le côté après dribble, sur réception après écran",
    },
    "switch": {
        "categorie": "Défense / PnR Coverage",
        "objectif": "Neutraliser le PnR en échangeant les marquages sans aide défensive",
        "principe": "Au signal, défenseur du porteur prend le pivot et vice versa, aucune aide requise, chacun reste sur son adversaire échangé",
        "avantages": "Simple à exécuter, pas de hedging ou gap à couvrir, efficace vs PnR si équipe polyvalente",
        "limites": "Crée des mismatches (petit sur grand, lent sur rapide), exploitable si adversaire intelligent",
        "reconnaître": "Défenseurs qui s'échangent au contact de l'écran sans communication longue",
        "vs_offense": "vs switch : chercher le mismatch immédiatement (iso sur le petit défenseur)",
        "contre_mesures": "Ne switcher que 1-4 (pas le 5), ou switcher uniquement avec profils similaires",
    },
    "hedge": {
        "categorie": "Défense / PnR Coverage",
        "objectif": "Ralentir le porteur après l'écran pour laisser le défenseur revenir",
        "principe": "Le défenseur du pivot sort vigoureusement pour bloquer le chemin du porteur (hedge/show), le défenseur du porteur contourne l'écran (go-under ou over) et reprend son homme",
        "avantages": "Empêche le drive facile du porteur, maintient la responsabilité individuelle",
        "limites": "Coûteux en énergie, le pivot doit être surveillé pendant le hedge",
        "reconnaître": "Défenseur du C sort agressivement sur le porteur au moment de l'écran",
        "vs_offense": "vs hedge : passer immédiatement au C qui roll derrière le défenseur écarté",
        "contre_mesures": "Hard show (exagéré), soft show, choisir selon timing",
    },
    "drop": {
        "categorie": "Défense / PnR Coverage",
        "objectif": "Protéger la raquette contre les roll hommes forts sans risquer de donner des tirs mi-distance",
        "principe": "Défenseur du pivot reste bas (dans la raquette), défenseur du porteur passe over ou tight, adversaire peut prendre le mid-range",
        "avantages": "Protège le cercle, défenseur du C reste entre la balle et le panier",
        "limites": "Concède les mid-ranges au porteur, inefficace vs les bons tireurs PG",
        "reconnaître": "Défenseur du C reste dans la raquette sans bouger sur l'écran",
        "vs_offense": "vs drop : porteur doit avoir un bon pull-up mid-range",
        "contre_mesures": "Ajuster la profondeur du drop selon le danger du porteur",
    },
    "ice": {
        "categorie": "Défense / PnR Coverage",
        "objectif": "Forcer le porteur du PnR à aller vers l'extérieur (baseline), loin du roll homme",
        "principe": "Défenseur du porteur se positionne côté fort pour forcer le drive vers la ligne de fond où le pivot peut aider plus facilement",
        "avantages": "Éloigne le porteur du roll homme, aide plus simple pour le défenseur du C",
        "limites": "Concède le drive baseline, le porteur peut pop vers l'extérieur si bien entraîné",
        "reconnaître": "Défenseur du PG positionné côté ballon avant l'écran, force vers la baseline",
        "vs_offense": "vs ice : écran doit être posé côté fort pour neutraliser le forçage",
        "contre_mesures": "Utiliser sur les côtés, communication 'ICE' dès que le screen est vu",
    },
    "blitz": {
        "categorie": "Défense / PnR Coverage",
        "objectif": "Forcer une perte de balle ou une mauvaise décision par double-équipe immédiate au PnR",
        "principe": "Dès l'écran, les deux défenseurs (porteur ET pivot) convergent agressivement sur le porteur. 3 autres joueurs interceptent les passes",
        "avantages": "Arrête les porteurs dominants du PnR, génère des turnovers si mal lu",
        "limites": "Risqué : laisse des joueurs libres, requiert lectures parfaites des 3 autres",
        "reconnaître": "Deux défenseurs sur le porteur dès l'écran, positionnement X-out des 3 autres",
        "vs_offense": "vs blitz : porteur doit passer vite au pop ou au slip avant que le second arrive",
        "contre_mesures": "Trigger : signal verbal ou positional, X-out des 3 autres immédiat",
    },
    "help_recover": {
        "categorie": "Défense / Aide",
        "objectif": "Stopper la pénétration tout en récupérant sa responsabilité sur le relais",
        "principe": "Un défenseur hors-balle vient aider sur le drive, son attaquant est temporairement libre, le défenseur revient sur son attaquant après que le drive est stoppé",
        "avantages": "Stoppe les drives sans laisser de tir facile si récupération rapide",
        "limites": "Si récupération trop lente, l'attaquant libre tire. Requiert lecture et sprint",
        "reconnaître": "Un défenseur sort de son attaquant pour bloquer un drive, récupère rapidement",
        "vs_offense": "vs help : kick-out immédiat vers l'attaquant laissé libre",
        "contre_mesures": "Communication 'HELP', sprint de récupération, timing précis",
    },
    "zone_press": {
        "categorie": "Défense / Press Zone",
        "objectif": "Générer des turnovers par une pression de zone agressif sur tout le terrain",
        "principe": "Zone appliquée en pression full court, typiquement 2-2-1. Premier rideau sur la balle, second rideau au milieu, dernier rideau au panier",
        "avantages": "Moins fatigant que le press homme, piège les équipes peu entraînées",
        "limites": "Attaque par le milieu peut être dévastatrice, équipe avec bon passeur peut la démolir",
        "reconnaître": "Formation 2-2-1 visibles depuis les tribunes, rotation de zone sur tout le terrain",
        "vs_offense": "vs 2-2-1 : dribbler par le milieu, passer au flash center",
        "contre_mesures": "Choisir 1-2-1-1 ou 2-2-1 selon effectif disponible",
    },
    "matchup_zone": {
        "categorie": "Défense / Zone spéciale",
        "objectif": "Combiner les avantages de l'homme à homme et de la zone pour déstabiliser l'adversaire",
        "principe": "Aspect zone : défenseurs bougent en référence au secteur. Aspect homme : quand le porteur entre dans une zone, un défenseur le marque individuellement",
        "avantages": "Difficile à lire pour l'adversaire, protège les mismatchs individuels, polyvalent",
        "limites": "Très complexe à enseigner, confusion possible entre coéquipiers si mal communiqué",
        "reconnaître": "Semble homme à homme mais les défenseurs ne suivent pas leurs attaquants hors de zone",
        "vs_offense": "Difficile : garder la balle en mouvement rapide, identifier le principe",
        "contre_mesures": "Communication parfaite, identifier les responsabilités",
    },
    # ── VARIATIONS AVANCÉES ───────────────────────────────────────────────────
    "empty_side_pnr": {
        "categorie": "PnR Variations",
        "objectif": "Maximiser l'espace pour le porteur du PnR en vidant le côté de l'action",
        "principe": "Les 3 autres joueurs se positionnent du côté opposé de l'écran, laissant tout le côté vide. Aucune aide défensive possible sans quitter un attaquant",
        "avantages": "Elimine les aides latérales, porteur peut drive ou mid-range sans obstacle",
        "limites": "Le porteur doit être capable de finir seul ou de lire les aides tardives",
        "reconnaître": "3 joueurs tous du même côté, PnR côté vide",
        "vs_defense": "vs drop : pull-up immédiat. vs hedge : roll gap énorme. vs blitz : aucune aide du côté vide",
        "contre_mesures": "Switch immédiat ou blitz pour forcer le pass vers les joueurs loin",
    },
    "double_drag": {
        "categorie": "PnR Variations",
        "objectif": "Créer une confusion défensive maximale avec deux écrans successifs en transition",
        "principe": "Le PG remonte la balle, deux joueurs posent des écrans successifs en course (drag screens). Le PG peut utiliser le premier ou le second",
        "avantages": "Très difficile à défendre en transition, crée des mismatches si switch",
        "limites": "Requiert deux bons poseurs d'écran et une bonne lecture du PG",
        "reconnaître": "PG qui remonte vite, deux joueurs qui sprinte et posent écrans haut côte à côte",
        "vs_defense": "vs switch : le PG choisit l'écran qui crée le meilleur mismatch. vs hedge : roll immédiat",
        "contre_mesures": "Switch systématique 1-4, ou two defenders hedge ensemble",
    },
    "spain_pnr": {
        "categorie": "PnR Variations",
        "objectif": "Créer un tir ouvert pour un tireur en ajoutant un écran supplémentaire sous le roll homme",
        "principe": "PnR classique en haut. Un 3ème joueur pose un écran sur le défenseur du roll homme sous la raquette. Crée un pick-the-picker pour le roll",
        "avantages": "Quasi-impossible à défendre sans switch ou double effort, crée un layup ou dunk sur roll",
        "limites": "Requiert 3 joueurs synchronisés, peut être illégal si mal exécuté",
        "reconnaître": "PnR en haut + un joueur qui va poser un écran sur le défenseur du C dans la raquette",
        "vs_defense": "vs switch : chercher le mismatch chain. vs hedge : le roll man est totalement libre",
        "contre_mesures": "Switch sur le 3ème écran, communiquer 'SPAIN'",
    },
    "delay_offense": {
        "categorie": "Attaque / Gestion du temps",
        "objectif": "Gérer le temps tout en maintenant la menace offensive pour forcer l'adversaire à sortir",
        "principe": "Motion lente, garder la balle en sécurité, exploiter les espaces si la défense sur-joue pour voler la balle. Utilisé pour protéger un avantage",
        "avantages": "Gère le score, fatigue les défenseurs qui courent pour piquer la balle",
        "limites": "Risque de faute technique pour passivité, peut encourager le foul game adverse",
        "reconnaître": "Passes lentes autour du périmètre, mouvement minimal, gestion de l'horloge",
        "vs_defense": "vs défense qui sort : drive immédiat. vs défense passive : layup ou tir facile",
        "contre_mesures": "Pression sur le porteur, foul stratégique si score le permet",
    },
    "stack_action": {
        "categorie": "Attaque / Sets",
        "objectif": "Créer de la confusion et des libérations multiples depuis une formation compacte",
        "principe": "Plusieurs joueurs dans une zone compacte (stack), explosent dans différentes directions avec des écrans croisés. Défenseurs perdent leurs hommes",
        "avantages": "Très difficile à défendre si bien synchronisé, plusieurs lecteurs possibles simultanément",
        "limites": "Requiert beaucoup d'entraînement, confusion possible entre coéquipiers",
        "reconnaître": "3-4 joueurs au même endroit (souvent coté fort) avant l'action",
        "vs_defense": "vs switch : chercher le mismatch. vs man strict : le décalage se crée naturellement",
        "contre_mesures": "Communication préventive sur qui prend qui, ne pas switch sur les mauvais matchups",
    },
    "flare_screen": {
        "categorie": "Ecrans / Mouvements sans balle",
        "objectif": "Libérer un tireur extérieur via un écran posé loin du porteur, en direction du coin ou de l'aile",
        "principe": "Joueur sans balle se déplace vers l'extérieur, partenaire pose un écran vers l'extérieur (flare), le tireur sort vers le coin ou l'aile pour recevoir",
        "avantages": "Crée un tir à 3 points ouvert pour les bons tireurs, difficile à défendre si timing parfait",
        "limites": "Peu efficace si le tireur n'est pas menaçant, l'écranneur doit être bien positionné",
        "reconnaître": "Joueur qui court vers l'extérieur avec un écran latéral loin du porteur",
        "vs_defense": "vs over : le tireur change de direction. vs under : il reçoit en rythme",
        "contre_mesures": "Défenseur sur le tireur joue entre l'écran et son homme, pas par derrière",
    },
    "staggers": {
        "categorie": "Ecrans / Mouvements sans balle",
        "objectif": "Libérer un tireur d'élite via deux ou trois écrans successifs",
        "principe": "Le tireur court à travers 2-3 écrans posés en séquence par des coéquipiers, créant un décalage difficile à suivre défensivement",
        "avantages": "Quasi-impossible à défendre pour les bons tireurs, crée un tir à 3pts ouvert régulièrement",
        "limites": "Requiert des poseurs d'écran sérieux et le timing du tireur",
        "reconnaître": "Un joueur qui passe à travers deux écrans successifs à l'aile ou au corner",
        "vs_defense": "vs over tight : le premier écran crée de la distance. vs switch : mismatch garanti",
        "contre_mesures": "Jump switch sur le premier écran avant que le second soit posé",
    },
    "pistol_action": {
        "categorie": "Attaque / Sets",
        "objectif": "Créer un PnR en transition déguisé via un dos-au-panier suivi d'un sprint",
        "principe": "PG passe à un ailier et coupe à 45°. L'ailier reçoit et fait face au panier, le PG reçoit en retour et un C pose un écran immédiat. Crée un PnR tempo élevé",
        "avantages": "Combine la transition et le demi-terrain, créé un PnR avant que la défense soit set",
        "limites": "Requiert timing parfait, peut être contré si défense lit la coupture du PG",
        "reconnaître": "PG coupe après passe à l'aile, reçoit en retour, écran immédiat du C",
        "vs_defense": "vs hedge tardif : porteur peut attaquer. vs switch préventif : mismatch potentiel",
        "contre_mesures": "Défenseur du PG anticipe la coupe, communication sur le PnR immédiat",
    },
    "zipper": {
        "categorie": "Ecrans / Mouvements sans balle",
        "objectif": "Amener un tireur ou créateur du coin vers la tête de la raquette via un écran du poste bas",
        "principe": "Joueur au corner court vers le haut via un écran du joueur de poste. Reçoit à l'elbow ou au sommet pour attaquer ou shooter",
        "avantages": "Crée un tir à mi-distance ou 3pts difficile à défendre, amène de la densité en haut",
        "limites": "Peu efficace si le défenseur est en avance sur la coupe",
        "reconnaître": "Joueur qui part du corner vers la tête de raquette via l'écran du poste bas",
        "vs_defense": "vs over : le joueur reçoit avec de l'espace. vs under : drive immédiat vers la ligne de fond",
        "contre_mesures": "Défenseur doit être proactif, anticiper la coupe",
    },
    "hammer": {
        "categorie": "Ecrans / Situations spéciales",
        "objectif": "Créer un tir à 3 points ouvert au corner via un écran en baseline pendant une pénétration",
        "principe": "Porteur drive vers la ligne de fond. Un joueur court vers le corner et reçoit un écran d'un coéquipier (hammer screen). Porteur kick-out vers le corner libre",
        "avantages": "Crée un 3pts ouvert pendant que la défense est occupée par le drive, difficile à anticiper",
        "limites": "Requiert porteur capable de passer du corner en drive, timing précis",
        "reconnaître": "Drive vers la baseline, joueur qui reçoit un écran en baseline et court au corner pour kick-out",
        "vs_defense": "vs défense sur le drive : passe au corner libre. vs close-out tardif : tir ouvert",
        "contre_mesures": "Défenseur du corner annonce 'HAMMER', sprint sur le tir possible",
    },
    "elevator_screen": {
        "categorie": "Ecrans / Animations",
        "objectif": "Libérer un tireur avec un couloir d'écran qui 'se ferme' sur le défenseur",
        "principe": "Deux joueurs côte à côte (avec un espace entre eux), le tireur passe entre eux puis les deux écraneurs se referment ensemble sur le défenseur qui suit. Couloir d'ascenseur",
        "avantages": "Piège complètement le défenseur si bien synchronisé, crée un tir à 3pts en rythme parfait",
        "limites": "Requiert deux bons poseurs d'écran et timing parfait du tireur",
        "reconnaître": "Deux joueurs côte à côte avec espace, tireur qui s'y engouffre, portes qui se ferment",
        "vs_defense": "vs switch préventif : le tireur change de direction. vs over : timing difficile mais possible",
        "contre_mesures": "Switch anticipé ou communication 'ELEVATOR' pour que le défenseur du tireur aille par dessus",
    },
}

# ── Football Tactics Playbook ─────────────────────────────────────────────────
FOOTBALL_PLAYBOOK: dict[str, dict] = {
    # ── SYSTÈMES / FORMATIONS ─────────────────────────────────────────────────
    "4-3-3": {
        "categorie": "Système / Formation",
        "objectif": "Domination possession et largeur offensive",
        "structure": "4 défenseurs, 3 milieux (MDC+2MC), 3 attaquants larges (2 ailiers + 1 avant-centre)",
        "declencheurs": "Équipe technique, ailiers de vitesse, MDC box-to-box",
        "avantages": "Largeur naturelle, pression haute efficace, transitions rapides sur les côtés",
        "limites": "Milieu sous-nombre si MDC seul contre 2 adverses, flancs exposés si ailiers ne défendent pas",
        "reconnaitre": "Ailiers larges qui hurlent la ligne de touche, MDC seul au centre, latéraux qui montent",
        "adaptations": "Ailiers rentrants + latéraux doublés côté, ou MDC stagger pour protéger",
        "contre_mesures": "Surcharger le milieu, pressing latéraux, transition sur les flancs exposés",
    },
    "4-2-3-1": {
        "categorie": "Système / Formation",
        "objectif": "Solidité défensive avec double pivot et largeur contrôlée",
        "structure": "4 défenseurs, double pivot, 1 meneur (n°10), 2 ailiers larges, 1 avant-centre",
        "declencheurs": "Équipe qui veut contrôler sans trop prendre de risques, meneur technique créateur",
        "avantages": "Double pivot protège, n°10 a de l'espace, transitions sur les côtés",
        "limites": "N°10 doit être excellent sinon aucune création, double pivot peut être lent",
        "reconnaitre": "Deux milieux récupérateurs côte à côte, joueur n°10 entre les lignes, ailiers larges",
        "adaptations": "Meneur récupérateur ou créateur selon phase, latéraux offensifs pour compenser",
        "contre_mesures": "Presser le n°10 entre les lignes, bloquer les reçus entre les lignes",
    },
    "4-4-2": {
        "categorie": "Système / Formation",
        "objectif": "Équilibre défensif-offensif, organisation collective claire",
        "structure": "4 défenseurs, 4 milieux (2 centraux + 2 ailiers), 2 attaquants en ligne",
        "declencheurs": "Équipe physique, duo d'attaquants complémentaires, milieux de terrain boîte-à-boîte",
        "avantages": "Compacité naturelle, double menace offensive, redoublements sur les côtés",
        "limites": "Manque de créativité si pas de joueur technique entre les lignes",
        "reconnaitre": "4 milieux en ligne, duo d'attaquants côte à côte, très compact",
        "adaptations": "4-4-2 losange (avec meneur), 4-4-2 avec milieux créatifs",
        "contre_mesures": "Jouer entre les lignes du bloc, utiliser le demi-espace",
    },
    "3-4-3": {
        "categorie": "Système / Formation",
        "objectif": "Agressivité offensive, surcharge sur les côtés",
        "structure": "3 défenseurs centraux, 4 milieux (2 pistons + 2 centraux), 3 attaquants",
        "declencheurs": "Équipe technique polyvalente, pistons endurants, défenseurs centraux qui jouent en 1c1",
        "avantages": "Supériorité numérique sur les côtés avec pistons, pressing haut structuré",
        "limites": "Extrêmement vulnérable aux transitions, 3 DC contre transitions rapides",
        "reconnaitre": "3 DC visibles, pistons très haut, attaque large",
        "adaptations": "Transition défensive = pistons qui reculent vite",
        "contre_mesures": "Transition rapide sur les flancs, exploiter l'espace derrière les pistons",
    },
    "3-5-2": {
        "categorie": "Système / Formation",
        "objectif": "Contrôle du milieu et solidité défensive à 5 derrière en repli",
        "structure": "3 défenseurs centraux, 5 milieux (2 pistons + 3 centraux), 2 attaquants",
        "declencheurs": "Équipe défensive qui veut surcharger le milieu, bons pistons bilatéraux",
        "avantages": "5 joueurs de milieu = domination du centre, solidité défensive à 5 en repli",
        "limites": "Pistons doivent couvrir tout le terrain, limitant si fatigués",
        "reconnaitre": "Milieu de terrain très large, 3 DC en repli, pistons alternant haut et bas",
        "adaptations": "En possession → 3-5-2. En repli → 5-3-2",
        "contre_mesures": "Contre-attaque sur les espaces laissés par les pistons",
    },
    "4-1-4-1": {
        "categorie": "Système / Formation",
        "objectif": "Protection défensive par le pivot bas, étage offensif à 4",
        "structure": "4 défenseurs, 1 pivot bas, 4 milieux offensifs en ligne, 1 avant-centre",
        "declencheurs": "Équipe avec récupérateur élite, 4 milieux techniques et offensifs",
        "avantages": "Pivot bas protège le bloc, 4 milieux créent du surnombre offensif",
        "limites": "Si le pivot est dépassé, le bloc est percé. L'avant-centre peut être isolé",
        "reconnaitre": "1 joueur seul devant la défense, 4 milieux en ligne derrière lui",
        "adaptations": "Pivot qui couvre les espaces, milieux offensifs qui se replient",
        "contre_mesures": "Presser le pivot en double, jouer dans les espaces entre le pivot et les milieux",
    },
    "5-3-2": {
        "categorie": "Système / Formation",
        "objectif": "Solidité défensive maximale, contre-attaque rapide",
        "structure": "5 défenseurs (3 DC + 2 latéraux pistons), 3 milieux, 2 attaquants",
        "declencheurs": "Équipe qui veut protéger un avantage ou affronter un adversaire supérieur",
        "avantages": "Quasi-imperméable défensivement, efficace en contre-attaque",
        "limites": "Très passif offensivement, pistons doivent monter pour attaquer",
        "reconnaitre": "5 joueurs en défense, bloc bas compact, contre-attaques directes",
        "adaptations": "Pistons qui montent selon le pressing adverse",
        "contre_mesures": "Patience, circulation rapide, tirs de loin pour sortir le bloc",
    },
    "4-3-2-1": {
        "categorie": "Système / Formation",
        "objectif": "Possession et densité centrale, créativité entre les lignes",
        "structure": "4 défenseurs, 3 milieux, 2 joueurs entre les lignes (meneur + ailier intérieur), 1 avant-centre",
        "declencheurs": "Équipe très technique, joueurs entre les lignes capables de dribble et de passe",
        "avantages": "Supériorité numérique au centre, difficile à presser, créativité entre les lignes",
        "limites": "Peu de largeur naturelle, flancs exposés, latéraux très sollicités",
        "reconnaitre": "Formation en sapin caractéristique, densité centrale, latéraux très haut",
        "adaptations": "Latéraux offensifs compensent le manque de largeur",
        "contre_mesures": "Écraser le centre, défendre en bloc bas, utiliser la largeur pour étirer",
    },
    # ── PRINCIPES OFFENSIFS ───────────────────────────────────────────────────
    "build_up_court": {
        "categorie": "Principe offensif",
        "objectif": "Ressortir proprement depuis le gardien en combinaisons courtes",
        "structure": "DC qui s'écartent, MDC qui descend entre les DC, gardien au sol",
        "declencheurs": "Adversaire non-pressant, équipe technique et courageuse balle au pied",
        "avantages": "Contrôle du rythme, attirer l'adversaire haut pour jouer derrière lui",
        "limites": "Risque de perte de balle dangereuse en zone de construction",
        "reconnaitre": "Gardien qui relance au pied, DC écartés, MDC qui descend",
        "adaptations": "Switch vers build-up long si press agressif adverse",
        "contre_mesures": "Pressing haut coordonné avec trap zone sur le gardien ou les DC",
    },
    "build_up_long": {
        "categorie": "Principe offensif",
        "objectif": "Sauter le pressing adverse par des passes longues vers les attaquants",
        "structure": "Gardien ou DC en profondeur, cibles longues (avant-centre ou ailier), deuxième balle",
        "declencheurs": "Adversaire qui presse haut, équipe avec cibles aériennes ou de vitesse",
        "avantages": "Rapide, neutralise le pressing, efficace si cibles solides dans les duels",
        "limites": "Peut perdre la balle facilement, dépend de la qualité des deuxièmes balles",
        "reconnaitre": "Passes longues directes depuis la défense, attaquants qui cherchent profondeur",
        "adaptations": "Combinaison avec troisième homme pour récupérer la deuxième balle",
        "contre_mesures": "Défense haute compacte sur les cibles, bien gagner les secondes balles",
    },
    "third_man": {
        "categorie": "Principe offensif",
        "objectif": "Créer une ligne de passe supplémentaire via un troisième joueur en déplacement",
        "structure": "Joueur A passe à B, pendant que C se déplace en troisième option. B passe à C qui est libre",
        "declencheurs": "Défense qui suit la balle, joueurs capables de mouvements sans ballon",
        "avantages": "Déstructure la défense, crée des espaces, difficilement pressable",
        "limites": "Requiert lecture simultanée de 3 joueurs et timing parfait",
        "reconnaitre": "Mouvement anticipé d'un joueur tiers pendant un échange A-B",
        "adaptations": "Peut aussi fonctionner sur corner ou free kick",
        "contre_mesures": "Défense en zone, intercepter les passes vers le 3ème homme",
    },
    "overload_isolate": {
        "categorie": "Principe offensif",
        "objectif": "Surcharger un côté pour libérer le côté opposé",
        "structure": "3-4 joueurs se concentrent côté fort, 1 joueur seul côté faible, switch rapide",
        "declencheurs": "Adversaire qui suit les mouvements numériques, latéral adverse poussé à monter",
        "avantages": "Crée un 1c1 ou 2c1 côté faible, difficile à défendre si switch rapide",
        "limites": "Nécessite un switch de jeu précis et rapide sous pression",
        "reconnaitre": "Accumulation numérique d'un côté, puis long switch vers l'espace libre",
        "adaptations": "Peut être déclenché par un latéral inversé ou une passe diagonale",
        "contre_mesures": "Ne pas suivre la surcharge, maintenir la forme défensive",
    },
    "half_space": {
        "categorie": "Principe offensif",
        "objectif": "Occuper les demi-espaces pour créer des lignes de passe obliques et des finitions au cercle",
        "structure": "Joueurs entre l'axe central et les latéraux (zones 8 et 14 du terrain), disponibles en réception",
        "declencheurs": "Équipe technique, joueurs capables de se retourner et de passer sous pression",
        "avantages": "Zone la plus dangereuse offensivement, difficile à défendre en zone ou en homme",
        "limites": "Requiert des joueurs techniques et conscients du terrain",
        "reconnaitre": "Milieu ou ailier intérieur qui se positionne entre le latéral et le DC adverse",
        "adaptations": "Ailiers intérieurs, pistons inversés, n°10 mobile",
        "contre_mesures": "Défenseur qui suit le joueur dans le demi-espace, compacité du bloc central",
    },
    "width_depth": {
        "categorie": "Principe offensif",
        "objectif": "Étirer la défense dans toutes les dimensions pour créer des espaces centraux",
        "structure": "Ailiers larges + avant-centre qui tire les DC en profondeur, latéraux hauts",
        "declencheurs": "Équipe rapide sur les côtés, avant-centre avec bonne course en profondeur",
        "avantages": "Défense étirée = espaces centraux immenses pour les milieux",
        "limites": "Si les attaquants ne tirent pas suffisamment les défenseurs, les espaces ne se créent pas",
        "reconnaitre": "Ailiers au maximum de la largeur, avant-centre qui fait des courses de profondeur",
        "adaptations": "Croiser largeur et profondeur : ailier large + course en profondeur de l'autre côté",
        "contre_mesures": "Défense haute pour couper les courses en profondeur, ne pas suivre les ailiers larges",
    },
    "positional_play": {
        "categorie": "Principe offensif",
        "objectif": "Conserver la balle en supériorité numérique locale pour progresser",
        "structure": "Triangles et losanges constants, joueurs toujours à 3 options de passe, positionnement entre les lignes",
        "declencheurs": "Équipe très technique, lecture collective du pressing adverse",
        "avantages": "Épuise l'adversaire, crée des passe-et-va dangereux, contrôle absolu",
        "limites": "Lent si adversaire bien organisé, peut manquer de verticalité",
        "reconnaitre": "Possession longue, triangles constants, joueurs qui cherchent toujours le 3ème homme",
        "adaptations": "Verticalisation dès que l'espace se crée, ne pas jouer pour jouer",
        "contre_mesures": "Pressing intense et organisé, trap zones, interdire les réceptions entre les lignes",
    },
    "direct_play": {
        "categorie": "Principe offensif",
        "objectif": "Attaquer rapidement la profondeur avec peu de touches de balle",
        "structure": "Passes verticales directes, appuis courts en transition vers la profondeur, avant-centre target man",
        "declencheurs": "Adversaire haut, équipe avec speed attaquants, cibles aériennes",
        "avantages": "Surprend les défenses replacées, réduit le temps de réaction adverse",
        "limites": "Dépend de la qualité des cibles et des deuxièmes balles, peu de contrôle",
        "reconnaitre": "Peu de passes, verticalité immédiate, avant-centre qui cherche profondeur",
        "adaptations": "Combiner avec jeu en appui si l'adversaire monte bien défensivement",
        "contre_mesures": "Bloc défensif compact, bien défendre les deuxièmes balles",
    },
    "counter_attacking": {
        "categorie": "Principe offensif",
        "objectif": "Exploiter les espaces laissés par un adversaire offensif pour attaquer en transition",
        "structure": "Bloc bas + transition rapide après récupération, vitesse maximale, 2-3 joueurs à l'avant",
        "declencheurs": "Adversaire qui monte beaucoup, récupération basse, attaquants de vitesse",
        "avantages": "Très efficace contre les équipes dominantes, crée des chances faciles",
        "limites": "Requiert des joueurs très rapides, les transitions échouent souvent sans vitesse",
        "reconnaitre": "Bloc bas, puis explosion rapide après récupération, peu de joueurs en transition",
        "adaptations": "Transition contrôlée si adversaire bien organisé en défense",
        "contre_mesures": "Rest defense, dernier défenseur toujours, ne pas monter à plus de 3-4 joueurs",
    },
    "rest_defense": {
        "categorie": "Principe offensif",
        "objectif": "Maintenir des joueurs positionnés pour contrer les transitions adverses",
        "structure": "1-2 joueurs qui restent positionnés pendant les phases offensives, souvent le MDC et un DC",
        "declencheurs": "Adversaire avec des joueurs de contre-attaque rapides",
        "avantages": "Neutralise les transitions rapides adverses, équilibre offensif-défensif",
        "limites": "Réduit le nombre de joueurs offensifs, peut limiter la finalisation",
        "reconnaitre": "1-2 joueurs qui ne montent pas pendant les phases offensives",
        "adaptations": "Identifier quelle vitesse adverse nécessite un rest defense renforcé",
        "contre_mesures": "Surcharger offensivement pour forcer les joueurs de rest defense à monter",
    },
    # ── PRINCIPES DÉFENSIFS ───────────────────────────────────────────────────
    "high_press": {
        "categorie": "Principe défensif",
        "objectif": "Récupérer la balle dans le camp adverse via une pression collective intense",
        "structure": "Ligne défensive haute (45-50m), pressing coordonné dès la perte de balle, 4-5 joueurs qui pressent",
        "declencheurs": "Signal (passe arrière adverse, gardien avec balle, DC sous pression)",
        "avantages": "Récupération haute = chances directes, déstabilise les équipes peu techniques",
        "limites": "Physiquement très exigeant, vulnérable aux longs dégagements précis",
        "reconnaitre": "Ligne défensive haute, attaquants qui pressent les DC adverses, agitation constante",
        "adaptations": "Press triggers clairs, pressing organisé par zones, couper les lignes de passe",
        "contre_mesures": "Long ball au-dessus du press, appuis courts derrière le press, gardien à pied sûr",
    },
    "mid_block": {
        "categorie": "Principe défensif",
        "objectif": "Défendre dans son propre camp à hauteur du milieu de terrain",
        "structure": "Bloc défensif compact à 35-40m du propre but, 2 lignes de 4 ou 5-4-1",
        "declencheurs": "Équipe qui ne presse pas mais ne s'écrase pas non plus",
        "avantages": "Équilibre risque/récompense, difficile à jouer contre, transitions possibles",
        "limites": "Laisse l'adversaire construire librement devant le bloc",
        "reconnaitre": "Deux lignes compactes au milieu, aucun joueur isolé devant",
        "adaptations": "Pressing ponctuel au signal, pas de pressing systématique",
        "contre_mesures": "Patience, jeu entre les lignes, tirs de loin pour ouvrir le bloc",
    },
    "low_block": {
        "categorie": "Principe défensif",
        "objectif": "Protéger le but en défendant très bas avec toute l'équipe",
        "structure": "Deux lignes de 4 à 25-30m du but, compacité maximale, aucun espace vertical",
        "declencheurs": "Protéger un avantage au score, adversaire très supérieur",
        "avantages": "Très difficile à percer, neutralise la possession adverse",
        "limites": "Passif, ne peut pas attaquer, épuisant mentalement et physiquement sur la durée",
        "reconnaitre": "Tous les joueurs derrière la ligne du ballon, bloc très bas",
        "adaptations": "Sorties rapides si ballon récupéré, transitions directes",
        "contre_mesures": "Circulation rapide, tirs de loin, centres sur le second poteau, corners",
    },
    "man_oriented_press": {
        "categorie": "Principe défensif",
        "objectif": "Presser chaque adversaire individuellement avec un marquage direct",
        "structure": "Chaque joueur assigné à un adversaire précis, pression individuelle coordonnée",
        "declencheurs": "Adversaire avec des joueurs techniques qui dictent le jeu",
        "avantages": "Aucun joueur adverse n'est libre, pression permanente",
        "limites": "Épuisant, laisse des espaces si un marquage rate",
        "reconnaitre": "Défenseurs qui suivent leur adversaire partout, peu de compacité par zones",
        "adaptations": "Trap sur le porteur, aide immédiate si marquage raté",
        "contre_mesures": "Mouvements sans ballon, permutations rapides pour créer des 2c1",
    },
    "zonal_pressing": {
        "categorie": "Principe défensif",
        "objectif": "Presser par zones avec des triggers déclencheurs collectifs",
        "structure": "Joueurs assignés à des zones sur le terrain, pressing déclenché quand la balle entre dans la zone",
        "declencheurs": "Balle dans la zone trigger, passe arrière adverse, indécision du porteur",
        "avantages": "Plus économique physiquement, organisation collective claire",
        "limites": "Requiert une lecture collective des triggers, peut rater si triggers mal définis",
        "reconnaitre": "Equipe qui presse uniquement sur certains déclencheurs, puis se replace",
        "adaptations": "Triggers clairs et entraînés : passe arrière, ballon aérien, joueur dos au jeu",
        "contre_mesures": "Jouer vite avant le trigger, changer le côté avant que le pressing se déclenche",
    },
    "trigger_pressing": {
        "categorie": "Principe défensif",
        "objectif": "Déclencher le pressing collectif sur un signal précis et entraîné",
        "structure": "Signal = trigger (passe arrière, DC qui reçoit, GK avec balle), 2-3 joueurs convergent immédiatement",
        "declencheurs": "Voir les exemples de triggers : pass-back, long ball latéral, joueur sous pression",
        "avantages": "Surprise pour l'adversaire, coordonné et difficile à éviter, efficace physiquement",
        "limites": "Si le trigger est raté, l'équipe est déséquilibrée pendant 2-3 secondes",
        "reconnaitre": "Déclenchement brutal et synchronisé du pressing après un événement précis",
        "adaptations": "3-4 triggers maximum, entraînés intensivement",
        "contre_mesures": "Identifier le trigger adverse et le provoquer de façon contrôlée",
    },
    "counter_press": {
        "categorie": "Principe défensif",
        "objectif": "Récupérer la balle immédiatement après une perte dans les 3-5 secondes",
        "structure": "Dès la perte : 2-3 joueurs proches pressent immédiatement, les autres se replacent",
        "declencheurs": "Perte de balle",
        "avantages": "Récupération haute, adversaire pas encore organisé, position offensive maintenue",
        "limites": "Si le counter-press échoue après 5 secondes, il faut renoncer et défendre en bloc",
        "reconnaitre": "Pressing immédiat et collectif à la perte, 3 secondes de chaos contrôlé",
        "adaptations": "Durée maximale du counter-press : 5 secondes puis repli",
        "contre_mesures": "Passe immédiate après la récupération pour sortir du counter-press",
    },
    "compactness": {
        "categorie": "Principe défensif",
        "objectif": "Réduire les espaces entre les lignes pour rendre la progression adverse impossible",
        "structure": "Distance inter-lignes : 10-15m maximum. Largeur : ne pas s'étirer. Bloc compact.",
        "declencheurs": "Permanente en phase défensive organisée",
        "avantages": "Aucun espace entre les lignes, difficile de jouer verticalement",
        "limites": "Peut être contourné par le jeu large (ailiers très larges), tirs de loin",
        "reconnaitre": "Équipe très resserrée, peu d'espace entre les lignes et entre les joueurs",
        "adaptations": "Sortir rapidement sur le porteur dès que la balle est dans la zone",
        "contre_mesures": "Jeu large pour étirer, switches de côté, tirs de loin",
    },
    "trap_zones": {
        "categorie": "Principe défensif",
        "objectif": "Forcer l'adversaire vers une zone piège où plusieurs défenseurs convergent",
        "structure": "Orienter la pression vers un coin ou un flanc, 2-3 défenseurs qui convergent",
        "declencheurs": "Balle dans la zone trap (coins, flancs, dos au jeu)",
        "avantages": "Force l'erreur de l'adversaire dans une zone peu dangereuse",
        "limites": "Les autres zones sont exposées pendant le trap, risque si la sortie est propre",
        "reconnaitre": "Défenseurs qui semblent laisser délibérément un espace pour attirer là",
        "adaptations": "Trap corner, trap flanc, trap milieu après pass-back",
        "contre_mesures": "Anticiper le trap, passer avant d'y rentrer, jouer en 2 touches",
    },
    # ── PATTERNS OFFENSIFS ────────────────────────────────────────────────────
    "overlaps": {
        "categorie": "Pattern offensif",
        "objectif": "Créer un 2c1 sur le côté via une montée du latéral derrière l'ailier",
        "structure": "Ailier garde la balle sur le côté, latéral monte en couloir extérieur derrière lui, 2c1 créé",
        "declencheurs": "Latéral qui monte dès que l'ailier a la balle et attire le défenseur",
        "avantages": "Crée un 2c1 difficile à défendre, libère l'ailier pour rentrer",
        "limites": "Latéral exposé en transition si le ballon est perdu",
        "reconnaitre": "Latéral qui monte en couloir extérieur pendant que l'ailier a la balle",
        "adaptations": "Ailier rentre en demi-espace, latéral croise derrière en overlapping run",
        "contre_mesures": "Latéral adverse qui monte pour contrer, défenseur double côté",
    },
    "underlaps": {
        "categorie": "Pattern offensif",
        "objectif": "Créer un 2c1 dans le demi-espace via une montée intérieure du latéral",
        "structure": "Ailier large, latéral coupe à l'intérieur (demi-espace), passe intérieure vers le latéral",
        "declencheurs": "Ailier qui occupe le latéral adverse à l'extérieur",
        "avantages": "Crée un angle de finition favorable, difficile à défendre si latéral arrive en demi-espace",
        "limites": "Requiert un ailier capable de garder la balle large pendant que le latéral coupe",
        "reconnaitre": "Latéral qui rentre à l'intérieur pendant que l'ailier est large",
        "adaptations": "Combinaison avec pistons inverser pour créer overload intérieur",
        "contre_mesures": "DC qui doit couvrir le demi-espace latéral",
    },
    "inverted_fullbacks": {
        "categorie": "Pattern offensif",
        "objectif": "Utiliser les latéraux inversés pour créer une supériorité numérique au centre",
        "structure": "Latéraux qui rentrent au milieu de terrain au lieu de monter côté, créant un triangle avec le MDC",
        "declencheurs": "Phase de construction, latéraux techniques capables de jouer au milieu",
        "avantages": "Surnombre central, libère les demi-espaces pour les ailiers qui rentrent",
        "limites": "Côtés sans couverture, vulnérable aux transitions latérales",
        "reconnaitre": "Latéraux qui se positionnent entre DC et MDC au lieu de monter côté",
        "adaptations": "Ailiers très larges pour compenser, MDC qui sort côté si nécessaire",
        "contre_mesures": "Ailiers adverses qui restent côtés pour contrer le déséquilibre",
    },
    "third_man_runs": {
        "categorie": "Pattern offensif",
        "objectif": "Libérer un coureur en troisième homme non-marqué via une combinaison à deux",
        "structure": "A passe à B, C fait une course de troisième homme vers la profondeur pendant l'échange A-B",
        "declencheurs": "Défense qui suit la balle, C qui s'échappe pendant que la défense regarde l'échange",
        "avantages": "Le troisième homme arrive en vitesse et est souvent seul, très difficile à anticiper",
        "limites": "Timing parfait requis de C, passe de B doit être précise et au bon moment",
        "reconnaitre": "Joueur qui sprinte en profondeur pendant que deux partenaires s'échangent la balle",
        "adaptations": "Courses de troisième homme sur les côtés, dans le dos des DC",
        "contre_mesures": "Défense qui continue à surveiller les courses même pendant l'échange",
    },
    "switch_play": {
        "categorie": "Pattern offensif",
        "objectif": "Changer rapidement le côté d'attaque pour trouver un espace libre",
        "structure": "Passe longue ou séquence de 3-4 passes rapides pour inverser le jeu côté opposé",
        "declencheurs": "Surcharge défensive côté fort, espace libre côté faible identifié",
        "avantages": "Défense qui ne se replace pas assez vite = espace libre côté faible",
        "limites": "Passe longue peut être interceptée, adversaire peut anticiper",
        "reconnaitre": "Long pass diagonale ou séquence de passes rapides de gauche à droite ou inversement",
        "adaptations": "Switch par le bas (gardien) ou par le haut (MDC pivot), ou diagonal direct",
        "contre_mesures": "Compacité défensive, rotation collective rapide sur le switch",
    },
    "diagonal_switches": {
        "categorie": "Pattern offensif",
        "objectif": "Changer de côté via une passe diagonale longue qui surprend la défense",
        "structure": "Passe diagonale d'un demi-espace vers l'autre, cible qui reçoit en courant vers la balle",
        "declencheurs": "Défense concentrée côté fort, espace derrière le latéral adverse côté faible",
        "avantages": "Très rapide, difficile à défendre, crée un 1c1 immédiat côté faible",
        "limites": "Requiert un pied droit/gauche et une précision technique élevée",
        "reconnaitre": "Passes longues diagonales depuis le milieu ou les demi-espaces",
        "adaptations": "Combiner avec troisième homme sur la réception",
        "contre_mesures": "Défenseur qui anticipe la diagonale et marque la cible côté faible",
    },
    "cross_strategies": {
        "categorie": "Pattern offensif",
        "objectif": "Créer des occasions via des centres dans la surface",
        "structure": "Plusieurs types : early cross (avant ligne de fond), cutback (retour rasant), centre pied levé (aérien), zone de centre",
        "declencheurs": "Ailier ou latéral en position de centre, attaquants dans la surface",
        "avantages": "Efficace si bonnes cibles dans la surface, crée du chaos défensif",
        "limites": "Dépend des qualités aériennes ou de timing des attaquants",
        "reconnaitre": "Montée du latéral/ailier sur le côté, courses des attaquants en surface",
        "adaptations": "Early cross (avant que la défense soit en place), cutback pour les arrivées tardives",
        "contre_mesures": "Défense sur les centres : zonal ou man-to-man selon équipe",
    },
    "cutbacks": {
        "categorie": "Pattern offensif",
        "objectif": "Créer un tir ouvert depuis le centre de la surface via un retour rasant",
        "structure": "Ailier ou latéral arrive au fond, au lieu de centrer, fait un retour en retrait vers le cercle",
        "declencheurs": "Ailier qui gagne le duel sur le côté, défense qui monte pour couvrir le centre direct",
        "avantages": "Tirs depuis le point de penalty avec balle au pied, défense souvent dépassée",
        "limites": "Requiert une arrivée tardive d'un milieu ou second attaquant",
        "reconnaitre": "Ailier qui arrive au fond et fait retour en retrait au lieu de centrer",
        "adaptations": "Combiner avec course du MDC ou deuxième attaquant",
        "contre_mesures": "Défenseur qui couvre le retrait, ne pas monter tous en premier poteau",
    },
    "box_occupation": {
        "categorie": "Pattern offensif",
        "objectif": "Occuper intelligemment la surface pour maximiser les chances de finition",
        "structure": "5 zones : premier poteau, second poteau, point de penalty, retrait court, fond de surface. Attaquants se répartissent",
        "declencheurs": "Présence de la balle côté ou en zone de centre",
        "avantages": "Maximise les surfaces de réception, défense difficile à organiser sur 5 zones",
        "limites": "Requiert des attaquants conscients de leur positionnement et de leurs zones",
        "reconnaitre": "Attaquants qui courent vers des zones distinctes lors d'un centre",
        "adaptations": "Selon le type de centreur : aérien = 1er et 2nd poteau. Ras du sol = retrait et point de penalty",
        "contre_mesures": "Défense zonale en surface organisée avec recrutement de zones",
    },
    "channel_runs": {
        "categorie": "Pattern offensif",
        "objectif": "Créer des espaces en faisant courir des attaquants dans les couloirs entre DC et latéral",
        "structure": "Attaquant court dans l'espace entre le DC et le latéral adverse (channel), passe en profondeur",
        "declencheurs": "Latéral adverse monté haut, DC qui penche vers l'intérieur",
        "avantages": "Espace souvent libre derrière les équipes qui défendent haut",
        "limites": "Hors-jeu fréquent, requiert timing parfait",
        "reconnaitre": "Attaquant qui court entre DC et latéral adverse",
        "adaptations": "Combiner avec ailier large qui attire le latéral, puis channel run derrière",
        "contre_mesures": "DC qui couvre l'espace channel, latéral qui ne monte pas trop",
    },
    # ── TRANSITIONS ───────────────────────────────────────────────────────────
    "immediate_counter": {
        "categorie": "Transition",
        "objectif": "Attaquer immédiatement après récupération avant que l'adversaire soit replacé",
        "structure": "Récupération → passe directe en profondeur → 2-3 joueurs en transition rapide",
        "declencheurs": "Récupération dans le camp adverse ou au milieu, adversaire déséquilibré",
        "avantages": "Chances faciles, défense adverse non-replacée, avantage numérique",
        "limites": "Risque de perte si trop précipité, requiert des joueurs très rapides",
        "reconnaitre": "Transition explosive dès la récupération, peu de passes, verticalité immédiate",
        "adaptations": "Choisir entre passer immédiatement ou garder si aucune option directe n'existe",
        "contre_mesures": "Rest defense permanente, tactical foul si nécessaire",
    },
    "controlled_transition": {
        "categorie": "Transition",
        "objectif": "Attaquer en transition avec contrôle et certitude plutôt que vitesse brute",
        "structure": "Récupération → 2-3 passes pour remonter proprement → attaque organisée mais rapide",
        "declencheurs": "Adversaire bien organisé en transition, pas de supériorité numérique immédiate",
        "avantages": "Moins de risques de perdre la balle, attaque plus structurée",
        "limites": "Laisse le temps à l'adversaire de se replacer",
        "reconnaitre": "Transition plus posée, quelques passes rapides avant l'attaque",
        "adaptations": "Combiner avec transition immédiate si supériorité numérique évidente",
        "contre_mesures": "Pressing intense dès la récupération adverse pour perturber",
    },
    "defensive_recovery": {
        "categorie": "Transition",
        "objectif": "Reprendre une organisation défensive solide après une perte de balle",
        "structure": "Sprints immédiats de tous les joueurs, formation défensive reconstituée en 3-4 secondes",
        "declencheurs": "Perte de balle partout sur le terrain",
        "avantages": "Neutralise les contre-attaques adverses, maintient la solidité défensive",
        "limites": "Très épuisant physiquement, surtout en fin de match",
        "reconnaitre": "Sprints de retour collectifs immédiats, formation qui se reconstitue",
        "adaptations": "Counter-press 3-5 secondes puis repli si échec",
        "contre_mesures": "Attaquer vite avant que la récupération soit complète",
    },
    "tactical_foul": {
        "categorie": "Transition",
        "objectif": "Casser la dynamique d'une transition adverse par une faute stratégique",
        "structure": "Joueur le plus proche de l'adversaire en transition réalise une faute préventive",
        "declencheurs": "Contre-attaque adverse avec surnombre, aucune option défensive propre",
        "avantages": "Casse le contre, récupère le temps de replacer l'équipe",
        "limites": "Risque de carton jaune ou rouge selon position et situation",
        "reconnaitre": "Faute 'calculée' au milieu de terrain pour stopper la transition",
        "adaptations": "MDC ou attaquant qui revient pour commettre la faute si nécessaire",
        "contre_mesures": "Jouer vite avant que l'adversaire puisse commettre la faute",
    },
    # ── COUPS DE PIED ARRÊTÉS ─────────────────────────────────────────────────
    "corner_offensif": {
        "categorie": "Coup de pied arrêté",
        "objectif": "Créer un but ou une occasion dangereuse depuis un corner",
        "structure": "Types : inswinger (rentrant), outswinger (sortant), corner court, zone de délivrance (1er poteau, 2nd poteau, point de penalty)",
        "declencheurs": "Corner obtenu",
        "avantages": "Occasion directe de but, organisation planifiée",
        "limites": "Défense bien organisée peut neutraliser si corners trop prévisibles",
        "reconnaitre": "Formation avant le corner : bloc, coureurs, flick-on au 1er poteau",
        "adaptations": "Varier les zones de délivrance, corner court pour déséquilibrer, blocker movements",
        "contre_mesures": "Défense zonale ou homme à homme sur les corners",
    },
    "corner_defensif": {
        "categorie": "Coup de pied arrêté",
        "objectif": "Défendre les corners sans concéder de but",
        "structure": "Types : zonal (défenseurs sur zones) ou man-to-man (marquage individuel). Souvent hybride au haut niveau",
        "declencheurs": "Corner adverse obtenu",
        "avantages": "Organisation claire, responsabilité définie",
        "limites": "Blockers adverses peuvent neutraliser les marqueurs, 2nd balle difficile à couvrir",
        "reconnaitre": "Positionnement des défenseurs : ligne de 6m ou ligne de zone",
        "adaptations": "Combiner zonal + marquage sur les meilleurs aériens adverses",
        "contre_mesures": "Corners inswinger/outswinger selon la défense adverse, blocker movements",
    },
    "free_kick_offensif": {
        "categorie": "Coup de pied arrêté",
        "objectif": "Marquer directement ou créer une occasion depuis un coup franc",
        "structure": "Types : direct (tir), indirect (combinaison), proche surface (mur), lointain (délivrance)",
        "declencheurs": "Coup franc obtenu dans la zone de danger",
        "avantages": "Occasion directe planifiée, défense figée",
        "limites": "Mur défensif bien organisé, gardien préparé",
        "reconnaitre": "Organisation des tireurs et des coureurs avant le coup franc",
        "adaptations": "Combinaisons sur coup franc indirect, 2ème tireur dans le mur",
        "contre_mesures": "Mur bien placé, gardien sur le premier poteau, couverture de zone",
    },
    "free_kick_defensif": {
        "categorie": "Coup de pied arrêté",
        "objectif": "Défendre un coup franc sans concéder",
        "structure": "Mur sur le premier poteau (nombre selon position), défenseurs sur zones, gardien sur le second poteau",
        "declencheurs": "Coup franc adverse dans la zone de danger",
        "avantages": "Organisation préventive, responsabilités claires",
        "limites": "Combinaisons indirectes peuvent contourner le mur",
        "reconnaitre": "Construction du mur, positionnement des défenseurs",
        "adaptations": "Joueur qui saute dans le mur à l'impact, anticipation de la zone de délivrance",
        "contre_mesures": "Surveiller les joueurs sans balle qui se déplacent pendant la prise du coup franc",
    },
    "throw_ins": {
        "categorie": "Coup de pied arrêté",
        "objectif": "Conserver la possession ou créer une occasion depuis une rentrée en touche",
        "structure": "Types : court (conserver), long (attaquer), rapide (surprendre)",
        "declencheurs": "Ballon sorti en touche",
        "avantages": "Rapide = défense non-organisée. Long = occasion directe sur flanc",
        "limites": "Perte de balle si déblayage mal anticipé",
        "reconnaitre": "Lanceur qui regarde les options avant de lancer, coureurs positionnés",
        "adaptations": "Routine de touche préparée dans les zones dangereuses",
        "contre_mesures": "Pression sur le lanceur, marquage serré des receveurs potentiels",
    },
}

# ── Effectifs réels par équipe (11 joueurs football, 5 basket, 9 rugby) ───────
TEAM_SQUADS: dict[str, list] = {
    # ── Ligue 1 2025-26 ───────────────────────────────────────────────────────
    "Paris Saint-Germain": [
        ["Chevalier","GB"],["Hakimi","RD"],["Marquinhos","DC"],
        ["Pacho","DC"],["Nuno Mendes","LD"],
        ["João Neves","MC"],["Vitinha","MC"],["Fabián Ruiz","MC"],
        ["Doué","AD"],["Dembélé","BU"],["Kvaratskhelia","AG"],
    ],
    "AS Monaco": [
        ["Hrádecký","GB"],["Vanderson","RD"],["Dier","DC"],
        ["Salisu","DC"],["Caio Henrique","LD"],
        ["Zakaria","MDC"],["Lamine Camara","MC"],
        ["Akliouche","MO"],["Golovin","MO"],["Minamino","AG"],["Balogun","BU"],
    ],
    "Olympique de Marseille": [
        ["Rulli","GB"],["Weah","RD"],["Balerdi","DC"],
        ["Aguerd","DC"],["Emerson","LD"],
        ["Højbjerg","MDC"],["O'Riley","MC"],["Angel Gomes","MC"],
        ["Greenwood","AD"],["Aubameyang","BU"],["Paixão","AG"],
    ],
    "Olympique Lyonnais": [
        ["Greif","GB"],["Maitland-Niles","RD"],["Niakhaté","DC"],
        ["Mata","DC"],["Tagliafico","LD"],
        ["Tessmann","MDC"],["Tolisso","MC"],["Morton","MC"],
        ["Fofana","AD"],["Satriano","BU"],["Karabec","AG"],
    ],
    "LOSC Lille": [
        ["Özer","GB"],["Meunier","RD"],["Diakité","DC"],
        ["Mbemba","DC"],["Gudmundsson","LD"],
        ["André","MDC"],["Bouaddi","MC"],
        ["Haraldsson","MO"],["Sahraoui","AD"],["Giroud","BU"],["Fernandez-Pardo","AG"],
    ],
    "OGC Nice": [
        ["Diouf","GB"],["Clauss","RD"],["Dante","DC"],
        ["Bombito","DC"],["Bard","LD"],
        ["Vanhoutte","MDC"],["Sanson","MC"],
        ["Boudaoui","MO"],["Cho","AD"],["Moffi","BU"],["Diop","AG"],
    ],
    "RC Lens": [
        ["Risser","GB"],["Aguilar","RD"],["Gradit","DC"],
        ["Sarr","DC"],["Machado","LD"],
        ["Abdul Samed","MDC"],["Thomasson","MC"],
        ["Fulgini","MO"],["Sotoca","AD"],["Edouard","BU"],["Saïd","AG"],
    ],
    "Toulouse FC": [
        ["Restes","GB"],["Sidibé","RD"],["Nicolaisen","DC"],
        ["McKenzie","DC"],["Suazo","LD"],
        ["Casseres","MDC"],["Sierro","MC"],
        ["Aboukhlal","AD"],["Gboho","MO"],["Emersonn","BU"],["Magri","AG"],
    ],
    "Stade Brestois 29": [
        ["Bizot","GB"],["Lala","RD"],["Chardonnet","DC"],
        ["Coulibaly","DC"],["Locko","LD"],
        ["Magnetti","MDC"],["Camara","MC"],
        ["Del Castillo","MO"],["Le Douaron","AD"],["Ajorque","BU"],["Sima","AG"],
    ],
    "Stade Rennais": [
        ["Samba","GB"],["Seidu","RD"],["Rouault","DC"],
        ["Wooh","DC"],["Truffert","LD"],
        ["Fofana","MDC"],["Camara","MC"],
        ["Blas","MO"],["Bourigeaud","AD"],["Embolo","BU"],["Kalimuendo","AG"],
    ],
    "FC Lorient": [
        ["Mvogo","GB"],["Kari","RD"],["Talbi","DC"],
        ["Mendy","DC"],["Avom","LD"],
        ["Abergel","MDC"],["Makengo","MC"],
        ["Le Bris","MO"],["Bamba","AD"],["Pagis","BU"],["Soumano","AG"],
    ],
    "Paris FC": [
        ["Trapp","GB"],["Sangaré","RD"],["Hanin","DC"],
        ["Otavio","DC"],["Mbow","LD"],
        ["Lees-Melou","MDC"],["Maxime Lopez","MC"],
        ["Kebbal","MO"],["Simon","AD"],["Krasso","BU"],["Geubbels","AG"],
    ],
    "FC Metz": [
        ["Fischer","GB"],["Kouao","RD"],["Sané","DC"],
        ["Colin","DC"],["Gbamin","LD"],
        ["Stambouli","MDC"],["Deminguet","MC"],
        ["Hein","MO"],["Sabaly","AD"],["Diallo","BU"],["Gueye","AG"],
    ],
    # ── Premier League 2025-26 ────────────────────────────────────────────────
    "Arsenal FC": [
        ["Raya","GB"],["Timber","RD"],["Saliba","DC"],
        ["Gabriel","DC"],["Calafiori","LD"],
        ["Zubimendi","MDC"],["Rice","MC"],["Ødegaard","MC"],
        ["Saka","AD"],["Gyökeres","BU"],["Martinelli","AG"],
    ],
    "Manchester City": [
        ["Donnarumma","GB"],["Khusanov","RD"],["Dias","DC"],
        ["Gvardiol","DC"],["Aït-Nouri","LD"],
        ["Rodri","MDC"],["Reijnders","MC"],["Bernardo Silva","MC"],
        ["Savinho","AD"],["Haaland","BU"],["Doku","AG"],
    ],
    "Liverpool FC": [
        ["Alisson","GB"],["Frimpong","RD"],["Konaté","DC"],
        ["Van Dijk","DC"],["Kerkez","LD"],
        ["Gravenberch","MDC"],["Mac Allister","MC"],
        ["Wirtz","MO"],["Salah","AD"],["Isak","BU"],["Gakpo","AG"],
    ],
    "Chelsea FC": [
        ["Sánchez","GB"],["Gusto","RD"],["Fofana","DC"],
        ["Chalobah","DC"],["Cucurella","LD"],
        ["Caicedo","MDC"],["Fernández","MC"],
        ["Palmer","MO"],["Pedro Neto","AD"],["João Pedro","BU"],["Estêvão","AG"],
    ],
    "Tottenham Hotspur": [
        ["Vicario","GB"],["Porro","RD"],["Romero","DC"],
        ["Van de Ven","DC"],["Spence","LD"],
        ["Palhinha","MDC"],["Bentancur","MC"],
        ["Xavi Simons","MO"],["Kudus","AD"],["Solanke","BU"],["Johnson","AG"],
    ],
    "Manchester United": [
        ["Lammens","GB"],["Yoro","DC"],["Maguire","DC"],
        ["Shaw","DC"],["Dalot","DD"],
        ["Casemiro","MDC"],["Bruno Fernandes","MC"],["Dorgu","DG"],
        ["Mbeumo","MO"],["Cunha","MO"],["Šeško","BU"],
    ],
    "Newcastle United": [
        ["Pope","GB"],["Trippier","RD"],["Schär","DC"],
        ["Burn","DC"],["Hall","LD"],
        ["Tonali","MDC"],["Guimarães","MC"],["Joelinton","MC"],
        ["Elanga","AD"],["Woltemade","BU"],["Gordon","AG"],
    ],
    "Aston Villa": [
        ["Martínez","GB"],["Cash","RD"],["Konsa","DC"],
        ["Torres","DC"],["Digne","LD"],
        ["Onana","MDC"],["Tielemans","MC"],["McGinn","MC"],
        ["Rogers","MO"],["Watkins","BU"],["Guessand","AG"],
    ],
    "Brighton & Hove Albion": [
        ["Verbruggen","GB"],["Veltman","RD"],["Dunk","DC"],
        ["Van Hecke","DC"],["De Cuyper","LD"],
        ["Baleba","MDC"],["Hinshelwood","MC"],
        ["Minteh","AD"],["Welbeck","BU"],["Mitoma","AG"],["Rutter","MO"],
    ],
    "West Ham United": [
        ["Areola","GB"],["Wan-Bissaka","RD"],["Todibo","DC"],
        ["Kilman","DC"],["Diouf","LD"],
        ["Soucek","MDC"],["Fernandes","MC"],
        ["Paquetá","MO"],["Bowen","AD"],["Füllkrug","BU"],["Summerville","AG"],
    ],
    # ── Champions League / top clubs 2025-26 ──────────────────────────────────
    "Real Madrid CF": [
        ["Courtois","GB"],["Alexander-Arnold","RD"],["Militão","DC"],
        ["Huijsen","DC"],["Carreras","LD"],
        ["Tchouaméni","MDC"],["Valverde","MC"],["Bellingham","MC"],
        ["Güler","MO"],["Mbappé","BU"],["Vinicius","AG"],
    ],
    "Bayern Munich": [
        ["Neuer","GB"],["Laimer","RD"],["Upamecano","DC"],
        ["Tah","DC"],["Davies","LD"],
        ["Kimmich","MDC"],["Goretzka","MC"],
        ["Olise","AD"],["Gnabry","MO"],["Luis Díaz","AG"],["Kane","BU"],
    ],
    "FC Barcelona": [
        ["Joan García","GB"],["Koundé","RD"],["Cubarsí","DC"],
        ["Araujo","DC"],["Balde","LD"],
        ["De Jong","MDC"],["Pedri","MC"],["Olmo","MO"],
        ["Yamal","AD"],["Lewandowski","BU"],["Raphinha","AG"],
    ],
    "Inter Milan": [
        ["Sommer","GB"],["Pavard","DC"],["Acerbi","DC"],
        ["Bastoni","DC"],["Dumfries","DD"],
        ["Barella","MC"],["Çalhanoğlu","MDC"],["Sučić","MC"],["Dimarco","DG"],
        ["Lautaro","BU"],["Thuram","BU"],
    ],
    "Atlético de Madrid": [
        ["Oblak","GB"],["Llorente","RD"],["Le Normand","DC"],
        ["Lenglet","DC"],["Hancko","LD"],
        ["Barrios","MDC"],["Gallagher","MC"],["Baena","MO"],
        ["Griezmann","AD"],["Julián Álvarez","BU"],["Sørloth","AG"],
    ],
    "Borussia Dortmund": [
        ["Kobel","GB"],["Ryerson","RD"],["Anton","DC"],
        ["Schlotterbeck","DC"],["Svensson","LD"],
        ["Nmecha","MDC"],["Sabitzer","MC"],
        ["Brandt","MO"],["Adeyemi","AD"],["Guirassy","BU"],["Beier","AG"],
    ],
    "Juventus FC": [
        ["Di Gregorio","GB"],["Kalulu","RD"],["Gatti","DC"],
        ["Bremer","DC"],["Cambiaso","LD"],
        ["Locatelli","MDC"],["Thuram","MC"],
        ["Yildiz","MO"],["Conceição","AD"],["David","BU"],["Zhegrova","AG"],
    ],
    "FC Porto": [
        ["Diogo Costa","GB"],["João Mário","RD"],["Pérez","DC"],
        ["Otávio","DC"],["Moura","LD"],
        ["Eustáquio","MDC"],["Varela","MC"],
        ["Pepê","AD"],["Samu","BU"],["Gül","AG"],["Mora","MO"],
    ],
    # ── Super League Suisse (conservé) ────────────────────────────────────────
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
    # ── NBA 2025-26 (post-trade Luka↔AD fév. 2025 + mouvements été 2025) ───────
    "Atlanta Hawks":          [["Trae Young","PG"],["Dyson Daniels","SG"],["Zaccharie Risacher","SF"],["Jalen Johnson","PF"],["Kristaps Porzingis","C"]],
    "Boston Celtics":         [["Anfernee Simons","PG"],["Derrick White","SG"],["Jaylen Brown","SF"],["Jayson Tatum","PF"],["Neemias Queta","C"]],
    "Brooklyn Nets":          [["Egor Demin","PG"],["Cam Thomas","SG"],["Michael Porter Jr.","SF"],["Noah Clowney","PF"],["Nic Claxton","C"]],
    "Charlotte Hornets":      [["LaMelo Ball","PG"],["Brandon Miller","SG"],["Kon Knueppel","SF"],["Miles Bridges","PF"],["Moussa Diabaté","C"]],
    "Chicago Bulls":          [["Josh Giddey","PG"],["Coby White","SG"],["Matas Buzelis","SF"],["Patrick Williams","PF"],["Nikola Vucevic","C"]],
    "Cleveland Cavaliers":    [["Darius Garland","PG"],["Donovan Mitchell","SG"],["De'Andre Hunter","SF"],["Evan Mobley","PF"],["Jarrett Allen","C"]],
    "Dallas Mavericks":       [["D'Angelo Russell","PG"],["Klay Thompson","SG"],["Cooper Flagg","SF"],["Anthony Davis","PF"],["Dereck Lively II","C"]],
    "Denver Nuggets":         [["Jamal Murray","PG"],["Christian Braun","SG"],["Cameron Johnson","SF"],["Aaron Gordon","PF"],["Nikola Jokic","C"]],
    "Detroit Pistons":        [["Cade Cunningham","PG"],["Jaden Ivey","SG"],["Ausar Thompson","SF"],["Tobias Harris","PF"],["Jalen Duren","C"]],
    "Golden State Warriors":  [["Stephen Curry","PG"],["Brandin Podziemski","SG"],["Jimmy Butler","SF"],["Draymond Green","PF"],["Al Horford","C"]],
    "Houston Rockets":        [["Fred VanVleet","PG"],["Amen Thompson","SG"],["Kevin Durant","SF"],["Jabari Smith Jr.","PF"],["Alperen Sengun","C"]],
    "Indiana Pacers":         [["Andrew Nembhard","PG"],["Bennedict Mathurin","SG"],["Aaron Nesmith","SF"],["Pascal Siakam","PF"],["Isaiah Jackson","C"]],
    "LA Clippers":            [["James Harden","PG"],["Bradley Beal","SG"],["Kawhi Leonard","SF"],["John Collins","PF"],["Ivica Zubac","C"]],
    "Los Angeles Lakers":     [["Luka Doncic","PG"],["Austin Reaves","SG"],["LeBron James","SF"],["Rui Hachimura","PF"],["Deandre Ayton","C"]],
    "Memphis Grizzlies":      [["Ja Morant","PG"],["Jaylen Wells","SG"],["Santi Aldama","SF"],["Jaren Jackson Jr.","PF"],["Zach Edey","C"]],
    "Miami Heat":             [["Davion Mitchell","PG"],["Tyler Herro","SG"],["Norman Powell","SF"],["Andrew Wiggins","PF"],["Bam Adebayo","C"]],
    "Milwaukee Bucks":        [["Kevin Porter Jr.","PG"],["Gary Trent Jr.","SG"],["Kyle Kuzma","SF"],["Giannis Antetokounmpo","PF"],["Myles Turner","C"]],
    "Minnesota Timberwolves": [["Mike Conley","PG"],["Anthony Edwards","SG"],["Jaden McDaniels","SF"],["Julius Randle","PF"],["Rudy Gobert","C"]],
    "New Orleans Pelicans":   [["Jordan Poole","PG"],["Trey Murphy III","SG"],["Herbert Jones","SF"],["Zion Williamson","PF"],["Yves Missi","C"]],
    "New York Knicks":        [["Jalen Brunson","PG"],["Mikal Bridges","SG"],["OG Anunoby","SF"],["Josh Hart","PF"],["Karl-Anthony Towns","C"]],
    "Oklahoma City Thunder":  [["Shai Gilgeous-Alexander","PG"],["Luguentz Dort","SG"],["Jalen Williams","SF"],["Chet Holmgren","PF"],["Isaiah Hartenstein","C"]],
    "Orlando Magic":          [["Jalen Suggs","PG"],["Desmond Bane","SG"],["Franz Wagner","SF"],["Paolo Banchero","PF"],["Wendell Carter Jr.","C"]],
    "Philadelphia 76ers":     [["Tyrese Maxey","PG"],["VJ Edgecombe","SG"],["Paul George","SF"],["Quentin Grimes","PF"],["Joel Embiid","C"]],
    "Phoenix Suns":           [["Jalen Green","PG"],["Devin Booker","SG"],["Dillon Brooks","SF"],["Ryan Dunn","PF"],["Mark Williams","C"]],
    "Portland Trail Blazers": [["Jrue Holiday","PG"],["Shaedon Sharpe","SG"],["Deni Avdija","SF"],["Jerami Grant","PF"],["Donovan Clingan","C"]],
    "Sacramento Kings":       [["Dennis Schröder","PG"],["Zach LaVine","SG"],["DeMar DeRozan","SF"],["Keegan Murray","PF"],["Domantas Sabonis","C"]],
    "San Antonio Spurs":      [["De'Aaron Fox","PG"],["Stephon Castle","SG"],["Devin Vassell","SF"],["Harrison Barnes","PF"],["Victor Wembanyama","C"]],
    "Toronto Raptors":        [["Immanuel Quickley","PG"],["RJ Barrett","SG"],["Brandon Ingram","SF"],["Scottie Barnes","PF"],["Jakob Poeltl","C"]],
    "Utah Jazz":              [["Isaiah Collier","PG"],["Keyonte George","SG"],["Ace Bailey","SF"],["Lauri Markkanen","PF"],["Walker Kessler","C"]],
    "Washington Wizards":     [["CJ McCollum","PG"],["Bub Carrington","SG"],["Bilal Coulibaly","SF"],["Khris Middleton","PF"],["Alex Sarr","C"]],
    # ── Euroleague 2025-26 ────────────────────────────────────────────────────
    "Real Madrid Baloncesto": [
        ["Campazzo","PG"],["Llull","SG"],["Tavares","C"],
        ["Hezonja","SF"],["Deck","PF"],
    ],
    "FC Barcelona Bàsquet": [
        ["Satoransky","PG"],["Punter","SG"],["Vesely","C"],
        ["Parker","PF"],["Brizuela","SG"],
    ],
    "Fenerbahce Beko": [
        ["Baldwin","PG"],["Horton-Tucker","SG"],["Hayes-Davis","SF"],
        ["Colson","PF"],["Sanli","C"],
    ],
    "Olympiacos BC": [
        ["Walkup","PG"],["Vezenkov","SF"],["Fall","C"],
        ["Peters","PF"],["Larentzakis","SG"],
    ],
    "Bayern Munich Basketball": [
        ["Baldwin","PG"],["Obst","SG"],["Edwards","SF"],
        ["Giffey","PF"],["Da Silva","C"],
    ],
    "Maccabi Tel Aviv": [
        ["Baldwin","PG"],["Sorkin","C"],["Blayzer","SG"],
        ["Leaf","PF"],["DiBartolomeo","PG"],
    ],
    "Dubai BC":                 [["Tomas Satoransky","PG"],["Joe Wieskamp","SG"],["Alessandro Gentile","SF"],["Mouhammadou Jaiteh","PF"],["Dwayne Bacon","C"]],
    "Partizan Belgrade":        [["Kevin Punter","PG"],["Dante Exum","SG"],["Carlik Jones","SF"],["Sterling Brown","PF"],["Tyrique Jones","C"]],
    "Valence Basket":           [["Martin Hermannsson","PG"],["Darius Thompson","SG"],["Jean Montero","SF"],["Brancou Badio","PF"],["Yankuba Sima","C"]],
    "Panathinaikos":            [["Kendrick Nunn","PG"],["Cedi Osman","SG"],["Mathias Lessort","C"],["Juancho Hernangomez","PF"],["Kostas Sloukas","PG"]],
    "Anadolu Efes Istanbul":    [["Shane Larkin","PG"],["Rodrigue Beaubois","SG"],["P.J. Dozier","SF"],["Ercan Osmani","PF"],["Georgios Papagiannis","C"]],
    "EA7 Emporio Armani Milano":[["Lorenzo Brown","PG"],["Nico Mannion","SG"],["Shavon Shields","SF"],["Zach LeDay","PF"],["Josh Nebo","C"]],
    "Virtus Segafredo Bologna": [["Alessandro Pajola","PG"],["Carsen Edwards","SG"],["Saliou Niang","SF"],["Momo Diouf","PF"],["Will Clyburn","C"]],
    "Baskonia Vitoria-Gasteiz": [["Markus Howard","PG"],["Trent Forrest","SG"],["Tadas Sedekerskis","SF"],["Hamidou Diallo","PF"],["Khalifa Diop","C"]],
    "Crvena Zvezda Meridianbet Belgrade": [["Codi Miller-McIntyre","PG"],["Isaac Bonga","SG"],["Nikola Kalinić","SF"],["Joel Bolomboy","PF"],["Nikola Milutinov","C"]],
    # ── Betclic Elite 2025-26 ─────────────────────────────────────────────────
    "AS Monaco Basket":         [["Mike James","PG"],["Elie Okobo","SG"],["Alpha Diallo","SF"],["Nikola Mirotic","PF"],["Daniel Theis","C"]],
    "Paris Basketball":         [["Nadir Hifi","SG"],["T.J. Shorts","PG"],["Tyson Ward","SF"],["Maodo Lo","PG"],["Yakuba Ouattara","SF"]],
    "LDLC ASVEL":               [["Edwin Jackson","SG"],["Paris Lee","PG"],["David Lighty","SF"],["Mam Jaiteh","C"],["Nando De Colo","SG"]],
    "JL Bourg-en-Bresse":       [["Darius McGhee","PG"],["Adam Mokoka","SG"],["Both Gach","SF"],["Tre Mitchell","PF"],["J.T. Shumate","C"]],
    "Cholet Basket":            [["Ousmane Camara","PG"],["Hugo Robineau","SG"],["Paul Rigot","SF"],["Killian Tillie","PF"],["Yannis Morin","C"]],
    "Nanterre 92":              [["Milan Barbitch","PG"],["Frank Jackson","SG"],["Lucas Dussoulier","SF"],["Desi Rodriguez","PF"],["Justin Tillman","C"]],
    "Saint-Quentin Basket-Ball":[["Lucas Boucaud","PG"],["Jerome Robinson","SG"],["Noah Kirkwood","SF"],["Giovan Oniangue","PF"],["Dominik Olejniczak","C"]],
    "Le Mans Sarthe Basket":    [["Tray Buchanan","PG"],["Abdoulaye Ndoye","SG"],["David DiLeo","SF"],["Williams Narace","PF"],["Selom Mawugbe","C"]],
    "JDA Dijon":                [["David Holston","PG"],["Justin Bibbins","SG"],["Chris Babb","SF"],["Vafessa Fofana","PF"],["Rob Skoupak","C"]],
    "SIG Strasbourg":           [["Edon Maxhuni","PG"],["Dominic Artis","SG"],["Hugo Invernizzi","SF"],["Jeff Roberson","PF"],["Brice Dessert","C"]],
    "Limoges CSP":              [["Tyrell Terry","PG"],["Nicolas Lang","SG"],["Kenny Baptiste","SF"],["Malik Osborne","PF"],["Alexandre Chassang","C"]],
    "Élan Chalon":              [["Mathéo Leray","PG"],["Clarence Nadolny","SG"],["Jeremiah Hill","SF"],["Justyn Mutts","PF"],["Obinna Anochili-Killen","C"]],
    "ESSM Le Portel":           [["DeAndre Gholston","PG"],["Kristers Zoriks","SG"],["Ivan Février","SF"],["Jack Nunge","PF"],["Idrissa Ba","C"]],
    "BCM Gravelines-Dunkerque": [["Gauthier Denis","PG"],["Breein Tyree","SG"],["Trevon Bluiett","SF"],["Frank Bartley","PF"],["Brian Quarters","C"]],
    "SLUC Nancy Basket":        [["Marcus Thornton","PG"],["Axel Julien","SG"],["Jordan Davis","SF"],["Yannick Bokolo","PF"],["Gavin Ware","C"]],
    "Stade Rochelais Basket":   [["Sam Sessoms","PG"],["Gaetan Clerc","SG"],["Jérôme Sanchez","SF"],["Jubrile Belo","PF"],["Ryan Hawkins","C"]],
    "Boulazac Basket Dordogne": [["Angelo Warner","PG"],["Cyrille Eliezer-Vanerot","SG"],["Tony Snell","SF"],["Malik Fitts","PF"],["K.J. Williams","C"]],
    # ── Top 14 (conservé) ─────────────────────────────────────────────────────
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



# ── Classement Ligue 1 2025-26 ───────────────────────────────────────────────
LIGUE1_STANDINGS = [
    {"pos":1,  "team":"Paris Saint-Germain", "j":24, "v":18, "n":3,  "d":3,  "bp":53, "bc":19, "diff":34,  "pts":57, "zone":"ucl"},
    {"pos":2,  "team":"RC Lens",             "j":24, "v":17, "n":2,  "d":5,  "bp":45, "bc":21, "diff":24,  "pts":53, "zone":"ucl"},
    {"pos":3,  "team":"Olympique Lyonnais",  "j":23, "v":14, "n":3,  "d":6,  "bp":37, "bc":23, "diff":14,  "pts":45, "zone":"ucl"},
    {"pos":4,  "team":"Olympique de Marseille","j":23,"v":12,"n":4,  "d":7,  "bp":48, "bc":31, "diff":17,  "pts":40, "zone":"ucl"},
    {"pos":5,  "team":"LOSC Lille",          "j":24, "v":12, "n":4,  "d":8,  "bp":37, "bc":31, "diff":6,   "pts":40, "zone":"uel"},
    {"pos":6,  "team":"Stade Rennais",       "j":24, "v":11, "n":7,  "d":6,  "bp":38, "bc":35, "diff":3,   "pts":40, "zone":"uel"},
    {"pos":7,  "team":"AS Monaco",           "j":24, "v":11, "n":4,  "d":9,  "bp":40, "bc":36, "diff":4,   "pts":37, "zone":"uel"},
    {"pos":8,  "team":"RC Strasbourg",       "j":24, "v":10, "n":5,  "d":9,  "bp":40, "bc":31, "diff":9,   "pts":35, "zone":""},
    {"pos":9,  "team":"Stade Brestois",      "j":24, "v":9,  "n":6,  "d":9,  "bp":32, "bc":34, "diff":-2,  "pts":33, "zone":""},
    {"pos":10, "team":"FC Lorient",          "j":24, "v":8,  "n":9,  "d":7,  "bp":34, "bc":38, "diff":-4,  "pts":33, "zone":""},
    {"pos":11, "team":"Toulouse FC",         "j":24, "v":8,  "n":7,  "d":9,  "bp":33, "bc":28, "diff":5,   "pts":31, "zone":""},
    {"pos":12, "team":"Angers SCO",          "j":24, "v":8,  "n":5,  "d":11, "bp":22, "bc":30, "diff":-8,  "pts":29, "zone":""},
    {"pos":13, "team":"Le Havre AC",         "j":24, "v":6,  "n":8,  "d":10, "bp":20, "bc":30, "diff":-10, "pts":26, "zone":""},
    {"pos":14, "team":"Paris FC",            "j":24, "v":6,  "n":8,  "d":10, "bp":28, "bc":40, "diff":-12, "pts":26, "zone":""},
    {"pos":15, "team":"OGC Nice",            "j":24, "v":6,  "n":6,  "d":12, "bp":30, "bc":44, "diff":-14, "pts":24, "zone":""},
    {"pos":16, "team":"AJ Auxerre",          "j":24, "v":4,  "n":6,  "d":14, "bp":19, "bc":35, "diff":-16, "pts":18, "zone":"rel"},
    {"pos":17, "team":"FC Nantes",           "j":24, "v":4,  "n":5,  "d":15, "bp":22, "bc":41, "diff":-19, "pts":17, "zone":"rel"},
    {"pos":18, "team":"FC Metz",             "j":24, "v":3,  "n":4,  "d":17, "bp":22, "bc":53, "diff":-31, "pts":13, "zone":"rel"},
]


# ══════════════════════════════════════════════════════════════════════════════
# REACT UI — merged from streamlit_app.py
# All data from the Python dicts above is serialised to JSON and injected as
# window.APP_MATCHES so the React prototype runs with real match data.
# ══════════════════════════════════════════════════════════════════════════════

def _build_js_matches() -> str:
    """Convert Python MATCHES dict → window.MATCHES JS array for the React UI.

    Enriches each team entry with:
    - rank: position in LIGUE1_STANDINGS for Ligue 1 teams (None otherwise)
    - form: last 5 results as V/N/D from MATCHES history, sorted descending by date
    """
    sport_map  = {"⚽ Football": "football", "🏀 Basket": "basket", "🏉 Rugby": "rugby"}
    status_map = {"Terminé": "finished", "Live": "live", "À venir": "upcoming"}
    day_fr = ["Lun.", "Mar.", "Mer.", "Jeu.", "Ven.", "Sam.", "Dim."]
    mon_fr = ["Jan.", "Fév.", "Mar.", "Avr.", "Mai", "Juin",
              "Juil.", "Août", "Sep.", "Oct.", "Nov.", "Déc."]

    # Build rank lookup from LIGUE1_STANDINGS
    l1_rank: dict[str, int] = {row["team"]: row["pos"] for row in LIGUE1_STANDINGS}

    # Build form lookup: team_name → [last-5 results newest-first]
    # Only from finished matches where both scores are available
    finished = [
        (mid, m) for mid, m in MATCHES.items()
        if m.get("status") == "Terminé"
        and m["home"].get("score") is not None
        and m["away"].get("score") is not None
    ]
    # Sort finished matches by date descending
    def _sort_key(item):
        try:
            return datetime.strptime(item[1].get("date", ""), "%Y-%m-%d")
        except Exception:
            return datetime.min
    finished.sort(key=_sort_key, reverse=True)

    form_map: dict[str, list] = {}
    for _mid, _m in finished:
        hs = int(_m["home"]["score"])
        as_ = int(_m["away"]["score"])
        hn = _m["home"]["name"]
        an = _m["away"]["name"]
        for team, scored, conceded in [(hn, hs, as_), (an, as_, hs)]:
            if len(form_map.get(team, [])) < 5:
                if scored > conceded:
                    r = "V"
                elif scored == conceded:
                    r = "N"
                else:
                    r = "D"
                form_map.setdefault(team, []).append(r)
    # Reverse so oldest→newest (left to right display)
    for team in form_map:
        form_map[team] = list(reversed(form_map[team]))

    grouped: dict = {"football": [], "basket": [], "rugby": []}

    for mid, m in MATCHES.items():
        sport_key = sport_map.get(m.get("sport", ""), "football")
        status    = status_map.get(m.get("status", ""), "upcoming")
        h, a      = m["home"], m["away"]

        date_str = m.get("date", "")
        time_str = m.get("time", "")
        try:
            d        = datetime.strptime(date_str, "%Y-%m-%d")
            fmt_date = f"{day_fr[d.weekday()]} {d.day:02d} {mon_fr[d.month - 1]}"
            if time_str:
                fmt_date += f" · {time_str}"
        except Exception:
            fmt_date = date_str

        entry: dict = {
            "id":          mid,
            "status":      status,
            "date":        fmt_date,
            "competition": m.get("competition", ""),
            "venue":       m.get("stadium", ""),
            "home": {
                "code":  h.get("short", h["name"][:3].upper()),
                "name":  h["name"],
                "color": h.get("color", "#888"),
                "rank":  l1_rank.get(h["name"]),
                "form":  form_map.get(h["name"], []),
            },
            "away": {
                "code":  a.get("short", a["name"][:3].upper()),
                "name":  a["name"],
                "color": a.get("color", "#888"),
                "rank":  l1_rank.get(a["name"]),
                "form":  form_map.get(a["name"], []),
            },
        }

        if h.get("score") is not None and a.get("score") is not None:
            entry["score"] = {"home": h["score"], "away": a["score"]}

        # Deterministic predicted scoreline (used by the pre-match screen)
        prng = _rng_mod.Random(int(hashlib.md5(("P" + mid).encode()).hexdigest()[:8], 16))
        _sp = m.get("sport", "")
        if "Basket" in _sp:
            base = prng.randint(96, 114)
            entry["predicted"] = f"{base + prng.randint(-6, 9)} – {base + prng.randint(-9, 6)}"
        elif "Rugby" in _sp:
            entry["predicted"] = f"{prng.randint(16, 32)} – {prng.randint(12, 27)}"
        else:
            entry["predicted"] = f"{prng.randint(0, 3)} – {prng.randint(0, 2)}"

        grouped[sport_key].append(entry)

    return f"window.MATCHES = {json.dumps(grouped, ensure_ascii=False)};"


def _build_js_analyses() -> str:
    """Generate synthetic analyses for all finished matches → window.ANALYSES."""
    analyses: dict = {}
    for mid, m in MATCHES.items():
        if m.get("status") != "Terminé":
            continue
        if m["home"].get("score") is None or m["away"].get("score") is None:
            continue
        # Use pre-authored analysis if available, otherwise generate synthetic
        if mid in ANALYSIS:
            raw = ANALYSIS[mid]
        else:
            try:
                raw = generate_synthetic_analysis(mid, m)
            except Exception:
                continue
        # Serialise to a compact form for the React UI
        tac = raw.get("tactique", {})
        jou = raw.get("joueurs", {})
        verd = raw.get("verdict", {})
        analyses[mid] = {
            "tactique": {
                "home_form": tac.get("home_form", ""),
                "away_form": tac.get("away_form", ""),
            },
            "joueurs": {
                "home": [
                    {"nom": p["nom"], "poste": p["poste"],
                     "note": p["note"], "stats": p["stats"]}
                    for p in jou.get("home", [])
                ],
                "away": [
                    {"nom": p["nom"], "poste": p["poste"],
                     "note": p["note"], "stats": p["stats"]}
                    for p in jou.get("away", [])
                ],
            },
            "verdict": {
                "home_perf":  verd.get("home_perf"),
                "away_perf":  verd.get("away_perf"),
                "intensite":  verd.get("intensite"),
                "spectacle":  verd.get("spectacle"),
                "home_txt":   verd.get("home_txt", ""),
                "away_txt":   verd.get("away_txt", ""),
                "coach_home": verd.get("coach_home", ""),
                "coach_away": verd.get("coach_away", ""),
            },
        }
    return f"window.ANALYSES = {json.dumps(analyses, ensure_ascii=False)};"


# ── Formation coordinate templates (football pitch %, GK bottom y=92) ─────────
_FORMATION_COORDS = {
    "4-3-3":   [(50,92),(12,72),(36,76),(64,76),(88,72),(28,52),(50,56),(72,52),(20,26),(50,18),(80,26)],
    "4-2-3-1": [(50,92),(12,72),(36,76),(64,76),(88,72),(36,58),(64,58),(20,38),(50,34),(80,38),(50,16)],
    "4-4-2":   [(50,92),(12,72),(36,76),(64,76),(88,72),(14,50),(38,52),(62,52),(86,50),(38,22),(62,22)],
    "3-5-2":   [(50,92),(26,76),(50,78),(74,76),(8,52),(32,56),(50,58),(68,56),(92,52),(38,22),(62,22)],
    "4-1-4-1": [(50,92),(12,72),(36,76),(64,76),(88,72),(50,62),(16,46),(40,44),(60,44),(84,46),(50,18)],
}
_FOOT_FORMS = ["4-3-3", "4-2-3-1", "4-4-2", "3-5-2", "4-1-4-1"]


def _mid_rng(mid: str, salt: str) -> "_rng_mod.Random":
    return _rng_mod.Random(int(hashlib.md5((salt + mid).encode()).hexdigest()[:8], 16))


def _build_js_lineups() -> str:
    """Per-match probable XI with pitch coordinates → window.LINEUPS (football)."""
    out: dict = {}
    for mid, m in MATCHES.items():
        if "Football" not in m.get("sport", ""):
            continue
        rng = _mid_rng(mid, "L")
        sides: dict = {}
        for side in ("home", "away"):
            squad = TEAM_SQUADS.get(m[side]["name"])
            if not squad or len(squad) < 11:
                continue
            form = rng.choice(_FOOT_FORMS)
            coords = _FORMATION_COORDS[form]
            players = [
                {"name": squad[i][0], "pos": squad[i][1], "num": i + 1,
                 "x": coords[i][0], "y": coords[i][1]}
                for i in range(11)
            ]
            sides[side] = {"formation": form, "players": players}
        if "home" in sides and "away" in sides:
            out[mid] = sides
    return f"window.LINEUPS = {json.dumps(out, ensure_ascii=False)};"


def _build_js_matchups() -> str:
    """Per-match key individual duels with real players → window.MATCHUPS."""
    notes_fb = [
        "Verticalité supérieure en zone 14", "Profondeur sur le couloir",
        "Duel physique 50/50", "Avantage à la course", "Bataille au pressing",
        "Supériorité dans les airs", "Création vs récupération",
    ]
    notes_bk = [
        "Avantage de taille sous le cercle", "Vitesse balle en main supérieure",
        "Mismatch à exploiter en iso", "Duel de scoreurs", "Bataille au rebond",
        "Adresse extérieure décisive",
    ]
    notes_rg = [
        "Domination au contact", "Vitesse dans les intervalles",
        "Bataille des rucks", "Duel de buteurs", "Supériorité en touche",
        "Plaquage offensif clé",
    ]
    out: dict = {}
    for mid, m in MATCHES.items():
        rng = _mid_rng(mid, "M")
        hsq = TEAM_SQUADS.get(m["home"]["name"])
        asq = TEAM_SQUADS.get(m["away"]["name"])
        if not hsq or not asq:
            continue
        sport = m.get("sport", "")
        if "Football" in sport and len(hsq) >= 11 and len(asq) >= 11:
            pairs, notes = [(9, 3), (6, 6), (2, 9)], notes_fb       # att/def, mid/mid, def/att
        elif "Basket" in sport and len(hsq) >= 5 and len(asq) >= 5:
            pairs, notes = [(0, 0), (2, 2), (4, 4)], notes_bk        # PG, SF, C
        elif len(hsq) >= 8 and len(asq) >= 8:
            pairs, notes = [(0, 0), (2, 2), (5, 5)], notes_rg        # rugby lines
        else:
            continue
        picked = rng.sample(notes, k=min(3, len(notes)))
        duels = []
        for k, (hi, ai) in enumerate(pairs):
            hi = min(hi, len(hsq) - 1); ai = min(ai, len(asq) - 1)
            duels.append({
                "home": {"name": hsq[hi][0], "pos": hsq[hi][1]},
                "away": {"name": asq[ai][0], "pos": asq[ai][1]},
                "edge": rng.choice(["home", "away", "neutral"]),
                "note": picked[k] if k < len(picked) else "",
            })
        out[mid] = duels
    return f"window.MATCHUPS = {json.dumps(out, ensure_ascii=False)};"


def _build_js_timelines() -> str:
    """Per-match chronology with real scorers → window.TIMELINES (finished only)."""
    out: dict = {}
    for mid, m in MATCHES.items():
        if m.get("status") != "Terminé":
            continue
        if m["home"].get("score") is None or m["away"].get("score") is None:
            continue
        rng = _mid_rng(mid, "T")
        sport = m.get("sport", "")
        hs, as_ = int(m["home"]["score"]), int(m["away"]["score"])
        hcode, acode = m["home"]["short"], m["away"]["short"]
        hsq = TEAM_SQUADS.get(m["home"]["name"]) or []
        asq = TEAM_SQUADS.get(m["away"]["name"]) or []
        ev: list = []

        if "Football" in sport:
            def _att(sq):
                a = [p[0] for p in sq if p[1] in ("BU", "AD", "AG", "MO")]
                return a or [p[0] for p in sq[-3:]] or ["?"]
            ha, aa = _att(hsq), _att(asq)
            ng = hs + as_
            mins = sorted(rng.sample(range(3, 91), min(ng, 8))) if ng else []
            goals = [("home", hcode, ha)] * hs + [("away", acode, aa)] * as_
            rng.shuffle(goals)
            for i, mn in enumerate(mins[:len(goals)]):
                _side, code, pool = goals[i]
                ev.append({"min": f"{mn}'", "event": f"⚽ {rng.choice(pool)} ({code})", "accent": True})
            if hsq and asq:
                cm = rng.randint(20, 80); cc = rng.choice([hcode, acode])
                cpool = hsq if cc == hcode else asq
                ev.append({"min": f"{cm}'", "event": f"🟨 {rng.choice(cpool)[0]} ({cc})", "accent": False})
            ev.sort(key=lambda e: int(e["min"].rstrip("'")))
        elif "Basket" in sport:
            htop = hsq[0][0] if hsq else "?"; atop = asq[0][0] if asq else "?"
            lead = hcode if hs > as_ else acode
            ev = [
                {"min": "Q1", "event": f"Échanges serrés, {htop} chaud d'entrée", "accent": False},
                {"min": "Q2", "event": f"Run {rng.randint(10,16)}-{rng.randint(2,6)} mené par {htop if hs>=as_ else atop}", "accent": True},
                {"min": "Q3", "event": f"{atop} maintient {acode} au contact", "accent": False},
                {"min": "Q4", "event": f"{lead} fait la différence dans le money time", "accent": True},
            ]
        else:  # rugby
            hpool = [p[0] for p in hsq] or ["?"]; apool = [p[0] for p in asq] or ["?"]
            ev = [
                {"min": f"{rng.randint(5,20)}'", "event": f"🏉 Essai {rng.choice(hpool)} ({hcode})", "accent": True},
                {"min": f"{rng.randint(22,38)}'", "event": f"🥅 Pénalité {rng.choice(apool)} ({acode})", "accent": False},
                {"min": f"{rng.randint(45,60)}'", "event": f"🏉 Essai {rng.choice(apool)} ({acode})", "accent": True},
                {"min": f"{rng.randint(62,78)}'", "event": f"🏉 Essai {rng.choice(hpool)} ({hcode})", "accent": True},
            ]
        out[mid] = ev
    return f"window.TIMELINES = {json.dumps(out, ensure_ascii=False)};"


# ══════════════════════════════════════════════════════════════════════════════
# RUGBY PLAYBOOK (le foot et le basket existent déjà : FOOTBALL_PLAYBOOK / PLAYBOOK)
# ══════════════════════════════════════════════════════════════════════════════
RUGBY_PLAYBOOK: dict[str, dict] = {
    "maul_offensif": {
        "categorie": "Conquête / Touche",
        "objectif": "Avancer collectivement ballon porté après une touche pour marquer ou gagner une pénalité",
        "principe": "Après réception en touche, les avants se lient autour du porteur et poussent en bloc vers l'en-but adverse",
        "avantages": "Très difficile à défendre légalement, gagne du terrain et des pénalités, use le pack adverse",
        "limites": "Risque de maul écroulé sanctionné, dépend d'une touche maîtrisée",
        "reconnaitre": "Touche proche des 5m, alignement qui se regroupe immédiatement après la prise",
        "contre_mesures": "Sack immédiat sur le receveur, défendre en biais, ne pas s'engager (laisser filer)",
    },
    "touche_lancee": {
        "categorie": "Conquête / Touche",
        "objectif": "Sécuriser une possession propre et créer une plateforme de lancement de jeu",
        "principe": "Alignement codé, sauteur soulevé par deux relayeurs, lancer précis du talonneur",
        "avantages": "Possession garantie si bien exécutée, base de tous les systèmes offensifs",
        "limites": "Vulnérable au contest si timing imparfait, lancer sous pression difficile",
        "reconnaitre": "Mouvements de leurre dans l'alignement, signaux codés du sauteur",
        "contre_mesures": "Contest sur le sauteur principal, lecture des codes, pression sur le lanceur",
    },
    "melee_offensive": {
        "categorie": "Conquête / Mêlée",
        "objectif": "Dominer la mêlée fermée pour gagner du terrain, des pénalités ou lancer le jeu",
        "principe": "Les 8 avants poussent de façon coordonnée à l'introduction pour reculer le pack adverse",
        "avantages": "Arme psychologique et territoriale majeure, source de pénalités",
        "limites": "Très technique, sanctions sévères si désaxée ou écroulée",
        "reconnaitre": "Pack qui cherche systématiquement la pénalité plutôt que le ballon rapide",
        "contre_mesures": "Stabilité du pack, introduction rapide, sortie immédiate du ballon par le N°8",
    },
    "jeu_au_pied_occupation": {
        "categorie": "Jeu au pied / Territoire",
        "objectif": "Gérer le territoire et mettre l'adversaire sous pression dans son camp",
        "principe": "Coups de pied de déplacement (touches, diagonales, chandelles) pour reculer l'adversaire",
        "avantages": "Réduit le risque, force des sorties de camp sous pression, récupère des ballons hauts",
        "limites": "Rend le ballon à l'adversaire, prévisible si trop systématique",
        "reconnaitre": "Ouvreur qui tape dès la 2e ou 3e phase, ailes qui montent sur la chandelle",
        "contre_mesures": "Bon arrière sous les ballons hauts, contre-attaque rapide, fixer avant de taper",
    },
    "jeu_deploye": {
        "categorie": "Attaque / Jeu à la main",
        "objectif": "Créer le surnombre sur les extérieurs par une circulation rapide du ballon",
        "principe": "Fixation au centre puis transmission rapide vers les ailes avec des lignes de course croisées",
        "avantages": "Exploite la largeur, met les ailiers rapides en un-contre-un, spectaculaire",
        "limites": "Exige précision des passes et timing, risque d'interception",
        "reconnaitre": "Trois-quarts alignés en profondeur, ballon qui voyage vite après contact",
        "contre_mesures": "Défense montante agressive, pression sur le premier centre, glissement coordonné",
    },
    "defense_montante": {
        "categorie": "Défense",
        "objectif": "Étouffer l'attaque adverse en réduisant son temps et son espace",
        "principe": "La ligne défensive monte vite et en bloc (rush defense) pour plaquer derrière la ligne d'avantage",
        "avantages": "Crée des turnovers, force l'erreur et le jeu au pied précipité",
        "limites": "Vulnérable aux passes après-contact et au jeu au pied par-dessus",
        "reconnaitre": "Défenseurs qui jaillissent dès la sortie de ruck, fermeture rapide des intervalles",
        "contre_mesures": "Jeu au pied à ras ou par-dessus, passes sautées, attaquer l'épaule intérieure",
    },
    "defense_glissee": {
        "categorie": "Défense",
        "objectif": "Couvrir la largeur et neutraliser le surnombre adverse sur les extérieurs",
        "principe": "Les défenseurs glissent vers l'extérieur en marquant l'adversaire d'un cran décalé",
        "avantages": "Solide contre le jeu déployé, évite d'être débordé sur les ailes",
        "limites": "Crée des brèches intérieures, exposée aux courses à contre",
        "reconnaitre": "Ligne qui se décale latéralement plutôt que de monter franchement",
        "contre_mesures": "Course à contre, jeu au près sur le ruck, fixer l'extérieur puis repiquer",
    },
    "ruck_rapide": {
        "categorie": "Continuité / Ruck",
        "objectif": "Conserver et accélérer la sortie du ballon pour jouer face à une défense non replacée",
        "principe": "Nettoyage explosif et bas du ruck, demi de mêlée prêt à relancer en moins de 3 secondes",
        "avantages": "Empêche la défense de se replacer, crée des temps de retard exploitables",
        "limites": "Coûteux physiquement, risque de grattage si soutien lent",
        "reconnaitre": "Demi de mêlée déjà sur le ballon, soutiens qui arrivent groupés et bas",
        "contre_mesures": "Gratteur posté sur chaque ruck (jackal), ralentir la sortie légalement",
    },
    "pick_and_go": {
        "categorie": "Attaque / Jeu au près",
        "objectif": "Avancer en zone proche par des charges répétées pour fixer et fatiguer la défense",
        "principe": "Les avants ramassent au ras du ruck et percutent sur un ou deux temps de jeu successifs",
        "avantages": "Fixe les défenseurs au centre, ouvre les extérieurs, idéal proche de l'en-but",
        "limites": "Faible gain au mètre, prévisible, expose aux grattages",
        "reconnaitre": "Avants qui jouent au ras sur plusieurs phases consécutives près de la ligne",
        "contre_mesures": "Défense basse et dominante, gratteur sur le porteur isolé, tenir la ligne",
    },
    "contre_attaque": {
        "categorie": "Transition",
        "objectif": "Exploiter une récupération ou un ballon de pied adverse mal négocié",
        "principe": "Relance immédiate depuis l'arrière, soutiens qui remontent, recherche des espaces non couverts",
        "avantages": "Très payante contre une défense désorganisée, prend l'adversaire à contre-pied",
        "limites": "Risquée dans son propre camp, exige une lecture parfaite",
        "reconnaitre": "Arrière qui relance balle en main au lieu de taper, soutiens lancés",
        "contre_mesures": "Monter en filet sur le relanceur, jeu au pied précis, repli organisé",
    },
    "sortie_de_camp": {
        "categorie": "Gestion / Territoire",
        "objectif": "Sortir proprement de sa zone défensive sous pression",
        "principe": "Sécuriser une phase, puis taper en touche long ou jouer quelques temps pour gagner du champ",
        "avantages": "Soulage la défense, inverse la pression territoriale",
        "limites": "Risque de charge contrée, touche manquée coûteuse",
        "reconnaitre": "Jeu au pied dès la récupération dans les 22m, recherche de la ligne de touche",
        "contre_mesures": "Charge sur le botteur, montée sur réception, contre sur touche non trouvée",
    },
    "offload": {
        "categorie": "Attaque / Continuité",
        "objectif": "Maintenir la continuité en passant après contact avant d'aller au sol",
        "principe": "Le porteur résiste au plaquage et libère le ballon pour un soutien lancé",
        "avantages": "Casse la ligne défensive, supprime le temps de ruck, dynamise le jeu",
        "limites": "Risque élevé de turnover si soutien absent ou passe forcée",
        "reconnaitre": "Porteurs qui cherchent le bras libre dans le contact, soutiens proches",
        "contre_mesures": "Plaquage à deux (un sur le ballon), enchaîner bas pour empêcher l'offload",
    },
}

# Quelles équipes (réelles, présentes dans l'app) emploient nettement chaque tactique
TACTIC_TEAMS: dict[str, list] = {
    # Football
    "positional_play": ["Manchester City", "FC Barcelona", "Paris Saint-Germain"],
    "high_press": ["Liverpool FC", "Paris Saint-Germain", "Bayern Munich", "Arsenal FC"],
    "low_block": ["Atlético de Madrid", "OGC Nice"],
    "counter_attacking": ["Real Madrid CF", "Inter Milan", "AS Monaco"],
    "direct_play": ["RC Lens", "Newcastle United"],
    "build_up_court": ["Manchester City", "FC Barcelona", "Liverpool FC"],
    "inverted_fullbacks": ["Manchester City", "Bayern Munich"],
    "counter_press": ["Liverpool FC", "Bayern Munich", "Arsenal FC"],
    "mid_block": ["Juventus FC", "Aston Villa"],
    "overlaps": ["Liverpool FC", "Real Madrid CF"],
    "switch_play": ["Manchester City", "Real Madrid CF"],
    "trigger_pressing": ["Atalanta", "RB Leipzig"],
    # Basket
    "pick_and_roll": ["Denver Nuggets", "Dallas Mavericks", "AS Monaco Basket"],
    "spain_pnr": ["Boston Celtics", "Real Madrid Baloncesto"],
    "motion_offense": ["Golden State Warriors", "San Antonio Spurs"],
    "spread_offense": ["Boston Celtics", "Oklahoma City Thunder"],
    "transition_offense": ["Indiana Pacers", "Golden State Warriors"],
    "iso": ["Dallas Mavericks", "Phoenix Suns"],
    "isolation": ["Dallas Mavericks", "Phoenix Suns"],
    "post_up": ["Denver Nuggets", "Philadelphia 76ers"],
    "drop": ["Minnesota Timberwolves", "Cleveland Cavaliers"],
    "switch": ["Boston Celtics", "Oklahoma City Thunder"],
    "zone_offense": ["Olympiacos BC", "Panathinaikos"],
    # Rugby
    "maul_offensif": ["Stade Toulousain", "Stade Rochelais", "Montpellier Hérault Rugby"],
    "jeu_deploye": ["Stade Toulousain", "Bordeaux-Bègles"],
    "jeu_au_pied_occupation": ["Stade Rochelais", "Racing 92"],
    "defense_montante": ["Stade Rochelais", "Clermont Auvergne"],
    "ruck_rapide": ["Stade Toulousain", "Lyon OU"],
    "melee_offensive": ["Castres Olympique", "Aviron Bayonnais"],
    "contre_attaque": ["Stade Toulousain", "Racing 92"],
}

# id de tactique → type de schéma SVG (rendu côté React)
def _diagram_for(sport_key: str, tid: str, categorie: str) -> str:
    c = (categorie or "").lower()
    if sport_key == "football":
        if "press" in tid or "press" in c: return "fb_press"
        if "block" in tid: return "fb_block"
        if "build" in tid or "possession" in tid or "positional" in tid: return "fb_buildup"
        if "counter" in tid or "transition" in tid or "direct" in tid: return "fb_counter"
        if "corner" in tid or "free_kick" in tid or "throw" in tid or "phases" in c or "arrêté" in c: return "fb_setpiece"
        if "width" in tid or "overlap" in tid or "switch" in tid or "cross" in tid or "half_space" in tid: return "fb_width"
        return "fb_buildup"
    if sport_key == "basket":
        if "pnr" in tid or "pick" in tid or "roll" in tid or "drag" in tid or "spain" in tid: return "bk_pnr"
        if "iso" in tid: return "bk_iso"
        if "post" in tid: return "bk_post"
        if "motion" in tid or "princeton" in tid or "flex" in tid or "spread" in tid: return "bk_motion"
        if "zone" in tid or "trap" in tid or "press" in tid or "switch" in tid or "drop" in tid or "hedge" in tid or "ice" in tid or "defense" in tid: return "bk_defense"
        if "transition" in tid: return "bk_transition"
        return "bk_motion"
    # rugby
    if "maul" in tid or "touche" in tid: return "rg_lineout"
    if "melee" in tid: return "rg_scrum"
    if "pied" in tid or "sortie" in tid: return "rg_kick"
    if "defense" in tid: return "rg_defense"
    if "ruck" in tid or "pick" in tid or "offload" in tid: return "rg_ruck"
    return "rg_backline"


def _norm_tactic(sport_key: str, tid: str, d: dict) -> dict:
    name = tid.replace("_", " ").title()
    cat = d.get("categorie", "")
    return {
        "id": tid,
        "name": name,
        "categorie": cat,
        "objectif": d.get("objectif", ""),
        "principe": d.get("principe", d.get("structure", "")),
        "avantages": d.get("avantages", ""),
        "limites": d.get("limites", ""),
        "reconnaitre": d.get("reconnaitre", d.get("reconnaître", "")),
        "contre_mesures": d.get("contre_mesures", ""),
        "teams": TACTIC_TEAMS.get(tid, []),
        "diagram": _diagram_for(sport_key, tid, cat),
    }


def _build_js_playbooks() -> str:
    """Football + basket + rugby tactics → window.PLAYBOOKS (with teams + diagram)."""
    out = {
        "football": [_norm_tactic("football", k, v) for k, v in FOOTBALL_PLAYBOOK.items()],
        "basket":   [_norm_tactic("basket", k, v) for k, v in PLAYBOOK.items()],
        "rugby":    [_norm_tactic("rugby", k, v) for k, v in RUGBY_PLAYBOOK.items()],
    }
    return f"window.PLAYBOOKS = {json.dumps(out, ensure_ascii=False)};"


def _build_js_squads() -> str:
    """Real squads per team → window.SQUADS (for the tactical simulator/lineup editor)."""
    # team → sport, derived from MATCHES
    team_sport: dict[str, str] = {}
    sport_map = {"⚽ Football": "football", "🏀 Basket": "basket", "🏉 Rugby": "rugby"}
    for m in MATCHES.values():
        sk = sport_map.get(m.get("sport", ""), "football")
        for side in ("home", "away"):
            team_sport.setdefault(m[side]["name"], sk)
    out: dict = {}
    for team, players in TEAM_SQUADS.items():
        # infer sport from squad size/positions if not in MATCHES
        sk = team_sport.get(team)
        if sk is None:
            sk = "basket" if len(players) == 5 else ("rugby" if len(players) in (8, 9) else "football")
        out[team] = {"sport": sk, "players": [[p[0], p[1]] for p in players]}
    return f"window.SQUADS = {json.dumps(out, ensure_ascii=False)};"


def _build_js_teamstats() -> str:
    """Aggregate per-team season stats from finished MATCHES → window.TEAMSTATS.

    Powers the comparator and season-trends screens (computed client-side from this).
    """
    stats: dict = {}
    sport_map = {"⚽ Football": "football", "🏀 Basket": "basket", "🏉 Rugby": "rugby"}

    def _row(team, sport_key, comp):
        return stats.setdefault(team, {
            "sport": sport_key, "competition": comp,
            "played": 0, "w": 0, "d": 0, "l": 0,
            "pf": 0, "pa": 0, "form": [], "results": [],
        })

    finished = [
        (mid, m) for mid, m in MATCHES.items()
        if m.get("status") == "Terminé"
        and m["home"].get("score") is not None
        and m["away"].get("score") is not None
    ]
    def _sk(item):
        try:
            return datetime.strptime(item[1].get("date", ""), "%Y-%m-%d")
        except Exception:
            return datetime.min
    finished.sort(key=_sk)

    for _mid, m in finished:
        sk = sport_map.get(m.get("sport", ""), "football")
        comp = m.get("competition", "")
        hs, as_ = int(m["home"]["score"]), int(m["away"]["score"])
        for team, gf, ga, opp in [
            (m["home"]["name"], hs, as_, m["away"]["name"]),
            (m["away"]["name"], as_, hs, m["home"]["name"]),
        ]:
            r = _row(team, sk, comp)
            r["played"] += 1
            r["pf"] += gf; r["pa"] += ga
            res = "V" if gf > ga else ("N" if gf == ga else "D")
            r["w"] += res == "V"; r["d"] += res == "N"; r["l"] += res == "D"
            r["form"].append(res)
            r["results"].append({"gf": gf, "ga": ga, "res": res, "opp": opp,
                                  "date": m.get("date", "")})
    for r in stats.values():
        r["form"] = r["form"][-5:]
    return f"window.TEAMSTATS = {json.dumps(stats, ensure_ascii=False)};"


def _build_js_standings() -> str:
    """Explicit league tables → window.STANDINGS (Ligue 1 authored; others derived)."""
    out: dict = {"Ligue 1": LIGUE1_STANDINGS}
    return f"window.STANDINGS = {json.dumps(out, ensure_ascii=False)};"


_ROOT = Path(__file__).parent

def _read(rel: str) -> str:
    return (_ROOT / rel).read_text(encoding="utf-8")


_CSS_TOKENS = _read("tokens.css")
_CSS_STYLES = _read("styles.css")
_JS_DATA    = _read("data.js")
_JSX_TWEAKS = _read("tweaks-panel.jsx")
_JSX_UI     = _read("components-ui.jsx")
_JSX_SHELL  = _read("components-shell.jsx")
_JSX_DASH   = _read("screen-dashboard.jsx")
_JSX_MATCH  = _read("screen-matches.jsx")
_JSX_PRE    = _read("screen-prematch.jsx")
_JSX_POST   = _read("screen-postmatch.jsx")
_JSX_MISC   = _read("screen-misc.jsx")
_JSX_APP    = _read("app.jsx")

_JS_REAL_MATCHES   = _build_js_matches()
_JS_REAL_ANALYSES  = _build_js_analyses()
_JS_REAL_LINEUPS   = _build_js_lineups()
_JS_REAL_MATCHUPS  = _build_js_matchups()
_JS_REAL_TIMELINES = _build_js_timelines()
_JS_PLAYBOOKS      = _build_js_playbooks()
_JS_SQUADS         = _build_js_squads()
_JS_TEAMSTATS      = _build_js_teamstats()
_JS_STANDINGS      = _build_js_standings()

_HTML = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>CoachIQ</title>
<style>{_CSS_TOKENS}</style>
<style>{_CSS_STYLES}</style>
<style>html,body{{margin:0;padding:0;overflow-x:hidden}}</style>
</head>
<body data-product="coachiq">
  <div id="root"></div>

  <script src="https://unpkg.com/react@18.3.1/umd/react.development.js"
          integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L"
          crossorigin="anonymous"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
          integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm"
          crossorigin="anonymous"></script>
  <script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
          integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y"
          crossorigin="anonymous"></script>

  <script>{_JS_DATA}</script>
  <script>{_JS_REAL_MATCHES}</script>
  <script>{_JS_REAL_ANALYSES}</script>
  <script>{_JS_REAL_LINEUPS}</script>
  <script>{_JS_REAL_MATCHUPS}</script>
  <script>{_JS_REAL_TIMELINES}</script>
  <script>{_JS_PLAYBOOKS}</script>
  <script>{_JS_SQUADS}</script>
  <script>{_JS_TEAMSTATS}</script>
  <script>{_JS_STANDINGS}</script>
  <script type="text/babel" data-presets="react">{_JSX_TWEAKS}</script>
  <script type="text/babel" data-presets="react">{_JSX_UI}</script>
  <script type="text/babel" data-presets="react">{_JSX_SHELL}</script>
  <script type="text/babel" data-presets="react">{_JSX_DASH}</script>
  <script type="text/babel" data-presets="react">{_JSX_MATCH}</script>
  <script type="text/babel" data-presets="react">{_JSX_PRE}</script>
  <script type="text/babel" data-presets="react">{_JSX_POST}</script>
  <script type="text/babel" data-presets="react">{_JSX_MISC}</script>
  <script type="text/babel" data-presets="react">{_JSX_APP}</script>
</body>
</html>"""

st.iframe(_HTML, height=1400)
