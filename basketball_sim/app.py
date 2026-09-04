import streamlit as st
import random

from game.player import Player
from game.leagues import LEAGUES, COUNTRIES, POSITIONS, get_next_league
from game.events import get_random_event, get_draft_event
from game.simulator import simulate_season, apply_season_results, check_promotion_eligibility, is_draft_eligible

st.set_page_config(page_title="NBA Dream — Career Simulator", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #0a0a0f !important; color: #f0f0f0 !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stHeader"] { background: #0a0a0f !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1200px; margin: auto; }
.card { background: linear-gradient(135deg, #111120 0%, #1a1a2e 100%); border: 1px solid #2a2a4a; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
.card-gold { background: linear-gradient(135deg, #1a1400 0%, #2a2000 100%); border: 1px solid #c9a227; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
.card-red { background: linear-gradient(135deg, #1a0000 0%, #2a0a0a 100%); border: 1px solid #e03a3a; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
.card-green { background: linear-gradient(135deg, #001a00 0%, #0a2a0a 100%); border: 1px solid #3aaa3a; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 0.8rem; margin: 0.8rem 0; }
.stat-box { background: #16162a; border: 1px solid #2a2a4a; border-radius: 8px; padding: 0.6rem; text-align: center; }
.stat-value { font-size: 1.6rem; font-weight: 900; color: #c9a227; }
.stat-label { font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 0.05em; }
.attr-row { margin: 0.4rem 0; }
.attr-label { font-size: 0.8rem; color: #aaa; display: flex; justify-content: space-between; margin-bottom: 2px; }
.attr-bar-bg { background: #1e1e3a; border-radius: 4px; height: 8px; overflow: hidden; }
.attr-bar-fill { height: 100%; border-radius: 4px; }
.badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin-right: 4px; }
.badge-gold { background: #c9a227; color: #000; } .badge-blue { background: #1e6aa8; color: #fff; } .badge-red { background: #c0392b; color: #fff; } .badge-green { background: #27ae60; color: #fff; } .badge-gray { background: #444; color: #ccc; }
.title-nba { font-size: 2.8rem; font-weight: 900; text-align: center; background: linear-gradient(90deg, #c9a227, #fff, #c9a227); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.1; margin-bottom: 0.3rem; }
.subtitle { text-align: center; color: #888; font-size: 0.95rem; margin-bottom: 2rem; }
.path-step { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin: 2px; }
.path-done { background: #1e4a1e; color: #3aaa3a; border: 1px solid #3aaa3a; } .path-current { background: #4a3a00; color: #c9a227; border: 1px solid #c9a227; } .path-future { background: #1a1a2a; color: #555; border: 1px solid #333; }
h1, h2, h3 { color: #f0f0f0 !important; }
.section-header { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #c9a227; border-bottom: 1px solid #2a2a4a; padding-bottom: 6px; margin-bottom: 12px; }
div.stButton > button { background: linear-gradient(135deg, #c9a227, #a67c00) !important; color: #000 !important; font-weight: 700 !important; border: none !important; border-radius: 8px !important; padding: 0.6rem 1.4rem !important; font-size: 0.9rem !important; width: 100%; }
div.stButton > button:hover { opacity: 0.85 !important; }
hr { border-color: #2a2a4a !important; }
.event-positive { background: linear-gradient(135deg, #001a08, #003010); border-left: 4px solid #27ae60; padding: 1rem; border-radius: 0 8px 8px 0; margin: 0.5rem 0; }
.event-negative { background: linear-gradient(135deg, #1a0000, #2a0808); border-left: 4px solid #e03a3a; padding: 1rem; border-radius: 0 8px 8px 0; margin: 0.5rem 0; }
.event-neutral { background: linear-gradient(135deg, #00081a, #001530); border-left: 4px solid #3a7ae0; padding: 1rem; border-radius: 0 8px 8px 0; margin: 0.5rem 0; }
.career-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.career-table th { background: #16162a; color: #c9a227; padding: 8px 10px; text-align: left; border-bottom: 1px solid #2a2a4a; }
.career-table td { padding: 7px 10px; border-bottom: 1px solid #1a1a2a; color: #ddd; }
.career-table tr:hover td { background: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

def init_state():
    defaults = {"screen": "home", "player": None, "season_sim": None, "season_event": None, "training_choice": None, "draft_result": None}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

def attr_bar(label, value, color="#c9a227"):
    pct = min(100, max(0, value))
    st.markdown(f'<div class="attr-row"><div class="attr-label"><span>{label}</span><span>{value}</span></div><div class="attr-bar-bg"><div class="attr-bar-fill" style="width:{pct}%;background:{color}"></div></div></div>', unsafe_allow_html=True)

def stat_grid(stats):
    items = "".join([f'<div class="stat-box"><div class="stat-value">{v}</div><div class="stat-label">{k}</div></div>' for k, v in stats.items()])
    st.markdown(f'<div class="stat-grid">{items}</div>', unsafe_allow_html=True)

def league_path_display(player):
    path = COUNTRIES[player.country]["path"]
    steps = []
    for league in path:
        done_leagues = [r.league for r in player.career_history]
        if league in done_leagues: cls, icon = "path-done", "✓"
        elif league == player.current_league: cls, icon = "path-current", "▶"
        else: cls, icon = "path-future", "○"
        name = LEAGUES.get(league, {}).get("name", league)
        steps.append(f'<span class="path-step {cls}">{icon} {name}</span>')
    st.markdown(" → ".join(steps), unsafe_allow_html=True)

def reputation_bar(rep):
    color = "#27ae60" if rep >= 60 else "#c9a227" if rep >= 30 else "#e03a3a"
    st.markdown(f'<div style="margin:0.3rem 0"><div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#aaa;margin-bottom:3px"><span>Réputation NBA</span><span>{rep}/100</span></div><div class="attr-bar-bg" style="height:12px"><div class="attr-bar-fill" style="width:{rep}%;background:{color}"></div></div></div>', unsafe_allow_html=True)

def player_header(player):
    flag = COUNTRIES[player.country]["flag"]
    overall = player.overall_rating()
    prospect = player.nba_prospect_score()
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"## {flag} {player.name}")
        st.markdown(f"<span class='badge badge-blue'>{player.position_label()}</span> <span class='badge badge-gray'>{player.country}</span> <span class='badge badge-gray'>Saison {player.season_number}</span> <span class='badge badge-gray'>Âge {player.age}</span>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align:center'><div class='stat-value' style='font-size:2.5rem'>{overall}</div><div class='stat-label'>Overall</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align:center'><div class='stat-value' style='font-size:2.5rem;color:#3aaa3a'>{prospect}</div><div class='stat-label'>Prospect</div></div>", unsafe_allow_html=True)
    reputation_bar(player.reputation)
    league_path_display(player)
    st.markdown("---")

def screen_home():
    st.markdown('<div class="title-nba">🏀 NBA DREAM</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Career Simulator — De ton lycée à la NBA</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="card"><div class="section-header">Comment jouer</div><p style="color:#bbb;font-size:0.9rem;line-height:1.6">Crée ton joueur, choisis ton pays de départ et trace ta route vers la NBA.<br>Chaque saison, tu devras <strong style="color:#c9a227">t\'entraîner</strong>, gérer des <strong style="color:#c9a227">événements imprévus</strong> et décider si tu <strong style="color:#c9a227">montes de division</strong>.<br><br>Les scouts NBA t\'observent. Ta réputation détermine ta position de draft.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem"><div><span class="badge badge-green">🇫🇷 France</span><br><small style="color:#888">Pro B → Elite → EuroLeague → NBA</small></div><div><span class="badge badge-red">🇨🇭 Suisse</span><br><small style="color:#888">SBL → Pro B → Elite → NBA</small></div><div><span class="badge badge-gold">🇪🇸 Espagne</span><br><small style="color:#888">LEB Gold → ACB → EuroLeague → NBA</small></div><div><span class="badge badge-blue">🇺🇸 USA NCAA</span><br><small style="color:#888">High School → NCAA → NBA Draft</small></div></div></div>', unsafe_allow_html=True)
        if st.button("🏀 DÉMARRER UNE CARRIÈRE", key="btn_start"):
            st.session_state.screen = "create"; st.rerun()

def screen_create():
    st.markdown('<div class="title-nba">⚙️ CRÉER TON JOUEUR</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Définis ton identité et ta trajectoire</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Identité</div>', unsafe_allow_html=True)
        name = st.text_input("Nom du joueur", placeholder="ex: Théo Martin")
        country = st.selectbox("Pays d'origine", list(COUNTRIES.keys()), format_func=lambda c: f"{COUNTRIES[c]['flag']} {c}")
        position = st.selectbox("Poste", POSITIONS, format_func=lambda p: {"PG": "PG — Meneur", "SG": "SG — Arrière", "SF": "SF — Ailier", "PF": "PF — Ailier Fort", "C": "C — Pivot"}[p])
        age = st.slider("Âge de départ", 15, 19, 17)
    with col2:
        st.markdown('<div class="section-header">Attributs de départ</div>', unsafe_allow_html=True)
        athleticism = st.slider("🏃 Athlétisme", 30, 70, 45)
        shooting = st.slider("🎯 Tir", 30, 70, 45)
        basketball_iq = st.slider("🧠 QI Basketball", 30, 70, 45)
        mental = st.slider("💪 Mental", 30, 70, 45)
        leadership = st.slider("📣 Leadership", 30, 70, 40)
        total = athleticism + shooting + basketball_iq + mental + leadership
        color = "#27ae60" if total <= 225 else "#e03a3a"
        st.markdown(f"<div style='text-align:right;color:{color};font-weight:700'>Points: {total}/225</div>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("← Retour", key="btn_back_home"): st.session_state.screen = "home"; st.rerun()
    with col_btn2:
        if not name: st.error("Donne un nom à ton joueur.")
        elif total > 225: st.error(f"Trop de points. Réduis de {total-225} pts.")
        elif st.button("✅ CRÉER ET DÉMARRER", key="btn_create"):
            start_league = COUNTRIES[country]["start_league"]
            player = Player(name=name, country=country, position=position, age=age, athleticism=athleticism, shooting=shooting, basketball_iq=basketball_iq, mental=mental, leadership=leadership, current_league=start_league, current_team=random.choice(LEAGUES[start_league]["teams"]))
            st.session_state.player = player; st.session_state.screen = "dashboard"; st.rerun()

def screen_dashboard():
    player = st.session_state.player
    player_header(player)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="section-header">Attributs</div>', unsafe_allow_html=True)
        attr_bar("🏃 Athlétisme", player.athleticism)
        attr_bar("🎯 Tir", player.shooting, "#3a9ae0")
        attr_bar("🧠 QI Basketball", player.basketball_iq, "#9a3ae0")
        attr_bar("💪 Mental", player.mental, "#e0663a")
        attr_bar("📣 Leadership", player.leadership, "#3ae09a")
        st.markdown('<div class="section-header" style="margin-top:1rem">État</div>', unsafe_allow_html=True)
        col_m, col_f = st.columns(2)
        with col_m: st.markdown(f"<div style='color:{'#27ae60' if player.morale>=60 else '#c9a227' if player.morale>=40 else '#e03a3a'};font-weight:700'>😤 Moral: {player.morale}/100</div>", unsafe_allow_html=True)
        with col_f: st.markdown(f"<div style='color:{'#27ae60' if player.fitness>=70 else '#c9a227' if player.fitness>=50 else '#e03a3a'};font-weight:700'>🏋️ Forme: {player.fitness}/100</div>", unsafe_allow_html=True)
    with col2:
        league_data = LEAGUES.get(player.current_league, {})
        st.markdown('<div class="section-header">Ligue actuelle</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-gold"><div style="font-size:1.1rem;font-weight:700">{league_data.get("name", player.current_league)}</div><div style="color:#888;font-size:0.8rem;margin-top:4px">{player.current_team}</div><div style="margin-top:8px;color:#c9a227">Difficulté: {"⭐" * league_data.get("level",1)}<br>Matchs: {league_data.get("games",0)}<br>Scouts NBA: {int(league_data.get("scout_presence",0)*100)}%</div></div>', unsafe_allow_html=True)
        if league_data.get("salary", 0) > 0: st.markdown(f"<div style='color:#27ae60;font-weight:700'>💰 {league_data['salary']:,}€/saison</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#aaa;font-size:0.8rem;margin-top:0.5rem'>💼 Total gagné: {player.total_earnings:,}€</div>", unsafe_allow_html=True)
        if player.career_history:
            st.markdown('<div class="section-header" style="margin-top:1rem">Stats Carrière</div>', unsafe_allow_html=True)
            stat_grid({"PPG": player.career_ppg(), "RPG": player.career_rpg(), "APG": player.career_apg()})
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("🏋️ PRÉPARER LA SAISON", key="btn_prep"): st.session_state.screen = "prepare"; st.rerun()
    with col_btn2:
        if player.career_history and st.button("📊 HISTORIQUE", key="btn_history"): st.session_state.screen = "history"; st.rerun()
    with col_btn3:
        if is_draft_eligible(player) and player.current_league != "NBA":
            if st.button("📋 ENTRER DANS LA DRAFT", key="btn_draft"): st.session_state.screen = "draft"; st.rerun()
        elif not player.career_history: st.info("Joue ta première saison.")

def screen_prepare():
    player = st.session_state.player
    player_header(player)
    st.markdown("## 🏋️ Préparation de la Saison")
    training_options = {
        "Tir": {"🎯": "🎯", "desc": "Améliore ton shooting", "boosts": "+Tir, +Mental"},
        "Athletisme": {"icon": "⚡", "desc": "Vitesse et explosivité", "boosts": "+Athlétisme"},
        "QI Basketball": {"icon": "🧠", "desc": "Analyse vidéo, lecture de jeu", "boosts": "+QI, +Leadership"},
        "Mental": {"icon": "🧘", "desc": "Gestion de la pression", "boosts": "+Mental, +Leadership"},
        "Physique Complet": {"icon": "💪", "desc": "Programme équilibré", "boosts": "+Tout (modéré)"},
    }
    selected = st.session_state.get("training_choice")
    cols = st.columns(len(training_options))
    for i, (key, data) in enumerate(training_options.items()):
        with cols[i]:
            border = "2px solid #c9a227" if selected == key else "1px solid #2a2a4a"
            icon = data.get("icon", data.get("🎯", "🏀"))
            st.markdown(f'<div class="card" style="text-align:center;border:{border};min-height:150px"><div style="font-size:2rem">{icon}</div><div style="font-weight:700;margin:4px 0">{key}</div><div style="color:#888;font-size:0.78rem">{data["desc"]}</div><div style="color:#c9a227;font-size:0.72rem;margin-top:6px">{data["boosts"]}</div></div>', unsafe_allow_html=True)
            if st.button(f"Choisir {key}", key=f"train_{key}"): st.session_state.training_choice = key; st.rerun()
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Retour", key="btn_back_dash"): st.session_state.screen = "dashboard"; st.rerun()
    with col2:
        if not selected: st.warning("Sélectionne un axe d'entraînement")
        elif st.button(f"✅ CONFIRMER : {selected}", key="btn_confirm_train"):
            player.train(selected)
            st.session_state.training_choice = None
            st.session_state.season_sim = simulate_season(player)
            st.session_state.season_event = get_random_event(player.reputation, player.morale, player.season_number)
            st.session_state.screen = "season_result"; st.rerun()

def screen_season_result():
    player = st.session_state.player
    sim = st.session_state.season_sim
    event = st.session_state.season_event
    if not sim: st.session_state.screen = "dashboard"; st.rerun()
    record = apply_season_results(player, sim, event)
    player_header(player)
    st.markdown(f"## 📅 Bilan Saison {player.season_number}")
    st.markdown('<div class="section-header">Statistiques</div>', unsafe_allow_html=True)
    stat_grid({"PPG": sim["ppg"], "RPG": sim["rpg"], "APG": sim["apg"], "SPG": sim["spg"], "BPG": sim["bpg"], "FG%": f"{int(sim['fg_pct']*100)}%", "Matchs": sim["games"]})
    if sim.get("award"): st.markdown(f'<div class="card-gold"><div style="font-size:1.2rem">🏆 {sim["award"]}</div></div>', unsafe_allow_html=True)
    event_type = event.get("type", "neutral")
    event_class = {"positive": "event-positive", "negative": "event-negative", "neutral": "event-neutral"}[event_type]
    rep_bonus = event.get('reputation_bonus', 0)
    mor_bonus = event.get('morale_bonus', 0)
    st.markdown(f'<div class="{event_class}"><div style="font-size:1.05rem;font-weight:700">{event.get("title","")}</div><div style="color:#bbb;font-size:0.88rem;margin-top:4px">{event.get("description","")}</div><div style="margin-top:8px;font-size:0.8rem">{"📈 Réputation +" if rep_bonus>0 else "📉 Réputation "}{rep_bonus} | {"😊 Moral +" if mor_bonus>0 else "😔 Moral "}{mor_bonus}</div></div>', unsafe_allow_html=True)
    can_promote = check_promotion_eligibility(player)
    next_league = get_next_league(player.current_league, player.country)
    draft_ok = is_draft_eligible(player) and player.current_league != "NBA"
    st.markdown("---\n### Que veux-tu faire ?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Saison suivante (même ligue)", key="btn_next_same"):
            st.session_state.season_sim = None; st.session_state.season_event = None; st.session_state.screen = "prepare"; st.rerun()
    with col2:
        if next_league and can_promote:
            if st.button(f"⬆️ Monter en {LEAGUES[next_league]['name']}", key="btn_promote"):
                player.current_league = next_league; player.current_team = random.choice(LEAGUES[next_league]["teams"])
                st.session_state.season_sim = None; st.session_state.season_event = None; st.session_state.screen = "prepare"; st.rerun()
        elif next_league: st.markdown(f"<div style='color:#888;font-size:0.82rem;padding:0.5rem'>❌ Pas encore pour {LEAGUES[next_league]['name']}</div>", unsafe_allow_html=True)
    with col3:
        if draft_ok:
            if st.button("📋 Draft NBA", key="btn_go_draft"): st.session_state.screen = "draft"; st.rerun()
        elif player.age < (18 if player.country != "USA (NCAA)" else 19):
            st.markdown(f"<div style='color:#888;font-size:0.82rem;padding:0.5rem'>⏳ Draft disponible à {18 if player.country != 'USA (NCAA)' else 19} ans</div>", unsafe_allow_html=True)

def screen_draft():
    player = st.session_state.player
    player_header(player)
    st.markdown("## 📋 NBA DRAFT")
    prospect = player.nba_prospect_score()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<div class="card"><div class="section-header">Ton profil de prospect</div><p style="color:#bbb">Score de prospect: <strong style="color:#c9a227">{prospect}/100</strong> — {player.season_number} saison(s) jouée(s).</p></div>', unsafe_allow_html=True)
        if prospect>=85: msg,cls="🔥 Top 5 Pick probable — future star NBA","card-gold"
        elif prospect>=75: msg,cls="⭐ Lottery Pick probable","card-gold"
        elif prospect>=65: msg,cls="✅ 1er tour possible","card-green"
        elif prospect>=55: msg,cls="🎯 2ème tour probable","card"
        elif prospect>=48: msg,cls="📋 Agent libre non drafté — chance de signing","card"
        else: msg,cls="❌ Trop tôt — renforce-toi","card-red"
        st.markdown(f'<div class="{cls}"><div>{msg}</div></div>', unsafe_allow_html=True)
    with col2: stat_grid({"Prospect": prospect, "Réputation": player.reputation, "Overall": player.overall_rating()})
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Revenir", key="btn_back_from_draft"): st.session_state.screen = "season_result" if st.session_state.season_sim else "dashboard"; st.rerun()
    with col2:
        if prospect>=48:
            if st.button("🏀 SE DÉCLARER POUR LA DRAFT", key="btn_enter_draft"):
                result = get_draft_event(prospect, player.age)
                if result: player.draft_round=result["round"]; player.draft_pick=result["pick"]; player.current_team=result["team"]; player.in_nba=True; player.current_league="NBA"
                st.session_state.draft_result = result; st.session_state.screen = "draft_result"; st.rerun()
        else: st.warning("Pas encore prêt pour la Draft.")

def screen_draft_result():
    player = st.session_state.player
    result = st.session_state.draft_result
    st.markdown('<div class="title-nba">🎉 NUIT DE LA DRAFT</div>', unsafe_allow_html=True)
    if result and result["round"]==1:
        st.balloons()
        st.markdown(f'<div class="card-gold" style="text-align:center;padding:2rem"><div style="font-size:3rem">🏀</div><div style="font-size:1.8rem;font-weight:900;color:#c9a227">DRAFTÉ EN 1ER TOUR !</div><div style="font-size:1.2rem;color:#fff">Pick #{result["pick"]} — {result["team"]}</div></div>', unsafe_allow_html=True)
    elif result and result["round"]==2:
        st.markdown(f'<div class="card-green" style="text-align:center;padding:2rem"><div style="font-size:3rem">🎯</div><div style="font-size:1.5rem;font-weight:900;color:#27ae60">DRAFTÉ EN 2ÈME TOUR !</div><div style="font-size:1.1rem;color:#fff">Pick #{result["pick"]} — {result["team"]}</div></div>', unsafe_allow_html=True)
    elif result and result["round"]==0:
        st.markdown(f'<div class="card" style="text-align:center;padding:2rem"><div style="font-size:3rem">✍️</div><div style="font-size:1.4rem;font-weight:900">NON DRAFTÉ — MAIS SIGNÉ !</div><div style="color:#aaa">{result["team"]} t\'offre un contrat.</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card-red" style="text-align:center;padding:2rem"><div style="font-size:3rem">😔</div><div style="font-size:1.4rem;font-weight:900;color:#e03a3a">NON RETENU</div><div style="color:#aaa">Continue à travailler.</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if player.in_nba and st.button("🏀 JOUER EN NBA", key="btn_play_nba"): st.session_state.screen="dashboard"; st.rerun()
    with col2:
        if not player.in_nba and st.button("🔄 Continuer en Europe", key="btn_continue_eu"): st.session_state.draft_result=None; st.session_state.screen="dashboard"; st.rerun()
    if st.button("🏠 Retour à l'accueil", key="btn_home_draft"): st.session_state.screen="home"; st.session_state.player=None; st.rerun()

def screen_history():
    player = st.session_state.player
    player_header(player)
    st.markdown("## 📊 Historique de Carrière")
    if not player.career_history: st.info("Aucune saison jouée."); return
    rows = ""
    for r in player.career_history:
        rows += f'<tr><td>S{r.season}</td><td>{r.age} ans</td><td>{LEAGUES.get(r.league,{}).get("name",r.league)}</td><td>{r.team}</td><td style="color:#c9a227">{r.ppg}</td><td>{r.rpg}</td><td>{r.apg}</td><td>{int(r.fg_pct*100)}%</td><td>{r.games}</td><td>{"🏆 "+r.award if r.award else ""}</td><td style="color:#888;font-size:0.75rem">{r.event or ""}</td></tr>'
    st.markdown(f'<div style="overflow-x:auto"><table class="career-table"><thead><tr><th>Sais.</th><th>Âge</th><th>Ligue</th><th>Équipe</th><th>PPG</th><th>RPG</th><th>APG</th><th>FG%</th><th>G</th><th>Award</th><th>Événement</th></tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("← Retour au Dashboard", key="btn_back_hist"): st.session_state.screen="dashboard"; st.rerun()

screen = st.session_state.screen
if screen=="home": screen_home()
elif screen=="create": screen_create()
elif screen=="dashboard":
    if not st.session_state.player: st.session_state.screen="home"; st.rerun()
    else: screen_dashboard()
elif screen=="prepare": screen_prepare()
elif screen=="season_result": screen_season_result()
elif screen=="draft": screen_draft()
elif screen=="draft_result": screen_draft_result()
elif screen=="history": screen_history()
else: st.session_state.screen="home"; st.rerun()
