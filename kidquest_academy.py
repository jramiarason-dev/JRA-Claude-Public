"""
KidQuest Academy — Gamified Learning Platform for Children (ages 4–7)
3 subject tabs: English Quest, Geo Explorer, Math Arena
Bilingual FR/EN — country data served by Countrylayer REST API
(falls back to 20 offline countries if API is unreachable)
"""

import streamlit as st
import random
import requests
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="KidQuest Academy 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# CSS  — Fredoka One font, rounded buttons, animated banners
# ──────────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@800;900&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Fredoka One', 'Nunito', cursive !important;
        }

        /* ── Main title ── */
        .kq-title {
            text-align: center;
            font-size: 3.2em;
            font-family: 'Fredoka One', cursive;
            background: linear-gradient(135deg, #FF6B35, #FFD93D, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0;
            line-height: 1.1;
        }
        .kq-subtitle {
            text-align: center;
            font-size: 1.25em;
            color: #888;
            margin-top: 0;
            font-family: 'Fredoka One', cursive;
        }

        /* ── Tab header bars ── */
        .tab-header-orange {
            background: linear-gradient(135deg, #FF6B35, #FF8E53);
            color: white;
            padding: 16px 24px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.35em;
            font-family: 'Fredoka One', cursive;
            margin-bottom: 14px;
        }
        .tab-header-teal {
            background: linear-gradient(135deg, #4ECDC4, #44A9C6);
            color: white;
            padding: 16px 24px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.35em;
            font-family: 'Fredoka One', cursive;
            margin-bottom: 14px;
        }
        .tab-header-green {
            background: linear-gradient(135deg, #A8E6CF, #56C596);
            color: white;
            padding: 16px 24px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.35em;
            font-family: 'Fredoka One', cursive;
            margin-bottom: 14px;
        }

        /* ── Question card ── */
        .q-card {
            background: #FFFDF7;
            border: 4px solid #FFD93D;
            border-radius: 24px;
            padding: 28px 20px;
            text-align: center;
            font-size: 2em;
            font-family: 'Fredoka One', cursive;
            margin: 14px 0;
            box-shadow: 0 6px 18px rgba(0,0,0,0.09);
            line-height: 1.4;
        }
        .q-card-teal  { border-color: #4ECDC4; }
        .q-card-green { border-color: #A8E6CF; }

        /* ── Feedback banners ── */
        @keyframes popIn {
            0%   { transform: scale(0.85); opacity: 0; }
            70%  { transform: scale(1.04); }
            100% { transform: scale(1);    opacity: 1; }
        }
        .banner-ok {
            background: linear-gradient(135deg, #6BCB77, #4D9BE6);
            color: white;
            padding: 18px 22px;
            border-radius: 20px;
            text-align: center;
            font-size: 1.35em;
            font-family: 'Fredoka One', cursive;
            animation: popIn 0.35s ease forwards;
            margin: 10px 0;
            line-height: 1.5;
        }
        .banner-err {
            background: linear-gradient(135deg, #FF6B6B, #FF8E53);
            color: white;
            padding: 18px 22px;
            border-radius: 20px;
            text-align: center;
            font-size: 1.35em;
            font-family: 'Fredoka One', cursive;
            animation: popIn 0.35s ease forwards;
            margin: 10px 0;
            line-height: 1.5;
        }
        .banner-info {
            background: linear-gradient(135deg, #4ECDC4, #44A9C6);
            color: white;
            padding: 13px 18px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.1em;
            font-family: 'Fredoka One', cursive;
            margin: 8px 0;
            line-height: 1.5;
        }
        .banner-info-green {
            background: linear-gradient(135deg, #A8E6CF, #56C596);
            color: white;
            padding: 13px 18px;
            border-radius: 16px;
            text-align: center;
            font-size: 1.1em;
            font-family: 'Fredoka One', cursive;
            margin: 8px 0;
            line-height: 1.5;
        }

        /* ── Feedback row items (Continent Sorter) ── */
        .fb-ok  { background:#6BCB77; color:white; padding:8px 14px; border-radius:12px; margin:4px 0; font-family:'Fredoka One',cursive; }
        .fb-err { background:#FF6B6B; color:white; padding:8px 14px; border-radius:12px; margin:4px 0; font-family:'Fredoka One',cursive; }

        /* ── Buttons ── */
        .stButton > button {
            font-family: 'Fredoka One', cursive !important;
            font-size: 1.15em !important;
            border-radius: 18px !important;
            padding: 14px 28px !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
            font-weight: normal !important;
        }
        .stButton > button:hover {
            transform: scale(1.06) !important;
            box-shadow: 0 8px 22px rgba(0,0,0,0.18) !important;
        }

        /* ── Number input ── */
        .stNumberInput input {
            font-size: 1.6em !important;
            text-align: center !important;
            font-family: 'Fredoka One', cursive !important;
            border-radius: 14px !important;
        }

        /* ── Radio ── */
        .stRadio label { font-family: 'Fredoka One', cursive !important; font-size: 1.05em !important; }

        /* ── Selectbox ── */
        .stSelectbox div[data-baseweb="select"] { font-family: 'Fredoka One', cursive !important; }

        /* ── Sidebar score cards ── */
        .sb-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 14px 16px;
            border-radius: 14px;
            text-align: center;
            font-family: 'Fredoka One', cursive;
            font-size: 1.05em;
            margin: 5px 0;
        }
        .sb-tab { padding:8px 12px; border-radius:0 12px 12px 0; margin:4px 0; font-family:'Fredoka One',cursive; }

        /* ── Score display inline ── */
        .score-line { text-align:right; font-size:1.25em; font-family:'Fredoka One',cursive; margin-bottom:6px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
# ════════════════════  GAME DATA  ════════════════════
# ──────────────────────────────────────────────────────────────────────────────

# ── Tab 1 · English Quest ─────────────────────────────────────────────────────

# 35 word pairs  (English, French, emoji, difficulty level)
WORD_PAIRS = [
    # easy — 3-4 letter words
    {"en": "CAT",    "fr": "CHAT",          "emoji": "🐱", "lvl": "easy"},
    {"en": "DOG",    "fr": "CHIEN",         "emoji": "🐶", "lvl": "easy"},
    {"en": "SUN",    "fr": "SOLEIL",        "emoji": "☀️", "lvl": "easy"},
    {"en": "BEE",    "fr": "ABEILLE",       "emoji": "🐝", "lvl": "easy"},
    {"en": "COW",    "fr": "VACHE",         "emoji": "🐄", "lvl": "easy"},
    {"en": "HEN",    "fr": "POULE",         "emoji": "🐔", "lvl": "easy"},
    {"en": "PIG",    "fr": "COCHON",        "emoji": "🐷", "lvl": "easy"},
    {"en": "OWL",    "fr": "HIBOU",         "emoji": "🦉", "lvl": "easy"},
    {"en": "ANT",    "fr": "FOURMI",        "emoji": "🐜", "lvl": "easy"},
    {"en": "EGG",    "fr": "OEUF",          "emoji": "🥚", "lvl": "easy"},
    {"en": "FISH",   "fr": "POISSON",       "emoji": "🐟", "lvl": "easy"},
    {"en": "DUCK",   "fr": "CANARD",        "emoji": "🦆", "lvl": "easy"},
    {"en": "FROG",   "fr": "GRENOUILLE",    "emoji": "🐸", "lvl": "easy"},
    {"en": "BEAR",   "fr": "OURS",          "emoji": "🐻", "lvl": "easy"},
    {"en": "BIRD",   "fr": "OISEAU",        "emoji": "🐦", "lvl": "easy"},
    {"en": "WOLF",   "fr": "LOUP",          "emoji": "🐺", "lvl": "easy"},
    {"en": "LION",   "fr": "LION",          "emoji": "🦁", "lvl": "easy"},
    {"en": "DEER",   "fr": "CERF",          "emoji": "🦌", "lvl": "easy"},
    {"en": "STAR",   "fr": "ETOILE",        "emoji": "⭐",  "lvl": "easy"},
    {"en": "RAIN",   "fr": "PLUIE",         "emoji": "🌧️", "lvl": "easy"},
    # medium — 5-7 letter words
    {"en": "HORSE",  "fr": "CHEVAL",        "emoji": "🐴", "lvl": "medium"},
    {"en": "TIGER",  "fr": "TIGRE",         "emoji": "🐯", "lvl": "medium"},
    {"en": "SNAKE",  "fr": "SERPENT",       "emoji": "🐍", "lvl": "medium"},
    {"en": "WHALE",  "fr": "BALEINE",       "emoji": "🐋", "lvl": "medium"},
    {"en": "EAGLE",  "fr": "AIGLE",         "emoji": "🦅", "lvl": "medium"},
    {"en": "PANDA",  "fr": "PANDA",         "emoji": "🐼", "lvl": "medium"},
    {"en": "KOALA",  "fr": "KOALA",         "emoji": "🐨", "lvl": "medium"},
    {"en": "SHARK",  "fr": "REQUIN",        "emoji": "🦈", "lvl": "medium"},
    {"en": "CAMEL",  "fr": "CHAMEAU",       "emoji": "🐪", "lvl": "medium"},
    {"en": "ZEBRA",  "fr": "ZEBRE",         "emoji": "🦓", "lvl": "medium"},
    {"en": "RABBIT", "fr": "LAPIN",         "emoji": "🐰", "lvl": "medium"},
    {"en": "TURTLE", "fr": "TORTUE",        "emoji": "🐢", "lvl": "medium"},
    {"en": "MONKEY", "fr": "SINGE",         "emoji": "🐵", "lvl": "medium"},
    {"en": "PARROT", "fr": "PERROQUET",     "emoji": "🦜", "lvl": "medium"},
    {"en": "FLOWER", "fr": "FLEUR",         "emoji": "🌸", "lvl": "medium"},
]

# 20 sentences with a blanked-out word
SENTENCES = [
    {"words": ["I",     "love",  "cats"],       "blank": 1, "opts": ["love",  "hate",  "see"],      "fr": "J'aime les chats"},
    {"words": ["The",   "sun",   "shines"],      "blank": 1, "opts": ["sun",   "moon",  "star"],     "fr": "Le soleil brille"},
    {"words": ["She",   "is",    "happy"],       "blank": 2, "opts": ["happy", "sad",   "big"],      "fr": "Elle est heureuse"},
    {"words": ["I",     "eat",   "apples"],      "blank": 2, "opts": ["apples","books", "shoes"],    "fr": "Je mange des pommes"},
    {"words": ["The",   "dog",   "runs"],        "blank": 1, "opts": ["dog",   "cat",   "fish"],     "fr": "Le chien court"},
    {"words": ["He",    "reads", "books"],       "blank": 1, "opts": ["reads", "eats",  "draws"],    "fr": "Il lit des livres"},
    {"words": ["We",    "like",  "music"],       "blank": 2, "opts": ["music", "water", "sleep"],    "fr": "Nous aimons la musique"},
    {"words": ["Birds", "can",   "fly"],         "blank": 2, "opts": ["fly",   "swim",  "jump"],     "fr": "Les oiseaux peuvent voler"},
    {"words": ["Fish",  "live",  "underwater"],  "blank": 1, "opts": ["live",  "sleep", "run"],      "fr": "Les poissons vivent sous l'eau"},
    {"words": ["I",     "drink", "milk"],        "blank": 2, "opts": ["milk",  "sand",  "rock"],     "fr": "Je bois du lait"},
    {"words": ["She",   "draws", "flowers"],     "blank": 2, "opts": ["flowers","tables","cars"],    "fr": "Elle dessine des fleurs"},
    {"words": ["The",   "bear",  "sleeps"],      "blank": 1, "opts": ["bear",  "horse", "bird"],     "fr": "L'ours dort"},
    {"words": ["We",    "play",  "outside"],     "blank": 2, "opts": ["outside","inside","upside"],  "fr": "Nous jouons dehors"},
    {"words": ["The",   "cat",   "meows"],       "blank": 2, "opts": ["meows", "barks", "roars"],    "fr": "Le chat miaule"},
    {"words": ["I",     "am",    "six"],         "blank": 2, "opts": ["six",   "two",   "ten"],      "fr": "J'ai six ans"},
    {"words": ["Stars", "shine", "bright"],      "blank": 1, "opts": ["shine", "fall",  "grow"],     "fr": "Les etoiles brillent"},
    {"words": ["Frogs", "love",  "rain"],        "blank": 2, "opts": ["rain",  "snow",  "heat"],     "fr": "Les grenouilles aiment la pluie"},
    {"words": ["I",     "see",   "rainbows"],    "blank": 1, "opts": ["see",   "hear",  "smell"],    "fr": "Je vois des arcs-en-ciel"},
    {"words": ["My",    "name",  "is"],          "blank": 0, "opts": ["My",    "His",   "Her"],      "fr": "Mon prenom est"},
    {"words": ["The",   "sky",   "is",  "blue"], "blank": 3, "opts": ["blue",  "red",   "green"],    "fr": "Le ciel est bleu"},
]

# 15 emoji/image items for Listen & Spell
SPELL_ITEMS = [
    {"emoji": "🌈", "name": "Rainbow",    "opts": ["Rainbow",    "Sunset",    "Thunder",   "Snowfall"]},
    {"emoji": "🎸", "name": "Guitar",     "opts": ["Guitar",     "Piano",     "Violin",    "Trumpet"]},
    {"emoji": "🏖️", "name": "Beach",      "opts": ["Beach",      "Forest",    "Desert",    "Mountain"]},
    {"emoji": "🚀", "name": "Rocket",     "opts": ["Rocket",     "Plane",     "Balloon",   "Spaceship"]},
    {"emoji": "🦋", "name": "Butterfly",  "opts": ["Butterfly",  "Dragonfly", "Ladybug",   "Caterpillar"]},
    {"emoji": "🌺", "name": "Flower",     "opts": ["Flower",     "Mushroom",  "Cactus",    "Leaf"]},
    {"emoji": "🐬", "name": "Dolphin",    "opts": ["Dolphin",    "Whale",     "Shark",     "Turtle"]},
    {"emoji": "🏔️", "name": "Mountain",  "opts": ["Mountain",   "Volcano",   "Island",    "Valley"]},
    {"emoji": "🌙", "name": "Moon",       "opts": ["Moon",       "Star",      "Comet",     "Planet"]},
    {"emoji": "🦁", "name": "Lion",       "opts": ["Lion",       "Tiger",     "Leopard",   "Cheetah"]},
    {"emoji": "🍓", "name": "Strawberry", "opts": ["Strawberry", "Raspberry", "Blueberry", "Cherry"]},
    {"emoji": "🌊", "name": "Wave",       "opts": ["Wave",       "Storm",     "Ripple",    "Tide"]},
    {"emoji": "🎯", "name": "Target",     "opts": ["Target",     "Shield",    "Arrow",     "Sword"]},
    {"emoji": "🎪", "name": "Circus",     "opts": ["Circus",     "Theater",   "Stadium",   "Market"]},
    {"emoji": "🎨", "name": "Painting",   "opts": ["Painting",   "Drawing",   "Sculpture", "Music"]},
]

# ── Tab 2 · Geo Explorer — Countrylayer API ──────────────────────────────────

# 20-country offline fallback used when the API is unreachable
FALLBACK_COUNTRIES = [
    {"name_en":"France",        "name_fr":"France",          "flag_emoji":"🇫🇷","capital":"Paris",          "lat": 46.23,"lon":   2.21,"region":"Europe",   "subregion":"Western Europe",    "population": 67_000_000},
    {"name_en":"Germany",       "name_fr":"Allemagne",       "flag_emoji":"🇩🇪","capital":"Berlin",         "lat": 51.17,"lon":  10.45,"region":"Europe",   "subregion":"Western Europe",    "population": 83_000_000},
    {"name_en":"Italy",         "name_fr":"Italie",          "flag_emoji":"🇮🇹","capital":"Rome",           "lat": 41.87,"lon":  12.57,"region":"Europe",   "subregion":"Southern Europe",   "population": 60_000_000},
    {"name_en":"Spain",         "name_fr":"Espagne",         "flag_emoji":"🇪🇸","capital":"Madrid",         "lat": 40.46,"lon":  -3.75,"region":"Europe",   "subregion":"Southern Europe",   "population": 47_000_000},
    {"name_en":"United Kingdom","name_fr":"Royaume-Uni",     "flag_emoji":"🇬🇧","capital":"London",         "lat": 55.38,"lon":  -3.44,"region":"Europe",   "subregion":"Northern Europe",   "population": 67_000_000},
    {"name_en":"Japan",         "name_fr":"Japon",           "flag_emoji":"🇯🇵","capital":"Tokyo",          "lat": 36.20,"lon": 138.25,"region":"Asia",     "subregion":"Eastern Asia",      "population":126_000_000},
    {"name_en":"China",         "name_fr":"Chine",           "flag_emoji":"🇨🇳","capital":"Beijing",        "lat": 35.86,"lon": 104.20,"region":"Asia",     "subregion":"Eastern Asia",      "population":1_400_000_000},
    {"name_en":"India",         "name_fr":"Inde",            "flag_emoji":"🇮🇳","capital":"New Delhi",      "lat": 20.59,"lon":  78.96,"region":"Asia",     "subregion":"Southern Asia",     "population":1_380_000_000},
    {"name_en":"United States", "name_fr":"Etats-Unis",      "flag_emoji":"🇺🇸","capital":"Washington D.C.","lat": 37.09,"lon": -95.71,"region":"Americas", "subregion":"Northern America",  "population":331_000_000},
    {"name_en":"Brazil",        "name_fr":"Bresil",          "flag_emoji":"🇧🇷","capital":"Brasilia",       "lat":-14.24,"lon": -51.93,"region":"Americas", "subregion":"South America",     "population":213_000_000},
    {"name_en":"Canada",        "name_fr":"Canada",          "flag_emoji":"🇨🇦","capital":"Ottawa",         "lat": 56.13,"lon":-106.35,"region":"Americas", "subregion":"Northern America",  "population": 38_000_000},
    {"name_en":"Mexico",        "name_fr":"Mexique",         "flag_emoji":"🇲🇽","capital":"Mexico City",    "lat": 23.63,"lon":-102.55,"region":"Americas", "subregion":"Central America",   "population":129_000_000},
    {"name_en":"Nigeria",       "name_fr":"Nigeria",         "flag_emoji":"🇳🇬","capital":"Abuja",          "lat":  9.08,"lon":   8.68,"region":"Africa",   "subregion":"Western Africa",    "population":211_000_000},
    {"name_en":"Egypt",         "name_fr":"Egypte",          "flag_emoji":"🇪🇬","capital":"Cairo",          "lat": 26.82,"lon":  30.80,"region":"Africa",   "subregion":"Northern Africa",   "population":102_000_000},
    {"name_en":"South Africa",  "name_fr":"Afrique du Sud",  "flag_emoji":"🇿🇦","capital":"Cape Town",      "lat":-30.56,"lon":  22.94,"region":"Africa",   "subregion":"Southern Africa",   "population": 60_000_000},
    {"name_en":"Kenya",         "name_fr":"Kenya",           "flag_emoji":"🇰🇪","capital":"Nairobi",        "lat":  0.02,"lon":  37.91,"region":"Africa",   "subregion":"Eastern Africa",    "population": 54_000_000},
    {"name_en":"Australia",     "name_fr":"Australie",       "flag_emoji":"🇦🇺","capital":"Canberra",       "lat":-25.27,"lon": 133.78,"region":"Oceania",  "subregion":"Australia and New Zealand","population": 26_000_000},
    {"name_en":"New Zealand",   "name_fr":"Nouvelle-Zelande","flag_emoji":"🇳🇿","capital":"Wellington",     "lat":-40.90,"lon": 174.89,"region":"Oceania",  "subregion":"Australia and New Zealand","population":  5_000_000},
    {"name_en":"Argentina",     "name_fr":"Argentine",       "flag_emoji":"🇦🇷","capital":"Buenos Aires",   "lat":-38.42,"lon": -63.62,"region":"Americas", "subregion":"South America",     "population": 45_000_000},
    {"name_en":"Turkey",        "name_fr":"Turquie",         "flag_emoji":"🇹🇷","capital":"Ankara",         "lat": 38.96,"lon":  35.24,"region":"Asia",     "subregion":"Western Asia",      "population": 84_000_000},
]

# Capital city coordinates for the map's second diamond pin.
# Country lat/lon comes from the API; capital coords are supplementary only.
CAPITAL_COORDS = {
    "France":         (48.86,   2.35), "Germany":        (52.52,  13.40),
    "Italy":          (41.90,  12.50), "Spain":          (40.42,  -3.70),
    "United Kingdom": (51.51,  -0.13), "Portugal":       (38.72,  -9.14),
    "Netherlands":    (52.37,   4.90), "Belgium":        (50.85,   4.35),
    "Switzerland":    (46.95,   7.45), "Sweden":         (59.33,  18.07),
    "Greece":         (37.98,  23.73), "Iceland":        (64.13, -21.82),
    "Japan":          (35.69, 139.69), "China":          (39.91, 116.39),
    "India":          (28.61,  77.21), "South Korea":    (37.57, 126.98),
    "Thailand":       (13.75, 100.52), "Vietnam":        (21.03, 105.85),
    "Saudi Arabia":   (24.69,  46.72), "Turkey":         (39.92,  32.85),
    "Philippines":    (14.60, 120.98), "Indonesia":      (-6.21, 106.85),
    "Iran":           (35.69,  51.42), "Afghanistan":    (34.52,  69.18),
    "United States":  (38.91, -77.04), "Brazil":         (-15.78,-47.93),
    "Canada":         (45.42, -75.70), "Mexico":         (19.43, -99.13),
    "Argentina":      (-34.60,-58.38), "Colombia":       ( 4.71, -74.07),
    "Peru":           (-12.05,-77.05), "Chile":          (-33.46,-70.65),
    "Cuba":           (23.11, -82.37), "Venezuela":      (10.50, -66.92),
    "South Africa":   (-33.93,  18.42),"Nigeria":        ( 9.07,   7.40),
    "Kenya":          (-1.29,  36.82), "Egypt":          (30.04,  31.24),
    "Morocco":        (34.02,  -6.84), "Ghana":          ( 5.56,  -0.20),
    "Ethiopia":       ( 9.03,  38.74), "Tanzania":       (-6.18,  35.74),
    "Australia":      (-35.28,149.13), "New Zealand":    (-41.29,174.78),
    "Fiji":           (-18.14,178.44),
}

# Countrylayer API region → child-friendly bilingual label
REGION_LABELS = {
    "Africa":   "Afrique 🌍 / Africa 🌍",
    "Americas": "Amériques 🌎 / Americas 🌎",
    "Asia":     "Asie 🌏 / Asia 🌏",
    "Europe":   "Europe 🏰 / Europe 🏰",
    "Oceania":  "Océanie 🏝️ / Oceania 🏝️",
    "Polar":    "Pôles ❄️ / Polar ❄️",
}

# Map zoom per API region: (center_lat, center_lon, projection_scale)
REGION_ZOOM = {
    "Europe":   (54.0,  15.0, 3.0),
    "Asia":     (32.0,  95.0, 1.8),
    "Americas": ( 5.0, -80.0, 1.4),
    "Africa":   ( 5.0,  20.0, 1.8),
    "Oceania":  (-25.0, 145.0, 2.5),
    "Polar":    ( 0.0,   0.0, 1.0),
}

# English names considered "easy" for Capital Challenge mode
EASY_CAPITAL_NAMES = {
    "France", "Japan", "Brazil", "United States", "United Kingdom",
    "Germany", "Italy", "Spain", "Canada", "Mexico", "Australia", "China", "India",
}


def code_to_flag(alpha2: str) -> str:
    """Convert ISO alpha-2 code to regional indicator flag emoji ('FR' → '🇫🇷')."""
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in alpha2.upper())


@st.cache_data(ttl=3600)
def _fetch_raw_countries(api_key: str) -> tuple:
    """Single cached HTTP call to Countrylayer /all endpoint."""
    try:
        resp = requests.get(
            "https://api.countrylayer.com/v2/all",
            params={"access_key": api_key},
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and "error" in data:
            return [], f"API error {data['error'].get('code','?')}: {data['error'].get('info','')}"
        return (data if isinstance(data, list) else []), ""
    except Exception as exc:
        return [], str(exc)


def load_countries() -> tuple:
    """Return (country_list, error_msg). Falls back to FALLBACK_COUNTRIES on any problem."""
    try:
        api_key = st.secrets["COUNTRYLAYER_API_KEY"]
    except Exception:
        return FALLBACK_COUNTRIES, "⚙️ secrets.toml not configured — playing offline"

    raw, err = _fetch_raw_countries(api_key)
    if err or not raw:
        return FALLBACK_COUNTRIES, err or "Empty API response — playing offline"

    countries = []
    for item in raw:
        try:
            latlng = item.get("latlng") or []
            if len(latlng) < 2:
                continue
            alpha2   = item.get("alpha2Code") or ""
            trans    = item.get("translations") or {}
            name_en  = item.get("name") or "?"
            region   = item.get("region") or ""
            countries.append({
                "name_en":    name_en,
                "name_fr":    trans.get("fr") or name_en,
                "flag_emoji": code_to_flag(alpha2) if alpha2 else "🏳️",
                "capital":    item.get("capital") or "?",
                "lat":        float(latlng[0]),
                "lon":        float(latlng[1]),
                "region":     region,
                "subregion":  item.get("subregion") or "",
                "population": int(item.get("population") or 0),
            })
        except (TypeError, ValueError):
            continue

    if not countries:
        return FALLBACK_COUNTRIES, "No valid countries parsed — playing offline"
    return countries, ""

# ── Tab 3 · Math Arena ────────────────────────────────────────────────────────

COUNTING_EMOJIS = ["🍎","🐱","⭐","🌸","🎈","🐶","🍕","🦋","🚀","🍓"]

# 15 number-sequence patterns  (sequence contains "__" as placeholder, answer, options)
PATTERNS = [
    # +1
    {"seq": [1,  2,  3,  "__", 5],   "ans": 4,  "opts": [3,  4,  6],  "rule": "+1"},
    {"seq": [5,  6,  7,  8,  "__"],  "ans": 9,  "opts": [9,  10, 7],  "rule": "+1"},
    {"seq": [10, "__",12, 13, 14],   "ans": 11, "opts": [11, 9,  15], "rule": "+1"},
    # +2
    {"seq": [2,  4,  "__", 8,  10],  "ans": 6,  "opts": [5,  6,  7],  "rule": "+2"},
    {"seq": [1,  3,  5,  "__", 9],   "ans": 7,  "opts": [6,  7,  8],  "rule": "+2"},
    {"seq": ["__",4,  6,  8,  10],   "ans": 2,  "opts": [1,  2,  3],  "rule": "+2"},
    # +3
    {"seq": [3,  6,  9,  "__", 15],  "ans": 12, "opts": [11, 12, 13], "rule": "+3"},
    {"seq": [0,  3,  6,  9,  "__"],  "ans": 12, "opts": [10, 12, 15], "rule": "+3"},
    # +5
    {"seq": [5,  10, "__",20, 25],   "ans": 15, "opts": [14, 15, 16], "rule": "+5"},
    {"seq": [0,  5,  10, "__",20],   "ans": 15, "opts": [12, 15, 18], "rule": "+5"},
    # ×2
    {"seq": [1,  2,  4,  "__",16],   "ans": 8,  "opts": [6,  8,  10], "rule": "×2"},
    {"seq": [2,  4,  "__",16, 32],   "ans": 8,  "opts": [7,  8,  9],  "rule": "×2"},
    # -2
    {"seq": [10, 8,  "__", 4,  2],   "ans": 6,  "opts": [5,  6,  7],  "rule": "-2"},
    {"seq": [20, 18, 16, "__",12],   "ans": 14, "opts": [13, 14, 15], "rule": "-2"},
    # +4
    {"seq": [4,  8,  12, 16, "__"],  "ans": 20, "opts": [18, 20, 22], "rule": "+4"},
]

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE BOOTSTRAP
# ──────────────────────────────────────────────────────────────────────────────

_STATE_DEFAULTS = {
    # Global
    "total_stars": 0,
    "tab_scores": {"english": 0, "geo": 0, "math": 0},
    # Geo — API country data (populated by init_state)
    "countries": None, "api_error": "",
    # English — Word Match
    "wm_word": None, "wm_opts": [], "wm_score": 0,
    "wm_lives": 3, "wm_level": "easy", "wm_feedback": None, "wm_q": 0,
    # English — Listen & Spell
    "ls_item": None, "ls_opts": [], "ls_score": 0,
    "ls_hint": False, "ls_feedback": None,
    # English — Sentence Builder
    "sb_sentence": None, "sb_opts": [], "sb_score": 0, "sb_feedback": None,
    # Geo — World Spotter map state
    "geo_markers": [],
    "geo_zoom_lat": 20.0, "geo_zoom_lon": 0.0, "geo_zoom_scale": 1.0,
    # Geo — Flag Finder
    "ff_country": None, "ff_score": 0, "ff_feedback": None, "ff_answered": False,
    # Geo — Capital Challenge
    "cc_country": None, "cc_opts": [], "cc_score": 0,
    "cc_streak": 0, "cc_hard": False, "cc_feedback": None, "cc_answered": False,
    # Geo — Continent Sorter
    "cs_countries": [], "cs_feedback": None, "cs_score": 0,
    # Math — Number Blaster
    "nb_q": None, "nb_ans": 0, "nb_round_score": 0,
    "nb_q_num": 0, "nb_feedback": None, "nb_done": False,
    # Math — Count the Objects
    "co_emoji": None, "co_count": 0, "co_opts": [],
    "co_score": 0, "co_feedback": None,
    # Math — Pattern Puzzle
    "pp_pat": None, "pp_score": 0, "pp_feedback": None,
}


def init_state():
    for k, v in _STATE_DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v.copy() if isinstance(v, dict) else v
    # Fetch country data once per session (uses @st.cache_data internally)
    if st.session_state.countries is None:
        countries, err = load_countries()
        st.session_state.countries = countries
        st.session_state.api_error = err


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def add_stars(n: int, tab: str):
    st.session_state.total_stars += n
    st.session_state.tab_scores[tab] += n


def get_badge() -> str:
    s = st.session_state.total_stars
    if s >= 30: return "🏅 Champion / Champion"
    if s >= 15: return "🌍 Explorateur / Explorer"
    if s >= 5:  return "⭐ Apprenti / Apprentice"
    return "🎮 Debutant / Beginner"


def banner_ok(fr: str, en: str):
    st.markdown(f'<div class="banner-ok">✅ {fr}<br>✅ {en}</div>', unsafe_allow_html=True)


def banner_err(fr: str, en: str):
    st.markdown(f'<div class="banner-err">❌ {fr}<br>❌ {en}</div>', unsafe_allow_html=True)


def show_feedback(feedback):
    """Render stored (type, fr, en) feedback tuple if present."""
    if not feedback:
        return
    kind, fr, en = feedback
    if kind == "ok":
        banner_ok(fr, en)
    else:
        banner_err(fr, en)


# ──────────────────────────────────────────────────────────────────────────────
# ════════════════════  TAB 1 — ENGLISH QUEST  ════════════════════
# ──────────────────────────────────────────────────────────────────────────────

# ── Game A · Word Match ───────────────────────────────────────────────────────

def _load_wm():
    pool = [w for w in WORD_PAIRS if w["lvl"] == st.session_state.wm_level]
    word = random.choice(pool)
    wrongs = random.sample([w for w in WORD_PAIRS if w["fr"] != word["fr"]], 3)
    opts = [w["fr"] for w in wrongs] + [word["fr"]]
    random.shuffle(opts)
    st.session_state.wm_word = word
    st.session_state.wm_opts = opts
    st.session_state.wm_q   += 1


def game_word_match():
    st.markdown("### 🔤 Word Match — Trouve la traduction! / Find the translation!")
    st.markdown(
        '<div class="banner-info">🇬🇧 Lis le mot anglais et clique sur la bonne traduction française!<br>'
        '🇬🇧 Read the English word and click the correct French translation!</div>',
        unsafe_allow_html=True,
    )

    # Level selector — radio stored in session_state automatically via key
    lvl = st.radio("🎯 Niveau / Level:", ["easy", "medium"], horizontal=True, key="_wm_lvl_radio")
    if lvl != st.session_state.wm_level:
        st.session_state.wm_level = lvl
        st.session_state.wm_lives = 3
        st.session_state.wm_score = 0
        st.session_state.wm_feedback = None
        _load_wm()
        st.rerun()

    if st.session_state.wm_word is None:
        _load_wm()

    col_l, col_r = st.columns([3, 1])
    with col_l:
        lives = "❤️" * st.session_state.wm_lives + "🖤" * (3 - st.session_state.wm_lives)
        st.markdown(f'<div style="font-size:2em; text-align:center;">{lives}</div>', unsafe_allow_html=True)
    with col_r:
        st.markdown(f'<div class="score-line">⭐ {st.session_state.wm_score}</div>', unsafe_allow_html=True)

    if st.session_state.wm_lives <= 0:
        st.markdown(
            '<div class="banner-err">😢 Partie terminee! / Game Over!<br>'
            'Clique pour recommencer / Click to restart</div>',
            unsafe_allow_html=True,
        )
        if st.button("🔄 Recommencer / Restart", key="wm_restart"):
            st.session_state.wm_lives = 3
            st.session_state.wm_score = 0
            st.session_state.wm_feedback = None
            _load_wm()
            st.rerun()
        return

    w = st.session_state.wm_word
    st.markdown(
        f'<div class="q-card">'
        f'{w["emoji"]}<br>'
        f'<span style="color:#FF6B35; font-size:1.1em;">{w["en"]}</span><br>'
        f'<span style="font-size:0.45em; color:#999;">Que veut dire ce mot? / What does this word mean?</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    q = st.session_state.wm_q
    for i, opt in enumerate(st.session_state.wm_opts):
        with cols[i % 2]:
            if st.button(f"🔤 {opt}", key=f"wm_{q}_{i}", use_container_width=True):
                if opt == w["fr"]:
                    st.session_state.wm_score += 1
                    add_stars(1, "english")
                    st.session_state.wm_feedback = ("ok",
                        f"Bravo! '{w['en']}' = {w['fr']} {w['emoji']}",
                        f"Well done! '{w['en']}' = {w['fr']} {w['emoji']}")
                    if st.session_state.wm_score == 5 and lvl == "easy":
                        st.session_state.wm_feedback = ("ok",
                            "Super! Niveau suivant debloque! 🎉",
                            "Amazing! Next level unlocked! 🎉")
                        st.session_state.wm_level = "medium"
                    _load_wm()
                    st.balloons()
                else:
                    st.session_state.wm_lives -= 1
                    st.session_state.wm_feedback = ("err",
                        f"Pas tout à fait! La reponse: {w['fr']}",
                        f"Not quite! The answer: {w['fr']}")
                    _load_wm()
                st.rerun()

    show_feedback(st.session_state.wm_feedback)


# ── Game B · Listen & Spell ───────────────────────────────────────────────────

def _load_ls():
    item = random.choice(SPELL_ITEMS)
    opts = item["opts"].copy()
    random.shuffle(opts)
    st.session_state.ls_item  = item
    st.session_state.ls_opts  = opts
    st.session_state.ls_hint  = False


def game_listen_spell():
    st.markdown("### 🎧 Listen & Spell — Devine le mot! / Guess the word!")
    st.markdown(
        '<div class="banner-info">👀 Regarde l\'image et choisis le bon mot anglais!<br>'
        '👀 Look at the image and choose the correct English word!</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.ls_item is None:
        _load_ls()

    item = st.session_state.ls_item

    col_s, _ = st.columns([3, 1])
    with col_s:
        st.markdown(f'<div class="score-line">⭐ Score: {st.session_state.ls_score}</div>',
                    unsafe_allow_html=True)

    st.markdown(
        f'<div class="q-card" style="font-size:3em;">'
        f'{item["emoji"]}<br>'
        f'<span style="font-size:0.3em; color:#999;">Quel est ce mot? / What is this word?</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.ls_hint:
        hint = item["name"][0] + " _ " * (len(item["name"]) - 1)
        st.markdown(
            f'<div style="text-align:center; font-size:1.4em; color:#FF6B35;">💡 Indice / Hint: {hint}</div>',
            unsafe_allow_html=True,
        )

    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.ls_opts):
        with cols[i % 2]:
            if st.button(f"📝 {opt}", key=f"ls_{id(item)}_{i}", use_container_width=True):
                if opt == item["name"]:
                    st.session_state.ls_score += 1
                    add_stars(1, "english")
                    st.session_state.ls_feedback = ("ok",
                        f"Excellent! C'est '{item['name']}'! {item['emoji']}",
                        f"Excellent! It is '{item['name']}'! {item['emoji']}")
                    _load_ls()
                    st.balloons()
                else:
                    st.session_state.ls_hint = True
                    st.session_state.ls_feedback = ("err",
                        "Essaie encore! Regarde l'indice ci-dessus!",
                        "Try again! Look at the hint above!")
                st.rerun()

    show_feedback(st.session_state.ls_feedback)


# ── Game C · Sentence Builder ─────────────────────────────────────────────────

def _load_sb():
    s = random.choice(SENTENCES)
    opts = s["opts"].copy()
    random.shuffle(opts)
    st.session_state.sb_sentence = s
    st.session_state.sb_opts     = opts


def game_sentence_builder():
    st.markdown("### 📝 Sentence Builder — Complete la phrase! / Complete the sentence!")
    st.markdown(
        '<div class="banner-info">🔍 Choisis le mot qui manque! / Pick the missing word!</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.sb_sentence is None:
        _load_sb()

    s = st.session_state.sb_sentence

    st.markdown(f'<div class="score-line">⭐ Score: {st.session_state.sb_score}</div>',
                unsafe_allow_html=True)

    # Build sentence display with blank slot highlighted
    parts = []
    for i, w in enumerate(s["words"]):
        if i == s["blank"]:
            parts.append(
                '<span style="color:#FF6B35; background:#FFE5D9; '
                'padding:2px 12px; border-radius:10px; font-size:1.1em;">___</span>'
            )
        else:
            parts.append(w)
    display = " ".join(parts)

    st.markdown(
        f'<div class="q-card">'
        f'🔤 {display}<br>'
        f'<span style="font-size:0.4em; color:#888;">🇫🇷 {s["fr"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for i, opt in enumerate(st.session_state.sb_opts):
        with cols[i]:
            if st.button(f"📖 {opt}", key=f"sb_{id(s)}_{i}", use_container_width=True):
                correct = s["words"][s["blank"]]
                if opt == correct:
                    st.session_state.sb_score += 1
                    add_stars(1, "english")
                    st.session_state.sb_feedback = ("ok",
                        f"Parfait! Le mot est '{correct}'!",
                        f"Perfect! The word is '{correct}'!")
                    _load_sb()
                    st.balloons()
                else:
                    st.session_state.sb_feedback = ("err",
                        f"Non! Le bon mot: '{correct}'",
                        f"No! The right word: '{correct}'")
                    _load_sb()
                st.rerun()

    show_feedback(st.session_state.sb_feedback)


# ──────────────────────────────────────────────────────────────────────────────
# ════════════════════  TAB 2 — GEO EXPLORER  ════════════════════
# ──────────────────────────────────────────────────────────────────────────────

# ── Map helpers ───────────────────────────────────────────────────────────────

def _set_map_country(country: dict, color: str = "#FFD93D",
                     show_capital: bool = False):
    """Place a single country star on the map, zoom to its region.

    country — unified dict with keys: name_en, lat, lon, capital, region
    """
    lat, lon = country.get("lat"), country.get("lon")
    if lat is None or lon is None:
        return

    markers = [{
        "lat": lat, "lon": lon,
        "color": color, "size": 20, "symbol": "star",
        "label": country["name_en"], "is_cap": False,
    }]

    # Capital pin uses CAPITAL_COORDS if available, otherwise approximates country centre
    if show_capital and country.get("capital"):
        cap_name = country["capital"]
        cap_coords = CAPITAL_COORDS.get(country["name_en"])
        cap_lat = cap_coords[0] if cap_coords else lat + 0.4
        cap_lon = cap_coords[1] if cap_coords else lon + 0.4
        markers.append({
            "lat": cap_lat, "lon": cap_lon,
            "color": "#FFD93D", "size": 14, "symbol": "diamond",
            "label": f"🏛 {cap_name}", "is_cap": True,
        })

    st.session_state.geo_markers = markers

    region = country.get("region", "")
    if region in REGION_ZOOM:
        zlat, zlon, zsc = REGION_ZOOM[region]
        st.session_state.geo_zoom_lat   = lat * 0.55 + zlat * 0.45
        st.session_state.geo_zoom_lon   = lon * 0.55 + zlon * 0.45
        st.session_state.geo_zoom_scale = zsc
    else:
        st.session_state.geo_zoom_lat   = lat
        st.session_state.geo_zoom_lon   = lon
        st.session_state.geo_zoom_scale = 3.0


def _set_map_countries(country_result_pairs: list):
    """Place multiple color-coded country markers (Continent Sorter CHECK).

    country_result_pairs: list of (country_dict, is_correct)
    """
    markers = []
    for country, ok in country_result_pairs:
        lat, lon = country.get("lat"), country.get("lon")
        if lat is None or lon is None:
            continue
        markers.append({
            "lat": lat, "lon": lon,
            "color": "#2ecc71" if ok else "#e74c3c",
            "size": 18, "symbol": "star",
            "label": country["name_en"], "is_cap": False,
        })
    st.session_state.geo_markers    = markers
    st.session_state.geo_zoom_lat   = 20.0
    st.session_state.geo_zoom_lon   = 0.0
    st.session_state.geo_zoom_scale = 1.0


def render_world_map():
    """Render the persistent World Spotter Plotly map at the top of the Geo tab."""
    markers   = st.session_state.get("geo_markers", [])
    zoom_lat  = st.session_state.get("geo_zoom_lat",   20.0)
    zoom_lon  = st.session_state.get("geo_zoom_lon",    0.0)
    zoom_sc   = st.session_state.get("geo_zoom_scale",  1.0)

    fig = go.Figure()

    country_m = [m for m in markers if not m.get("is_cap")]
    capital_m = [m for m in markers if     m.get("is_cap")]

    if country_m:
        fig.add_trace(go.Scattergeo(
            lat=[m["lat"]   for m in country_m],
            lon=[m["lon"]   for m in country_m],
            text=[m["label"] for m in country_m],
            mode="markers+text",
            marker=dict(
                size=[m["size"]  for m in country_m],
                symbol="star",
                color=[m["color"] for m in country_m],
                line=dict(width=2, color="white"),
            ),
            textposition="bottom center",
            textfont=dict(size=11, color="white"),
            hoverinfo="text",
            showlegend=False,
        ))

    if capital_m:
        fig.add_trace(go.Scattergeo(
            lat=[m["lat"]   for m in capital_m],
            lon=[m["lon"]   for m in capital_m],
            text=[m["label"] for m in capital_m],
            mode="markers+text",
            marker=dict(
                size=[m["size"]  for m in capital_m],
                symbol="diamond",
                color=[m["color"] for m in capital_m],
                line=dict(width=2, color="white"),
            ),
            textposition="top center",
            textfont=dict(size=10, color="#FFD93D"),
            hoverinfo="text",
            showlegend=False,
        ))

    fig.update_layout(
        height=370,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#1a1a2e",
        geo=dict(
            projection=dict(type="natural earth", scale=zoom_sc),
            center=dict(lat=zoom_lat, lon=zoom_lon),
            bgcolor="#1a1a2e",
            landcolor="#e8f4f8",
            oceancolor="#1a1a2e",
            showocean=True,
            showland=True,
            showlakes=False,
            showcountries=True,
            countrycolor="#8899aa",
            countrywidth=0.5,
            showcoastlines=True,
            coastlinecolor="#8899aa",
            coastlinewidth=0.5,
        ),
        font=dict(color="white"),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── Game A · Flag Finder ──────────────────────────────────────────────────────

def _load_ff():
    countries = st.session_state.countries or FALLBACK_COUNTRIES
    c = random.choice(countries)
    st.session_state.ff_country  = c
    st.session_state.ff_answered = False
    _set_map_country(c, color="#FFD93D")


def game_flag_finder():
    st.markdown("### 🏳️ Flag Finder — A quel continent? / Which continent?")
    st.markdown(
        '<div class="banner-info">🌍 Quel continent pour ce drapeau? / Which continent for this flag?</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.ff_country is None:
        _load_ff()

    c = st.session_state.ff_country

    st.markdown(f'<div class="score-line">⭐ Score: {st.session_state.ff_score}</div>',
                unsafe_allow_html=True)

    # Large flag — 80 px per spec
    st.markdown(
        f'<div style="text-align:center; font-size:80px; line-height:1.1; margin:10px 0;">'
        f'{c["flag_emoji"]}</div>'
        f'<div style="text-align:center; font-size:1.3em; font-family:Fredoka One,cursive; '
        f'color:#4ECDC4; margin-bottom:14px;">{c["name_en"]} / {c["name_fr"]}</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.ff_answered:
        show_feedback(st.session_state.ff_feedback)
        if st.button("▶️ Suivant / Next", key="ff_next", use_container_width=True):
            _load_ff()
            st.rerun()
        return

    # Build region buttons dynamically from loaded data
    countries    = st.session_state.countries or FALLBACK_COUNTRIES
    all_regions  = sorted({cc["region"] for cc in countries if cc.get("region")})
    cols = st.columns(min(3, len(all_regions)))
    for i, region in enumerate(all_regions):
        label = REGION_LABELS.get(region, region)
        with cols[i % len(cols)]:
            if st.button(label, key=f"ff_{c['name_en']}_{region}", use_container_width=True):
                if region == c["region"]:
                    st.session_state.ff_score += 1
                    add_stars(1, "geo")
                    _set_map_country(c, color="#2ecc71")
                    st.session_state.ff_feedback = ("ok",
                        f"Oui! {c['name_en']} est en {REGION_LABELS.get(region, region)}!",
                        f"Yes! {c['name_en']} is in {region}!")
                    st.session_state.ff_answered = True
                    st.balloons()
                else:
                    _set_map_country(c, color="#e74c3c")
                    correct_label = REGION_LABELS.get(c["region"], c["region"])
                    st.session_state.ff_feedback = ("err",
                        f"Non! {c['name_en']} est en {correct_label}!",
                        f"No! {c['name_en']} is in {c['region']}!")
                    st.session_state.ff_answered = True
                st.rerun()


# ── Game B · Capital City Challenge ──────────────────────────────────────────

def _load_cc():
    countries = st.session_state.countries or FALLBACK_COUNTRIES
    pool = (
        countries if st.session_state.cc_hard
        else [c for c in countries if c["name_en"] in EASY_CAPITAL_NAMES]
    ) or countries
    country  = random.choice(pool)
    all_caps = [c["capital"] for c in countries if c.get("capital") and c["capital"] != "?"]
    wrongs   = random.sample([cap for cap in all_caps if cap != country["capital"]], min(3, len(all_caps) - 1))
    opts = wrongs + [country["capital"]]
    random.shuffle(opts)
    st.session_state.cc_country  = country
    st.session_state.cc_opts     = opts
    st.session_state.cc_answered = False
    _set_map_country(country, color="#FFD93D", show_capital=True)


def game_capital_challenge():
    st.markdown("### 🏛️ Capital Challenge — Quelle est la capitale? / What is the capital?")

    if st.session_state.cc_country is None:
        _load_cc()

    c = st.session_state.cc_country

    col_sc, col_str = st.columns(2)
    with col_sc:
        st.markdown(f'<div class="score-line">⭐ Score: {st.session_state.cc_score}</div>',
                    unsafe_allow_html=True)
    with col_str:
        flames = "🔥" * min(st.session_state.cc_streak, 5)
        st.markdown(
            f'<div class="score-line" style="text-align:left;">'
            f'Serie / Streak: {flames} ({st.session_state.cc_streak})</div>',
            unsafe_allow_html=True,
        )

    if st.session_state.cc_hard:
        st.markdown(
            '<div style="text-align:center; color:#4ECDC4; font-size:1.1em;">'
            '🔓 Mode Expert / Expert Mode!</div>',
            unsafe_allow_html=True,
        )

    pop = c.get("population", 0)
    pop_str = f"{pop:,}" if pop else "?"
    st.markdown(
        f'<div class="q-card q-card-teal">'
        f'{c["flag_emoji"]}<br>'
        f'<span style="color:#4ECDC4; font-size:0.7em;">{c["name_en"]} / {c["name_fr"]}</span><br>'
        f'<span style="font-size:0.35em; color:#4ECDC4;">🧑‍🤝‍🧑 Population: {pop_str}</span><br>'
        f'<span style="font-size:0.4em; color:#999;">'
        f'Quelle est la capitale? / What is the capital?</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.cc_answered:
        show_feedback(st.session_state.cc_feedback)
        if st.button("▶️ Suivant / Next", key="cc_next", use_container_width=True):
            _load_cc()
            st.rerun()
        return

    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.cc_opts):
        with cols[i % 2]:
            if st.button(f"🏛️ {opt}", key=f"cc_{c['name_en']}_{i}", use_container_width=True):
                if opt == c["capital"]:
                    st.session_state.cc_score  += 1
                    st.session_state.cc_streak += 1
                    add_stars(1, "geo")
                    _set_map_country(c, color="#2ecc71", show_capital=True)
                    if st.session_state.cc_streak >= 5 and not st.session_state.cc_hard:
                        st.session_state.cc_hard = True
                        st.session_state.cc_feedback = ("ok",
                            "🔓 Mode Expert debloque! Serie de 5!",
                            "🔓 Expert Mode Unlocked! 5 in a row!")
                    else:
                        st.session_state.cc_feedback = ("ok",
                            f"Correct! {c['name_en']} → {c['capital']}!",
                            f"Correct! {c['name_en']} → {c['capital']}!")
                    st.session_state.cc_answered = True
                    st.balloons()
                else:
                    _set_map_country(c, color="#e74c3c", show_capital=True)
                    st.session_state.cc_streak  = 0
                    st.session_state.cc_feedback = ("err",
                        f"Non! La capitale: {c['capital']}",
                        f"No! The capital: {c['capital']}")
                    st.session_state.cc_answered = True
                st.rerun()


# ── Game C · Continent Sorter ─────────────────────────────────────────────────

def _load_cs():
    countries = st.session_state.countries or FALLBACK_COUNTRIES
    pool = [c for c in countries if c.get("lat") is not None]
    st.session_state.cs_countries = random.sample(pool, min(5, len(pool)))
    st.session_state.cs_feedback  = None
    # Yellow markers for all 5 on the global view
    markers = []
    for c in st.session_state.cs_countries:
        if c.get("lat") is not None:
            markers.append({"lat": c["lat"], "lon": c["lon"],
                            "color": "#FFD93D", "size": 18, "symbol": "star",
                            "label": c["name_en"], "is_cap": False})
    st.session_state.geo_markers    = markers
    st.session_state.geo_zoom_lat   = 20.0
    st.session_state.geo_zoom_lon   = 0.0
    st.session_state.geo_zoom_scale = 1.0


def game_continent_sorter():
    st.markdown("### 🗺️ Continent Sorter — Trie les pays! / Sort the countries!")
    st.markdown(
        '<div class="banner-info">'
        '🌍 Assigne chaque pays a son continent, puis clique CHECK!<br>'
        '🌍 Assign each country to its continent, then click CHECK!'
        '</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.cs_countries:
        _load_cs()

    countries = st.session_state.cs_countries

    # Build region list dynamically from loaded API data
    all_countries = st.session_state.countries or FALLBACK_COUNTRIES
    region_options = sorted({cc["region"] for cc in all_countries if cc.get("region")})

    st.markdown(f'<div class="score-line">⭐ Score total: {st.session_state.cs_score}</div>',
                unsafe_allow_html=True)

    for country in countries:
        c1, c2, c3 = st.columns([1, 2, 3])
        with c1:
            st.markdown(
                f'<div style="font-size:2.2em; text-align:center;">{country["flag_emoji"]}</div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div style="font-size:1.05em; font-family:Fredoka One,cursive; padding-top:8px;">'
                f'{country["name_en"]}<br>'
                f'<span style="color:#999; font-size:0.85em;">{country["name_fr"]}</span></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.selectbox(
                f"Continent — {country['name_en']}",
                region_options,
                key=f"cs_{country['name_en']}",
                label_visibility="collapsed",
            )

    st.markdown("<br>", unsafe_allow_html=True)
    col_check, col_new = st.columns(2)

    with col_check:
        if st.button("🚀 CHECK / VERIFIER", key="cs_check", use_container_width=True):
            results, correct_count = [], 0
            for country in countries:
                user_ans = st.session_state.get(f"cs_{country['name_en']}", region_options[0] if region_options else "")
                right    = country["region"]
                ok       = user_ans == right
                if ok:
                    correct_count += 1
                results.append((country["name_en"], country["flag_emoji"], user_ans, right, ok, country))
            add_stars(correct_count, "geo")
            st.session_state.cs_score   += correct_count
            st.session_state.cs_feedback = results
            _set_map_countries([(row[5], row[4]) for row in results])
            if correct_count == 5:
                st.balloons()
            st.rerun()

    with col_new:
        if st.button("🔄 Nouveau round / New Round", key="cs_new", use_container_width=True):
            _load_cs()
            st.rerun()

    if st.session_state.cs_feedback:
        st.markdown("---")
        for name, flag, user_ans, right, ok, _ in st.session_state.cs_feedback:
            right_label = REGION_LABELS.get(right, right)
            user_label  = REGION_LABELS.get(user_ans, user_ans)
            if ok:
                st.markdown(
                    f'<div class="fb-ok">✅ {flag} {name} → {right_label}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="fb-err">❌ {flag} {name} — '
                    f'Tu as dit / You said: {user_label} &nbsp;|&nbsp; '
                    f'✅ {right_label}</div>',
                    unsafe_allow_html=True,
                )


# ──────────────────────────────────────────────────────────────────────────────
# ════════════════════  TAB 3 — MATH ARENA  ════════════════════
# ──────────────────────────────────────────────────────────────────────────────

# ── Game A · Number Blaster ───────────────────────────────────────────────────

def _load_nb():
    op = random.choice(["+", "-"])
    if op == "+":
        a = random.randint(1, 15)
        b = random.randint(1, 20 - a)
        ans = a + b
        question = f"{a}  +  {b}  =  ?"
    else:
        a = random.randint(2, 20)
        b = random.randint(1, a)
        ans = a - b
        question = f"{a}  −  {b}  =  ?"
    st.session_state.nb_q   = question
    st.session_state.nb_ans = ans


def game_number_blaster():
    st.markdown("### 💥 Number Blaster — Calcule vite! / Calculate fast!")

    if st.session_state.nb_done:
        # Round summary
        s = st.session_state.nb_round_score
        stars = "⭐⭐⭐" if s >= 9 else "⭐⭐" if s >= 6 else "⭐"
        st.markdown(
            f'<div class="banner-ok">'
            f'🎉 Round termine! / Round Complete!<br>'
            f'Score: {s}/10  {stars}'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button("🔄 Nouveau round / New Round", key="nb_restart"):
            st.session_state.nb_q_num       = 0
            st.session_state.nb_round_score = 0
            st.session_state.nb_done        = False
            st.session_state.nb_feedback    = None
            _load_nb()
            st.rerun()
        return

    if st.session_state.nb_q is None:
        _load_nb()

    q_num = st.session_state.nb_q_num
    st.progress((q_num) / 10, text=f"Question {q_num + 1} / 10")

    col_sc, col_prog = st.columns([1, 2])
    with col_sc:
        st.markdown(f'<div class="score-line">✅ {st.session_state.nb_round_score}/10</div>',
                    unsafe_allow_html=True)

    st.markdown(
        f'<div class="q-card q-card-green" style="font-size:2.5em;">'
        f'🔢 {st.session_state.nb_q}'
        f'</div>',
        unsafe_allow_html=True,
    )

    col_in, col_btn = st.columns([2, 1])
    with col_in:
        user_val = st.number_input(
            "Ta reponse / Your answer:",
            min_value=0, max_value=40, value=0, step=1,
            key=f"nb_input_{q_num}",
        )
    with col_btn:
        st.write("")
        st.write("")
        if st.button("✅ OK", key=f"nb_ok_{q_num}", use_container_width=True):
            correct = st.session_state.nb_ans
            if int(user_val) == correct:
                st.session_state.nb_round_score += 1
                add_stars(1, "math")
                st.session_state.nb_feedback = ("ok", "Correct! 🎉", "Correct! 🎉")
            else:
                st.session_state.nb_feedback = ("err",
                    f"Non! La reponse: {correct}",
                    f"No! The answer: {correct}")
            st.session_state.nb_q_num += 1
            if st.session_state.nb_q_num >= 10:
                st.session_state.nb_done = True
                # Bonus stars for performance
                bonus = 3 if st.session_state.nb_round_score >= 9 else 1 if st.session_state.nb_round_score >= 6 else 0
                if bonus:
                    add_stars(bonus, "math")
            else:
                _load_nb()
            st.rerun()

    show_feedback(st.session_state.nb_feedback)


# ── Game B · Count the Objects ────────────────────────────────────────────────

def _load_co():
    emoji = random.choice(COUNTING_EMOJIS)
    count = random.randint(1, 15)
    wrong = set()
    while len(wrong) < 3:
        w = random.randint(max(1, count - 4), min(15, count + 4))
        if w != count:
            wrong.add(w)
    opts = list(wrong) + [count]
    random.shuffle(opts)
    st.session_state.co_emoji = emoji
    st.session_state.co_count = count
    st.session_state.co_opts  = opts


def game_count_objects():
    st.markdown("### 🔢 Count the Objects — Compte les objets! / Count the objects!")
    st.markdown(
        '<div class="banner-info-green">🍎 Compte bien tous les objets! / Count all the objects carefully!</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.co_emoji is None:
        _load_co()

    emoji = st.session_state.co_emoji
    count = st.session_state.co_count

    st.markdown(f'<div class="score-line">⭐ Score: {st.session_state.co_score}</div>',
                unsafe_allow_html=True)

    # Render objects in a wrapped block, spaced for readability
    items_html = "&nbsp;&nbsp;".join([emoji] * count)
    st.markdown(
        f'<div class="q-card q-card-green" '
        f'style="font-size:2em; word-break:break-all; line-height:1.7em;">'
        f'{items_html}'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="text-align:center; font-size:1.15em; font-family:Fredoka One,cursive;">'
        'Combien y en a-t-il? / How many are there?'
        '</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    for i, opt in enumerate(st.session_state.co_opts):
        with cols[i]:
            if st.button(f"**{opt}**", key=f"co_{count}_{emoji}_{i}", use_container_width=True):
                if opt == count:
                    st.session_state.co_score += 1
                    add_stars(1, "math")
                    st.session_state.co_feedback = ("ok",
                        f"Oui! Il y en a {count}! {emoji * 3}",
                        f"Yes! There are {count}! {emoji * 3}")
                    _load_co()
                    st.balloons()
                else:
                    st.session_state.co_feedback = ("err",
                        f"Non! Il y en avait {count}!",
                        f"No! There were {count}!")
                    _load_co()
                st.rerun()

    show_feedback(st.session_state.co_feedback)


# ── Game C · Pattern Puzzle ───────────────────────────────────────────────────

def _load_pp():
    st.session_state.pp_pat = random.choice(PATTERNS)


def game_pattern_puzzle():
    st.markdown("### 🧩 Pattern Puzzle — Trouve le nombre manquant! / Find the missing number!")
    st.markdown(
        '<div class="banner-info-green">🔍 Quelle est la regle de la suite? / What is the pattern rule?</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.pp_pat is None:
        _load_pp()

    pat = st.session_state.pp_pat

    st.markdown(f'<div class="score-line">⭐ Score: {st.session_state.pp_score}</div>',
                unsafe_allow_html=True)

    # Build sequence display
    parts = []
    for val in pat["seq"]:
        if val == "__":
            parts.append(
                '<span style="color:#FF6B35; background:#FFE5D9; '
                'padding:3px 14px; border-radius:12px; font-size:1.1em;">  ?  </span>'
            )
        else:
            parts.append(f'<span style="color:#2C3E50;">{val}</span>')
    seq_html = '<span style="color:#999; font-size:0.7em;"> , </span>'.join(parts)

    st.markdown(
        f'<div class="q-card q-card-green" style="font-size:1.8em; letter-spacing:0.04em;">'
        f'🔢 {seq_html}'
        f'</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for i, opt in enumerate(pat["opts"]):
        with cols[i]:
            if st.button(f"**{opt}**", key=f"pp_{pat['ans']}_{i}", use_container_width=True):
                if opt == pat["ans"]:
                    st.session_state.pp_score += 1
                    add_stars(1, "math")
                    st.session_state.pp_feedback = ("ok",
                        f"Bravo! La reponse est {pat['ans']}! (regle: {pat['rule']})",
                        f"Great job! The answer is {pat['ans']}! (rule: {pat['rule']})")
                    _load_pp()
                    st.balloons()
                else:
                    st.session_state.pp_feedback = ("err",
                        f"Non! La reponse: {pat['ans']} (regle: {pat['rule']})",
                        f"No! The answer: {pat['ans']} (rule: {pat['rule']})")
                    _load_pp()
                st.rerun()

    show_feedback(st.session_state.pp_feedback)


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR — GLOBAL GAMIFICATION DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div style="text-align:center; font-size:2em; font-family:Fredoka One,cursive; '
            'line-height:1.2; padding:10px 0;">🎓 KidQuest<br>Academy</div>',
            unsafe_allow_html=True,
        )
        st.divider()

        # Total stars
        stars = st.session_state.total_stars
        st.markdown(
            f'<div class="sb-card">'
            f'🌟 Etoiles / Stars<br>'
            f'<span style="font-size:2.2em;">{stars} ⭐</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Badge
        badge = get_badge()
        st.markdown(
            f'<div class="sb-card" style="background:linear-gradient(135deg,#f093fb,#f5576c);">'
            f'{badge}'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Per-tab scores
        st.markdown(
            '<div style="font-size:1.1em; font-family:Fredoka One,cursive; margin-bottom:6px;">'
            '📊 Scores par onglet / Per Tab</div>',
            unsafe_allow_html=True,
        )
        tab_info = [
            ("🦊 English", "english", "#FF6B35"),
            ("🌍 Geo",     "geo",     "#4ECDC4"),
            ("🔢 Maths",   "math",    "#A8E6CF"),
        ]
        for label, key, color in tab_info:
            sc = st.session_state.tab_scores[key]
            st.markdown(
                f'<div class="sb-tab" style="background:{color}30; border-left:5px solid {color};">'
                f'{label}: <strong>{sc} pts</strong></div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # Badge progress bar
        st.markdown(
            '<div style="font-size:1.05em; font-family:Fredoka One,cursive; margin-bottom:4px;">'
            '🏅 Prochain badge / Next badge</div>',
            unsafe_allow_html=True,
        )
        thresholds = [5, 15, 30]
        nxt = next((t for t in thresholds if t > stars), None)
        if nxt:
            st.progress(min(stars / nxt, 1.0), text=f"{stars} / {nxt} ⭐")
        else:
            st.markdown("🏆 Maximum atteint! / Maximum reached!")

        st.divider()

        if st.button("🔄 Tout reinitialiser / Reset All", key="global_reset"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        # API error diagnostic (collapsible, only shown when non-empty)
        api_err = st.session_state.get("api_error", "")
        if api_err:
            with st.expander("⚠️ API Info / Diagnostic", expanded=False):
                st.caption(
                    "Les données pays utilisent le mode hors-ligne.\n"
                    "Country data is using offline fallback."
                )
                st.code(api_err, language=None)


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    inject_css()
    init_state()
    render_sidebar()

    st.markdown('<div class="kq-title">🎓 KidQuest Academy</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="kq-subtitle">Apprends en t\'amusant! / Learn while having fun! 🌟</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🦊 English Quest", "🌍 Geo Explorer", "🔢 Math Arena"])

    # ── Tab 1 ──
    with tab1:
        st.markdown(
            '<div class="tab-header-orange">'
            '🦊 English Quest — Apprends l\'anglais! / Learn English!'
            '</div>',
            unsafe_allow_html=True,
        )
        game = st.radio(
            "🎮 Choisis un jeu / Choose a game:",
            ["🔤 Word Match", "🎧 Listen & Spell", "📝 Sentence Builder"],
            horizontal=True,
            key="eng_game",
        )
        st.divider()
        if game == "🔤 Word Match":
            game_word_match()
        elif game == "🎧 Listen & Spell":
            game_listen_spell()
        else:
            game_sentence_builder()

    # ── Tab 2 ──
    with tab2:
        st.markdown(
            '<div class="tab-header-teal">'
            '🌍 Geo Explorer — Explore le monde! / Explore the world!'
            '</div>',
            unsafe_allow_html=True,
        )
        # ── Persistent World Spotter map — always rendered first ──
        render_world_map()

        game = st.radio(
            "🎮 Choisis un jeu / Choose a game:",
            ["🏳️ Flag Finder", "🏛️ Capital Challenge", "🗺️ Continent Sorter"],
            horizontal=True,
            key="geo_game",
        )
        st.divider()
        if game == "🏳️ Flag Finder":
            game_flag_finder()
        elif game == "🏛️ Capital Challenge":
            game_capital_challenge()
        else:
            game_continent_sorter()

    # ── Tab 3 ──
    with tab3:
        st.markdown(
            '<div class="tab-header-green">'
            '🔢 Math Arena — Maitrise les maths! / Master math!'
            '</div>',
            unsafe_allow_html=True,
        )
        game = st.radio(
            "🎮 Choisis un jeu / Choose a game:",
            ["💥 Number Blaster", "🔢 Count the Objects", "🧩 Pattern Puzzle"],
            horizontal=True,
            key="math_game",
        )
        st.divider()
        if game == "💥 Number Blaster":
            game_number_blaster()
        elif game == "🔢 Count the Objects":
            game_count_objects()
        else:
            game_pattern_puzzle()


if __name__ == "__main__":
    main()
