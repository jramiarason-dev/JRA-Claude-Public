import streamlit as st
import random

from game.player import Player, xp_for_level
from game.leagues import LEAGUES, COUNTRIES, POSITIONS, get_next_league
from game.events import get_random_event, get_draft_event
from game.simulator import (simulate_season, simulate_playoffs, apply_season_results,
                             check_promotion_eligibility, is_draft_eligible)

st.set_page_config(page_title="NBA Dream — Career Simulator", page_icon="🏀",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0a0a0f !important; color: #f0f0f0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: #0a0a0f !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1200px; margin: auto; }
.card { background: linear-gradient(135deg,#111120,#1a1a2e); border:1px solid #2a2a4a; border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem; }
.card-gold { background: linear-gradient(135deg,#1a1400,#2a2000); border:1px solid #c9a227; border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem; }
.card-red  { background: linear-gradient(135deg,#1a0000,#2a0a0a); border:1px solid #e03a3a; border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem; }
.card-green{ background: linear-gradient(135deg,#001a00,#0a2a0a); border:1px solid #3aaa3a; border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1rem; }
.stat-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(90px,1fr)); gap:.7rem; margin:.8rem 0; }
.stat-box  { background:#16162a; border:1px solid #2a2a4a; border-radius:8px; padding:.6rem; text-align:center; }
.stat-value{ font-size:1.5rem; font-weight:900; color:#c9a227; }
.stat-label{ font-size:.68rem; color:#888; text-transform:uppercase; letter-spacing:.05em; }
.attr-row  { margin:.4rem 0; }
.attr-label{ font-size:.8rem; color:#aaa; display:flex; justify-content:space-between; margin-bottom:2px; }
.attr-bar-bg  { background:#1e1e3a; border-radius:4px; height:8px; overflow:hidden; }
.attr-bar-fill{ height:100%; border-radius:4px; }
.badge { display:inline-block; padding:.2rem .6rem; border-radius:20px; font-size:.72rem; font-weight:700; text-transform:uppercase; letter-spacing:.04em; margin-right:4px; }
.badge-gold  { background:#c9a227; color:#000; }
.badge-blue  { background:#1e6aa8; color:#fff; }
.badge-red   { background:#c0392b; color:#fff; }
.badge-green { background:#27ae60; color:#fff; }
.badge-gray  { background:#444;    color:#ccc; }
.badge-purple{ background:#7b2fbe; color:#fff; }
.title-nba { font-size:2.8rem; font-weight:900; text-align:center; background:linear-gradient(90deg,#c9a227,#fff,#c9a227); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; line-height:1.1; margin-bottom:.3rem; }
.subtitle  { text-align:center; color:#888; font-size:.95rem; margin-bottom:2rem; }
.path-step   { display:inline-flex; align-items:center; gap:4px; padding:4px 10px; border-radius:20px; font-size:.75rem; font-weight:600; margin:2px; }
.path-done   { background:#1e4a1e; color:#3aaa3a; border:1px solid #3aaa3a; }
.path-current{ background:#4a3a00; color:#c9a227; border:1px solid #c9a227; }
.path-future { background:#1a1a2a; color:#555;    border:1px solid #333; }
h1,h2,h3 { color:#f0f0f0 !important; }
.section-header { font-size:.75rem; font-weight:700; text-transform:uppercase; letter-spacing:.1em; color:#c9a227; border-bottom:1px solid #2a2a4a; padding-bottom:6px; margin-bottom:12px; }
div.stButton > button { background:linear-gradient(135deg,#c9a227,#a67c00) !important; color:#000 !important; font-weight:700 !important; border:none !important; border-radius:8px !important; padding:.6rem 1.4rem !important; font-size:.9rem !important; width:100%; }
div.stButton > button:hover { opacity:.85 !important; }
hr { border-color:#2a2a4a !important; }
.event-positive{ background:linear-gradient(135deg,#001a08,#003010); border-left:4px solid #27ae60; padding:1rem; border-radius:0 8px 8px 0; margin:.5rem 0; }
.event-negative{ background:linear-gradient(135deg,#1a0000,#2a0808); border-left:4px solid #e03a3a; padding:1rem; border-radius:0 8px 8px 0; margin:.5rem 0; }
.event-neutral { background:linear-gradient(135deg,#00081a,#001530); border-left:4px solid #3a7ae0; padding:1rem; border-radius:0 8px 8px 0; margin:.5rem 0; }
.playoff-champ   { background:linear-gradient(135deg,#1a1000,#3a2a00); border:2px solid #c9a227; border-radius:12px; padding:1.2rem; margin:.5rem 0; text-align:center; }
.playoff-finalist{ background:linear-gradient(135deg,#0a0a1a,#12122a); border:1px solid #888; border-radius:12px; padding:1rem; margin:.5rem 0; }
.level-up { background:linear-gradient(135deg,#1a001a,#2a002a); border:2px solid #c040e0; border-radius:12px; padding:1rem; margin:.5rem 0; text-align:center; }
.xp-bar-bg  { background:#1e1e3a; border-radius:6px; height:10px; overflow:hidden; margin-top:3px; }
.xp-bar-fill{ height:100%; border-radius:6px; background:linear-gradient(90deg,#7b2fbe,#c040e0); }
.career-table { width:100%; border-collapse:collapse; font-size:.78rem; }
.career-table th { background:#16162a; color:#c9a227; padding:8px 10px; text-align:left; border-bottom:1px solid #2a2a4a; }
.career-table td { padding:7px 10px; border-bottom:1px solid #1a1a2a; color:#ddd; }
.career-table tr:hover td { background:#1a1a2e; }
</style>
""", unsafe_allow_html=True)

# ── State ──────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {"screen": "home", "player": None, "season_sim": None, "season_event": None,
                "season_playoff": None, "season_training": None, "training_choice": None,
                "draft_result": None}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

# ── UI helpers ─────────────────────────────────────────────────────────────────
def attr_bar(label, value, color="#c9a227"):
    pct = min(100, max(0, value))
    st.markdown(f'<div class="attr-row"><div class="attr-label"><span>{label}</span><span>{value}</span></div>'
                f'<div class="attr-bar-bg"><div class="attr-bar-fill" style="width:{pct}%;background:{color}"></div></div></div>',
                unsafe_allow_html=True)

def xp_bar(player: Player):
    pct   = player.xp_progress_pct()
    needed = xp_for_level(player.level + 1)
    st.markdown(f'<div style="margin:.3rem 0">'
                f'<div style="display:flex;justify-content:space-between;font-size:.78rem;color:#aaa;margin-bottom:2px">'
                f'<span>⚡ Niveau {player.level}</span><span>{player.xp} / {needed} XP</span></div>'
                f'<div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{pct}%"></div></div></div>',
                unsafe_allow_html=True)

def stat_grid(stats):
    items = "".join([f'<div class="stat-box"><div class="stat-value">{v}</div>'
                     f'<div class="stat-label">{k}</div></div>' for k, v in stats.items()])
    st.markdown(f'<div class="stat-grid">{items}</div>', unsafe_allow_html=True)

def league_path_display(player: Player):
    path = COUNTRIES[player.country]["path"]
    done = [r.league for r in player.career_history]
    steps = []
    for lg in path:
        if lg in done and lg != player.current_league: cls, icon = "path-done", "✓"
        elif lg == player.current_league:             cls, icon = "path-current", "▶"
        else:                                         cls, icon = "path-future",  "○"
        steps.append(f'<span class="path-step {cls}">{icon} {LEAGUES.get(lg,{}).get("name",lg)}</span>')
    st.markdown(" → ".join(steps), unsafe_allow_html=True)

def reputation_bar(rep):
    color = "#27ae60" if rep >= 60 else "#c9a227" if rep >= 30 else "#e03a3a"
    st.markdown(f'<div style="margin:.3rem 0">'
                f'<div style="display:flex;justify-content:space-between;font-size:.8rem;color:#aaa;margin-bottom:3px">'
                f'<span>Réputation NBA</span><span>{rep}/100</span></div>'
                f'<div class="attr-bar-bg" style="height:12px"><div class="attr-bar-fill" style="width:{rep}%;background:{color}"></div></div></div>',
                unsafe_allow_html=True)

def player_header(player: Player):
    flag  = COUNTRIES[player.country]["flag"]
    overall  = player.overall_rating()
    prospect = player.nba_prospect_score()
    champs   = player.total_championships()
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        st.markdown(f"## {flag} {player.name}")
        champ_str = f" {'🏆'*min(champs,5)}" if champs else ""
        st.markdown(
            f"<span class='badge badge-blue'>{player.position_label()}</span>"
            f"<span class='badge badge-gray'>{player.country}</span>"
            f"<span class='badge badge-gray'>Saison {player.season_number}</span>"
            f"<span class='badge badge-gray'>Âge {player.age}</span>"
            f"<span class='badge badge-purple'>Niv.{player.level}</span>{champ_str}",
            unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align:center'><div class='stat-value' style='font-size:2.2rem'>{overall}</div><div class='stat-label'>Overall</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align:center'><div class='stat-value' style='font-size:2.2rem;color:#3aaa3a'>{prospect}</div><div class='stat-label'>Prospect</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div style='text-align:center'><div class='stat-value' style='font-size:2.2rem;color:#c040e0'>{player.level}</div><div class='stat-label'>Niveau</div></div>", unsafe_allow_html=True)
    reputation_bar(player.reputation)
    xp_bar(player)
    league_path_display(player)
    st.markdown("---")

# ── Screens ────────────────────────────────────────────────────────────────────
def screen_home():
    st.markdown('<div class="title-nba">🏀 NBA DREAM</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Career Simulator — De ton lycée à la NBA</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('''<div class="card"><div class="section-header">Comment jouer</div>
<p style="color:#bbb;font-size:.9rem;line-height:1.6">
Crée ton joueur, choisis ton pays et trace ta route vers la NBA.<br>
Chaque saison : <strong style="color:#c9a227">entraîne-toi</strong>, affronte des
<strong style="color:#c9a227">événements</strong>, joue les <strong style="color:#c9a227">playoffs</strong>
et monte en <strong style="color:#c040e0">niveau</strong>.<br><br>
Les scouts NBA t\'observent. Ta réputation détermine ta position de draft.
</p></div>''', unsafe_allow_html=True)
        st.markdown('''<div class="card"><div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem">
<div><span class="badge badge-green">🇫🇷 France</span><br><small style="color:#888">Pro B → Elite → EuroLeague → NBA</small></div>
<div><span class="badge badge-red">🇨🇭 Suisse</span><br><small style="color:#888">SBL → Pro B → Elite → NBA</small></div>
<div><span class="badge badge-gold">🇪🇸 Espagne</span><br><small style="color:#888">LEB Gold → ACB → EuroLeague → NBA</small></div>
<div><span class="badge badge-blue">🇺🇸 USA NCAA</span><br><small style="color:#888">High School → NCAA → NBA Draft</small></div>
</div></div>''', unsafe_allow_html=True)
        if st.button("🏀 DÉMARRER UNE CARRIÈRE", key="btn_start"):
            st.session_state.screen = "create"; st.rerun()

def screen_create():
    st.markdown('<div class="title-nba">⚙️ CRÉER TON JOUEUR</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Définis ton identité et ta trajectoire</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Identité</div>', unsafe_allow_html=True)
        name     = st.text_input("Nom du joueur", placeholder="ex: Théo Martin")
        country  = st.selectbox("Pays d'origine", list(COUNTRIES.keys()),
                                format_func=lambda c: f"{COUNTRIES[c]['flag']} {c}")
        position = st.selectbox("Poste", POSITIONS,
                                format_func=lambda p: {"PG":"PG — Meneur","SG":"SG — Arrière",
                                                        "SF":"SF — Ailier","PF":"PF — Ailier Fort","C":"C — Pivot"}[p])
        age = st.slider("Âge de départ", 15, 19, 17)
    with col2:
        st.markdown('<div class="section-header">Attributs de départ (max 225 pts)</div>', unsafe_allow_html=True)
        athl = st.slider("🏃 Athlétisme",    30, 70, 45)
        shot = st.slider("🎯 Tir",           30, 70, 45)
        biq  = st.slider("🧠 QI Basketball", 30, 70, 45)
        ment = st.slider("💪 Mental",        30, 70, 45)
        lead = st.slider("📣 Leadership",    30, 70, 40)
        total = athl + shot + biq + ment + lead
        color = "#27ae60" if total <= 225 else "#e03a3a"
        st.markdown(f"<div style='text-align:right;color:{color};font-weight:700'>Points: {total}/225</div>",
                    unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Retour", key="btn_back_home"): st.session_state.screen="home"; st.rerun()
    with c2:
        if not name: st.error("Donne un nom à ton joueur.")
        elif total > 225: st.error(f"Trop de points. Réduis de {total-225} pts.")
        elif st.button("✅ CRÉER ET DÉMARRER", key="btn_create"):
            sl = COUNTRIES[country]["start_league"]
            p  = Player(name=name, country=country, position=position, age=age,
                        athleticism=athl, shooting=shot, basketball_iq=biq, mental=ment, leadership=lead,
                        current_league=sl, current_team=random.choice(LEAGUES[sl]["teams"]))
            st.session_state.player = p; st.session_state.screen = "dashboard"; st.rerun()

def screen_dashboard():
    p = st.session_state.player
    player_header(p)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="section-header">Attributs</div>', unsafe_allow_html=True)
        attr_bar("🏃 Athlétisme",    p.athleticism)
        attr_bar("🎯 Tir",           p.shooting,      "#3a9ae0")
        attr_bar("🧠 QI Basketball", p.basketball_iq, "#9a3ae0")
        attr_bar("💪 Mental",        p.mental,         "#e0663a")
        attr_bar("📣 Leadership",    p.leadership,     "#3ae09a")
        st.markdown('<div class="section-header" style="margin-top:1rem">État</div>', unsafe_allow_html=True)
        cm, cf = st.columns(2)
        with cm:
            mc = "#27ae60" if p.morale>=60 else "#c9a227" if p.morale>=40 else "#e03a3a"
            st.markdown(f"<div style='color:{mc};font-weight:700'>😤 Moral: {p.morale}/100</div>", unsafe_allow_html=True)
        with cf:
            fc = "#27ae60" if p.fitness>=70 else "#c9a227" if p.fitness>=50 else "#e03a3a"
            st.markdown(f"<div style='color:{fc};font-weight:700'>🏋️ Forme: {p.fitness}/100</div>", unsafe_allow_html=True)
    with col2:
        ld = LEAGUES.get(p.current_league, {})
        st.markdown('<div class="section-header">Ligue actuelle</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-gold">'
                    f'<div style="font-size:1.1rem;font-weight:700">{ld.get("name",p.current_league)}</div>'
                    f'<div style="color:#888;font-size:.8rem;margin-top:4px">{p.current_team}</div>'
                    f'<div style="margin-top:8px;color:#c9a227">Difficulté: {"⭐"*ld.get("level",1)}<br>'
                    f'Matchs: {ld.get("games",0)}<br>Scouts NBA: {int(ld.get("scout_presence",0)*100)}%</div></div>',
                    unsafe_allow_html=True)
        if ld.get("salary", 0) > 0:
            st.markdown(f"<div style='color:#27ae60;font-weight:700'>💰 {ld['salary']:,}€/saison</div>",
                        unsafe_allow_html=True)
        st.markdown(f"<div style='color:#aaa;font-size:.8rem;margin-top:.5rem'>"
                    f"💼 {p.total_earnings:,}€ | 🏆 {p.total_championships()} titre(s)</div>",
                    unsafe_allow_html=True)
        if p.career_history:
            st.markdown('<div class="section-header" style="margin-top:1rem">Stats Carrière</div>',
                        unsafe_allow_html=True)
            stat_grid({"PPG": p.career_ppg(), "RPG": p.career_rpg(), "APG": p.career_apg()})
    st.markdown("---")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🏋️ PRÉPARER LA SAISON", key="btn_prep"):
            st.session_state.screen = "prepare"; st.rerun()
    with b2:
        if p.career_history and st.button("📊 HISTORIQUE", key="btn_history"):
            st.session_state.screen = "history"; st.rerun()
    with b3:
        if is_draft_eligible(p) and p.current_league != "NBA":
            if st.button("📋 ENTRER DANS LA DRAFT", key="btn_draft"):
                st.session_state.screen = "draft"; st.rerun()
        elif not p.career_history:
            st.info("Joue ta première saison.")

def screen_prepare():
    p = st.session_state.player
    player_header(p)
    st.markdown("## 🏋️ Préparation de la Saison")
    st.markdown("<p style='color:#888'>Ton choix d'entraînement influence les gains d'attributs ET les XP reçus en fin de saison.</p>",
                unsafe_allow_html=True)
    TRAINING = {
        "Tir":           {"icon":"🎯", "desc":"Shooting et précision",         "boosts":"+Tir, +Mental"},
        "Athletisme":    {"icon":"⚡", "desc":"Vitesse et explosivité",         "boosts":"+Athlétisme"},
        "QI Basketball": {"icon":"🧠", "desc":"Analyse vidéo, lecture de jeu", "boosts":"+QI, +Leadership"},
        "Mental":        {"icon":"🧘", "desc":"Gestion de la pression",         "boosts":"+Mental, +Leadership"},
        "Physique Complet":{"icon":"💪","desc":"Programme équilibré toutes aptitudes","boosts":"+Tout (modéré)"},
    }
    selected = st.session_state.get("training_choice")
    cols = st.columns(len(TRAINING))
    for i, (key, data) in enumerate(TRAINING.items()):
        with cols[i]:
            border = "2px solid #c9a227" if selected == key else "1px solid #2a2a4a"
            st.markdown(f'<div class="card" style="text-align:center;border:{border};min-height:150px">'
                        f'<div style="font-size:2rem">{data["icon"]}</div>'
                        f'<div style="font-weight:700;margin:4px 0">{key}</div>'
                        f'<div style="color:#888;font-size:.76rem">{data["desc"]}</div>'
                        f'<div style="color:#c9a227;font-size:.72rem;margin-top:5px">{data["boosts"]}</div></div>',
                        unsafe_allow_html=True)
            if st.button(f"Choisir {key}", key=f"train_{key}"):
                st.session_state.training_choice = key; st.rerun()
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Retour", key="btn_back_dash"): st.session_state.screen="dashboard"; st.rerun()
    with c2:
        if not selected:
            st.warning("Sélectionne un axe d'entraînement")
        elif st.button(f"✅ CONFIRMER : {selected}", key="btn_confirm_train"):
            p.train(selected)
            st.session_state.training_choice = None
            sim     = simulate_season(p)
            event   = get_random_event(p.reputation, p.morale, p.season_number)
            playoff = simulate_playoffs(p, sim["performance_factor"]) if sim.get("playoff_qualified") else None
            st.session_state.season_sim      = sim
            st.session_state.season_event    = event
            st.session_state.season_playoff  = playoff
            st.session_state.season_training = selected
            st.session_state.screen = "season_result"; st.rerun()

def screen_season_result():
    p       = st.session_state.player
    sim     = st.session_state.season_sim
    event   = st.session_state.season_event
    playoff = st.session_state.season_playoff
    training= st.session_state.get("season_training", "Physique Complet")
    if not sim: st.session_state.screen="dashboard"; st.rerun()

    record, leveled_up = apply_season_results(p, sim, event, training, playoff)
    player_header(p)
    st.markdown(f"## 📅 Bilan Saison {p.season_number}")

    # ─ Stats saison régulière
    st.markdown('<div class="section-header">Statistiques — Saison régulière</div>', unsafe_allow_html=True)
    stat_grid({"PPG": sim["ppg"], "RPG": sim["rpg"], "APG": sim["apg"],
               "SPG": sim["spg"], "BPG": sim["bpg"],
               "FG%": f"{int(sim['fg_pct']*100)}%", "Matchs": sim["games"]})
    if sim.get("award"):
        st.markdown(f'<div class="card-gold"><div style="font-size:1.1rem">🏆 {sim["award"]}</div>'
                    f'<div style="color:#aaa;font-size:.82rem">Récompense individuelle</div></div>',
                    unsafe_allow_html=True)

    # ─ Playoffs
    st.markdown('<div class="section-header">Playoffs</div>', unsafe_allow_html=True)
    if playoff is None:
        st.markdown('<div class="card"><div style="color:#888">❌ Ton équipe n\'a pas atteint les playoffs cette saison.</div></div>',
                    unsafe_allow_html=True)
    elif playoff.champion:
        st.balloons()
        st.markdown(f'<div class="playoff-champ">'
                    f'<div style="font-size:2.5rem">🏆</div>'
                    f'<div style="font-size:1.5rem;font-weight:900;color:#c9a227">{playoff.title}</div>'
                    f'<div style="color:#fff;margin-top:4px">{playoff.rounds_won}/3 rounds gagnés</div></div>',
                    unsafe_allow_html=True)
    elif playoff.reached_final:
        st.markdown(f'<div class="playoff-finalist">'
                    f'<div style="font-size:1.1rem;font-weight:700">🥈 Finaliste</div>'
                    f'<div style="color:#aaa;font-size:.85rem">Défaite en finale contre {playoff.opponent}.</div>'
                    f'<div style="color:#888;font-size:.8rem">{playoff.rounds_won}/3 rounds gagnés</div></div>',
                    unsafe_allow_html=True)
    elif playoff.rounds_won >= 1:
        st.markdown(f'<div class="card"><div style="font-size:1rem;font-weight:700">🎯 Demi-finale atteinte</div>'
                    f'<div style="color:#aaa;font-size:.85rem">Éliminé en demi-finale ({playoff.rounds_won}/3 rounds gagnés).</div></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="card"><div style="font-size:1rem;font-weight:700">📉 Éliminé en quarts</div>'
                    f'<div style="color:#aaa;font-size:.85rem">Défaite dès les quarts contre {playoff.opponent}.</div></div>',
                    unsafe_allow_html=True)

    # ─ Événement
    event_type  = event.get("type", "neutral")
    event_class = {"positive":"event-positive","negative":"event-negative","neutral":"event-neutral"}[event_type]
    rb = event.get("reputation_bonus", 0); mb = event.get("morale_bonus", 0)
    st.markdown(f'<div class="{event_class}">'
                f'<div style="font-size:1.05rem;font-weight:700">{event.get("title","")}</div>'
                f'<div style="color:#bbb;font-size:.88rem;margin-top:4px">{event.get("description","")}</div>'
                f'<div style="margin-top:8px;font-size:.8rem">'
                f'{"📈 Réputation +" if rb>0 else "📉 Réputation "}{rb}'
                f' | {"😊 Moral +" if mb>0 else "😔 Moral "}{mb}</div></div>',
                unsafe_allow_html=True)

    # ─ XP & Level Up
    st.markdown('<div class="section-header">Progression</div>', unsafe_allow_html=True)
    xp_gained = record.xp_gained
    if leveled_up:
        st.markdown(f'<div class="level-up">'
                    f'<div style="font-size:1.8rem">⚡</div>'
                    f'<div style="font-size:1.3rem;font-weight:900;color:#c040e0">NIVEAU {p.level} ATTEINT !</div>'
                    f'<div style="color:#aaa;font-size:.85rem;margin-top:4px">+{xp_gained} XP — Tes attributs ont augmenté</div></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="card"><div style="color:#c040e0;font-weight:700">+{xp_gained} XP cette saison</div>'
                    f'<div style="color:#888;font-size:.8rem">{p.xp}/{xp_for_level(p.level+1)} XP pour le niveau {p.level+1}</div></div>',
                    unsafe_allow_html=True)

    # ─ Actions
    can_promote = check_promotion_eligibility(p)
    next_league = get_next_league(p.current_league, p.country)
    draft_ok    = is_draft_eligible(p) and p.current_league != "NBA"
    st.markdown("---\n### Que veux-tu faire ?")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 Saison suivante (même ligue)", key="btn_next_same"):
            st.session_state.season_sim = None; st.session_state.screen="prepare"; st.rerun()
    with c2:
        if next_league and can_promote:
            if st.button(f"⬆️ Monter en {LEAGUES[next_league]['name']}", key="btn_promote"):
                p.current_league = next_league
                p.current_team   = random.choice(LEAGUES[next_league]["teams"])
                st.session_state.season_sim = None; st.session_state.screen="prepare"; st.rerun()
        elif next_league:
            st.markdown(f"<div style='color:#888;font-size:.82rem;padding:.5rem'>❌ Pas encore prêt pour {LEAGUES[next_league]['name']}</div>",
                        unsafe_allow_html=True)
    with c3:
        if draft_ok:
            if st.button("📋 Se déclarer pour la Draft NBA", key="btn_go_draft"):
                st.session_state.screen="draft"; st.rerun()
        elif p.age < (18 if p.country != "USA (NCAA)" else 19):
            st.markdown(f"<div style='color:#888;font-size:.82rem;padding:.5rem'>⏳ Draft dispo à {18 if p.country!='USA (NCAA)' else 19} ans</div>",
                        unsafe_allow_html=True)

def screen_draft():
    p = st.session_state.player
    player_header(p)
    st.markdown("## 📋 NBA DRAFT")
    prospect = p.nba_prospect_score()
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f'<div class="card"><div class="section-header">Ton profil de prospect</div>'
                    f'<p style="color:#bbb">Score prospect: <strong style="color:#c9a227">{prospect}/100</strong>'
                    f' — {p.season_number} saison(s), Niveau {p.level}</p></div>',
                    unsafe_allow_html=True)
        if prospect>=85:   msg,cls="🔥 Top 5 Pick probable — future star NBA","card-gold"
        elif prospect>=75: msg,cls="⭐ Lottery Pick probable","card-gold"
        elif prospect>=65: msg,cls="✅ 1er tour possible","card-green"
        elif prospect>=55: msg,cls="🎯 2ème tour probable","card"
        elif prospect>=48: msg,cls="📋 Agent libre non drafté — chance de signing","card"
        else:              msg,cls="❌ Trop tôt — renforce-toi","card-red"
        st.markdown(f'<div class="{cls}"><div>{msg}</div></div>', unsafe_allow_html=True)
    with c2:
        stat_grid({"Prospect": prospect, "Réputation": p.reputation,
                   "Overall": p.overall_rating(), "Niveau": p.level})
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Revenir", key="btn_back_from_draft"):
            st.session_state.screen = "season_result" if st.session_state.season_sim else "dashboard"
            st.rerun()
    with c2:
        if prospect >= 48:
            if st.button("🏀 SE DÉCLARER POUR LA DRAFT", key="btn_enter_draft"):
                result = get_draft_event(prospect, p.age)
                if result:
                    p.draft_round = result["round"]; p.draft_pick = result["pick"]
                    p.current_team = result["team"]; p.in_nba = True; p.current_league = "NBA"
                st.session_state.draft_result = result; st.session_state.screen="draft_result"; st.rerun()
        else:
            st.warning("Pas encore prêt pour la Draft.")

def screen_draft_result():
    p      = st.session_state.player
    result = st.session_state.draft_result
    st.markdown('<div class="title-nba">🎉 NUIT DE LA DRAFT</div>', unsafe_allow_html=True)
    if result and result["round"] == 1:
        st.balloons()
        st.markdown(f'<div class="card-gold" style="text-align:center;padding:2rem">'
                    f'<div style="font-size:3rem">🏀</div>'
                    f'<div style="font-size:1.8rem;font-weight:900;color:#c9a227">DRAFTÉ EN 1ER TOUR !</div>'
                    f'<div style="font-size:1.2rem;color:#fff">Pick #{result["pick"]} — {result["team"]}</div></div>',
                    unsafe_allow_html=True)
    elif result and result["round"] == 2:
        st.markdown(f'<div class="card-green" style="text-align:center;padding:2rem">'
                    f'<div style="font-size:3rem">🎯</div>'
                    f'<div style="font-size:1.5rem;font-weight:900;color:#27ae60">DRAFTÉ EN 2ÈME TOUR !</div>'
                    f'<div style="font-size:1.1rem;color:#fff">Pick #{result["pick"]} — {result["team"]}</div></div>',
                    unsafe_allow_html=True)
    elif result and result["round"] == 0:
        st.markdown(f'<div class="card" style="text-align:center;padding:2rem">'
                    f'<div style="font-size:3rem">✍️</div>'
                    f'<div style="font-size:1.4rem;font-weight:900">NON DRAFTÉ — MAIS SIGNÉ !</div>'
                    f'<div style="color:#aaa">{result["team"]} t\'offre un contrat.</div></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="card-red" style="text-align:center;padding:2rem">'
                    '<div style="font-size:3rem">😔</div>'
                    '<div style="font-size:1.4rem;font-weight:900;color:#e03a3a">NON RETENU</div>'
                    '<div style="color:#aaa">Continue à travailler.</div></div>',
                    unsafe_allow_html=True)
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if p.in_nba and st.button("🏀 JOUER EN NBA", key="btn_play_nba"):
            st.session_state.screen="dashboard"; st.rerun()
    with c2:
        if not p.in_nba and st.button("🔄 Continuer en Europe", key="btn_continue_eu"):
            st.session_state.draft_result=None; st.session_state.screen="dashboard"; st.rerun()
    if st.button("🏠 Retour à l'accueil", key="btn_home_draft"):
        st.session_state.screen="home"; st.session_state.player=None; st.rerun()

def screen_history():
    p = st.session_state.player
    player_header(p)
    st.markdown("## 📊 Historique de Carrière")
    if not p.career_history: st.info("Aucune saison jouée."); return

    rows = ""
    for r in p.career_history:
        if r.playoff:
            if r.playoff.champion:       po = "🏆 Champion"
            elif r.playoff.reached_final: po = "🥈 Finaliste"
            elif r.playoff.rounds_won>0:  po = "🎯 Demi-finale"
            else:                         po = "❌ Quarts"
        else:
            po = "— Non qualifié"
        lv = f"Niv.{r.level_before}"
        if r.level_after > r.level_before:
            lv += f" → <span style='color:#c040e0'>Niv.{r.level_after}⬆</span>"
        rows += (
            f"<tr><td>S{r.season}</td><td>{r.age} ans</td>"
            f"<td>{LEAGUES.get(r.league,{}).get('name',r.league)}</td>"
            f"<td style='font-size:.72rem;color:#aaa'>{r.team}</td>"
            f"<td style='color:#c9a227'>{r.ppg}</td><td>{r.rpg}</td><td>{r.apg}</td>"
            f"<td>{int(r.fg_pct*100)}%</td><td>{r.games}</td>"
            f"<td style='font-size:.72rem'>{'🏆 '+r.award if r.award else ''}</td>"
            f"<td style='font-size:.75rem'>{po}</td>"
            f"<td style='color:#c040e0;font-size:.75rem'>+{r.xp_gained}</td>"
            f"<td style='font-size:.75rem'>{lv}</td>"
            f"<td style='color:#888;font-size:.72rem'>{r.training_focus or ''}</td></tr>"
        )
    st.markdown(
        '<div style="overflow-x:auto"><table class="career-table"><thead><tr>'
        '<th>Sais.</th><th>Âge</th><th>Ligue</th><th>Équipe</th>'
        '<th>PPG</th><th>RPG</th><th>APG</th><th>FG%</th><th>G</th>'
        '<th>Award</th><th>Playoffs</th><th>XP</th><th>Niveau</th><th>Training</th>'
        f'</tr></thead><tbody>{rows}</tbody></table></div>',
        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Résumé de carrière</div>', unsafe_allow_html=True)
    stat_grid({"PPG moy.": p.career_ppg(), "RPG moy.": p.career_rpg(), "APG moy.": p.career_apg(),
               "Saisons": len(p.career_history), "Titres 🏆": p.total_championships(),
               "Niveau": p.level, "XP total": p.total_xp_earned, "Gains": f"{p.total_earnings:,}€"})

    if st.button("← Retour au Dashboard", key="btn_back_hist"):
        st.session_state.screen="dashboard"; st.rerun()

# ── Router ─────────────────────────────────────────────────────────────────────
screen = st.session_state.screen
if   screen=="home":         screen_home()
elif screen=="create":       screen_create()
elif screen=="dashboard":
    if not st.session_state.player: st.session_state.screen="home"; st.rerun()
    else: screen_dashboard()
elif screen=="prepare":      screen_prepare()
elif screen=="season_result":screen_season_result()
elif screen=="draft":        screen_draft()
elif screen=="draft_result": screen_draft_result()
elif screen=="history":      screen_history()
else: st.session_state.screen="home"; st.rerun()
