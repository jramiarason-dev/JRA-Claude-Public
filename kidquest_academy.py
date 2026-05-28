"""
KidQuest Academy — Bilingual Edutainment Platform (ages 4–7)
New design: HTML/React prototype served full-bleed via Streamlit.
Legacy Python game logic preserved below (reachable via kidquest/streamlit_app.py).
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import random
import requests
import plotly.graph_objects as go
import json
import time
import base64
import pathlib
import re
import datetime
from datetime import date as _date

try:
    import anthropic as _anthropic
except ImportError:
    _anthropic = None

st.set_page_config(
    page_title="KidQuest — L'aventure du savoir",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Full-bleed: hide all Streamlit chrome so the HTML fills the screen ──────
st.markdown(
    """
    <style>
      #MainMenu, header, footer { visibility: hidden; height: 0; }
      .block-container { padding: 0 !important; max-width: 100% !important; }
      [data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
      [data-testid="stSidebar"] { display: none; }
      body, .stApp { background: #FFF6E8; margin: 0; }
      iframe { border: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Serve the redesigned HTML/React app full-bleed ──────────────────────────
_HTML_PATH = Path(__file__).parent / "kidquest" / "index.html"
if _HTML_PATH.exists():
    components.html(_HTML_PATH.read_text(encoding="utf-8"), height=1700, scrolling=True)
    st.stop()  # Don't render legacy Streamlit UI when design is available

# ─── FALLBACK: legacy Streamlit app (runs only if kidquest/index.html missing) ─

PROFILES_DIR = pathlib.Path("data/profiles")


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@800&display=swap');
html,body,[class*="css"],.stApp{font-family:'Fredoka One','Nunito',cursive !important;}
.kq-title{text-align:center;font-size:3em;font-family:'Fredoka One',cursive;
  background:linear-gradient(135deg,#FF6B35,#FFD93D,#4ECDC4);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin-bottom:0;line-height:1.1;}
.kq-subtitle{text-align:center;font-size:1.2em;color:var(--text-secondary);
  margin-top:0;font-family:'Fredoka One',cursive;}
.tab-header-orange{background:linear-gradient(135deg,#FF6B35,#FF8E53);color:white;
  padding:14px 20px;border-radius:14px;text-align:center;font-size:1.2em;
  font-family:'Fredoka One',cursive;margin-bottom:12px;}
.tab-header-teal{background:linear-gradient(135deg,#4ECDC4,#44A9C6);color:white;
  padding:14px 20px;border-radius:14px;text-align:center;font-size:1.2em;
  font-family:'Fredoka One',cursive;margin-bottom:12px;}
.tab-header-green{background:linear-gradient(135deg,#A8E6CF,#56C596);color:white;
  padding:14px 20px;border-radius:14px;text-align:center;font-size:1.2em;
  font-family:'Fredoka One',cursive;margin-bottom:12px;}
.q-card{background:var(--bg-card);border:4px solid #FFD93D;border-radius:22px;
  padding:22px 16px;text-align:center;font-size:1.8em;font-family:'Fredoka One',cursive;
  margin:12px 0;box-shadow:0 6px 18px rgba(0,0,0,.09);line-height:1.4;color:var(--text-primary);}
.q-card-teal{border-color:#4ECDC4;}.q-card-green{border-color:#A8E6CF;}
@keyframes popIn{0%{transform:scale(.85);opacity:0}70%{transform:scale(1.04)}100%{transform:scale(1);opacity:1}}
.banner-ok{background:linear-gradient(135deg,#6BCB77,#4D9BE6);color:white;padding:14px 18px;
  border-radius:16px;text-align:center;font-size:1.2em;font-family:'Fredoka One',cursive;
  animation:popIn .35s ease;margin:10px 0;line-height:1.5;}
.banner-err{background:linear-gradient(135deg,#FF6B6B,#FF8E53);color:white;padding:14px 18px;
  border-radius:16px;text-align:center;font-size:1.2em;font-family:'Fredoka One',cursive;
  animation:popIn .35s ease;margin:10px 0;line-height:1.5;}
.banner-info{background:linear-gradient(135deg,#4ECDC4,#44A9C6);color:white;padding:11px 15px;
  border-radius:13px;text-align:center;font-size:1em;font-family:'Fredoka One',cursive;margin:7px 0;line-height:1.5;}
.banner-info-green{background:linear-gradient(135deg,#A8E6CF,#56C596);color:white;padding:11px 15px;
  border-radius:13px;text-align:center;font-size:1em;font-family:'Fredoka One',cursive;margin:7px 0;line-height:1.5;}
.banner-idk{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:13px 16px;
  border-radius:15px;text-align:center;font-size:1.05em;font-family:'Fredoka One',cursive;margin:9px 0;line-height:1.5;}
.fb-ok{background:#6BCB77;color:white;padding:7px 12px;border-radius:11px;margin:3px 0;font-family:'Fredoka One',cursive;}
.fb-err{background:#FF6B6B;color:white;padding:7px 12px;border-radius:11px;margin:3px 0;font-family:'Fredoka One',cursive;}
.stButton>button{font-family:'Fredoka One',cursive !important;font-size:18px !important;
  border-radius:16px !important;min-height:60px !important;padding:10px 22px !important;
  transition:transform .15s ease,box-shadow .15s ease !important;}
.stButton>button:hover{transform:scale(1.05) !important;box-shadow:0 8px 22px rgba(0,0,0,.18) !important;}
.stNumberInput input{font-size:1.6em !important;text-align:center !important;
  font-family:'Fredoka One',cursive !important;border-radius:12px !important;}
.stRadio label{font-family:'Fredoka One',cursive !important;font-size:1em !important;}
.sb-card{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:12px 14px;
  border-radius:13px;text-align:center;font-family:'Fredoka One',cursive;font-size:1em;margin:4px 0;}
.sb-tab{padding:7px 11px;border-radius:0 11px 11px 0;margin:3px 0;font-family:'Fredoka One',cursive;}
.score-line{text-align:right;font-size:1.2em;font-family:'Fredoka One',cursive;margin-bottom:5px;color:var(--text-primary);}
.country-card{background:var(--bg-card);border:2px solid var(--border);border-radius:18px;padding:14px;margin:10px 0;}
.aid-panel{background:var(--bg-card);border:2px solid var(--border);border-radius:14px;padding:10px 8px;margin:9px 0;}
.aid-label{font-size:.72em;color:var(--text-secondary);font-family:'Fredoka One',cursive;margin-bottom:5px;}
.disc-banner{background:linear-gradient(135deg,#f093fb,#f5576c);color:white;padding:9px 14px;
  border-radius:13px;text-align:center;font-size:.95em;font-family:'Fredoka One',cursive;margin:5px 0;}
.round-bar{display:flex;gap:6px;justify-content:center;margin:8px 0;}
.rstar-full{font-size:1.6em;}.rstar-empty{font-size:1.6em;opacity:.3;}
@keyframes bounce{0%,100%{transform:translateY(0)}40%{transform:translateY(-16px)}}
@keyframes shake{0%,100%{transform:rotate(0)}25%{transform:rotate(-10deg)}75%{transform:rotate(10deg)}}
.av-bounce{animation:bounce .5s ease;}
.av-shake{animation:shake .4s ease;}
</style>""", unsafe_allow_html=True)


def inject_theme_css(dark_mode: bool):
    if dark_mode:
        p = {"--bg-main":"#0F0F1A","--bg-card":"#1A1A2E","--text-primary":"#F0F0FF",
             "--text-secondary":"#A0A0C0","--accent":"#FF8C5A","--tab-bg":"#16213E","--border":"#2A2A4A"}
    else:
        p = {"--bg-main":"#FEFEFE","--bg-card":"#F0F4FF","--text-primary":"#1A1A2E",
             "--text-secondary":"#4A4A6A","--accent":"#FF6B35","--tab-bg":"#FFFFFF","--border":"#E0E0F0"}
    v = "".join(f"{k}:{v};" for k, v in p.items())
    st.markdown(f"<style>:root{{{v}}}.stApp{{background:{p['--bg-main']} !important;}}</style>",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# BADGES & AVATARS
# ─────────────────────────────────────────────────────────────────────────────
BADGES = [
    {"id":1, "min_stars":0,   "emoji":"🥚","name_fr":"Œuf Mystère",     "name_en":"Mystery Egg",      "color":"#BDC3C7","desc_fr":"Ton aventure commence !",       "desc_en":"Your adventure begins!"},
    {"id":2, "min_stars":5,   "emoji":"🐣","name_fr":"Poussin Curieux",  "name_en":"Curious Chick",    "color":"#F9E79F","desc_fr":"Tu apprends vite !",            "desc_en":"You learn fast!"},
    {"id":3, "min_stars":12,  "emoji":"🦊","name_fr":"Renard Malin",     "name_en":"Clever Fox",       "color":"#F0A500","desc_fr":"Rusé comme un renard !",        "desc_en":"Sly as a fox!"},
    {"id":4, "min_stars":22,  "emoji":"🦁","name_fr":"Lion Courageux",   "name_en":"Brave Lion",       "color":"#E67E22","desc_fr":"Tu rugis de talent !",          "desc_en":"You roar with talent!"},
    {"id":5, "min_stars":35,  "emoji":"🦅","name_fr":"Aigle Visionnaire","name_en":"Eagle Eye",        "color":"#5DADE2","desc_fr":"Tu vois loin !",                "desc_en":"You see far ahead!"},
    {"id":6, "min_stars":50,  "emoji":"🐉","name_fr":"Dragon Sage",      "name_en":"Wise Dragon",      "color":"#8E44AD","desc_fr":"La sagesse est en toi !",       "desc_en":"Wisdom is within you!"},
    {"id":7, "min_stars":70,  "emoji":"🧙","name_fr":"Mage Suprême",     "name_en":"Supreme Mage",     "color":"#1ABC9C","desc_fr":"La magie du savoir !",          "desc_en":"The magic of knowledge!"},
    {"id":8, "min_stars":95,  "emoji":"🚀","name_fr":"Astronaute Pro",   "name_en":"Pro Astronaut",    "color":"#2980B9","desc_fr":"Tu vises les étoiles !",        "desc_en":"Reach for the stars!"},
    {"id":9, "min_stars":125, "emoji":"⚡","name_fr":"Génie Éclair",     "name_en":"Lightning Genius", "color":"#F39C12","desc_fr":"La foudre de l'intelligence !","desc_en":"Strike of intelligence!"},
    {"id":10,"min_stars":160, "emoji":"👑","name_fr":"Grand Maître",     "name_en":"Grand Master",     "color":"#FFD700","desc_fr":"Tu es légendaire !",            "desc_en":"You are legendary!"},
]

AVATAR_LIST = [
    {"id":"fox",      "emoji":"🦊","name_fr":"Renard",    "name_en":"Fox"},
    {"id":"lion",     "emoji":"🦁","name_fr":"Lion",      "name_en":"Lion"},
    {"id":"owl",      "emoji":"🦉","name_fr":"Hibou",     "name_en":"Owl"},
    {"id":"dragon",   "emoji":"🐲","name_fr":"Dragon",    "name_en":"Dragon"},
    {"id":"panda",    "emoji":"🐼","name_fr":"Panda",     "name_en":"Panda"},
    {"id":"penguin",  "emoji":"🐧","name_fr":"Pingouin",  "name_en":"Penguin"},
    {"id":"wizard",   "emoji":"🧙","name_fr":"Mage",      "name_en":"Wizard"},
    {"id":"ninja",    "emoji":"🥷","name_fr":"Ninja",     "name_en":"Ninja"},
    {"id":"astronaut","emoji":"🧑‍🚀","name_fr":"Astronaute","name_en":"Astronaut"},
    {"id":"knight",   "emoji":"🧝","name_fr":"Elfe",      "name_en":"Elf"},
    {"id":"robot",    "emoji":"🤖","name_fr":"Robot",     "name_en":"Robot"},
    {"id":"unicorn",  "emoji":"🦄","name_fr":"Licorne",   "name_en":"Unicorn"},
]

# ─────────────────────────────────────────────────────────────────────────────
# ENGLISH QUEST DATA
# ─────────────────────────────────────────────────────────────────────────────
WORD_PAIRS = [
    {"en":"CAT",    "fr":"CHAT",       "emoji":"🐱","lvl":"easy"},
    {"en":"DOG",    "fr":"CHIEN",      "emoji":"🐶","lvl":"easy"},
    {"en":"SUN",    "fr":"SOLEIL",     "emoji":"☀️","lvl":"easy"},
    {"en":"BEE",    "fr":"ABEILLE",    "emoji":"🐝","lvl":"easy"},
    {"en":"COW",    "fr":"VACHE",      "emoji":"🐄","lvl":"easy"},
    {"en":"HEN",    "fr":"POULE",      "emoji":"🐔","lvl":"easy"},
    {"en":"PIG",    "fr":"COCHON",     "emoji":"🐷","lvl":"easy"},
    {"en":"OWL",    "fr":"HIBOU",      "emoji":"🦉","lvl":"easy"},
    {"en":"ANT",    "fr":"FOURMI",     "emoji":"🐜","lvl":"easy"},
    {"en":"EGG",    "fr":"OEUF",       "emoji":"🥚","lvl":"easy"},
    {"en":"FISH",   "fr":"POISSON",    "emoji":"🐟","lvl":"easy"},
    {"en":"DUCK",   "fr":"CANARD",     "emoji":"🦆","lvl":"easy"},
    {"en":"FROG",   "fr":"GRENOUILLE", "emoji":"🐸","lvl":"easy"},
    {"en":"BEAR",   "fr":"OURS",       "emoji":"🐻","lvl":"easy"},
    {"en":"BIRD",   "fr":"OISEAU",     "emoji":"🐦","lvl":"easy"},
    {"en":"WOLF",   "fr":"LOUP",       "emoji":"🐺","lvl":"easy"},
    {"en":"LION",   "fr":"LION",       "emoji":"🦁","lvl":"easy"},
    {"en":"DEER",   "fr":"CERF",       "emoji":"🦌","lvl":"easy"},
    {"en":"STAR",   "fr":"ETOILE",     "emoji":"⭐","lvl":"easy"},
    {"en":"RAIN",   "fr":"PLUIE",      "emoji":"🌧️","lvl":"easy"},
    {"en":"HORSE",  "fr":"CHEVAL",     "emoji":"🐴","lvl":"medium"},
    {"en":"TIGER",  "fr":"TIGRE",      "emoji":"🐯","lvl":"medium"},
    {"en":"SNAKE",  "fr":"SERPENT",    "emoji":"🐍","lvl":"medium"},
    {"en":"WHALE",  "fr":"BALEINE",    "emoji":"🐋","lvl":"medium"},
    {"en":"EAGLE",  "fr":"AIGLE",      "emoji":"🦅","lvl":"medium"},
    {"en":"PANDA",  "fr":"PANDA",      "emoji":"🐼","lvl":"medium"},
    {"en":"KOALA",  "fr":"KOALA",      "emoji":"🐨","lvl":"medium"},
    {"en":"SHARK",  "fr":"REQUIN",     "emoji":"🦈","lvl":"medium"},
    {"en":"CAMEL",  "fr":"CHAMEAU",    "emoji":"🐪","lvl":"medium"},
    {"en":"ZEBRA",  "fr":"ZEBRE",      "emoji":"🦓","lvl":"medium"},
    {"en":"RABBIT", "fr":"LAPIN",      "emoji":"🐰","lvl":"medium"},
    {"en":"TURTLE", "fr":"TORTUE",     "emoji":"🐢","lvl":"medium"},
    {"en":"MONKEY", "fr":"SINGE",      "emoji":"🐵","lvl":"medium"},
    {"en":"PARROT", "fr":"PERROQUET",  "emoji":"🦜","lvl":"medium"},
    {"en":"FLOWER", "fr":"FLEUR",      "emoji":"🌸","lvl":"medium"},
]

WORD_CONTEXT = {
    "CAT":    ("J'ai un chat.",        "I have a cat. 🐱"),
    "DOG":    ("Le chien court.",      "The dog runs. 🐶"),
    "SUN":    ("Le soleil brille.",    "The sun shines. ☀️"),
    "BEE":    ("L'abeille butine.",    "The bee buzzes. 🐝"),
    "COW":    ("La vache mange.",      "The cow eats. 🐄"),
    "HEN":    ("La poule pond.",       "The hen lays. 🐔"),
    "PIG":    ("Le cochon grogne.",    "The pig oinks. 🐷"),
    "OWL":    ("Le hibou vole.",       "The owl flies. 🦉"),
    "ANT":    ("La fourmi travaille.", "The ant works. 🐜"),
    "EGG":    ("L'oeuf est chaud.",    "The egg is warm. 🥚"),
    "FISH":   ("Le poisson nage.",     "The fish swims. 🐟"),
    "DUCK":   ("Le canard nage.",      "The duck swims. 🦆"),
    "FROG":   ("La grenouille saute.", "The frog jumps. 🐸"),
    "BEAR":   ("L'ours dort.",         "The bear sleeps. 🐻"),
    "BIRD":   ("L'oiseau chante.",     "The bird sings. 🐦"),
    "WOLF":   ("Le loup hurle.",       "The wolf howls. 🐺"),
    "LION":   ("Le lion rugit.",       "The lion roars. 🦁"),
    "DEER":   ("Le cerf court.",       "The deer runs. 🦌"),
    "STAR":   ("L'étoile brille.",     "The star shines. ⭐"),
    "RAIN":   ("La pluie tombe.",      "The rain falls. 🌧️"),
    "HORSE":  ("Le cheval galope.",    "The horse gallops. 🐴"),
    "TIGER":  ("Le tigre bondit.",     "The tiger leaps. 🐯"),
    "SNAKE":  ("Le serpent glisse.",   "The snake slides. 🐍"),
    "WHALE":  ("La baleine plonge.",   "The whale dives. 🐋"),
    "EAGLE":  ("L'aigle vole haut.",   "The eagle soars. 🦅"),
    "PANDA":  ("Le panda mange.",      "The panda eats. 🐼"),
    "SHARK":  ("Le requin nage.",      "The shark swims. 🦈"),
    "CAMEL":  ("Le chameau marche.",   "The camel walks. 🐪"),
    "ZEBRA":  ("Le zèbre court.",      "The zebra runs. 🦓"),
    "RABBIT": ("Le lapin saute.",      "The rabbit hops. 🐰"),
}

SENTENCES = [
    {"words":["I","love","cats"],      "blank":1,"opts":["love","hate","see"],     "fr":"J'aime les chats"},
    {"words":["The","sun","shines"],   "blank":1,"opts":["sun","moon","star"],     "fr":"Le soleil brille"},
    {"words":["She","is","happy"],     "blank":2,"opts":["happy","sad","big"],     "fr":"Elle est heureuse"},
    {"words":["I","eat","apples"],     "blank":2,"opts":["apples","books","shoes"],"fr":"Je mange des pommes"},
    {"words":["The","dog","runs"],     "blank":1,"opts":["dog","cat","fish"],      "fr":"Le chien court"},
    {"words":["He","reads","books"],   "blank":1,"opts":["reads","eats","draws"],  "fr":"Il lit des livres"},
    {"words":["We","like","music"],    "blank":2,"opts":["music","water","sleep"], "fr":"Nous aimons la musique"},
    {"words":["Birds","can","fly"],    "blank":2,"opts":["fly","swim","jump"],     "fr":"Les oiseaux peuvent voler"},
    {"words":["Fish","live","underwater"],"blank":1,"opts":["live","sleep","run"], "fr":"Les poissons vivent sous l'eau"},
    {"words":["I","drink","milk"],     "blank":2,"opts":["milk","sand","rock"],    "fr":"Je bois du lait"},
    {"words":["She","draws","flowers"],"blank":2,"opts":["flowers","tables","cars"],"fr":"Elle dessine des fleurs"},
    {"words":["The","bear","sleeps"],  "blank":1,"opts":["bear","horse","bird"],   "fr":"L'ours dort"},
    {"words":["We","play","outside"],  "blank":2,"opts":["outside","inside","upside"],"fr":"Nous jouons dehors"},
    {"words":["The","cat","meows"],    "blank":2,"opts":["meows","barks","roars"], "fr":"Le chat miaule"},
    {"words":["I","am","six"],         "blank":2,"opts":["six","two","ten"],       "fr":"J'ai six ans"},
    {"words":["Stars","shine","bright"],"blank":1,"opts":["shine","fall","grow"],  "fr":"Les étoiles brillent"},
    {"words":["Frogs","love","rain"],  "blank":2,"opts":["rain","snow","heat"],    "fr":"Les grenouilles aiment la pluie"},
    {"words":["I","see","rainbows"],   "blank":1,"opts":["see","hear","smell"],    "fr":"Je vois des arcs-en-ciel"},
    {"words":["My","name","is"],       "blank":0,"opts":["My","His","Her"],        "fr":"Mon prénom est"},
    {"words":["The","sky","is","blue"],"blank":3,"opts":["blue","red","green"],    "fr":"Le ciel est bleu"},
]

SPELL_ITEMS = [
    {"emoji":"🌈","name":"Rainbow",   "opts":["Rainbow","Sunset","Thunder","Snowfall"]},
    {"emoji":"🎸","name":"Guitar",    "opts":["Guitar","Piano","Violin","Trumpet"]},
    {"emoji":"🏖️","name":"Beach",     "opts":["Beach","Forest","Desert","Mountain"]},
    {"emoji":"🚀","name":"Rocket",    "opts":["Rocket","Plane","Balloon","Spaceship"]},
    {"emoji":"🦋","name":"Butterfly", "opts":["Butterfly","Dragonfly","Ladybug","Caterpillar"]},
    {"emoji":"🌺","name":"Flower",    "opts":["Flower","Mushroom","Cactus","Leaf"]},
    {"emoji":"🐬","name":"Dolphin",   "opts":["Dolphin","Whale","Shark","Turtle"]},
    {"emoji":"🏔️","name":"Mountain", "opts":["Mountain","Volcano","Island","Valley"]},
    {"emoji":"🌙","name":"Moon",      "opts":["Moon","Star","Comet","Planet"]},
    {"emoji":"🦁","name":"Lion",      "opts":["Lion","Tiger","Leopard","Cheetah"]},
    {"emoji":"🍓","name":"Strawberry","opts":["Strawberry","Raspberry","Blueberry","Cherry"]},
    {"emoji":"🌊","name":"Wave",      "opts":["Wave","Storm","Ripple","Tide"]},
    {"emoji":"🎯","name":"Target",    "opts":["Target","Shield","Arrow","Sword"]},
    {"emoji":"🎪","name":"Circus",    "opts":["Circus","Theater","Stadium","Market"]},
    {"emoji":"🎨","name":"Painting",  "opts":["Painting","Drawing","Sculpture","Music"]},
]

# ─────────────────────────────────────────────────────────────────────────────
# GEO DATA — flag helper (needed by fallback constructor)
# ─────────────────────────────────────────────────────────────────────────────
def code_to_flag(a2: str) -> str:
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in a2.upper())


def _c(ne, nf, a2, cap, lat, lon, reg, sub, pop, area=0, cur="", cursym="", lang=""):
    return {"name_en":ne,"name_fr":nf,"alpha2":a2,"capital":cap,
            "lat":lat,"lon":lon,"region":reg,"subregion":sub,"population":pop,
            "area":area,"currency_name":cur,"currency_symbol":cursym,
            "language_name":lang,"flag_emoji":code_to_flag(a2)}


FALLBACK_COUNTRIES = [
    # Europe (20)
    _c("France","France","FR","Paris",46.23,2.21,"Europe","Western Europe",67_000_000,551_695,"Euro","€","French"),
    _c("Germany","Allemagne","DE","Berlin",51.17,10.45,"Europe","Western Europe",83_000_000,357_114,"Euro","€","German"),
    _c("Italy","Italie","IT","Rome",41.87,12.57,"Europe","Southern Europe",60_000_000,301_336,"Euro","€","Italian"),
    _c("Spain","Espagne","ES","Madrid",40.46,-3.75,"Europe","Southern Europe",47_000_000,505_990,"Euro","€","Spanish"),
    _c("United Kingdom","Royaume-Uni","GB","London",55.38,-3.44,"Europe","Northern Europe",67_000_000,243_610,"Pound","£","English"),
    _c("Portugal","Portugal","PT","Lisbon",39.40,-8.22,"Europe","Southern Europe",10_000_000,92_212,"Euro","€","Portuguese"),
    _c("Netherlands","Pays-Bas","NL","Amsterdam",52.13,5.29,"Europe","Western Europe",17_000_000,41_543,"Euro","€","Dutch"),
    _c("Belgium","Belgique","BE","Brussels",50.50,4.47,"Europe","Western Europe",11_000_000,30_528,"Euro","€","Dutch"),
    _c("Switzerland","Suisse","CH","Bern",46.82,8.23,"Europe","Western Europe",8_000_000,41_285,"Swiss Franc","CHF","German"),
    _c("Sweden","Suède","SE","Stockholm",60.13,18.64,"Europe","Northern Europe",10_000_000,450_295,"Krona","kr","Swedish"),
    _c("Greece","Grèce","GR","Athens",39.07,21.82,"Europe","Southern Europe",11_000_000,131_957,"Euro","€","Greek"),
    _c("Poland","Pologne","PL","Warsaw",51.92,19.15,"Europe","Eastern Europe",38_000_000,312_685,"Zloty","zł","Polish"),
    _c("Czech Republic","Tchéquie","CZ","Prague",49.82,15.47,"Europe","Eastern Europe",11_000_000,78_866,"Koruna","Kč","Czech"),
    _c("Austria","Autriche","AT","Vienna",47.52,14.55,"Europe","Western Europe",9_000_000,83_871,"Euro","€","German"),
    _c("Hungary","Hongrie","HU","Budapest",47.16,19.50,"Europe","Eastern Europe",10_000_000,93_028,"Forint","Ft","Hungarian"),
    _c("Romania","Roumanie","RO","Bucharest",45.94,24.97,"Europe","Eastern Europe",19_000_000,238_397,"Leu","lei","Romanian"),
    _c("Finland","Finlande","FI","Helsinki",61.92,25.75,"Europe","Northern Europe",5_000_000,338_145,"Euro","€","Finnish"),
    _c("Norway","Norvège","NO","Oslo",60.47,8.47,"Europe","Northern Europe",5_000_000,323_802,"Krone","kr","Norwegian"),
    _c("Denmark","Danemark","DK","Copenhagen",56.26,9.50,"Europe","Northern Europe",6_000_000,42_924,"Krone","kr","Danish"),
    _c("Ireland","Irlande","IE","Dublin",53.41,-8.24,"Europe","Northern Europe",5_000_000,70_273,"Euro","€","English"),
    # Asia (20)
    _c("Japan","Japon","JP","Tokyo",36.20,138.25,"Asia","Eastern Asia",126_000_000,377_930,"Yen","¥","Japanese"),
    _c("China","Chine","CN","Beijing",35.86,104.20,"Asia","Eastern Asia",1_400_000_000,9_596_960,"Yuan","¥","Chinese"),
    _c("India","Inde","IN","New Delhi",20.59,78.96,"Asia","Southern Asia",1_380_000_000,3_287_263,"Rupee","₹","Hindi"),
    _c("Turkey","Turquie","TR","Ankara",38.96,35.24,"Asia","Western Asia",84_000_000,783_562,"Lira","₺","Turkish"),
    _c("South Korea","Corée du Sud","KR","Seoul",35.91,127.77,"Asia","Eastern Asia",52_000_000,100_210,"Won","₩","Korean"),
    _c("Thailand","Thaïlande","TH","Bangkok",15.87,100.99,"Asia","South-Eastern Asia",70_000_000,513_120,"Baht","฿","Thai"),
    _c("Vietnam","Vietnam","VN","Hanoi",14.06,108.28,"Asia","South-Eastern Asia",97_000_000,331_212,"Dong","₫","Vietnamese"),
    _c("Indonesia","Indonésie","ID","Jakarta",-0.79,113.92,"Asia","South-Eastern Asia",273_000_000,1_904_569,"Rupiah","Rp","Indonesian"),
    _c("Philippines","Philippines","PH","Manila",12.88,121.77,"Asia","South-Eastern Asia",110_000_000,300_000,"Peso","₱","Filipino"),
    _c("Saudi Arabia","Arabie Saoudite","SA","Riyadh",23.89,45.08,"Asia","Western Asia",35_000_000,2_149_690,"Riyal","﷼","Arabic"),
    _c("Iran","Iran","IR","Tehran",32.43,53.69,"Asia","Southern Asia",84_000_000,1_648_195,"Rial","﷼","Persian"),
    _c("Pakistan","Pakistan","PK","Islamabad",30.38,69.35,"Asia","Southern Asia",220_000_000,881_913,"Rupee","₨","Urdu"),
    _c("Bangladesh","Bangladesh","BD","Dhaka",23.68,90.36,"Asia","Southern Asia",165_000_000,147_570,"Taka","৳","Bengali"),
    _c("Malaysia","Malaisie","MY","Kuala Lumpur",4.21,101.98,"Asia","South-Eastern Asia",32_000_000,329_847,"Ringgit","RM","Malay"),
    _c("Myanmar","Myanmar","MM","Naypyidaw",17.11,96.96,"Asia","South-Eastern Asia",54_000_000,676_578,"Kyat","K","Burmese"),
    _c("Nepal","Népal","NP","Kathmandu",28.39,84.12,"Asia","Southern Asia",29_000_000,147_181,"Rupee","₨","Nepali"),
    _c("Sri Lanka","Sri Lanka","LK","Sri Jayawardenepura",7.87,80.77,"Asia","Southern Asia",22_000_000,65_610,"Rupee","₨","Sinhala"),
    _c("United Arab Emirates","Émirats arabes unis","AE","Abu Dhabi",23.42,53.85,"Asia","Western Asia",10_000_000,83_600,"Dirham","د.إ","Arabic"),
    _c("Afghanistan","Afghanistan","AF","Kabul",33.94,67.71,"Asia","Southern Asia",39_000_000,652_230,"Afghani","؋","Pashto"),
    _c("Cambodia","Cambodge","KH","Phnom Penh",12.57,104.99,"Asia","South-Eastern Asia",17_000_000,181_035,"Riel","៛","Khmer"),
    # Americas (15)
    _c("United States","États-Unis","US","Washington D.C.",37.09,-95.71,"Americas","Northern America",331_000_000,9_372_610,"Dollar","$","English"),
    _c("Brazil","Brésil","BR","Brasília",-14.24,-51.93,"Americas","South America",213_000_000,8_515_767,"Real","R$","Portuguese"),
    _c("Canada","Canada","CA","Ottawa",56.13,-106.35,"Americas","Northern America",38_000_000,9_984_670,"Dollar","CA$","English"),
    _c("Mexico","Mexique","MX","Mexico City",23.63,-102.55,"Americas","Central America",129_000_000,1_964_375,"Peso","$","Spanish"),
    _c("Argentina","Argentine","AR","Buenos Aires",-38.42,-63.62,"Americas","South America",45_000_000,2_780_400,"Peso","$","Spanish"),
    _c("Colombia","Colombie","CO","Bogotá",4.57,-74.30,"Americas","South America",51_000_000,1_141_748,"Peso","$","Spanish"),
    _c("Peru","Pérou","PE","Lima",-9.19,-75.02,"Americas","South America",32_000_000,1_285_216,"Sol","S/.","Spanish"),
    _c("Chile","Chili","CL","Santiago",-35.68,-71.54,"Americas","South America",19_000_000,756_102,"Peso","$","Spanish"),
    _c("Venezuela","Venezuela","VE","Caracas",6.42,-66.59,"Americas","South America",28_000_000,916_445,"Bolívar","Bs","Spanish"),
    _c("Cuba","Cuba","CU","Havana",21.52,-77.78,"Americas","Caribbean",11_000_000,109_884,"Peso","$","Spanish"),
    _c("Ecuador","Équateur","EC","Quito",-1.83,-78.18,"Americas","South America",18_000_000,283_561,"Dollar","$","Spanish"),
    _c("Bolivia","Bolivie","BO","Sucre",-16.29,-63.59,"Americas","South America",12_000_000,1_098_581,"Boliviano","Bs","Spanish"),
    _c("Uruguay","Uruguay","UY","Montevideo",-32.52,-55.77,"Americas","South America",3_000_000,176_215,"Peso","$","Spanish"),
    _c("Paraguay","Paraguay","PY","Asunción",-23.44,-58.44,"Americas","South America",7_000_000,406_752,"Guaraní","₲","Spanish"),
    _c("Jamaica","Jamaïque","JM","Kingston",18.10,-77.30,"Americas","Caribbean",3_000_000,10_991,"Dollar","J$","English"),
    # Africa (15)
    _c("Nigeria","Nigeria","NG","Abuja",9.08,8.68,"Africa","Western Africa",211_000_000,923_768,"Naira","₦","English"),
    _c("Egypt","Égypte","EG","Cairo",26.82,30.80,"Africa","Northern Africa",102_000_000,1_001_450,"Pound","£","Arabic"),
    _c("South Africa","Afrique du Sud","ZA","Cape Town",-30.56,22.94,"Africa","Southern Africa",60_000_000,1_219_090,"Rand","R","Zulu"),
    _c("Kenya","Kenya","KE","Nairobi",0.02,37.91,"Africa","Eastern Africa",54_000_000,580_367,"Shilling","Ksh","Swahili"),
    _c("Ethiopia","Éthiopie","ET","Addis Ababa",9.15,40.49,"Africa","Eastern Africa",115_000_000,1_104_300,"Birr","Br","Amharic"),
    _c("Tanzania","Tanzanie","TZ","Dodoma",-6.37,34.89,"Africa","Eastern Africa",61_000_000,945_087,"Shilling","Tsh","Swahili"),
    _c("Ghana","Ghana","GH","Accra",7.95,-1.02,"Africa","Western Africa",32_000_000,238_533,"Cedi","₵","English"),
    _c("Morocco","Maroc","MA","Rabat",31.79,-7.09,"Africa","Northern Africa",37_000_000,446_550,"Dirham","MAD","Arabic"),
    _c("Algeria","Algérie","DZ","Algiers",28.03,1.66,"Africa","Northern Africa",44_000_000,2_381_741,"Dinar","DA","Arabic"),
    _c("Tunisia","Tunisie","TN","Tunis",33.89,9.54,"Africa","Northern Africa",12_000_000,163_610,"Dinar","DT","Arabic"),
    _c("Cameroon","Cameroun","CM","Yaoundé",3.85,11.50,"Africa","Middle Africa",27_000_000,475_442,"CFA Franc","FCFA","French"),
    _c("Ivory Coast","Côte d'Ivoire","CI","Yamoussoukro",7.54,-5.55,"Africa","Western Africa",27_000_000,322_463,"CFA Franc","FCFA","French"),
    _c("Senegal","Sénégal","SN","Dakar",14.50,-14.45,"Africa","Western Africa",17_000_000,196_722,"CFA Franc","FCFA","French"),
    _c("Zimbabwe","Zimbabwe","ZW","Harare",-19.02,29.15,"Africa","Eastern Africa",15_000_000,390_757,"Dollar","$","Shona"),
    _c("Uganda","Ouganda","UG","Kampala",1.37,32.29,"Africa","Eastern Africa",47_000_000,241_038,"Shilling","USh","English"),
    # Oceania (10)
    _c("Australia","Australie","AU","Canberra",-25.27,133.78,"Oceania","Australia and New Zealand",26_000_000,7_692_024,"Dollar","A$","English"),
    _c("New Zealand","Nouvelle-Zélande","NZ","Wellington",-40.90,174.89,"Oceania","Australia and New Zealand",5_000_000,270_467,"Dollar","NZ$","English"),
    _c("Fiji","Fidji","FJ","Suva",-17.71,178.07,"Oceania","Melanesia",900_000,18_274,"Dollar","FJ$","English"),
    _c("Papua New Guinea","Papouasie","PG","Port Moresby",-6.31,143.96,"Oceania","Melanesia",9_000_000,462_840,"Kina","K","English"),
    _c("Samoa","Samoa","WS","Apia",-13.76,-172.10,"Oceania","Polynesia",200_000,2_842,"Tala","T","Samoan"),
    _c("Tonga","Tonga","TO","Nuku'alofa",-21.18,-175.20,"Oceania","Polynesia",100_000,747,"Paʻanga","T$","Tongan"),
    _c("Vanuatu","Vanuatu","VU","Port Vila",-15.38,166.96,"Oceania","Melanesia",300_000,12_189,"Vatu","VT","Bislama"),
    _c("Solomon Islands","Îles Salomon","SB","Honiara",-9.65,160.16,"Oceania","Melanesia",700_000,28_896,"Dollar","SI$","English"),
    _c("Kiribati","Kiribati","KI","South Tarawa",1.34,173.01,"Oceania","Micronesia",120_000,811,"Dollar","$","English"),
    _c("Nauru","Nauru","NR","Yaren",-0.53,166.93,"Oceania","Micronesia",10_000,21,"Dollar","A$","Nauruan"),
]

CAPITAL_COORDS = {
    "France":(48.86,2.35),"Germany":(52.52,13.40),"Italy":(41.90,12.50),"Spain":(40.42,-3.70),
    "United Kingdom":(51.51,-0.13),"Portugal":(38.72,-9.14),"Netherlands":(52.37,4.90),
    "Belgium":(50.85,4.35),"Switzerland":(46.95,7.45),"Sweden":(59.33,18.07),
    "Greece":(37.98,23.73),"Poland":(52.23,21.01),"Czech Republic":(50.08,14.44),
    "Austria":(48.21,16.37),"Hungary":(47.50,19.04),"Romania":(44.43,26.10),
    "Finland":(60.17,24.94),"Norway":(59.91,10.75),"Denmark":(55.68,12.57),"Ireland":(53.33,-6.25),
    "Japan":(35.69,139.69),"China":(39.91,116.39),"India":(28.61,77.21),"Turkey":(39.92,32.85),
    "South Korea":(37.57,126.98),"Thailand":(13.75,100.52),"Vietnam":(21.03,105.85),
    "Indonesia":(-6.21,106.85),"Philippines":(14.60,120.98),"Saudi Arabia":(24.69,46.72),
    "Iran":(35.69,51.42),"Pakistan":(33.72,73.04),"Bangladesh":(23.72,90.41),
    "Malaysia":(3.15,101.71),"Myanmar":(19.75,96.10),"Nepal":(27.47,85.31),
    "Sri Lanka":(6.92,79.86),"United Arab Emirates":(24.45,54.37),
    "Afghanistan":(34.52,69.18),"Cambodia":(11.57,104.92),
    "United States":(38.91,-77.04),"Brazil":(-15.78,-47.93),"Canada":(45.42,-75.70),
    "Mexico":(19.43,-99.13),"Argentina":(-34.60,-58.38),"Colombia":(4.71,-74.07),
    "Peru":(-12.05,-77.05),"Chile":(-33.46,-70.65),"Venezuela":(10.50,-66.92),
    "Cuba":(23.11,-82.37),"Ecuador":(-0.23,-78.51),"Bolivia":(-16.50,-68.15),
    "Uruguay":(-34.90,-56.19),"Paraguay":(-25.28,-57.65),"Jamaica":(17.99,-76.79),
    "Nigeria":(9.07,7.40),"Egypt":(30.04,31.24),"South Africa":(-33.93,18.42),
    "Kenya":(-1.29,36.82),"Ethiopia":(9.03,38.74),"Tanzania":(-6.18,35.74),
    "Ghana":(5.56,-0.20),"Morocco":(34.02,-6.84),"Algeria":(36.74,3.06),
    "Tunisia":(36.82,10.18),"Cameroon":(3.87,11.52),"Ivory Coast":(6.82,-5.28),
    "Senegal":(14.76,-17.37),"Zimbabwe":(-17.83,31.05),"Uganda":(0.32,32.58),
    "Australia":(-35.28,149.13),"New Zealand":(-41.29,174.78),"Fiji":(-18.14,178.44),
    "Papua New Guinea":(-9.44,147.18),"Samoa":(-13.83,-171.77),
}

REGION_LABELS = {
    "Africa":"Afrique 🌍 / Africa 🌍","Americas":"Amériques 🌎 / Americas 🌎",
    "Asia":"Asie 🌏 / Asia 🌏","Europe":"Europe 🏰 / Europe 🏰",
    "Oceania":"Océanie 🏝️ / Oceania 🏝️","Polar":"Pôles ❄️ / Polar ❄️",
}
REGION_ZOOM = {
    "Europe":(54.0,15.0,3.0),"Asia":(32.0,95.0,1.8),"Americas":(5.0,-80.0,1.4),
    "Africa":(5.0,20.0,1.8),"Oceania":(-25.0,145.0,2.5),"Polar":(0.0,0.0,1.0),
}
EASY_CAPITAL_NAMES = {
    "France","Japan","Brazil","United States","United Kingdom",
    "Germany","Italy","Spain","Canada","Mexico","Australia","China","India",
}

COUNTRY_EMOJI = {
    "FR":("🗼","🥖","🧀","🍷","🐓","🎨"),"JP":("⛩️","🍣","🗻","🌸","🎎","🤖"),
    "BR":("🌴","⚽","🦜","☕","🎭","🏖️"),"IN":("🕌","🐘","🌶️","🎬","🦚","🍛"),
    "AU":("🦘","🪃","🐨","🌊","🦎","🏄"),"US":("🗽","🦅","🍔","🎸","🚀","🤠"),
    "CN":("🐉","🥟","🏯","🐼","🎋","🧧"),"DE":("🍺","🌭","🏰","🚗","🎻","🦅"),
    "ZA":("🦁","💎","🌍","🦒","🏉","🎷"),"IT":("🍕","🎭","⛵","🧶","🏛️","🍝"),
    "MX":("🌮","🎺","🦅","🏜️","💀","🌵"),"EG":("🐪","🏺","☀️","🌊","🔺","🦂"),
    "CH":("⛷️","🧀","⌚","🏔️","🍫","🏦"),"GB":("☕","🎭","🏰","🎸","🚂","🌧️"),
    "ES":("💃","🥘","🏖️","⚽","🐂","🎸"),"PT":("🐟","🏄","🎸","🍷","🏰","⛵"),
    "NL":("🌷","🧀","🚲","🎨","⛵","🌊"),"BE":("🍫","🍟","🍺","🎭","🚂","💎"),
    "SE":("🌲","🫐","🏔️","🎄","🦌","🔔"),"GR":("🏛️","🫒","🐬","🌞","🧿","⛵"),
    "TR":("🕌","☕","🌹","🏺","🎭","🧿"),"SA":("🌴","🐪","🛢️","🕌","💎","🌙"),
    "RU":("🏰","🍳","🐻","❄️","🚀","🎻"),"CA":("🍁","🏒","🐻","🌲","🦌","🍺"),
    "AR":("🥩","💃","⚽","🌿","🐄","🎻"),"CL":("🌋","🍷","🐧","🌊","🦔","⛷️"),
    "PE":("🦙","🌽","🏔️","🐦","🌿","🍟"),"CO":("☕","🦋","🌺","💃","🌴","🐦"),
    "NG":("🦅","🥁","🌴","⚽","🎭","🌶️"),"KE":("🦁","🌍","☕","🦒","🏃","🌺"),
    "ET":("☕","🌺","🦓","🏔️","🌾","⛪"),"GH":("🍫","🥁","🌴","⚽","🎭","🌊"),
    "TZ":("🦁","🏔️","🌴","🦒","☕","🌍"),"MA":("🕌","🍵","🐪","🌺","🏺","🌴"),
    "NZ":("🐑","🏉","🌿","🦜","🏔️","🌊"),"PH":("🏝️","🌺","🦅","🍚","🌴","🐟"),
    "ID":("🌋","🦜","🍚","🏝️","🛕","🌺"),"TH":("🛕","🐘","🌺","🍜","🏝️","🐊"),
    "VN":("🍜","🎋","🏮","🌾","⛵","🎎"),"KR":("🎎","🍱","🏯","🌸","🎮","⛷️"),
    "PL":("🦅","🌾","🥟","🏰","⛷️","🎻"),"AT":("⛷️","🎻","🏰","🍺","🧁","🌸"),
    "FI":("🎄","🦌","🏔️","❄️","☀️","🫐"),"NO":("🐋","⛷️","🌊","🦌","🌄","❄️"),
    "DK":("🧜","🍩","🚲","🌊","⚓","🧸"),"IS":("🌋","🐬","🌈","❄️","🐟","♨️"),
    "IE":("🍀","☘️","🏰","🎸","🐑","🍺"),"TN":("🕌","🏜️","🌊","🍋","🐫","☀️"),
    "DZ":("🌴","🏜️","🕌","🐫","🌾","☀️"),"CM":("🌴","🦁","☕","🥁","🌋","🌿"),
    "SN":("🌊","🥁","🌴","🎭","🦅","☀️"),"UG":("🦍","☕","🌺","🐊","🌍","🥁"),
    "MY":("🌴","🦧","🌺","🍜","🏙️","🦅"),"PK":("🕌","🏔️","🌾","🍵","🦅","🌹"),
    "BD":("🛶","🌾","🎎","🐊","🍵","🌺"),"LK":("🐘","🍵","🌺","🦚","🏝️","💎"),
}

COUNTRY_FACTS = {
    "FR":("Paris: 90 millions de touristes/an ! 🤯","Paris gets 90M tourists/year! 🤯"),
    "JP":("Le Japon a plus de 6 800 îles ! 🏝️","Japan has over 6,800 islands! 🏝️"),
    "CH":("La Suisse a 4 langues officielles ! 🗣️","Switzerland has 4 official languages! 🗣️"),
    "US":("Les USA ont 50 états ! 🗺️","The USA has 50 states! 🗺️"),
    "BR":("Le Brésil abrite 60% de l'Amazonie ! 🌳","Brazil holds 60% of the Amazon! 🌳"),
    "CN":("La Grande Muraille: 21 000 km ! 🧱","The Great Wall is 21,000 km long! 🧱"),
    "IN":("L'Inde a 22 langues officielles ! 🗣️","India has 22 official languages! 🗣️"),
    "AU":("L'Australie est aussi un continent ! 🌏","Australia is also a continent! 🌏"),
    "CA":("Le Canada a la plus longue côte du monde ! 🌊","Canada has the world's longest coastline! 🌊"),
    "DE":("L'Allemagne: 1500 types de bières ! 🍺","Germany has 1,500 types of beer! 🍺"),
    "IT":("L'Italie: plus de sites UNESCO au monde ! 🏛️","Italy has the most UNESCO sites! 🏛️"),
    "ES":("L'Espagne fait la sieste ! 💤","Spain invented the siesta! 💤"),
    "MX":("Le Mexique a inventé le chocolat chaud ! ☕","Mexico invented hot chocolate! ☕"),
    "EG":("Les pyramides ont 4 500 ans ! 🔺","The pyramids are 4,500 years old! 🔺"),
    "ZA":("L'Afrique du Sud a 3 capitales ! 🏛️","South Africa has 3 capitals! 🏛️"),
    "NG":("Nigeria: 1er pays d'Afrique en population ! 🌍","Nigeria is Africa's most populous country! 🌍"),
    "KE":("Le Kenya: les coureurs les plus rapides ! 🏃","Kenya has the world's fastest runners! 🏃"),
    "GB":("100 millions de tasses de thé/jour ! ☕","100 million cups of tea per day! ☕"),
    "NZ":("Plus de moutons que d'habitants ! 🐑","More sheep than people! 🐑"),
    "AR":("L'Argentine adore le tango ! 💃","Argentina loves the tango! 💃"),
    "TR":("Istanbul est sur 2 continents ! 🌍","Istanbul is on 2 continents! 🌍"),
    "SA":("Pas une seule rivière en Arabie ! 🏜️","Saudi Arabia has no rivers! 🏜️"),
    "TH":("40 000 temples en Thaïlande ! 🛕","Thailand has 40,000 temples! 🛕"),
    "PE":("Machu Picchu: 2 430 m d'altitude ! 🏔️","Machu Picchu is at 2,430m! 🏔️"),
    "CO":("Meilleur café du monde ! ☕","Some of the world's best coffee! ☕"),
    "GR":("La Grèce a plus de 6 000 îles ! ⛵","Greece has over 6,000 islands! ⛵"),
    "NL":("23M vélos pour 17M d'habitants ! 🚲","23M bikes for 17M people! 🚲"),
    "IS":("100% d'énergie renouvelable ! ♻️","100% renewable energy! ♻️"),
    "NO":("La Norvège a inventé le coupe-fromage ! 🧀","Norway invented the cheese slicer! 🧀"),
    "SE":("IKEA et ABBA viennent de Suède ! 🎵","Both IKEA and ABBA are from Sweden! 🎵"),
    "FI":("La Finlande: le pays le plus heureux ! 😊","Finland is the world's happiest country! 😊"),
    "KR":("Internet le plus rapide du monde ! 🌐","World's fastest internet! 🌐"),
    "AT":("Mozart est né en Autriche ! 🎻","Mozart was born in Austria! 🎻"),
    "PT":("Le pays le plus vieux d'Europe ! 🏰","The oldest country in Europe! 🏰"),
    "IE":("Le trèfle à 4 feuilles pour porte-bonheur ! ☘️","The four-leaf clover brings luck! ☘️"),
    "CL":("4 300 km de long — le plus long pays ! 📏","4,300 km long — the world's longest! 📏"),
    "PL":("Le plus grand château médiéval ! 🏰","The world's largest medieval castle! 🏰"),
    "MA":("Plus ancienne université: 859 ap. J.-C. ! 📚","World's oldest university: AD 859! 📚"),
    "PH":("Plus de 7 000 îles aux Philippines ! 🏝️","Over 7,000 islands! 🏝️"),
    "ID":("Le plus grand archipel du monde ! 🌊","The world's largest archipelago! 🌊"),
}

FEEDBACK_MESSAGES = {
    "word_match": {
        "ok":  ["Tu connais ce mot ! 📚 / You know this word! 📚",
                "Anglais top niveau ! 🇬🇧 / Top English level! 🇬🇧",
                "Vocabulaire excellent ! ✨ / Excellent vocabulary! ✨",
                "Bien joué ! 🌟 / Well played! 🌟"],
        "err": ["Presque ! Continue ! 💪 / Almost! Keep going! 💪",
                "Pas de souci, réessaie ! 🔄 / No worries, try again! 🔄",
                "Tu vas y arriver ! 🚀 / You'll get it! 🚀"],
    },
    "listen_spell": {
        "ok":  ["Tu as bien écouté ! 👂 / Great listening! 👂",
                "Orthographe parfaite ! ✅ / Perfect spelling! ✅",
                "Super oreille ! 🎧 / Super ear! 🎧"],
        "err": ["Écoute encore ! 🎧 / Listen again! 🎧",
                "Concentre-toi ! 🧠 / Focus! 🧠"],
    },
    "sentence_builder": {
        "ok":  ["Phrase parfaite ! 📝 / Perfect sentence! 📝",
                "Tu construis bien ! 🏗️ / Great building! 🏗️",
                "Grammaire top ! 🇬🇧 / Top grammar! 🇬🇧"],
        "err": ["Regarde les mots ! 👀 / Look at the words! 👀",
                "Réessaie ! 💪 / Try again! 💪"],
    },
    "flag_finder": {
        "ok":  ["Tu as reconnu le drapeau ! 🏳️🌟 / You spotted the flag! 🏳️🌟",
                "Géographe en herbe ! 🌍 / Budding geographer! 🌍",
                "Ce pays n'a plus de secret ! ✅ / That country has no secrets! ✅",
                "Super géo ! 🗺️ / Super geo! 🗺️"],
        "err": ["Le monde est grand ! 🌍 / The world is big! 🌍",
                "Apprends ce drapeau ! 🏳️ / Learn this flag! 🏳️"],
    },
    "capital_challenge": {
        "ok":  ["Tu connais les capitales ! 🏛️ / You know the capitals! 🏛️",
                "Explorateur mondial ! 🌐 / World explorer! 🌐",
                "Capital connaissance ! 🏙️ / Capital knowledge! 🏙️"],
        "err": ["Mémorise cette ville ! 🏙️ / Remember this city! 🏙️",
                "Continue d'explorer ! 🗺️ / Keep exploring! 🗺️"],
    },
    "continent_sorter": {
        "ok":  ["Bien trié ! 🗺️ / Well sorted! 🗺️","Géo-expert ! 🌍 / Geo-expert! 🌍"],
        "err": ["Regarde la carte ! 🗺️ / Look at the map! 🗺️"],
    },
    "number_blaster": {
        "ok":  ["Calcul éclair ! ⚡ / Lightning calculation! ⚡",
                "Chiffres magiques ! 🔢✨ / Magic numbers! 🔢✨",
                "Mathématicien ! 🧮 / Mathematician! 🧮",
                "Exact ! 🎯 / Exactly right! 🎯"],
        "err": ["Compte encore ! 🔢 / Count again! 🔢",
                "Presque ! 💪 / Almost! 💪"],
    },
    "count_objects": {
        "ok":  ["Tu comptes bien ! 🔢 / Great counting! 🔢",
                "Yeux de lynx ! 👀 / Eagle eyes! 👀",
                "Tout compté ! ✅ / All counted! ✅"],
        "err": ["Recompte ! 🔄 / Count again! 🔄","Un par un ! 👆 / One by one! 👆"],
    },
    "pattern_puzzle": {
        "ok":  ["Suite trouvée ! 🧩 / Pattern found! 🧩",
                "Logique parfaite ! 🧠 / Perfect logic! 🧠",
                "Génie des suites ! ⚡ / Pattern genius! ⚡"],
        "err": ["Cherche la règle ! 🔍 / Find the rule! 🔍","Regarde la suite ! 👀 / Look at the sequence! 👀"],
    },
}

COUNTING_EMOJIS = ["🍎","🐱","⭐","🌸","🎈","🐶","🍕","🦋","🚀","🍓"]
MATH_EMOJIS     = ["🍎","🌟","🐸","🏀","🦋","🍭","🚀","🐙","🎈","🦄"]

PATTERNS = [
    {"seq":[1,2,3,"__",5],  "ans":4,  "opts":[3,4,6],   "rule":"+1"},
    {"seq":[5,6,7,8,"__"],  "ans":9,  "opts":[9,10,7],  "rule":"+1"},
    {"seq":[10,"__",12,13,14],"ans":11,"opts":[11,9,15], "rule":"+1"},
    {"seq":[2,4,"__",8,10], "ans":6,  "opts":[5,6,7],   "rule":"+2"},
    {"seq":[1,3,5,"__",9],  "ans":7,  "opts":[6,7,8],   "rule":"+2"},
    {"seq":["__",4,6,8,10], "ans":2,  "opts":[1,2,3],   "rule":"+2"},
    {"seq":[3,6,9,"__",15], "ans":12, "opts":[11,12,13],"rule":"+3"},
    {"seq":[0,3,6,9,"__"],  "ans":12, "opts":[10,12,15],"rule":"+3"},
    {"seq":[5,10,"__",20,25],"ans":15,"opts":[14,15,16],"rule":"+5"},
    {"seq":[0,5,10,"__",20],"ans":15, "opts":[12,15,18],"rule":"+5"},
    {"seq":[1,2,4,"__",16], "ans":8,  "opts":[6,8,10],  "rule":"×2"},
    {"seq":[2,4,"__",16,32],"ans":8,  "opts":[7,8,9],   "rule":"×2"},
    {"seq":[10,8,"__",4,2], "ans":6,  "opts":[5,6,7],   "rule":"-2"},
    {"seq":[20,18,16,"__",12],"ans":14,"opts":[13,14,15],"rule":"-2"},
    {"seq":[4,8,12,16,"__"],"ans":20, "opts":[18,20,22],"rule":"+4"},
]

# ─────────────────────────────────────────────────────────────────────────────
# API — Countrylayer
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def _fetch_raw_countries(api_key: str) -> tuple:
    try:
        r = requests.get("https://api.countrylayer.com/v2/all",
                         params={"access_key": api_key}, timeout=8)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and "error" in data:
            return [], f"API error {data['error'].get('code','?')}: {data['error'].get('info','')}"
        return (data if isinstance(data, list) else []), ""
    except Exception as exc:
        return [], str(exc)


def load_countries() -> tuple:
    try:
        api_key = st.secrets["COUNTRYLAYER_API_KEY"]
    except Exception:
        return FALLBACK_COUNTRIES, "⚙️ secrets.toml not configured — using offline data"
    raw, err = _fetch_raw_countries(api_key)
    if err or not raw:
        return FALLBACK_COUNTRIES, err or "Empty response — using offline data"
    countries = []
    for item in raw:
        try:
            ll = item.get("latlng") or []
            if len(ll) < 2:
                continue
            a2   = item.get("alpha2Code") or ""
            tr   = item.get("translations") or {}
            curs = item.get("currencies") or [{}]
            langs = item.get("languages") or [{}]
            countries.append({
                "name_en": item.get("name") or "?",
                "name_fr": tr.get("fr") or item.get("name") or "?",
                "alpha2":  a2,
                "flag_emoji": code_to_flag(a2) if a2 else "🏳️",
                "capital":    item.get("capital") or "?",
                "lat": float(ll[0]), "lon": float(ll[1]),
                "region":    item.get("region") or "",
                "subregion": item.get("subregion") or "",
                "population": int(item.get("population") or 0),
                "area":          item.get("area"),
                "currency_name": curs[0].get("name","") if curs else "",
                "currency_symbol": curs[0].get("symbol","") if curs else "",
                "language_name": langs[0].get("name","") if langs else "",
            })
        except (TypeError, ValueError):
            continue
    return (countries if countries else FALLBACK_COUNTRIES), ""


# ─────────────────────────────────────────────────────────────────────────────
# PROFILE PERSISTENCE
# ─────────────────────────────────────────────────────────────────────────────
def _ensure_profiles_dir():
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)


def _profile_path(name: str) -> pathlib.Path:
    safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip() or "player"
    return PROFILES_DIR / f"{safe}.json"


def list_profiles() -> list:
    _ensure_profiles_dir()
    profiles = []
    for f in sorted(PROFILES_DIR.glob("*.json")):
        try:
            with open(f) as fh:
                profiles.append(json.load(fh))
        except Exception:
            pass
    return profiles


def save_profile():
    _ensure_profiles_dir()
    name = st.session_state.get("child_name") or "player"
    av   = st.session_state.get("avatar") or {}
    data = {
        "child_name":      name,
        "avatar_id":       av.get("id","fox"),
        "avatar_emoji":    av.get("emoji","🦊"),
        "total_stars":     st.session_state.get("total_stars", 0),
        "badge_id":        st.session_state.get("prev_badge_id", 1),
        "tab_scores":      st.session_state.get("tab_scores", {"english":0,"geo":0,"math":0}),
        "collectibles":    list(st.session_state.get("collectibles", set())),
        "errors_log":      st.session_state.get("errors_log", [])[-50:],
        "session_time_total": st.session_state.get("session_time_total", 0),
        "last_session":    str(_date.today()),
        "discovery_mode_seen": st.session_state.get("discovery_mode_seen", {}),
        "stories":         _load_existing_stories(name),
        "geo_countries_seen":  list(st.session_state.get("geo_countries_seen", [])),
        "english_words_seen":  list(st.session_state.get("english_words_seen", [])),
        "math_last_correct":   st.session_state.get("math_last_correct", ""),
    }
    try:
        with open(_profile_path(name), "w") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _load_existing_stories(name: str) -> list:
    try:
        with open(_profile_path(name)) as fh:
            return json.load(fh).get("stories", [])
    except Exception:
        return []


def load_profile(name: str) -> dict:
    try:
        with open(_profile_path(name)) as fh:
            return json.load(fh)
    except Exception:
        return {}


def delete_profile(name: str):
    try:
        _profile_path(name).unlink(missing_ok=True)
    except Exception:
        pass


def restore_from_profile(data: dict):
    st.session_state.child_name       = data.get("child_name", "")
    st.session_state.total_stars      = data.get("total_stars", 0)
    st.session_state.prev_badge_id    = data.get("badge_id", 1)
    st.session_state.tab_scores       = data.get("tab_scores", {"english":0,"geo":0,"math":0})
    st.session_state.collectibles     = set(data.get("collectibles", []))
    st.session_state.errors_log       = data.get("errors_log", [])
    st.session_state.session_time_total = data.get("session_time_total", 0)
    st.session_state.discovery_mode_seen = data.get("discovery_mode_seen", {})
    av_id = data.get("avatar_id", "fox")
    av    = next((a for a in AVATAR_LIST if a["id"] == av_id), AVATAR_LIST[0])
    st.session_state.avatar        = av
    st.session_state.avatar_chosen = True
    st.session_state.geo_countries_seen  = data.get("geo_countries_seen", [])
    st.session_state.english_words_seen  = data.get("english_words_seen", [])
    st.session_state.math_last_correct   = data.get("math_last_correct", "")


# ─────────────────────────────────────────────────────────────────────────────
# CROSS-TAB TRACKING HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _track_english_word(word: str):
    seen = list(st.session_state.get("english_words_seen", []))
    if word not in seen:
        seen = ([word] + seen)[:5]
    st.session_state.english_words_seen = seen


def _track_geo_country(name_fr: str):
    seen = list(st.session_state.get("geo_countries_seen", []))
    if name_fr not in seen:
        seen = seen + [name_fr]
    st.session_state.geo_countries_seen = seen


def _track_math(fact: str):
    st.session_state.math_last_correct = fact


# ─────────────────────────────────────────────────────────────────────────────
# AUDIO (gTTS optional)
# ─────────────────────────────────────────────────────────────────────────────
def speak(text: str, lang: str = "fr"):
    try:
        from gtts import gTTS
        import io as _io
        buf = _io.BytesIO()
        gTTS(text=text, lang=lang, slow=False).write_to_fp(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        st.markdown(
            f'<audio autoplay style="display:none">'
            f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
            unsafe_allow_html=True,
        )
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_STATE_DEFAULTS: dict = {
    # App flow
    "app_screen": "splash",   # splash | profiles | avatar | game
    "avatar_chosen": False, "avatar": None, "child_name": "",
    "dark_mode": False,
    "avatar_clicks": 0,
    # Profile
    "active_profile": None,
    "delete_confirm": None,
    # Gamification
    "total_stars": 0,
    "tab_scores": {"english":0,"geo":0,"math":0},
    "prev_badge_id": 1, "badge_just_unlocked": False,
    "collectibles": set(),
    "errors_log": [],
    # Session tracking
    "session_start": 0.0,
    "session_time_total": 0,
    "pause_shown": False,
    "session_items_this_round": {"words":0,"countries":0,"maths":0},
    # Adaptive difficulty
    "consec_errors": {"english":0,"geo":0,"math":0},
    "correct_streak": {"english":0,"geo":0,"math":0},
    "difficulty_level": {"english":1,"geo":1,"math":1},
    "slow_down_mode": {"english":False,"geo":False,"math":False},
    # Discovery mode seen
    "discovery_mode_seen": {},
    # Geo — API
    "countries": None, "api_error": "",
    # Map
    "geo_markers": [], "geo_zoom_lat": 20.0, "geo_zoom_lon": 0.0, "geo_zoom_scale": 1.0,
    # English — Word Match
    "wm_word": None,"wm_opts":[],"wm_score":0,"wm_lives":3,"wm_level":"easy",
    "wm_feedback":None,"wm_q":0,"wm_rq":0,"wm_rs":0,"wm_rdone":False,
    # English — Listen & Spell
    "ls_item":None,"ls_opts":[],"ls_score":0,"ls_hint":False,"ls_feedback":None,
    "ls_rq":0,"ls_rs":0,"ls_rdone":False,
    # English — Sentence Builder
    "sb_sentence":None,"sb_opts":[],"sb_score":0,"sb_feedback":None,
    "sb_rq":0,"sb_rs":0,"sb_rdone":False,
    # Geo — Flag Finder
    "ff_country":None,"ff_score":0,"ff_feedback":None,"ff_answered":False,
    "ff_rq":0,"ff_rs":0,"ff_rdone":False,
    # Geo — Capital Challenge
    "cc_country":None,"cc_opts":[],"cc_score":0,"cc_streak":0,"cc_hard":False,
    "cc_feedback":None,"cc_answered":False,"cc_rq":0,"cc_rs":0,"cc_rdone":False,
    # Geo — Continent Sorter
    "cs_countries":[],"cs_feedback":None,"cs_score":0,
    # Math — Number Blaster
    "nb_q":None,"nb_ans":0,"nb_op":"+","nb_a":0,"nb_b":0,
    "nb_round_score":0,"nb_q_num":0,"nb_feedback":None,"nb_done":False,
    "nb_rq":0,"nb_rs":0,"nb_rdone":False,
    # Math — Count the Objects
    "co_emoji":None,"co_count":0,"co_opts":[],"co_score":0,"co_feedback":None,
    "co_rq":0,"co_rs":0,"co_rdone":False,
    # Math — Pattern Puzzle
    "pp_pat":None,"pp_score":0,"pp_feedback":None,
    "pp_rq":0,"pp_rs":0,"pp_rdone":False,
    # Story tracking (cross-tab context)
    "geo_countries_seen":[],"english_words_seen":[],"math_last_correct":"",
    # Story tab state
    "story_generated":False,"story_cooldown":0.0,
    "current_story_raw":"","current_story_title":"","current_story_body":"",
}


def init_state():
    for k, v in _STATE_DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v.copy() if isinstance(v, (dict, set)) else v
    if st.session_state.countries is None:
        countries, err = load_countries()
        st.session_state.countries  = countries
        st.session_state.api_error  = err
    if st.session_state.session_start == 0.0:
        st.session_state.session_start = time.time()

# ─────────────────────────────────────────────────────────────────────────────
# CORE HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def add_stars(n: int, tab: str):
    old = st.session_state.total_stars
    st.session_state.total_stars += n
    st.session_state.tab_scores[tab] += n
    new = st.session_state.total_stars
    old_b = get_current_badge(old)
    new_b = get_current_badge(new)
    if new_b["id"] > old_b["id"]:
        st.session_state.badge_just_unlocked = True
        st.session_state.prev_badge_id = new_b["id"]
    # adaptive streak tracking
    st.session_state.correct_streak[tab] = st.session_state.correct_streak.get(tab, 0) + n
    st.session_state.consec_errors[tab]  = 0
    if st.session_state.slow_down_mode.get(tab) and st.session_state.correct_streak[tab] >= 3:
        st.session_state.slow_down_mode[tab]   = False
        st.session_state.correct_streak[tab]   = 0


def record_error(tab: str, game: str, question: str, wrong_ans: str):
    st.session_state.consec_errors[tab] = st.session_state.consec_errors.get(tab, 0) + 1
    st.session_state.correct_streak[tab] = 0
    if st.session_state.consec_errors[tab] >= 3:
        st.session_state.slow_down_mode[tab] = True
    st.session_state.errors_log.append({"game":game,"question":question,"wrong_answer":wrong_ans})


def get_current_badge(stars: int) -> dict:
    b = BADGES[0]
    for badge in BADGES:
        if stars >= badge["min_stars"]:
            b = badge
    return b


def get_next_badge(stars: int):
    cur = get_current_badge(stars)
    nxt = [b for b in BADGES if b["id"] > cur["id"]]
    return nxt[0] if nxt else None


def get_feedback(game_id: str, correct: bool) -> str:
    pool = FEEDBACK_MESSAGES.get(game_id, {}).get("ok" if correct else "err",
           ["Bien ! / Good!", "Réessaie ! / Try again!"])
    return random.choice(pool)


def banner_ok(fr: str, en: str):
    st.markdown(f'<div class="banner-ok">✅ {fr}<br>✅ {en}</div>', unsafe_allow_html=True)

def banner_err(fr: str, en: str):
    st.markdown(f'<div class="banner-err">❌ {fr}<br>❌ {en}</div>', unsafe_allow_html=True)

def show_feedback(fb):
    if not fb:
        return
    kind, fr, en = fb
    if kind == "ok":
        banner_ok(fr, en)
    else:
        banner_err(fr, en)


def show_slow_down(tab: str):
    if st.session_state.slow_down_mode.get(tab):
        st.markdown(
            '<div class="banner-info">🐢 On ralentit un peu... / Let\'s slow down a bit... 🐢💪</div>',
            unsafe_allow_html=True)


def show_on_fire(tab: str):
    streak = st.session_state.correct_streak.get(tab, 0)
    if streak > 0 and streak % 5 == 0:
        st.markdown(
            '<div class="banner-ok">🔥 Tu es en feu ! / You\'re on fire! 🔥</div>',
            unsafe_allow_html=True)


# Round helpers
ROUND_SIZE = 5

def round_stars_html(rs: int, rq: int) -> str:
    html = '<div class="round-bar">'
    for i in range(ROUND_SIZE):
        if i < rs:
            html += '<span class="rstar-full">⭐</span>'
        elif i < rq:
            html += '<span class="rstar-empty">☆</span>'
        else:
            html += '<span class="rstar-empty" style="opacity:.15;">☆</span>'
    html += '</div>'
    return html


def show_round_header(game_id: str, rq_key: str, rs_key: str):
    rq = st.session_state.get(rq_key, 0)
    rs = st.session_state.get(rs_key, 0)
    st.markdown(
        f'<div style="text-align:center;font-family:Fredoka One,cursive;font-size:1em;color:var(--text-secondary);">'
        f'Question {rq+1} / {ROUND_SIZE} 🎯</div>',
        unsafe_allow_html=True)
    st.markdown(round_stars_html(rs, rq), unsafe_allow_html=True)
    st.progress((rq) / ROUND_SIZE)


def show_round_end(rq_key, rs_key, rdone_key, restart_fn, tab: str):
    rs = st.session_state.get(rs_key, 0)
    if rs == ROUND_SIZE:
        st.markdown('<div class="banner-ok">🌟 PARFAIT ! / PERFECT! 🌟<br>5/5 ⭐⭐⭐⭐⭐</div>',
                    unsafe_allow_html=True)
        st.balloons()
    elif rs >= 3:
        st.markdown(f'<div class="banner-info">{rs}/5 ⭐ Super ! / Great! 🎉</div>',
                    unsafe_allow_html=True)
        st.snow()
    else:
        st.markdown(f'<div class="banner-err">{rs}/5 — Continue ! / Keep going! 💪</div>',
                    unsafe_allow_html=True)
    add_stars(rs, tab)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Round suivant / Next round", key=f"rnd_next_{rdone_key}", use_container_width=True):
            st.session_state[rq_key]    = 0
            st.session_state[rs_key]    = 0
            st.session_state[rdone_key] = False
            restart_fn()
            st.rerun()
    with col2:
        if st.button("🔁 Rejouer / Replay", key=f"rnd_replay_{rdone_key}", use_container_width=True):
            st.session_state[rq_key]    = 0
            st.session_state[rs_key]    = 0
            st.session_state[rdone_key] = False
            restart_fn()
            st.rerun()


def idk_button(key: str, correct_fr: str, correct_en: str, game_id: str, question: str):
    """'I don't know' button — reveals answer, logs error, no penalty."""
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🤷 Je ne sais pas / I don't know", key=f"idk_{key}"):
        record_error("", game_id, question, "__idk__")
        st.markdown(
            f'<div class="banner-idk">Pas de souci ! La réponse : {correct_fr}<br>'
            f'No worries! The answer: {correct_en}</div>',
            unsafe_allow_html=True)
        return True
    return False

# ─────────────────────────────────────────────────────────────────────────────
# PROFILE / SPLASH / AVATAR SCREENS
# ─────────────────────────────────────────────────────────────────────────────
def splash_screen():
    st.markdown(
        '<div class="kq-title" style="font-size:3.6em;margin-top:40px;">🎓 KidQuest Academy</div>',
        unsafe_allow_html=True)
    st.markdown(
        '<div class="kq-subtitle" style="font-size:1.4em;margin:8px 0 30px;">Apprends en jouant ! / Learn by playing! 🌟</div>',
        unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="tab-header-orange" style="font-size:1.5em;padding:30px;">🦊<br>English Quest</div>',
                    unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="tab-header-teal" style="font-size:1.5em;padding:30px;">🌍<br>Geo Explorer</div>',
                    unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="tab-header-green" style="font-size:1.5em;padding:30px;">🔢<br>Math Arena</div>',
                    unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("🚀 COMMENCER L'AVENTURE ! / START! 🚀", use_container_width=True, key="splash_start"):
            st.session_state.app_screen = "profiles"
            st.rerun()


def profile_selector():
    st.markdown('<div class="kq-title">👤 Qui joue ? / Who\'s playing?</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    profiles = list_profiles()
    if profiles:
        cols = st.columns(min(3, len(profiles)))
        for i, p in enumerate(profiles):
            with cols[i % 3]:
                badge = next((b for b in BADGES if b["id"] == p.get("badge_id", 1)), BADGES[0])
                st.markdown(
                    f'<div class="sb-card" style="font-size:1.1em;padding:18px;">'
                    f'<div style="font-size:3em;">{p.get("avatar_emoji","🦊")}</div>'
                    f'<div style="font-size:1.2em;">{p.get("child_name","?")}</div>'
                    f'{badge["emoji"]} {p.get("total_stars",0)} ⭐</div>',
                    unsafe_allow_html=True)
                if st.button(f"▶️ Jouer / Play", key=f"play_{p['child_name']}", use_container_width=True):
                    restore_from_profile(p)
                    st.session_state.app_screen = "game"
                    st.session_state.session_start = time.time()
                    st.rerun()
                # Delete with confirmation
                if st.session_state.delete_confirm == p["child_name"]:
                    if st.button("⚠️ Confirmer / Confirm 🗑️", key=f"del_confirm_{p['child_name']}", use_container_width=True):
                        delete_profile(p["child_name"])
                        st.session_state.delete_confirm = None
                        st.rerun()
                else:
                    if st.button("🗑️", key=f"del_{p['child_name']}", use_container_width=True):
                        st.session_state.delete_confirm = p["child_name"]
                        st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("Aucun profil — crée le tien ! / No profiles — create yours!")
    if len(profiles) < 3:
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            if st.button("➕ Nouveau joueur / New player", use_container_width=True, key="new_player"):
                st.session_state.app_screen = "avatar"
                st.rerun()


def avatar_picker():
    st.markdown(
        '<div class="kq-title">🎭 Choisis ton héros ! / Choose your hero! 🎭</div>',
        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    name = st.text_input(
        "Comment tu t'appelles ? / What is your name?",
        value=st.session_state.get("child_name", ""),
        max_chars=20, key="name_input_av")
    st.session_state.child_name = name
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, av in enumerate(AVATAR_LIST):
        with cols[i % 4]:
            st.markdown(
                f'<div style="text-align:center;font-size:72px;line-height:1;">{av["emoji"]}</div>'
                f'<div style="text-align:center;font-size:.9em;font-family:Fredoka One,cursive;">'
                f'{av["name_fr"]} / {av["name_en"]}</div>',
                unsafe_allow_html=True)
            if st.button("Choisir / Pick", key=f"av_{av['id']}", use_container_width=True):
                st.session_state.avatar        = av
                st.session_state.avatar_chosen = True
                st.session_state.app_screen    = "game"
                st.session_state.session_start = time.time()
                save_profile()
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# WORLD MAP
# ─────────────────────────────────────────────────────────────────────────────
def _set_map_country(country: dict, color: str = "#FFD93D", show_capital: bool = False):
    lat, lon = country.get("lat"), country.get("lon")
    if lat is None:
        return
    markers = [{"lat":lat,"lon":lon,"color":color,"size":20,"symbol":"star",
                "label":country["name_en"],"is_cap":False}]
    if show_capital and country.get("capital"):
        coords = CAPITAL_COORDS.get(country["name_en"])
        clat = coords[0] if coords else lat + 0.4
        clon = coords[1] if coords else lon + 0.4
        markers.append({"lat":clat,"lon":clon,"color":"#FFD93D","size":14,"symbol":"diamond",
                         "label":f"🏛 {country['capital']}","is_cap":True})
    st.session_state.geo_markers = markers
    reg = country.get("region","")
    if reg in REGION_ZOOM:
        zlat, zlon, zsc = REGION_ZOOM[reg]
        st.session_state.geo_zoom_lat   = lat * .55 + zlat * .45
        st.session_state.geo_zoom_lon   = lon * .55 + zlon * .45
        st.session_state.geo_zoom_scale = zsc
    else:
        st.session_state.geo_zoom_lat, st.session_state.geo_zoom_lon = lat, lon
        st.session_state.geo_zoom_scale = 3.0


def _set_map_countries(pairs: list):
    markers = []
    for country, ok in pairs:
        lat, lon = country.get("lat"), country.get("lon")
        if lat is None:
            continue
        markers.append({"lat":lat,"lon":lon,"color":"#2ecc71" if ok else "#e74c3c",
                         "size":18,"symbol":"star","label":country["name_en"],"is_cap":False})
    st.session_state.geo_markers    = markers
    st.session_state.geo_zoom_lat   = 20.0
    st.session_state.geo_zoom_lon   = 0.0
    st.session_state.geo_zoom_scale = 1.0


def render_world_map(dark_mode: bool = False):
    markers  = st.session_state.get("geo_markers", [])
    zoom_lat = st.session_state.get("geo_zoom_lat", 20.0)
    zoom_lon = st.session_state.get("geo_zoom_lon", 0.0)
    zoom_sc  = st.session_state.get("geo_zoom_scale", 1.0)
    fig = go.Figure()
    cm = [m for m in markers if not m.get("is_cap")]
    cp = [m for m in markers if     m.get("is_cap")]
    if cm:
        fig.add_trace(go.Scattergeo(lat=[m["lat"] for m in cm],lon=[m["lon"] for m in cm],
            text=[m["label"] for m in cm],mode="markers+text",
            marker=dict(size=[m["size"] for m in cm],symbol="star",
                        color=[m["color"] for m in cm],line=dict(width=2,color="white")),
            textposition="bottom center",textfont=dict(size=11,color="white"),
            hoverinfo="text",showlegend=False))
    if cp:
        fig.add_trace(go.Scattergeo(lat=[m["lat"] for m in cp],lon=[m["lon"] for m in cp],
            text=[m["label"] for m in cp],mode="markers+text",
            marker=dict(size=[m["size"] for m in cp],symbol="diamond",
                        color=[m["color"] for m in cp],line=dict(width=2,color="white")),
            textposition="top center",textfont=dict(size=10,color="#FFD93D"),
            hoverinfo="text",showlegend=False))
    if dark_mode:
        bg="#0F0F1A"; land="#2a3a4a"; ocean="#0F0F1A"; cc="#4a5a6a"
    else:
        bg="#f0f4ff"; land="#e8f4f8"; ocean="#b0d8f0"; cc="#8899aa"
    fig.update_layout(height=340,margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor=bg,
        geo=dict(projection=dict(type="natural earth",scale=zoom_sc),
                 center=dict(lat=zoom_lat,lon=zoom_lon),bgcolor=ocean,
                 landcolor=land,oceancolor=ocean,showocean=True,showland=True,
                 showlakes=False,showcountries=True,countrycolor=cc,countrywidth=.5,
                 showcoastlines=True,coastlinecolor=cc,coastlinewidth=.5),
        font=dict(color="white" if dark_mode else "#1A1A2E"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})


# ─────────────────────────────────────────────────────────────────────────────
# COUNTRY INFO CARD
# ─────────────────────────────────────────────────────────────────────────────
def render_country_card(country: dict):
    a2   = country.get("alpha2","")
    emojis = COUNTRY_EMOJI.get(a2, None)
    if emojis is None:
        emojis = (country.get("flag_emoji","🏳️"),) * 4
    fact = COUNTRY_FACTS.get(a2, None)
    pop  = country.get("population", 0)
    pop_s = f"{pop:,}" if pop else "?"
    area = country.get("area")
    area_s = f"{int(area):,} km²" if area else "?"
    cur  = country.get("currency_name","") or "?"
    cursym = country.get("currency_symbol","") or ""
    lang = country.get("language_name","") or "?"
    st.markdown(
        f'<div class="country-card">'
        f'<div style="font-size:.72em;color:var(--text-secondary);margin-bottom:6px;">ℹ️ Carte du pays / Country card</div>'
        f'<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start;">'
        f'<div style="flex:1;min-width:160px;">'
        f'<div style="font-size:64px;line-height:1;">{country.get("flag_emoji","🏳️")}</div>'
        f'<div style="font-size:1.15em;font-weight:bold;font-family:Fredoka One,cursive;">{country.get("name_en","?")} / {country.get("name_fr","?")}</div>'
        f'<div style="font-size:.9em;margin-top:4px;">🏛️ {country.get("capital","?")}</div>'
        f'<div style="font-size:.9em;">🌍 {country.get("region","?")}</div>'
        f'<div style="font-size:.9em;">🧑‍🤝‍🧑 {pop_s}</div>'
        f'<div style="font-size:.9em;">📐 {area_s}</div>'
        f'<div style="font-size:.9em;">💰 {cur} {cursym}</div>'
        f'<div style="font-size:.9em;">🗣️ {lang}</div>'
        f'</div>'
        f'<div style="flex:1;min-width:160px;">'
        f'<div style="font-size:36px;text-align:center;letter-spacing:4px;">{"".join(emojis)}</div>'
        + (f'<div style="font-size:.82em;font-style:italic;margin-top:6px;text-align:center;">{fact[0]}<br>{fact[1]}</div>' if fact else "")
        + f'</div></div></div>',
        unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MATH VISUAL AIDS
# ─────────────────────────────────────────────────────────────────────────────
def render_nb_visual_aid(op: str, a: int, b: int):
    obj = st.session_state.get("nb_visual_emoji", "🍎")
    st.markdown('<div class="aid-label">Aide visuelle 🔍 / Visual helper 🔍</div>', unsafe_allow_html=True)
    with st.container():
        if op == "+":
            a_rows = [obj * min(5, a - i*5) for i in range((a-1)//5 + 1)]
            b_rows = [obj * min(5, b - i*5) for i in range((b-1)//5 + 1)]
            col1, col2, col3, col4, col5 = st.columns([3,1,3,1,3])
            with col1:
                st.markdown(f'<div class="aid-panel" style="background:#dff5e3;text-align:center;font-size:1.8em;">{"<br>".join(a_rows)}</div>',
                            unsafe_allow_html=True)
            with col2:
                st.markdown('<div style="font-size:2em;text-align:center;padding-top:12px;">➕</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="aid-panel" style="background:#dde9ff;text-align:center;font-size:1.8em;">{"<br>".join(b_rows)}</div>',
                            unsafe_allow_html=True)
            with col4:
                st.markdown('<div style="font-size:2em;text-align:center;padding-top:12px;">=</div>', unsafe_allow_html=True)
            with col5:
                st.markdown('<div class="aid-panel" style="border:3px dashed #FF6B35;text-align:center;font-size:2.5em;padding:20px;">❓</div>',
                            unsafe_allow_html=True)
        else:
            total = [obj] * a
            crossed = set(range(a - b, a))
            parts = []
            for i, e in enumerate(total):
                if i in crossed:
                    parts.append(f'<span style="color:#e74c3c;text-decoration:line-through;font-size:1.6em;">{e}</span>')
                else:
                    parts.append(f'<span style="color:#27ae60;font-size:1.6em;">{e}</span>')
            st.markdown(f'<div class="aid-panel" style="text-align:center;line-height:1.8;">{"".join(parts)}</div>',
                        unsafe_allow_html=True)


def render_co_visual_aid(emoji: str, count: int):
    st.markdown('<div class="aid-label">Aide visuelle 🔍 / Visual helper 🔍</div>', unsafe_allow_html=True)
    rows = []
    full_rows = count // 5
    remainder = count % 5
    items = list(range(count))
    for row_i in range(full_rows + (1 if remainder else 0)):
        start = row_i * 5
        chunk = items[start:start+5]
        bg = "#dff5e3" if row_i % 2 == 0 else "#dde9ff"
        cells = st.columns(6)
        for ci, idx in enumerate(chunk):
            with cells[ci]:
                st.markdown(f'<div style="text-align:center;font-size:2em;background:{bg};border-radius:8px;padding:4px;">{emoji}</div>',
                            unsafe_allow_html=True)
        with cells[5]:
            st.markdown(f'<div style="text-align:center;font-size:1em;font-family:Fredoka One,cursive;padding-top:6px;">{min((row_i+1)*5, count)}</div>',
                        unsafe_allow_html=True)


def render_pp_visual_aid(pat: dict):
    seq = pat["seq"]
    rule = pat["rule"]
    st.markdown('<div class="aid-label">Aide visuelle 🔍 / Visual helper 🔍</div>', unsafe_allow_html=True)
    colors = ["#FF6B35","#4ECDC4","#FFD93D","#A8E6CF","#F093FB"]
    cols = st.columns(len(seq) * 2 - 1)
    for i, val in enumerate(seq):
        with cols[i * 2]:
            if val == "__":
                st.markdown(
                    '<div style="background:#fff;border:3px dashed #FF6B35;border-radius:12px;'
                    'text-align:center;font-size:1.6em;padding:8px 0;font-family:Fredoka One,cursive;">❓</div>',
                    unsafe_allow_html=True)
            else:
                bg = colors[i % len(colors)]
                st.markdown(
                    f'<div style="background:{bg};border-radius:12px;text-align:center;'
                    f'font-size:1.6em;padding:8px 0;color:white;font-family:Fredoka One,cursive;">{val}</div>',
                    unsafe_allow_html=True)
        if i < len(seq) - 1:
            with cols[i * 2 + 1]:
                st.markdown('<div style="text-align:center;font-size:1.4em;padding-top:8px;">→</div>', unsafe_allow_html=True)
    rule_label = f"{rule} chaque fois / each time"
    st.markdown(f'<div style="text-align:center;font-size:.9em;color:var(--text-secondary);margin-top:4px;">{rule_label}</div>',
                unsafe_allow_html=True)


def render_abacus():
    st.markdown("**🧮 Abaque / Abacus — Compte avec moi ! 🖐️ / Count with me! 🖐️**")
    val = st.slider("Valeur / Value", 0, 20, 0, key="abacus_val")
    if val > 0:
        chunks = []
        for i in range(0, val, 5):
            row_count = min(5, val - i)
            color = "🔵" if (i // 5) % 2 == 0 else "🔴"
            chunks.append(color * row_count)
        st.markdown(
            '<div style="font-size:2em;text-align:center;letter-spacing:4px;">'
            + "<br>".join(chunks) + '</div>',
            unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;font-size:1.2em;color:var(--text-secondary);">0</div>',
                    unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# BREAK ALERT  &  SESSION RECAP
# ─────────────────────────────────────────────────────────────────────────────
def check_break_alert():
    if st.session_state.pause_shown:
        return
    elapsed = time.time() - st.session_state.get("session_start", time.time())
    if elapsed > 600:
        st.session_state.pause_shown = True
        st.session_state.session_time_total += 600
        st.markdown(
            '<div class="break-overlay" style="background:linear-gradient(135deg,#a8edea,#fed6e3);">'
            '🧃 Pause !<br>Tu joues depuis 10 minutes.<br>'
            'Va boire un verre d\'eau ! 💧<br><br>'
            'Time for a break! You\'ve been playing 10 minutes.<br>'
            'Go drink some water! 💧'
            '</div>',
            unsafe_allow_html=True)
        if st.button("Je reviens ! / I'm back! 🎮", key="break_back"):
            st.session_state.session_start = time.time()
            st.rerun()
        st.stop()


def render_session_recap():
    st.markdown('<div class="kq-title" style="font-size:2em;">🏁 Bilan de session / Session recap</div>',
                unsafe_allow_html=True)
    s = st.session_state.get("session_items_this_round", {})
    badge = get_current_badge(st.session_state.total_stars)
    st.markdown(f"""
<div class="country-card" style="font-size:1.15em;">
  Aujourd'hui tu as... / Today you...<br><br>
  📚 {s.get("words",0)} mots appris / words learned<br>
  🌍 {s.get("countries",0)} pays découverts / countries found<br>
  🔢 {s.get("maths",0)} calculs réussis / math solved<br>
  ⭐ {st.session_state.total_stars} étoiles totales / total stars<br>
  {badge["emoji"]} {badge["name_fr"]} / {badge["name_en"]}<br>
</div>""", unsafe_allow_html=True)
    tab_scores = st.session_state.tab_scores
    st.bar_chart(tab_scores)
    if st.button("💾 Sauvegarder et quitter / Save & quit", key="session_save_quit"):
        save_profile()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# DISCOVERY MODE TOGGLE
# ─────────────────────────────────────────────────────────────────────────────
def discovery_toggle(game_id: str) -> bool:
    key = f"disc_{game_id}"
    seen = st.session_state.discovery_mode_seen.get(game_id, False)
    default = not seen
    val = st.toggle(
        "👀 Mode Découverte / Discovery Mode" if st.session_state.get(key, default) else "🎮 Mode Jeu / Play Mode",
        value=st.session_state.get(key, default),
        key=key)
    if val:
        st.markdown('<div class="disc-banner">👀 Mode Découverte actif — Explore sans pression ! / Explore freely!</div>',
                    unsafe_allow_html=True)
        st.session_state.discovery_mode_seen[game_id] = True
    return val


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — ENGLISH QUEST
# ─────────────────────────────────────────────────────────────────────────────

def _load_wm():
    pool = [w for w in WORD_PAIRS if w["lvl"] == st.session_state.wm_level]
    word = random.choice(pool)
    wrongs = random.sample([w for w in WORD_PAIRS if w["fr"] != word["fr"]], 3)
    opts = [w["fr"] for w in wrongs] + [word["fr"]]
    random.shuffle(opts)
    st.session_state.wm_word = word
    st.session_state.wm_opts = opts
    st.session_state.wm_q   += 1
    st.session_state.nb_visual_emoji = random.choice(MATH_EMOJIS)


def game_word_match():
    st.markdown("### 🔤 Choisis le mot ! / Pick the word! 🇬🇧")
    disc = discovery_toggle("word_match")

    lvl = st.radio("🎯 Niveau / Level:", ["easy","medium"], horizontal=True, key="_wm_lvl")
    if lvl != st.session_state.wm_level:
        st.session_state.wm_level = lvl
        st.session_state.wm_lives = 3
        st.session_state.wm_score = 0
        st.session_state.wm_feedback = None
        st.session_state.wm_rq = 0
        st.session_state.wm_rs = 0
        st.session_state.wm_rdone = False
        _load_wm()
        st.rerun()

    if st.session_state.wm_word is None:
        _load_wm()

    if st.session_state.wm_rdone:
        show_round_end("wm_rq","wm_rs","wm_rdone", _load_wm, "english")
        return

    show_round_header("word_match","wm_rq","wm_rs")
    show_slow_down("english")

    if not disc:
        col_l, col_r = st.columns([3,1])
        with col_l:
            lives = "❤️" * st.session_state.wm_lives + "🖤" * (3 - st.session_state.wm_lives)
            st.markdown(f'<div style="font-size:1.8em;text-align:center;">{lives}</div>', unsafe_allow_html=True)
        with col_r:
            st.markdown(f'<div class="score-line">⭐ {st.session_state.wm_score}</div>', unsafe_allow_html=True)

        if st.session_state.wm_lives <= 0:
            st.markdown('<div class="banner-err">😢 Partie terminée ! / Game Over!</div>', unsafe_allow_html=True)
            if st.button("🔄 Recommencer / Restart", key="wm_restart"):
                st.session_state.wm_lives = 3
                st.session_state.wm_score = 0
                st.session_state.wm_feedback = None
                st.session_state.wm_rq = 0
                st.session_state.wm_rs = 0
                st.session_state.wm_rdone = False
                _load_wm()
                st.rerun()
            return

    w = st.session_state.wm_word
    ctx = WORD_CONTEXT.get(w["en"])
    st.markdown(
        f'<div class="q-card">{w["emoji"]}<br>'
        f'<span style="color:#FF6B35;font-size:1.1em;">{w["en"]}</span>'
        + (f'<br><span style="font-size:.38em;color:#999;font-style:italic;">{ctx[0]}</span>' if ctx and not disc else "")
        + f'<br><span style="font-size:.38em;color:#bbb;">Traduction / Translation ?</span>'
        + (f'<br><span style="font-size:.45em;color:#4ECDC4;font-weight:bold;">{w["fr"]}</span>' if disc else "")
        + '</div>',
        unsafe_allow_html=True)

    if disc:
        for opt in st.session_state.wm_opts:
            info = next((x for x in WORD_PAIRS if x["fr"] == opt), None)
            note = f' — {info["en"]} {info["emoji"]}' if info else ""
            st.markdown(f'<div class="aid-panel">{opt}{note}</div>', unsafe_allow_html=True)
        if st.button("🎮 J'ai compris ! / I got it!", key="wm_disc_done"):
            st.session_state.discovery_mode_seen["word_match"] = True
            _load_wm()
            st.rerun()
        return

    cols = st.columns(2)
    q = st.session_state.wm_q
    for i, opt in enumerate(st.session_state.wm_opts):
        with cols[i % 2]:
            if st.button(f"🔤 {opt}", key=f"wm_{q}_{i}", use_container_width=True):
                if opt == w["fr"]:
                    st.session_state.wm_score += 1
                    st.session_state.wm_rs += 1
                    add_stars(0, "english")
                    _track_english_word(w["en"])
                    st.session_state.session_items_this_round["words"] = \
                        st.session_state.session_items_this_round.get("words",0) + 1
                    msg = get_feedback("word_match", True)
                    st.session_state.wm_feedback = ("ok", msg, msg)
                    st.balloons()
                else:
                    st.session_state.wm_lives -= 1
                    record_error("english","word_match",w["en"],opt)
                    msg = get_feedback("word_match", False)
                    st.session_state.wm_feedback = ("err", msg + f" ({w['fr']})", msg + f" ({w['fr']})")
                st.session_state.wm_rq += 1
                if st.session_state.wm_rq >= ROUND_SIZE:
                    st.session_state.wm_rdone = True
                else:
                    _load_wm()
                save_profile()
                st.rerun()

    idk_button(f"wm_{q}", w["fr"], w["fr"], "word_match", w["en"])
    show_feedback(st.session_state.wm_feedback)
    show_on_fire("english")


def game_listen_spell():
    st.markdown("### 🎧 Écoute ! / Listen! 🎧")
    disc = discovery_toggle("listen_spell")

    if st.session_state.ls_item is None:
        item = random.choice(SPELL_ITEMS)
        st.session_state.ls_item = item
        st.session_state.ls_opts = item["opts"][:]
        random.shuffle(st.session_state.ls_opts)

    if st.session_state.ls_rdone:
        show_round_end("ls_rq","ls_rs","ls_rdone",
                       lambda: setattr(st.session_state,"ls_item",None), "english")
        return

    show_round_header("listen_spell","ls_rq","ls_rs")
    show_slow_down("english")
    item = st.session_state.ls_item
    st.markdown(
        f'<div class="q-card">'
        f'<span style="font-size:1.2em;">{item["emoji"]}</span>'
        + (f'<br><span style="font-size:.5em;color:#4ECDC4;">✅ {item["name"]}</span>' if disc else "")
        + '<br><span style="font-size:.38em;color:#999;">Quel est ce mot ? / What is this word?</span>'
        + '</div>',
        unsafe_allow_html=True)

    if disc:
        for opt in item["opts"]:
            st.markdown(f'<div class="aid-panel">{opt}</div>', unsafe_allow_html=True)
        if st.button("🎮 J'ai compris ! / I got it!", key="ls_disc_done"):
            st.session_state.ls_item = None
            st.rerun()
        return

    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.ls_opts):
        with cols[i % 2]:
            if st.button(f"📝 {opt}", key=f"ls_{item['name']}_{i}", use_container_width=True):
                if opt == item["name"]:
                    st.session_state.ls_score += 1
                    st.session_state.ls_rs += 1
                    add_stars(0, "english")
                    _track_english_word(item["name"])
                    msg = get_feedback("listen_spell", True)
                    st.session_state.ls_feedback = ("ok", msg, msg)
                    st.balloons()
                else:
                    record_error("english","listen_spell",item["emoji"],opt)
                    msg = get_feedback("listen_spell", False)
                    st.session_state.ls_feedback = ("err", msg, msg)
                st.session_state.ls_rq += 1
                st.session_state.ls_item = None
                if st.session_state.ls_rq >= ROUND_SIZE:
                    st.session_state.ls_rdone = True
                save_profile()
                st.rerun()

    idk_button(f"ls_{item['name']}", item["name"], item["name"], "listen_spell", item["emoji"])
    show_feedback(st.session_state.ls_feedback)
    show_on_fire("english")


def game_sentence_builder():
    st.markdown("### 📝 Complète ! / Complete! 📝")
    disc = discovery_toggle("sentence_builder")

    if st.session_state.sb_sentence is None:
        s = random.choice(SENTENCES)
        st.session_state.sb_sentence = s
        opts = s["opts"][:]
        random.shuffle(opts)
        st.session_state.sb_opts = opts

    if st.session_state.sb_rdone:
        show_round_end("sb_rq","sb_rs","sb_rdone",
                       lambda: setattr(st.session_state,"sb_sentence",None), "english")
        return

    show_round_header("sentence_builder","sb_rq","sb_rs")
    show_slow_down("english")
    s   = st.session_state.sb_sentence
    ans = s["words"][s["blank"]]
    words_html = " ".join(
        f'<span style="color:#FF6B35;font-size:1.05em;background:#FFE5D9;padding:2px 10px;border-radius:10px;">___</span>'
        if i == s["blank"] else f'<span>{w}</span>'
        for i, w in enumerate(s["words"]))
    st.markdown(
        f'<div class="q-card">{words_html}'
        f'<br><span style="font-size:.4em;color:#999;font-style:italic;">{s["fr"]}</span>'
        + (f'<br><span style="font-size:.45em;color:#4ECDC4;font-weight:bold;">→ {ans}</span>' if disc else "")
        + '</div>',
        unsafe_allow_html=True)

    if disc:
        if st.button("🎮 J'ai compris ! / I got it!", key="sb_disc_done"):
            st.session_state.sb_sentence = None
            st.rerun()
        return

    cols = st.columns(3)
    for i, opt in enumerate(st.session_state.sb_opts):
        with cols[i]:
            if st.button(f"📝 {opt}", key=f"sb_{s['fr']}_{i}", use_container_width=True):
                if opt == ans:
                    st.session_state.sb_score += 1
                    st.session_state.sb_rs += 1
                    add_stars(0, "english")
                    _track_english_word(ans)
                    msg = get_feedback("sentence_builder", True)
                    st.session_state.sb_feedback = ("ok", msg, msg)
                    st.balloons()
                else:
                    record_error("english","sentence_builder"," ".join(s["words"]),opt)
                    msg = get_feedback("sentence_builder", False)
                    st.session_state.sb_feedback = ("err", msg + f" → {ans}", msg + f" → {ans}")
                st.session_state.sb_rq += 1
                st.session_state.sb_sentence = None
                if st.session_state.sb_rq >= ROUND_SIZE:
                    st.session_state.sb_rdone = True
                save_profile()
                st.rerun()

    idk_button(f"sb_{s['fr']}", ans, ans, "sentence_builder", " ".join(s["words"]))
    show_feedback(st.session_state.sb_feedback)
    show_on_fire("english")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — GEO EXPLORER
# ─────────────────────────────────────────────────────────────────────────────

def _load_ff():
    countries = st.session_state.countries or FALLBACK_COUNTRIES
    c = random.choice(countries)
    st.session_state.ff_country  = c
    st.session_state.ff_answered = False
    _set_map_country(c, color="#FFD93D")


def game_flag_finder():
    st.markdown("### 🏳️ Trouve le pays ! / Find the country! 🌍")
    disc = discovery_toggle("flag_finder")

    if st.session_state.ff_country is None:
        _load_ff()

    if st.session_state.ff_rdone:
        show_round_end("ff_rq","ff_rs","ff_rdone", _load_ff, "geo")
        return

    show_round_header("flag_finder","ff_rq","ff_rs")
    show_slow_down("geo")

    c = st.session_state.ff_country
    st.markdown(f'<div class="score-line">⭐ {st.session_state.ff_score}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:center;font-size:80px;line-height:1.1;margin:10px 0;">{c["flag_emoji"]}</div>'
        f'<div style="text-align:center;font-size:1.2em;font-family:Fredoka One,cursive;color:#4ECDC4;">'
        f'{c["name_en"]} / {c["name_fr"]}</div>',
        unsafe_allow_html=True)

    render_country_card(c)

    if disc:
        st.markdown(
            f'<div class="aid-panel"><b>Continent :</b> {REGION_LABELS.get(c["region"],c["region"])}</div>',
            unsafe_allow_html=True)
        if st.button("🎮 J'ai compris ! / I got it!", key="ff_disc_done"):
            _load_ff()
            st.rerun()
        return

    if st.session_state.ff_answered:
        show_feedback(st.session_state.ff_feedback)
        if st.button("▶️ Suivant / Next", key="ff_next", use_container_width=True):
            st.session_state.ff_rq += 1
            if st.session_state.ff_rq >= ROUND_SIZE:
                st.session_state.ff_rdone = True
            else:
                _load_ff()
            st.rerun()
        return

    countries    = st.session_state.countries or FALLBACK_COUNTRIES
    all_regions  = sorted({cc["region"] for cc in countries if cc.get("region")})
    cols = st.columns(min(3, len(all_regions)))
    for i, region in enumerate(all_regions):
        label = REGION_LABELS.get(region, region)
        with cols[i % len(cols)]:
            if st.button(label, key=f"ff_{c['name_en']}_{region}", use_container_width=True):
                if region == c["region"]:
                    st.session_state.ff_score += 1
                    st.session_state.ff_rs    += 1
                    add_stars(0, "geo")
                    st.session_state.collectibles.add(c.get("alpha2",""))
                    _track_geo_country(c.get("name_fr") or c["name_en"])
                    st.session_state.session_items_this_round["countries"] = \
                        st.session_state.session_items_this_round.get("countries",0) + 1
                    _set_map_country(c, color="#2ecc71")
                    msg = get_feedback("flag_finder", True)
                    st.session_state.ff_feedback = ("ok", msg, msg)
                    st.session_state.ff_answered = True
                    st.balloons()
                else:
                    record_error("geo","flag_finder",c["name_en"],region)
                    _set_map_country(c, color="#e74c3c")
                    msg = get_feedback("flag_finder", False)
                    correct_label = REGION_LABELS.get(c["region"], c["region"])
                    st.session_state.ff_feedback = ("err", msg + f" — {correct_label}", msg + f" — {correct_label}")
                    st.session_state.ff_answered = True
                save_profile()
                st.rerun()

    idk_button(f"ff_{c['name_en']}",
               REGION_LABELS.get(c["region"],c["region"]),
               c["region"], "flag_finder", c["name_en"])
    show_feedback(st.session_state.ff_feedback)
    show_on_fire("geo")


def _load_cc():
    countries = st.session_state.countries or FALLBACK_COUNTRIES
    pool = (countries if st.session_state.cc_hard
            else [cc for cc in countries if cc["name_en"] in EASY_CAPITAL_NAMES]) or countries
    country  = random.choice(pool)
    all_caps = [cc["capital"] for cc in countries if cc.get("capital") and cc["capital"] != "?"]
    wrongs   = random.sample([cap for cap in all_caps if cap != country["capital"]], min(3,len(all_caps)-1))
    opts = wrongs + [country["capital"]]
    random.shuffle(opts)
    st.session_state.cc_country  = country
    st.session_state.cc_opts     = opts
    st.session_state.cc_answered = False
    _set_map_country(country, color="#FFD93D", show_capital=True)


def game_capital_challenge():
    st.markdown("### 🏛️ Quelle capitale ? / What capital? 🏛️")
    disc = discovery_toggle("capital_challenge")

    if st.session_state.cc_country is None:
        _load_cc()

    if st.session_state.cc_rdone:
        show_round_end("cc_rq","cc_rs","cc_rdone", _load_cc, "geo")
        return

    show_round_header("capital_challenge","cc_rq","cc_rs")
    show_slow_down("geo")
    c = st.session_state.cc_country

    col_sc, col_str = st.columns(2)
    with col_sc:
        st.markdown(f'<div class="score-line">⭐ {st.session_state.cc_score}</div>', unsafe_allow_html=True)
    with col_str:
        flames = "🔥" * min(st.session_state.cc_streak, 5)
        st.markdown(f'<div class="score-line" style="text-align:left;">Série : {flames}</div>', unsafe_allow_html=True)

    pop = c.get("population", 0)
    pop_s = f"{pop:,}" if pop else "?"
    st.markdown(
        f'<div class="q-card q-card-teal">{c["flag_emoji"]}<br>'
        f'<span style="color:#4ECDC4;font-size:.7em;">{c["name_en"]} / {c["name_fr"]}</span><br>'
        f'<span style="font-size:.35em;color:#4ECDC4;">🧑‍🤝‍🧑 {pop_s}</span><br>'
        f'<span style="font-size:.38em;color:#999;">Capitale ? / Capital city?</span>'
        + (f'<br><span style="font-size:.45em;color:#2ecc71;font-weight:bold;">✅ {c["capital"]}</span>' if disc else "")
        + '</div>',
        unsafe_allow_html=True)

    render_country_card(c)

    if disc:
        if st.button("🎮 J'ai compris ! / I got it!", key="cc_disc_done"):
            _load_cc()
            st.rerun()
        return

    if st.session_state.cc_answered:
        show_feedback(st.session_state.cc_feedback)
        if st.button("▶️ Suivant / Next", key="cc_next", use_container_width=True):
            st.session_state.cc_rq += 1
            if st.session_state.cc_rq >= ROUND_SIZE:
                st.session_state.cc_rdone = True
            else:
                _load_cc()
            st.rerun()
        return

    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.cc_opts):
        with cols[i % 2]:
            if st.button(f"🏛️ {opt}", key=f"cc_{c['name_en']}_{i}", use_container_width=True):
                if opt == c["capital"]:
                    st.session_state.cc_score  += 1
                    st.session_state.cc_rs     += 1
                    st.session_state.cc_streak += 1
                    add_stars(0, "geo")
                    st.session_state.collectibles.add(c.get("alpha2",""))
                    _track_geo_country(c.get("name_fr") or c["name_en"])
                    st.session_state.session_items_this_round["countries"] = \
                        st.session_state.session_items_this_round.get("countries",0) + 1
                    _set_map_country(c, color="#2ecc71", show_capital=True)
                    if st.session_state.cc_streak >= 5 and not st.session_state.cc_hard:
                        st.session_state.cc_hard = True
                        msg = "🔓 Mode Expert débloqué ! / Expert Mode Unlocked! 🔥"
                    else:
                        msg = get_feedback("capital_challenge", True)
                    st.session_state.cc_feedback  = ("ok", msg, msg)
                    st.session_state.cc_answered  = True
                    st.balloons()
                else:
                    record_error("geo","capital_challenge",c["name_en"],opt)
                    st.session_state.cc_streak = 0
                    _set_map_country(c, color="#e74c3c", show_capital=True)
                    msg = get_feedback("capital_challenge", False)
                    st.session_state.cc_feedback = ("err", msg + f" → {c['capital']}", msg + f" → {c['capital']}")
                    st.session_state.cc_answered = True
                save_profile()
                st.rerun()

    idk_button(f"cc_{c['name_en']}", c["capital"], c["capital"], "capital_challenge", c["name_en"])
    show_feedback(st.session_state.cc_feedback)
    show_on_fire("geo")


def _load_cs():
    countries = st.session_state.countries or FALLBACK_COUNTRIES
    pool = [cc for cc in countries if cc.get("lat") is not None]
    st.session_state.cs_countries = random.sample(pool, min(5, len(pool)))
    st.session_state.cs_feedback  = None
    markers = []
    for cc in st.session_state.cs_countries:
        if cc.get("lat") is not None:
            markers.append({"lat":cc["lat"],"lon":cc["lon"],"color":"#FFD93D",
                             "size":18,"symbol":"star","label":cc["name_en"],"is_cap":False})
    st.session_state.geo_markers    = markers
    st.session_state.geo_zoom_lat   = 20.0
    st.session_state.geo_zoom_lon   = 0.0
    st.session_state.geo_zoom_scale = 1.0


def game_continent_sorter():
    st.markdown("### 🗺️ Trie les pays ! / Sort the countries! 🗺️")
    st.markdown('<div class="banner-info">🌍 Assigne chaque pays à son continent, puis CHECK !</div>',
                unsafe_allow_html=True)

    if not st.session_state.cs_countries:
        _load_cs()

    countries     = st.session_state.cs_countries
    all_countries = st.session_state.countries or FALLBACK_COUNTRIES
    region_opts   = sorted({cc["region"] for cc in all_countries if cc.get("region")})
    st.markdown(f'<div class="score-line">⭐ Score: {st.session_state.cs_score}</div>', unsafe_allow_html=True)

    for country in countries:
        c1, c2, c3 = st.columns([1,2,3])
        with c1:
            st.markdown(f'<div style="font-size:2em;text-align:center;">{country["flag_emoji"]}</div>',
                        unsafe_allow_html=True)
        with c2:
            st.markdown(
                f'<div style="font-size:1em;font-family:Fredoka One,cursive;padding-top:8px;">'
                f'{country["name_en"]}<br><span style="color:#999;font-size:.85em;">{country["name_fr"]}</span></div>',
                unsafe_allow_html=True)
        with c3:
            st.selectbox(f"Continent — {country['name_en']}", region_opts,
                         key=f"cs_{country['name_en']}", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    col_check, col_new = st.columns(2)
    with col_check:
        if st.button("🚀 CHECK", key="cs_check", use_container_width=True):
            results, n_ok = [], 0
            for country in countries:
                user_ans = st.session_state.get(f"cs_{country['name_en']}", region_opts[0] if region_opts else "")
                right    = country["region"]
                ok       = user_ans == right
                if ok:
                    n_ok += 1
                    st.session_state.collectibles.add(country.get("alpha2",""))
                else:
                    record_error("geo","continent_sorter",country["name_en"],user_ans)
                results.append((country["name_en"],country["flag_emoji"],user_ans,right,ok,country))
            add_stars(n_ok, "geo")
            st.session_state.cs_score   += n_ok
            st.session_state.cs_feedback = results
            _set_map_countries([(row[5], row[4]) for row in results])
            if n_ok == 5:
                st.balloons()
            save_profile()
            st.rerun()
    with col_new:
        if st.button("🔄 Nouveau round / New Round", key="cs_new", use_container_width=True):
            _load_cs()
            st.rerun()

    if st.session_state.cs_feedback:
        st.markdown("---")
        for name, flag, user_ans, right, ok, _ in st.session_state.cs_feedback:
            rl = REGION_LABELS.get(right, right)
            ul = REGION_LABELS.get(user_ans, user_ans)
            if ok:
                st.markdown(f'<div class="fb-ok">✅ {flag} {name} → {rl}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="fb-err">❌ {flag} {name} — {ul} | ✅ {rl}</div>',
                            unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — MATH ARENA
# ─────────────────────────────────────────────────────────────────────────────

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
    st.session_state.nb_op  = op
    st.session_state.nb_a   = a
    st.session_state.nb_b   = b
    st.session_state.nb_visual_emoji = random.choice(MATH_EMOJIS)


def game_number_blaster():
    st.markdown("### 💥 Calcule vite ! / Calculate fast! 💥")
    disc = discovery_toggle("number_blaster")

    if st.session_state.nb_done:
        s = st.session_state.nb_round_score
        stars = "⭐⭐⭐" if s >= 9 else "⭐⭐" if s >= 6 else "⭐"
        st.markdown(
            f'<div class="banner-ok">🎉 Round terminé ! Score: {s}/10 {stars}</div>',
            unsafe_allow_html=True)
        if st.button("🔄 Nouveau round / New Round", key="nb_restart"):
            st.session_state.nb_q_num       = 0
            st.session_state.nb_round_score = 0
            st.session_state.nb_done        = False
            st.session_state.nb_feedback    = None
            st.session_state.nb_rq          = 0
            st.session_state.nb_rs          = 0
            st.session_state.nb_rdone       = False
            _load_nb()
            st.rerun()
        return

    if st.session_state.nb_q is None:
        _load_nb()

    q_num = st.session_state.nb_q_num
    st.progress(q_num / 10, text=f"Question {q_num + 1} / 10")
    st.markdown(f'<div class="score-line">✅ {st.session_state.nb_round_score}/10</div>',
                unsafe_allow_html=True)

    st.markdown(
        f'<div class="q-card q-card-green" style="font-size:2.4em;">🔢 {st.session_state.nb_q}</div>',
        unsafe_allow_html=True)

    # Visual aid (always visible)
    render_nb_visual_aid(
        st.session_state.nb_op,
        st.session_state.nb_a,
        st.session_state.nb_b)

    if disc:
        st.markdown(
            f'<div class="aid-panel" style="text-align:center;font-size:1.6em;color:#2ecc71;">'
            f'✅ Réponse / Answer: <b>{st.session_state.nb_ans}</b></div>',
            unsafe_allow_html=True)
        if st.button("🎮 J'ai compris ! / I got it!", key="nb_disc_done"):
            _load_nb()
            st.rerun()
        # Abacus always available
        with st.expander("🧮 Abaque / Abacus"):
            render_abacus()
        return

    col_in, col_btn = st.columns([2, 1])
    with col_in:
        user_val = st.number_input(
            "Ta réponse / Your answer:", min_value=0, max_value=40,
            value=0, step=1, key=f"nb_input_{q_num}")
    with col_btn:
        st.write(""); st.write("")
        if st.button("✅ OK", key=f"nb_ok_{q_num}", use_container_width=True):
            correct = st.session_state.nb_ans
            if int(user_val) == correct:
                st.session_state.nb_round_score += 1
                st.session_state.nb_rs          += 1
                add_stars(0, "math")
                _track_math(st.session_state.nb_q)
                st.session_state.session_items_this_round["maths"] = \
                    st.session_state.session_items_this_round.get("maths",0) + 1
                msg = get_feedback("number_blaster", True)
                st.session_state.nb_feedback = ("ok", msg, msg)
                st.balloons()
            else:
                record_error("math","number_blaster",st.session_state.nb_q,str(user_val))
                msg = get_feedback("number_blaster", False)
                st.session_state.nb_feedback = ("err", msg + f" ({correct})", msg + f" ({correct})")
            st.session_state.nb_rq  += 1
            st.session_state.nb_q_num += 1
            if st.session_state.nb_q_num >= 10:
                st.session_state.nb_done = True
                bonus = 3 if st.session_state.nb_round_score >= 9 else 1 if st.session_state.nb_round_score >= 6 else 0
                if bonus:
                    add_stars(bonus, "math")
            else:
                _load_nb()
            save_profile()
            st.rerun()

    idk_button(f"nb_{q_num}", str(st.session_state.nb_ans), str(st.session_state.nb_ans),
               "number_blaster", st.session_state.nb_q)
    show_feedback(st.session_state.nb_feedback)
    show_on_fire("math")

    with st.expander("🧮 Abaque / Abacus"):
        render_abacus()


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
    st.markdown("### 🔢 Compte les objets ! / Count the objects! 🔢")
    disc = discovery_toggle("count_objects")

    if st.session_state.co_emoji is None:
        _load_co()

    if st.session_state.co_rdone:
        show_round_end("co_rq","co_rs","co_rdone", _load_co, "math")
        return

    show_round_header("count_objects","co_rq","co_rs")
    show_slow_down("math")

    emoji = st.session_state.co_emoji
    count = st.session_state.co_count
    st.markdown(f'<div class="score-line">⭐ {st.session_state.co_score}</div>', unsafe_allow_html=True)

    # Structured grid visual aid (always visible)
    render_co_visual_aid(emoji, count)

    st.markdown(
        '<div style="text-align:center;font-size:1.1em;font-family:Fredoka One,cursive;">'
        'Combien ? / How many?</div>', unsafe_allow_html=True)

    if disc:
        st.markdown(
            f'<div class="aid-panel" style="text-align:center;font-size:1.6em;color:#2ecc71;">'
            f'✅ {count} {emoji}</div>', unsafe_allow_html=True)
        if st.button("🎮 J'ai compris ! / I got it!", key="co_disc_done"):
            _load_co()
            st.rerun()
        return

    cols = st.columns(4)
    for i, opt in enumerate(st.session_state.co_opts):
        with cols[i]:
            if st.button(f"**{opt}**", key=f"co_{count}_{emoji}_{i}", use_container_width=True):
                if opt == count:
                    st.session_state.co_score += 1
                    st.session_state.co_rs    += 1
                    add_stars(0, "math")
                    _track_math(f"{count} {emoji} = {count}")
                    st.session_state.session_items_this_round["maths"] = \
                        st.session_state.session_items_this_round.get("maths",0) + 1
                    msg = get_feedback("count_objects", True)
                    st.session_state.co_feedback = ("ok", msg + f" — {count} {emoji*3}", msg + f" — {count} {emoji*3}")
                    st.balloons()
                else:
                    record_error("math","count_objects",f"{count}x{emoji}",str(opt))
                    msg = get_feedback("count_objects", False)
                    st.session_state.co_feedback = ("err", msg + f" ({count})", msg + f" ({count})")
                st.session_state.co_rq += 1
                _load_co()
                if st.session_state.co_rq >= ROUND_SIZE:
                    st.session_state.co_rdone = True
                save_profile()
                st.rerun()

    idk_button(f"co_{count}", f"{count} {emoji}", f"{count} {emoji}", "count_objects", f"count {emoji}")
    show_feedback(st.session_state.co_feedback)
    show_on_fire("math")

    with st.expander("🧮 Abaque / Abacus"):
        render_abacus()


def _load_pp():
    st.session_state.pp_pat = random.choice(PATTERNS)


def game_pattern_puzzle():
    st.markdown("### 🧩 Trouve le nombre ! / Find the number! 🧩")
    disc = discovery_toggle("pattern_puzzle")

    if st.session_state.pp_pat is None:
        _load_pp()

    if st.session_state.pp_rdone:
        show_round_end("pp_rq","pp_rs","pp_rdone", _load_pp, "math")
        return

    show_round_header("pattern_puzzle","pp_rq","pp_rs")
    show_slow_down("math")

    pat = st.session_state.pp_pat
    st.markdown(f'<div class="score-line">⭐ {st.session_state.pp_score}</div>', unsafe_allow_html=True)

    # Train track visual aid (always visible)
    render_pp_visual_aid(pat)

    if disc:
        st.markdown(
            f'<div class="aid-panel" style="text-align:center;font-size:1.6em;color:#2ecc71;">'
            f'✅ {pat["ans"]} (règle: {pat["rule"]})</div>', unsafe_allow_html=True)
        if st.button("🎮 J'ai compris ! / I got it!", key="pp_disc_done"):
            _load_pp()
            st.rerun()
        return

    cols = st.columns(3)
    for i, opt in enumerate(pat["opts"]):
        with cols[i]:
            if st.button(f"**{opt}**", key=f"pp_{pat['ans']}_{i}", use_container_width=True):
                if opt == pat["ans"]:
                    st.session_state.pp_score += 1
                    st.session_state.pp_rs    += 1
                    add_stars(0, "math")
                    _track_math(f"suite {pat['rule']} → {pat['ans']}")
                    st.session_state.session_items_this_round["maths"] = \
                        st.session_state.session_items_this_round.get("maths",0) + 1
                    msg = get_feedback("pattern_puzzle", True)
                    st.session_state.pp_feedback = ("ok", msg + f" ({pat['rule']})", msg + f" ({pat['rule']})")
                    st.balloons()
                else:
                    record_error("math","pattern_puzzle",str(pat["seq"]),str(opt))
                    msg = get_feedback("pattern_puzzle", False)
                    st.session_state.pp_feedback = ("err", msg + f" ({pat['ans']})", msg + f" ({pat['ans']})")
                st.session_state.pp_rq += 1
                _load_pp()
                if st.session_state.pp_rq >= ROUND_SIZE:
                    st.session_state.pp_rdone = True
                save_profile()
                st.rerun()

    idk_button(f"pp_{pat['ans']}", str(pat["ans"]), str(pat["ans"]), "pattern_puzzle", str(pat["seq"]))
    show_feedback(st.session_state.pp_feedback)
    show_on_fire("math")

    with st.expander("🧮 Abaque / Abacus"):
        render_abacus()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Dark mode toggle (must be first so theme applies immediately)
        dark = st.toggle("🌙 Mode Nuit / Night Mode",
                         value=st.session_state.get("dark_mode", False),
                         key="dark_mode_toggle")
        st.session_state.dark_mode = dark
        inject_theme_css(dark)

        st.divider()

        # Avatar card + name
        av  = st.session_state.get("avatar") or {}
        name = st.session_state.get("child_name") or "Joueur"
        av_emoji = av.get("emoji", "🦊")

        # Easter egg: count sidebar avatar clicks
        if st.button(av_emoji, key="sb_avatar_click", help="Clique sur ton avatar... 🤫"):
            st.session_state.avatar_clicks = st.session_state.get("avatar_clicks", 0) + 1
            if st.session_state.avatar_clicks >= 5:
                st.session_state.avatar_clicks = 0
                surprise = random.choice([
                    lambda: st.snow(),
                    lambda: (st.balloons(), st.toast("Abracadabra ! 🎩✨")),
                    lambda: st.toast("🌈 Magie ! / Magic! 🌈"),
                ])
                surprise()
            st.rerun()

        st.markdown(
            f'<div class="sb-card">'
            f'<div style="font-size:3em;line-height:1;">{av_emoji}</div>'
            f'<div style="font-size:1.1em;">{name}</div>'
            f'<div style="font-size:.8em;opacity:.8;">{av.get("name_fr","?")}</div>'
            f'</div>',
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Stars
        stars = st.session_state.total_stars
        st.markdown(
            f'<div class="sb-card">🌟 Étoiles / Stars<br>'
            f'<span style="font-size:2em;">{stars} ⭐</span></div>',
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Current badge (64px)
        badge = get_current_badge(stars)
        nxt   = get_next_badge(stars)
        st.markdown(
            f'<div class="sb-card" style="background:linear-gradient(135deg,{badge["color"]},{badge["color"]}cc);">'
            f'<div style="font-size:3em;">{badge["emoji"]}</div>'
            f'<div style="font-size:1em;">{badge["name_fr"]}<br>{badge["name_en"]}</div>'
            f'</div>',
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Progress bar to next badge
        if nxt:
            lo = badge["min_stars"]
            hi = nxt["min_stars"]
            pct = min((stars - lo) / max(hi - lo, 1), 1.0)
            st.markdown(
                f'<div style="font-size:.9em;font-family:Fredoka One,cursive;color:var(--text-secondary);">'
                f'🏅 Vers {nxt["emoji"]} {nxt["name_fr"]}</div>',
                unsafe_allow_html=True)
            st.progress(pct, text=f"{stars - lo} / {hi - lo} ⭐")
        else:
            st.markdown("👑 Maximum atteint ! / Maximum reached!", unsafe_allow_html=True)

        st.divider()

        # Per-tab scores
        st.markdown('<div style="font-size:1em;font-family:Fredoka One,cursive;margin-bottom:5px;">📊 Scores</div>',
                    unsafe_allow_html=True)
        for label, key, color in [("🦊 English","english","#FF6B35"),
                                   ("🌍 Geo","geo","#4ECDC4"),
                                   ("🔢 Maths","math","#A8E6CF")]:
            sc = st.session_state.tab_scores[key]
            st.markdown(
                f'<div class="sb-tab" style="background:{color}30;border-left:5px solid {color};">'
                f'{label}: <b>{sc} pts</b></div>',
                unsafe_allow_html=True)

        st.divider()

        # Trophy room
        with st.expander("🏆 Mes Trophées / My Trophies"):
            rows = [BADGES[:5], BADGES[5:]]
            for row in rows:
                cols = st.columns(5)
                for bi, badge_item in enumerate(row):
                    with cols[bi]:
                        unlocked = stars >= badge_item["min_stars"]
                        if unlocked:
                            st.markdown(
                                f'<div style="text-align:center;font-family:Fredoka One,cursive;">'
                                f'<div style="font-size:1.8em;">{badge_item["emoji"]}</div>'
                                f'<div style="font-size:.6em;color:{badge_item["color"]};">{badge_item["name_en"]}</div>'
                                f'</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(
                                f'<div style="text-align:center;color:#aaa;font-size:1.8em;">🔒</div>'
                                f'<div style="text-align:center;font-size:.6em;color:#aaa;">{badge_item["min_stars"]}⭐</div>',
                                unsafe_allow_html=True)

        # Collectibles
        with st.expander(f"🎴 Ma collection / My collection ({len(st.session_state.collectibles)} pays)"):
            if st.session_state.collectibles:
                all_c = st.session_state.countries or FALLBACK_COUNTRIES
                a2_map = {c.get("alpha2",""): c for c in all_c}
                cols = st.columns(3)
                for ci, a2 in enumerate(sorted(st.session_state.collectibles)):
                    cc = a2_map.get(a2)
                    if not cc:
                        continue
                    with cols[ci % 3]:
                        emojis = COUNTRY_EMOJI.get(a2, (cc.get("flag_emoji","🏳️"),) * 4)
                        pop = cc.get("population",0)
                        pop_s = f'{pop//1_000_000}M' if pop >= 1_000_000 else str(pop)
                        st.markdown(
                            f'<div style="text-align:center;font-size:.75em;font-family:Fredoka One,cursive;'
                            f'background:var(--bg-card);border-radius:10px;padding:6px;margin:3px;">'
                            f'<div style="font-size:2em;">{cc["flag_emoji"]}</div>'
                            f'{cc["name_en"]}<br>'
                            f'<span style="font-size:.8em;">{"".join(emojis[:4])}</span><br>'
                            f'<span style="font-size:.75em;color:var(--text-secondary);">{pop_s} · {cc.get("region","")}</span>'
                            f'</div>', unsafe_allow_html=True)
            else:
                st.caption("Joue en Geo Explorer pour collectionner des pays ! / Play Geo Explorer to collect countries!")

        # Session recap button
        st.divider()
        if st.button("🏁 Fin de session / End session", key="end_session", use_container_width=True):
            st.session_state.show_recap = True
            st.rerun()

        if st.button("🔄 Tout réinitialiser / Reset All", key="global_reset", use_container_width=True):
            save_profile()
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        # Switch player
        if st.button("👤 Changer de joueur / Switch player", key="switch_player", use_container_width=True):
            save_profile()
            st.session_state.app_screen    = "profiles"
            st.session_state.avatar_chosen = False
            st.rerun()

        # API diagnostic
        api_err = st.session_state.get("api_error","")
        if api_err:
            with st.expander("⚠️ API Diagnostic", expanded=False):
                st.caption("Mode hors-ligne actif / Offline mode active")
                st.code(api_err, language=None)

# ─────────────────────────────────────────────────────────────────────────────
# HISTOIRE DU SOIR — STORY TAB CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
STORY_SYSTEM_PROMPT = """Tu es Conteur des Rêves, un narrateur bienveillant et chaleureux pour enfants de 4 à 7 ans.
Tu crées des histoires du soir douces, apaisantes et éducatives.

Règles absolues :
- L'histoire dure exactement 250 à 320 mots.
- Elle se termine TOUJOURS par le héros qui s'endort paisiblement.
- Le ton est doux, lent, rassurant — comme un câlin en mots.
- La narration est principalement en français, simple (niveau CE1).
- Intègre naturellement 2 à 4 mots anglais du contexte, toujours traduits juste après entre parenthèses.
- Mentionne au moins 1 pays ou lieu géographique du contexte de façon poétique.
- Glisse une notion mathématique légère (compter, forme, taille) de façon ludique.
- Le héros est l'avatar de l'enfant — utilise son nom ET son emoji.
- Pas de suspense effrayant, pas de vilains, pas de danger réel.
- Structure : TITRE: [titre poétique sur une ligne]\n---\n[corps de l'histoire]
- Le titre est court (3 à 6 mots), poétique, en français.

Format de sortie STRICT :
TITRE: [titre]
---
[corps de l'histoire en 250-320 mots, se terminant par l'endormissement du héros]"""

FALLBACK_STORIES = {
    "fox": ("Le Renard et les Étoiles Dorées",
            "Dans la forêt silencieuse, le petit Renard 🦊 compta les étoiles — une, deux, trois… bientôt ses yeux se fermèrent tout doucement."),
    "cat": ("La Chatte et la Lune Argentée",
            "La petite Chatte 🐱 regarda la lune monter haut dans le ciel. Elle murmura *good night* (bonne nuit) à chaque étoile, puis s'endormit."),
    "dog": ("Le Chien et le Nuage Moelleux",
            "Le petit Chien 🐶 trouva un nuage doux comme un oreiller. Il s'y coucha, ferma les yeux, et rêva de prés verts et de papillons."),
    "bear": ("L'Ours et la Forêt Enchantée",
            "L'Ours 🐻 se promena dans la forêt magique jusqu'à trouver sa grotte parfaite. Il compta trois feuilles dorées et s'endormit."),
    "bunny": ("Le Lapin et les Carottes d'Or",
            "Le Lapin 🐰 rangea ses cinq carottes dans son terrier. Dehors, la nuit tombait. Il ferma les yeux en souriant doucement."),
    "owl": ("La Chouette et les Secrets de la Nuit",
            "La Chouette 🦉 gardienne de la nuit chuchota *sleep tight* (dors bien) à tous les animaux, puis posa la tête sur son aile."),
    "dino": ("Le Dinosaure et les Montagnes Roses",
            "Le petit Dino 🦕 traversa trois grandes montagnes roses au coucher du soleil. Épuisé et heureux, il s'allongea et s'endormit."),
    "robot": ("Le Robot et les Étoiles Binaires",
            "Le Robot 🤖 compta les étoiles : un, zéro, un, zéro… Ses circuits se mirent en veille, et il fit de beaux rêves électriques."),
    "princess": ("La Princesse et le Jardin Secret",
            "La Princesse 👸 cueillit sept fleurs magiques dans son jardin secret. Elle les compta, sourit, et s'endormit dans ses draps de soie."),
    "knight": ("Le Chevalier et le Dragon Gentil",
            "Le Chevalier 🧙 et son ami dragon firent la paix au bord du lac. Ensemble, ils s'endormirent sous un ciel étoilé."),
    "mermaid": ("La Sirène et les Perles Bleues",
            "La Sirène 🧜 plongea dans les eaux calmes et trouva cinq perles bleues. Elle les serra contre son cœur et s'endormit sous les vagues."),
    "astronaut": ("L'Astronaute et la Planète des Rêves",
            "L'Astronaute 👨‍🚀 flotta jusqu'à une petite planète bleue. Il dit *good night* (bonne nuit) à la Terre et ferma les yeux dans son vaisseau."),
}


def get_story_context() -> dict:
    return {
        "avatar":       st.session_state.get("avatar", AVATAR_LIST[0]),
        "child_name":   st.session_state.get("child_name", "ami"),
        "countries":    st.session_state.get("geo_countries_seen", [])[-3:],
        "eng_words":    st.session_state.get("english_words_seen", [])[:4],
        "math_fact":    st.session_state.get("math_last_correct", ""),
        "stars":        st.session_state.get("total_stars", 0),
    }


def build_user_prompt(ctx: dict) -> str:
    av   = ctx["avatar"]
    name = ctx["child_name"]
    parts = [f"Héros : {name}, avatar {av['emoji']} ({av['id']})."]
    if ctx["countries"]:
        parts.append(f"Pays vus aujourd'hui : {', '.join(ctx['countries'])}.")
    if ctx["eng_words"]:
        parts.append(f"Mots anglais appris : {', '.join(ctx['eng_words'])}.")
    if ctx["math_fact"]:
        parts.append(f"Dernière réussite maths : {ctx['math_fact']}.")
    parts.append(f"{name} a gagné {ctx['stars']} étoiles aujourd'hui.")
    parts.append("Crée une histoire du soir douce et apaisante.")
    return " ".join(parts)


def parse_story(raw: str) -> tuple[str, str]:
    if "---" in raw:
        header, _, body = raw.partition("---")
        title = header.replace("TITRE:", "").strip().strip('"').strip("'")
        return title, body.strip()
    lines = raw.strip().splitlines()
    title = lines[0].replace("TITRE:", "").strip() if lines else "Histoire du Soir"
    body  = "\n".join(lines[1:]).strip()
    return title, body


def highlight_story(body: str, ctx: dict) -> str:
    result = body
    for w in ctx.get("eng_words", []):
        result = re.sub(
            rf"\b({re.escape(w)})\b",
            r'<span style="color:#f59e0b;font-weight:700">\1</span>',
            result, flags=re.IGNORECASE
        )
    for c in ctx.get("countries", []):
        result = re.sub(
            rf"\b({re.escape(c)})\b",
            r'<span style="color:#0d9488;font-weight:700">\1</span>',
            result, flags=re.IGNORECASE
        )
    result = re.sub(
        r"\b(\d+)\b",
        r'<span style="color:#16a34a;font-weight:700">\1</span>',
        result
    )
    return result.replace("\n", "<br>")


def render_book_card(title: str, body_html: str, cursor: bool = False):
    cursor_html = '<span class="story-cursor">▌</span>' if cursor else ""
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);
            border-radius:16px;padding:24px 28px;margin:12px 0;
            border:2px solid #6366f1;box-shadow:0 4px 20px rgba(99,102,241,0.3)">
  <div style="color:#fbbf24;font-size:1.2em;font-weight:700;
              margin-bottom:14px;text-align:center">📖 {title}</div>
  <div style="color:#e0e7ff;line-height:1.9;font-size:1.05em">{body_html}{cursor_html}</div>
</div>
""", unsafe_allow_html=True)


def generate_story_streaming(ctx: dict):
    if _anthropic is None:
        st.error("📦 Package `anthropic` manquant. Installe : `pip install anthropic`")
        return
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        st.error("🔑 Clé API Anthropic manquante dans `.streamlit/secrets.toml`.")
        return

    client = _anthropic.Anthropic(api_key=api_key)
    prompt = build_user_prompt(ctx)

    placeholder = st.empty()
    full_text   = ""
    try:
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=STORY_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for chunk in stream.text_stream:
                full_text += chunk
                title_live, body_live = parse_story(full_text)
                body_html = highlight_story(body_live, ctx)
                with placeholder:
                    render_book_card(title_live, body_html, cursor=True)
    except Exception as e:
        st.error(f"❌ Erreur génération : {e}")
        return

    title, body = parse_story(full_text)
    with placeholder:
        render_book_card(title, highlight_story(body, ctx), cursor=False)

    st.session_state.current_story_raw   = full_text
    st.session_state.current_story_title = title
    st.session_state.current_story_body  = body
    st.session_state.story_generated     = True
    st.session_state.story_cooldown      = time.time()

    # Persist to profile (max 10 stories)
    child_name = ctx["child_name"]
    existing   = _load_existing_stories(child_name)
    new_entry  = {
        "date":  str(_date.today()),
        "title": title,
        "body":  body,
        "avatar": ctx["avatar"].get("emoji", "🦊"),
    }
    updated = ([new_entry] + existing)[:10]
    try:
        path = _profile_path(child_name)
        with open(path) as fh:
            prof = json.load(fh)
    except Exception:
        prof = {}
    prof["stories"] = updated
    try:
        _ensure_profiles_dir()
        with open(_profile_path(child_name), "w") as fh:
            json.dump(prof, fh, ensure_ascii=False, indent=2)
    except Exception:
        pass


def tab_histoire_du_soir():
    st.markdown('<div class="tab-header-orange">🌙 Histoire du Soir — Dors bien ! / Sleep tight!</div>',
                unsafe_allow_html=True)

    av   = st.session_state.get("avatar", AVATAR_LIST[0])
    name = st.session_state.get("child_name", "ami")
    ctx  = get_story_context()

    st.markdown(f"### {av['emoji']} Bonsoir, **{name}** ! Prêt·e pour ton histoire ?")

    # Show context summary
    with st.expander("🎒 Ton aventure d'aujourd'hui / Today's adventure", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌍 Pays explorés", len(ctx["countries"]))
            if ctx["countries"]:
                st.caption(", ".join(ctx["countries"]))
        with col2:
            st.metric("🦊 Mots anglais", len(ctx["eng_words"]))
            if ctx["eng_words"]:
                st.caption(", ".join(ctx["eng_words"]))
        with col3:
            st.metric("⭐ Étoiles", ctx["stars"])
            if ctx["math_fact"]:
                st.caption(ctx["math_fact"])

    st.divider()

    # Cooldown check
    cooldown_left = 0
    last_gen = st.session_state.get("story_cooldown", 0.0)
    if last_gen:
        elapsed = time.time() - last_gen
        cooldown_left = max(0, 30 - int(elapsed))

    col_gen, col_read = st.columns([2, 1])
    with col_gen:
        if cooldown_left > 0:
            st.info(f"⏳ Attends encore {cooldown_left}s avant une nouvelle histoire…")
            gen_disabled = True
        else:
            gen_disabled = False

        if st.button("✨ Génère mon histoire du soir !", disabled=gen_disabled,
                     use_container_width=True, type="primary"):
            st.session_state.story_generated = False
            generate_story_streaming(ctx)
            st.rerun()

    with col_read:
        if st.session_state.get("story_generated") and st.session_state.get("current_story_body"):
            if st.button("🔊 Lire à voix haute", use_container_width=True):
                speak(st.session_state.current_story_body, lang="fr")
        else:
            # Fallback story button
            av_id = av.get("id", "fox")
            fb = FALLBACK_STORIES.get(av_id, list(FALLBACK_STORIES.values())[0])
            if st.button("📖 Histoire surprise !", use_container_width=True):
                st.session_state.current_story_title = fb[0]
                st.session_state.current_story_body  = fb[1]
                st.session_state.story_generated     = True
                st.rerun()

    # Display current story
    if st.session_state.get("story_generated") and st.session_state.get("current_story_body"):
        render_book_card(
            st.session_state.current_story_title,
            highlight_story(st.session_state.current_story_body, ctx),
            cursor=False,
        )
        if st.button("🌟 Nouvelle histoire", use_container_width=False):
            st.session_state.story_generated     = False
            st.session_state.current_story_raw   = ""
            st.session_state.current_story_title = ""
            st.session_state.current_story_body  = ""
            st.rerun()

    st.divider()

    # Saved stories library
    saved = _load_existing_stories(name)
    if saved:
        st.markdown("### 📚 Tes histoires sauvegardées / Your saved stories")
        for s in saved:
            with st.expander(f"{s.get('avatar','📖')} {s.get('title','Histoire')} — {s.get('date','')}"):
                st.markdown(highlight_story(s.get("body",""), ctx), unsafe_allow_html=True)
                if st.button("🔊 Écouter", key=f"listen_{s.get('date','')}_{s.get('title','')}"):
                    speak(s.get("body",""), lang="fr")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    init_state()

    # Theme CSS (dark_mode may be set before sidebar renders)
    inject_theme_css(st.session_state.get("dark_mode", False))

    # Badge unlock celebration (shown before anything else)
    if st.session_state.get("badge_just_unlocked"):
        b = get_current_badge(st.session_state.total_stars)
        st.markdown(
            f'<div style="background:{b["color"]};border-radius:24px;padding:28px;text-align:center;'
            f'font-family:Fredoka One,cursive;margin-bottom:16px;">'
            f'<div style="font-size:4em;">{b["emoji"]}</div>'
            f'<div style="font-size:1.8em;color:white;">{b["name_fr"]} !</div>'
            f'<div style="font-size:1.2em;color:white;">{b["name_en"]}!</div>'
            f'<div style="font-size:1em;color:rgba(255,255,255,.85);margin-top:6px;">'
            f'{b["desc_fr"]}<br>{b["desc_en"]}</div>'
            f'</div>',
            unsafe_allow_html=True)
        st.balloons()
        st.session_state.badge_just_unlocked = False

    # ── App flow routing ──
    screen = st.session_state.get("app_screen", "splash")

    if screen == "splash":
        splash_screen()
        return

    if screen == "profiles":
        profile_selector()
        return

    if screen == "avatar":
        avatar_picker()
        return

    # ── Main game view ──
    render_sidebar()
    check_break_alert()

    # Session recap overlay
    if st.session_state.get("show_recap"):
        render_session_recap()
        if st.button("◀️ Retour / Back", key="back_from_recap"):
            st.session_state.show_recap = False
            st.rerun()
        return

    # Title
    av = st.session_state.get("avatar") or {}
    name = st.session_state.get("child_name") or ""
    greeting = f"{av.get('emoji','')} {name} !" if name else "🎓 KidQuest Academy"
    st.markdown(f'<div class="kq-title">{greeting}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="kq-subtitle">Apprends en t\'amusant ! / Learn while having fun! 🌟</div>',
        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🦊 English Quest", "🌍 Geo Explorer", "🔢 Math Arena", "🌙 Histoire du Soir"])

    with tab1:
        st.markdown('<div class="tab-header-orange">🦊 English Quest — Apprends l\'anglais ! / Learn English!</div>',
                    unsafe_allow_html=True)
        game = st.radio("🎮 Choisis / Choose:", ["🔤 Word Match","🎧 Listen & Spell","📝 Sentence Builder"],
                        horizontal=True, key="eng_game")
        st.divider()
        if game == "🔤 Word Match":
            game_word_match()
        elif game == "🎧 Listen & Spell":
            game_listen_spell()
        else:
            game_sentence_builder()

    with tab2:
        st.markdown('<div class="tab-header-teal">🌍 Geo Explorer — Explore le monde ! / Explore the world!</div>',
                    unsafe_allow_html=True)
        dark = st.session_state.get("dark_mode", False)
        render_world_map(dark_mode=dark)
        game = st.radio("🎮 Choisis / Choose:", ["🏳️ Flag Finder","🏛️ Capital Challenge","🗺️ Continent Sorter"],
                        horizontal=True, key="geo_game")
        st.divider()
        if game == "🏳️ Flag Finder":
            game_flag_finder()
        elif game == "🏛️ Capital Challenge":
            game_capital_challenge()
        else:
            game_continent_sorter()

    with tab3:
        st.markdown('<div class="tab-header-green">🔢 Math Arena — Maîtrise les maths ! / Master math!</div>',
                    unsafe_allow_html=True)
        game = st.radio("🎮 Choisis / Choose:", ["💥 Number Blaster","🔢 Count the Objects","🧩 Pattern Puzzle"],
                        horizontal=True, key="math_game")
        st.divider()
        if game == "💥 Number Blaster":
            game_number_blaster()
        elif game == "🔢 Count the Objects":
            game_count_objects()
        else:
            game_pattern_puzzle()

    with tab4:
        tab_histoire_du_soir()


if __name__ == "__main__":
    main()
