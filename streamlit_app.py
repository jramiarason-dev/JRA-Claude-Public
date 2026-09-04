"""
CoachIQ — Streamlit entry point.

Loads the HTML/React prototype and embeds it full-bleed inside a
Streamlit page. The prototype is a *UI/UX mockup*; back-end logic
(Claude calls, real data feeds) would replace the mocked data in
data.js when wired up.

Cette entrée sert la maquette avec les seules données de `data.js`.
Pour la version alimentée par les données Python (effectifs, compos,
chronologies), lancer `coachiq_app.py`. Les deux partagent le même
gabarit de page via `coachiq_shell`, pour qu'un écran ajouté à l'une
ne manque jamais à l'autre.
"""

import streamlit as st

from coachiq_shell import build_html

# ── Page setup ────────────────────────────────────────────────────
st.set_page_config(
    page_title="CoachIQ — Analyse tactique",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Strip Streamlit chrome — the prototype provides its own shell
st.markdown(
    """
    <style>
      #MainMenu, header, footer { visibility: hidden; height: 0; }
      .block-container {
        padding: 0 !important;
        max-width: 100% !important;
      }
      [data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
      [data-testid="stSidebar"] { display: none; }
      body, .stApp { background: #070b14; }
      iframe { border: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Render full-bleed ────────────────────────────────────────────
# Height is generous so internal scroll happens inside the prototype.
st.iframe(build_html(), height=1400)
