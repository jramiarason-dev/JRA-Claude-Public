import streamlit as st
import anthropic
import os
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CoachIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Dark-mode CSS ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #0d0f14 !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] { background-color: #111318 !important; }

    .hero {
        background: linear-gradient(135deg, #1a1f2e 0%, #0f1722 60%, #0d1a2a 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 2.5rem 2rem 2rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #60a5fa, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -1px;
    }
    .hero p { color: #94a3b8; font-size: 1.1rem; margin-top: 0.5rem; }

    .form-card {
        background: #111827;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
    }
    .form-card h3 {
        color: #60a5fa;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1.25rem;
    }
    .step-label {
        color: #3b82f6;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.25rem;
    }

    [data-testid="stSelectbox"] > div > div {
        background-color: #1e2535 !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 8px !important;
    }
    label { color: #94a3b8 !important; font-size: 0.9rem !important; }

    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(37,99,235,0.35) !important;
    }
    [data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
        box-shadow: 0 6px 20px rgba(59,130,246,0.45) !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="stButton"] > button:disabled {
        background: #1e2535 !important;
        color: #475569 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    .section-card {
        background: #111827;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #1e293b;
    }

    .match-badge {
        background: linear-gradient(135deg, #1e3a5f 0%, #1a2f4a 100%);
        border: 1px solid #2563eb;
        border-radius: 12px;
        padding: 1.25rem 1.75rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .match-badge .teams { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; }
    .match-badge .meta {
        font-size: 0.85rem; color: #93c5fd;
        background: rgba(37,99,235,0.2);
        padding: 0.3rem 0.8rem; border-radius: 20px;
    }
    .divider-step {
        border: none; border-top: 1px solid #1e293b; margin: 1.25rem 0;
    }
    hr { border-color: #1e293b !important; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0d0f14; }
    ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3b82f6; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Data ──────────────────────────────────────────────────────────────────────
COMPETITIONS = {
    "Ligue 1": {"sport": "football", "icon": "⚽", "country": "France"},
    "Super League Suisse": {"sport": "football", "icon": "⚽", "country": "Suisse"},
    "Champions League": {"sport": "football", "icon": "⚽", "country": "Europe"},
    "Betclic Elite": {"sport": "basketball", "icon": "🏀", "country": "France"},
    "Euroleague": {"sport": "basketball", "icon": "🏀", "country": "Europe"},
    "NBA": {"sport": "basketball", "icon": "🏀", "country": "USA"},
    "Top 14": {"sport": "rugby", "icon": "🏉", "country": "France"},
}

TEAMS = {
    "Ligue 1": [
        "Paris Saint-Germain", "Olympique de Marseille", "AS Monaco", "OGC Nice",
        "Stade Rennais", "RC Lens", "LOSC Lille", "Olympique Lyonnais",
        "Montpellier HSC", "RC Strasbourg", "Stade de Reims", "Stade Brestois",
        "FC Nantes", "Le Havre AC", "Toulouse FC", "AJ Auxerre",
        "Angers SCO", "AS Saint-Étienne",
    ],
    "Super League Suisse": [
        "FC Basel", "BSC Young Boys", "Servette FC", "Grasshopper Club",
        "FC Lugano", "FC Zurich", "FC Luzern", "FC Sion",
        "FC St. Gallen", "FC Winterthur", "Lausanne-Sport", "Yverdon-Sport",
    ],
    "Champions League": [
        "Real Madrid", "FC Barcelona", "Manchester City", "Bayern Munich",
        "Paris Saint-Germain", "Liverpool", "Arsenal", "Chelsea",
        "Juventus", "Inter Milan", "AC Milan", "Atletico Madrid",
        "Borussia Dortmund", "Napoli", "Porto", "Benfica",
        "PSV Eindhoven", "Bayer Leverkusen", "RB Leipzig", "Atalanta",
        "Aston Villa", "Club Brugge", "AS Monaco", "LOSC Lille",
        "Celtic", "Sporting CP", "Feyenoord", "Girona",
        "VfB Stuttgart", "Sparta Prague", "Sturm Graz", "BSC Young Boys",
        "Red Star Belgrade", "Shakhtar Donetsk", "Slavia Prague", "Red Bull Salzburg",
    ],
    "Betclic Elite": [
        "LDLC ASVEL", "Paris Basketball", "Monaco Basket", "Cholet Basket",
        "Strasbourg IG", "Boulazac Basket Dordogne", "Limoges CSP", "Nanterre 92",
        "Elan Chalon", "JL Bourg", "Dijon Basketball", "Gravelines-Dunkerque",
        "Le Mans Sarthe Basket", "Metropolitans 92", "Pau-Lacq-Orthez", "Roanne Basket",
        "Blois Basket", "Antibes Sharks",
    ],
    "Euroleague": [
        "Real Madrid", "FC Barcelona", "Fenerbahce Beko", "Olympiacos",
        "Panathinaikos", "Maccabi Tel Aviv", "Anadolu Efes", "Bayern Munich",
        "Alba Berlin", "Zalgiris Kaunas", "Valencia Basket", "Olimpia Milano",
        "LDLC ASVEL", "Monaco Basket", "Virtus Bologna", "Baskonia",
        "Partizan Belgrade", "Red Star Belgrade",
    ],
    "NBA": [
        "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
        "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
        "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
        "LA Clippers", "LA Lakers", "Memphis Grizzlies", "Miami Heat",
        "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
        "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
        "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
        "Utah Jazz", "Washington Wizards",
    ],
    "Top 14": [
        "Stade Toulousain", "Racing 92", "Stade Rochelais", "Union Bordeaux-Bègles",
        "Montpellier Hérault RC", "Stade Français", "Lyon OU", "Clermont Auvergne",
        "Castres Olympique", "Aviron Bayonnais", "Section Paloise", "USA Perpignan",
        "RC Toulon", "Vannes RC",
    ],
}

SPORT_PHASES = {
    "football": [
        "pressing haut / bloc médian",
        "transitions offensives et défensives",
        "phases arrêtées (corners, coups francs, penalties)",
        "construction depuis l'arrière et sorties de balle",
        "organisation défensive (ligne haute vs ligne basse)",
    ],
    "basketball": [
        "pick and roll offensif et défensif",
        "transition rapide (fast break)",
        "isolation et jeu à un contre un",
        "défense de zone vs homme à homme",
        "clutch time et gestion du money time",
    ],
    "rugby": [
        "jeu au sol (ruck, maul) et combat de conquête",
        "phases de touche et mêlées",
        "jeu au pied tactique (up and under, grubber)",
        "défense en ligne / en rideau",
        "maul offensif et défensif",
    ],
}


# ── Anthropic client ──────────────────────────────────────────────────────────
def get_client():
    api_key = ""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("Clé API Anthropic manquante. Ajoutez ANTHROPIC_API_KEY dans les secrets Streamlit.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


# ── Analysis engine ───────────────────────────────────────────────────────────
def generate_analysis(equipe1: str, equipe2: str, competition: str) -> str:
    client = get_client()
    meta = COMPETITIONS[competition]
    sport = meta["sport"]
    phases_str = "\n".join(f"  - {p}" for p in SPORT_PHASES[sport])

    system_prompt = (
        "Tu es un analyste tactique d'élite et entraîneur expert avec 20 ans d'expérience "
        "dans le sport professionnel. Tu fournis des analyses de match ultra-détaillées, précises "
        "et professionnelles en français. Ton style est direct, technique et orienté performance. "
        "Tu t'appuies sur des données concrètes et des observations tactiques précises. "
        "Tes analyses sont lues par des coaches professionnels."
    )

    user_prompt = f"""Tu dois analyser le match le plus récent entre {equipe1} et {equipe2} en {competition}.

**Étape 1 — Recherche du match récent**
Commence par rechercher sur le web : "{equipe1} {equipe2} {competition} résultat 2025"
Trouve le match le plus récent (dernières semaines ou derniers mois) avec :
- La date exacte
- Le score final
- Les buteurs / marqueurs / essayeurs selon le sport
- Les compositions si disponibles

Si aucun match récent n'existe entre ces deux équipes dans cette compétition, indique-le clairement
en introduction puis analyse le match le plus récent disponible ou le dernier affrontement connu.

**Étape 2 — Analyse coaching complète**
Une fois le match identifié, rédige une analyse structurée avec exactement ces sections (titres Markdown ##) :

## 🔍 Résumé du Match
Date, score final, contexte, enjeux, faits marquants. Précise le match analysé en en-tête.

## 📋 Formations et Dispositifs Tactiques
Dispositifs utilisés par chaque équipe, changements de schéma en cours de match, positionnement des joueurs clés.

## ⚡ Phases de Jeu Analysées
Analyse détaillée de chacune de ces phases spécifiques au {sport} :
{phases_str}

## 🌟 Performances Individuelles Clés
Top 3 des performances remarquables par équipe avec statistiques individuelles et impact tactique.

## 💪 Points Forts
**{equipe1} :** Top 4 points forts observés pendant le match.
**{equipe2} :** Top 4 points forts observés pendant le match.

## ⚠️ Points Faibles et Axes d'Amélioration
**{equipe1} :** Failles tactiques et manques observés.
**{equipe2} :** Failles tactiques et manques observés.

## 🧠 Ce que le Coach Aurait Dû Faire Différemment
Pour **{equipe1}** : Décisions tactiques discutables, remplacements ratés, ajustements manqués.
Pour **{equipe2}** : Décisions tactiques discutables, remplacements ratés, ajustements manqués.

## 📊 Verdict Final CoachIQ
Note de performance tactique (/10) pour chaque équipe et conclusion en 3 phrases.

Tout en français. Sois précis et utilise la terminologie professionnelle du {sport}."""

    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 6}]

    with st.status("🔍 Recherche du match récent en cours...", expanded=True) as status:
        st.write(f"Recherche du dernier {equipe1} — {equipe2} en {competition}...")

        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=[{"role": "user", "content": user_prompt}],
        )

        st.write("Génération de l'analyse tactique complète...")

        full_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                full_text += block.text

        status.update(label="✅ Analyse générée !", state="complete", expanded=False)

    return full_text


# ── Section renderer ──────────────────────────────────────────────────────────
def render_analysis(text: str, equipe1: str, equipe2: str, competition: str):
    meta = COMPETITIONS[competition]
    st.markdown(
        f"""
        <div class="match-badge">
            <span class="teams">{meta['icon']} {equipe1} <span style="color:#3b82f6;">vs</span> {equipe2}</span>
            <span class="meta">{competition} · {meta['country']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sections = re.split(r"(?=##\s)", text.strip())
    for section in sections:
        if not section.strip():
            continue
        if section.startswith("##"):
            lines = section.strip().split("\n", 1)
            title = lines[0].replace("##", "").strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            st.markdown(
                f'<div class="section-card"><div class="section-title">{title}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(body)
            st.markdown("---")
        else:
            st.markdown(section)


# ── Main UI ───────────────────────────────────────────────────────────────────
def main():
    st.markdown(
        """
        <div class="hero">
            <h1>CoachIQ</h1>
            <p>Analyse tactique professionnelle propulsée par l'IA · Tous sports · En français</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="form-card"><h3>🏟 Configurer le match</h3>', unsafe_allow_html=True)

    # ── Étape 1 : Championnat ──
    st.markdown('<p class="step-label">① Championnat</p>', unsafe_allow_html=True)
    competition = st.selectbox(
        "Compétition",
        options=list(COMPETITIONS.keys()),
        format_func=lambda c: f"{COMPETITIONS[c]['icon']}  {c}",
        label_visibility="collapsed",
    )

    st.markdown('<hr class="divider-step">', unsafe_allow_html=True)

    # ── Étape 2 : Équipes ──
    st.markdown('<p class="step-label">② Équipes</p>', unsafe_allow_html=True)
    teams = TEAMS[competition]

    col1, col2 = st.columns(2)
    with col1:
        equipe1 = st.selectbox("Équipe 1 (domicile)", options=teams, key="eq1")
    with col2:
        # Exclude the team already selected for eq1
        teams_eq2 = [t for t in teams if t != equipe1]
        equipe2 = st.selectbox("Équipe 2 (extérieur)", options=teams_eq2, key="eq2")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Info ──
    meta = COMPETITIONS[competition]
    st.info(
        f"{meta['icon']} L'IA va rechercher automatiquement le **match le plus récent** "
        f"entre {equipe1} et {equipe2} en {competition} et générer l'analyse.",
        icon=None,
    )

    if st.button("🧠 Rechercher & Analyser le dernier match"):
        st.session_state["last_analysis"] = None
        try:
            analysis = generate_analysis(equipe1, equipe2, competition)
            st.session_state["last_analysis"] = {
                "text": analysis,
                "equipe1": equipe1,
                "equipe2": equipe2,
                "competition": competition,
            }
        except anthropic.APIStatusError as e:
            st.error(f"Erreur API Anthropic : {e.status_code} — {e.message}")
        except Exception as e:
            st.error(f"Erreur inattendue : {e}")

    # ── Render stored analysis ──
    if st.session_state.get("last_analysis"):
        data = st.session_state["last_analysis"]
        st.markdown("## 📄 Analyse Complète")
        render_analysis(data["text"], data["equipe1"], data["equipe2"], data["competition"])

        filename = f"CoachIQ_{data['equipe1'].replace(' ', '_')}_vs_{data['equipe2'].replace(' ', '_')}.md"
        st.download_button(
            label="⬇️ Télécharger l'analyse (Markdown)",
            data=data["text"],
            file_name=filename,
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
