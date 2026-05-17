"""
KidQuest Academy — Gamified Learning Platform for Children (ages 4–7)
3 subject tabs: English Quest, Geo Explorer, Math Arena
Fully bilingual FR/EN — no external APIs — single-file Streamlit app
"""

import streamlit as st
import random
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

# ── Tab 2 · Geo Explorer ──────────────────────────────────────────────────────

CONTINENTS = ["Europe", "Asia", "Americas", "Africa", "Oceania"]

CONTINENT_EMOJI = {
    "Europe":   "🏰",
    "Asia":     "🏯",
    "Americas": "🌎",
    "Africa":   "🦒",
    "Oceania":  "🦘",
}

# 42 countries: flag emoji, English name, French name, continent, capital
COUNTRIES = [
    # ── Europe (12) ──
    {"flag":"🇫🇷","en":"France",          "fr":"France",             "cont":"Europe",   "cap":"Paris"},
    {"flag":"🇩🇪","en":"Germany",         "fr":"Allemagne",          "cont":"Europe",   "cap":"Berlin"},
    {"flag":"🇮🇹","en":"Italy",           "fr":"Italie",             "cont":"Europe",   "cap":"Rome"},
    {"flag":"🇪🇸","en":"Spain",           "fr":"Espagne",            "cont":"Europe",   "cap":"Madrid"},
    {"flag":"🇬🇧","en":"United Kingdom",  "fr":"Royaume-Uni",        "cont":"Europe",   "cap":"London"},
    {"flag":"🇵🇹","en":"Portugal",        "fr":"Portugal",           "cont":"Europe",   "cap":"Lisbon"},
    {"flag":"🇳🇱","en":"Netherlands",     "fr":"Pays-Bas",           "cont":"Europe",   "cap":"Amsterdam"},
    {"flag":"🇧🇪","en":"Belgium",         "fr":"Belgique",           "cont":"Europe",   "cap":"Brussels"},
    {"flag":"🇨🇭","en":"Switzerland",     "fr":"Suisse",             "cont":"Europe",   "cap":"Bern"},
    {"flag":"🇸🇪","en":"Sweden",          "fr":"Suede",              "cont":"Europe",   "cap":"Stockholm"},
    {"flag":"🇬🇷","en":"Greece",          "fr":"Grece",              "cont":"Europe",   "cap":"Athens"},
    {"flag":"🇮🇸","en":"Iceland",         "fr":"Islande",            "cont":"Europe",   "cap":"Reykjavik"},
    # ── Asia (12) ──
    {"flag":"🇯🇵","en":"Japan",           "fr":"Japon",              "cont":"Asia",     "cap":"Tokyo"},
    {"flag":"🇨🇳","en":"China",           "fr":"Chine",              "cont":"Asia",     "cap":"Beijing"},
    {"flag":"🇮🇳","en":"India",           "fr":"Inde",               "cont":"Asia",     "cap":"New Delhi"},
    {"flag":"🇰🇷","en":"South Korea",     "fr":"Coree du Sud",       "cont":"Asia",     "cap":"Seoul"},
    {"flag":"🇹🇭","en":"Thailand",        "fr":"Thailande",          "cont":"Asia",     "cap":"Bangkok"},
    {"flag":"🇻🇳","en":"Vietnam",         "fr":"Vietnam",            "cont":"Asia",     "cap":"Hanoi"},
    {"flag":"🇸🇦","en":"Saudi Arabia",    "fr":"Arabie Saoudite",    "cont":"Asia",     "cap":"Riyadh"},
    {"flag":"🇹🇷","en":"Turkey",          "fr":"Turquie",            "cont":"Asia",     "cap":"Ankara"},
    {"flag":"🇵🇭","en":"Philippines",     "fr":"Philippines",        "cont":"Asia",     "cap":"Manila"},
    {"flag":"🇮🇩","en":"Indonesia",       "fr":"Indonesie",          "cont":"Asia",     "cap":"Jakarta"},
    {"flag":"🇮🇷","en":"Iran",            "fr":"Iran",               "cont":"Asia",     "cap":"Tehran"},
    {"flag":"🇦🇫","en":"Afghanistan",     "fr":"Afghanistan",        "cont":"Asia",     "cap":"Kabul"},
    # ── Americas (10) ──
    {"flag":"🇺🇸","en":"United States",   "fr":"Etats-Unis",         "cont":"Americas", "cap":"Washington D.C."},
    {"flag":"🇧🇷","en":"Brazil",          "fr":"Bresil",             "cont":"Americas", "cap":"Brasilia"},
    {"flag":"🇨🇦","en":"Canada",          "fr":"Canada",             "cont":"Americas", "cap":"Ottawa"},
    {"flag":"🇲🇽","en":"Mexico",          "fr":"Mexique",            "cont":"Americas", "cap":"Mexico City"},
    {"flag":"🇦🇷","en":"Argentina",       "fr":"Argentine",          "cont":"Americas", "cap":"Buenos Aires"},
    {"flag":"🇨🇴","en":"Colombia",        "fr":"Colombie",           "cont":"Americas", "cap":"Bogota"},
    {"flag":"🇵🇪","en":"Peru",            "fr":"Perou",              "cont":"Americas", "cap":"Lima"},
    {"flag":"🇨🇱","en":"Chile",           "fr":"Chili",              "cont":"Americas", "cap":"Santiago"},
    {"flag":"🇨🇺","en":"Cuba",            "fr":"Cuba",               "cont":"Americas", "cap":"Havana"},
    {"flag":"🇻🇪","en":"Venezuela",       "fr":"Venezuela",          "cont":"Americas", "cap":"Caracas"},
    # ── Africa (8) ──
    {"flag":"🇿🇦","en":"South Africa",    "fr":"Afrique du Sud",     "cont":"Africa",   "cap":"Cape Town"},
    {"flag":"🇳🇬","en":"Nigeria",         "fr":"Nigeria",            "cont":"Africa",   "cap":"Abuja"},
    {"flag":"🇰🇪","en":"Kenya",           "fr":"Kenya",              "cont":"Africa",   "cap":"Nairobi"},
    {"flag":"🇪🇬","en":"Egypt",           "fr":"Egypte",             "cont":"Africa",   "cap":"Cairo"},
    {"flag":"🇲🇦","en":"Morocco",         "fr":"Maroc",              "cont":"Africa",   "cap":"Rabat"},
    {"flag":"🇬🇭","en":"Ghana",           "fr":"Ghana",              "cont":"Africa",   "cap":"Accra"},
    {"flag":"🇪🇹","en":"Ethiopia",        "fr":"Ethiopie",           "cont":"Africa",   "cap":"Addis Ababa"},
    {"flag":"🇹🇿","en":"Tanzania",        "fr":"Tanzanie",           "cont":"Africa",   "cap":"Dodoma"},
    # ── Oceania (3) ──
    {"flag":"🇦🇺","en":"Australia",       "fr":"Australie",          "cont":"Oceania",  "cap":"Canberra"},
    {"flag":"🇳🇿","en":"New Zealand",     "fr":"Nouvelle-Zelande",   "cont":"Oceania",  "cap":"Wellington"},
    {"flag":"🇫🇯","en":"Fiji",            "fr":"Fidji",              "cont":"Oceania",  "cap":"Suva"},
]

