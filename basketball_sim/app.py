import os
import re
import sys
import random

import streamlit as st

# Hosts differ on what they put on sys.path for the entrypoint, so put this app's
# own directory first and make sure it wins over anything installed.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE in sys.path:
    sys.path.remove(_HERE)
sys.path.insert(0, _HERE)

from nba_dream.player import Player, xp_for_level, RETIREMENT_AGE
from nba_dream.leagues import LEAGUES, COUNTRIES, POSITIONS, get_next_league
from nba_dream.teams import (ROLES, generate_team_offers, generate_draft_offers,
                             strength_label, market_value)
from nba_dream.sponsors import (generate_sponsor_offers, sponsor_income,
                                MAX_ACTIVE_SPONSORS, TIER_COLORS)
from nba_dream.tactics import TACTICS, fit_score, fit_label
from nba_dream.interviews import pick_interview, apply_answer, SENTIMENT_ICON
from nba_dream.simulator import (run_season, run_draft, check_promotion_eligibility,
                                 is_nba_ready, draft_eligibility_age,
                                 can_enter_draft, can_sign_nba_contract, DRAFT_MAX_AGE)

st.set_page_config(page_title="NBA Dream — Career Simulator", page_icon="🏀",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@700&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background:
      radial-gradient(1200px 600px at 50% -10%, #1b1206 0%, transparent 60%),
      #0a0a0c !important;
    color:#ededed !important; font-family:'Inter',sans-serif !important;
}
[data-testid="stHeader"] { background:transparent !important; }
.block-container { padding:1.2rem 2rem !important; max-width:1240px; margin:auto; }
h1,h2,h3 { color:#fff !important; font-family:'Barlow Condensed',sans-serif !important;
           letter-spacing:.01em; text-transform:uppercase; }

/* ── Hardwood court panel ─────────────────────────────────────── */
.court {
    position:relative; overflow:hidden; border-radius:14px; padding:1.3rem 1.6rem; margin-bottom:1rem;
    background:
      repeating-linear-gradient(90deg, rgba(0,0,0,.16) 0 2px, transparent 2px 46px),
      linear-gradient(140deg,#8a5a24 0%,#b07a35 40%,#7d4f1f 100%);
    border:1px solid #3a2410;
    box-shadow:inset 0 0 90px rgba(0,0,0,.55), 0 6px 24px rgba(0,0,0,.5);
}
.court::after {
    content:""; position:absolute; right:-70px; top:50%; transform:translateY(-50%);
    width:230px; height:230px; border:3px solid rgba(255,255,255,.16); border-radius:50%;
}
.court::before {
    content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:rgba(255,255,255,.16);
}
.court-inner { position:relative; z-index:1; }

/* ── Cards ────────────────────────────────────────────────────── */
.card       { background:linear-gradient(150deg,#141418,#1c1c24); border:1px solid #2e2e3a; border-radius:12px; padding:1.1rem 1.3rem; margin-bottom:.9rem; }
.card-gold  { background:linear-gradient(150deg,#1d1503,#2e2205); border:1px solid #d08a1e; border-radius:12px; padding:1.1rem 1.3rem; margin-bottom:.9rem; }
.card-red   { background:linear-gradient(150deg,#1d0505,#2c0b0b); border:1px solid #e0492c; border-radius:12px; padding:1.1rem 1.3rem; margin-bottom:.9rem; }
.card-green { background:linear-gradient(150deg,#04180c,#0a2a16); border:1px solid #2fa35c; border-radius:12px; padding:1.1rem 1.3rem; margin-bottom:.9rem; }
.offer-card { background:linear-gradient(150deg,#141418,#1e1e28); border:1px solid #2e2e3a; border-left:5px solid #e07a1e;
              border-radius:10px; padding:1rem 1.1rem; margin-bottom:.7rem; min-height:230px; }

/* ── Jersey + scoreboard ──────────────────────────────────────── */
.jersey { display:inline-flex; flex-direction:column; align-items:center; justify-content:center;
          width:62px; height:70px; border-radius:8px 8px 16px 16px; background:linear-gradient(160deg,#e07a1e,#a8500c);
          border:2px solid #2a1806; box-shadow:0 4px 14px rgba(0,0,0,.5); }
.jersey-num { font-family:'Barlow Condensed',sans-serif; font-size:2rem; font-weight:800; color:#fff; line-height:1; }
.jersey-pos { font-size:.6rem; font-weight:700; color:#2a1806; letter-spacing:.08em; }

.scoreboard { background:#08080a; border:2px solid #2c2c36; border-radius:10px; padding:.75rem;
              display:grid; grid-template-columns:repeat(auto-fit,minmax(78px,1fr)); gap:.55rem;
              box-shadow:inset 0 0 26px rgba(224,122,30,.09); margin:.7rem 0; }
.sb-cell  { text-align:center; padding:.3rem .2rem; }
.sb-value { font-family:'JetBrains Mono',monospace; font-size:1.35rem; font-weight:700; color:#ffa53a;
            text-shadow:0 0 12px rgba(255,165,58,.45); line-height:1.2; }
.sb-label { font-size:.6rem; color:#8a8a96; text-transform:uppercase; letter-spacing:.1em; margin-top:2px; }

/* ── Bars ─────────────────────────────────────────────────────── */
.attr-row   { margin:.35rem 0; }
.attr-label { font-size:.78rem; color:#a8a8b4; display:flex; justify-content:space-between; margin-bottom:3px; }
.bar-bg     { background:#202028; border-radius:4px; height:8px; overflow:hidden; }
.bar-fill   { height:100%; border-radius:4px; }
.xp-fill    { background:linear-gradient(90deg,#7b2fbe,#d054ff); }

/* ── Badges ───────────────────────────────────────────────────── */
.badge { display:inline-block; padding:.2rem .55rem; border-radius:4px; font-size:.68rem; font-weight:700;
         text-transform:uppercase; letter-spacing:.06em; margin:2px 3px 2px 0; }
.badge-orange{ background:#e07a1e; color:#1a1005; }
.badge-blue  { background:#1e6aa8; color:#fff; }
.badge-red   { background:#c0392b; color:#fff; }
.badge-green { background:#27ae60; color:#fff; }
.badge-gray  { background:#33333d; color:#c8c8d2; }
.badge-purple{ background:#7b2fbe; color:#fff; }

.title-nba { font-family:'Barlow Condensed',sans-serif; font-size:3.4rem; font-weight:800; text-align:center;
             letter-spacing:.02em; background:linear-gradient(90deg,#e07a1e,#fff 50%,#e07a1e);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
             line-height:1; margin-bottom:.2rem; }
.subtitle { text-align:center; color:#8a8a96; font-size:.92rem; margin-bottom:1.6rem; letter-spacing:.04em; }
.section-header { font-family:'Barlow Condensed',sans-serif; font-size:1rem; font-weight:700; text-transform:uppercase;
                  letter-spacing:.12em; color:#e07a1e; border-bottom:2px solid #2e2e3a; padding-bottom:5px; margin:1rem 0 .7rem; }

.path-step   { display:inline-block; padding:3px 9px; border-radius:4px; font-size:.72rem; font-weight:700; margin:2px; }
.path-done   { background:#123b1f; color:#4ecb77; border:1px solid #2fa35c; }
.path-current{ background:#3d2607; color:#ffa53a; border:1px solid #e07a1e; }
.path-future { background:#1a1a20; color:#55555f; border:1px solid #2e2e3a; }

div.stButton > button { background:linear-gradient(140deg,#e07a1e,#b35a0d) !important; color:#fff !important;
    font-family:'Barlow Condensed',sans-serif !important; font-weight:700 !important; font-size:1rem !important;
    text-transform:uppercase !important; letter-spacing:.06em !important; border:none !important;
    border-radius:7px !important; padding:.55rem 1.2rem !important; width:100%; }
div.stButton > button:hover { filter:brightness(1.12) !important; }
hr { border-color:#2e2e3a !important; }

.event-positive{ background:linear-gradient(140deg,#04180c,#0a2a16); border-left:4px solid #2fa35c; padding:.9rem 1.1rem; border-radius:0 8px 8px 0; margin:.5rem 0; }
.event-negative{ background:linear-gradient(140deg,#1d0505,#2c0b0b); border-left:4px solid #e0492c; padding:.9rem 1.1rem; border-radius:0 8px 8px 0; margin:.5rem 0; }
.event-neutral { background:linear-gradient(140deg,#05101d,#0b1a2c); border-left:4px solid #3a7ae0; padding:.9rem 1.1rem; border-radius:0 8px 8px 0; margin:.5rem 0; }
.playoff-champ { background:linear-gradient(140deg,#1d1503,#3a2a05); border:2px solid #d08a1e; border-radius:12px; padding:1.2rem; margin:.5rem 0; text-align:center; }
.level-up { background:linear-gradient(140deg,#160020,#280038); border:2px solid #c040e0; border-radius:12px; padding:1rem; margin:.5rem 0; text-align:center; }
.badge-captain{ background:#c9a227; color:#1a1005; }
.badge-legend { background:linear-gradient(90deg,#ef4444,#f59e0b); color:#fff; }
.presser { background:linear-gradient(140deg,#0c0c14,#16161f); border:1px solid #2e2e3a; border-left:5px solid #b4b4c0;
           border-radius:10px; padding:1.1rem 1.3rem; margin:.6rem 0; }
.presser-q { font-family:'Barlow Condensed',sans-serif; font-size:1.45rem; font-weight:700; color:#fff; line-height:1.25; }
.mic { font-size:.7rem; color:#8a8a96; text-transform:uppercase; letter-spacing:.14em; margin-bottom:.35rem; }
.answer-card { background:#141418; border:1px solid #2e2e3a; border-radius:9px; padding:.85rem 1rem;
               margin-bottom:.5rem; min-height:118px; }
.reaction { border-radius:8px; padding:.75rem 1rem; margin:.4rem 0; font-size:.85rem; }
.reaction-positive{ background:#04180c; border-left:4px solid #2fa35c; }
.reaction-neutral { background:#15151c; border-left:4px solid #8a8a96; }
.reaction-negative{ background:#1d0505; border-left:4px solid #e0492c; }
.tactic-card { background:#141418; border:1px solid #2e2e3a; border-radius:9px; padding:.8rem .9rem;
               margin-bottom:.5rem; min-height:172px; }
.verdict { background:linear-gradient(140deg,#0d0d14,#17171f); border:1px solid #2e2e3a; border-left:5px solid #e07a1e;
           border-radius:10px; padding:1.1rem 1.3rem; margin:.6rem 0; font-size:.92rem; line-height:1.7; color:#c8c8d2; }

.boxscore { width:100%; border-collapse:collapse; font-size:.76rem; }
.boxscore th { background:#15151c; color:#e07a1e; padding:8px 9px; text-align:left; border-bottom:2px solid #2e2e3a;
               font-family:'Barlow Condensed',sans-serif; text-transform:uppercase; letter-spacing:.08em; font-size:.74rem; white-space:nowrap; }
.boxscore td { padding:7px 9px; border-bottom:1px solid #1e1e26; color:#dcdce4; white-space:nowrap; }
.boxscore td.num { font-family:'JetBrains Mono',monospace; }
.boxscore tr:nth-child(even) td { background:#111117; }
.boxscore tr:hover td { background:#1d1d26; }
</style>
""", unsafe_allow_html=True)


# ── State ──────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "home", "player": None,
        "team_offers": None, "offer_context": None,
        "sponsor_offers": None, "season_result": None,
        "training_choice": None, "tactic_choice": None,
        "draft_result": None, "interview": None, "interview_result": None,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


init_state()


def goto(screen):
    st.session_state.screen = screen
    st.rerun()


def rich(text):
    """Render the **bold** markers used in career prose as real HTML."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong style='color:#fff'>\1</strong>", text)


def money(v):
    if v >= 1_000_000:
        return f"{v/1_000_000:.1f}M€".replace(".0M", "M")
    if v >= 1_000:
        return f"{v/1_000:.0f}k€"
    return f"{v}€"


# ── UI helpers ─────────────────────────────────────────────────────────────────
def attr_bar(label, value, color="#e07a1e"):
    st.markdown(f'<div class="attr-row"><div class="attr-label"><span>{label}</span><span>{value}</span></div>'
                f'<div class="bar-bg"><div class="bar-fill" style="width:{min(100,max(0,value))}%;background:{color}"></div></div></div>',
                unsafe_allow_html=True)


def scoreboard(stats):
    cells = "".join(f'<div class="sb-cell"><div class="sb-value">{v}</div><div class="sb-label">{k}</div></div>'
                    for k, v in stats.items())
    st.markdown(f'<div class="scoreboard">{cells}</div>', unsafe_allow_html=True)


def league_path(player):
    steps = []
    done = {r.league for r in player.career_history}
    for lg in COUNTRIES[player.country]["path"]:
        if lg == player.current_league:
            cls, icon = "path-current", "▶"
        elif lg in done:
            cls, icon = "path-done", "✓"
        else:
            cls, icon = "path-future", "○"
        steps.append(f'<span class="path-step {cls}">{icon} {LEAGUES.get(lg,{}).get("name",lg)}</span>')
    st.markdown(" ".join(steps), unsafe_allow_html=True)


def player_header(p):
    flag = COUNTRIES[p.country]["flag"]
    champs = p.total_championships()
    role = ROLES.get(p.current_role, ROLES["Titulaire"])
    champ_str = " " + "🏆" * min(champs, 5) if champs else ""
    status = p.club_status()
    badge_cls = {"Légende du club": "badge-legend", "Capitaine": "badge-captain"}.get(status, "badge-gray")
    status_badge = (f'<span class="badge {badge_cls}">{status} · {p.seasons_with_team} sais.</span>'
                    if status else "")

    def stat_block(value, label):
        return (f'<div style="text-align:center;min-width:76px">'
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:2.3rem;'
                f'font-weight:700;color:#fff;line-height:1">{value}</div>'
                f'<div style="font-size:.6rem;color:#2a1806;font-weight:800;'
                f'letter-spacing:.1em">{label}</div></div>')

    # Emitted as one unindented line: an empty interpolation followed by an indented
    # line would be read as a markdown code block and printed as raw HTML.
    st.markdown(
        f'<div class="court"><div class="court-inner">'
        f'<div style="display:flex;align-items:center;gap:1.1rem;flex-wrap:wrap">'
        f'<div class="jersey"><div class="jersey-num">{p.jersey}</div>'
        f'<div class="jersey-pos">{p.position}</div></div>'
        f'<div style="flex:1;min-width:230px">'
        f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:2.1rem;'
        f'font-weight:800;color:#fff;line-height:1.05">{flag} {p.name}{champ_str}</div>'
        f'<div style="margin-top:.3rem">'
        f'<span class="badge badge-orange">{role["icon"]} {p.current_role}</span>'
        f'<span class="badge badge-gray">{p.current_team}</span>'
        f'<span class="badge badge-gray">'
        f'{LEAGUES.get(p.current_league, {}).get("name", p.current_league)}</span>'
        f'<span class="badge badge-purple">Niv.{p.level}</span>{status_badge}</div></div>'
        + stat_block(p.overall_rating(), "OVERALL")
        + stat_block(p.age, "ANS")
        + stat_block(f"S{p.season_number}", "SAISON")
        + '</div></div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        rep_color = "#2fa35c" if p.reputation >= 60 else "#e07a1e" if p.reputation >= 30 else "#e0492c"
        st.markdown(f'<div class="attr-label"><span>📡 Réputation NBA</span><span>{p.reputation}/100</span></div>'
                    f'<div class="bar-bg" style="height:11px"><div class="bar-fill" style="width:{p.reputation}%;background:{rep_color}"></div></div>',
                    unsafe_allow_html=True)
    with c2:
        needed = xp_for_level(p.level + 1)
        st.markdown(f'<div class="attr-label"><span>⚡ Niveau {p.level}</span><span>{p.xp} / {needed} XP</span></div>'
                    f'<div class="bar-bg" style="height:11px"><div class="bar-fill xp-fill" style="width:{p.xp_progress_pct()}%"></div></div>',
                    unsafe_allow_html=True)
    league_path(p)
    st.markdown("---")


def offer_card(o):
    """Rendered as a single unindented HTML block — indented lines would be read as code."""
    r = ROLES[o["role"]]
    st.markdown(
        f'<div class="offer-card">'
        f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.35rem;font-weight:800;color:#fff">{o["team"]}</div>'
        f'<div style="margin:.35rem 0"><span class="badge badge-orange">{r["icon"]} {o["role"]}</span></div>'
        f'<div style="color:#9a9aa6;font-size:.78rem;line-height:1.45;min-height:52px">{r["desc"]}</div>'
        f'<div style="margin-top:.6rem;font-size:.78rem;color:#c8c8d2">'
        f'<div>⏱️ <strong>{o["minutes"]} min</strong> / match visées</div>'
        f'<div>💰 <strong style="color:#ffa53a">{money(o["salary"])}</strong> / saison — {o["years"]} an(s)</div>'
        f'<div>🏟️ Effectif : <strong>{strength_label(o["strength"])}</strong></div></div>'
        f'<div class="bar-bg" style="margin-top:.45rem"><div class="bar-fill" '
        f'style="width:{int(o["strength"]*100)}%;background:#3a7ae0"></div></div>'
        f'<div style="font-size:.68rem;color:#8a8a96;margin-top:.25rem">'
        f'XP ×{r["xp_mult"]:.2f} · Visibilité ×{r["rep_mult"]:.2f}</div></div>',
        unsafe_allow_html=True)


# ── Screens ────────────────────────────────────────────────────────────────────
def screen_home():
    st.markdown('<div class="title-nba">🏀 NBA DREAM</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Career Simulator — du lycée au parquet NBA</div>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("""<div class="card">
        <div class="section-header">Le principe</div>
        <p style="color:#b4b4c0;font-size:.89rem;line-height:1.65">
        Chaque saison tu <strong style="color:#ffa53a">choisis un club</strong> parmi plusieurs offres.
        Star d'une équipe en reconstruction, ou 6ème homme d'un contender&nbsp;?<br>
        Le rôle décide de tes <strong style="color:#ffa53a">minutes</strong>, donc de tes stats, de ton
        <strong style="color:#ffa53a">salaire</strong> et de ton <strong style="color:#c040e0">XP</strong>.<br><br>
        Moins de minutes chez un gros&nbsp;= moins de stats, mais plus d'apprentissage et un vrai
        <strong style="color:#ffa53a">titre</strong> à aller chercher.<br>
        Une saison = un an. Pas de raccourci.
        </p></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="card"><div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem">
        <div><span class="badge badge-blue">🇫🇷 France</span><br><small style="color:#8a8a96">Pro B → Elite → EuroLeague → Draft</small></div>
        <div><span class="badge badge-red">🇨🇭 Suisse</span><br><small style="color:#8a8a96">SBL → Pro B → Elite → Draft</small></div>
        <div><span class="badge badge-orange">🇪🇸 Espagne</span><br><small style="color:#8a8a96">LEB Gold → ACB → EuroLeague → Draft</small></div>
        <div><span class="badge badge-green">🇺🇸 USA</span><br><small style="color:#8a8a96">High School → NCAA → Draft</small></div>
        </div></div>""", unsafe_allow_html=True)
        if st.button("🏀 Démarrer une carrière", key="start"):
            goto("create")


def screen_create():
    st.markdown('<div class="title-nba">Créer ton joueur</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Ton âge de départ change tout : tôt = plus de marge de progression</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-header">Identité</div>', unsafe_allow_html=True)
        name = st.text_input("Nom du joueur", placeholder="ex: Théo Martin")
        jersey = st.number_input("Numéro de maillot", 0, 99, 23)
        country = st.selectbox("Pays d'origine", list(COUNTRIES.keys()),
                               format_func=lambda c: f"{COUNTRIES[c]['flag']} {c}")
        position = st.selectbox("Poste", POSITIONS, format_func=lambda p: {
            "PG": "PG — Meneur", "SG": "SG — Arrière", "SF": "SF — Ailier",
            "PF": "PF — Ailier Fort", "C": "C — Pivot"}[p])
        age = st.slider("Âge de départ", 15, 19, 17)
        cap = 170 + (age - 15) * 12
        st.caption(f"À {age} ans tu démarres avec **{cap} points** à répartir. "
                   f"Draft NBA accessible à partir de {draft_eligibility_age(country)} ans.")
    with c2:
        st.markdown('<div class="section-header">Attributs de départ</div>', unsafe_allow_html=True)
        athl = st.slider("🏃 Athlétisme", 25, 75, 34)
        shot = st.slider("🎯 Tir", 25, 75, 34)
        biq = st.slider("🧠 QI Basketball", 25, 75, 34)
        ment = st.slider("💪 Mental", 25, 75, 34)
        lead = st.slider("📣 Leadership", 25, 75, 34)
        total = athl + shot + biq + ment + lead
        left = cap - total
        color = "#2fa35c" if left >= 0 else "#e0492c"
        st.markdown(f"<div style='text-align:right;color:{color};font-weight:700;font-size:1.05rem'>"
                    f"{total} / {cap} points · <span style='font-size:.85rem'>"
                    f"{'reste ' + str(left) if left >= 0 else 'dépassé de ' + str(-left)}</span></div>",
                    unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Retour", key="back_home"):
            goto("home")
    with c2:
        if not name:
            st.caption("Renseigne un nom pour continuer.")
        elif total > cap:
            st.caption(f"Trop de points — réduis de {total - cap}.")
        if st.button("✅ Créer et signer", key="create", disabled=not name or total > cap):
            start = COUNTRIES[country]["start_league"]
            p = Player(name=name, country=country, position=position, age=age, jersey=int(jersey),
                       athleticism=athl, shooting=shot, basketball_iq=biq, mental=ment,
                       leadership=lead, current_league=start)
            st.session_state.player = p
            st.session_state.team_offers = generate_team_offers(p, start)
            st.session_state.offer_context = {"kind": "start", "league": start}
            goto("offers")


def screen_offers():
    p = st.session_state.player
    ctx = st.session_state.offer_context or {}
    offers = st.session_state.team_offers or []
    league_name = LEAGUES.get(ctx.get("league", p.current_league), {}).get("name", "")

    titles = {"start": "Tes premières offres", "expiry": "Fin de contrat — le marché s'ouvre",
              "promotion": "Tu montes d'un cran", "draft": "Offres post-draft",
              "nba_contract": "Des franchises NBA t'appellent"}
    st.markdown(f'<div class="title-nba">{titles.get(ctx.get("kind"), "Offres de clubs")}</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{league_name} — le rôle que tu acceptes décide de ta saison</div>',
                unsafe_allow_html=True)

    if p.season_number:
        st.markdown(f'<div class="card"><span class="badge badge-gray">Overall {p.overall_rating()}</span>'
                    f'<span class="badge badge-gray">Réputation {p.reputation}</span>'
                    f'<span class="badge badge-purple">Niveau {p.level}</span>'
                    f'<span class="badge badge-gray">Valeur marché ≈ {money(market_value(p, ctx.get("league", p.current_league)))}</span>'
                    f'</div>', unsafe_allow_html=True)

    cols = st.columns(len(offers))
    for i, (col, o) in enumerate(zip(cols, offers)):
        with col:
            offer_card(o)
            if st.button(f"Signer — {o['team']}", key=f"sign_{i}"):
                p.sign_contract(o)
                st.session_state.team_offers = None
                st.session_state.offer_context = None
                goto("dashboard")


def screen_dashboard():
    p = st.session_state.player
    player_header(p)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="section-header">Attributs</div>', unsafe_allow_html=True)
        attr_bar("🏃 Athlétisme", p.athleticism)
        attr_bar("🎯 Tir", p.shooting, "#3a9ae0")
        attr_bar("🧠 QI Basketball", p.basketball_iq, "#9a3ae0")
        attr_bar("💪 Mental", p.mental, "#e0663a")
        attr_bar("📣 Leadership", p.leadership, "#3ae09a")

        st.markdown('<div class="section-header">Forme & moral</div>', unsafe_allow_html=True)
        cm, cf = st.columns(2)
        with cm:
            c = "#2fa35c" if p.morale >= 60 else "#e07a1e" if p.morale >= 40 else "#e0492c"
            st.markdown(f"<div style='color:{c};font-weight:700'>😤 Moral {p.morale}/100</div>", unsafe_allow_html=True)
        with cf:
            c = "#2fa35c" if p.fitness >= 70 else "#e07a1e" if p.fitness >= 50 else "#e0492c"
            st.markdown(f"<div style='color:{c};font-weight:700'>🏋️ Forme {p.fitness}/100</div>", unsafe_allow_html=True)

        if p.career_history:
            st.markdown('<div class="section-header">Moyennes carrière</div>', unsafe_allow_html=True)
            scoreboard({"MPG": p.career_mpg(), "PPG": p.career_ppg(), "RPG": p.career_rpg(),
                        "APG": p.career_apg(), "TITRES": p.total_championships()})

    with c2:
        ld = LEAGUES.get(p.current_league, {})
        role = ROLES.get(p.current_role, ROLES["Titulaire"])
        st.markdown('<div class="section-header">Contrat</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="card-gold">
        <div style="font-size:1.15rem;font-weight:700;color:#fff">{p.current_team}</div>
        <div style="color:#c8a86a;font-size:.8rem">{ld.get('name', p.current_league)}</div>
        <div style="margin-top:.6rem;font-size:.84rem;color:#e8d8b8">
          {role['icon']} <strong>{p.current_role}</strong> · ~{role['minutes']} min<br>
          💰 {money(p.contract_salary)} / saison<br>
          📄 {p.contract_years_left} an(s) restant(s)<br>
          🏟️ {strength_label(p.team_strength)}
        </div></div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">Sponsors</div>', unsafe_allow_html=True)
        if p.sponsors:
            for s in p.sponsors:
                col = TIER_COLORS.get(s["tier"], "#888")
                st.markdown(f"<div style='font-size:.8rem;color:#c8c8d2;margin-bottom:3px'>{s['icon']} "
                            f"<strong>{s['name']}</strong> <span style='color:{col}'>({s['tier']})</span><br>"
                            f"<span style='color:#8a8a96'>{money(s['annual_value'])}/an · {s['years']} an(s)</span></div>",
                            unsafe_allow_html=True)
            st.markdown(f"<div style='color:#2fa35c;font-weight:700;font-size:.85rem;margin-top:.4rem'>"
                        f"+{money(sponsor_income(p))}/an</div>", unsafe_allow_html=True)
        else:
            st.caption("Aucun sponsor. Ta réputation en attirera.")

        st.markdown(f"<div style='color:#ffa53a;font-weight:700;margin-top:.6rem'>💼 Total gagné : "
                    f"{money(p.total_earnings)}</div>", unsafe_allow_html=True)

    st.markdown("---")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🏋️ Préparer la saison", key="prep"):
            goto("prepare")
    with b2:
        if st.button("🤝 Sponsoring", key="spons"):
            st.session_state.sponsor_offers = generate_sponsor_offers(p, 2)
            goto("sponsors")
    with b3:
        if p.career_history and st.button("📊 Historique", key="hist"):
            goto("history")

    if p.should_consider_retirement():
        st.markdown("---")
        st.caption(f"Tu as {p.age} ans. Retraite obligatoire à {RETIREMENT_AGE} ans.")
        if st.button("🎬 Prendre sa retraite", key="retire"):
            p.retired = True
            goto("retired")


def screen_sponsors():
    p = st.session_state.player
    player_header(p)
    st.markdown("## 🤝 Sponsoring")
    offers = st.session_state.sponsor_offers or []

    st.markdown(f'<div class="card"><span class="badge badge-gray">Réputation {p.reputation}/100</span>'
                f'<span class="badge badge-gray">{len(p.sponsors)}/{MAX_ACTIVE_SPONSORS} contrats actifs</span>'
                f'<div style="color:#9a9aa6;font-size:.82rem;margin-top:.5rem">Les sponsors paient chaque saison, '
                f'remontent ton moral et ajoutent un peu d\'XP grâce à la visibilité.</div></div>',
                unsafe_allow_html=True)

    if not offers:
        st.info("Aucune offre pour l'instant — fais monter ta réputation.")
    elif len(p.sponsors) >= MAX_ACTIVE_SPONSORS:
        st.warning(f"Tu as déjà {MAX_ACTIVE_SPONSORS} contrats actifs. Attends qu'un expire.")
    else:
        cols = st.columns(len(offers))
        for i, (col, s) in enumerate(zip(cols, offers)):
            with col:
                color = TIER_COLORS.get(s["tier"], "#888")
                st.markdown(f"""<div class="offer-card" style="border-left-color:{color};min-height:190px">
                  <div style="font-size:2rem">{s['icon']}</div>
                  <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.3rem;font-weight:800;color:#fff">{s['name']}</div>
                  <div><span class="badge" style="background:{color};color:#fff">{s['tier']}</span></div>
                  <div style="margin-top:.5rem;font-size:.82rem;color:#c8c8d2">
                    💰 <strong style="color:#ffa53a">{money(s['annual_value'])}</strong> / an<br>
                    📄 {s['years']} an(s)<br>
                    😊 Moral +{s['morale_bonus']} · ⚡ +{s['xp_bonus']} XP/saison</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Signer {s['name']}", key=f"sp_{i}"):
                    p.sponsors.append(dict(s))
                    st.session_state.sponsor_offers = [o for o in offers if o["name"] != s["name"]]
                    st.rerun()

    st.markdown("---")
    if st.button("← Retour au vestiaire", key="back_sp"):
        goto("dashboard")


TRAINING = {
    "Tir":              {"icon": "🎯", "desc": "Shooting, mécanique, tir en sortie d'écran", "boosts": "+Tir, +Mental"},
    "Athletisme":       {"icon": "⚡", "desc": "Détente, vitesse, explosivité", "boosts": "+Athlétisme"},
    "QI Basketball":    {"icon": "🧠", "desc": "Vidéo, lecture de jeu, spacing", "boosts": "+QI, +Leadership"},
    "Mental":           {"icon": "🧘", "desc": "Gestion de la pression, clutch", "boosts": "+Mental, +Leadership"},
    "Physique Complet": {"icon": "💪", "desc": "Préparation équilibrée", "boosts": "+Tout (modéré)"},
}


def screen_prepare():
    p = st.session_state.player
    player_header(p)
    st.markdown("## 🏋️ Intersaison")

    # ─ Tactical system
    st.markdown('<div class="section-header">Système de jeu de l\'équipe</div>', unsafe_allow_html=True)
    st.caption("Le système décide de ce qu'on attend de toi. Le « fit » compare ses exigences "
               "à **tes points forts** : bien choisi il gonfle tes stats, tes XP et les chances "
               "de l'équipe ; à contre-emploi, il te bride toute la saison.")

    tactic = st.session_state.tactic_choice or p.current_tactic
    cols = st.columns(len(TACTICS))
    for col, (name, t) in zip(cols, TACTICS.items()):
        with col:
            fit = fit_score(p, name)
            label, color = fit_label(fit)
            border = "#e07a1e" if tactic == name else "#2e2e3a"
            st.markdown(f'<div class="tactic-card" style="border-color:{border}">'
                        f'<div style="font-size:1.6rem">{t["icon"]}</div>'
                        f'<div style="font-weight:700;color:#fff;font-size:.92rem">{name}</div>'
                        f'<div style="color:#8a8a96;font-size:.72rem;line-height:1.4;min-height:48px">{t["desc"]}</div>'
                        f'<div style="margin-top:.4rem;font-size:.75rem;color:{color};font-weight:700">'
                        f'Fit {fit:.0f} — {label}</div>'
                        f'<div class="bar-bg" style="margin-top:3px"><div class="bar-fill" '
                        f'style="width:{fit}%;background:{color}"></div></div></div>',
                        unsafe_allow_html=True)
            if st.button("Adopter", key=f"tac_{name}"):
                st.session_state.tactic_choice = name
                st.rerun()

    # ─ Training
    st.markdown('<div class="section-header">Axe de travail</div>', unsafe_allow_html=True)
    st.caption("Détermine les gains d'attributs et une partie de l'XP. "
               "Après 27 ans, les gains physiques ralentissent nettement.")

    selected = st.session_state.training_choice
    cols = st.columns(len(TRAINING))
    for col, (key, d) in zip(cols, TRAINING.items()):
        with col:
            border = "#e07a1e" if selected == key else "#2e2e3a"
            st.markdown(f'<div class="card" style="text-align:center;border-color:{border};min-height:158px">'
                        f'<div style="font-size:2rem">{d["icon"]}</div>'
                        f'<div style="font-weight:700;margin:4px 0;color:#fff">{key}</div>'
                        f'<div style="color:#8a8a96;font-size:.74rem">{d["desc"]}</div>'
                        f'<div style="color:#ffa53a;font-size:.7rem;margin-top:5px">{d["boosts"]}</div></div>',
                        unsafe_allow_html=True)
            if st.button("Choisir", key=f"tr_{key}"):
                st.session_state.training_choice = key
                st.rerun()

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Retour", key="back_prep"):
            goto("dashboard")
    with c2:
        if not selected:
            st.warning("Sélectionne un axe d'entraînement.")
        elif st.button(f"🏀 Jouer la saison — {TACTICS[tactic]['icon']} {tactic} / {selected}", key="play"):
            st.session_state.season_result = run_season(p, selected, tactic=tactic)
            st.session_state.training_choice = None
            st.session_state.tactic_choice = None
            st.session_state.interview = None
            st.session_state.interview_result = None
            goto("season_result")


def screen_season_result():
    """Render only — the season was already committed in screen_prepare."""
    p = st.session_state.player
    res = st.session_state.season_result
    if not res:
        goto("dashboard")

    rec, event, playoff = res["record"], res["event"], res["playoff"]
    player_header(p)
    st.markdown(f"## 📅 Bilan saison {rec.season} — {rec.age} ans")

    st.markdown(f'<div class="section-header">Box score — {rec.team} · {rec.role}</div>', unsafe_allow_html=True)
    scoreboard({"G": rec.games, "MPG": rec.mpg, "PPG": rec.ppg, "RPG": rec.rpg,
                "APG": rec.apg, "SPG": rec.spg, "BPG": rec.bpg, "FG%": f"{int(rec.fg_pct*100)}"})

    if rec.award:
        st.markdown(f'<div class="card-gold"><div style="font-size:1.1rem;color:#ffd98a">🏆 {rec.award}</div></div>',
                    unsafe_allow_html=True)

    st.markdown('<div class="section-header">Playoffs</div>', unsafe_allow_html=True)
    if playoff is None:
        st.markdown('<div class="card"><div style="color:#8a8a96">❌ Pas de playoffs cette saison.</div></div>',
                    unsafe_allow_html=True)
    elif playoff.champion:
        st.balloons()
        st.markdown(f'<div class="playoff-champ"><div style="font-size:2.6rem">🏆</div>'
                    f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.7rem;font-weight:800;color:#ffd98a">'
                    f'{playoff.title}</div><div style="color:#fff">3 tours remportés</div></div>',
                    unsafe_allow_html=True)
    elif playoff.reached_final:
        st.markdown(f'<div class="card"><div style="font-size:1.05rem;font-weight:700">🥈 Finaliste</div>'
                    f'<div style="color:#9a9aa6;font-size:.85rem">Défaite en finale contre {playoff.opponent}.</div></div>',
                    unsafe_allow_html=True)
    elif playoff.rounds_won:
        st.markdown(f'<div class="card"><div style="font-size:1.05rem;font-weight:700">🎯 Demi-finale</div>'
                    f'<div style="color:#9a9aa6;font-size:.85rem">Éliminé par {playoff.opponent}.</div></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="card"><div style="font-size:1.05rem;font-weight:700">📉 Sorti en quarts</div>'
                    f'<div style="color:#9a9aa6;font-size:.85rem">Défaite contre {playoff.opponent}.</div></div>',
                    unsafe_allow_html=True)

    cls = {"positive": "event-positive", "negative": "event-negative",
           "neutral": "event-neutral"}[event.get("type", "neutral")]
    rb, mb = event.get("reputation_bonus", 0), event.get("morale_bonus", 0)
    st.markdown(f'<div class="{cls}"><div style="font-size:1.02rem;font-weight:700">{event.get("title","")}</div>'
                f'<div style="color:#b4b4c0;font-size:.86rem;margin-top:4px">{event.get("description","")}</div>'
                f'<div style="margin-top:8px;font-size:.78rem">Réputation {rb:+d} · Moral {mb:+d}</div></div>',
                unsafe_allow_html=True)

    st.markdown('<div class="section-header">Système & statut</div>', unsafe_allow_html=True)
    label, color = fit_label(rec.tactic_fit)
    st.markdown(f'<div class="card"><span class="badge badge-gray">'
                f'{TACTICS[rec.tactic]["icon"]} {rec.tactic}</span>'
                f'<span class="badge" style="background:{color};color:#fff">Fit {rec.tactic_fit:.0f} — {label}</span>'
                f'</div>', unsafe_allow_html=True)
    loyalty = res.get("loyalty") or {}
    if loyalty:
        st.markdown(f'<div class="card-green"><strong>🎖️ {loyalty["status"]} — {p.current_team}</strong>'
                    f'<div style="color:#9fdfba;font-size:.85rem;margin-top:3px">'
                    f'{p.seasons_with_team} saisons au club : Mental +{loyalty["mental"]}, '
                    f'Leadership +{loyalty["leadership"]}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Finances</div>', unsafe_allow_html=True)
    scoreboard({"SALAIRE": money(rec.salary_earned), "SPONSORS": money(rec.sponsor_earned),
                "TOTAL SAISON": money(rec.salary_earned + rec.sponsor_earned),
                "CARRIÈRE": money(p.total_earnings)})
    for s in res["expired_sponsors"]:
        st.caption(f"📄 Contrat {s['name']} arrivé à expiration.")

    st.markdown('<div class="section-header">Progression</div>', unsafe_allow_html=True)
    if res["levels_gained"]:
        st.markdown(f'<div class="level-up"><div style="font-size:1.7rem">⚡</div>'
                    f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.5rem;font-weight:800;color:#d054ff">'
                    f'NIVEAU {p.level} ATTEINT</div>'
                    f'<div style="color:#9a9aa6;font-size:.84rem">+{rec.xp_gained} XP · '
                    f'{res["levels_gained"]} niveau(x) — tes attributs progressent</div></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="card"><div style="color:#d054ff;font-weight:700">+{rec.xp_gained} XP</div>'
                    f'<div style="color:#8a8a96;font-size:.8rem">{p.xp}/{xp_for_level(p.level+1)} '
                    f'pour le niveau {p.level+1}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🎙️ Conférence de presse de fin de saison", key="to_presser"):
        goto("interview")


# ── End-of-season press conference ─────────────────────────────────────────────
def screen_interview():
    p = st.session_state.player
    res = st.session_state.season_result
    if not res:
        goto("dashboard")

    if not st.session_state.interview:
        key, data = pick_interview(res["record"], p)
        st.session_state.interview = {"key": key, **data}
    itw = st.session_state.interview
    result = st.session_state.interview_result

    player_header(p)
    st.markdown("## 🎙️ Conférence de presse")
    st.markdown(f'<div class="presser"><div class="mic">Salle de presse · fin de saison {res["record"].season}</div>'
                f'<div class="presser-q">« {itw["question"]} »</div></div>', unsafe_allow_html=True)

    if result is None:
        st.caption("Ce que tu réponds change durablement ton **mental** et ton **leadership**, "
                   "et fixe la réaction des supporters et de la direction. Une sortie agressive "
                   "fait grimper ta notoriété, mais coûte cher dans le vestiaire.")
        cols = st.columns(len(itw["answers"]))
        for i, (col, a) in enumerate(zip(cols, itw["answers"])):
            with col:
                def sign(v):
                    return f"<span style='color:{'#2fa35c' if v > 0 else '#e0492c'}'>{v:+d}</span>" if v else "—"
                st.markdown(f'<div class="answer-card">'
                            f'<div style="color:#fff;font-size:.88rem;line-height:1.5;min-height:66px">'
                            f'« {a["text"]} »</div>'
                            f'<div style="font-size:.72rem;color:#8a8a96;margin-top:.5rem">'
                            f'Mental {sign(a["mental"])} · Leadership {sign(a["leadership"])}</div></div>',
                            unsafe_allow_html=True)
                if st.button("Répondre", key=f"ans_{i}"):
                    st.session_state.interview_result = apply_answer(p, a)
                    st.rerun()
        return

    st.markdown('<div class="section-header">Réactions</div>', unsafe_allow_html=True)
    for who, icon, key in [("Supporters", "🧣", "fans"), ("Direction & vestiaire", "🏢", "staff")]:
        sentiment, text = result[key]
        st.markdown(f'<div class="reaction reaction-{sentiment}">'
                    f'<strong>{icon} {who}</strong> {SENTIMENT_ICON[sentiment]}<br>'
                    f'<span style="color:#b4b4c0">{text}</span></div>', unsafe_allow_html=True)

    def delta(label, v):
        color = "#2fa35c" if v > 0 else "#e0492c" if v < 0 else "#8a8a96"
        return f"<span style='color:{color};font-weight:700'>{label} {v:+d}</span>"

    st.markdown(f'<div class="card">{delta("Mental", result["mental_delta"])} · '
                f'{delta("Leadership", result["leadership_delta"])} · '
                f'{delta("Moral", result["morale"])} · '
                f'{delta("Réputation", result["reputation"])}</div>', unsafe_allow_html=True)

    career_next_actions(p, res)


# ── What comes next, once the press conference is done ─────────────────────────
def career_next_actions(p, res):
    st.markdown("---\n### Suite de la carrière")

    if p.must_retire():
        st.warning(f"Tu as {p.age} ans. L'heure de la retraite a sonné.")
        if st.button("🎬 Raccrocher", key="force_retire"):
            p.retired = True
            goto("retired")
        return

    nxt = get_next_league(p.current_league, p.country)
    expired = res["contract_expired"]

    def clear_season():
        st.session_state.season_result = None
        st.session_state.interview = None
        st.session_state.interview_result = None

    c1, c2, c3 = st.columns(3)
    with c1:
        if expired:
            st.caption("📄 Ton contrat est arrivé à son terme.")
            if st.button("📝 Voir les offres", key="renew"):
                st.session_state.team_offers = generate_team_offers(
                    p, p.current_league, include_current=True)
                st.session_state.offer_context = {"kind": "expiry", "league": p.current_league}
                clear_season()
                goto("offers")
        else:
            if st.button(f"🔄 Saison suivante ({p.contract_years_left} an(s) restants)", key="next"):
                clear_season()
                goto("prepare")
    with c2:
        if nxt and nxt != "NBA":
            if check_promotion_eligibility(p):
                if st.button(f"⬆️ Monter en {LEAGUES[nxt]['name']}", key="promote"):
                    st.session_state.team_offers = generate_team_offers(p, nxt)
                    st.session_state.offer_context = {"kind": "promotion", "league": nxt}
                    clear_season()
                    goto("offers")
            else:
                st.caption(f"⬆️ {LEAGUES[nxt]['name']} : pas encore le niveau.")
        elif not p.in_nba:
            st.caption("Tu es au sommet de ta filière nationale.")
    with c3:
        # The NBA is reachable from any league — prospects declare from Pro B or the
        # NCAA, not only after climbing every rung at home.
        if p.in_nba:
            st.caption("🏀 Tu es en NBA.")
        elif can_enter_draft(p):
            if st.button("🏀 Se présenter à la Draft NBA", key="draft"):
                st.session_state.draft_result = run_draft(p)
                clear_season()
                goto("draft_night")
            st.caption(f"Draft ouverte jusqu'à {DRAFT_MAX_AGE} ans — tu en as {p.age}.")
        elif can_sign_nba_contract(p):
            if st.button("🏀 Signer un contrat NBA", key="nba_contract"):
                st.session_state.team_offers = generate_team_offers(p, "NBA")
                st.session_state.offer_context = {"kind": "nba_contract", "league": "NBA"}
                clear_season()
                goto("offers")
            st.caption(f"Trop âgé pour la draft ({DRAFT_MAX_AGE} ans max) : "
                       "les franchises te signent sur ton bilan.")
        elif p.age > DRAFT_MAX_AGE:
            need = []
            if p.overall_rating() < 70:
                need.append(f"overall 70 (actuel {p.overall_rating()})")
            if p.reputation < 55:
                need.append(f"réputation 55 (actuel {p.reputation})")
            st.caption(f"🏀 Draft fermée (>{DRAFT_MAX_AGE} ans). Contrat NBA — il manque : "
                       + ", ".join(need))
        else:
            need = []
            if p.age < draft_eligibility_age(p.country):
                need.append(f"{draft_eligibility_age(p.country)} ans")
            if p.nba_prospect_score() < 52:
                need.append(f"prospect 52 (actuel {p.nba_prospect_score()})")
            if p.reputation < 32:
                need.append(f"réputation 32 (actuel {p.reputation})")
            st.caption("🏀 Draft NBA — il te manque : " + ", ".join(need))

    st.markdown("")
    if st.button("🏠 Vestiaire", key="to_dash"):
        clear_season()
        goto("dashboard")


def screen_draft_night():
    p = st.session_state.player
    d = st.session_state.draft_result
    st.markdown('<div class="title-nba">🎉 Draft Night</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Score prospect {d["score"]} · {p.season_number} saisons · {p.age} ans</div>',
                unsafe_allow_html=True)

    if d["round"] == 1 and d["pick"] <= 5:
        st.balloons()
        cls, head, sub = "card-gold", f"🔥 TOP {d['pick']} PICK", "Une franchise mise tout sur toi."
    elif d["round"] == 1:
        st.balloons()
        cls, head, sub = "card-gold", f"⭐ 1ER TOUR — PICK #{d['pick']}", "Contrat garanti, place assurée."
    elif d["round"] == 2:
        cls, head, sub = "card-green", f"🎯 2ÈME TOUR — PICK #{d['pick']}", "Rien n'est garanti. À toi de t'imposer."
    else:
        cls, head, sub = "card", "✍️ NON DRAFTÉ", "Aucun nom appelé. Des clubs te proposent quand même un essai."

    st.markdown(f'<div class="{cls}" style="text-align:center;padding:2rem">'
                f'<div style="font-size:3rem">🏀</div>'
                f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:2rem;font-weight:800;color:#fff">{head}</div>'
                f'<div style="color:#b4b4c0">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Offres des franchises</div>', unsafe_allow_html=True)
    st.caption("Ton rang de draft détermine le type d'offres : les premiers choix atterrissent sur des "
               "équipes en reconstruction avec un rôle majeur, les derniers sur des contenders avec peu de minutes.")

    if not st.session_state.team_offers:
        st.session_state.team_offers = generate_draft_offers(p, d["round"], d["pick"])

    offers = st.session_state.team_offers
    cols = st.columns(len(offers))
    for i, (col, o) in enumerate(zip(cols, offers)):
        with col:
            offer_card(o)
            if st.button(f"Signer — {o['team']}", key=f"draft_sign_{i}"):
                p.draft_team = o["team"]
                p.sign_contract(o)
                st.session_state.team_offers = None
                st.session_state.draft_result = None
                goto("dashboard")


def screen_history():
    p = st.session_state.player
    player_header(p)
    st.markdown("## 📊 Historique de carrière")
    if not p.career_history:
        st.info("Aucune saison jouée.")
        return

    rows = ""
    for r in p.career_history:
        if r.playoff:
            po = ("🏆 Champion" if r.playoff.champion else "🥈 Finaliste"
                  if r.playoff.reached_final else "🎯 Demi" if r.playoff.rounds_won else "❌ Quarts")
        else:
            po = "—"
        lv = f"{r.level_before}"
        if r.level_after > r.level_before:
            lv = f"{r.level_before} → <span style='color:#d054ff;font-weight:700'>{r.level_after} ⬆</span>"
        rows += (
            f"<tr><td>S{r.season}</td><td class='num'>{r.age}</td>"
            f"<td>{LEAGUES.get(r.league,{}).get('name',r.league)}</td>"
            f"<td style='color:#a8a8b4'>{r.team}</td>"
            f"<td style='font-size:.72rem'>{ROLES.get(r.role,{}).get('icon','')} {r.role}</td>"
            f"<td class='num'>{r.games}</td><td class='num'>{r.mpg}</td>"
            f"<td class='num' style='color:#ffa53a;font-weight:700'>{r.ppg}</td>"
            f"<td class='num'>{r.rpg}</td><td class='num'>{r.apg}</td>"
            f"<td class='num'>{int(r.fg_pct*100)}%</td>"
            f"<td style='font-size:.72rem'>{r.award or ''}</td>"
            f"<td style='font-size:.72rem'>{po}</td>"
            f"<td class='num' style='color:#2fa35c'>{money(r.salary_earned + r.sponsor_earned)}</td>"
            f"<td class='num' style='color:#d054ff'>+{r.xp_gained}</td>"
            f"<td style='font-size:.72rem'>{lv}</td>"
            f"<td style='color:#8a8a96;font-size:.7rem'>{r.training_focus or ''}</td>"
            f"<td style='font-size:.7rem'>{TACTICS.get(r.tactic,{}).get('icon','')} {r.tactic or ''}"
            f"<span style='color:{fit_label(r.tactic_fit)[1]}'> ({r.tactic_fit:.0f})</span></td>"
            f"<td style='font-size:.7rem;color:#c9a227'>{r.club_status or ''}</td></tr>")

    st.markdown(
        '<div style="overflow-x:auto"><table class="boxscore"><thead><tr>'
        '<th>Sais.</th><th>Âge</th><th>Ligue</th><th>Équipe</th><th>Rôle</th>'
        '<th>G</th><th>MPG</th><th>PPG</th><th>RPG</th><th>APG</th><th>FG%</th>'
        '<th>Award</th><th>Playoffs</th><th>Revenus</th><th>XP</th><th>Niv.</th><th>Training</th>'
        '<th>Système</th><th>Statut club</th>'
        f'</tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Où en est cette carrière ?</div>', unsafe_allow_html=True)
    tier, icon, color = p.career_tier()
    st.markdown(f'<div class="verdict">'
                f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.5rem;font-weight:800;'
                f'color:{color};margin-bottom:.5rem">{icon} {tier}</div>'
                f'{rich(p.career_verdict())}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Résumé</div>', unsafe_allow_html=True)
    scoreboard({"SAISONS": len(p.career_history), "MPG": p.career_mpg(), "PPG": p.career_ppg(),
                "RPG": p.career_rpg(), "APG": p.career_apg(), "TITRES": p.total_championships(),
                "AWARDS": p.total_awards(), "NIVEAU": p.level})
    scoreboard({"XP TOTAL": p.total_xp_earned, "SAISONS NBA": p.nba_seasons,
                "GAINS": money(p.total_earnings)})

    if st.button("← Retour", key="back_hist"):
        goto("dashboard")


def screen_retired():
    p = st.session_state.player
    st.markdown('<div class="title-nba">🎬 Fin de carrière</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{p.name} — {len(p.career_history)} saisons, raccroche à {p.age} ans</div>',
                unsafe_allow_html=True)

    champs, nba = p.total_championships(), p.nba_seasons
    if champs >= 3 and nba >= 8:
        verdict, cls = "🐐 LÉGENDE — Hall of Fame au premier tour de scrutin.", "card-gold"
    elif champs >= 1 and nba >= 5:
        verdict, cls = "🏆 CHAMPION — un maillot retiré aux chevrons.", "card-gold"
    elif nba >= 5:
        verdict, cls = "🏀 CARRIÈRE NBA SOLIDE — tu as tenu au plus haut niveau.", "card-green"
    elif nba >= 1:
        verdict, cls = "✅ TU AS TOUCHÉ LE RÊVE — quelques saisons en NBA.", "card-green"
    elif champs >= 1:
        verdict, cls = "🥇 CHAMPION EN EUROPE — une belle carrière, sans la NBA.", "card"
    else:
        verdict, cls = "📘 CARRIÈRE HONNÊTE — la NBA est restée hors de portée.", "card"

    st.markdown(f'<div class="{cls}" style="text-align:center;padding:2rem">'
                f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.6rem;font-weight:800;color:#fff">'
                f'{verdict}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="verdict">{rich(p.career_verdict())}</div>', unsafe_allow_html=True)
    scoreboard({"SAISONS": len(p.career_history), "PPG": p.career_ppg(), "RPG": p.career_rpg(),
                "APG": p.career_apg(), "TITRES": champs, "AWARDS": p.total_awards(),
                "NBA": nba, "NIVEAU": p.level})
    st.markdown(f"<div style='text-align:center;color:#ffa53a;font-size:1.2rem;font-weight:700'>"
                f"💼 {money(p.total_earnings)} gagnés en carrière</div>", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📊 Revoir l'historique", key="ret_hist"):
            goto("history")
    with c2:
        if st.button("🏀 Nouvelle carrière", key="ret_new"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            init_state()
            goto("home")


# ── Router ─────────────────────────────────────────────────────────────────────
SCREENS = {
    "home": screen_home, "create": screen_create, "offers": screen_offers,
    "dashboard": screen_dashboard, "prepare": screen_prepare,
    "season_result": screen_season_result, "sponsors": screen_sponsors,
    "interview": screen_interview,
    "draft_night": screen_draft_night, "history": screen_history, "retired": screen_retired,
}

screen = st.session_state.screen
needs_player = screen not in ("home", "create")
if needs_player and not st.session_state.player:
    st.session_state.screen = "home"
    st.rerun()
SCREENS.get(screen, screen_home)()
