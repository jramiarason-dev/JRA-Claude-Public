import streamlit as st
import anthropic
import json
import os
from datetime import date

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
    /* ---- Global background ---- */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #0d0f14 !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] { background-color: #111318 !important; }

    /* ---- Header / hero ---- */
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
    .hero p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* ---- Form card ---- */
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
        margin-bottom: 1rem;
    }

    /* ---- Inputs ---- */
    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stDateInput"] input {
        background-color: #1e2535 !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 8px !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stSelectbox"] > div > div:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important;
    }
    label { color: #94a3b8 !important; font-size: 0.9rem !important; }

    /* ---- Button ---- */
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

    /* ---- Analysis sections ---- */
    .section-card {
        background: #111827;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.1rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #1e293b;
    }
    .section-icon { font-size: 1.25rem; }

    /* ---- Match header badge ---- */
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
    .match-badge .teams {
        font-size: 1.5rem;
        font-weight: 800;
        color: #f1f5f9;
    }
    .match-badge .meta {
        font-size: 0.85rem;
        color: #93c5fd;
        background: rgba(37,99,235,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
    }

    /* ---- Spinner override ---- */
    [data-testid="stSpinner"] { color: #3b82f6 !important; }

    /* ---- Progress / info ---- */
    .stAlert { border-radius: 10px !important; }
    [data-testid="stExpander"] {
        background: #111827 !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
    }

    /* ---- Separator ---- */
    hr { border-color: #1e293b !important; }

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0d0f14; }
    ::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3b82f6; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sport metadata ────────────────────────────────────────────────────────────
COMPETITIONS = {
    "Ligue 1": {"sport": "football", "icon": "⚽", "country": "France"},
    "Super League Suisse": {"sport": "football", "icon": "⚽", "country": "Suisse"},
    "Champions League": {"sport": "football", "icon": "⚽", "country": "Europe"},
    "Betclic Elite": {"sport": "basketball", "icon": "🏀", "country": "France"},
    "Euroleague": {"sport": "basketball", "icon": "🏀", "country": "Europe"},
    "NBA": {"sport": "basketball", "icon": "🏀", "country": "USA"},
    "Top 14": {"sport": "rugby", "icon": "🏉", "country": "France"},
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
@st.cache_resource
def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY", st.secrets.get("ANTHROPIC_API_KEY", ""))
    if not api_key:
        st.error("Clé API Anthropic manquante. Définissez ANTHROPIC_API_KEY.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


# ── Analysis engine ───────────────────────────────────────────────────────────
def generate_analysis(equipe1: str, equipe2: str, date_match: str, competition: str) -> str:
    client = get_client()
    meta = COMPETITIONS[competition]
    sport = meta["sport"]
    phases = SPORT_PHASES[sport]
    phases_str = "\n".join(f"  - {p}" for p in phases)

    system_prompt = """Tu es un analyste tactique d'élite et entraîneur expert avec 20 ans d'expérience
dans le sport professionnel. Tu fournis des analyses de match ultra-détaillées, précises et professionnelles
en français. Ton style est direct, technique et orienté performance. Tu t'appuies sur des données concrètes
et des observations tactiques précises. Tes analyses sont lues par des coaches professionnels."""

    user_prompt = f"""Effectue une analyse coaching complète et détaillée du match suivant :

**Match :** {equipe1} vs {equipe2}
**Date :** {date_match}
**Compétition :** {competition} ({meta['country']})
**Sport :** {sport}

Commence par rechercher les informations réelles de ce match (score, statistiques, événements clés, compositions d'équipes).

Ensuite, rédige une analyse structurée avec exactement ces sections (utilise des titres Markdown ##) :

## 🔍 Résumé du Match
Score final, contexte, enjeux, ambiance générale et faits marquants.

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

Sois précis, technique et utilise la terminologie professionnelle du {sport}. Tout en français."""

    # Call with web_search tool for real match data
    tools = [
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 5,
        }
    ]

    with st.status("🔍 Recherche des données du match en cours...", expanded=True) as status:
        st.write("Interrogation de l'API Anthropic avec web search...")

        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=[{"role": "user", "content": user_prompt}],
        )

        st.write("Génération de l'analyse tactique...")

        # Collect all text blocks from response
        full_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                full_text += block.text

        status.update(label="✅ Analyse générée !", state="complete", expanded=False)

    return full_text


# ── Section renderer ──────────────────────────────────────────────────────────
SECTION_ICONS = {
    "Résumé": ("🔍", "Résumé du Match"),
    "Formations": ("📋", "Formations & Tactiques"),
    "Phases": ("⚡", "Phases de Jeu"),
    "Performances": ("🌟", "Performances Individuelles"),
    "Points Forts": ("💪", "Points Forts"),
    "Points Faibles": ("⚠️", "Points Faibles"),
    "Coach": ("🧠", "Analyse Coach"),
    "Verdict": ("📊", "Verdict Final CoachIQ"),
}


def render_analysis(text: str, equipe1: str, equipe2: str, competition: str):
    meta = COMPETITIONS[competition]
    # Match header badge
    st.markdown(
        f"""
        <div class="match-badge">
            <span class="teams">{meta['icon']} {equipe1} <span style="color:#3b82f6;">vs</span> {equipe2}</span>
            <span class="meta">{competition} · {meta['country']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Split by ## headers and render each section
    import re
    sections = re.split(r"(?=##\s)", text.strip())
    for section in sections:
        if not section.strip():
            continue
        if section.startswith("##"):
            lines = section.strip().split("\n", 1)
            title = lines[0].replace("##", "").strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            st.markdown(
                f"""
                <div class="section-card">
                    <div class="section-title">{title}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(body)
            st.markdown("---")
        else:
            st.markdown(section)


# ── Main UI ───────────────────────────────────────────────────────────────────
def main():
    # Hero header
    st.markdown(
        """
        <div class="hero">
            <h1>CoachIQ</h1>
            <p>Analyse tactique professionnelle propulsée par l'IA · Tous sports · En français</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Input form ──
    st.markdown('<div class="form-card"><h3>🏟 Saisir un match</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        equipe1 = st.text_input("Équipe 1 (domicile)", placeholder="ex: Paris Saint-Germain")
        equipe2 = st.text_input("Équipe 2 (extérieur)", placeholder="ex: Olympique de Marseille")
    with col2:
        competition = st.selectbox(
            "Compétition",
            options=list(COMPETITIONS.keys()),
            format_func=lambda c: f"{COMPETITIONS[c]['icon']}  {c}",
        )
        date_match = st.date_input(
            "Date du match",
            value=date.today(),
            max_value=date.today(),
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Validation
    ready = equipe1.strip() and equipe2.strip()

    if not ready:
        st.info("Renseignez les deux équipes pour lancer l'analyse.", icon="ℹ️")

    if st.button("🧠 Générer l'analyse CoachIQ", disabled=not ready):
        if equipe1.strip().lower() == equipe2.strip().lower():
            st.error("Les deux équipes doivent être différentes.")
            return

        st.session_state["last_analysis"] = None

        try:
            analysis = generate_analysis(
                equipe1.strip(),
                equipe2.strip(),
                date_match.strftime("%d/%m/%Y"),
                competition,
            )
            st.session_state["last_analysis"] = {
                "text": analysis,
                "equipe1": equipe1.strip(),
                "equipe2": equipe2.strip(),
                "competition": competition,
                "date": date_match.strftime("%d/%m/%Y"),
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

        # Download button
        st.download_button(
            label="⬇️ Télécharger l'analyse (Markdown)",
            data=data["text"],
            file_name=f"CoachIQ_{data['equipe1']}_vs_{data['equipe2']}_{data['date'].replace('/', '-')}.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