# Subset of well-known countries for Capital Challenge easy mode (first 5 correct answers)
EASY_CAPITALS = {"France","Japan","Brazil","United States","United Kingdom",
                 "Germany","Italy","Spain","Canada","Mexico","Australia","China","India"}

# ── Geographic coordinates for the World Spotter map ─────────────────────────
# Each entry: country lat/lon centre + capital lat/lon
GEO_DATA = {
    # Europe
    "France":         {"lat": 46.23, "lon":   2.21, "cap_lat": 48.86, "cap_lon":   2.35},
    "Germany":        {"lat": 51.17, "lon":  10.45, "cap_lat": 52.52, "cap_lon":  13.40},
    "Italy":          {"lat": 41.87, "lon":  12.57, "cap_lat": 41.90, "cap_lon":  12.50},
    "Spain":          {"lat": 40.46, "lon":  -3.75, "cap_lat": 40.42, "cap_lon":  -3.70},
    "United Kingdom": {"lat": 55.38, "lon":  -3.44, "cap_lat": 51.51, "cap_lon":  -0.13},
    "Portugal":       {"lat": 39.40, "lon":  -8.22, "cap_lat": 38.72, "cap_lon":  -9.14},
    "Netherlands":    {"lat": 52.13, "lon":   5.29, "cap_lat": 52.37, "cap_lon":   4.90},
    "Belgium":        {"lat": 50.50, "lon":   4.47, "cap_lat": 50.85, "cap_lon":   4.35},
    "Switzerland":    {"lat": 46.82, "lon":   8.23, "cap_lat": 46.95, "cap_lon":   7.45},
    "Sweden":         {"lat": 60.13, "lon":  18.64, "cap_lat": 59.33, "cap_lon":  18.07},
    "Greece":         {"lat": 39.07, "lon":  21.82, "cap_lat": 37.98, "cap_lon":  23.73},
    "Iceland":        {"lat": 64.96, "lon": -19.02, "cap_lat": 64.13, "cap_lon": -21.82},
    # Asia
    "Japan":          {"lat": 36.20, "lon": 138.25, "cap_lat": 35.69, "cap_lon": 139.69},
    "China":          {"lat": 35.86, "lon": 104.20, "cap_lat": 39.91, "cap_lon": 116.39},
    "India":          {"lat": 20.59, "lon":  78.96, "cap_lat": 28.61, "cap_lon":  77.21},
    "South Korea":    {"lat": 35.91, "lon": 127.77, "cap_lat": 37.57, "cap_lon": 126.98},
    "Thailand":       {"lat": 15.87, "lon": 100.99, "cap_lat": 13.75, "cap_lon": 100.52},
    "Vietnam":        {"lat": 14.06, "lon": 108.28, "cap_lat": 21.03, "cap_lon": 105.85},
    "Saudi Arabia":   {"lat": 23.89, "lon":  45.08, "cap_lat": 24.69, "cap_lon":  46.72},
    "Turkey":         {"lat": 38.96, "lon":  35.24, "cap_lat": 39.92, "cap_lon":  32.85},
    "Philippines":    {"lat": 12.88, "lon": 121.77, "cap_lat": 14.60, "cap_lon": 120.98},
    "Indonesia":      {"lat":  -0.79,"lon": 113.92, "cap_lat": -6.21, "cap_lon": 106.85},
    "Iran":           {"lat": 32.43, "lon":  53.69, "cap_lat": 35.69, "cap_lon":  51.42},
    "Afghanistan":    {"lat": 33.94, "lon":  67.71, "cap_lat": 34.52, "cap_lon":  69.18},
    # Americas
    "United States":  {"lat": 37.09, "lon": -95.71, "cap_lat": 38.91, "cap_lon": -77.04},
    "Brazil":         {"lat":-14.24, "lon": -51.93, "cap_lat":-15.78, "cap_lon": -47.93},
    "Canada":         {"lat": 56.13, "lon":-106.35, "cap_lat": 45.42, "cap_lon": -75.70},
    "Mexico":         {"lat": 23.63, "lon":-102.55, "cap_lat": 19.43, "cap_lon": -99.13},
    "Argentina":      {"lat":-38.42, "lon": -63.62, "cap_lat":-34.60, "cap_lon": -58.38},
    "Colombia":       {"lat":  4.57, "lon": -74.30, "cap_lat":  4.71, "cap_lon": -74.07},
    "Peru":           {"lat": -9.19, "lon": -75.02, "cap_lat":-12.05, "cap_lon": -77.05},
    "Chile":          {"lat":-35.68, "lon": -71.54, "cap_lat":-33.46, "cap_lon": -70.65},
    "Cuba":           {"lat": 21.52, "lon": -77.78, "cap_lat": 23.11, "cap_lon": -82.37},
    "Venezuela":      {"lat":  6.42, "lon": -66.59, "cap_lat": 10.50, "cap_lon": -66.92},
    # Africa
    "South Africa":   {"lat":-30.56, "lon":  22.94, "cap_lat":-33.93, "cap_lon":  18.42},
    "Nigeria":        {"lat":  9.08, "lon":   8.68, "cap_lat":  9.07, "cap_lon":   7.40},
    "Kenya":          {"lat":  0.02, "lon":  37.91, "cap_lat": -1.29, "cap_lon":  36.82},
    "Egypt":          {"lat": 26.82, "lon":  30.80, "cap_lat": 30.04, "cap_lon":  31.24},
    "Morocco":        {"lat": 31.79, "lon":  -7.09, "cap_lat": 34.02, "cap_lon":  -6.84},
    "Ghana":          {"lat":  7.95, "lon":  -1.02, "cap_lat":  5.56, "cap_lon":  -0.20},
    "Ethiopia":       {"lat":  9.15, "lon":  40.49, "cap_lat":  9.03, "cap_lon":  38.74},
    "Tanzania":       {"lat": -6.37, "lon":  34.89, "cap_lat": -6.18, "cap_lon":  35.74},
    # Oceania
    "Australia":      {"lat":-25.27, "lon": 133.78, "cap_lat":-35.28, "cap_lon": 149.13},
    "New Zealand":    {"lat":-40.90, "lon": 174.89, "cap_lat":-41.29, "cap_lon": 174.78},
    "Fiji":           {"lat":-17.71, "lon": 178.07, "cap_lat":-18.14, "cap_lon": 178.44},
}

# Continent-level zoom: (center_lat, center_lon, projection_scale)
CONTINENT_ZOOM = {
    "Europe":   (54.0,  15.0, 3.0),
    "Asia":     (32.0,  95.0, 1.8),
    "Americas": ( 5.0, -80.0, 1.4),
    "Africa":   ( 5.0,  20.0, 1.8),
    "Oceania":  (-25.0, 145.0, 2.5),
}

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
            # deep-copy mutable defaults
            st.session_state[k] = v.copy() if isinstance(v, dict) else v


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

def _country_continent(name: str) -> str:
    for c in COUNTRIES:
        if c["en"] == name:
            return c["cont"]
    return ""


def _set_map_country(name: str, color: str = "#FFD93D",
                     show_capital: bool = False, cap_label: str = ""):
    """Place a single country star on the map, zoom to its continent region."""
    if name not in GEO_DATA:
        return
    geo  = GEO_DATA[name]
    cont = _country_continent(name)

    markers = [{
        "lat": geo["lat"], "lon": geo["lon"],
        "color": color, "size": 20, "symbol": "star",
        "label": name, "is_cap": False,
    }]
    if show_capital and cap_label:
        markers.append({
            "lat": geo["cap_lat"], "lon": geo["cap_lon"],
            "color": "#FFD93D", "size": 14, "symbol": "diamond",
            "label": f"🏛 {cap_label}", "is_cap": True,
        })

    st.session_state.geo_markers = markers

    if cont in CONTINENT_ZOOM:
        zlat, zlon, zsc = CONTINENT_ZOOM[cont]
        # Blend country centre with continent centre for a focused but contextual zoom
        st.session_state.geo_zoom_lat   = geo["lat"] * 0.55 + zlat * 0.45
        st.session_state.geo_zoom_lon   = geo["lon"] * 0.55 + zlon * 0.45
        st.session_state.geo_zoom_scale = zsc
    else:
        st.session_state.geo_zoom_lat   = geo["lat"]
        st.session_state.geo_zoom_lon   = geo["lon"]
        st.session_state.geo_zoom_scale = 3.0


def _set_map_countries(pairs: list):
    """Place multiple country markers (for Continent Sorter CHECK result).

    pairs: list of (country_name, is_correct)
    """
    markers = []
    for name, ok in pairs:
        if name not in GEO_DATA:
            continue
        geo = GEO_DATA[name]
        markers.append({
            "lat": geo["lat"], "lon": geo["lon"],
            "color": "#2ecc71" if ok else "#e74c3c",
            "size": 18, "symbol": "star",
            "label": name, "is_cap": False,
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
    c = random.choice(COUNTRIES)
    st.session_state.ff_country  = c
    st.session_state.ff_answered = False
    _set_map_country(c["en"], color="#FFD93D")  # yellow = pending question


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

    # Large flag display — 80 px font per spec
    st.markdown(
        f'<div style="text-align:center; font-size:80px; line-height:1.1; margin:10px 0;">'
        f'{c["flag"]}</div>'
        f'<div style="text-align:center; font-size:1.3em; font-family:Fredoka One,cursive; '
        f'color:#4ECDC4; margin-bottom:14px;">{c["en"]} / {c["fr"]}</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.ff_answered:
        # Show colored map + feedback, then a Next button
        show_feedback(st.session_state.ff_feedback)
        if st.button("▶️ Suivant / Next", key="ff_next", use_container_width=True):
            _load_ff()
            st.rerun()
        return

    cols = st.columns(3)
    for i, cont in enumerate(CONTINENTS):
        with cols[i % 3]:
            if st.button(
                f'{CONTINENT_EMOJI[cont]} {cont}',
                key=f"ff_{c['en']}_{cont}",
                use_container_width=True,
            ):
                if cont == c["cont"]:
                    st.session_state.ff_score += 1
                    add_stars(1, "geo")
                    _set_map_country(c["en"], color="#2ecc71")   # flash green
                    st.session_state.ff_feedback = ("ok",
                        f"Oui! {c['en']} est en {cont}! {CONTINENT_EMOJI[cont]}",
                        f"Yes! {c['en']} is in {cont}! {CONTINENT_EMOJI[cont]}")
                    st.session_state.ff_answered = True
                    st.balloons()
                else:
                    _set_map_country(c["en"], color="#e74c3c")   # flash red
                    st.session_state.ff_feedback = ("err",
                        f"Non! {c['en']} est en {c['cont']}!",
                        f"No! {c['en']} is in {c['cont']}!")
                    st.session_state.ff_answered = True
                st.rerun()


# ── Game B · Capital City Challenge ──────────────────────────────────────────

def _load_cc():
    pool = (
        COUNTRIES if st.session_state.cc_hard
        else [c for c in COUNTRIES if c["en"] in EASY_CAPITALS]
    )
    if not pool:
        pool = COUNTRIES
    country = random.choice(pool)
    all_caps = [c["cap"] for c in COUNTRIES]
    wrongs = random.sample([cap for cap in all_caps if cap != country["cap"]], 3)
    opts = wrongs + [country["cap"]]
    random.shuffle(opts)
    st.session_state.cc_country  = country
    st.session_state.cc_opts     = opts
    st.session_state.cc_answered = False
    # Show both country star (yellow) + capital diamond (gold) on the map
    _set_map_country(country["en"], color="#FFD93D",
                     show_capital=True, cap_label=country["cap"])


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

    st.markdown(
        f'<div class="q-card q-card-teal">'
        f'{c["flag"]}<br>'
        f'<span style="color:#4ECDC4; font-size:0.7em;">{c["en"]} / {c["fr"]}</span><br>'
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
            if st.button(f"🏛️ {opt}", key=f"cc_{c['en']}_{i}", use_container_width=True):
                if opt == c["cap"]:
                    st.session_state.cc_score  += 1
                    st.session_state.cc_streak += 1
                    add_stars(1, "geo")
                    _set_map_country(c["en"], color="#2ecc71",
                                     show_capital=True, cap_label=c["cap"])
                    if st.session_state.cc_streak >= 5 and not st.session_state.cc_hard:
                        st.session_state.cc_hard = True
                        st.session_state.cc_feedback = ("ok",
                            "🔓 Mode Expert debloque! Serie de 5!",
                            "🔓 Expert Mode Unlocked! 5 in a row!")
                    else:
                        st.session_state.cc_feedback = ("ok",
                            f"Correct! {c['en']} → {c['cap']}!",
                            f"Correct! {c['en']} → {c['cap']}!")
                    st.session_state.cc_answered = True
                    st.balloons()
                else:
                    _set_map_country(c["en"], color="#e74c3c",
                                     show_capital=True, cap_label=c["cap"])
                    st.session_state.cc_streak  = 0
                    st.session_state.cc_feedback = ("err",
                        f"Non! La capitale: {c['cap']}",
                        f"No! The capital: {c['cap']}")
                    st.session_state.cc_answered = True
                st.rerun()


# ── Game C · Continent Sorter ─────────────────────────────────────────────────

def _load_cs():
    st.session_state.cs_countries = random.sample(COUNTRIES, 5)
    st.session_state.cs_feedback  = None
    # Show all 5 as neutral yellow markers on the global map
    pairs = [(c["en"], None) for c in st.session_state.cs_countries]
    markers = []
    for name, _ in pairs:
        if name in GEO_DATA:
            geo = GEO_DATA[name]
            markers.append({"lat": geo["lat"], "lon": geo["lon"],
                            "color": "#FFD93D", "size": 18, "symbol": "star",
                            "label": name, "is_cap": False})
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

    st.markdown(f'<div class="score-line">⭐ Score total: {st.session_state.cs_score}</div>',
                unsafe_allow_html=True)

    for country in countries:
        c1, c2, c3 = st.columns([1, 2, 3])
        with c1:
            st.markdown(
                f'<div style="font-size:2.2em; text-align:center;">{country["flag"]}</div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div style="font-size:1.05em; font-family:Fredoka One,cursive; padding-top:8px;">'
                f'{country["en"]}<br>'
                f'<span style="color:#999; font-size:0.85em;">{country["fr"]}</span></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.selectbox(
                f"Continent — {country['en']}",
                CONTINENTS,
                key=f"cs_{country['en']}",
                label_visibility="collapsed",
            )

    st.markdown("<br>", unsafe_allow_html=True)
    col_check, col_new = st.columns(2)

    with col_check:
        if st.button("🚀 CHECK / VERIFIER", key="cs_check", use_container_width=True):
            results, correct_count = [], 0
            for country in countries:
                user_ans = st.session_state.get(f"cs_{country['en']}", CONTINENTS[0])
                right    = country["cont"]
                ok       = user_ans == right
                if ok:
                    correct_count += 1
                results.append((country["en"], country["flag"], user_ans, right, ok))
            add_stars(correct_count, "geo")
            st.session_state.cs_score   += correct_count
            st.session_state.cs_feedback = results
            # Update map: color each country green/red
            _set_map_countries([(name, ok) for name, _, _, _, ok in results])
            if correct_count == 5:
                st.balloons()
            st.rerun()

    with col_new:
        if st.button("🔄 Nouveau round / New Round", key="cs_new", use_container_width=True):
            _load_cs()
            st.rerun()

    if st.session_state.cs_feedback:
        st.markdown("---")
        for name, flag, user_ans, right, ok in st.session_state.cs_feedback:
            if ok:
                st.markdown(
                    f'<div class="fb-ok">✅ {flag} {name} → {right}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="fb-err">❌ {flag} {name} — '
                    f'Tu as dit / You said: {user_ans} &nbsp;|&nbsp; '
                    f'✅ Reponse / Answer: {right}</div>',
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
